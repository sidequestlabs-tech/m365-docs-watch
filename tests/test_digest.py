import json

from fakes import FakeSession
from notifier.digest import build_digest, run_digest


def item(section, summary, slug="s"):
    return {"kind": "change", "slug": slug, "title": f"T {summary}", "section": section, "url": f"https://x/{slug}",
            "summary": summary, "old_text": "o", "new_text": "n", "updated_at": None, "detected_at": "2026-11-16"}


FIVE = [item("1. Purview Audit", f"A{i}", f"a{i}") for i in range(3)] + [item("2. eDiscovery", f"E{i}", f"e{i}") for i in range(2)]


def test_empty_week_heartbeat():
    _, title, body = build_digest([], "2026-W47")
    assert title == "No notable changes this week"


def test_groups_by_section_and_top3():
    md, title, body = build_digest(FIVE, "2026-W47")
    assert "## 1. Purview Audit" in md and "## 2. eDiscovery" in md and title == "Weekly digest: 5 changes"
    assert body.count("\n- ") == 3 or body.startswith("- ") and body.count("- ") == 3


def test_suggestions_listed_separately():
    md, title, _ = build_digest(FIVE + [{"kind": "suggestion", "url": "https://learn.microsoft.com/en-us/purview/new",
                                         "found_on": "https://x", "section": "9", "detected_at": "d"}], "2026-W47")
    assert "## Suggested pages to watch" in md and "purview/new" in md and title == "Weekly digest: 5 changes"


def test_run_digest_writes_file_drains_queue_and_sends(tmp_path, monkeypatch):
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/m365-docs-watch")
    (tmp_path / "digest-queue.json").write_text(json.dumps(FIVE))
    ntfy = FakeSession()
    run_digest(tmp_path, ntfy, "t", week="2026-W47")
    assert (tmp_path / "digests" / "2026-W47.md").exists()
    assert json.loads((tmp_path / "digest-queue.json").read_text()) == []
    assert ntfy.json["click"] == "https://github.com/owner/m365-docs-watch/blob/main/digests/2026-W47.md"
    assert ntfy.json["priority"] == 3
