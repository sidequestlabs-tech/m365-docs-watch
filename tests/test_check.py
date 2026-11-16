import pytest
from fakes import DEST, FakeClient, FakeFetcher, FakeSession, learn_html
from notifier.check import run_check
from notifier.fetch import FetchError, FetchResult
from notifier.watchlist import Page, dump_watchlist, slug_for

B = "https://learn.microsoft.com/en-us/"
URLS = [B + "purview/audit-search", B + "purview/edisc", B + "purview/whats-new"]
AI_DIGEST = '{"level":"digest","summary":"Wording changed","old_text":"a","new_text":"b"}'


@pytest.fixture
def repo(tmp_path):
    pages = [Page(u, slug_for(u), u.rsplit("/", 1)[1], "9. Change feeds" if "whats-new" in u else "1. Audit", True, "")
             for u in URLS]
    dump_watchlist(pages, tmp_path / "watchlist.yaml")
    return tmp_path


def run(repo, responses, ai=AI_DIGEST, dry_run=False):
    ntfy = FakeSession()
    report = run_check(repo, FakeFetcher(responses), FakeClient(ai), ntfy, DEST, dry_run)
    return report, ntfy.sent


def base(**override):
    r = {u: learn_html(["Records are kept for 90 days."]) for u in URLS}
    r.update(override)
    return r


def test_first_run_baselines_and_sends_one_push(repo):
    report, sent = run(repo, base())
    assert len(report.baselined) == 3 and len(list((repo / "snapshots").glob("*.md"))) == 3
    assert [m["title"] for m in sent] == ["Baseline complete: 3 pages watched"]


def test_retention_change_pushes(repo):
    run(repo, base())
    report, sent = run(repo, base(**{URLS[0]: learn_html(["Records are kept for 180 days."])}))
    assert len(sent) == 1 and sent[0]["priority"] == 4 and sent[0]["click"] == URLS[0]
    assert "180 days" in (repo / "snapshots" / f"{slug_for(URLS[0])}.md").read_text()
    assert report.pushed == [slug_for(URLS[0])]


def test_wording_change_is_queued(repo):
    run(repo, base())
    report, sent = run(repo, base(**{URLS[1]: learn_html(["Records are kept for 90 days.", "Select the Search button first."])}))
    assert sent == [] and report.queued == [slug_for(URLS[1])]
    import json
    q = json.loads((repo / "digest-queue.json").read_text())
    assert q[0]["kind"] == "change" and q[0]["section"] == "1. Audit" and q[0]["url"] == URLS[1]


def test_trivial_change_silent(repo):
    run(repo, base())
    report, sent = run(repo, base(**{URLS[0]: learn_html(["Records are kept for  90 days"])}))
    assert sent == [] and report.queued == []


def test_new_page_added_later_is_silent(repo):           # Review Focus 3
    run(repo, base())
    extra = B + "purview/audit-copilot"
    pages = [*__import__("notifier.watchlist", fromlist=["x"]).load_watchlist(repo / "watchlist.yaml"),
             Page(extra, slug_for(extra), "audit-copilot", "1. Audit", True, "")]
    dump_watchlist(pages, repo / "watchlist.yaml")
    report, sent = run(repo, base(**{extra: learn_html(["Copilot audit."])}))
    assert sent == [] and report.baselined == [slug_for(extra)]


def test_404_pushes_once(repo):
    run(repo, base())
    gone = base(**{URLS[1]: FetchResult(404, URLS[1], "", None, None)})
    _, sent = run(repo, gone)
    assert len(sent) == 1 and "moved or removed" in sent[0]["title"]
    _, sent = run(repo, gone)
    assert sent == []                                      # no repeat every 3 hours


def test_redirect_to_other_page_pushes(repo):
    run(repo, base())
    moved = base(**{URLS[1]: FetchResult(200, B + "purview/edisc-new", learn_html(["x"]), None, None)})
    _, sent = run(repo, moved)
    assert len(sent) == 1 and "moved or removed" in sent[0]["title"]


def test_query_only_redirect_ignored(repo):
    run(repo, base())
    r = base(**{URLS[0]: FetchResult(200, URLS[0] + "?view=x", learn_html(["Records are kept for 90 days."]), None, None)})
    _, sent = run(repo, r)
    assert sent == []


def test_fetch_failure_alerts_on_third_run_only(repo):
    run(repo, base())
    bad = base(**{URLS[0]: FetchError("timeout")})
    counts = [len(run(repo, bad)[1]) for _ in range(4)]
    assert counts == [0, 0, 1, 0]


def test_whats_new_link_suggestion(repo):
    run(repo, base())
    html = learn_html(["Records are kept for 90 days.", 'New: <a href="audit-copilot">Copilot audit</a> and <a href="audit-search">search</a>'])
    run(repo, base(**{URLS[2]: html}))
    import json
    q = json.loads((repo / "digest-queue.json").read_text())
    sugg = [i for i in q if i["kind"] == "suggestion"]
    assert [s["url"] for s in sugg] == [B + "purview/audit-copilot"]


def test_dry_run_writes_nothing(repo):
    report, sent = run(repo, base(), dry_run=True)
    assert sent == [] and not (repo / "snapshots").exists() and not (repo / "state.json").exists()
    assert len(report.baselined) == 3


def test_roadmap_wired_into_run(repo):
    from conftest import read
    import json
    xml = read("roadmap.xml")
    ntfy = FakeSession()
    run_check(repo, FakeFetcher(base()), FakeClient(AI_DIGEST), ntfy, DEST, roadmap_xml=xml)
    assert json.loads((repo / "state.json").read_text())["roadmap_seen"] == ["1001", "1002", "1003"]
    push = '{"level":"push","summary":"New thing","old_text":"","new_text":"x"}'
    xml2 = xml.replace("<guid isPermaLink=\"false\">1003</guid>", "<guid isPermaLink=\"false\">1004</guid>")
    ntfy = FakeSession()
    run_check(repo, FakeFetcher(base()), FakeClient(push), ntfy, DEST, roadmap_xml=xml2)
    assert [m["title"] for m in ntfy.sent] == ["Roadmap: New thing"]
