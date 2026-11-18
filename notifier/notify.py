"""Phone notifications via a Telegram bot (sendMessage, HTML formatting)."""
import re
from dataclasses import dataclass
from html import escape

from notifier.classify import Classification
from notifier.watchlist import Page

API = "https://api.telegram.org/bot{token}/sendMessage"
MAX_BODY_BYTES = 3500      # Telegram's limit is 4096 characters; leave room for title and link


class SendError(Exception):
    """A notification could not be delivered. Never contains the bot token."""


@dataclass(frozen=True)
class Telegram:
    token: str
    chat_id: str

    def __repr__(self):                 # keep the token out of logs and tracebacks
        return f"Telegram(chat_id={self.chat_id!r})"

    @classmethod
    def from_env(cls) -> "Telegram":
        import os
        return cls(os.environ.get("TELEGRAM_BOT_TOKEN", ""), os.environ.get("TELEGRAM_CHAT_ID", ""))
EXCERPT_CHARS = 600
# Bodies are plain text (escaped in send); only these exact change-alert labels are turned bold.
_LABEL = re.compile(r"^((?:🔴|🟢|📅) (?:OLD|NEW|Page updated):)", re.M)


def _trim(text: str, limit: int = MAX_BODY_BYTES) -> str:
    raw = text.encode("utf-8")
    if len(raw) <= limit:
        return text
    return raw[: limit - len("…".encode())].decode("utf-8", errors="ignore") + "…"


def send(dest: Telegram, title: str, body: str, click: str | None, priority: int, session) -> None:
    """priority 4 = normal alert with sound; 3 = informational, delivered silently."""
    body = _LABEL.sub(r"<b>\1</b>", escape(_trim(body), quote=False))
    text = f"<b>{escape(title[:200], quote=False)}</b>\n{body}"
    if click:
        text += f'\n<a href="{escape(click, quote=True)}">Open page</a>'
    payload = {"chat_id": dest.chat_id, "text": text, "parse_mode": "HTML",
               "disable_notification": priority < 4, "link_preview_options": {"is_disabled": True}}
    try:
        session.post(API.format(token=dest.token), json=payload, timeout=30).raise_for_status()
    except Exception as e:
        raise SendError(f"Telegram send failed: {type(e).__name__}: {str(e).replace(dest.token, '***')}") from None


def _clip(s: str) -> str:
    s = " ".join(s.split())
    return s if len(s) <= EXCERPT_CHARS else s[:EXCERPT_CHARS] + "…"


def format_change(page: Page, c: Classification, ms_date: str | None, updated_at: str | None) -> tuple[str, str]:
    def quoted(s):
        return f'"{_clip(s)}"' if _clip(s) else "(none)"
    lines = ["🔴 OLD:", "", quoted(c.old_text), "", "🟢 NEW:", "", quoted(c.new_text), ""]
    if updated_at:
        lines += [f"📅 Page updated: {updated_at[:10]}", ""]
    lines.append(f"🔷 {page.section}")
    return c.summary, "\n".join(lines)
