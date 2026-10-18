import json
from pathlib import Path
import pytest
from tt.eval.devscore import score, gold_supplier

ROOT = Path(__file__).parent.parent
LABELS = ROOT / "reports" / "dev_labels_draft.json"
DEV = ROOT / "data" / "dev_raw"


def perfect(L):
    comps = []
    name, st = gold_supplier(L)
    if st == "SUPPORTED":
        q = next(c["quote"] for c in L["claims"] if c["id"] == "S2")
        sec = next(c["section"] for c in L["claims"] if c["id"] == "S2")
        comps.append({"name": name, "role": "SUPPLIER", "status": "SUPPORTED", "evidence": {"section": sec, "quote": q}})
    evs = [{"date_text": e["date_text"], "type": e["type"], "status": "SUPPORTED", "evidence": {"section": "chronology", "quote": e["quote"]}} for e in L["events"]]
    return {"companies": comps, "supply_path": [], "locus": "UNDETERMINED", "locus_status": "INSUFFICIENT", "events": evs,
            "cause_reported": L["cause"]["status"] == "SUPPORTED"}


@pytest.mark.skipif(not DEV.exists(), reason="run `tt dev-fetch` first")
def test_scorer_on_synthetic_predictions():
    L = json.load(open(LABELS))
    preds = [{"file": l["file"], "extraction": perfect(l)} for l in L]
    s = score(L, preds, DEV)
    assert s["json_valid_rate"] == 1 and s["s2_recovery"] == 1 and s["unsupported_claim_rate"] == 0 and s["cause_accuracy"] == 1
    assert s["event_recall"] == 1 and s["event_precision"] == 1
    # a model that guesses the block supplier everywhere is penalised
    bad = []
    for l in L:
        e = perfect(l); e["companies"] = [{"name": "Acme Corp", "role": "SUPPLIER", "status": "SUPPORTED", "evidence": {"section": "cause", "quote": "x"}}]; bad.append({"file": l["file"], "extraction": e})
    sb = score(L, bad, DEV)
    assert sb["s2_recovery"] == 0 and sb["unsupported_claim_rate"] > 0.9
    # invalid JSON counts as invalid, not as a guess
    inv = score(L, [{"file": l["file"], "extraction": None} for l in L], DEV)
    assert inv["json_valid_rate"] == 0 and inv["unsupported_claim_rate"] == 0


def test_summarize_and_bench_with_stub_model(tmp_path):
    from types import SimpleNamespace
    from tt.agent.run_dev import run, summarize
    L = json.load(open(LABELS))[:3]
    if not DEV.exists():
        pytest.skip("run `tt dev-fetch` first")
    calls = []

    def stub(**kw):  # no model is run
        calls.append(kw)
        return SimpleNamespace(message=SimpleNamespace(content=json.dumps(perfect(L[len(calls) - 1]))), eval_count=100, eval_duration=2_000_000_000,
                               prompt_eval_count=900, prompt_eval_duration=3_000_000_000)

    recs = run("stub:model", [l["file"] for l in L], DEV, tmp_path / "o.jsonl", chat=stub)
    assert all(c["think"] is False and c["options"]["temperature"] == 0 and c["options"]["presence_penalty"] == 0 for c in calls)
    s = summarize(recs)
    assert s["n"] == 3 and s["json_valid_rate"] == 1 and abs(s["generation_tokens_per_s"] - 50) < 1e-6 and abs(s["prompt_tokens_per_s"] - 300) < 1e-6
    bad = summarize([{"file": "x", "extraction": None, "seconds": 2.0}, {"file": "y", "extraction": {"nope": 1}, "seconds": 4.0}])
    assert bad["json_valid_rate"] == 0 and bad["seconds_p50_all"] == 2.0 and bad["seconds_p95_all"] == 4.0
