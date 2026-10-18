"""Deterministic parse of the Component Manufacturer block (L0 labels)."""
import re
from dataclasses import dataclass, asdict

NR = {"nr", "n/r", "not reported", "n/a", "none", ""}
_LABEL = re.compile(r"^\s*(Tier of Supplier|Supplier Type|Name|Address|Country)\s*:\s*(.*)$", re.I)
_KEY = {"tier of supplier": "tier", "supplier type": "type", "name": "name",
        "address": "address", "country": "country"}


@dataclass
class Block:
    name: str | None = None
    tier: str | None = None
    type: str | None = None
    country: str | None = None

    def asdict(self):
        return asdict(self)


def _clean(v: str | None) -> str | None:
    v = re.sub(r"\s+", " ", v or "").strip(" :\t")
    return None if v.lower() in NR else v


def parse_block(text: str) -> Block:
    """`text` must keep its line breaks (use the raw cleaned block, see parse_block_from_doc)."""
    fields: dict[str, list[str]] = {}
    cur = None
    for line in text.splitlines():
        m = _LABEL.match(line)
        if m:
            cur = _KEY[m[1].lower()]
            fields.setdefault(cur, []).append(m[2])
        elif cur:
            fields[cur].append(line)
    g = lambda k: _clean(" ".join(fields.get(k, [])))
    return Block(g("name"), g("tier"), g("type"), g("country"))


def raw_block(full_text: str) -> str:
    """Block text with line breaks preserved, from 'Component Manufacturer' to the next section."""
    from tt.parse.sections import clean
    t = clean(full_text)
    m = re.search(r"(?im)^[ \t]*(?:supplier identification[ \t]*:?[ \t]*\n[ \t]*)?component manufacturer[ \t]*:?[ \t]*\n", t)
    if not m:
        return ""
    end = re.search(r"(?im)^[ \t]*(?:involved components|chronology|description of (?:the )?remedy)\b", t[m.end():])
    return t[m.end(): m.end() + end.start()] if end else t[m.end():]


def mask_text(text: str, name: str | None) -> str:
    """Evaluation masking: drop the block name wherever it appears."""
    if not name:
        return text
    return re.sub(re.escape(name), "[MASKED]", text, flags=re.I)
