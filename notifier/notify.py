"""Phone notifications via ntfy.sh (JSON publish, so non-ASCII titles work)."""
from notifier.classify import Classification
from notifier.watchlist import Page

NTFY_URL = "https://ntfy.sh/"
MAX_BODY_BYTES = 3500
EXCERPT_CHARS = 600


def _trim(text: str, limit: int = MAX_BODY_BYTES) -> str:
    raw = text.encode("utf-8")
    if len(raw) <= limit:
        return text
    return raw[: limit - len("…".encode())].decode("utf-8", errors="ignore") + "…"


def send(topic: str, title: str, body: str, click: str | None, priority: int, session) -> None:
    payload = {"topic": topic, "title": title[:200], "message": _trim(body), "priority": priority, "tags": ["mag"]}
    if click:
        payload["click"] = click
    session.post(NTFY_URL, json=payload, timeout=30).raise_for_status()


def _clip(s: str) -> str:
    s = " ".join(s.split())
    return s if len(s) <= EXCERPT_CHARS else s[:EXCERPT_CHARS] + "…"


def format_change(page: Page, c: Classification, ms_date: str | None, updated_at: str | None) -> tuple[str, str]:
    lines = [f"OLD: {_clip(c.old_text) or '(none)'}", f"NEW: {_clip(c.new_text) or '(none)'}"]
    if updated_at:
        lines.append(f"Page updated: {updated_at[:10]}")
    lines.append(page.section)
    return c.summary, "\n".join(lines)
