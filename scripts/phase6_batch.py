"""Phase 6 labelling orchestration (glue only; the labelling rules, pipeline code and prompts are the frozen ones).
Per split (testA | testB | unseen) and batch k of 25 filings, work dir data/labels/work/<split>/b<kk>/.
  select <split>            -> config/<split>_selection.json (readable filings of the frozen ID list)
  sheet  <split> <k>        -> prints the review sheet for batch k (text + auto draft) so overrides can be written
  passa  <split> <k>        -> Pass A for batch k from the auto draft + config/overrides/<split>_*.json
  export <split> <k>        -> Pass B batch dir (texts + rules) for batch k
  compare <split> <k>       -> A-vs-B comparison and Pass C packaging
  final  <split> <k>        -> apply Pass C, code checks, per-batch silver labels, agreement stats
  merge  <split>            -> merge all batches into data/labels/<split>_{passA,passB,silver}.json and print hashes
Nothing here reads runs/ (tt/labels/blind.py would refuse)."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SPLITS = {"testA": ("testA_labelled_ids.txt", "data/testA_raw", "test_a"), "testB": ("testB_ids.txt", "data/testB_raw", "test_b"),
          "unseen": ("unseen_filer_ids.txt", "data/unseen_raw", "unseen")}
N = 25


def paths(split, k):
    ids, raw, ov = SPLITS[split]
    w = ROOT / f"data/labels/work/{split}/b{k:02d}"
    return {"raw": raw, "work": w, "ov_ev": f"config/overrides/{ov}_events.json", "ov_cl": f"config/overrides/{ov}_claims.json"}


def batch_files(split, k):
    sel = json.load(open(ROOT / f"config/{split}_selection.json"))["filings"]
    return sel[(k - 1) * N:k * N]


def cli(*a):
    r = subprocess.run([sys.executable, "scripts/phase6_runner.py", *a], cwd=ROOT, capture_output=True, text=True)
    print(r.stdout[-1500:], r.stderr[-1500:] if r.returncode else "")
    if r.returncode:
        sys.exit(r.returncode)
    return r.stdout


def main():
    cmd, split = sys.argv[1], sys.argv[2]
    if cmd == "select":
        cli("label-select", SPLITS[split][1], f"data/splits/{SPLITS[split][0]}", f"config/{split}_selection.json")
        return
    if cmd == "merge":
        return merge(split)
    k = int(sys.argv[3]); P = paths(split, k); w = P["work"]; w.mkdir(parents=True, exist_ok=True)
    for p in (P["ov_ev"], P["ov_cl"]):
        if not (ROOT / p).exists():
            (ROOT / p).parent.mkdir(exist_ok=True); (ROOT / p).write_text("{}\n")
    files = batch_files(split, k)
    (w / "selection.json").write_text(json.dumps({"filings": files}, indent=1))
    rel = str(w.relative_to(ROOT))
    if cmd == "sheet":
        return sheet(split, k, files, P)
    if cmd == "passa":
        cli("pass-a", "--selection", f"{rel}/selection.json", "--drafts", "", "--pdf-dir", P["raw"], "--out", f"{rel}/passA.json",
            "--event-overrides", P["ov_ev"], "--claim-overrides", P["ov_cl"])
    elif cmd == "export":
        (w / "files.json").write_text(json.dumps([f["file"] for f in files]))
        cli("label-export", f"{rel}/files.json", f"{rel}/passB", "--pdf-dir", P["raw"], "--per-batch", str(N))
    elif cmd == "compare":
        cli("label-compare", f"{rel}/passA.json", f"{rel}/passB", f"{rel}/cmp", "--pdf-dir", P["raw"])
    elif cmd == "final":
        out = cli("label-final", f"{rel}/passA.json", f"{rel}/cmp/items.json", f"{rel}/cmp/passC", f"{rel}/silver.json", "--pdf-dir", P["raw"])
        (w / "final_stats.json").write_text(out)
    elif cmd == "row":
        return row(split, k, w)


def row(split, k, w):
    import collections
    st = json.load(open(w / "cmp/ab_stats.json")); fin = json.load(open(w / "final_stats.json")); it = json.load(open(w / "cmp/items.json"))
    c = collections.Counter(i["claim"] for i in it); d = fin["decisions"]; a = fin["pass_c_agreement"]
    nev = sum(len(v) for v in json.load(open(P_ev(split)) ).values()) if False else None
    print(f"| b{k:02d} | {len(batch_files(split, k))} | {len(it)} (S1/S2/C/U/E = {c['S1']}/{c['S2']}/{c['C']}/{c['U']}/{c['E']}) | {st['E']['agree']}/{st['E']['units']} = {st['E']['rate']:.1%} "
          f"| {a['position']['chose_X']} X / {a['position']['chose_Y']} Y / {d['NEITHER']} NEITHER / {d['CONTESTED'] + d['missing']} CONTESTED | {d['A']}/{a['items']} = {d['A']/a['items']:.1%} | {d['B']}/{a['items']} = {d['B']/a['items']:.1%} | checks {len(fin['check_failures'])} fail; {fin['events']} events |")


def sheet(split, k, files, P):
    from tt.labeldraft import load
    A = json.load(open(P["work"] / "passA_auto.json")) if (P["work"] / "passA_auto.json").exists() else None
    if A is None:
        rel = str(P["work"].relative_to(ROOT))
        subprocess.run([sys.executable, "scripts/phase6_runner.py", "pass-a", "--selection", f"{rel}/selection.json", "--drafts", "", "--pdf-dir", P["raw"], "--out", f"{rel}/passA_auto.json",
                        "--event-overrides", P["ov_ev"], "--claim-overrides", P["ov_cl"]], cwd=ROOT, check=True, capture_output=True)
        A = json.load(open(P["work"] / "passA_auto.json"))
    for r in A:
        d = load(ROOT / P["raw"] / r["file"])
        s = d["sections"]
        print(f"\n######## {r['file']}  filer={r['filer']}  filed={r['filing_date']}")
        print("BLOCK name:", d["block"].name)
        print("CAUSE:", " ".join(s.get("cause", "").split())[:600])
        print("CHRONOLOGY:", " ".join(s.get("chronology", "").split())[:3500])
        c = {x["id"]: x for x in r["claims"]}
        print(f"AUTO S1={c['S1']['status']} S2={c['S2']['status']} ({c['S2'].get('quote','')[:70]!r}) C={r['cause']['status']} U={r['upstream']['kind']} {r['upstream'].get('names')}")
        for i, e in enumerate(r["events"]):
            print(f"  E{i} {e['date_text'] or '(inferred)'} | {e['type']} | {'inh ' if e['inherited_date'] else ''}{e['quote'][:90]}")
        for x in r.get("events_excluded", []):
            print(f"  X {x['reason'][:28]} | {x['sentence'][:80]}")


def merge(split):
    out = ROOT / "data/labels"
    kinds = {"passA": "passA.json", "silver": "silver.json"}
    for name, fn in kinds.items():
        recs = []
        for d in sorted((ROOT / f"data/labels/work/{split}").glob("b*")):
            if (d / fn).exists():
                recs += json.loads((d / fn).read_text())
        (out / f"{split}_{name}.json").write_text(json.dumps(recs, indent=1, ensure_ascii=False))
        print(name, len(recs))
    pb = []
    for d in sorted((ROOT / f"data/labels/work/{split}").glob("b*")):
        for f in sorted((d / "passB").glob("batch_*/passB.json")):
            pb += json.loads(f.read_text())
    (out / f"{split}_passB.json").write_text(json.dumps(pb, indent=1, ensure_ascii=False)); print("passB", len(pb))
    import hashlib
    for fn in sorted(out.glob(f"{split}_*.json")):
        print(hashlib.sha256(fn.read_bytes()).hexdigest(), fn.name)


if __name__ == "__main__":
    main()
