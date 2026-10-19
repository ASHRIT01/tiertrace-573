"""Runs `python -m tt.cli ...` with ONE runtime guard and no change to any frozen file: tt.labels.dates.parse_span raises AttributeError on a
year-less fuzzy date ("mid-April", "early October"); here that case returns None, which parse_span already returns for other dates it cannot
parse. See reports/DEVIATIONS.md D-T2."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import importlib
import tt.labels.dates as D

_orig = D.parse_span


def parse_span(text, years=None, filing=None):
    try:
        return _orig(text, years=years, filing=filing)
    except (AttributeError, ValueError):
        return None


D.parse_span = parse_span
for name in ("tt.labels.agree", "tt.labels.events", "tt.labels.protocol", "tt.labels.draft", "tt.labels.schema", "tt.eval.diagnose", "tt.eval.devscore"):
    try:
        m = importlib.import_module(name)
        if hasattr(m, "parse_span"):
            m.parse_span = parse_span
    except Exception:
        pass
from tt.cli import app
sys.argv = ["tt.cli", *sys.argv[1:]]
app()
