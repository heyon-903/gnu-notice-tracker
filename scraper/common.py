import time

import requests

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

DEFAULT_HEADERS = {"User-Agent": USER_AGENT}


def fetch(url, params=None, retries=3, timeout=15):
    last_error = None
    for attempt in range(retries):
        try:
            resp = requests.get(
                url, params=params, headers=DEFAULT_HEADERS, timeout=timeout
            )
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding or "utf-8"
            return resp.text
        except requests.RequestException as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_error}")
