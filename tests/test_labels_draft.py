import json
import re
from pathlib import Path

import pymupdf
import pytest

from tt.labeldraft import ends_at_sentence_end, event_date_failures, load, render

ROOT = Path(__file__).parent.parent
LABELS = ROOT / "reports" / "dev_labels_draft.json"
MD = ROOT / "reports" / "dev_labels_draft.md"
DEV = ROOT / "data" / "dev_raw"
pytestmark = pytest.mark.skipif(not DEV.exists(), reason="run `tt dev-fetch` first")


def _flat(s: str) -> str:
    return re.sub(r"\s+", "", s).lower()


def test_headings_match_records_pdf_filer_and_date():
    L = json.load(open(LABELS))
    md = MD.read_text()
    blocks = re.findall(r"^## (\d+)\. (\S+)  \((\d{4})\)\nFiler: (.*?)  \|  filing date: (\S+)  \|", md, re.M)
    assert len(blocks) == len(L) == 30
    for (n, fname, year, filer, fdate), rec in zip(blocks, L):
        assert int(n) == L.index(rec) + 1
        assert fname == rec["file"] and int(year) == rec["year"]
        # independent check against the PDF's own text: campaign number, filer and submission date as printed
        raw = "\n".join(p.get_text() for p in pymupdf.open(DEV / fname))
        flat = _flat(raw)
        camp = re.match(r"RCLRPT-(\d\d[VE]\d{3})-", fname).group(1)
        assert _flat(camp[:3] + "-" + camp[3:]) in flat or _flat(camp) in flat, fname
        assert _flat(filer) in flat, (fname, filer)
        y, mo, d = fdate.split("-")
        mon = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"][int(mo) - 1]
        assert _flat(f"{mon} {int(d):02d}, {y}") in flat or _flat(f"{mon} {int(d)}, {y}") in flat or _flat(f"{mon[0]}{mon[1:].lower()} {int(d):02d}, {y}") in flat, (fname, fdate)


def test_render_is_stable_and_matches_committed_md():
    L = json.load(open(LABELS))
    assert render(L, DEV) == MD.read_text()
    assert render(L, DEV) == render(L, DEV)


def test_event_quotes_have_date_and_end_at_sentence_end():
    L = json.load(open(LABELS))
    assert event_date_failures(L) == []
    for rec in L:
        chron = load(DEV / rec["file"])["sections"].get("chronology", "")
        cut = "cut at a clause boundary" in rec.get("note", "")
        for i, e in enumerate(rec["events"], 1):
            assert len(e["quote"]) <= 300
            if not cut:
                assert ends_at_sentence_end(e["quote"], chron), (rec["file"], i, e["quote"][-60:])
