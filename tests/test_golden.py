"""Golden tests on the six reference filings. PDFs are not redistributed:
run `tt fetch-list` to populate data/raw first; tests skip if absent."""
from datetime import date
from pathlib import Path
import pytest

from tt.parse.block import parse_block, raw_block
from tt.parse.pdf import extract_text
from tt.parse.sections import parse_header, split_sections

RAW = Path(__file__).parent.parent / "data" / "raw"

# file -> (filer, filing date, supplier name, tier, type, country, cause is NR/blank, chronology snippet)
GOLD = {
    "RCLRPT-24V418-6316.PDF": ("General Motors, LLC", date(2024, 7, 25), "ZF Group", None, None, "United States", False, "Speak Up For Safety"),
    "RCLRPT-24V284-8773.PDF": ("Tesla, Inc.", date(2024, 4, 19), "Autoliv, Inc.", None, None, "United States", True, "Jidoka"),
    "RCLRPT-24V795-9882.PDF": ("General Motors, LLC", date(2024, 10, 24), "Yanfeng Ramos Arizpe", None, None, "Mexico", False, "supplier quality engineer"),
    "RCLRPT-25V446-2933.pdf": ("Terminal Investment Corporation", date(2025, 6, 30), "Blackhawk Industries", "Tier 1", "Distributor", "United States", False, "non-DOT product was supplied"),
    "RCLRPT-23E052-7894.PDF": ("Dana Incorporated", date(2023, 10, 3), "Productos Especializados de Acero, S.A.", None, None, "Mexico", False, "Freightliner"),
    "RCLRPT-26E042-9936.pdf": ("Prime-Time Specialty Vehicles", date(2026, 7, 13), "Q'Straint", "Tier 1", "OEM", "United States", True, "Q'Straint delivered a written notice"),
}


@pytest.mark.parametrize("fname", GOLD)
def test_golden(fname):
    path = RAW / fname
    if not path.exists():
        pytest.skip("run `tt fetch-list` first")
    filer, fdate, name, tier, typ, country, nr, snippet = GOLD[fname]
    text, empty = extract_text(path)
    assert empty == []  # text layer on every page
    h = parse_header(text)
    assert (h["filer"], h["filing_date"]) == (filer, fdate)
    b = parse_block(raw_block(text))
    assert (b.name, b.tier, b.type, b.country) == (name, tier, typ, country)
    s = split_sections(text)
    assert snippet in s["chronology"]
    assert (s.get("cause", "").strip().lower() in {"", "nr"}) == nr
