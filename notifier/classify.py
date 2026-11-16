"""Ask Claude which alert level a page change deserves."""
import json
import logging
from dataclasses import dataclass

from notifier.diff import Hunk
from notifier.rules import rule_floor
from notifier.watchlist import Page

MODEL = "claude-haiku-5-5"
MAX_PROMPT_CHARS = 24_000
LEVELS = ["ignore", "digest", "push"]
log = logging.getLogger(__name__)

LEVEL_DEFINITIONS = """\
- push: a retention or lookback number changes, licensing changes, limits change, something is deprecated or retired, a new table or audit operation appears, a watched page is removed or moved.
- digest: other real wording changes (new steps, clarifications, new sections).
- ignore: typos, formatting, screenshots, link fixes.
When unsure between two levels, choose the higher one."""

SCHEMA = {
    "type": "object",
    "properties": {
        "level": {"type": "string", "enum": LEVELS},
        "summary": {"type": "string"},
        "old_text": {"type": "string"},
        "new_text": {"type": "string"},
    },
    "required": ["level", "summary", "old_text", "new_text"],
    "additionalProperties": False,
}


@dataclass
class Classification:
    level: str
    summary: str
    old_text: str
    new_text: str


def _higher(a: str, b: str) -> str:
    return a if LEVELS.index(a) >= LEVELS.index(b) else b


def _prompt(page: Page, hunks: list[Hunk]) -> str:
    head = (
        "You triage changes to Microsoft documentation for a Microsoft 365 digital forensics investigator.\n"
        f"Page: {page.title}\nSection: {page.section}\nURL: {page.url}\n\n"
        f"Levels:\n{LEVEL_DEFINITIONS}\n\n"
        "Return the level, a one-line summary under 90 characters naming the concrete change "
        "(e.g. 'Audit (Standard) retention: 90 → 180 days'), and the shortest old/new excerpts that show it.\n\n"
        "Changes:\n"
    )
    budget = MAX_PROMPT_CHARS - len(head) - 200
    parts, used = [], 0
    for i, h in enumerate(hunks):
        chunk = f"--- change {i + 1}\nOLD: {h.old_text or '(none)'}\nNEW: {h.new_text or '(none)'}\n"
        if used + len(chunk) > budget:
            parts.append(f"... {len(hunks) - i} more changes omitted\n")
            break
        parts.append(chunk)
        used += len(chunk)
    return head + "".join(parts)


def _fallback(page: Page, hunks: list[Hunk], level: str) -> Classification:
    first = next((h for h in hunks if rule_floor(h) == "push"), hunks[0])
    return Classification(level, f"{page.title} changed", first.old_text, first.new_text)


def classify(page: Page, hunks: list[Hunk], client) -> Classification:
    floor = "digest"
    for h in hunks:
        floor = _higher(floor, rule_floor(h))
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            output_config={"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
            messages=[{"role": "user", "content": _prompt(page, hunks)}],
        )
        text = next(b.text for b in resp.content if b.type == "text")
        data = json.loads(text)
        level = _higher(floor, data["level"]) if data.get("level") in LEVELS else floor
        c = Classification(level, data.get("summary") or f"{page.title} changed",
                           data.get("old_text", ""), data.get("new_text", ""))
        if not (c.old_text or c.new_text):
            fb = _fallback(page, hunks, level)
            c.old_text, c.new_text = fb.old_text, fb.new_text
        return c
    except Exception as e:  # any API/parse failure must not lose the alert
        log.warning("classify failed for %s: %r", page.slug, e)
        return _fallback(page, hunks, floor)
