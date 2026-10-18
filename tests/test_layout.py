from pathlib import Path
import pytest
from tt.parse.layout import detect_layout
from tt.parse.report import build_report, check_pdf

RAW = Path(__file__).parent.parent / "data" / "raw"
EXPECT = {"RCLRPT-24V418-6316.PDF": "inline", "RCLRPT-24V284-8773.PDF": "inline",
          "RCLRPT-24V795-9882.PDF": "inline", "RCLRPT-23E052-7894.PDF": "inline",
          "RCLRPT-25V446-2933.pdf": "stacked", "RCLRPT-26E042-9936.pdf": "stacked"}


def test_layout_synthetic():
    assert detect_layout("Name : ZF Group\nAddress : x\nCountry : US\n") == "inline"
    assert detect_layout("Name:\nZF Group\nAddress:\nx\n") == "stacked"
    assert detect_layout("nothing here") == "unknown"


@pytest.mark.parametrize("fname", EXPECT)
def test_layout_real(fname):
    if not (RAW / fname).exists():
        pytest.skip("run `tt fetch-list` first")
    r = check_pdf(RAW / fname)
    assert r["layout"] == EXPECT[fname] and r["fails"] == []


def test_header_date_without_space_after_comma():
    from tt.parse.sections import parse_header
    from datetime import date
    t = "Manufacturer Name :  Acme\nSubmission Date : JAN 26,2015\nNHTSA Recall No. : 15V-049\n"
    assert parse_header(t)["filing_date"] == date(2015, 1, 26)


def test_narrative_rules():
    from tt.narrative import companies, narrative_dates
    assert "Allison Transmission Inc." in " ".join(companies("Nova Bus receives a letter from Allison Transmission Inc. informing"))
    d = narrative_dates("2023-02-16 Issue found. 09/06/18 letter. On 5-May-2020 a call.", set())
    assert len(d) == 3


def test_mask_classify():
    from tt.maskrecover import classify
    from tt.norm.aliases import AliasTable
    al = AliasTable()
    assert classify("Hale Products Inc", "notice from Hale Products received", al)[0] in ("M1", "M2")
    assert classify("Bendix Commercial Vehicle Systems, LLC", "email from Bendix says", al)[0] == "PARTIAL"
    assert classify("Acme Corp", "the supplier shipped bad steel", al)[0] == "INFERENTIAL"
