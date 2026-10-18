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


def event_date_failures(labels: list[dict]) -> list[tuple[str, str, str, str]]:
    """[(file, event number, date_text, quote)] for events whose date text is not inside the quote."""
    out = []
    for L in labels:
        for i, e in enumerate(L.get("events", []), 1):
            if not date_in_quote(e["date_text"], e["quote"]):
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
           "E = dated event (the date text must appear inside its quote). C = cause. U = supplier-chain involvement in the narrative: NAMED / UNNAMED /",
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
        for i, e in enumerate(L.get("events", []), 1):
            line(f"E{i}", f"{e['date_text']} — {e['type']}", "SUPPORTED", e["quote"], "chronology",
                 "" if date_in_quote(e["date_text"], e["quote"]) else "**DATE NOT IN QUOTE**")
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
    fails = event_date_failures(labels)
    n_ev = sum(len(L.get("events", [])) for L in labels)
    out.insert(2, f"Event date check: {n_ev - len(fails)} of {n_ev} events have the date text inside the quote" + ("" if not fails else f"; **{len(fails)} fail**") + ".")
    out.insert(3, f"Quote check: {total - bad} of {total} quotes located by code" + ("" if not bad else f"; **{bad} NOT FOUND**") + ".")
    return "\n".join(out)
