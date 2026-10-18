"""Local parse of NHTSA FLAT_RCL_POST_2010.zip (29 tab-separated fields; layout in RCL.txt).
Reads the user-supplied file only; never downloads."""
import csv
import re
import zipfile
import io
from pathlib import Path

FIELDS = ["RECORD_ID", "CAMPNO", "MAKETXT", "MODELTXT", "YEARTXT", "MFGCAMPNO", "COMPNAME", "MFGNAME",
          "BGMAN", "ENDMAN", "RCLTYPECD", "POTAFF", "ODATE", "INFLUENCED_BY", "MFGTXT", "RCDATE", "DATEA",
          "RPNO", "FMVSS", "DESC_DEFECT", "CONEQUENCE_DEFECT", "CORRECTIVE_ACTION", "NOTES", "RCL_CMPT_ID",
          "MFR_COMP_NAME", "MFR_COMP_DESC", "MFR_COMP_PTNO", "DO_NOT_DRIVE", "PARK_OUTSIDE"]
_CAMP = re.compile(r"^(\d{2})([VECT])(\d{3})\d{3}$")


def campaign_id(campno: str) -> str | None:
    """'24V418000' -> '24V418'. None for pre-2000-style or malformed ids."""
    m = _CAMP.match(campno.strip().upper())
    return f"{m[1]}{m[2]}{m[3]}" if m else None


def load_campaigns(zip_path: str | Path, first_year: int = 2015, types: str = "VE") -> list[dict]:
    """One row per campaign (first row by RECORD_ID) filed in `first_year`+, with n_rows and the
    distinct manufacturer-supplied component fields kept as counts of non-empty values."""
    out: dict[str, dict] = {}
    with zipfile.ZipFile(zip_path) as z:
        name = z.namelist()[0]
        with z.open(name) as raw:
            for line in io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""):
                f = line.rstrip("\r\n").split("\t")
                if len(f) != 29:
                    continue
                r = dict(zip(FIELDS, f))
                cid = campaign_id(r["CAMPNO"])
                if not cid or 2000 + int(cid[:2]) < first_year or cid[2] not in types:
                    continue
                c = out.get(cid)
                if c is None:
                    c = out[cid] = {"campaign": cid, "year": 2000 + int(cid[:2]), "type": r["RCLTYPECD"] or cid[2],
                                    "filer": r["MFGNAME"], "component": r["COMPNAME"], "rcdate": r["RCDATE"],
                                    "potaff": r["POTAFF"], "n_rows": 0, "has_mfr_comp_name": False,
                                    "has_part_no": False}
                c["n_rows"] += 1
                c["has_mfr_comp_name"] |= bool(r["MFR_COMP_NAME"].strip())
                c["has_part_no"] |= bool(r["MFR_COMP_PTNO"].strip())
    return sorted(out.values(), key=lambda c: c["campaign"])


def write_csv(rows: list[dict], path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
