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
