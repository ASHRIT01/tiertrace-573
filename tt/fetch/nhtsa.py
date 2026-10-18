"""Polite NHTSA fetcher: ~1 req/s, robots.txt, identifying UA, on-disk cache.
URL enumeration is the Week 1 gate: the numeric suffix in RCLRPT-<campaign>-<id>.PDF
cannot be derived from the campaign number, so `candidate_urls` is a stub to be filled
after inspecting how nhtsa.gov lists a recall's documents."""
import time
import urllib.robotparser
from pathlib import Path
import requests

UA = "TierTrace-573 research crawler (contact: ashrit0104@gmail.com)"
BASE = "https://static.nhtsa.gov"


class PoliteFetcher:
    def __init__(self, cache: Path, rate_s: float = 1.0):
        self.cache, self.rate_s, self._last = Path(cache), rate_s, 0.0
        self.cache.mkdir(parents=True, exist_ok=True)
        self.robots = urllib.robotparser.RobotFileParser(f"{BASE}/robots.txt")
        try:
            self.robots.read()
        except Exception:
            self.robots = None

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
        if r.status_code != 200:
            return None
        dest.write_bytes(r.content)
        return r.content


def candidate_urls(campaign: str) -> list[str]:
    raise NotImplementedError("Week 1 gate: determine how nhtsa.gov lists per-recall document URLs")
