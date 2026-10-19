"""Pass A drafting procedure (AI drafter, code-assisted): automatic proposals for S1, S2, C, U and events, then per-filing
corrections from config/claim_overrides.json and config/event_overrides.json. Output: one label record per filing."""
import json
import re
from pathlib import Path

from tt.labels.events import POINTER, build
from tt.maskrecover import classify
from tt.norm.aliases import AliasTable
from tt.parse.block import parse_block, raw_block
from tt.parse.pdf import extract_text
from tt.parse.sections import parse_header, split_sections

GENERIC = re.compile(r"[^.]*\b(?:sub-?suppliers?|suppliers?|vendors?|component manufacturer|their supplier)\b[^.]*\.?", re.I)
UNDETERMINED = re.compile(r"not (?:yet )?(?:been )?determined|still (?:being|under) (?:evaluat|investigat)|under investigation|unknown|root cause is still", re.I)


def _sentence_with(text: str, needle: str) -> str:
    from tt.labeldraft import sentence_end
    c, p = re.sub(r"\s+", " ", text).strip(), 0
    while p < len(c):
        e = max(sentence_end(c, p + 1), p + 1)
        s = c[p:e].strip()
        if needle.lower() in s.lower():
            return s[:300]
        p = e
    return ""


def auto(pdf: Path, overrides_ev: dict | None = None) -> dict:
    t, _ = extract_text(pdf)
    h, s, sr = parse_header(t), split_sections(t), split_sections(t, collapse=False)
    rb = raw_block(t)
    blk = parse_block(rb)
    cause, chron = s.get("cause", ""), s.get("chronology", "")
    narr = cause + " " + chron
    pointer = bool(POINTER.search(chron) and len(chron) < 260) or not chron or chron.strip().lower().rstrip(".") in {"nr", "n/a", "na", "none", "not reported"}
    # S1
    name_line = next((ln.strip() for ln in rb.splitlines() if re.match(r"\s*Name\s*:", ln)), "")
    if blk.name:
        s1 = {"id": "S1", "label": f"Block reports component manufacturer: {blk.name}", "status": "SUPPORTED",
              "quote": re.sub(r"\s+", " ", name_line) if blk.name in name_line else f"Name : {blk.name}", "section": "block"}
    else:
        nr = re.search(r"Name\s*:\s*(NR|N/A|n/a|Not Reported)", rb)
        s1 = {"id": "S1", "label": "Block reports a component manufacturer", "status": "NOT_REPORTED",
              "quote": re.sub(r"\s+", " ", nr.group(0)) if nr else "", "section": "block"}
    # S2
    gen = GENERIC.search(cause) or GENERIC.search(chron)
    gen_q = gen.group(0).strip()[:300] if gen else ""
    gen_sec = "cause" if gen and gen_q in cause else "chronology"
    if blk.name:
        cls, hit = classify(blk.name, narr, AliasTable())
        if cls in ("M1", "M2", "M3", "PARTIAL"):
            needle = hit if cls != "M2" else hit.split()[0]
            qc, qh = _sentence_with(cause, needle), _sentence_with(chron, needle)
            q, sec = (qc, "cause") if qc else (qh, "chronology")
            s2 = {"id": "S2", "label": f"Narrative (cause/chronology) names the supplier: {blk.name}", "status": "SUPPORTED", "quote": q, "section": sec}
        elif gen_q:
            s2 = {"id": "S2", "label": f"Narrative (cause/chronology) names the supplier: {blk.name}", "status": "INSUFFICIENT", "quote": gen_q, "section": gen_sec}
        else:
            s2 = {"id": "S2", "label": f"Narrative (cause/chronology) names the supplier: {blk.name}", "status": "INSUFFICIENT", "quote": s1["quote"], "section": "block"}
    else:
        if gen_q:
            s2 = {"id": "S2", "label": "Narrative (cause/chronology) names the supplier: an unnamed supplier", "status": "INSUFFICIENT", "quote": gen_q, "section": gen_sec}
        else:
            s2 = {"id": "S2", "label": "Narrative (cause/chronology) names the supplier: none named", "status": "NOT_REPORTED", "quote": "", "section": "any"}
    # C
    c0 = cause.strip()
    if c0.lower().rstrip(".") in {"", "nr", "n/r", "n/a", "not reported", "na"}:
        C = {"label": "cause not reported", "status": "NOT_REPORTED", "quote": c0 if c0 else "", "section": "cause"}
    elif UNDETERMINED.search(c0):
        C = {"label": "cause not settled", "status": "INSUFFICIENT", "quote": _sentence_with(c0, UNDETERMINED.search(c0).group(0)) or c0[:300], "section": "cause"}
    else:
        first = re.split(r"(?<=[.!?])\s+", c0)[0]
        C = {"label": "cause stated", "status": "SUPPORTED", "quote": first[:300].rstrip(), "section": "cause"}
    # U
    if s2["status"] == "SUPPORTED":
        U = {"kind": "NAMED", "names": [blk.name], "quote": s2["quote"], "section": s2["section"]}
    elif pointer and not GENERIC.search(cause):
        U = {"kind": "NOT_REPORTED", "names": [], "quote": "", "section": "chronology"}
    elif gen_q:
        U = {"kind": "UNNAMED", "names": [], "quote": gen_q, "section": gen_sec}
    else:
        U = {"kind": "NONE_MENTIONED", "names": [], "quote": "", "section": "any"}
    from tt.kind import kind as _kind, load_groups
    external = bool(blk.name) and _kind(blk.name, h["filer"], load_groups())[0] == "external"
    sups = tuple(x for x in ([blk.name, blk.name.split()[0]] if external else []) if x and len(x) >= 3)
    ev, ex = build(sr.get("chronology", ""), h["filing_date"], overrides_ev or {}, sups)
    return {"file": pdf.name, "filer": h["filer"], "filing_date": str(h["filing_date"]), "claims": [s1, s2], "events": ev,
            "events_excluded": [{"sentence": a, "reason": b} for a, b in ex], "cause": C, "upstream": U}


