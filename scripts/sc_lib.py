"""SC-1 supplier/component check: library (pure Python, deterministic, no model).
Reference = filer-declared supplier/component (non-AI, not ground truth). Only company names, supplier type and country are kept from the
supplier block; address and telephone lines are never stored or returned."""
import re
import unicodedata

# ---------------------------------------------------------------- supplier block -------------------------------------------------------
BLOCK_HEAD = re.compile(r"^[ \t]*(?:supplier identification[ \t]*:?[ \t]*)?component manufacturer[ \t]*:?[ \t]*$", re.I)
SUPPLIER_ID = re.compile(r"^[ \t]*supplier identification[ \t]*:?[ \t]*$", re.I)
BLOCK_END = re.compile(r"^[ \t]*(?:involved components|chronology|description of (?:the )?remedy|component name\b|component description\b|"
                       r"component part number\b|recall schedule|purchaser information|remedy information|identify how|"
                       r"description of remedy program|planned dates|manufacturer information|population|equipment information|vehicle information)",
                       re.I)
FIELD = re.compile(r"^[ \t]*(tier of supplier|supplier type|name|address|country)[ \t]*:[ \t]*(.*)$", re.I)
# repeated page-header lines of the 2025+ form that can fall inside a block
PAGE_HDR = re.compile(r"^[ \t]*(?:u\.s\. department|of transportation|national highway|traffic safety|administration|part 573 safety recall report|"
                      r"\d{2}[vect]-?\d{3}|manufacturer name\s*:|submission date\s*:|nhtsa recall no|manufacturer recall no|"
                      r"the information contained in this report|omb control no|page \d+)", re.I)
NR = {"", "nr", "n/r", "n/a", "na", "none", "not reported", "not applicable", "unknown", "tbd", "-"}
POINTER = re.compile(r"(?i)^see\b|\battach|\.pdf\b|\bappendix\b|\benclos")


def _val(v: str):
    v = re.sub(r"\s+", " ", v or "").strip(" :;,.\t")
    return None if v.lower() in NR else v


def supplier_blocks(text: str):
    """-> list of blocks; each = {'start', 'end' (char offsets in `text`), 'records': [{'name','type','tier','country'}]}.
    `text` = the frozen cleaned text (tt.parse.sections.clean). Address lines are skipped and never returned."""
    lines = text.split("\n")
    offs, o = [], 0
    for ln in lines:
        offs.append(o); o += len(ln) + 1
    blocks, i = [], 0
    while i < len(lines):
        if not BLOCK_HEAD.match(lines[i]):
            i += 1; continue
        start = offs[i - 1] if i > 0 and SUPPLIER_ID.match(lines[i - 1]) else offs[i]
        recs, cur, field, j = [], {}, None, i + 1
        while j < len(lines) and j < i + 60:
            ln = lines[j]
            if BLOCK_HEAD.match(ln) or BLOCK_END.match(ln):
                break
            if PAGE_HDR.match(ln):
                j += 1; continue
            m = FIELD.match(ln)
            if m:
                k = m[1].lower().replace("tier of supplier", "tier").replace("supplier type", "type")
                if k in ("name", "tier", "type") and cur.get("name") is not None and (k == "name" or "name" in cur):
                    recs.append(cur); cur = {}
                field = k
                if k != "address":
                    cur[k] = (cur.get(k) or "") + " " + m[2] if cur.get(k) else m[2]
                j += 1; continue
            if field and field != "address" and ln.strip():
                cur[field] = (cur.get(field) or "") + " " + ln
            j += 1
        if cur:
            recs.append(cur)
        recs = [{k: _val(r.get(k)) for k in ("name", "type", "tier", "country")} | {"has_name_label": "name" in r} for r in recs]
        end = offs[j] if j < len(lines) else len(text)
        blocks.append({"start": start, "end": end, "records": recs})
        i = j
    return blocks


# ---------------------------------------------------------------- involved components ---------------------------------------------------
COMP_FIELD = re.compile(r"^[ \t]*component (name|description|part number)(?:[ \t]*\d+)?[ \t]*:[ \t]*(.*)$", re.I)
COMP_STOP = re.compile(r"^[ \t]*(?:supplier identification|component manufacturer|chronology|description of|identify how|recall schedule|"
                       r"tier of supplier|supplier type)", re.I)


