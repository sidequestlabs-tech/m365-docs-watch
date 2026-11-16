"""Monday digest of queued changes. `python -m notifier.digest [--dry-run]`"""
import argparse
import os
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import requests

from notifier.notify import Telegram, send
from notifier.state import queue_drain


def build_digest(items: list[dict], week: str) -> tuple[str, str, str]:
    changes = [i for i in items if i.get("kind") == "change"]
    suggestions = [i for i in items if i.get("kind") == "suggestion"]
    md = [f"# Weekly digest — {week}\n"]
    if not changes and not suggestions:
        md.append("No notable changes this week.\n")
        return "\n".join(md), "No notable changes this week", "The notifier is running; nothing needed your attention."

    by_section = defaultdict(list)
    for c in changes:
        by_section[c.get("section") or "Other"].append(c)
    for section in sorted(by_section):
        md.append(f"## {section}\n")
        for c in by_section[section]:
            md.append(f"### [{c['title']}]({c['url']})\n**{c['summary']}**\n")
            if c.get("old_text"):
                md.append(f"- Old: {c['old_text'][:600]}")
            if c.get("new_text"):
                md.append(f"- New: {c['new_text'][:600]}")
            md.append("")
    if suggestions:
        md.append("## Suggested pages to watch\n")
        for s in suggestions:
            md.append(f"- {s['url']} (found on {s['found_on']})")
        md.append("")

    title = f"Weekly digest: {len(changes)} changes" if changes else "Weekly digest: new pages to consider"
    counts = " · ".join(f"{sec.split('—')[0].strip()}: {len(v)}" for sec, v in sorted(by_section.items()))
    top = "".join(f"\n- {c['summary']}" for c in changes[:3])
    extra = f"\n+ {len(suggestions)} suggested page(s) to watch" if suggestions else ""
    return "\n".join(md), title, (counts or "") + top + extra


def run_digest(root: Path, notify_session, dest, week: str | None = None, dry_run: bool = False) -> str:
    root = Path(root)
    week = week or "{}-W{:02d}".format(*date.today().isocalendar()[:2])
    queue_path = root / "digest-queue.json"
    if dry_run:
        import json
        items = json.loads(queue_path.read_text()) if queue_path.exists() else []
    else:
        items = queue_drain(queue_path)
    md, title, body = build_digest(items, week)
    repo = os.environ.get("GITHUB_REPOSITORY")
    click = f"https://github.com/{repo}/blob/main/digests/{week}.md" if repo else None
    if dry_run:
        print(md)
        print(f"[dry-run] would send: {title}\n{body}")
        return md
    (root / "digests").mkdir(exist_ok=True)
    (root / "digests" / f"{week}.md").write_text(md, encoding="utf-8")
    send(dest, title, body, click, 4 if items else 3, notify_session)
    return md


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent)
    args = ap.parse_args(argv)
    run_digest(Path(args.root), requests.Session(), Telegram.from_env(), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
