"""Leak check (run by scripts/freeze.py before anything is frozen). Verifies that no Test-A, Test-B or unseen-filer campaign ID appears
as a file name or inside a file anywhere under data/, runs/ or reports/ (a downloaded PDF, parsed text, label, run output or score).
Expected homes of the IDs are excluded from the verdict and their matches are reported separately: the NHTSA flat file (data/flat/),
its parsed index data/processed/campaigns.csv, and the split ID lists (data/splits/). Everything else that matches is a leak, with one softer class:
a CROSS-REFERENCE is a test ID that is only mentioned inside the contents of a source document (a PDF, or a fetch cache under
data/cache/ or data/api_cache/) that is itself named for a different campaign. It is not a file of the test campaign, so it does not fail
the check, but it is printed with its surrounding text.
PDFs are checked by file name and by their extracted text; every other file by name and raw bytes (so pickles and JSON are covered).
A test ID that is a LEAK may be waived only through config/leak_waivers.json ({id: reason}) and only if it is in no scored subset
(Test-A labelled, Test-B, unseen-filer); waivers are printed and recorded in the freeze manifest."""
import hashlib
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ("data", "runs", "reports")
EXCLUDED = ("data/flat/", "data/processed/campaigns.csv", "data/splits/")
SPLIT_FILES = {"Test-A": "testA_ids.txt", "Test-A labelled": "testA_labelled_ids.txt", "Test-B": "testB_ids.txt", "Unseen-filer": "unseen_filer_ids.txt"}
# 23V002, 23V-002, 23V002000 (campaign id with a 3-digit suffix); not part of a longer alphanumeric token
ID_RX = re.compile(rb"(?<![0-9A-Za-z])(\d{2}[CEPV])-?(\d{3})(?:\d{3})?(?![0-9A-Za-z])")


def load_ids(root: Path = ROOT) -> dict[str, set[str]]:
    out = {}
    for name, fn in SPLIT_FILES.items():
        for d in (root / "data/splits", root / "data/splits/proposed"):
            if (d / fn).exists():
                out[name] = set((d / fn).read_text().split()); break
    if "Test-A" not in out:
        raise SystemExit("leak check: data/splits/testA_ids.txt missing")
    return out


def _ids_in(data: bytes) -> set[str]:
    return {(m.group(1) + m.group(2)).decode() for m in ID_RX.finditer(data)}


def _pdf_text(p: Path) -> bytes:
    import pymupdf
    with pymupdf.open(p) as d:
        return "\n".join(pg.get_text("text") for pg in d).encode("utf-8", "ignore")


SCORED = ("Test-A labelled", "Test-B", "Unseen-filer")
SOURCE_DIRS = ("data/cache/", "data/api_cache/")


def _snippets(data: bytes, ids: set[str], width: int = 70) -> list[str]:
    out = []
    for m in ID_RX.finditer(data):
        if (m.group(1) + m.group(2)).decode() in ids and len(out) < 2:
            a, b = max(0, m.start() - width), min(len(data), m.end() + width)
            out.append(" ".join(data[a:b].decode("utf-8", "ignore").split()))
    return out


def run(root: Path = ROOT, scan=SCAN, excluded=EXCLUDED) -> dict:
    sets = load_ids(root)
    test_ids = set().union(*sets.values())
    hits, ex_hits, scanned, unreadable = defaultdict(set), defaultdict(set), defaultdict(int), []
    cross = {}
    for top in scan:
        base = root / top
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.name.startswith("._") or p.name == ".DS_Store":
                continue
            rel = str(p.relative_to(root))
            scanned[top] += 1
            own = _ids_in(p.name.encode()) & test_ids
            found = set(own)
            try:
                data = _pdf_text(p) if p.suffix.lower() == ".pdf" else p.read_bytes()
            except Exception as e:
                unreadable.append((rel, str(e)[:80])); data = b""
            in_dirs = _ids_in(str(Path(rel).parent).encode()) & test_ids   # a directory named for a test ID
            content = _ids_in(data) & test_ids
            found |= content | in_dirs
            if not found:
                continue
            if rel.startswith(excluded):
                ex_hits[rel] |= found
            elif not own and not in_dirs and (p.suffix.lower() == ".pdf" or rel.startswith(SOURCE_DIRS)):
                cross[rel] = (content, _snippets(data, content))
            else:
                hits[rel] |= found
    waivers = {}
    wf = root / "config/leak_waivers.json"
    if wf.exists():
        import json
        waivers = json.loads(wf.read_text())
    leak_ids = set().union(*hits.values()) if hits else set()
    bad_waiver = sorted(i for i in waivers if any(i in sets[k] for k in SCORED if k in sets))
    unwaived = {f: ids - set(waivers) for f, ids in hits.items() if ids - set(waivers)}
    return {"sets": sets, "leaks": unwaived, "all_leaks": dict(hits), "waivers": waivers, "bad_waivers": bad_waiver,
            "cross_refs": cross, "excluded": dict(ex_hits), "scanned": dict(scanned), "unreadable": unreadable}


def report(r: dict, verbose_limit: int = 60) -> str:
    sets, L = r["sets"], []
    L.append("LEAK CHECK: Test-A / Test-B / unseen-filer IDs in file names or contents under data/, runs/, reports/")
    L.append("  ID sets: " + ", ".join(f"{k} {len(v)}" for k, v in sets.items()) + f" (union {len(set().union(*sets.values()))})")
    L.append("  files scanned: " + ", ".join(f"{k}/ {v}" for k, v in r["scanned"].items()) + f"; unreadable: {len(r['unreadable'])}")
    for rel, e in r["unreadable"]:
        L.append(f"    unreadable (name still checked): {rel}: {e}")
    inset = lambda i: "/".join(k for k, v in sets.items() if i in v)
    L.append(f"  LEAKS (a file or content of a test campaign) in non-excluded files: {len(r['leaks'])} file(s)" + ("" if r["leaks"] else "  -> none"))
    for rel, ids in sorted(r["leaks"].items()):
        L.append(f"    LEAK {rel}: " + ", ".join(f"{i} [{inset(i)}]" for i in sorted(ids)[:10]) + (" ..." if len(ids) > 10 else ""))
    for i, why in sorted(r["waivers"].items()):
        L.append(f"  WAIVER {i} [{inset(i)}]: {why}" + ("   <- REFUSED: ID is in a scored subset" if i in r["bad_waivers"] else ""))
    L.append(f"  CROSS-REFERENCES (test ID only mentioned inside another campaign's source document; not a file of that ID): {len(r['cross_refs'])}")
    for rel, (ids, snip) in sorted(r["cross_refs"].items()):
        L.append(f"    {rel}: " + ", ".join(f"{i} [{inset(i)}]" for i in sorted(ids)) + "".join(f"\n      ...{x}..." for x in snip))
    L.append("  ID matches in EXCLUDED files (expected; reported separately, not part of the verdict):")
    for rel, ids in sorted(r["excluded"].items()):
        by = ", ".join(f"{k} {len(ids & v)}/{len(v)}" for k, v in sets.items())
        s = ", ".join(sorted(ids)) if len(ids) <= verbose_limit else f"{len(ids)} IDs, sha256 of the sorted list {hashlib.sha256(chr(10).join(sorted(ids)).encode()).hexdigest()[:16]}"
        L.append(f"    {rel}: {by}\n      {s}")
    return "\n".join(L)


def main():
    r = run()
    print(report(r))
    return 1 if r["leaks"] or r["bad_waivers"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
