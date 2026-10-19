"""Blind labelling guard. Silver labelling of Test-A, Test-B and unseen-filer filings must be done blind to every model and baseline
output (4B, 2B, B0, B1). Model outputs live under runs/, so every labelling command and pipeline function refuses a path that is inside
runs/ (or has a directory named `runs` anywhere in it), whether it would be read or written. Labelling scratch goes under data/labels/work/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN = ROOT / "runs"


class BlindViolation(RuntimeError):
    pass


def assert_blind(*paths) -> None:
    for p in paths:
        if p is None or str(p) == "":
            continue
        r = (Path(p) if Path(p).is_absolute() else Path.cwd() / p).resolve()
        if r == FORBIDDEN or FORBIDDEN in r.parents or "runs" in r.parts:
            raise BlindViolation(f"Refusing {str(p)!r}: labelling must be blind to model and baseline outputs, which are stored under runs/. "
                                 f"Use data/labels/work/<split>/ for labelling scratch files.")
