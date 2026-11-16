"""Microsoft 365 Roadmap RSS: alert on new security/compliance items."""
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

import feedparser

from notifier.classify import classify
from notifier.diff import Hunk
from notifier.notify import format_change
from notifier.state import State, queue_append
from notifier.watchlist import Page

FEED_URL = "https://www.microsoft.com/releasecommunications/api/v2/m365/rss"
KEYWORDS = re.compile(r"Purview|Audit|eDiscovery|Insider Risk|Defender|Entra|Sentinel|retention", re.I)
EXCLUDE = re.compile(r"Dynamics 365|Power (Apps|Automate|BI|Pages)")
SECTION = "M365 Roadmap"
MASS_NEW_LIMIT = 25


@dataclass
class RoadmapItem:
    id: str
    title: str
    summary: str
    link: str


@dataclass
class RoadmapReport:
    notifications: list[tuple] = field(default_factory=list)
    queued: list[str] = field(default_factory=list)


def _text(html: str) -> str:
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", html or "")).split())


def _all_items(feed_xml: str) -> list[tuple[RoadmapItem, str]]:
    out = []
    for e in feedparser.parse(feed_xml).entries:
        cats = " ".join(t.get("term", "") for t in e.get("tags", []))
        out.append((RoadmapItem(str(e.get("id", e.get("link"))), e.get("title", ""), _text(e.get("summary", "")),
                                e.get("link", "")), cats))
    return out


def new_roadmap_items(feed_xml: str, seen_ids: set[str]) -> list[RoadmapItem]:
    # Match on title + product category only: descriptions mention "audit"/"retention" far too often.
    return [i for i, cats in _all_items(feed_xml)
            if i.id not in seen_ids and KEYWORDS.search(f"{i.title} {cats}") and not EXCLUDE.match(i.title)]


def check_roadmap(feed_xml: str, state: State, client, queue_path: Path, dry_run: bool = False) -> RoadmapReport:
    report = RoadmapReport()
    all_ids = [i.id for i, _ in _all_items(feed_xml)]
    if not all_ids:                                 # empty/broken feed: change nothing
        return report
    if state.roadmap_seen is None:                  # first run: remember everything, alert on nothing
        state.roadmap_seen = all_ids
        return report
    seen = set(state.roadmap_seen)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_items = new_roadmap_items(feed_xml, seen)
    if len(new_items) > MASS_NEW_LIMIT:             # feed re-keyed or was empty last time: re-baseline silently
        state.roadmap_seen = sorted(seen | set(all_ids))
        return report
    for item in new_items:
        page = Page(url=item.link, slug=f"roadmap-{item.id}", title=f"M365 Roadmap: {item.title}",
                    section=SECTION, core=True, why="")
        c = classify(page, [Hunk("", f"{item.title}\n{item.summary}")], client, use_rules=False)
        if c.level == "push":
            title, body = format_change(page, c, None, None)
            report.notifications.append((f"Roadmap: {title}", body, item.link, 4))
        else:
            if not dry_run:
                queue_append(queue_path, {"kind": "change", "slug": page.slug, "title": page.title, "section": SECTION,
                                          "url": item.link, "summary": c.summary, "old_text": "",
                                          "new_text": item.summary[:600], "updated_at": None, "detected_at": now})
            report.queued.append(page.slug)
    state.roadmap_seen = sorted(seen | set(all_ids))
    return report
