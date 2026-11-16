"""Generate watchlist.yaml from starter-list.md. Usage: python scripts/build_watchlist.py"""
import re
from pathlib import Path

from notifier.watchlist import Page, dump_watchlist, slug_for

ROOT = Path(__file__).resolve().parent.parent
ROW = re.compile(r"^\|\s*(⭐|◽)\s*\|\s*\[(.+?)\]\((\S+?)\)\s*\|\s*(.+?)\s*\|\s*$")
ROADMAP = "www.microsoft.com/releasecommunications"


def parse(md: str) -> list[Page]:
    pages, section = [], ""
    for line in md.splitlines():
        if line.startswith("## "):
            section = re.sub(r"\s*\(\d+\)\s*$", "", line[3:].strip())
            continue
        m = ROW.match(line)
        if not m or ROADMAP in m.group(3):
            continue
        mark, title, url, why = m.groups()
        pages.append(Page(url=url, slug=slug_for(url), title=title, section=section, core=mark == "⭐", why=why))
    return pages


if __name__ == "__main__":
    pages = parse((ROOT / "starter-list.md").read_text(encoding="utf-8"))
    dump_watchlist(pages, ROOT / "watchlist.yaml")
    print(f"{len(pages)} pages, {sum(p.core for p in pages)} core")
