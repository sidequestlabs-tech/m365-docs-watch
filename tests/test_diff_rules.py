from notifier.diff import Hunk, diff_hunks, is_trivial
from notifier.rules import rule_floor


def test_retention_change_is_push():
    h = Hunk("Audit records are retained for 90 days.", "Audit records are retained for 180 days.")
    assert rule_floor(h) == "push"


def test_deprecation_word_is_push():
    assert rule_floor(Hunk("Use Search-MailboxAuditLog.", "Search-MailboxAuditLog will be retired.")) == "push"


def test_license_name_is_push():
    assert rule_floor(Hunk("Requires E3.", "Requires E5 or the Audit (Premium) add-on.")) == "push"


def test_plain_rewording_is_digest():
    assert rule_floor(Hunk("Select Search.", "Select the Search button.")) == "digest"


def test_trivial():
    assert is_trivial(Hunk("See [docs](a).", "See  [docs](b)"))
    assert not is_trivial(Hunk("90 days", "180 days"))


def test_diff_finds_changed_paragraph_only():
    hunks = diff_hunks("A\n\nB 90 days\n\nC", "A\n\nB 180 days\n\nC")
    assert hunks == [Hunk("B 90 days", "B 180 days")]


def test_diff_table_row_is_its_own_unit():
    old = "| Cap | Std |\n|---|---|\n| Retention | 180 days |\n| Search | Yes |"
    new = "| Cap | Std |\n|---|---|\n| Retention | 365 days |\n| Search | Yes |"
    assert diff_hunks(old, new) == [Hunk("| Retention | 180 days |", "| Retention | 365 days |")]


def test_diff_added_paragraph():
    assert diff_hunks("A\n\nC", "A\n\nB new\n\nC") == [Hunk("", "B new")]
