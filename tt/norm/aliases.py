import csv
import re
from dataclasses import dataclass
from pathlib import Path

_SUFFIX = re.compile(r"\b(inc|incorporated|llc|ltd|limited|corp|corporation|co|company|gmbh|ag|sa|s\s?a\s?de\s?c\s?v|plc|group)\b\.?", re.I)


def squash(name: str) -> str:
    s = _SUFFIX.sub(" ", name.lower())
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


@dataclass
class Alias:
    parent_id: str
    confidence: float
    source: str


class AliasTable:
    """config/aliases.csv columns: alias,parent_id,confidence,source"""

    def __init__(self, rows: list[tuple[str, str, float, str]] | None = None):
        self._map = {squash(a): Alias(p, c, s) for a, p, c, s in (rows or [])}

    @classmethod
    def load(cls, path: str | Path) -> "AliasTable":
        with open(path, newline="") as f:
            rows = [(r["alias"], r["parent_id"], float(r["confidence"]), r["source"])
                    for r in csv.DictReader(f)]
        return cls(rows)

    def resolve(self, name: str) -> Alias | None:
        return self._map.get(squash(name))
