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


def test_page_break_marker_removed_from_cause():
    from tt.parse.sections import split_sections
    t = ("Description of the Cause : A spacer lacks clearance and forces the shaft key out of \n\nPage \n2\n\n"
         "position. The gear may move.\nIdentification of Any Warning that can Occur : none\nChronology :\nOn May 1, 2015 it began.\n")
    s = split_sections(t)
    assert "Page" not in s["cause"] and "key out of position. The gear may move." in s["cause"]


def test_page_x_of_y_and_inline_marker_removed():
    from tt.parse.sections import clean
    assert "Page" not in clean("alpha\nPage 2 of 4\nbeta\nPage 3\ngamma\n")


def test_stacked_header_block_removed_from_risk_and_keeps_filing_date():
    from tt.parse.sections import split_sections, parse_header
    from datetime import date
    t = ("U.S. Department\nof Transportation\nNational Highway\nTraffic Safety\nAdministration\n"
         "Part 573 Safety Recall Report\n26V622\nManufacturer Name: Chrysler (FCA US, LLC)\nSubmission Date: Sep 29, 2026\n"
         "NHTSA Recall No.: 26V622\nManufacturer Recall No.: 94D\nThe information contained in this report was submitted pursuant to 49 CFR § 573\n"
         "OMB Control No.:2127-0004\n\nDescription of the safety risk:\nA wheel may detach\n"
         "U.S. Department\nof Transportation\nNational Highway\nTraffic Safety\nAdministration\nPart 573 Safety Recall Report\n26V622\n"
         "Manufacturer Name: Chrysler (FCA US, LLC)\nSubmission Date: Sep 29, 2026\nNHTSA Recall No.: 26V622\nManufacturer Recall No.: 94D\n"
         "The information contained in this report was submitted pursuant to 49 CFR § 573\nOMB Control No.:2127-0004\n\nand injure people.\n"
         "Description of the cause:\nA bolt was loose.\nIdentification of any warning that can occur:\nNone\n")
    s = split_sections(t)
    assert s["risk"] == "A wheel may detach and injure people." and s["cause"] == "A bolt was loose."
    assert parse_header(t)["filing_date"] == date(2026, 9, 29)
