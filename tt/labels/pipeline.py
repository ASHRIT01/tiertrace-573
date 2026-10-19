"""Silver-label pipeline stages for any split (used for dev in Phase 1 and for the Phase 6 test labels): export Pass B batches,
compare A vs B and package Pass C, finalize. The subagent steps (Pass B, Pass C) are run by the assistant with the prompts in docs/."""
import hashlib
import json
import shutil
from pathlib import Path

from tt.labels import protocol, schema
from tt.labels.blind import assert_blind
from tt.labels.agree import compare
from tt.labels.texts import export


def export_pass_b(files: list[str], pdf_dir: Path, rules: Path, out_root: Path, per_batch: int = 20) -> dict:
    assert_blind(pdf_dir, rules, out_root)
    manifest = {}
    for k in range(0, len(files), per_batch):
        d = out_root / f"batch_{k // per_batch + 1}"
        paths = export(files[k:k + per_batch], pdf_dir, d / "texts")
        shutil.copy(rules, d / "LABELING_RULES.md")
        manifest[d.name] = [p.name for p in paths]
    (out_root / "manifest.json").write_text(json.dumps(manifest, indent=1))
    return manifest


def compare_and_package(pass_a: list[dict], pass_b_dirs: list[Path], pdf_dir: Path, rules: Path, out_dir: Path) -> dict:
    assert_blind(*pass_b_dirs, pdf_dir, rules, out_dir)
    B = protocol.load_pass(pass_b_dirs)
    fails_b = schema.check(B, pdf_dir)
    ctx = protocol.context([a["file"] for a in pass_a], pdf_dir)
    res = compare(pass_a, B, ctx)
    items = protocol.number_items(res["items"])
    out_dir.mkdir(parents=True, exist_ok=True)
    texts = out_dir / "alltexts"
    texts.mkdir(exist_ok=True)
    for d in pass_b_dirs:
        for t in (d / "texts").glob("*.txt"):
            shutil.copy(t, texts)
    dirs = protocol.package_for_c(items, texts, rules, out_dir / "passC")
    stats = {k: {**v, "wilson95": list(v["wilson95"])} for k, v in res["stats"].items()}
    (out_dir / "items.json").write_text(json.dumps(items, indent=1, ensure_ascii=False))
    (out_dir / "ab_stats.json").write_text(json.dumps(stats, indent=1))
    (out_dir / "passB.json").write_text(json.dumps(B, indent=1, ensure_ascii=False))
    return {"n_B": len(B), "B_check_failures": fails_b, "stats": stats, "n_items": len(items), "passC_dirs": [str(d) for d in dirs]}


def finalize(pass_a: list[dict], items: list[dict], decision_dirs: list[Path], pdf_dir: Path, out: Path) -> dict:
    assert_blind(*decision_dirs, pdf_dir, out)
    dec = []
    for d in decision_dirs:
        dec += json.loads((d / "decisions.json").read_text())
    recs, counts = protocol.apply_c(pass_a, items, dec)
    fails = schema.check(recs, pdf_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(recs, indent=1, ensure_ascii=False))
    return {"decisions": counts, "check_failures": fails, "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "contested": sum(len(r["contested"]) for r in recs), "events": sum(len(r["events"]) for r in recs)}
