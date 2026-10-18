import json
from pathlib import Path
from tt.fetch.api import ApiClient, list_573


def test_list_573_versions(tmp_path):
    doc = lambda f, s, d: {"fileName": f, "summary": s, "loadDate": d, "url": f"https://x/{f}"}
    payload = {"results": [{"recalls": [{"associatedDocuments": [
        doc("RCLRPT-1-B.PDF", "Recall 573 Report - 8/8/24", "2024-08-10T00:00:00Z"),
        doc("RCMN-1-A.pdf", "Manufacturer Notices", "2024-06-12T00:00:00Z"),
        doc("RCLRPT-1-A.PDF", "Recall 573 Report", "2024-06-12T00:00:00Z")]}]}]}
    (tmp_path / "si_24V001.json").write_text(json.dumps(payload))
    rows = list_573(ApiClient(tmp_path), "24V001")  # served from cache: no network
    assert [r["fileName"] for r in rows] == ["RCLRPT-1-A.PDF", "RCLRPT-1-B.PDF"]
    assert rows[0]["is_original"] and not rows[0]["is_latest"] and rows[1]["is_latest"]
