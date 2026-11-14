"""AL-1 amendment 2: the two document lists for the extraction run. Reads only committed metadata and the SN-1 manifest; opens no PDF except
the first 4 bytes of SN-1 candidates (to exclude NHTSA's NO SUCH ENTITY replies).

  python scripts/al1_lists.py [--sn1 ~/tiertrace_sn1_cache]
  -> config/al1_docs.json          the 712 documents of the 248 primary campaigns (AL1_PROTOCOL section B), campaign by campaign in sorted
                                   campaign order, versions in their resolved order (versions_in_order), with the committed SHA-256
  -> config/al1_equivalence.json   the 20 equivalence campaigns (amendment 2)

Equivalence draw (fixed in amendment 2): the frame is every campaign with exactly one PDF in the SN-1 cache whose file begins with %PDF,
minus every campaign in data/splits/{dev,testA,testA_labelled,testB,unseen_filer}_ids.txt and minus the 300 AL-1 sample campaigns
(reports/al1/AL1_ORDER.json). The draw is random.Random(0).sample(sorted(frame), 20)."""
import argparse
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from al1_kaggle_lib import AL1_ORDER_SHA256, sha256_file  # noqa: E402

SPLITS = ("dev_ids", "testA_ids", "testA_labelled_ids", "testB_ids", "unseen_filer_ids")
SN1_RE = re.compile(r"cache/static\.nhtsa\.gov_odi_rcl_\d{4}_(RCLRPT-(\d{2}[VE]\d{3})-\d+\.pdf)$", re.I)
SN1_MANIFEST_SHA256 = "7686b2344fb96a7ce1bd4b80b702aacbb007720d6e12bd47911ed887e9232131"


def primary_docs(order: dict) -> list[dict]:
    camps = sorted(c for c, v in order.items() if v["order_status"] == "ORDERED" and c != "24V528")
    out = []
    for c in camps:
        by = {x["fileName"]: x for x in order[c]["versions"]}
        for f in order[c]["versions_in_order"]:
            assert by[f]["usable"]
            out.append({"campaign": c, "file": f, "sha256": by[f]["sha256"]})
    return out


def equivalence_frame(sn1_files: dict, excluded: set, is_pdf) -> dict:
    per = {}
    for p, v in sn1_files.items():
        m = SN1_RE.match(p)
        if m:
            per.setdefault(m.group(2), []).append((p, m.group(1), v["sha256"]))
    return {c: v[0] for c, v in per.items() if len(v) == 1 and c not in excluded and is_pdf(v[0][0])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sn1", default=str(Path.home() / "tiertrace_sn1_cache"))
    a = ap.parse_args()
    op = ROOT / "reports/al1/AL1_ORDER.json"
    assert sha256_file(op) == AL1_ORDER_SHA256, "AL1_ORDER.json is not the committed file"
    order = json.load(open(op))["campaigns"]
    docs = primary_docs(order)
    assert len(docs) == 712 and len({d["campaign"] for d in docs}) == 248
    (ROOT / "config/al1_docs.json").write_text(json.dumps(docs, indent=1) + "\n")

    sn1 = Path(a.sn1)
    assert sha256_file(sn1 / "sn1_manifest.json") == SN1_MANIFEST_SHA256, "SN-1 manifest differs from the recorded one"
    files = json.load(open(sn1 / "sn1_manifest.json"))["files"]
    excluded = set(order)
    for s in SPLITS:
        excluded |= {l.strip() for l in open(ROOT / f"data/splits/{s}.txt") if l.strip()}
    frame = equivalence_frame(files, excluded, lambda p: open(sn1 / p, "rb").read(4) == b"%PDF")
    pick = random.Random(0).sample(sorted(frame), 20)
    eq = {"rule": __doc__.split("Equivalence draw (fixed in amendment 2): ")[1].strip(), "seed": 0, "frame_size": len(frame),
          "excluded_ids": len(excluded), "sn1_manifest_sha256": SN1_MANIFEST_SHA256,
          "documents": [{"campaign": c, "file": frame[c][1], "sn1_path": frame[c][0], "sha256": frame[c][2]} for c in pick]}
    (ROOT / "config/al1_equivalence.json").write_text(json.dumps(eq, indent=1) + "\n")
    print("primary documents", len(docs), "campaigns", len({d['campaign'] for d in docs}), "| equivalence frame", len(frame), "->",
          " ".join(pick))


if __name__ == "__main__":
    main()