def apply_claim_overrides(rec: dict, ov: dict) -> dict:
    """ov keys: S1, S2 (dict merged into the claim), cause, upstream (dict merged), note (str)."""
    for c in rec["claims"]:
        if c["id"] in ov:
            c.update(ov[c["id"]])
    for k in ("cause", "upstream"):
        if k in ov:
            rec[k].update(ov[k])
    if "note" in ov:
        rec["note"] = ov["note"]
    return rec


def build_pass_a(selection: list[dict], drafts30: list[dict], pdf_dir: Path, ev_overrides: dict, claim_overrides: dict) -> list[dict]:
    """Pass A for the labelled dev set. Filings already drafted (and adjudicated) keep their S1/S2/cause/upstream/note;
    events are rebuilt for every filing with the shared rules + overrides so all 100 follow one procedure."""
    from tt.parse.block import parse_block, raw_block
    from tt.parse.pdf import extract_text
    from tt.parse.sections import parse_header, split_sections
    prev = {d["file"]: d for d in drafts30}
    out = []
    for s in selection:
        f = s["file"]
        rec = apply_claim_overrides(auto(pdf_dir / f, ev_overrides.get(f, {})), claim_overrides.get(f, {}))
        if f in prev:
            d = prev[f]
            for k in ("claims", "cause", "upstream"):
                rec[k] = d[k]
            rec["note"] = d.get("note", "")
            if f in claim_overrides:
                rec = apply_claim_overrides(rec, claim_overrides[f])
        # normalise older drafts to the current rules: extra claims (e.g. 'C2' mechanism notes) go to the note;
        # an INSUFFICIENT S2 with no narrative reference quotes the block's Name line
        extra = [c for c in rec["claims"] if c["id"] not in ("S1", "S2")]
        if extra:
            rec["claims"] = [c for c in rec["claims"] if c["id"] in ("S1", "S2")]
            rec["note"] = (rec.get("note", "") + " " + " ".join(f"[{c['id']}: {c.get('label', '')}: \"{c.get('quote', '')}\"]" for c in extra)).strip()
        s1 = next(c for c in rec["claims"] if c["id"] == "S1")
        s2 = next(c for c in rec["claims"] if c["id"] == "S2")
        if s2["status"] == "INSUFFICIENT" and not s2.get("quote") and s1["status"] == "SUPPORTED":
            s2["quote"], s2["section"] = s1["quote"], "block"
        rec.update({"year": s["year"], "origin": s["origin"]})
        out.append(rec)
    return out
