"""Size of the mask-and-recover test set: how often the block-named supplier also appears in the
narrative (cause + chronology)?  Rules (deterministic):
 M1 exact   : the block supplier name, normalised (NFKC, lowercase, whitespace), is a substring of the narrative.
 M2 squash  : the name with corporate suffixes and punctuation removed (e.g. 'zf', 'allison transmission') occurs
              as whole words in the narrative squashed the same way (>= 2 chars).
 M3 alias   : any alias-table alias with the same parent id occurs as in M2.
 SELF       : (checked first) component_manufacturer_kind == filer_itself (tt/kind.py: equal after squashing and singularising);
              excluded from the task. Foreign-parent / regional / group-member names (kind == filer_affiliate) STAY in the
              task and are reported separately.
 M4 partial : (reported separately) only the first significant word of the squashed name (>= 4 chars) occurs
              as a whole word, e.g. 'Allison' for 'Allison Transmission Inc.'.
EXTRACTIVE = M1 or M2 or M3. PARTIAL-ONLY = M4 and not EXTRACTIVE. The rest are INFERENTIAL (name absent).
Masking for the task must remove all of M1-M4 occurrences in every section the model sees."""
import json
import random
import re
from collections import defaultdict
from pathlib import Path

from tt.kind import kind as ckind, load_groups
from tt.norm.aliases import AliasTable, squash
from tt.parse.block import parse_block, raw_block
from tt.parse.pdf import extract_text
from tt.parse.sections import norm, parse_header, split_sections


def _words_in(sq_needle: str, sq_text: str) -> bool:
    return len(sq_needle) >= 2 and f" {sq_needle} " in f" {sq_text} "


def classify(name: str, narrative: str, aliases: AliasTable) -> tuple[str, str]:
    """-> (class, matched string). class in EXTRACTIVE_M1/M2/M3, PARTIAL, INFERENTIAL."""
    if norm(name) in norm(narrative):
        return "M1", name
    sq, st = squash(name), squash(narrative)
    if _words_in(sq, st):
        return "M2", sq
    a = aliases.resolve(name)
    if a:
        for key, v in aliases._map.items():
            if v.parent_id == a.parent_id and _words_in(key, st):
                return "M3", key
    first = sq.split()[0] if sq.split() else ""
    if len(first) >= 4 and _words_in(first, st):
        return "PARTIAL", first
    return "INFERENTIAL", ""


