"""AL-1 amendment 2: pure helpers for the extraction run (Mac reference and Kaggle). No model call, no PDF parsing, no lineage result.

- hashing and manifest verification (PDFs, bundles, output zips);
- the model acceptance check: the Ollama API digest must equal the frozen digest, the blob named by that digest (the registry manifest) must
  re-hash to it, and every blob it lists must exist, have its size and re-hash to its digest (same idea as scripts/freeze.py, which re-hashes
  the weight blobs; here every blob is checked, as amendment 2 requires);
- tolerant JSONL reading for resume (a record cut off by a kill is dropped and re-run);
- the session time budget;
- the equivalence metric (amendment 2): accepted run-1 event claims matched by document, event type and normalised date text."""
import hashlib
import json
import re
import time
from collections import Counter
from pathlib import Path

FROZEN_DIGEST = "d8b0f5e9760cd1682034f292d7ef72ec46f432149be0df7574bf2d6e92e38c04"
FROZEN_WEIGHT_BLOBS = ("a9d0a3e1d8c91732a3812becd31f8d4a8ff57414903f226306069f0437e2ac50",
                       "e56a899b1540860385465756dd308c84417410b94dbc1c380adffd20a921ca60")
RUN_SETTINGS_SHA256 = "7a13cd4a37e391d672c1ad8c071d03cde0bdf62c30e8c50a4c4a00328f0edbb9"
AL1_ORDER_SHA256 = "29e181b5b064bf1cde6844b46377faf530b9462430ea79f98d839c1fce434f17"
THRESHOLD = 0.85


# ---- hashing ------------------------------------------------------------------------------------------------------------
def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def verify_files(expected: dict, root) -> dict:
    """expected {relative path: sha256} -> {"ok": n, "missing": [...], "bad": [...]} (paths sorted)."""
    root = Path(root)
    missing, bad, ok = [], [], 0
    for rel, want in sorted(expected.items()):
        p = root / rel
        if not p.is_file():
            missing.append(rel)
        elif sha256_file(p) != want:
            bad.append(rel)
        else:
            ok += 1
    return {"ok": ok, "missing": missing, "bad": bad}


def manifest_of(root, rels) -> dict:
    root = Path(root)
    return {r: sha256_file(root / r) for r in sorted(rels)}


# ---- model acceptance ---------------------------------------------------------------------------------------------------
def blob_path(blobs_dir, digest: str) -> Path:
    return Path(blobs_dir) / f"sha256-{digest.split(':')[-1]}"


def model_check(api_digest: str, blobs_dir, frozen_digest: str = FROZEN_DIGEST, weight_blobs=FROZEN_WEIGHT_BLOBS) -> dict:
    """Raise ValueError unless the model is the frozen one. Returns the verified blob list {digest: size}.
    1. the API digest equals the frozen digest;
    2. the blob named by that digest (the registry manifest) re-hashes to it;
    3. every blob it lists (config and layers) exists, has the listed size and re-hashes to its digest;
    4. the frozen weight blobs are among them."""
    if api_digest != frozen_digest:
        raise ValueError(f"API digest {api_digest} != frozen {frozen_digest}")
    mp = blob_path(blobs_dir, frozen_digest)
    if not mp.is_file():
        raise ValueError(f"manifest blob {mp.name} missing")
    if sha256_file(mp) != frozen_digest:
        raise ValueError("manifest blob does not re-hash to the frozen digest")
    man = json.loads(mp.read_bytes())
    layers = [man["config"], *man["layers"]]
    out = {}
    for l in layers:
        d = l["digest"].split(":")[-1]
        p = blob_path(blobs_dir, d)
        if not p.is_file():
            raise ValueError(f"blob {d[:16]} missing")
        if p.stat().st_size != l["size"]:
            raise ValueError(f"blob {d[:16]} size {p.stat().st_size} != {l['size']}")
        if sha256_file(p) != d:
            raise ValueError(f"blob {d[:16]} does not re-hash to its digest")
        out[d] = l["size"]
    missing_w = [w for w in weight_blobs if w not in out]
    if missing_w:
        raise ValueError(f"frozen weight blobs not in the manifest: {missing_w}")
    out[frozen_digest] = mp.stat().st_size
    return out


