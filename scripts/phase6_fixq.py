"""Mechanical Pass A fix (D-T3): for the 2025+ Part 573 layout where the block reads "Name:\\n<name>", rewrite the Pass A claim quote
"Name : <name>" as "Name: <name>" (verbatim after whitespace collapse) by adding a per-filing claim override. Usage: phase6_fixq.py <split> <k>"""
import ast, json, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
split, k = sys.argv[1], int(sys.argv[2])
ov = {"testA": "test_a", "testB": "test_b", "unseen": "unseen"}[split]
raw = {"testA": "data/testA_raw", "testB": "data/testB_raw", "unseen": "data/unseen_raw"}[split]
w = f"data/labels/work/{split}/b{k:02d}"
code = ("import json,sys;sys.path.insert(0,'.');from pathlib import Path;from tt.labels.schema import check;"
        f"print(json.dumps(check(json.load(open('{w}/passA.json')), Path('{raw}'))))")
fails = json.loads(subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True).stdout)
p = ROOT / f"config/overrides/{ov}_claims.json"; d = json.loads(p.read_text())
n = 0
for f, chk, detail in fails:
    m = re.match(r'(S1|S2) quote not in block: [\'"]Name : (.+)[\'"]$', detail)
    if chk == "Q1" and m:
        d.setdefault(f, {}).setdefault(m[1], {})["quote"] = "Name: " + m[2]; n += 1
p.write_text(json.dumps(d, indent=1, ensure_ascii=False))
print("fixed", n, "of", len(fails))
