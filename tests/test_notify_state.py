from fakes import PAGE, FakeSession
from notifier.classify import Classification
from notifier.notify import format_change, send
from notifier.state import PageState, State, queue_append, queue_drain


def test_body_trimmed():                                  # Review Focus 4
    sent = FakeSession()
    send("t", "Title →", "x" * 10_000, None, 4, sent)
    assert len(sent.json["message"].encode()) <= 3500 and sent.json["title"] == "Title →"
    assert sent.json["topic"] == "t" and sent.json["priority"] == 4


def test_body_trim_multibyte_safe():
    sent = FakeSession()
    send("t", "T", "→" * 5000, "https://x", 3, sent)
    assert len(sent.json["message"].encode()) <= 3500 and sent.json["click"] == "https://x"


def test_format_change_has_old_and_new():
    title, body = format_change(PAGE, Classification("push", "Audit retention 90→180 days", "90 days", "180 days"), None, "2026-07-08T17:35:00Z")
    assert title == "Audit retention 90→180 days"
    assert "OLD: 90 days" in body and "NEW: 180 days" in body and "2026-07-08" in body


def test_state_roundtrip(tmp_path):
    s = State(pages={"a": PageState(hash="h", ms_date="d1", updated_at="d2", failures=1)}, roadmap_seen=["x"])
    s.save(tmp_path / "state.json")
    assert State.load(tmp_path / "state.json") == s


def test_state_load_missing_returns_none(tmp_path):
    assert State.load(tmp_path / "nope.json") is None


def test_queue_drain_empties(tmp_path):
    q = tmp_path / "q.json"
    queue_append(q, {"kind": "change", "slug": "a"})
    queue_append(q, {"kind": "change", "slug": "b"})
    assert [i["slug"] for i in queue_drain(q)] == ["a", "b"]
    assert queue_drain(q) == []
