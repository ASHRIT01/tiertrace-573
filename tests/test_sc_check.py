"""SC-1 supplier check: unit tests (protocol sc-protocol-1, sections B, C, D, E). Pure Python, synthetic inputs only."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sc_inventory import stratum  # noqa: E402
from sc_lib import (component_records, inside, locate_quote, match_contain, match_exact, match_fuzzy, norm_name, ptno_norm,  # noqa: E402
                    supplier_blocks, token_set_ratio, _indel_ratio)


# ---- B. normalisation
def test_dare_auto():
    assert norm_name("Dare Auto Inc") == norm_name("DARE AUTO, INC.") == "dare auto"
    assert match_exact("Dare Auto Inc", "DARE AUTO, INC.")


def test_legal_forms_accents_and_sadecv():
    assert norm_name("Industrias Mecánicas S.A. de C.V.") == "industrias mecanicas"
    assert norm_name("Industrias Mecanicas S A DE C V") == "industrias mecanicas"
    assert norm_name("The Bosch GmbH") == "bosch"
    assert norm_name("Q'Straint") == norm_name("Qstraint")
    assert norm_name("GLOBAL LINK DISTRIBUTION,CORP") == "global link distribution"


def test_empty_never_matches():
    assert not match_exact("Inc.", "LLC") and not match_exact("", "")


# ---- B. containment edge cases
def test_containment_single_long_token():
    assert match_contain("Bosch", "Robert Bosch LLC")                     # shared 'bosch' (5 characters)


def test_containment_single_short_token_fails():
    assert not match_contain("ZF", "ZF Group") and not match_contain("Lear", "Lear Seating")   # 'zf' 2, 'lear' 4 characters


def test_containment_two_tokens():
    assert match_contain("Joyson Safety", "Joyson Safety Systems")


def test_containment_needs_subset():
    assert not match_contain("Bosch Rexroth", "Robert Bosch")


# ---- B. fuzzy (pure-Python rapidfuzz token_set_ratio)
def test_token_set_ratio_known_values():
    assert token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear") == 100.0
    assert token_set_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear") == 100.0
    assert abs(_indel_ratio("this is a test", "this is a test!") - 96.55172413793103) < 1e-9
    assert token_set_ratio("", "abc") == 0.0


def test_fuzzy_threshold():
    assert match_fuzzy("Continental Automotive Systems", "Continental Automotive Sytems")
    assert not match_fuzzy("Denso", "Delphi")


# ---- C. strata (OEM_SELF detection)
def _rec(name, typ=None):
    return {"name": name, "type": typ, "tier": None, "country": None, "has_name_label": True}


def test_oem_self_by_filer_name():
    assert stratum([_rec("Autocar LLC")], {"AUTOCAR, LLC"}) == "OEM_SELF"


def test_oem_type_is_not_self_in_primary_but_is_in_literal():
    recs = [_rec("DENSO CORPORATION", "OEM")]
    assert stratum(recs, {"Toyota Motor Engineering"}) == "NAMED_SUPPLIER"
    assert stratum(recs, {"Toyota Motor Engineering"}, literal_oem=True) == "OEM_SELF"


def test_other_strata():
    assert stratum([_rec(None)], {"X"}) == "BLANK"
    assert stratum([_rec("See - Supplier.pdf")], {"X"}) == "BLANK"
    assert stratum([_rec("Alpha Parts"), _rec("Beta Parts")], {"X"}) == "MULTIPLE"
    assert stratum([_rec("Gamma Supply", "Distributor")], {"X"}) == "OBTAINED_FROM"
    assert stratum([], {"X"}) == "PARSE_FAIL"


# ---- block parser: both layouts, address never kept
OLDER = "Component Part Number : 123\nSupplier Identification :\nComponent Manufacturer\nName : DARE AUTO, INC.\nAddress : 1 Main Street\n Town MI 48000\nCountry : United States\nChronology :\nOn May 1, 2023, Dare Auto Inc notified the filer.\n"
PORTAL = "Component Manufacturer\nTier of Supplier:\nTier 1\nSupplier Type:\nOEM\nName:\nAlpha Parts GmbH\nAddress:\nStrasse 5\n12345 Stadt\nCountry:\nGermany\nInvolved Components\nComponent Name 1:\nBrake Hose\nComponent Description:\nFront hose\nComponent Part Number:\nBH-100 20\n"


def test_parse_older_and_portal_without_address():
    b = supplier_blocks(OLDER)[0]["records"][0]
    assert (b["name"], b["country"]) == ("DARE AUTO, INC", "United States") and "address" not in b   # trailing punctuation stripped by _val
    p = supplier_blocks(PORTAL)[0]["records"][0]
    assert (p["name"], p["type"], p["tier"], p["country"]) == ("Alpha Parts GmbH", "OEM", "Tier 1", "Germany")
    assert all("Strasse" not in str(v) and "Main Street" not in str(v) for v in list(b.values()) + list(p.values()))


# ---- E. part number
def test_part_number_match():
    found, recs, _ = component_records(PORTAL)
    assert found and recs[0]["name"] == "Brake Hose"
    assert ptno_norm(recs[0]["ptno"]) == ptno_norm("BH100-20") == "BH10020"


# ---- D. in-block span detection
def test_in_block_and_out_of_block():
    blk = supplier_blocks(OLDER)[0]
    s_in = locate_quote("Name : DARE AUTO, INC.", OLDER)
    s_out = locate_quote("On May 1, 2023, Dare Auto Inc notified the filer.", OLDER)
    assert inside(s_in, [(blk["start"], blk["end"])]) and not inside(s_out, [(blk["start"], blk["end"])])
    assert locate_quote("On May 1, 2023, [MASKED] notified   the filer.", OLDER) == s_out
    assert locate_quote("not in the text", OLDER) is None and not inside(None, [(0, 10)])
