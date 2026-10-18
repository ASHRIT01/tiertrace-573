"""Week-2 go/no-go measure: does the narrative (cause + chronology) of a Part 573 report give a
company, a dated event or a cause that the Component Manufacturer block and the flat file do not?

RULES (deterministic; heuristics, precision UNVERIFIED -- see examples in the report):
 A  COMPANY. A capitalised name ending in a corporate suffix (Inc, LLC, Corp, Corporation, Company, Co,
    Ltd, Limited, GmbH, AG, S.A., LP, Industries, Group, Holdings) appears in cause+chronology and, after
    squashing suffixes, neither equals/contains nor is contained by the filer (PDF header or flat file
    MFGNAME) nor the block supplier name. Names without a corporate suffix are NOT detected, so A under-counts.
 B  DATED EVENT. The chronology contains a date (numeric m/d/y, yyyy-mm-dd, d-Mon-yyyy, 'Month d, yyyy', or 'Month yyyy') that is
    not the flat file's RCDATE, ODATE, BGMAN or ENDMAN.
 C  CAUSE. The PDF cause section has >=40 chars and is not NR (C1), or it is NR/blank but the chronology
    contains a causal cue (C2), AND the flat file's defect summary (DESC_DEFECT) contains no causal cue.
 GAIN = A or B or C.
"""
import json
import re
from datetime import date
from pathlib import Path

from tt.norm.aliases import squash
from tt.parse.block import parse_block, raw_block
from tt.parse.pdf import extract_text
from tt.parse.sections import parse_header, split_sections
from tt.verify.dates import parse_date

SUFFIX = r"(?:Inc\.?|Incorporated|L\.?L\.?C\.?|Corp\.?|Corporation|Company|Co\.|Ltd\.?|Limited|GmbH|AG|S\.A\.|LP|L\.P\.|Industries|Group|Holdings)"
STOP = {"the", "on", "in", "at", "after", "a", "an", "following", "once", "when", "and", "by", "from", "to", "of", "that",
        "this", "its", "their", "our", "with", "for", "as", "which", "also", "then", "since", "during", "all", "any", "each"}
CO_RE = re.compile(rf"((?:[A-Z][\w&'’.\-]*,?\s+){{0,4}}?[A-Z][\w&'’.\-]*)\s*,?\s+({SUFFIX})(?=[\s,.;:)”\"']|$)")
MON = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?"
DATE_RE = re.compile(rf"\b{MON}\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}\b|\b\d{{1,2}}/\d{{1,2}}/\d{{2,4}}\b|\b{MON}\s+\d{{4}}\b"
                     rf"|\b\d{{4}}-\d{{2}}-\d{{2}}\b|\b\d{{1,2}}-{MON}-\d{{4}}\b")
CUE = re.compile(r"root cause|caused by|due to|as a result of|resulted from|attributed to|out[- ]of[- ]spec|non-?conform|"
                 r"not (?:properly|correctly) (?:assembled|installed|adjusted|manufactured|torqued|welded|seated|cured)|"
                 r"improperly (?:assembled|installed|adjusted|manufactured|torqued|welded)", re.I)


def companies(text: str) -> list[str]:
    out = []
    for m in CO_RE.finditer(text):
        words = [w for w in re.split(r"\s+", m[1].strip()) if w]
        while words and words[0].lower().strip(",") in STOP:
            words.pop(0)
        if words:
            out.append(" ".join(words).strip(",") + " " + m[2])
    return out


def _same(a: str, b: str) -> bool:
    a, b = squash(a), squash(b)
    return bool(a and b and (a == b or a in b or b in a))


def narrative_dates(chron: str, flat_dates: set[date]) -> list[str]:
    anchor = date(2100, 1, 1)
    hits = []
    for m in DATE_RE.finditer(chron):
        d = parse_date(m[0], anchor)
        if d and d not in flat_dates:
            hits.append(m[0])
    return hits


def _flatdate(s: str) -> date | None:
    return date(int(s[:4]), int(s[4:6]), int(s[6:8])) if re.fullmatch(r"\d{8}", s or "") else None


def analyse(pdf: Path, flat: dict) -> dict:
    text, _ = extract_text(pdf)
    sec, blk, hdr = split_sections(text), parse_block(raw_block(text)), parse_header(text)
    cause, chron = sec.get("cause", ""), sec.get("chronology", "")
    known = [x for x in (hdr["filer"], flat.get("MFGNAME", ""), blk.name or "") if x]
    A = sorted({c for c in companies(cause + " . " + chron) if not any(_same(c, k) for k in known)})
    fd = {d for d in (_flatdate(flat.get(k, "")) for k in ("RCDATE", "ODATE", "BGMAN", "ENDMAN")) if d}
    B = narrative_dates(chron, fd)
    nr = cause.strip().lower().rstrip(".") in {"", "nr", "n/r", "not reported"}
    c1 = (not nr) and len(cause.strip()) >= 40
    c2 = nr and bool(CUE.search(chron))
    flat_cue = bool(CUE.search(flat.get("DESC_DEFECT", "")))
    C = (c1 or c2) and not flat_cue
    return {"A": A, "B": B, "C1": c1 and not flat_cue, "C2": c2 and not flat_cue, "C": C,
            "gain": bool(A or B or C), "cause": cause[:160], "chron": chron[:160]}


def run(sample_jsonl: Path, pdf_dir: Path, zip_path: Path, n_examples: int = 10, seed: int = 0) -> str:
    import random
    from collections import defaultdict
    from tt.data.flat import load_fields
    rows = [json.loads(l) for l in sample_jsonl.read_text().splitlines()]
    latest = [r for r in rows if r["is_latest"]]
    flat = load_fields(zip_path, {r["campaign"] for r in latest},
                       ["MFGNAME", "RCDATE", "ODATE", "BGMAN", "ENDMAN", "DESC_DEFECT"])
    res = []
    for r in latest:
        a = analyse(pdf_dir / r["url"].rsplit("/", 1)[1], flat.get(r["campaign"], {}))
        res.append({**a, "year": r["year"], "file": r["url"].rsplit("/", 1)[1]})
    by = defaultdict(lambda: defaultdict(int))
    for x in res:
        by[x["year"]]["n"] += 1
        for k in ("A", "B", "C", "gain"):
            by[x["year"]][k] += bool(x[k])
    tot = lambda k: sum(bool(x[k]) for x in res)
    out = ["# Narrative gain (Week-2 go/no-go measure)", "", "Rules (deterministic heuristics; precision UNVERIFIED):", "```", __doc__.split("RULES")[1].split('"""')[0].strip("(); \n"), "```", "",
           f"Of {len(res)} filings: A company {tot('A')}, B dated event {tot('B')}, C cause {tot('C')}, any (GAIN) {tot('gain')}.", "",
           "| year | n | A company | B dated event | C cause | GAIN |", "|---|---|---|---|---|---|"]
    out += [f"| {y} | {v['n']} | {v['A']} | {v['B']} | {v['C']} | {v['gain']} |" for y, v in sorted(by.items())]
    hits = [x for x in res if x["gain"]]
    random.Random(seed).shuffle(hits)
    out += ["", f"## {n_examples} random GAIN examples (seed {seed}; not cherry-picked)", ""]
    for x in hits[:n_examples]:
        out += [f"- **{x['file']}** ({x['year']}): A={x['A'][:3]} B={x['B'][:3]} C1={x['C1']} C2={x['C2']}",
                f"  - cause: {x['cause']!r}", f"  - chronology: {x['chron']!r}"]
    return "\n".join(out)
