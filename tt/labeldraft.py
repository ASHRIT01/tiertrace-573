"""Draft-label tooling. Labels are AI-DRAFTED and must be human-reviewed.
Input: a JSON list of per-filing label dicts (see render()). Every quote is located in the named section with the same
normalisation as verifier V1 (NFKC, lowercase, whitespace collapsed); quotes that are not found are flagged in the output."""
import json
from pathlib import Path

from tt.parse.block import parse_block, raw_block
from tt.parse.pdf import extract_text
from tt.parse.sections import clean, norm, parse_header, split_sections

REVIEW = "review: [ ] yes  [ ] no  [ ] fix: ________"


def load(pdf: Path) -> dict:
    text, _ = extract_text(pdf)
    sec = split_sections(text)
    sec["block"] = raw_block(text)
    return {"text": text, "clean": clean(text), "sections": sec, "header": parse_header(text), "block": parse_block(raw_block(text))}


def found(quote: str, section: str, doc: dict) -> bool:
    body = doc["clean"] if section == "any" else doc["sections"].get(section, "")
    return norm(quote) in norm(body)


def date_in_quote(date_text: str, quote: str) -> bool:
    """An event's date text must appear inside its quote (the quote spans date and event)."""
    return norm(date_text) in norm(quote)


def event_date_failures(labels: list[dict], pdf_dir: Path | None = None) -> list[tuple[str, str, str, str]]:
    """[(file, event number, date_text, quote)] for events that break the date rule.
    Own-date event: the date text must appear inside its quote. Inherited-date event (inherited_date=True): the date text must
    appear inside its entry_quote (the dated sentence of the same entry); with pdf_dir, the entry_quote must also be located in the
    chronology at or before the event's quote."""
    out = []
    for L in labels:
        chron = ""
        if pdf_dir is not None:
            chron = norm(load(pdf_dir / L["file"])["sections"].get("chronology", ""))
        for i, e in enumerate(L.get("events", []), 1):
            if e.get("inherited_date"):
                ok = date_in_quote(e["date_text"], e.get("entry_quote", ""))
                if ok and pdf_dir is not None:
                    pe, pq = chron.find(norm(e["entry_quote"])), chron.find(norm(e["quote"]))
                    ok = 0 <= pe <= pq
            else:
                ok = date_in_quote(e["date_text"], e["quote"])
            if not ok:
                out.append((L["file"], f"E{i}", e["date_text"], e["quote"]))
    return out


def show(pdf: Path, maxlen: int = 2600) -> str:
    d = load(pdf)
    s, b, h = d["sections"], d["block"], d["header"]
    return "\n".join([f"##### {pdf.name}  filer={h['filer']!r} date={h['filing_date']}",
                      f"BLOCK: name={b.name!r} tier={b.tier!r} type={b.type!r} country={b.country!r}",
                      "DEFECT: " + s.get("defect", "")[:500], "CAUSE: " + s.get("cause", "")[:900],
                      "CHRONOLOGY: " + s.get("chronology", "")[:maxlen], ""])


