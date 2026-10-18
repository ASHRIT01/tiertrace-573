"""Polite NHTSA fetcher: ~1 req/s, robots.txt, identifying UA, on-disk cache.
The numeric suffix in RCLRPT-<campaign>-<id>.PDF cannot be derived from the campaign number;
URLs come from tt.fetch.api.list_573 (api.nhtsa.gov/safetyIssues/byNhtsaId)."""
import time
import urllib.robotparser
from pathlib import Path
import requests

UA = "TierTrace-573 research crawler (contact: ashrit0104@gmail.com)"
BASE = "https://static.nhtsa.gov"


class Blocked(RuntimeError):
    """Server refused us (401/403/429). Per project rules: stop, do not retry or evade."""


class PoliteFetcher:
    def __init__(self, cache: Path, rate_s: float = 1.0):
        self.cache, self.rate_s, self._last = Path(cache), rate_s, 0.0
        self.cache.mkdir(parents=True, exist_ok=True)
        self.robots = urllib.robotparser.RobotFileParser()
        r = requests.get(f"{BASE}/robots.txt", headers={"User-Agent": UA}, timeout=30)
        if r.status_code == 200:
            self.robots.parse(r.text.splitlines())
        elif r.status_code in (404, 410):
            self.robots.parse([])  # no robots.txt: nothing disallowed
        else:
            raise RuntimeError(f"robots.txt returned {r.status_code}; not crawling")

    def get(self, url: str) -> bytes | None:
        dest = self.cache / url.replace("https://", "").replace("/", "_")
        if dest.exists():
            return dest.read_bytes()
        if self.robots and not self.robots.can_fetch(UA, url):
            return None
        wait = self.rate_s - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        if r.status_code in (401, 403, 429):
            raise Blocked(f"{r.status_code} from {url}; stopping")
        if r.status_code != 200:
            return None
        dest.write_bytes(r.content)
        return r.content
