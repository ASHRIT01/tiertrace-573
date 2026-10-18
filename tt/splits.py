"""Draw the dev and Test-A campaign lists from the LOCAL flat-file index (no network, no PDFs).
Dev: campaigns of 2015-2022, equal number per year. Test-A: 2023 through Feb 2026, allocated to years in proportion to the
number of eligible campaigns. Both exclude the 300 audit-sample campaigns. Vehicle (V) and equipment (E) campaigns only.
Deterministic: eligible ids are sorted, then shuffled with random.Random(seed)."""
import csv
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

TESTA_END = "20260228"  # RCDATE cutoff for the 2026 part of Test-A


def eligible(campaigns_csv: Path, sample_jsonl: Path) -> list[dict]:
    seen = {json.loads(l)["campaign"] for l in sample_jsonl.read_text().splitlines()}
    rows = [r for r in csv.DictReader(open(campaigns_csv)) if r["type"] in ("V", "E") and r["campaign"] not in seen]
    for r in rows:
        r["year"] = int(r["year"])
    return sorted(rows, key=lambda r: r["campaign"])


def draw(rows: list[dict], dev_per_year: int = 50, testa_n: int = 1000, seed: int = 0) -> tuple[list[dict], list[dict], dict]:
    rng = random.Random(seed)
    by = defaultdict(list)
    for r in rows:
        by[r["year"]].append(r)
    dev = []
    for y in range(2015, 2023):
        pool = by[y][:]
        rng.shuffle(pool)
        dev += pool[:dev_per_year]
    win = {y: [r for r in by[y] if y < 2026 or r["rcdate"] <= TESTA_END] for y in (2023, 2024, 2025, 2026)}
    total = sum(len(v) for v in win.values())
    alloc = {y: round(testa_n * len(v) / total) for y, v in win.items()}
    alloc[2025] += testa_n - sum(alloc.values())  # rounding remainder
    testa = []
    for y, pool in win.items():
        pool = pool[:]
        rng.shuffle(pool)
        testa += pool[: alloc[y]]
    return dev, testa, {"dev_per_year": dev_per_year, "testA_alloc": alloc, "eligible_by_year": {y: len(v) for y, v in sorted(by.items())},
                         "testA_window_pool": {y: len(v) for y, v in win.items()}}


def write(dev: list[dict], testa: list[dict], out: Path, info: dict, seed: int) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for name, rows in (("dev_ids.txt", dev), ("testA_ids.txt", testa)):
        (out / name).write_text("\n".join(sorted(r["campaign"] for r in rows)) + "\n")
        hashes[name] = hashlib.sha256((out / name).read_bytes()).hexdigest()
    (out / "SHA256SUMS").write_text("".join(f"{h}  {n}\n" for n, h in hashes.items()))
    (out / "README.md").write_text(
        "# Splits (IDs only)\n\nCampaign ids drawn by tt/splits.py from the local flat-file index; seed %d. Dev: 2015-2022, %d per year. "
        "Test-A: 2023-Feb 2026, allocated in proportion to eligible campaigns per year. The 300 audit-sample campaigns are excluded from both. "
        "V and E campaigns only. SHA-256 of each file is in SHA256SUMS. No Test-A filing has been downloaded or read.\n\n```\n%s\n```\n"
        % (seed, info["dev_per_year"], json.dumps(info, indent=1)))
    return hashes
