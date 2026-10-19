"""Three-pass silver-label protocol helpers: load Pass B, compare A vs B, package disagreements for the Pass C adjudicator,
apply Pass C decisions. Final labels start from Pass A; each disagreement is resolved by Pass C as A, B, NEITHER (with a corrected
label) or CONTESTED (excluded from scoring and counted)."""
import copy
import json
import shutil
from pathlib import Path

from tt.labels.agree import compare
from tt.labels.events import chronology_years
from tt.parse.pdf import extract_text
from tt.parse.sections import parse_header, split_sections


def load_pass(dirs: list[Path], name: str = "passB.json") -> list[dict]:
    out = []
    for d in dirs:
        out += json.loads((d / name).read_text())
    for r in out:   # format-only normalisation: an empty section (used with an empty quote) means "any"
        for c in [*r.get("claims", []), r.get("cause", {}), r.get("upstream", {})]:
            if c.get("section") == "":
                c["section"] = "any"
    return out


def context(files: list[str], pdf_dir: Path) -> dict:
    ctx = {}
    for f in files:
        t, _ = extract_text(pdf_dir / f)
        ctx[f] = (chronology_years(split_sections(t, collapse=False).get("chronology", "")), parse_header(t)["filing_date"])
    return ctx


def number_items(items: list[dict]) -> list[dict]:
    for i, it in enumerate(items, 1):
        it["item_id"] = f"D{i:03d}"
    return items


def package_for_c(items: list[dict], texts_dir: Path, rules: Path, out_root: Path, per_batch: int = 25) -> list[Path]:
    """One directory per batch: texts of the filings involved, the rules, and items.json (both versions per item)."""
    by_file = {}
    for it in items:
        by_file.setdefault(it["file"], []).append(it)
    files = sorted(by_file)
    batches, cur, n = [], [], 0
    for f in files:
        if cur and n + len(by_file[f]) > per_batch:
            batches.append(cur); cur, n = [], 0
        cur.append(f); n += len(by_file[f])
    if cur:
        batches.append(cur)
    dirs = []
    for k, fs in enumerate(batches, 1):
        d = out_root / f"batch_{k}"
        (d / "texts").mkdir(parents=True, exist_ok=True)
        shutil.copy(rules, d / "LABELING_RULES.md")
        its = []
        for f in fs:
            shutil.copy(texts_dir / (f.rsplit(".", 1)[0] + ".txt"), d / "texts")
            for it in by_file[f]:
                its.append({"item_id": it["item_id"], "file": f, "claim": it["claim"], "what_differs": it.get("kind", "status/kind differs"),
                            "version_A": it["A"], "version_B": it["B"]})
        (d / "items.json").write_text(json.dumps(its, indent=1, ensure_ascii=False))
        dirs.append(d)
    return dirs


def _strip(e: dict | None) -> dict | None:
    if e is None:
        return None
    return {k: v for k, v in e.items() if k in ("date_text", "type", "quote", "inherited_date", "entry_quote", "date_inferred", "status", "kind", "names", "name", "section", "id")}


def apply_c(A: list[dict], items: list[dict], decisions: list[dict]) -> tuple[list[dict], dict]:
    """Final labels from Pass A + Pass C decisions. Returns (records, counts)."""
    dec = {d["item_id"]: d for d in decisions}
    recs = {a["file"]: copy.deepcopy(a) for a in A}
    for r in recs.values():
        r.setdefault("contested", [])
    counts = {"A": 0, "B": 0, "NEITHER": 0, "CONTESTED": 0, "missing": 0}
    for it in items:
        d = dec.get(it["item_id"])
        r = recs[it["file"]]
        r.setdefault("contested", [])
        choice = (d or {}).get("decision", "missing")
        counts[choice if choice in counts else "missing"] += 1
        if choice in ("CONTESTED", "missing"):
            r["contested"].append({"item_id": it["item_id"], "claim": it["claim"], "reason": (d or {}).get("reason", "no decision")})
            if it["claim"] == "E" and it["A"] is not None:
                for e in r["events"]:
                    if e is not None and e.get("quote") == it["A"].get("quote") and e.get("type") == it["A"].get("type"):
                        e["contested"] = True
            continue
        if choice == "A":
            continue
        new = it["B"] if choice == "B" else d.get("corrected")
        cl = it["claim"]
        if cl in ("S1", "S2"):
            idx = next(i for i, c in enumerate(r["claims"]) if c["id"] == cl)
            r["claims"][idx] = {**_strip(new), "id": cl, "decided_by": f"C:{choice}"}
        elif cl == "C":
            r["cause"] = {**_strip(new), "decided_by": f"C:{choice}"}
        elif cl == "U":
            r["upstream"] = {**_strip(new), "decided_by": f"C:{choice}"}
        elif cl == "E":
            a_ev = it["A"]
            if a_ev is not None:   # remove A's event
                r["events"] = [e for e in r["events"] if not (e.get("quote") == a_ev.get("quote") and e.get("type") == a_ev.get("type") and e.get("date_text") == a_ev.get("date_text"))]
            if new:                # add the chosen/corrected event
                r["events"].append({**_strip(new), "decided_by": f"C:{choice}"})
    return list(recs.values()), counts


def prepare_gold(records: list[dict], pdf_dir: Path) -> list[dict]:
    """Scoring view of the final silver labels: every scored event gets a `span` (from date_text, with the chronology's year
    context), contested events are dropped, and a contested S2 claim gets status CONTESTED (skipped by the scorer)."""
    from datetime import date
    from tt.labels.dates import parse_span
    ctx = context([r["file"] for r in records], pdf_dir)
    out = []
    for r in records:
        r = copy.deepcopy(r)
        years, fd = ctx[r["file"]]
        evs = []
        for e in r["events"]:
            if e.get("contested"):
                continue
            if not e.get("span") and e.get("date_text") and not e.get("date_inferred"):
                sp = parse_span(e["date_text"], years=years, filing=fd)
                if sp is not None and not sp.inferred:
                    e["span"] = {"start": sp.start.isoformat(), "end": sp.end.isoformat(), "granularity": sp.granularity}
            evs.append(e)
        r["events"] = evs
        for c in r["contested"]:
            if c["claim"] == "S2":
                next(x for x in r["claims"] if x["id"] == "S2")["status"] = "CONTESTED"
        out.append(r)
    return out
