"""HA-1 audit sheet, built from the draw committed under tag ha-protocol-1 (no model run). Prints counts and hashes only, never a verdict.
  TT_PDF, TT_GOLD, TT_CACHE, TT_RUN1, TT_RUN2 point at the uncommitted data (see scripts/ha1_draw.py)
  -> audit/HA1_sheet.csv, audit/HA1_sheet.html, audit/sealed/HA1_answer_key.json (not referenced by the sheet)"""
import csv
import hashlib
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ha1_draw as H

ROOT = Path(__file__).resolve().parents[1]
SIDE = 300
COLUMNS = ["ITEM", "FILING_ID", "PDF_URL", "CLAIMED_DATE", "CLAIMED_TYPE", "EVIDENCE_QUOTE", "SURROUNDING_TEXT", "DATE_OK", "TYPE_OK", "MINUTES", "NOTE"]
PAGE = (ROOT / "scripts" / "ha1_sheet_template.html")


def pdf_url(file):
    """Same layout as the frozen fetcher's static.nhtsa.gov paths: odi/rcl/<campaign year>/<file>."""
    return f"https://static.nhtsa.gov/odi/rcl/20{file[7:9]}/{file}"


def window(quote, text):
    """-> (before, matched, after) from the unmasked, whitespace-collapsed section, or None. A [MASKED] in the quote stands for the block name the agent did not see."""
    s = re.sub(r"\s+", " ", text).strip()
    parts = [r"\s*".join(re.escape(w) for w in p.split()) for p in re.split(r"\[MASKED\]", re.sub(r"\s+", " ", quote).strip())]
    m = re.search(r".{1,120}?".join(parts), s, re.I)
    if not m:
        return None
    a, b = max(0, m.start() - SIDE), min(len(s), m.end() + SIDE)
    if a > 0:
        a = s.find(" ", a) + 1 or a
    if b < len(s):
        b = s.rfind(" ", m.end(), b) if s.rfind(" ", m.end(), b) > 0 else b
    return ("… " if a > 0 else "") + s[a:m.start()], s[m.start():m.end()], s[m.end():b] + (" …" if b < len(s) else "")


def main():
    S = json.load(open(ROOT / "reports" / "ha1" / "HA1_SAMPLE.json"))
    acc, ex1, docs, _blocks = H.accepted_claims()
    assert len(acc) == H.N_POP and H.draw([(f, i) for _ok, f, i in acc])[3] == [int(x["repeat_of"][3:]) - 1 for x in S["items"][H.N_FILINGS:]], "not the committed draw"
    verdict = {(f, i): ok for ok, f, i in acc}
    rows, spans, missing = [], [], 0
    for it in S["items"]:
        f, i = it["file"], it["event_index"]
        e = ex1[f].events[i]
        w = window(e.evidence.quote, docs[f].sections.get(e.evidence.section, ""))
        if w is None:
            missing += 1
            w = ("", "", re.sub(r"\s+", " ", docs[f].sections.get(e.evidence.section, ""))[:2 * SIDE] + " …")
        spans.append(w)
        rows.append({"ITEM": it["item"], "FILING_ID": f.split("-")[1], "PDF_URL": pdf_url(f), "CLAIMED_DATE": e.date_text, "CLAIMED_TYPE": e.type, "EVIDENCE_QUOTE": e.evidence.quote,
                     "SURROUNDING_TEXT": "".join(w), "DATE_OK": "", "TYPE_OK": "", "MINUTES": "", "NOTE": ""})
    audit = ROOT / "audit"; (audit / "sealed").mkdir(parents=True, exist_ok=True)
    with open(audit / "HA1_sheet.csv", "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.DictWriter(fh, COLUMNS); wr.writeheader(); wr.writerows(rows)
    secs = []
    for r, (a, m, b) in zip(rows, spans):
        secs.append(f'<section class="item" id="{r["ITEM"]}"><header><h2>{r["ITEM"]}</h2><span class="filing">{html.escape(r["FILING_ID"])}</span>'
                    f'<a href="{html.escape(r["PDF_URL"])}" target="_blank" rel="noopener noreferrer">Open the PDF</a></header>'
                    f'<dl><div><dt>Claimed date</dt><dd>{html.escape(r["CLAIMED_DATE"])}</dd></div><div><dt>Claimed type</dt><dd>{html.escape(r["CLAIMED_TYPE"])}</dd></div></dl>'
                    f'<h3>Evidence quote</h3><blockquote>{html.escape(r["EVIDENCE_QUOTE"])}</blockquote>'
                    f'<h3>Surrounding chronology</h3><p class="ctx">{html.escape(a)}<mark>{html.escape(m)}</mark>{html.escape(b)}</p></section>')
    (audit / "HA1_sheet.html").write_text(PAGE.read_text().replace("<!--ITEMS-->", "\n".join(secs)), encoding="utf-8")
    key = {"note": "SEALED. Do not open until the filled sheet is committed (reports/HA_PROTOCOL.md, section C).",
           "items": [{"item": it["item"], "silver_correct": bool(verdict[(it["file"], it["event_index"])])} for it in S["items"]],
           "mean_silver_correct_536": sum(map(bool, verdict.values())) / len(verdict)}
    json.dump(key, open(audit / "sealed" / "HA1_answer_key.json", "w"), indent=1)
    # blinding checks, on what the auditor can see
    tmpl = PAGE.read_text().lower()
    for word in ("silver", "accepted", "gate", "score", "verdict", "answer_key", "sealed", "b1", "b2"):
        assert not re.search(rf"\b{word}\b", tmpl), word
    assert list(csv.DictReader(open(audit / "HA1_sheet.csv", encoding="utf-8-sig")))[0].keys() == set(COLUMNS)
    pairs = {x["item"]: x["repeat_of"] for x in S["items"]}
    assert all(rows[n]["EVIDENCE_QUOTE"] == rows[int(pairs[rows[n]["ITEM"]][3:]) - 1]["EVIDENCE_QUOTE"] for n in range(H.N_FILINGS, len(rows)))
    assert len({r["FILING_ID"] for r in rows}) == H.N_FILINGS
    print(f"rows {len(rows)}; quote located {len(rows) - missing}/{len(rows)}; context chars min {min(len(r['SURROUNDING_TEXT']) for r in rows)} max {max(len(r['SURROUNDING_TEXT']) for r in rows)}; "
          f"cells starting with a spreadsheet formula character {sum(r[c][:1] in '=+@-' and bool(r[c]) for r in rows for c in ('EVIDENCE_QUOTE', 'SURROUNDING_TEXT'))}; "
          f"key sha256 {hashlib.sha256(open(audit / 'sealed' / 'HA1_answer_key.json', 'rb').read()).hexdigest()}")


if __name__ == "__main__":
    main()
