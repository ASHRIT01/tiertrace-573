"""AL-1 amendment 2: extraction runner for the frozen agent and gate (used for the Mac equivalence reference and on Kaggle).

  python scripts/al1_extract.py --docs DOCS.json --pdf-dir DIR --out-dir OUT [--mode campaign|batch] [--deadline EPOCH] [--blobs-dir DIR]

DOCS.json is a list of {"campaign", "file"} in run order. PDFs are read from --pdf-dir/<file>.
- Model calls go through the FROZEN tt.agent.run_dev.run, one call per document, with config/run_settings.json (model, prompt v2, think off,
  run 1 temperature 0 seed 0, run 2 temperature 0.5 seed 1, num_ctx 6144) and the 300 s timeout, exactly as scripts/phase6_run.py.
- The gate is the FROZEN tt.agent.agent.decide on run 1 with run 2 as the agreement filter and the B1 rule baseline, after installing the
  amendment-1 wrapper, exactly as scripts/ts_gate.py; the only difference is that the document list comes from DOCS.json instead of a gold
  file (ts_gate builds each document with tt.eval.devscore._doc and the block name with tt.labeldraft.load, which use only the file).
  A claim is accepted iff its score >= 3. A missing run 2 makes run 2 "not agree".
- mode "campaign": campaign by campaign, run 1 on the campaign's documents, then run 2 on them, then the gate. mode "batch": run 1 on all
  documents, then run 2 on all, then the gate (used for the 20 equivalence documents, one per campaign, so that a document's run 2 never
  directly follows its own run 1).
- Resume: documents already in run1.jsonl / run2.jsonl / gate.jsonl are skipped; a record cut off by a kill is dropped and re-run. A
  timeout is recorded and not retried. Every start and restart is logged in run_log.txt.
- --deadline: no call is started unless it is expected to finish before the deadline (mean call time so far + 60 s); exit code 3.
- Prints and writes to progress.json ONLY counts and timing: never file names, claims, quotes, dates or any result.
Exit codes: 0 all documents done, 2 a check failed, 3 stopped by the deadline."""
import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CWD = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
os.chdir(ROOT)

import tt.eval.amend1 as AM  # noqa: E402  (installs the crash-only parse_span guard on import, as in ts_gate.py)

AM.install()
from tt.agent import agent as A  # noqa: E402
from tt.agent.run_dev import build_user, run  # noqa: E402
from tt.agent.schemas import Extraction  # noqa: E402
from tt.baselines.rules import b1  # noqa: E402
from tt.eval.devscore import _doc  # noqa: E402
from tt.labeldraft import load  # noqa: E402
from tt.parse.block import mask_text  # noqa: E402

from al1_kaggle_lib import (FROZEN_DIGEST, RUN_SETTINGS_SHA256, Budget, campaign_groups, done_files, model_check,  # noqa: E402
                            read_jsonl_repair, sha256_bytes, sha256_file)

OLLAMA_VERSION = "0.40.6"


def host() -> str:
    h = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434")
    return h if h.startswith("http") else f"http://{h}"


def server_checks(model: str, blobs_dir: str | None) -> dict:
    v = json.load(urllib.request.urlopen(f"{host()}/api/version", timeout=10))["version"]
    if v != OLLAMA_VERSION:
        raise SystemExit(f"CHECK FAILED: Ollama server version {v} != {OLLAMA_VERSION}")
    tags = json.load(urllib.request.urlopen(f"{host()}/api/tags", timeout=10))["models"]
    m = next((t for t in tags if t["name"] == model), None)
    if m is None:
        raise SystemExit(f"CHECK FAILED: model {model} is not installed (this runner never pulls)")
    if m["digest"] != FROZEN_DIGEST:
        raise SystemExit(f"CHECK FAILED: model digest {m['digest']} != frozen {FROZEN_DIGEST}")
    blobs = None
    if blobs_dir:
        try:
            blobs = len(model_check(m["digest"], blobs_dir))
        except ValueError as e:
            raise SystemExit(f"CHECK FAILED: {e}")
    return {"ollama_version": v, "digest": m["digest"], "blobs_verified": blobs}


