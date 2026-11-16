import pytest
from conftest import read
from notifier.fetch import FetchError
from notifier.normalize import extract_article, parse_dates


def test_normalize_stable():
    assert extract_article(read("audit-overview-a.html")) == extract_article(read("audit-overview-b.html"))


def test_normalize_strips_chrome():
    md = extract_article(read("audit-overview-a.html"))
    assert "Audit (Standard)" in md
    for junk in ("Feedback", "In this article", "Was this page helpful", "Additional resources"):
        assert junk not in md


def test_dates():
    ms_date, updated_at = parse_dates(read("audit-overview-a.html"))
    assert ms_date.startswith("20") and updated_at.startswith("20")


def test_empty_article_is_fetch_error():          # Review Focus 1
    with pytest.raises(FetchError):
        extract_article(read("throttle.html"))
