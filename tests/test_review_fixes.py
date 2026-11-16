"""Regression tests for the final-review findings."""
import json

from fakes import PAGE, FailingSession, FakeClient, FakeFetcher, FakeSession, RaisingClient, learn_html
from notifier.check import run_check
from notifier.classify import classify
from notifier.diff import Hunk
from notifier.fetch import FetchError, FetchResult
from notifier.roadmap import check_roadmap
from notifier.state import State
from notifier.watchlist import Page, dump_watchlist, load_watchlist, slug_for
from test_check import AI_DIGEST, B, URLS, base, repo, run  # noqa: F401  (fixture reuse)

PUSH_AI = '{"level":"push","summary":"Changed","old_text":"a","new_text":"b"}'


def many_pages(repo, n):
    urls = [B + f"purview/p{i}" for i in range(n)]
    dump_watchlist([Page(u, slug_for(u), f"p{i}", "1. Audit", True, "") for i, u in enumerate(urls)], repo / "watchlist.yaml")
    return urls


# Critical 1
def test_first_run_creates_queue_file(repo):
    run(repo, base())
    assert json.loads((repo / "digest-queue.json").read_text()) == []


# Critical 2
def test_failed_sends_kept_in_outbox_and_retried(repo):
    rep = run_check(repo, FakeFetcher(base()), FakeClient(AI_DIGEST), FailingSession(), "t")
    assert rep.unsent == 1
    assert len(json.loads((repo / "state.json").read_text())["outbox"]) == 1
    ntfy = FakeSession()
    rep = run_check(repo, FakeFetcher(base()), FakeClient(AI_DIGEST), ntfy, "t")
    assert [m["title"] for m in ntfy.sent] == ["Baseline complete: 3 pages watched"] and rep.unsent == 0
    assert json.loads((repo / "state.json").read_text())["outbox"] == []


# Important 3
def test_big_shrink_is_fetch_failure(repo):
    run(repo, base())
    long = learn_html(["Records are kept for 90 days. " * 200])
    run(repo, base(**{URLS[0]: long}))
    rep, sent = run(repo, base(**{URLS[0]: learn_html(["Records are kept for 90 days."])}))
    assert sent == [] and slug_for(URLS[0]) in rep.failed


def test_mass_change_collapsed_to_one_push(repo):
    urls = many_pages(repo, 8)
    run(repo, {u: learn_html(["Kept 90 days."]) for u in urls})
    rep, sent = run(repo, {u: learn_html(["Kept 180 days."]) for u in urls}, ai=PUSH_AI)
    assert len(sent) == 1 and "8 pages" in sent[0]["title"]
    q = json.loads((repo / "digest-queue.json").read_text())
    assert len([i for i in q if i["kind"] == "change"]) == 8


def test_mass_unreachable_collapsed(repo):
    urls = many_pages(repo, 8)
    run(repo, {u: learn_html(["Kept 90 days."]) for u in urls})
    bad = {u: FetchError("down") for u in urls}
    counts = [len(run(repo, bad)[1]) for _ in range(3)]
    assert counts == [0, 0, 1]


# Important 4
def test_oversized_hunk_truncated_not_dropped():
    fake = FakeClient('{"level":"digest","summary":"s","old_text":"","new_text":""}')
    classify(PAGE, [Hunk("OLDSTART " + "x" * 50_000, "NEWSTART " + "y" * 50_000)], fake)
    assert "OLDSTART" in fake.last_prompt and "NEWSTART" in fake.last_prompt and len(fake.last_prompt) <= 24_000


# Important 5
def test_ai_outage_alerts_once(repo):
    run(repo, base())
    rc = RaisingClient()
    ntfy = FakeSession()
    run_check(repo, FakeFetcher(base(**{URLS[1]: learn_html(["Kept 90 days.", "New step one."])})), rc, ntfy, "t")
    assert any("AI classification unavailable" in m["title"] for m in ntfy.sent)
    ntfy = FakeSession()
    run_check(repo, FakeFetcher(base(**{URLS[1]: learn_html(["Kept 90 days.", "New step two."])})), rc, ntfy, "t")
    assert not any("AI classification" in m["title"] for m in ntfy.sent)


# Important 6
def test_flapping_change_pushes_once(repo):
    run(repo, base())
    a = base()
    b = base(**{URLS[0]: learn_html(["Records are kept for 180 days."])})
    sends = [len(run(repo, x, ai=PUSH_AI)[1]) for x in (b, a, b, a)]
    assert sends == [1, 0, 0, 0]


# Important 7
def test_empty_feed_does_not_baseline(tmp_path):
    state = State()
    check_roadmap('<?xml version="1.0"?><rss version="2.0"><channel><title>x</title></channel></rss>', state,
                  FakeClient("{}"), tmp_path / "q.json")
    assert state.roadmap_seen is None


def test_mass_new_roadmap_items_rebaseline_silently(tmp_path):
    from conftest import read
    xml = read("roadmap.xml")
    items = "".join(f'<item><guid isPermaLink="false">9{i:03d}</guid><link>https://x/{i}</link>'
                    f'<category>Microsoft Purview</category><title>Microsoft Purview: thing {i}</title>'
                    f'<description>d</description></item>' for i in range(30))
    xml = xml.replace("</channel>", items + "</channel>")
    state = State(roadmap_seen=["1001", "1002", "1003"])
    fake = FakeClient(PUSH_AI)
    rep = check_roadmap(xml, state, fake, tmp_path / "q.json")
    assert rep.notifications == [] and fake.calls == 0 and len(state.roadmap_seen) == 33


# Important 8
def test_never_baselined_404_is_reported(repo):
    rep, sent = run(repo, base(**{URLS[1]: FetchResult(404, URLS[1], "", None, None)}))
    assert any("moved or removed" in m["title"] for m in sent)


def test_real_shrink_accepted_on_third_run(repo):
    run(repo, base(**{URLS[0]: learn_html(["Records are kept for 90 days. " * 200])}))
    short = base(**{URLS[0]: learn_html(["Records are kept for 180 days."])})
    sends = [len(run(repo, short, ai=PUSH_AI)[1]) for _ in range(3)]
    assert sends == [0, 0, 1]
    assert "180 days" in (repo / "snapshots" / f"{slug_for(URLS[0])}.md").read_text()
