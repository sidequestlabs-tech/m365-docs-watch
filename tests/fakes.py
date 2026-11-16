"""Test doubles for external services."""
from types import SimpleNamespace

from notifier.notify import Telegram
from notifier.watchlist import Page

DEST = Telegram(token="TOKEN123", chat_id="42")

PAGE = Page(url="https://learn.microsoft.com/en-us/purview/audit-solutions-overview",
            slug="purview__audit-solutions-overview", title="Learn about auditing solutions",
            section="1. Purview Audit — the unified audit log (UAL)", core=True, why="retention")


class FakeClient:
    """Mimics anthropic.Anthropic().messages.create, returning a fixed text block."""

    def __init__(self, text: str):
        self.text, self.calls, self.last_prompt, self.last_kwargs = text, 0, "", {}
        self.messages = self

    def create(self, **kwargs):
        self.calls += 1
        self.last_kwargs = kwargs
        self.last_prompt = kwargs["messages"][-1]["content"]
        return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=self.text)])


class RaisingClient:
    def __init__(self):
        self.messages = self

    def create(self, **kwargs):
        raise RuntimeError("API down")


class FakeSession:
    """Captures Telegram sendMessage POSTs and decodes them for assertions."""

    def __init__(self):
        self.sent, self.urls = [], []

    @property
    def json(self):
        return self.sent[-1]

    def post(self, url, json=None, timeout=None):
        import html, re
        self.urls.append(url)
        text = json["text"]
        title = html.unescape(re.match(r"<b>(.*?)</b>", text, re.S).group(1))
        link = re.search(r'<a href="([^"]+)">Open page</a>\Z', text)
        body = text[text.index("</b>") + 5:]
        if link:
            body = body[: link.start() - (text.index("</b>") + 5)].rstrip("\n")
        self.sent.append({"title": title, "message": html.unescape(body), "raw": json,
                          "click": html.unescape(link.group(1)) if link else None,
                          "priority": 3 if json.get("disable_notification") else 4})
        return SimpleNamespace(status_code=200, raise_for_status=lambda: None)


FILLER = "This paragraph describes how auditing works in Microsoft Purview for investigators. " * 4


def learn_html(body_md_paragraphs: list[str], title: str = "Test page") -> str:
    paras = "".join(f"<p>{p}</p>" for p in body_md_paragraphs)
    return (f'<html><head><meta name="updated_at" content="2026-11-01T00:00:00Z"></head><body><main>'
            f'<div class="content"><h1>{title}</h1></div>'
            f'<div class="content"><p>{FILLER}</p>{paras}</div></main></body></html>')


class FakeFetcher:
    """url -> FetchResult, or an Exception instance to raise."""

    def __init__(self, responses: dict):
        self.responses = responses

    def __call__(self, url):
        from notifier.fetch import FetchResult
        r = self.responses[url]
        if isinstance(r, Exception):
            raise r
        if isinstance(r, FetchResult):
            return r
        return FetchResult(200, url, r, None, "2026-11-01T00:00:00Z")


class FailingSession(FakeSession):
    def post(self, url, json=None, timeout=None):
        raise RuntimeError("ntfy 503")
