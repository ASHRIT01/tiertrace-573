"""Build an adjudication sheet from two AI label sets: every difference, plus a random sample of items where they agreed.
Nothing is pre-marked. A = reference drafts, B = blind labels."""
import random
from pathlib import Path

from tt.eval.compare_labels import compare
from tt.labeldraft import load

CHECK = "[ ] A right   [ ] B right   [ ] neither: ________________"
SECTIONS = {"S1": ("block",), "S2": ("cause", "chronology"), "E": ("chronology",), "C": ("cause",), "U": ("cause", "chronology")}


def _val(t: str, x: dict | None) -> list[tuple[str, str]]:
    if x is None:
        return [("value", "(none: no such item in this set)")]
    if t == "E":
        return [("date_text", x["date_text"]), ("type", x["type"]), ("quote", x["quote"])]
    if t == "U":
        return [("kind", x["kind"]), ("names", ", ".join(x.get("names") or []) or "(none)"), ("quote", x.get("quote") or "(none)")]
    return [("status", x["status"]), ("quote", x.get("quote") or "(none)")]


def _item(num: int, row, dn: dict, pdf_dir: Path, a_name: str, b_name: str) -> list[str]:
    t, f, verdict, why, a, b = row
    d = load(pdf_dir / f)
    va, vb = _val(t, a), _val(t, b)
    fields = [k for k, _ in va] if a is not None else [k for k, _ in vb]
    out = [f"### Item {num}: claim {t} on draft #{dn[f]} ({f})", f"What differs (mechanical): {'; '.join(why) if why else 'nothing; both passes gave the same value'}", "",
           "| field | A (draft) | B (blind) |", "|---|---|---|"]
    da, db = dict(va), dict(vb)
    for k in dict.fromkeys(fields + [k for k, _ in vb]):
        out.append(f"| {k} | {da.get(k, '(none)')} | {db.get(k, '(none)')} |".replace("\n", " "))
    out.append("")
    for sec in SECTIONS[t]:
        body = d["sections"].get(sec, "") or "(empty)"
        out += [f"PDF section `{sec}`:", "", "```", body[:3500] + (" [...]" if len(body) > 3500 else ""), "```", ""]
    out += [CHECK, ""]
    return out


def build(a_labels: list[dict], b_labels: list[dict], pdf_dir: Path, a_name: str, b_name: str, n_agree: int = 10, seed: int = 0) -> str:
    res = compare(a_labels, b_labels)
    dn = {d["file"]: i + 1 for i, d in enumerate(a_labels)}
    diffs = [r for r in res["rows"] if r[2] != "same"]
    same = [r for r in res["rows"] if r[2] == "same"]
    random.Random(seed).shuffle(same)
    agreed = same[:n_agree]
    out = ["# Adjudication sheet (nothing is marked)", "",
           f"A = {a_name}; B = {b_name}. Both sets were produced by AI. For each item mark exactly one box. The PDF section is the text the labels were drawn from.",
           f"Part 1: the {len(diffs)} items where A and B differ. Part 2: {len(agreed)} items drawn at random (seed {seed}) from the {len(same)} where they agreed, so you can see how the sheet looks when both passes are the same.",
           f"Filings covered: {', '.join('#%d' % dn[f] for f in sorted({r[1] for r in res['rows']}, key=lambda f: dn[f]))}.", "",
           "## Part 1: differences", ""]
    n = 0
    for r in diffs:
        n += 1
        out += _item(n, r, dn, pdf_dir, a_name, b_name)
    out += ["## Part 2: agreed items (random sample)", ""]
    for r in agreed:
        n += 1
        out += _item(n, r, dn, pdf_dir, a_name, b_name)
    return "\n".join(out)
