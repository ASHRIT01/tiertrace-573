import zipfile
from tt.data.flat import campaign_id, load_campaigns, FIELDS


def _row(camp, typ="V", comp_name="", ptno=""):
    f = [""] * 29
    f[FIELDS.index("RECORD_ID")] = "1"; f[FIELDS.index("CAMPNO")] = camp; f[FIELDS.index("RCLTYPECD")] = typ
    f[FIELDS.index("MFGNAME")] = "ACME"; f[FIELDS.index("MFR_COMP_NAME")] = comp_name; f[FIELDS.index("MFR_COMP_PTNO")] = ptno
    return "\t".join(f)


def test_campaign_id():
    assert campaign_id("24V418000") == "24V418" and campaign_id("98V123") is None


def test_load_one_row_per_campaign(tmp_path):
    z = tmp_path / "f.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("x.txt", "\n".join([_row("24V418000"), _row("24V418000", ptno="123"), _row("14V001000"),
                                        _row("23E052000", "E"), "bad\trow"]))
    rows = load_campaigns(z, 2015, "VE")
    assert [r["campaign"] for r in rows] == ["23E052", "24V418"]
    assert rows[1]["n_rows"] == 2 and rows[1]["has_part_no"] and not rows[1]["has_mfr_comp_name"]
