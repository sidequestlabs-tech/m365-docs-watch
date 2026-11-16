"""One check run: fetch every watched page, diff, classify, notify. `python -m notifier.check [--dry-run]`"""
import argparse
import hashlib
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests

from notifier.classify import classify
from notifier.diff import diff_hunks, is_trivial
from notifier.fetch import FetchError, FetchResult, fetch
from notifier.normalize import extract_article
from notifier.notify import format_change, send
from notifier.roadmap import FEED_URL, check_roadmap
from notifier.state import PageState, State, queue_append
from notifier.watchlist import Page, load_watchlist, slug_for

FAILURE_ALERT_AT = 3
PUSH, INFO = 4, 3
MD_LINK = re.compile(r"\]\(([^)\s]+)")


@dataclass
class RunReport:
    pushed: list[str] = field(default_factory=list)
    queued: list[str] = field(default_factory=list)
    baselined: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    notifications: list[tuple] = field(default_factory=list)


def _path(url: str) -> str:
    return urlsplit(url).path.rstrip("/").lower()


def make_fetcher(session: requests.Session, delay: float = 1.0):
    def _fetch(url: str) -> FetchResult:
        time.sleep(delay)
        return fetch(url, session)
    return _fetch


def _suggestions(page: Page, new_texts: list[str], watched: set[str]) -> list[str]:
    found = []
    for text in new_texts:
        for href in MD_LINK.findall(text):
            url = urljoin(page.url, href)
            parts = urlsplit(url)
            if parts.netloc != "learn.microsoft.com":
                continue
            clean = f"https://{parts.netloc}{parts.path}"
            if slug_for(clean) not in watched and clean not in found:
                found.append(clean)
    return found


def run_check(root: Path, fetcher, client, ntfy_session, topic: str, dry_run: bool = False,
              roadmap_xml: str | None = None) -> RunReport:
    root = Path(root)
    pages = load_watchlist(root / "watchlist.yaml")
    watched = {p.slug for p in pages}
    state_path, snap_dir, queue_path = root / "state.json", root / "snapshots", root / "digest-queue.json"
    loaded = State.load(state_path)
    first_run = loaded is None
    state = loaded or State()
    report = RunReport()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    def notify(title, body, click, priority):
        report.notifications.append((title, body, click, priority))

    def queue(item):
        if not dry_run:
            queue_append(queue_path, item)

    for page in pages:
        ps = state.pages.get(page.slug)
        snap = snap_dir / f"{page.slug}.md"
        try:
            res = fetcher(page.url)
            gone = res.status == 404 or (res.status == 200 and _path(res.final_url) != _path(page.url))
            if gone:
                report.failed.append(page.slug)
                if ps and not ps.missing:
                    ps.missing = True
                    notify(f"Page moved or removed: {page.title}",
                           f"Was: {page.url}\nNow: {res.final_url if res.status != 404 else 'HTTP 404'}\n{page.section}",
                           res.final_url if res.status != 404 else page.url, PUSH)
                    report.pushed.append(page.slug)
                continue
            if res.status != 200:
                raise FetchError(f"HTTP {res.status}")
            text = extract_article(res.html)
        except FetchError as e:
            report.failed.append(page.slug)
            if ps:
                ps.failures += 1
                if ps.failures == FAILURE_ALERT_AT:
                    notify(f"Page unreachable 3 runs in a row: {page.title}", f"{page.url}\n{e}", page.url, INFO)
            continue

        digest = hashlib.sha256(text.encode()).hexdigest()
        if ps is None or not snap.exists():
            report.baselined.append(page.slug)
        elif ps.hash != digest:
            old = snap.read_text(encoding="utf-8")
            hunks = [h for h in diff_hunks(old, text) if not is_trivial(h)]
            if hunks:
                c = classify(page, hunks, client)
                if c.level == "push":
                    title, body = format_change(page, c, res.ms_date, res.updated_at)
                    notify(title, body, page.url, PUSH)
                    report.pushed.append(page.slug)
                else:
                    queue({"kind": "change", "slug": page.slug, "title": page.title, "section": page.section,
                           "url": page.url, "summary": c.summary, "old_text": c.old_text, "new_text": c.new_text,
                           "updated_at": res.updated_at, "detected_at": now})
                    report.queued.append(page.slug)
                if "whats-new" in page.slug:
                    for url in _suggestions(page, [h.new_text for h in hunks], watched):
                        queue({"kind": "suggestion", "url": url, "found_on": page.url, "section": page.section,
                               "detected_at": now})
        state.pages[page.slug] = PageState(hash=digest, ms_date=res.ms_date, updated_at=res.updated_at)
        if not dry_run:
            snap_dir.mkdir(exist_ok=True)
            snap.write_text(text, encoding="utf-8")

    if roadmap_xml:
        rm = check_roadmap(roadmap_xml, state, client, queue_path, dry_run)
        report.notifications.extend(rm.notifications)
        report.queued.extend(rm.queued)

    if first_run:
        notify(f"Baseline complete: {len(state.pages)} pages watched",
               "The notifier is running. You'll get a push when an important doc change appears, "
               "and a digest every Monday.", None, INFO)

    if dry_run:
        for n in report.notifications:
            print(f"[dry-run] would send (priority {n[3]}): {n[0]}\n  {n[1][:300]}")
    else:
        state.save(state_path)
        for title, body, click, priority in report.notifications:
            send(topic, title, body, click, priority, ntfy_session)
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent)
    args = ap.parse_args(argv)
    import anthropic
    session = requests.Session()
    client = anthropic.Anthropic() if os.environ.get("ANTHROPIC_API_KEY") else None
    try:
        resp = session.get(FEED_URL, headers={"User-Agent": "m365-docs-watch/1.0"}, timeout=60)
        resp.raise_for_status()
        roadmap_xml = resp.text
    except requests.RequestException as e:
        print(f"roadmap feed skipped: {e!r}")
        roadmap_xml = None
    report = run_check(Path(args.root), make_fetcher(session), client, session,
                       os.environ.get("NTFY_TOPIC", ""), args.dry_run, roadmap_xml)
    print(f"pushed={len(report.pushed)} queued={len(report.queued)} "
          f"baselined={len(report.baselined)} failed={len(report.failed)}")
    for slug in report.failed:
        print(f"  failed: {slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
