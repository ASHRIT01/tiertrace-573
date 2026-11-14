"""AL-1 amendment 2: build the Kaggle input bundle (outside the repo). Copies bytes only; opens no PDF.

  python scripts/al1_bundle.py --ref runs/al1_equiv_m2 [--al1 ~/tiertrace_al1_cache] [--sn1 ~/tiertrace_sn1_cache] [--out ~/tiertrace_al1_kaggle_bundle.zip]

Layout inside the zip (top folder al1_bundle/):
  al1_pdfs/<fileName>         the 712 documents of config/al1_docs.json, each verified against its committed SHA-256 and the AL-1 manifest
  equiv_pdfs/<fileName>       the 20 documents of config/al1_equivalence.json, each verified against the SN-1 manifest
  m2_reference/               gate.jsonl, run1.jsonl, run2.jsonl, prompts.jsonl, progress.json, run_log.txt, env.json of the M2 reference run
  BUNDLE_MANIFEST.json        SHA-256 of every file above, plus the AL-1 and SN-1 manifest hashes
  SHA256SUMS                  the same, in sha256sum format
Nothing else."""
import argparse
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from al1_kaggle_lib import sha256_bytes, sha256_file  # noqa: E402

AL1_MANIFEST_SHA256 = "000b497cb6c54457e5e034b6703ca49c921f798ad9430a06158d459599947511"
SN1_MANIFEST_SHA256 = "7686b2344fb96a7ce1bd4b80b702aacbb007720d6e12bd47911ed887e9232131"
REF_FILES = ("gate.jsonl", "run1.jsonl", "run2.jsonl", "prompts.jsonl", "progress.json", "run_log.txt", "env.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True)
    ap.add_argument("--al1", default=str(Path.home() / "tiertrace_al1_cache"))
    ap.add_argument("--sn1", default=str(Path.home() / "tiertrace_sn1_cache"))
    ap.add_argument("--out", default=str(Path.home() / "tiertrace_al1_kaggle_bundle.zip"))
    a = ap.parse_args()
    al1, sn1, ref, out = Path(a.al1), Path(a.sn1), Path(a.ref), Path(a.out)
    assert sha256_file(al1 / "al1_manifest.json") == AL1_MANIFEST_SHA256
    assert sha256_file(sn1 / "sn1_manifest.json") == SN1_MANIFEST_SHA256
    am = json.load(open(al1 / "al1_manifest.json"))["files"]
    sm = json.load(open(sn1 / "sn1_manifest.json"))["files"]
    by_sha = {v["sha256"]: p for p, v in am.items()}

    entries = []   # (path in zip, bytes)
    for d in json.load(open(ROOT / "config/al1_docs.json")):
        src = al1 / by_sha[d["sha256"]]
        b = src.read_bytes()
        assert sha256_bytes(b) == d["sha256"], d["file"]
        entries.append((f"al1_pdfs/{d['file']}", b))
    for d in json.load(open(ROOT / "config/al1_equivalence.json"))["documents"]:
        b = (sn1 / d["sn1_path"]).read_bytes()
        assert sha256_bytes(b) == d["sha256"] == sm[d["sn1_path"]]["sha256"], d["file"]
        entries.append((f"equiv_pdfs/{d['file']}", b))
    for n in REF_FILES:
        entries.append((f"m2_reference/{n}", (ref / n).read_bytes()))
    names = [n for n, _ in entries]
    assert len(names) == len({n.lower() for n in names}) == 712 + 20 + len(REF_FILES)

    man = {"al1_manifest_sha256": AL1_MANIFEST_SHA256, "sn1_manifest_sha256": SN1_MANIFEST_SHA256,
           "al1_docs_sha256": sha256_file(ROOT / "config/al1_docs.json"), "al1_equivalence_sha256": sha256_file(ROOT / "config/al1_equivalence.json"),
           "files": {n: sha256_bytes(b) for n, b in entries}}
    sums = "".join(f"{h}  {n}\n" for n, h in man["files"].items())
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:   # PDFs are already compressed
        for n, b in entries:
            z.writestr(f"al1_bundle/{n}", b)
        z.writestr("al1_bundle/BUNDLE_MANIFEST.json", json.dumps(man, indent=1) + "\n")
        z.writestr("al1_bundle/SHA256SUMS", sums)
    print(f"bundle {out} | files {len(entries) + 2} (al1 {sum(n.startswith('al1_pdfs/') for n in names)}, equiv "
          f"{sum(n.startswith('equiv_pdfs/') for n in names)}, m2_reference {len(REF_FILES)}, 2 manifests) | bytes {out.stat().st_size} | "
          f"sha256 {sha256_file(out)} | BUNDLE_MANIFEST sha256 {sha256_bytes((json.dumps(man, indent=1) + chr(10)).encode())}")


if __name__ == "__main__":
    main()
