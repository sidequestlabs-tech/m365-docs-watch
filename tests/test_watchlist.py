from conftest import ROOT
from notifier.watchlist import load_watchlist, slug_for


def test_watchlist_counts():
    pages = load_watchlist(ROOT / "watchlist.yaml")
    assert len(pages) == 115                             # 116 minus the Roadmap RSS (Task 7)
    assert sum(p.core for p in pages) == 65
    assert len({p.slug for p in pages}) == 115          # slugs unique


def test_slug_for():
    assert slug_for("https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/search-unifiedauditlog?view=exchange-ps") \
        == "powershell__module__exchangepowershell__search-unifiedauditlog"
