from datetime import date
from tt.verify.dates import parse_date
from tt.parse.block import parse_block, mask_text
from tt.parse.sections import Doc, split_sections
from tt.norm.aliases import AliasTable
from tt.agent.schemas import Extraction, Company, Event, Evidence
from tt.verify.verifier import verify

A = date(2024, 6, 30)


def test_dates():
    assert parse_date("February 5, 2024", A) == date(2024, 2, 5)
    assert parse_date("02/05/2024", A) == date(2024, 2, 5)
    assert parse_date("late April", A) == date(2024, 4, 25)
    assert parse_date("mid-May", A) == date(2024, 5, 15)
    assert parse_date("December", A) == date(2023, 12, 1)  # not after anchor
    assert parse_date("sometime soon", A) is None


def test_block_and_mask():
    t = "Name: ZF Group\nTier of Supplier:\nNR\nSupplier Type:\nManufacturer\nCountry:\nGermany"
    b = parse_block(t)
    assert (b.name, b.tier, b.type, b.country) == ("ZF Group", None, "Manufacturer", "Germany")
    assert "ZF Group" not in mask_text("ZF Group notified GM", b.name)


def test_sections():
    s = split_sections("Description of the Cause:\nNR\nChronology:\nOn March 1, 2024 supplier told us.\n")
    assert s["cause"] == "NR" and "supplier told us" in s["chronology"]


def mkdoc(cause="Machine misadjusted after maintenance."):
    chron = "On March 1, 2024 ZF Group notified General Motors of a defect."
    return Doc("24V418", "General Motors", date(2024, 4, 1), cause + " " + chron,
               {"cause": cause, "chronology": chron})


def ex(quote="ZF Group notified General Motors", name="ZF Group", date_text="March 1, 2024", cause_reported=True):
    ev = Evidence(section="chronology", quote=quote)
    return Extraction(
        companies=[Company(name=name, role="SUPPLIER", status="SUPPORTED", evidence=ev)],
        supply_path=["General Motors", name], locus="UNDETERMINED", locus_status="INSUFFICIENT",
        events=[Event(date_text=date_text, type="SUPPLIER_NOTICE", status="SUPPORTED", evidence=ev)],
        cause_reported=cause_reported)


AL = AliasTable()


def test_verifier_ok():
    assert verify(ex(), mkdoc(), AL) == []


def test_verifier_forged_quote_future_date_filer_nr():
    assert any(e.startswith("V1") for e in verify(ex(quote="ZF forged this"), mkdoc(), AL))
    assert any(e.startswith("V3") for e in verify(ex(date_text="May 5, 2024"), mkdoc(), AL))
    assert any("filer listed" in e for e in verify(ex(name="General Motors"), mkdoc(), AL))
    assert any(e.startswith("V4") for e in verify(ex(), mkdoc(cause="NR"), AL))
    assert any(e.startswith("V2") for e in verify(ex(name="Acme Corp"), mkdoc(), AL))
