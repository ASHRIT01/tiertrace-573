import re

_INLINE = re.compile(r"^[A-Z][^:\n]{2,60} :[ \t]*\S", re.M)      # 'Name : ZF Group'
_STACKED = re.compile(r"^[A-Z][^:\n]{2,80}:[ \t]*$", re.M)        # 'Name:' then value next line


def detect_layout(text: str) -> str:
    """'inline' (older, space before colon, value on same line), 'stacked' (label line, value
    on next line) or 'unknown'. Heuristic from the six reference filings; UNVERIFIED beyond them."""
    i, s = len(_INLINE.findall(text)), len(_STACKED.findall(text))
    if i == s == 0:
        return "unknown"
    return "inline" if i >= s else "stacked"
