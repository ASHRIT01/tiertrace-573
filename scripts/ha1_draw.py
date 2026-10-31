"""HA-1 sample draw (no model run; read-only use of the run outputs and the frozen gate). Rebuilds the 536 accepted Test-A event claims with the construction of
scripts/phase6_testA_exploratory.py, then draws the audit sample. The draw never reads a silver verdict: each item's verdict is left out of `pop` before sampling.
Run from the checkout that holds the uncommitted data (runs/, data/):
  python <worktree>/scripts/ha1_draw.py   -> <worktree>/reports/ha1/HA1_SAMPLE.json"""
import hashlib
import json
import os
import random
import sys
from pathlib import Path

os.environ.setdefault("TT_PDF", "data/testA_raw"); os.environ.setdefault("TT_GOLD", "data/labels/testA_silver.json")
os.environ.setdefault("TT_CACHE", "runs/testA_cache.pkl"); os.environ.setdefault("TT_RUN1", "runs/testA_4b_v2_run1.jsonl")
os.environ.setdefault("TT_RUN2", "runs/testA_4b_v2_run2.jsonl")

import tt.eval.amend1 as AM
AM.install()
from tt.agent import agent as A
from tt.agent.schemas import Extraction
from tt.baselines.rules import b1
from tt.eval import diagnose as D
from tt.parse.block import mask_text

SEED, N_FILINGS, N_REPEATS, N_POP = 7, 40, 8, 536
OUT = Path(__file__).resolve().parents[1] / "reports" / "ha1"
INPUTS = ["runs/testA_4b_v2_run1.jsonl", "runs/testA_4b_v2_run2.jsonl", "data/labels/testA_silver.json", "runs/testA_cache.pkl", "docs/LABELING_RULES.md"]


def accepted_claims():
    """-> [(silver_ok, silver_class, file, event_index)] for the accepted event claims, in filing and run-1 order. Same construction as the H1 accepted set."""
    gold, docs, raw, blocks = D.load_world()
    P1, P2 = D.load_preds(os.environ["TT_RUN1"]), D.load_preds(os.environ["TT_RUN2"])
    ex1 = {f: Extraction.model_validate(p["extraction"]) for f, p in P1.items()}
    ex2 = {f: Extraction.model_validate(p["extraction"]) if p.get("extraction") else None for f, p in P2.items()}
    dec = {}
    for l in gold:
        f = l["file"]; d = docs[f]
        c, ch = (mask_text(d.sections.get(k, ""), blocks[f]) for k in ("cause", "chronology"))
        dec[f] = A.decide(ex1[f], ex2[f], Extraction.model_validate(b1(c, ch, d.filer)), d, blocks[f])
    key = {(f, x["kind"], id(x["ref"]) if x["ref"] is not None else None): x for f, xs in dec.items() for x in xs}
    index = {id(e): i for ex in ex1.values() for i, e in enumerate(ex.events)}
    sf = lambda kind, ex, claim, f: (lambda x: (f, index.get(id(claim)), not x["reasons"], bool(x["agree2"]), x["accepted"]))(key[(f, kind, id(claim) if claim is not None else None)])
    items, _ = AM.items_for(gold, docs, ex1, sf)
    out = [(ok, f, i) for ok, (f, i, noreason, agree, acc), _cl in items["E"] if noreason and agree and acc]
    return out, ex1, docs, blocks


def draw(pop):
    """pop: [(file, event_index)] in filing and run-1 order. The whole random draw, one generator: filings, then one claim per filing, then the repeats."""
    by = {}
    for f, i in pop:
        by.setdefault(f, []).append(i)
    frame = sorted(by)
    rng = random.Random(SEED)
    filings = rng.sample(frame, N_FILINGS)
    items = [(f, rng.choice(sorted(by[f]))) for f in filings]
    repeats = rng.sample(range(N_FILINGS), N_REPEATS)
    rng.shuffle(repeats)
    return frame, by, items, repeats


def main():
    acc, ex1, docs, blocks = accepted_claims()
    assert len(acc) == N_POP, f"accepted set is {len(acc)}, not {N_POP}"
    pop = [(f, i) for _ok, f, i in acc]
    assert len(set(pop)) == N_POP
    frame, by, items, repeats = draw(pop)
    assert draw(pop)[2:] == (items, repeats)
    located = sum(D.qfound(ex1[f].events[i].evidence.quote, docs[f].sections.get(ex1[f].events[i].evidence.section, "")) or "[MASKED]" in ex1[f].events[i].evidence.quote for f, i in pop)
    sections = sorted({ex1[f].events[i].evidence.section for f, i in pop})
    R = {"protocol": "reports/HA_PROTOCOL.md", "seed": SEED, "population_claims": N_POP, "frame_filings": len(frame),
         "accepted_claims_per_frame_filing": {f: len(by[f]) for f in frame},
         "input_sha256": {p: hashlib.sha256(open(p, "rb").read()).hexdigest() for p in INPUTS},
         "items": [{"item": f"HA-{n + 1:02d}", "file": f, "event_index": i, "repeat_of": None} for n, (f, i) in enumerate(items)]
                  + [{"item": f"HA-{N_FILINGS + n + 1:02d}", "file": items[j][0], "event_index": items[j][1], "repeat_of": f"HA-{j + 1:02d}"} for n, j in enumerate(repeats)]}
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(R, open(OUT / "HA1_SAMPLE.json", "w"), indent=1)
    print(f"population {N_POP}; frame filings {len(frame)}; items {len(R['items'])}; quotes located {located}; evidence sections {sections}; claims per filing min {min(map(len, by.values()))} max {max(map(len, by.values()))}")


if __name__ == "__main__":
    main()
