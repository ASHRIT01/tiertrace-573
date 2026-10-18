"""Deterministic parse of the Component Manufacturer block (L0 labels).
Label-driven and tolerant of 'Label: value' on one line or value on the next.
UNTESTED against real PDFs; Week 1/2 gate."""
import re
from dataclasses import dataclass, asdict

NR = {"nr", "n/r", "not reported", "n/a", "none", ""}
LABELS = {
    "name": r"(?:component )?manufacturer name",
    "tier": r"tier of supplier|supplier tier",
    "type": r"supplier type|type of supplier",
    "address": r"address",
    "country": r"country",
}


@dataclass
class Block:
    name: str | None = None
    tier: str | None = None
    type: str | None = None
    country: str | None = None

    def asdict(self):
        return asdict(self)


def _clean(v: str | None) -> str | None:
    if v is None:
        return None
    v = re.sub(r"\s+", " ", v).strip(" :\t")
    return None if v.lower() in NR else v


def parse_block(text: str) -> Block:
    all_labels = "|".join(f"(?:{p})" for p in LABELS.values())
    found = {}
    for key, pat in LABELS.items():
        m = re.search(rf"(?is)\b(?:{pat})\s*:?\s*(.*?)(?=\b(?:{all_labels})\s*:|\Z)", text)
        found[key] = _clean(m.group(1)) if m else None
    return Block(found["name"], found["tier"], found["type"], found["country"])


def mask_text(text: str, name: str | None) -> str:
    """Evaluation masking: drop the block name wherever it appears."""
    if not name:
        return text
    return re.sub(re.escape(name), "[MASKED]", text, flags=re.I)