def run(sample_jsonl: Path, pdf_dir: Path, aliases: AliasTable, n_examples: int = 10, seed: int = 0) -> str:
    rows = [json.loads(l) for l in sample_jsonl.read_text().splitlines() if '"is_latest": true' in l]
    groups = load_groups()
    res = []
    for r in rows:
        f = r["url"].rsplit("/", 1)[1]
        text, _ = extract_text(pdf_dir / f)
        blk, sec = parse_block(raw_block(text)), split_sections(text)
        if not blk.name:
            res.append({"year": r["year"], "file": f, "cls": "NO_NAME"})
            continue
        narr = sec.get("cause", "") + " . " + sec.get("chronology", "")
        filer = parse_header(text)["filer"]
        ck, why = ckind(blk.name, filer, groups)
        if ck == "filer_itself":
            res.append({"year": r["year"], "file": f, "cls": "SELF", "name": blk.name, "filer": filer})
            continue
        cls, hit = classify(blk.name, narr, aliases)
        i = norm(narr).find(norm(hit)) if hit else -1
        res.append({"year": r["year"], "file": f, "cls": cls, "name": blk.name, "hit": hit, "kind": ck, "why": why, "filer": filer,
                    "ctx": norm(narr)[max(0, i - 70): i + len(hit) + 70] if i >= 0 else "",
                    "in_defect": bool(hit) and norm(hit) in norm(sec.get("defect", ""))})
    by = defaultdict(lambda: defaultdict(int))
    for x in res:
        by[x["year"]][x["cls"]] += 1
        by[x["year"]]["n"] += 1
    ext = lambda c: c in ("M1", "M2", "M3")
    named = [x for x in res if x["cls"] not in ("NO_NAME", "SELF")]
    n_ext = sum(ext(x["cls"]) for x in named)
    out = ["# Mask-and-recover test-set size", "", "Rules:", "```", __doc__.split("Rules (deterministic):")[1].strip(), "```", "",
           f"Of {len(res)} filings: {sum(x['cls'] == 'NO_NAME' for x in res)} have no supplier name in the block, "
           f"{sum(x['cls'] == 'SELF' for x in res)} name the filer itself, {len(named)} name a different company.",
           f"Among those {len(named)}: **extractive {n_ext}** (name in cause/chronology), partial-only "
           f"{sum(x['cls'] == 'PARTIAL' for x in named)}, **inferential {sum(x['cls'] == 'INFERENTIAL' for x in named)}** (name absent from cause/chronology).",
           f"Alias-table matches (M3): {sum(x['cls'] == 'M3' for x in named)} (the seed table has only 5 aliases, so M3 is a floor).", "",
           "| year | filings | no block name | block = filer | extractive (M1-M3) | partial only | inferential |", "|---|---|---|---|---|---|---|"]
    for y, v in sorted(by.items()):
        out.append(f"| {y} | {v['n']} | {v['NO_NAME']} | {v['SELF']} | {v['M1'] + v['M2'] + v['M3']} | {v['PARTIAL']} | {v['INFERENTIAL']} |")
    ext_k = [x for x in named if x["kind"] == "external"]
    aff_k = [x for x in named if x["kind"] == "filer_affiliate"]
    split = lambda xs: (sum(ext(x["cls"]) for x in xs), sum(x["cls"] == "PARTIAL" for x in xs), sum(x["cls"] == "INFERENTIAL" for x in xs))
    out += ["", "By kind (extractive / partial-only / inferential):", "",
            f"- external ({len(ext_k)}): {split(ext_k)[0]} / {split(ext_k)[1]} / {split(ext_k)[2]}",
            f"- filer_affiliate ({len(aff_k)}): {split(aff_k)[0]} / {split(aff_k)[1]} / {split(aff_k)[2]}"]
    # reconcile with the earlier looser rule (containment on un-singularised squashed names)
    withnames = [x for x in res if x["cls"] != "NO_NAME"]
    contains = lambda x: (lambda a, b: bool(a and b and (a == b or a in b or b in a)))(squash(x["name"]), squash(x["filer"]))
    old_self = [x for x in withnames if contains(x)]
    moved_out = [x for x in old_self if x["cls"] != "SELF"]
    moved_in = [x for x in withnames if x["cls"] == "SELF" and not contains(x)]
    out += ["", f"## Reconciliation: earlier report said {len(old_self)} 'block = filer'; now {sum(x['cls'] == 'SELF' for x in res)}", "",
            f"Earlier rule: squashed name contained in / containing the filer name. Now: equal after squashing and singularising tokens. {len(old_self)} - {len(moved_out)} + {len(moved_in)} = {sum(x['cls'] == 'SELF' for x in res)}.", "",
            f"Moved OUT of 'filer itself' (kind = filer_affiliate; they stay in the task): {len(moved_out)}"]
    out += [f"- {x['file']}: filer `{x['filer']}` vs block `{x['name']}` ({x['why']})" for x in moved_out]
    out += ["", "Of these, 7 are a foreign parent / regional entity (Volvo Car Corporation, Volkswagen AG, Mercedes-Benz AG x4, Jaguar Land Rover Limited) and 1 (Blue Bird) is probably the same entity (known miss of the containment rule).",
            "", f"Moved IN to 'filer itself' (singular/plural variant): {len(moved_in)}"]
    out += [f"- {x['file']}: filer `{x['filer']}` vs block `{x['name']}`" for x in moved_in]
    pool = [x for x in named if x["cls"] != "INFERENTIAL"]
    random.Random(seed).shuffle(pool)
    out += ["", f"## {n_examples} random examples of the name ALSO appearing in the narrative (seed {seed})", ""]
    for x in pool[:n_examples]:
        out.append(f"- **{x['file']}** ({x['year']}) block name `{x['name']}` -> {x['cls']} match `{x['hit']}`; also in defect section: {x['in_defect']}\n  - ...{x['ctx']}...")
    return "\n".join(out)
