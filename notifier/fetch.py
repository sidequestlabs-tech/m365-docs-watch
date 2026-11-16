"""Download Learn pages politely."""
import time
from dataclasses import dataclass

import requests

USER_AGENT = "m365-docs-watch/1.0"
RETRY_STATUSES = {429, 500, 502, 503, 504}


class FetchError(Exception):
    """The page could not be fetched or did not contain an article."""


@dataclass
class FetchResult:
    status: int
    final_url: str
    html: str
    ms_date: str | None
    updated_at: str | None


def fetch(url: str, session: requests.Session, retries: int = 3, backoff: float = 2.0) -> FetchResult:
    from notifier.normalize import parse_dates

    last = None
    for attempt in range(retries):
        try:
            r = session.get(url, headers={"User-Agent": USER_AGENT}, timeout=30, allow_redirects=True)
            if r.status_code in RETRY_STATUSES:
                last = f"HTTP {r.status_code}"
            else:
                ms_date, updated_at = parse_dates(r.text) if r.status_code == 200 else (None, None)
                return FetchResult(r.status_code, r.url, r.text, ms_date, updated_at)
        except requests.RequestException as e:
            last = repr(e)
        if attempt < retries - 1:
            time.sleep(backoff * (2 ** attempt))
    raise FetchError(f"{url}: {last}")
