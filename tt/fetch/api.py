"""Cached, rate-limited client for api.nhtsa.gov. Stops (raises Blocked) on 401/403/429."""
import json
import time
from pathlib import Path

import requests

from tt.fetch.nhtsa import UA, Blocked

API = "https://api.nhtsa.gov"


class ApiClient:
    def __init__(self, cache: Path = Path("data/api_cache"), rate_s: float = 1.0):
        self.cache, self.rate_s, self._last = Path(cache), rate_s, 0.0
        self.cache.mkdir(parents=True, exist_ok=True)
        self.requests_made = 0

    def get_json(self, path: str, params: dict, key: str) -> dict | None:
        dest = self.cache / f"{key}.json"
        if dest.exists():
            return json.loads(dest.read_text())
        wait = self.rate_s - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()
        r = requests.get(API + path, params=params, headers={"User-Agent": UA}, timeout=30)
        self.requests_made += 1
        if r.status_code in (401, 403, 429):
            raise Blocked(f"{r.status_code} from {r.url}; stopping")
        if r.status_code != 200:
            return None
        dest.write_text(r.text)
        return r.json()

    def safety_issues(self, nhtsa_id: str) -> dict | None:
        return self.get_json("/safetyIssues/byNhtsaId", {"name": "", "nhtsaId": nhtsa_id}, f"si_{nhtsa_id}")
