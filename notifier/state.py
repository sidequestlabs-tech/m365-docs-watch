"""Persistent state (state.json) and the digest queue (digest-queue.json)."""
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class PageState:
    hash: str
    ms_date: str | None = None
    updated_at: str | None = None
    failures: int = 0
    missing: bool = False


@dataclass
class State:
    pages: dict[str, PageState] = field(default_factory=dict)
    roadmap_seen: list[str] | None = None      # None = roadmap never checked yet

    @classmethod
    def load(cls, path: Path) -> "State | None":
        path = Path(path)
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(pages={k: PageState(**v) for k, v in data.get("pages", {}).items()},
                   roadmap_seen=data.get("roadmap_seen"))

    def save(self, path: Path) -> None:
        data = {"pages": {k: asdict(v) for k, v in sorted(self.pages.items())}, "roadmap_seen": self.roadmap_seen}
        Path(path).write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def _read(path: Path) -> list[dict]:
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def queue_append(path: Path, item: dict) -> None:
    items = _read(path) + [item]
    Path(path).write_text(json.dumps(items, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def queue_drain(path: Path) -> list[dict]:
    items = _read(path)
    Path(path).write_text("[]\n", encoding="utf-8")
    return items