def render(labels: list[dict], pdf_dir: Path) -> str:
    out = ["# Dev labels: DRAFT, AI-drafted, to be human-reviewed", "",
           "Nothing here is verified by a person. Every quote below was checked by code to appear verbatim (whitespace-normalised) in the",
           "named section of the filing; a line marked **QUOTE NOT FOUND** needs fixing. For each claim write yes / no / fix on the review line.",
           "Statuses: SUPPORTED (a passage directly supports it), INSUFFICIENT (the text does not settle it), NOT_REPORTED (the information is absent/NR).",
           "Claim layers: S1 = block-reported component manufacturer (the filing's own field). S2 = supplier named in the NARRATIVE (cause or chronology),",
           "the mask-and-recover target: SUPPORTED only with a quote, otherwise INSUFFICIENT (name absent from the narrative) or NOT_REPORTED (nothing to name).",
           "E = event: one per sentence of a dated entry; the date is the sentence's own, or inherited from its entry (then the entry sentence is shown). C = cause. U = supplier-chain involvement in the narrative: NAMED / UNNAMED /",
           "NONE_MENTIONED (the narrative is present and mentions none) / NOT_REPORTED (chronology is a pointer or NR, so the narrative cannot settle it).", ""]
    bad = total = 0
    for n, L in enumerate(labels, 1):
        d = load(pdf_dir / L["file"])
        b, h = d["block"], d["header"]
        out += [f"## {n}. {L['file']}  ({L['year']})", f"Filer: {h['filer']}  |  filing date: {h['filing_date']}  |  block supplier (parsed): {b.name!r}, tier {b.tier!r}, country {b.country!r}", ""]
        def line(cid, label, status, quote, section, extra=""):
            nonlocal bad, total
            if quote:
                total += 1
                ok = found(quote, section, d)
                bad += not ok
                q = f'"{quote}" [{section}]' + ("" if ok else "  **QUOTE NOT FOUND**")
            else:
                q = "(no quote: none exists)"
            out.append(f"- **{cid}** {label} — **{status}** {extra} — {q}\n  - {REVIEW}")
        for c in L["claims"]:
            line(c["id"], c["label"], c["status"], c.get("quote", ""), c.get("section", "any"))
        bad_ev = {(f, n) for f, n, _, _ in event_date_failures([L], pdf_dir)}
        for i, e in enumerate(L.get("events", []), 1):
            tag = "" if (L["file"], f"E{i}") not in bad_ev else "**DATE CHECK FAILED**"
            if e.get("inherited_date"):
                tag = (f"(date inherited from its entry; entry sentence: \"{e['entry_quote']}\") " + tag).strip()
                total += 1
                bad += not found(e["entry_quote"], "chronology", d)
            line(f"E{i}", f"{e['date_text']} — {e['type']}", "SUPPORTED", e["quote"], "chronology", tag)
        if not L.get("events"):
            out.append("- **E** dated events — **NOT_REPORTED** (no dated event in the chronology)\n  - " + REVIEW)
        c = L["cause"]
        line("C", "Cause: " + c["label"], c["status"], c.get("quote", ""), c.get("section", "cause"))
        u = L["upstream"]
        names = f" ({', '.join(u['names'])})" if u.get("names") else ""
        q = f'"{u["quote"]}" [{u.get("section", "any")}]' if u.get("quote") else "(no quote)"
        if u.get("quote"):
            total += 1
            ok = found(u["quote"], u.get("section", "any"), d)
            bad += not ok
            q += "" if ok else "  **QUOTE NOT FOUND**"
        out.append(f"- **U** Upstream involvement in the narrative: **{u['kind']}**{names} — {q}\n  - {REVIEW}")
        for fl in L.get("flags", []):
            out.append(f"- FLAG: {fl}")
        if L.get("note"):
            out.append(f"- note: {L['note']}")
        out.append("")
    fails = event_date_failures(labels, pdf_dir)
    n_ev = sum(len(L.get("events", [])) for L in labels)
    out.insert(2, f"Event date check: {n_ev - len(fails)} of {n_ev} events pass the date rule (own date inside the quote, or date inherited from the entry sentence)" + ("" if not fails else f"; **{len(fails)} fail**") + ".")
    out.insert(3, f"Quote check: {total - bad} of {total} quotes located by code" + ("" if not bad else f"; **{bad} NOT FOUND**") + ".")
    return "\n".join(out)


# ---- sentence-end logic used to extend event quotes (chronology text is whitespace-collapsed)
import re as _re

_ABBR = {"u.s", "no", "inc", "corp", "co", "ltd", "mr", "mrs", "dr", "st", "vs", "a.m", "p.m", "e.g", "i.e", "jan", "feb", "mar", "apr", "jun",
         "jul", "aug", "sep", "sept", "oct", "nov", "dec", "approx", "dept", "mfg", "mgr", "eng", "fig"}
_PREP = {"on", "in", "of", "by", "from", "to", "since", "until", "through", "and", "between", "as", "or", "about", "before", "after", "at",
         "than", "during", "within", "the", "with", "for", "that"}
_MON = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?"
_DATE = _re.compile(rf"(?:{_MON}\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}|\d{{1,2}}/\d{{1,2}}/\d{{2,4}}|\d{{4}}-\d{{2}}-\d{{2}})")


def sentence_end(c: str, e: int) -> int:
    """Index just past the end of the sentence (or, in a list with no periods, the entry) containing position e-1 of `c`."""
    if e >= len(c):
        return len(c)
    if c[e - 1] in ".!?" or (c[e - 1] in "\u201d\")" and e >= 2 and c[e - 2] in ".!?"):
        return e
    i = e
    while i < len(c):
        ch = c[i]
        if ch == "\u2022":
            return len(c[:i].rstrip(" -\u2013"))
        if ch in ".!?" and (i + 1 >= len(c) or c[i + 1] in " \u201d\")'"):
            w = _re.search(r"([A-Za-z.]+)$", c[:i])
            tok = (w.group(1) if w else "").lower().strip(".")
            if tok not in _ABBR and not (tok.isdigit() and i + 1 < len(c) and c[i + 1:i + 3].strip().isdigit()):
                j = i + 1
                while j < len(c) and c[j] in "\u201d\")'":
                    j += 1
                return j
        if ch == " ":
            m = _DATE.match(c, i + 1)
            if m:
                pw = _re.search(r"([A-Za-z]+)$", c[:i])
                if not (pw and pw.group(1).lower() in _PREP):
                    return len(c[:i].rstrip(" -\u2013"))
        i += 1
    return len(c)


def ends_at_sentence_end(quote: str, chronology: str) -> bool:
    """True if the quote (located in the chronology) already ends where its sentence/entry ends."""
    c = _re.sub(r"\s+", " ", chronology).strip()
    q = _re.sub(r"\s+", " ", quote).strip()
    s = c.lower().find(q.lower())
    return s >= 0 and sentence_end(c, s + len(q)) == s + len(q)
