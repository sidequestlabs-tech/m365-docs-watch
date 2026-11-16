from fakes import PAGE, FakeClient, RaisingClient
from notifier.classify import classify
from notifier.diff import Hunk


def test_ai_cannot_lower_rule_floor():
    fake = FakeClient('{"level":"ignore","summary":"x","old_text":"90 days","new_text":"180 days"}')
    c = classify(PAGE, [Hunk("kept 90 days", "kept 180 days")], fake)
    assert c.level == "push"


def test_ai_can_raise():
    fake = FakeClient('{"level":"push","summary":"New audit operation","old_text":"","new_text":"CopilotInteraction"}')
    c = classify(PAGE, [Hunk("", "New operation CopilotInteraction")], fake)
    assert c.level == "push" and c.summary == "New audit operation"


def test_api_failure_falls_back():
    assert classify(PAGE, [Hunk("Select Search.", "Select the Search button.")], RaisingClient()).level == "digest"
    assert classify(PAGE, [Hunk("90 days", "180 days")], RaisingClient()).level == "push"


def test_fallback_has_old_new_and_summary():
    c = classify(PAGE, [Hunk("90 days", "180 days")], RaisingClient())
    assert c.old_text == "90 days" and c.new_text == "180 days" and c.summary == "Learn about auditing solutions changed"


def test_bad_json_falls_back():
    assert classify(PAGE, [Hunk("a b c", "a b d")], FakeClient("not json")).level == "digest"


def test_huge_rewrite_one_call_capped():                 # Review Focus 2
    fake = FakeClient('{"level":"digest","summary":"Page restructured","old_text":"","new_text":""}')
    classify(PAGE, [Hunk(f"old {i}", f"new {i}") for i in range(500)], fake)
    assert fake.calls == 1 and len(fake.last_prompt) <= 24_000


def test_uses_haiku_with_json_schema():
    fake = FakeClient('{"level":"digest","summary":"s","old_text":"","new_text":""}')
    classify(PAGE, [Hunk("a", "b")], fake)
    assert fake.last_kwargs["model"] == "claude-haiku-5-5"
    assert fake.last_kwargs["output_config"]["format"]["type"] == "json_schema"


def test_empty_ai_excerpts_replaced_by_hunk_text():      # anti-goal: alert without old -> new
    fake = FakeClient('{"level":"push","summary":"Retention changed","old_text":"","new_text":""}')
    c = classify(PAGE, [Hunk("kept 90 days", "kept 180 days")], fake)
    assert c.old_text == "kept 90 days" and c.new_text == "kept 180 days"
