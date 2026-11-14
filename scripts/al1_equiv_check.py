"""AL-1 amendment 2: the equivalence check between the M2 reference and another machine (Kaggle).

  python scripts/al1_equiv_check.py REF_GATE.jsonl NEW_GATE.jsonl OUT.json

Both files are gate.jsonl outputs of scripts/al1_extract.py on the 20 documents of config/al1_equivalence.json. Writes the counts and the two
shares to OUT.json and prints them. Exit 0 if both shares are >= 0.85 (continue to the AL-1 run), 1 otherwise (stop; the decision returns to
the author). The equivalence documents are not AL-1 filings, so printing these counts reveals nothing about AL-1."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from al1_kaggle_lib import equivalence, read_jsonl_repair, sha256_file  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main(ref_path, new_path, out_path) -> int:
    files = [d["file"] for d in json.load(open(ROOT / "config/al1_equivalence.json"))["documents"]]
    ref = {r["file"]: r for r in read_jsonl_repair(ref_path)}
    new = {r["file"]: r for r in read_jsonl_repair(new_path)}
    R = equivalence(ref, new, files)
    R["reference_gate_sha256"], R["new_gate_sha256"] = sha256_file(ref_path), sha256_file(new_path)
    Path(out_path).write_text(json.dumps(R, indent=1) + "\n")
    f = lambda x: "n/a" if x is None else f"{x:.3f}"  # noqa: E731
    print(f"EQUIVALENCE: documents {R['documents']} | M2 accepted {R['reference_accepted']} | new accepted {R['new_accepted']} | matched {R['matched']} | "
          f"M2->new {f(R['share_reference_also_new'])} | new->M2 {f(R['share_new_also_reference'])} | threshold {R['threshold']} | "
          f"{'CONTINUE' if R['continue'] else 'STOP: decision returns to the author'}")
    return 0 if R["continue"] else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
