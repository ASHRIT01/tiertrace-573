"""Audit of the sampled filings: download/text-layer/OCR need and field fill rates by year."""
import json
from collections import defaultdict
from pathlib import Path

from tt.parse.block import parse_block, raw_block
from tt.parse.layout import detect_layout
from tt.parse.pdf import extract_text
from tt.parse.sections import parse_header, split_sections


def audit(sample_jsonl: Path, pdf_dir: Path) -> str:
    rows = [json.loads(l) for l in sample_jsonl.read_text().splitlines()]
    latest = [r for r in rows if r["is_latest"]]
    stat = defaultdict(lambda: defaultdict(int))
    layouts = defaultdict(int)
    for r in latest:
        y, s = r["year"], stat[r["year"]]
        s["campaigns"] += 1
        s["multi"] += r["n_versions"] > 1
        p = pdf_dir / r["url"].rsplit("/", 1)[1]
        if not p.exists():
            s["download_failed"] += 1
            continue
        try:
            text, empty = extract_text(p)
        except Exception:
            s["unreadable"] += 1
            continue
        s["downloaded"] += 1
        s["needs_ocr"] += bool(empty)
        s["has_text"] += not empty
        sec, blk = split_sections(text), parse_block(raw_block(text))
        layouts[detect_layout(text)] += 1
        s["filer"] += bool(parse_header(text)["filer"])
        s["supplier_name"] += bool(blk.name)
        s["tier"] += bool(blk.tier)
        s["cause"] += sec.get("cause", "").strip().lower() not in {"", "nr", "n/r", "not reported"}
        s["chronology"] += bool(sec.get("chronology"))
    ys = sorted(stat)
    pct = lambda n, d: f"{100 * n / d:.0f}%" if d else "-"
    out = ["# Audit (latest 573 version per sampled campaign)", "",
           f"{len(latest)} campaigns with a 573 report; {sum(stat[y]['multi'] for y in ys)} have several versions.", "",
           "## Downloads and text layer", "", "| year | campaigns | several versions | downloaded | failed | text layer | needs OCR |", "|---|---|---|---|---|---|---|"]
    out += [f"| {y} | {stat[y]['campaigns']} | {stat[y]['multi']} | {stat[y]['downloaded']} | {stat[y]['download_failed'] + stat[y]['unreadable']} | {stat[y]['has_text']} | {stat[y]['needs_ocr']} |" for y in ys]
    out += ["", "## Field fill rate among downloaded filings (parser-detected; NR counts as unfilled)", "",
            "| year | n | supplier name | tier | cause | chronology |", "|---|---|---|---|---|---|"]
    out += [f"| {y} | {stat[y]['downloaded']} | " + " | ".join(pct(stat[y][k], stat[y]['downloaded']) for k in ("supplier_name", "tier", "cause", "chronology")) + " |" for y in ys]
    out += ["", f"Layouts detected: {dict(layouts)}"]
    return "\n".join(out)
