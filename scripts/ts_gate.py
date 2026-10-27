"""TS-1: read-only extraction of the frozen gate decisions for run-1 event claims (no model call, nothing frozen changed).
  python scripts/ts_gate.py {testA|testB|unseen}  -> runs/ts/<split>_agent_events.json  (gitignored: it holds recall numbers)
Same machinery as the H1 accepted set: amendment-1 wrapper installed, frozen agent.decide on run 1 with run 2 as the agreement filter;
a claim is ACCEPTED iff its rank score >= 3 (no verifier fired and run 2 agrees). Run-2 records without an extraction (Test-A: 4 timeouts)
make run 2 'not agree', exactly as in the frozen scoring."""
import json
import os
import sys
from pathlib import Path

SPLITS = {"testA": ("data/testA_raw", "data/labels/testA_silver.json", "runs/testA_cache.pkl", "runs/testA_4b_v2_run1.jsonl", "runs/testA_4b_v2_run2.jsonl"),
          "testB": ("data/testB_raw", "data/labels/testB_silver.json", "runs/testB_cache.pkl", "runs/testB_4b_v2_run1.jsonl", "runs/testB_4b_v2_run2.jsonl"),
          "unseen": ("data/unseen_raw", "data/labels/unseen_silver.json", "runs/unseen_cache.pkl", "runs/unseen_4b_v2_run1.jsonl", "runs/unseen_4b_v2_run2.jsonl")}
split = sys.argv[1]
os.environ["TT_PDF"], os.environ["TT_GOLD"], os.environ["TT_CACHE"], os.environ["TT_RUN1"], os.environ["TT_RUN2"] = SPLITS[split]
import tt.eval.amend1 as AM
AM.install()
from tt.agent import agent as A
from tt.agent.schemas import Extraction
from tt.baselines.rules import b1
from tt.eval import diagnose as D
from tt.parse.block import mask_text


def main():
    gold, docs, raw, blocks = D.load_world()
    P1, P2 = D.load_preds(os.environ["TT_RUN1"]), D.load_preds(os.environ["TT_RUN2"])
    out = {}
    for l in gold:
        f = l["file"]; d = docs[f]
        p1 = P1.get(f)
        if not p1 or not p1.get("extraction"):
            out[f] = {"run1_valid": False, "events": []}
            continue
        ex = Extraction.model_validate(p1["extraction"])
        p2 = P2.get(f)
        ex2 = Extraction.model_validate(p2["extraction"]) if p2 and p2.get("extraction") else None
        c, ch = (mask_text(d.sections.get(k, ""), blocks[f]) for k in ("cause", "chronology"))
        dec = [x for x in A.decide(ex, ex2, Extraction.model_validate(b1(c, ch, d.filer)), d, blocks[f]) if x["kind"] == "E"]
        assert len(dec) == len(ex.events)
        out[f] = {"run1_valid": True, "run2_valid": ex2 is not None,
                  "events": [{"date_text": e.date_text or "", "type": e.type, "quote": e.evidence.quote if e.evidence else "",
                              "score": dec[i]["score"], "accepted": dec[i]["score"] >= 3} for i, e in enumerate(ex.events)]}
    Path("runs/ts").mkdir(parents=True, exist_ok=True)
    json.dump(out, open(f"runs/ts/{split}_agent_events.json", "w"), indent=1)
    print(split, len(out), "filings;", sum(len(v["events"]) for v in out.values()), "run-1 events;",
          sum(e["accepted"] for v in out.values() for e in v["events"]), "accepted")


if __name__ == "__main__":
    main()
