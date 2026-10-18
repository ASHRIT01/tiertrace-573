import re
from pathlib import Path

MD = Path(__file__).parent.parent / "reports" / "adjudication.md"


def test_adjudication_sheet_is_unmarked_and_complete():
    t = MD.read_text()
    items = re.findall(r"^### Item (\d+):", t, re.M)
    assert len(items) == 24                      # 14 differences + 10 agreed
    assert t.count("[ ] A right   [ ] B right   [ ] neither:") == 24
    assert not re.search(r"\[[xX]\]", t)         # nothing is pre-marked
    assert "## Part 1: differences" in t and "## Part 2: agreed items" in t
