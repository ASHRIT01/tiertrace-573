import re
from collections import defaultdict
from pathlib import Path

from tt.parse.block import parse_block, raw_block
from tt.parse.layout import detect_layout
from tt.parse.pdf import extract_text
from tt.parse.sections import parse_header, split_sections

_NAME_NR = re.compile(r"(?im)^\s*Name\s*:\s*(?:n/?r|not reported)\s*$")


def check_pdf(path: Path) -> dict:
    """`fails` are parser problems; `info` are facts about the filing (e.g. block says NR)."""
    fails, info = [], []
    try:
        text, empty = extract_text(path)
    except Exception as e:
        return {"file": path.name, "layout": "unreadable", "fails": [f"unreadable: {e.__class__.__name__}"], "info": []}
    if empty:
        fails.append("no_text_layer")
    h, s = parse_header(text), split_sections(text)
    rb = raw_block(text)
    b = parse_block(rb)
    if not h["filer"]: fails.append("no_filer")
    if not h["filing_date"]: fails.append("no_filing_date")
    if not h["campaign"]: fails.append("no_campaign")
    if "cause" not in s: fails.append("no_cause_heading")
    if not s.get("chronology"): fails.append("no_chronology")
    if not rb.strip():
        fails.append("no_block_section")
    elif not b.name:
        # 'Name : NR' is the filing reporting no supplier, not a parser miss
        if _NAME_NR.search(rb):
            info.append("block_name_NR")
        elif not (b.tier or b.type or b.country):
            info.append("block_blank")  # labels present, no values: the filer left the block empty
        else:
            fails.append("no_block_name")
    return {"file": path.name, "layout": detect_layout(text), "fails": fails, "info": info}


def build_report(folder: Path) -> str:
    rows = [check_pdf(p) for p in sorted(folder.iterdir())
            if p.suffix.lower() == ".pdf" and not p.name.startswith(".")]
    by = defaultdict(list)
    for r in rows:
        by[r["layout"]].append(r)
    nr = sum("block_name_NR" in r["info"] for r in rows)
    blank = sum("block_blank" in r["info"] for r in rows)
    out = ["# Parse report", "", f"{len(rows)} PDFs; {sum(not r['fails'] for r in rows)} parsed with no flagged field.",
           f"{nr} filings have a supplier block whose Name is NR and {blank} have a blank block (filing's own content; not counted as failures).", "",
           "| layout | files | with failures |", "|---|---|---|"]
    out += [f"| {k} | {len(v)} | {sum(bool(r['fails']) for r in v)} |" for k, v in sorted(by.items())]
    bad = [r for r in rows if r["fails"]]
    if bad:
        out += ["", "## Failures", ""] + [f"- {r['file']} ({r['layout']}): {', '.join(r['fails'])}" for r in bad]
    return "\n".join(out)
