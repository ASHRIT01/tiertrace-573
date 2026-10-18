"""Hand-check sheet: parsed fields next to verbatim source text, for human comparison.
Read-only: the parser must not be tuned on these filings."""
import json
import random
import re
from pathlib import Path

from tt.parse.block import parse_block, raw_block
from tt.parse.pdf import extract_text
from tt.parse.sections import clean, parse_header, split_sections


def _window(text: str, pat: str, n: int) -> str:
    m = re.search(pat, text, re.I | re.M)
    return text[m.start(): m.start() + n] if m else "(heading not found in text)"


def build(sample_jsonl: Path, pdf_dir: Path, exclude: Path, per_year: int = 4, seed: int = 0, total: int = 50) -> str:
    skip = {l.strip() for l in exclude.read_text().splitlines() if l.strip() and not l.startswith("#")}
    rows = [json.loads(l) for l in sample_jsonl.read_text().splitlines()]
    latest = [r for r in rows if r["is_latest"] and r["url"].rsplit("/", 1)[1] not in skip]
    rng = random.Random(seed)
    out = ["# Hand-check sheet", "",
           f"{per_year} filings per year plus random top-up to {total} (seed {seed}), latest version, excluding {len(skip)} filings opened during development.",
           "Compare PARSED against the PDF. Mark each field OK / WRONG. Do not ask for parser changes tuned to these files.", ""]
    n = 0
    chosen, rest = [], []
    for y in range(2015, 2027):
        pick = [r for r in latest if r["year"] == y]
        rng.shuffle(pick)
        chosen += pick[:per_year]
        rest += pick[per_year:]
    rng.shuffle(rest)
    chosen += rest[: max(0, total - len(chosen))]  # top up to `total` with random extras
    chosen.sort(key=lambda r: (r["year"], r["campaign"]))
    if True:
        for r in chosen:
            y = r["year"]
            n += 1
            f = r["url"].rsplit("/", 1)[1]
            raw, _ = extract_text(pdf_dir / f)
            t = clean(raw)
            h, s, b = parse_header(raw), split_sections(raw), parse_block(raw_block(raw))
            out += [f"## {n}. {f}  ({y}, {r['type']})", f"File: `{pdf_dir / f}`", "",
                    "| field | PARSED | SOURCE (verbatim window) |", "|---|---|---|",
                    f"| filer | {h['filer']!r} | `{_window(raw, r'Manufacturer Name', 80)!r}` |",
                    f"| filing date | {h['filing_date']} | `{_window(raw, r'Submission Date', 40)!r}` |",
                    f"| supplier name | {b.name!r} | `{raw_block(raw)[:220]!r}` |",
                    f"| tier | {b.tier!r} | `{_window(raw, r'Tier of Supplier', 60)!r}` |",
                    f"| cause | {s.get('cause', '')[:200]!r} | `{_window(t, r'Description of the Cause', 300)!r}` |",
                    f"| chronology (start) | {s.get('chronology', '')[:200]!r} | `{_window(t, r'^[ \\t]*Chronology', 300)!r}` |", ""]
    return "\n".join(out)
