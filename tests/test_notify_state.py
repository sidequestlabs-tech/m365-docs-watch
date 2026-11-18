from fakes import DEST, PAGE, FakeSession
from notifier.classify import Classification
from notifier.notify import format_change, send
from notifier.state import PageState, State, queue_append, queue_drain


def test_body_trimmed():                                  # Review Focus 4
    sent = FakeSession()
    send(DEST, "Title →", "x" * 10_000, None, 4, sent)
    assert len(sent.json["message"].encode()) <= 3500 and sent.json["title"] == "Title →"
    assert sent.json["raw"]["chat_id"] == "42" and sent.json["priority"] == 4
    assert sent.urls[-1] == "https://api.telegram.org/botTOKEN123/sendMessage"


def test_body_trim_multibyte_safe():
    sent = FakeSession()
    send(DEST, "T", "→" * 5000, "https://x", 3, sent)
    assert len(sent.json["message"].encode()) <= 3500 and sent.json["click"] == "https://x"


def test_html_escaped():
    sent = FakeSession()
    send(DEST, "A <b> & C", "if x < 5 & y > 2", "https://x/?a=1&b=2", 4, sent)
    assert sent.json["raw"]["parse_mode"] == "HTML" and "x &lt; 5 &amp; y" in sent.json["raw"]["text"]
    assert sent.json["title"] == "A <b> & C" and sent.json["click"] == "https://x/?a=1&b=2"


def test_info_priority_is_silent():
    sent = FakeSession()
    send(DEST, "T", "b", None, 3, sent)
    assert sent.json["raw"]["disable_notification"] is True


def test_send_error_never_contains_token():               # public repo: Actions logs are public
    import pytest
    from types import SimpleNamespace
    import requests

    class Bad(FakeSession):
        def post(self, url, json=None, timeout=None):
            def boom():
                raise requests.HTTPError(f"400 Client Error: Bad Request for url: {url}")
            return SimpleNamespace(status_code=400, raise_for_status=boom)

    with pytest.raises(Exception) as e:
        send(DEST, "T", "b", None, 4, Bad())
    assert "TOKEN123" not in str(e.value) and "TOKEN123" not in repr(e.value)


def test_format_change_has_old_and_new():
    title, body = format_change(PAGE, Classification("push", "Audit retention 90→180 days", "90 days", "180 days"), None, "2026-07-08T17:35:00Z")
    assert title == "Audit retention 90→180 days"
    assert '🔴 OLD:\n\n"90 days"\n\n🟢 NEW:\n\n"180 days"\n\n📅 Page updated: 2026-07-08\n\n🔷 ' in body
    sent = FakeSession()
    send(DEST, title, body, None, 4, sent)
    text = sent.json["raw"]["text"]
    assert "<b>🔴 OLD:</b>" in text and "<b>🟢 NEW:</b>" in text and "<b>📅 Page updated:</b>" in text


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