def gate_record(campaign: str, f: str, pdf_dir: Path, p1: dict | None, p2: dict | None) -> dict:
    """Same machinery as scripts/ts_gate.py for one document."""
    if not p1 or not p1.get("extraction"):
        return {"campaign": campaign, "file": f, "run1_valid": False, "run2_valid": bool(p2 and p2.get("extraction")), "events": []}
    d = _doc({"file": f}, pdf_dir)
    block = load(pdf_dir / f)["block"].name
    ex = Extraction.model_validate(p1["extraction"])
    ex2 = Extraction.model_validate(p2["extraction"]) if p2 and p2.get("extraction") else None
    c, ch = (mask_text(d.sections.get(k, ""), block) for k in ("cause", "chronology"))
    dec = [x for x in A.decide(ex, ex2, Extraction.model_validate(b1(c, ch, d.filer)), d, block) if x["kind"] == "E"]
    assert len(dec) == len(ex.events)
    return {"campaign": campaign, "file": f, "run1_valid": True, "run2_valid": ex2 is not None,
            "events": [{"date_text": e.date_text or "", "type": e.type, "quote": e.evidence.quote if e.evidence else "",
                        "reasons": dec[i]["reasons"], "score": dec[i]["score"], "accepted": dec[i]["score"] >= 3}
                       for i, e in enumerate(ex.events)]}


