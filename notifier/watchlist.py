"""The list of watched Microsoft Learn pages."""
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlsplit

import yaml


@dataclass
class Page:
    url: str
    slug: str
    title: str
    section: str
    core: bool
    why: str


def slug_for(url: str) -> str:
    path = urlsplit(url).path.strip("/")
    parts = path.split("/")
    if parts and len(parts[0]) == 5 and parts[0][2] == "-":   # locale like en-us
        parts = parts[1:]
    return "__".join(p for p in parts if p)


def load_watchlist(path: Path) -> list[Page]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return [Page(**item) for item in data["pages"]]


def dump_watchlist(pages: list[Page], path: Path) -> None:
    Path(path).write_text(
        yaml.safe_dump({"pages": [asdict(p) for p in pages]}, sort_keys=False, allow_unicode=True, width=200),
        encoding="utf-8",
    )
