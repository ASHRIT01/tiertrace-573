"""Score B0/B1 on the dev silver labels with the same scorer as the models. python -m tt.eval.baselines_run out.json"""
import json
import sys
from collections import Counter

from tt.baselines.rules import b0, b1
from tt.eval.devscore import score
from tt.eval.diagnose import PDF, load_world
from tt.parse.block import mask_text


def run():
    gold, docs, raw, blocks = load_world()
    maj = Counter(l["cause"]["status"] == "SUPPORTED" for l in gold).most_common(1)[0][0]
    p0, p1 = [], []
    for l in gold:
        d = docs[l["file"]]
        cause, chron = (mask_text(d.sections.get(k, ""), blocks[l["file"]]) for k in ("cause", "chronology"))
        p0.append({"file": l["file"], "extraction": b0(maj)})
        p1.append({"file": l["file"], "extraction": b1(cause, chron, d.filer)})
    return {"B0": score(gold, p0, PDF), "B1": score(gold, p1, PDF), "B0_cause_reported": maj}


if __name__ == "__main__":
    R = run(); json.dump(R, open(sys.argv[1], "w"), indent=1, default=str)
    for k in ("B0", "B1"):
        print(k, {m: (round(v, 3) if isinstance(v, float) else v) for m, v in R[k].items() if m in ("json_valid_rate", "verifier_pass_rate", "s2_recovery", "unsupported_claim_rate", "event_precision", "event_recall", "event_f1", "cause_accuracy", "s2_recovered", "s2_gold_supported")})