def append(path: Path, rec: dict):
    with open(path, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", required=True)
    ap.add_argument("--pdf-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--mode", choices=("campaign", "batch"), default="campaign")
    ap.add_argument("--deadline", type=float, default=None)
    ap.add_argument("--blobs-dir", default=None)
    ap.add_argument("--stop-at-campaign-boundary", action="store_true",
                    help="amendment 3: check the deadline only before a campaign, for all its remaining calls")
    a = ap.parse_args(argv)

    if sha256_file(ROOT / "config/run_settings.json") != RUN_SETTINGS_SHA256:
        print("CHECK FAILED: config/run_settings.json is not the frozen file"); return 2
    S = json.load(open(ROOT / "config/run_settings.json"))
    model, prompt = S["agent_model"], S["prompt"]
    assert S["think"] is False and prompt == "v2"
    try:
        srv = server_checks(model, str(CWD / a.blobs_dir) if a.blobs_dir else None)
    except SystemExit as e:
        print(e); return 2

    docs = json.load(open(CWD / a.docs))
    docs = docs["documents"] if isinstance(docs, dict) else docs
    pdf_dir, out = (CWD / a.pdf_dir).resolve(), (CWD / a.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    missing = [d["file"] for d in docs if not (pdf_dir / d["file"]).is_file()]
    if missing:
        print(f"CHECK FAILED: {len(missing)} PDFs missing from --pdf-dir"); return 2
    groups = [("ALL", [d["file"] for d in docs])] if a.mode == "batch" else campaign_groups(docs)
    camp_of = {d["file"]: d["campaign"] for d in docs}
    P = {k: out / f"run{k}.jsonl" for k in (1, 2)}
    G, PR, LOG, PROG = out / "gate.jsonl", out / "prompts.jsonl", out / "run_log.txt", out / "progress.json"
    recs = {k: read_jsonl_repair(P[k]) for k in (1, 2)}
    gated = done_files(read_jsonl_repair(G))
    prompted = done_files(read_jsonl_repair(PR))
    budget = Budget(a.deadline)
    t0 = time.time()

    def counts(state: str) -> dict:
        r1, r2 = (read_jsonl_repair(P[k]) for k in (1, 2))
        c = {"state": state, "documents": len(docs), "campaigns": len(groups) if a.mode == "campaign" else len({d['campaign'] for d in docs}),
             "run1_records": len(r1), "run2_records": len(r2), "gated": len(gated),
             "run1_valid_json": sum(1 for r in r1 if r.get("extraction") is not None),
             "run2_valid_json": sum(1 for r in r2 if r.get("extraction") is not None),
             "timeouts": sum(1 for r in r1 + r2 if r.get("timeout")), "call_errors": sum(1 for r in r1 + r2 if r.get("error")),
             "truncated": sum(1 for r in r1 + r2 if r.get("truncated")),
             "session_calls": budget.n, "session_seconds": round(time.time() - t0, 1),
             "mean_call_seconds_session": round(budget.estimate(), 1) if budget.n else None,
             "updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "server": srv, "mode": a.mode}
        PROG.write_text(json.dumps(c, indent=1))
        return c

    have = len(recs[1]) + len(recs[2]) + len(gated)
    with open(LOG, "a") as fh:
        fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {'RESTART' if have else 'START'} | mode {a.mode} | documents {len(docs)} | "
                 f"run1 {len(recs[1])} run2 {len(recs[2])} gated {len(gated)}\n")
    print(f"model={model} digest={srv['digest'][:12]} ollama={srv['ollama_version']} blobs_verified={srv['blobs_verified']} prompt={prompt} "
          f"think=False documents={len(docs)} mode={a.mode} run1_done={len(recs[1])} run2_done={len(recs[2])} gated={len(gated)}", flush=True)

    for f in (d["file"] for d in docs):
        if f not in prompted:
            append(PR, {"file": f, "user_message_sha256": sha256_bytes(build_user(pdf_dir / f).encode())})
            prompted.add(f)

    def deadline_stop():
        c = counts("STOPPED_BY_DEADLINE")
        with open(LOG, "a") as fh:
            fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | DEADLINE STOP | run1 {c['run1_records']} run2 {c['run2_records']} gated {c['gated']}\n")
        print(f"DEADLINE STOP: {json.dumps({k2: c[k2] for k2 in ('run1_records', 'run2_records', 'gated', 'documents')})}", flush=True)
        return 3

    for gi, (_, files) in enumerate(groups, 1):
        if a.stop_at_campaign_boundary:
            todo = sum(f not in done_files(read_jsonl_repair(P[k])) for k in (1, 2) for f in files)
            if todo and not budget.can_start(todo):
                return deadline_stop()
        for k in (1, 2):
            r = S[f"run{k}"]
            done = done_files(read_jsonl_repair(P[k]))
            for f in files:
                if f in done:
                    continue
                if not a.stop_at_campaign_boundary and not budget.can_start():
                    return deadline_stop()
                rec = run(model, [f], pdf_dir, P[k], r["num_ctx"], resume=True, timeout=300.0, prompt=prompt,
                          extra_options={"temperature": r["temperature"], "seed": r["seed"], "presence_penalty": r["presence_penalty"]})[-1]
                budget.record(rec["seconds"])
        p1 = {x["file"]: x for x in read_jsonl_repair(P[1])}
        p2 = {x["file"]: x for x in read_jsonl_repair(P[2])}
        for f in files:
            if f not in gated:
                append(G, gate_record(camp_of[f], f, pdf_dir, p1.get(f), p2.get(f)))
                gated.add(f)
        c = counts("RUNNING")
        print(f"  group {gi}/{len(groups)} | run1 {c['run1_records']}/{len(docs)} run2 {c['run2_records']}/{len(docs)} gated {c['gated']}/{len(docs)} "
              f"| valid_json {c['run1_valid_json']}+{c['run2_valid_json']} timeouts {c['timeouts']} errors {c['call_errors']} "
              f"| mean_call {c['mean_call_seconds_session']}s elapsed {c['session_seconds']:.0f}s", flush=True)

    c = counts("DONE")
    with open(LOG, "a") as fh:
        fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | DONE | run1 {c['run1_records']} run2 {c['run2_records']} gated {c['gated']} | "
                 f"timeouts {c['timeouts']} errors {c['call_errors']}\n")
    print(f"DONE: {json.dumps({k: c[k] for k in ('documents', 'run1_records', 'run2_records', 'gated', 'run1_valid_json', 'run2_valid_json', 'timeouts', 'call_errors', 'truncated')})}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
