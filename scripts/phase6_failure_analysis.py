"""POST HOC, EXPLORATORY failure analysis of event claims (silver labels, not human-verified, not a result). Existing outputs and the frozen scorer
machinery only (amendment-1 wrapper, primary settings); no model run, nothing frozen changed.
  python scripts/phase6_failure_analysis.py {testA|testB|unseen}  -> reports/phase_6_failure_analysis_<split>.json
Mismatch classes are assigned by code, in this order, for every ACCEPTED event claim scored wrong:
  (iv)  duplicate: an earlier accepted claim in the same filing has the same event type and the same normalised evidence quote (dates and digits removed);
  (i)   not duplicate; the date matches a scored gold event of that filing (coarse overlap) but the type differs;
  (ii)  the type matches a scored gold event of that filing but no gold event of that type has a matching date;
  (iii) neither date nor type matches a scored gold event; sub-flag iii_undated_same_type = the filing has an unscored (undated) gold event of the same type;
  (v)   the claim's own date text cannot be parsed (frozen class wrong:date_unparsed) - not in the requested list, needed so the classes add up."""
import json
import os
import re
import sys

SPLITS = {"testA": ("data/testA_raw", "data/labels/testA_silver.json", "runs/testA_cache.pkl", "runs/testA_4b_v2_run1.jsonl", "runs/testA_4b_v2_run2.jsonl"),
          "testB": ("data/testB_raw", "data/labels/testB_silver.json", "runs/testB_cache.pkl", "runs/testB_4b_v2_run1.jsonl", "runs/testB_4b_v2_run2.jsonl"),
          "unseen": ("data/unseen_raw", "data/labels/unseen_silver.json", "runs/unseen_cache.pkl", "runs/unseen_4b_v2_run1.jsonl", "runs/unseen_4b_v2_run2.jsonl")}
split = sys.argv[1]
os.environ["TT_PDF"], os.environ["TT_GOLD"], os.environ["TT_CACHE"], os.environ["TT_RUN1"], os.environ["TT_RUN2"] = SPLITS[split]
from collections import Counter, defaultdict

import tt.eval.amend1 as AM
AM.install()
from tt.agent import agent as A
from tt.agent.schemas import Extraction
from tt.baselines.rules import b1
from tt.eval import diagnose as D
from tt.labels.dates import coarse_overlap
from tt.labels.events import DATE_FIND, sentences
from tt.parse.block import mask_text
from tt.eval.riskcov import cluster_bootstrap

NORM_DROP = re.compile(r"[^a-z ]")


def normsent(s: str) -> str:
    s = DATE_FIND.sub(" ", s)          # dates are found on the original casing, then the text is lower-cased
    s = NORM_DROP.sub(" ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def err(items):
    return sum(not x[0] for x in items) / len(items) if items else float("nan")


def main():
    gold, docs, raw, blocks = D.load_world()
    P1, P2 = D.load_preds(os.environ["TT_RUN1"]), D.load_preds(os.environ["TT_RUN2"])
    ex1 = {f: Extraction.model_validate(p["extraction"]) for f, p in P1.items()}
    ex2 = {f: Extraction.model_validate(p["extraction"]) if p.get("extraction") else None for f, p in P2.items()}
    claims, rep = [], []
    for l in gold:
        f = l["file"]; d = docs[f]; ex = ex1[f]; cl = d.filer.lower().strip(); years = D.years_of(ex)
        c, ch = (mask_text(d.sections.get(k, ""), blocks[f]) for k in ("cause", "chronology"))
        dec = A.decide(ex, ex2[f], Extraction.model_validate(b1(c, ch, d.filer)), d, blocks[f])
        evdec = [x for x in dec if x["kind"] == "E"]
        assert len(evdec) == len(ex.events)
        golds = D.event_spans(l)
        seen = set(); acc_n = acc_wrong = 0; n_claims = n_wrong = 0
        for i, e in enumerate(ex.events):
            k = D.event_class(e, l, d, years)
            if k == "ignored":
                continue
            accepted = evdec[i]["score"] >= 3
            sp = D.pred_span(e, d.filing_date, years)
            ov = [t for gs, t in golds if gs.granularity != "fuzzy" and sp is not None and coarse_overlap(gs, sp)]
            row = {"file": f, "filer": cl, "ok": k == "right", "accepted": accepted, "date_ok": bool(ov), "cls": None, "dup_underlying": None}
            n_claims += 1; n_wrong += (k != "right")
            if accepted:
                acc_n += 1
                key = (e.type, normsent(e.evidence.quote))
                is_dup = key in seen
                seen.add(key)
                if k != "right":
                    acc_wrong += 1
                    if k == "wrong:date_unparsed":
                        under = "v"
                    elif ov:
                        under = "i"
                    elif any(t == e.type for gs, t in golds):
                        under = "ii"
                    else:
                        under = "iii_undated_same_type" if any(g["type"] == e.type and (g.get("date_inferred") or not g.get("span")) for g in l["events"]) else "iii"
                    row["cls"] = "iv" if is_dup else under
                    row["dup_underlying"] = under if is_dup else None
            claims.append(row)
        sents = [normsent(s["text"]) for s in sentences(raw[f].get("chronology", ""))]
        sents = [s for s in sents if len(s.split()) >= 4]
        dup = len(sents) - len(set(sents))
        rep.append({"file": f, "filer": cl, "norm": sents, "entries": len(sents), "dup_entries": dup, "claims": n_claims, "wrong": n_wrong, "accepted": acc_n, "accepted_wrong": acc_wrong})
    R = {"split": split, "claims": len(claims), "accepted": sum(c["accepted"] for c in claims), "accepted_wrong": sum(1 for c in claims if c["cls"])}
    # (a) classes
    R["classes"] = dict(Counter(c["cls"] for c in claims if c["cls"]))
    R["duplicate_underlying"] = dict(Counter(c["dup_underlying"] for c in claims if c["cls"] == "iv"))
    byf = Counter(c["filer"] for c in claims if c["cls"]); top = [k for k, _ in byf.most_common(5)]
    R["top5_filers_by_accepted_wrong"] = top
    R["classes_by_filer"] = {}
    for c in claims:
        if c["cls"]:
            R["classes_by_filer"].setdefault(c["filer"] if c["filer"] in top else "other", Counter())[c["cls"]] += 1
    R["classes_by_filer"] = {k: dict(v) for k, v in R["classes_by_filer"].items()}
    # (b) date-only view, same filer-cluster bootstrap (2000, seed 0); same item set as the strict view
    def view(okf):
        its = [(okf(c), 3 if c["accepted"] else 0, c["filer"]) for c in claims]
        acc = lambda it: [x for x in it if x[1] >= 3]
        return {"claims": len(its), "accepted": len(acc(its)), "coverage": len(acc(its)) / len(its), "error_all": list(cluster_bootstrap(its, err)),
                "error_accepted": list(cluster_bootstrap(acc(its), err)),
                "delta_all_minus_accepted": list(cluster_bootstrap(its, lambda it: err(it) - err(acc(it)) if acc(it) else float("nan")))}
    R["strict_view"] = view(lambda c: c["ok"])
    R["date_only_view"] = view(lambda c: c["date_ok"])
    R["repetition_rows"] = rep
    json.dump(R, open(f"reports/phase_6_failure_analysis_{split}.json", "w"), indent=1)
    print(split, R["claims"], R["accepted"], R["accepted_wrong"], R["classes"])


if __name__ == "__main__":
    main()
