"""Stratified-by-year campaign sample with usable Part 573 PDFs.
For each year, shuffle (seeded) the V/E campaigns and call list_573 until `per_year` campaigns
with at least one 573 report are found, or `max_try` candidates are exhausted."""
import json
import random
from collections import defaultdict
from pathlib import Path

from tt.fetch.api import ApiClient, list_573


def build_sample(client: ApiClient, campaigns: list[dict], per_year: int = 25, max_try: int = 40,
                 seed: int = 0, out_jsonl: Path = Path("data/processed/sample_573.jsonl"),
                 years: range = range(2015, 2027)) -> dict:
    by_year = defaultdict(list)
    for c in campaigns:
        if c["type"] in ("V", "E"):
            by_year[c["year"]].append(c)
    rng = random.Random(seed)
    stats = {"tried": 0, "with_573": 0, "no_573": 0, "multi_version": 0, "per_year": {}}
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with open(out_jsonl, "w") as f:
        for y in years:
            cands = by_year[y][:]
            rng.shuffle(cands)
            found = tried = 0
            for c in cands:
                if found >= per_year or tried >= max_try:
                    break
                tried += 1
                docs = list_573(client, c["campaign"])
                stats["tried"] += 1
                if not docs:
                    stats["no_573"] += 1
                    continue
                found += 1
                stats["with_573"] += 1
                stats["multi_version"] += len(docs) > 1
                for d in docs:
                    f.write(json.dumps({**d, "year": y, "type": c["type"], "filer": c["filer"], "n_versions": len(docs)}) + "\n")
                f.flush()
            stats["per_year"][y] = {"tried": tried, "found": found}
    return stats
