"""Test doubles for external services."""
from types import SimpleNamespace

from notifier.watchlist import Page

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
    """Captures ntfy POSTs."""

    def __init__(self):
        self.sent = []

    @property
    def json(self):
        return self.sent[-1]

    def post(self, url, json=None, timeout=None):
        self.sent.append(json)
        return SimpleNamespace(status_code=200, raise_for_status=lambda: None)
