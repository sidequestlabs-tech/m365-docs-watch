import importlib.util

from conftest import ROOT

spec = importlib.util.spec_from_file_location("setup_secrets", ROOT / "scripts" / "setup_secrets.py")
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


def test_find_chat_id_uses_latest_private_message():
    updates = {"ok": True, "result": [
        {"update_id": 1, "message": {"chat": {"id": 111, "type": "private"}, "text": "/start"}},
        {"update_id": 2, "message": {"chat": {"id": -5, "type": "group"}, "text": "hi"}},
        {"update_id": 3, "message": {"chat": {"id": 222, "type": "private"}, "text": "hello"}},
    ]}
    assert setup.find_chat_id(updates) == "222"


def test_find_chat_id_none_when_no_messages():
    assert setup.find_chat_id({"ok": True, "result": []}) is None