# ---- resume -------------------------------------------------------------------------------------------------------------
def read_jsonl_repair(path) -> list[dict]:
    """Read a JSONL file written one record per line. A final line that does not parse (a write cut off by a kill) is removed from the
    file and dropped, so that document is run again. A bad line anywhere else is an error."""
    p = Path(path)
    if not p.exists():
        return []
    raw = p.read_bytes()
    lines = raw.split(b"\n")
    recs, keep = [], []
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            recs.append(json.loads(line))
            keep.append(line)
        except json.JSONDecodeError:
            if any(x.strip() for x in lines[i + 1:]):
                raise ValueError(f"{p}: malformed record at line {i + 1} that is not the last line")
            p.write_bytes(b"".join(x + b"\n" for x in keep))
            break
    return recs


def done_files(recs: list[dict]) -> set:
    return {r["file"] for r in recs}


class Budget:
    """Stop before starting a call that is not expected to finish before the deadline. The estimate is the mean call time so far
    (default `first_guess` seconds before any call), plus a safety margin."""

    def __init__(self, deadline: float | None, first_guess: float = 120.0, margin: float = 60.0, clock=time.time):
        self.deadline, self.first_guess, self.margin, self.clock = deadline, first_guess, margin, clock
        self.n, self.total = 0, 0.0

    def record(self, seconds: float):
        self.n += 1
        self.total += seconds

    def estimate(self) -> float:
        return self.total / self.n if self.n else self.first_guess

    def can_start(self, calls: int = 1) -> bool:
        """True if `calls` more calls are expected to finish before the deadline."""
        return self.deadline is None or self.clock() + calls * self.estimate() + self.margin <= self.deadline


def campaign_groups(docs: list[dict]) -> list[tuple[str, list[str]]]:
    """[{"campaign", "file"}, ...] in run order -> [(campaign, [files])], keeping order; a campaign must be contiguous."""
    out, seen = [], set()
    for d in docs:
        if out and out[-1][0] == d["campaign"]:
            out[-1][1].append(d["file"])
            continue
        if d["campaign"] in seen:
            raise ValueError(f"campaign {d['campaign']} is not contiguous in the document list")
        seen.add(d["campaign"])
        out.append((d["campaign"], [d["file"]]))
    return out


# ---- equivalence metric -------------------------------------------------------------------------------------------------
def norm_date(s: str) -> str:
    return re.sub(r"[^0-9a-z]", "", (s or "").casefold())


def accepted_keys(gate_rec: dict | None) -> Counter:
    if not gate_rec or not gate_rec.get("run1_valid"):
        return Counter()
    return Counter((e["type"], norm_date(e["date_text"])) for e in gate_rec["events"] if e["accepted"])


def equivalence(ref: dict, new: dict, files: list[str], threshold: float = THRESHOLD) -> dict:
    """ref, new: {file: gate record}. files: the equivalence documents. A reference claim is matched if the other machine has an accepted
    claim in the same document with the same type and normalised date text (one-to-one: multiset intersection per document).
    share_ref = matched / reference accepted; share_new = matched / new accepted. Continue only if both are >= threshold; a zero
    denominator does not pass."""
    n_ref = n_new = n_both = 0
    for f in files:
        a, b = accepted_keys(ref.get(f)), accepted_keys(new.get(f))
        n_ref += sum(a.values())
        n_new += sum(b.values())
        n_both += sum((a & b).values())
    s_ref = n_both / n_ref if n_ref else None
    s_new = n_both / n_new if n_new else None
    ok = s_ref is not None and s_new is not None and s_ref >= threshold and s_new >= threshold
    return {"documents": len(files), "reference_accepted": n_ref, "new_accepted": n_new, "matched": n_both,
            "share_reference_also_new": s_ref, "share_new_also_reference": s_new, "threshold": threshold, "continue": ok,
            "ref_missing": sorted(f for f in files if f not in ref), "new_missing": sorted(f for f in files if f not in new)}