def component_records(text: str):
    """-> (found_heading_or_fields: bool, records [{'name','desc','ptno'}], spans [(start,end)]) from 'Component Name/Description/Part Number'."""
    lines = text.split("\n")
    offs, o = [], 0
    for ln in lines:
        offs.append(o); o += len(ln) + 1
    recs, cur, field, spans, found = [], {}, None, [], False
    for j, ln in enumerate(lines):
        m = COMP_FIELD.match(ln)
        if m:
            found = True
            k = {"name": "name", "description": "desc", "part number": "ptno"}[m[1].lower()]
            if k == "name" and cur:
                recs.append(cur); cur = {}
            field = k
            cur[k] = m[2]
            spans.append((offs[j], offs[j] + len(ln)))
            continue
        if field and ln.strip() and not COMP_STOP.match(ln) and not PAGE_HDR.match(ln) and not FIELD.match(ln) and len(cur.get(field, "")) < 300:
            if cur.get(field, "").strip() == "":
                cur[field] = ln; spans.append((offs[j], offs[j] + len(ln)))
            continue
        if COMP_STOP.match(ln) or FIELD.match(ln):
            field = None
    if cur:
        recs.append(cur)
    return found, [{k: _val(r.get(k)) for k in ("name", "desc", "ptno")} for r in recs], spans


# ---------------------------------------------------------------- normalisation and matching ---------------------------------------------
LEGAL = {"inc", "incorporated", "llc", "ltd", "limited", "co", "company", "corp", "corporation", "plc", "gmbh", "ag", "sa", "sas", "spa", "srl",
         "bv", "nv", "kk", "oy", "ab", "as", "sl", "pty", "pvt", "private", "de", "cv", "the"}


def norm_name(s: str) -> str:
    """lowercase; strip accents; delete apostrophes and periods ("Q'Straint" -> qstraint, "S.A." -> sa); every other non-alphanumeric
    character -> space; drop the phrase 's a de c v' and the legal-form tokens; collapse spaces."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    s = re.sub(r"['\u2019\u2018.`]", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\bs a de c v\b", " ", s)
    return " ".join(t for t in s.split() if t not in LEGAL)


def match_exact(a: str, b: str) -> bool:
    na, nb = norm_name(a), norm_name(b)
    return bool(na) and na == nb


def match_contain(a: str, b: str) -> bool:
    """Token containment: one name's token set is a subset of the other's, and the shared tokens are >= 2, or one token of >= 5 characters."""
    ta, tb = set(norm_name(a).split()), set(norm_name(b).split())
    if not ta or not tb or not (ta <= tb or tb <= ta):
        return False
    shared = ta & tb
    return len(shared) >= 2 or (len(shared) == 1 and len(next(iter(shared))) >= 5)


def _indel_ratio(a: str, b: str) -> float:
    """rapidfuzz fuzz.ratio: 100 * (1 - indel_distance / (len a + len b)); indel distance = len a + len b - 2 * LCS."""
    if not a and not b:
        return 100.0
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0]
        for jj, cb in enumerate(b, 1):
            cur.append(prev[jj - 1] + 1 if ca == cb else max(prev[jj], cur[jj - 1]))
        prev = cur
    lcs = prev[-1]
    return 100.0 * (2 * lcs) / (len(a) + len(b))


def token_set_ratio(s1: str, s2: str) -> float:
    """Pure-Python reimplementation of rapidfuzz 3.x fuzz.token_set_ratio (no processor)."""
    a, b = set(s1.split()), set(s2.split())
    if not a or not b:
        return 0.0
    inter, dab, dba = a & b, a - b, b - a
    if inter and (not dab or not dba):
        return 100.0
    jab, jba = " ".join(sorted(dab)), " ".join(sorted(dba))
    lab, lba = len(jab), len(jba)
    sect = " ".join(sorted(inter)); ls = len(sect)
    res = _indel_ratio(jab, jba)
    if ls == 0:
        return res
    sab_len, sba_len = ls + 1 + lab, ls + 1 + lba
    r_ab = 100.0 * (1 - (1 + lab) / (ls + sab_len))
    r_ba = 100.0 * (1 - (1 + lba) / (ls + sba_len))
    return max(res, r_ab, r_ba)


def match_fuzzy(a: str, b: str, thr: float = 90.0) -> bool:
    na, nb = norm_name(a), norm_name(b)
    return bool(na and nb) and token_set_ratio(na, nb) >= thr


def ptno_norm(s: str) -> str:
    return re.sub(r"[\s\-]+", "", (s or "")).upper()


# ---------------------------------------------------------------- quote location ----------------------------------------------------------
def locate_quote(quote: str, text: str):
    """Character span of `quote` in `text`, whitespace-insensitive; a '[MASKED]' token (frozen evaluation masking) matches any short run.
    -> (start, end) or None."""
    toks = (quote or "").split()
    if not toks:
        return None
    parts = [r".{1,200}?" if t == "[MASKED]" else re.escape(t).replace(r"\[MASKED\]", r".{1,200}?") for t in toks]
    m = re.search(r"\s+".join(parts), text, re.S)
    return (m.start(), m.end()) if m else None


def inside(span, spans) -> bool:
    return span is not None and any(s <= span[0] and span[1] <= e for s, e in spans)
