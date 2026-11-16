from conftest import read
from fakes import FakeClient, FakeSession
from notifier.roadmap import check_roadmap, new_roadmap_items
from notifier.state import State

XML = read("roadmap.xml")


def test_keyword_filter_and_seen():
    items = new_roadmap_items(XML, seen_ids={"1003"})
    assert [i.id for i in items] == ["1001"]          # Teams item dropped, 1003 already seen
    assert items[0].link.endswith("id=1001") and "365 days" in items[0].summary


def test_first_run_records_all_without_alerting(tmp_path):
    state = State()
    report = check_roadmap(XML, state, FakeClient("{}"), tmp_path / "q.json")
    assert report.notifications == [] and sorted(state.roadmap_seen) == ["1001", "1002", "1003"]


def test_new_item_classified_push(tmp_path):
    state = State(roadmap_seen=["1002", "1003"])
    fake = FakeClient('{"level":"push","summary":"Audit Standard retention → 365 days","old_text":"","new_text":"365 days"}')
    report = check_roadmap(XML, state, fake, tmp_path / "q.json")
    assert [n[0] for n in report.notifications] == ["Roadmap: Audit Standard retention → 365 days"]
    assert "1001" in state.roadmap_seen


def test_new_item_digest_queued(tmp_path):
    import json
    state = State(roadmap_seen=["1001", "1002"])
    fake = FakeClient('{"level":"digest","summary":"New hunting table","old_text":"","new_text":"x"}')
    report = check_roadmap(XML, state, fake, tmp_path / "q.json")
    q = json.loads((tmp_path / "q.json").read_text())
    assert report.notifications == [] and q[0]["section"] == "M365 Roadmap" and q[0]["url"].endswith("id=1003")


def test_roadmap_item_level_comes_from_ai_not_number_rules(tmp_path):
    # 1001 mentions "365 days" — a brand-new roadmap item has no "old" text, so the number rule must not force push
    state = State(roadmap_seen=["1002", "1003"])
    fake = FakeClient('{"level":"digest","summary":"Retention preview","old_text":"","new_text":"x"}')
    report = check_roadmap(XML, state, fake, tmp_path / "q.json")
    assert report.notifications == [] and report.queued == ["roadmap-1001"]


def test_copilot_alone_is_not_enough():
    xml = XML.replace("New advanced hunting table for Copilot activity", "Copilot in Word drafts faster") \
             .replace("Microsoft Defender XDR", "Microsoft Word").replace("Hunt across Copilot interactions.", "Faster drafts.")
    assert [i.id for i in new_roadmap_items(xml, set())] == ["1001"]


def test_description_only_match_ignored():
    xml = XML.replace("Microsoft Teams: New meeting reactions", "Dynamics 365: Autofill") \
             .replace("More emoji in meetings.", "Supports audit trails and retention.")
    assert "1002" not in [i.id for i in new_roadmap_items(xml, set())]
