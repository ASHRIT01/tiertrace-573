"""POST HOC, EXPLORATORY: type-ambiguity ceiling. Labeller-vs-labeller event-type agreement (Pass A vs Pass B, existing label files) next to the agent's type
agreement on date-matched accepted claims. No model call, nothing frozen changed.
  python scripts/phase6_type_ceiling.py {testA|testB|unseen}  -> reports/phase_6_type_ceiling_<split>.json
Matching rule = the frozen scorer's rule for a predicted event (tt.eval.diagnose.event_class): an event is 'date-matched' if its date span coarsely overlaps a
non-fuzzy event of the other side in the same filing, and its type 'agrees' if any of those overlapping events has the same type. Dates of both passes are parsed
with the same (guarded) parse_span and the filing's chronology-year context; undated / inferred / unparseable events take no part."""
import json
import os
import sys
from collections import Counter
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
from tt.labels.dates import coarse_overlap
from tt.labels.protocol import context
from tt.parse.block import mask_text


def group(filer: str) -> str:
    f = filer.lower()
    for key, name in (("ford motor", "Ford"), ("jayco", "Jayco"), ("paccar", "PACCAR"), ("fca", "FCA")):
        if key in f:
            return name
    return "other"


def spans(evs, years, fd):
    out = []
    for e in evs:
        if not (e.get("date_text") or "").strip() or e.get("date_inferred"):
            continue
        sp = AM.safe_parse_span(e["date_text"], years=years, filing=fd)
        if sp is not None and not sp.inferred:
            out.append((sp, e["type"]))
    return out


def compare(pred, gold):
    """-> list of (agrees, pred_type, most frequent overlapping gold type) for every date-matched pred event (frozen event_class rule)."""
    res = []
    for sp, t in pred:
        ov = [gt for gs, gt in gold if gs.granularity != "fuzzy" and coarse_overlap(gs, sp)]
        if ov:
            c = Counter(ov); top = sorted(c, key=lambda x: (-c[x], x))[0]
            res.append((t in ov, t, top))
    return res


def main():
    PA = {r["file"]: r for r in json.load(open(f"data/labels/{split}_passA.json"))}
    PB = {r["file"]: r for r in json.load(open(f"data/labels/{split}_passB.json"))}
    gold, docs, raw, blocks = D.load_world()
    files = [l["file"] for l in gold]
    ctx = context(files, Path(os.environ["TT_PDF"]))
    P1, P2 = D.load_preds(os.environ["TT_RUN1"]), D.load_preds(os.environ["TT_RUN2"])
    ex1 = {f: Extraction.model_validate(p["extraction"]) for f, p in P1.items()}
    ex2 = {f: Extraction.model_validate(p["extraction"]) if p.get("extraction") else None for f, p in P2.items()}
    out = {"split": split, "groups": {}, "pairs_AB": Counter(), "pairs_agent": Counter(), "filings": len(files)}
    for l in gold:
        f = l["file"]; d = docs[f]; g = group(d.filer); years, fd = ctx[f]
        a, b = spans(PA[f]["events"], years, fd), spans(PB[f]["events"], years, fd)
        row = out["groups"].setdefault(g, Counter())
        for agrees, t, gt in compare(a, b):
            row["AB_n"] += 1; row["AB_agree"] += agrees
            if not agrees: out["pairs_AB"][" / ".join(sorted((t, gt)))] += 1
        for agrees, t, gt in compare(b, a):
            row["BA_n"] += 1; row["BA_agree"] += agrees
        # agent: accepted run-1 event claims (H1 accepted set), date-matched against the final scoring gold, same rule
        ex = ex1[f]; ys = D.years_of(ex)
        c, ch = (mask_text(d.sections.get(k, ""), blocks[f]) for k in ("cause", "chronology"))
        ev = [x for x in A.decide(ex, ex2[f], Extraction.model_validate(b1(c, ch, d.filer)), d, blocks[f]) if x["kind"] == "E"]
        golds = D.event_spans(l)
        for i, e in enumerate(ex.events):
            if D.event_class(e, l, d, ys) == "ignored" or ev[i]["score"] < 3:
                continue
            sp = D.pred_span(e, d.filing_date, ys)
            if sp is None:
                continue
            ov = [gt for gs, gt in golds if gs.granularity != "fuzzy" and coarse_overlap(gs, sp)]
            if not ov:
                continue
            row["agent_n"] += 1; row["agent_agree"] += e.type in ov
            if e.type not in ov:
                cc = Counter(ov); top = sorted(cc, key=lambda x: (-cc[x], x))[0]
                out["pairs_agent"][" / ".join(sorted((e.type, top)))] += 1
    out["groups"] = {k: dict(v) for k, v in out["groups"].items()}
    out["pairs_AB"], out["pairs_agent"] = dict(out["pairs_AB"]), dict(out["pairs_agent"])
    json.dump(out, open(f"reports/phase_6_type_ceiling_{split}.json", "w"), indent=1)
    tot = Counter()
    for v in out["groups"].values(): tot.update(v)
    print(split, dict(tot))


if __name__ == "__main__":
    main()
