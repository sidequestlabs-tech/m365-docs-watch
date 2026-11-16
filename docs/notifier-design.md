# M365 DFIR Docs Notifier — Design

Status: draft for approval · 2026-11-15
Companion file: `../starter-list.md` (the 116-page watch list)

## 1. Intent

The user is a digital forensics professional responding to incidents in Microsoft 365. What they can prove depends on details Microsoft changes quietly in its documentation: log retention, license requirements, search and export limits, cmdlet deprecations, new audit operations, new hunting tables.

**Goal:** when Microsoft changes one of these details on a page that matters to M365 forensics, the user's phone gets an alert within hours. The alert shows the old wording, the new wording and the link, so they never have to reread a page to find what changed.

Example of success: Audit (Standard) retention goes from 90 to 180 days → push: *"Audit retention: ~~90 days~~ → 180 days · purview/audit-solutions-overview"*.

This is **tool 1 of 2**. Tool 2 (a plain-language playbook built from the same sources) is a separate, later project. The notifier's alerts will later prompt playbook updates, done by hand at the user's discretion.

## 2. Goals / non-goals / anti-goals

**Goals**
- Watch the 116 pages in `starter-list.md`, plus the M365 Roadmap RSS feed.
- Send three levels of output (agreed with user):
  - **Push now:** a retention or lookback number changes, licensing changes, limits change, something is deprecated or retired, a new table or audit operation appears, a watched page is removed or moved.
  - **Weekly digest (Mondays):** other real wording changes (new steps, clarifications, new sections), plus newly discovered pages worth adding to the list.
  - **Ignored:** typos, formatting, screenshots, link fixes.
- Keep a dated history of every page's text (useful evidence of what the docs said on a given date).

**Non-goals**
- Crawling all of Microsoft Learn. Only the watch list.
- Writing or updating the playbook.
- Microsoft 365 Message Center. It needs tenant access the user doesn't have.
- Automatically adding pages to the watch list. It suggests pages; the user decides.

**Anti-goals (failure even if it "works")**
- **Alert fatigue.** More than about 3 push alerts a week, sustained, means the classifier needs tuning.
- **A missed retention, limit or licensing change.** Missing one of these is worse than an extra alert, so ambiguous cases go up a level, never down.
- An alert without the old → new text.

## 3. Constraints

- Runs on **GitHub Actions** in a **public** repo (user's choice, option A + public repo). Public repos get unlimited free Actions minutes, so the minute budget in 5.8 no longer constrains us. Secrets (API key, ntfy topic) stay hidden in a public repo. The README credits Microsoft Learn as the source of the snapshots (the docs are CC BY 4.0).
- Public repos disable scheduled workflows after 60 days without repo activity. The snapshot commits and weekly digest commit keep the repo active, so this shouldn't trigger. The Monday heartbeat would reveal it if it did.
- Polite fetching: robots.txt allows these pages (checked 2026-11-15). About 1 request per second, generic User-Agent, retry with backoff. No personal info in requests.
- Phone delivery via **ntfy** (free app), on a long random topic name stored as a GitHub secret.
- AI classification uses the Claude API (`claude-haiku-5-5`). Expected cost is well under $1/month, because only changed paragraphs are sent.
- User timezone: US Eastern.

## 4. Approaches considered

| Approach | Trade-off | Outcome |
|---|---|---|
| **A. GitHub Actions + snapshots in git + AI classification + ntfy** | Runs when the Mac is off; free hosting; full change history. Needs a GitHub account and an API key. | **Chosen by user** |
| B. Same, scheduled on the user's Mac | No GitHub. Misses checks while the Mac is asleep or away, then sends a burst of catch-up alerts. | Rejected |
| C. Claude Code scheduled routine doing the check each run | Least code, but higher usage cost per run and results that vary run to run. | Rejected |
| User's initial idea: compare only each page's "updated" date | Simple, but says *that* something changed, not *what*. And dates are unreliable: e.g. the Audit overview shows `ms.date` 2026-05-18 but `updated_at` 2026-07-08. We have to download the page to read the date anyway, so comparing text costs nothing extra. | Folded in: dates are recorded and shown in alerts, but text comparison decides |

## 5. Design

### 5.1 Repo layout
```
watchlist.yaml          # 116 URLs: section, title, core/optional, why (generated from starter-list.md)
snapshots/<slug>.md     # normalized main text of each page, one file per page
state.json              # per page: last hash, ms.date, updated_at, consecutive fetch failures
digest-queue.json       # digest-level changes waiting for Monday
digests/YYYY-Www.md     # each sent weekly digest, kept for reference
notifier/               # Python package: fetch, normalize, diff, classify, notify
tests/                  # unit tests with saved page fixtures
.github/workflows/check.yml    # every 3 hours
.github/workflows/digest.yml   # Mondays 08:00 Eastern
```

### 5.2 Check run (every 3 hours)
1. **Fetch** each watched page, about 1/sec. Read `ms.date` and `updated_at` from metadata.
2. **Normalize:** extract only the article body (no navigation, footer, feedback widgets or "In this article" box), convert to Markdown, collapse whitespace. The goal is that a page with no real edit produces identical text.
3. **Compare** with `snapshots/<slug>.md`. Identical → done.
4. **Diff** at paragraph and table-row level. Throw out hunks that differ only in whitespace, punctuation, letter case or link targets. If nothing remains, the change is "ignored" (snapshot still updated).
5. **Safety-net rules** (deterministic, run before the AI). Force **Push** if a changed hunk:
   - changes a number next to a time or size unit (day/days/month/year/GB/TB/items/rows/results), or
   - adds or removes the words *retire, deprecat, end of support, no longer, removed, replaced by*, or a license name (E3, E5, A5, G5, P1, P2, Premium, Standard, add-on).
6. **Classify with AI:** send the remaining hunks plus page title and section to `claude-haiku-5-5`. It returns JSON: `{level: push|digest|ignore, one_line_summary, old_text, new_text}`. The level can only be raised by the AI, never lowered below what the safety net set. If the API fails, default to **digest** (or push if the safety net fired).
7. **Notify:** push alerts go out immediately (ntfy priority high). Title = one-line summary. Body = old → new excerpt (trimmed to fit) + both dates. Tap → the Learn page. Digest items get appended to `digest-queue.json`.
8. **Commit** updated snapshots, state and queue to the repo. Commit message = list of changed pages, which gives the dated change history.

### 5.3 Special sources
- **"What's new" pages** (Purview, Defender XDR, Entra, Sentinel, Defender for Endpoint): handled like any page. Also, any `learn.microsoft.com` link in a new entry that isn't on the watch list → digest item "Suggested page to watch".
- **M365 Roadmap RSS:** new items only. Pre-filter by keywords (Purview, Audit, eDiscovery, Insider Risk, Defender, Entra, Sentinel, retention, Copilot audit), then classify like a page change.

### 5.4 Weekly digest (Mondays 08:00 Eastern)
- Group queued items by section. Write `digests/YYYY-Www.md` and commit it.
- Send one ntfy message: counts per section plus top 3 items. Tap → the digest file on GitHub.
- An empty week sends a one-line "No notable changes this week." That doubles as a weekly heartbeat proving the tool still runs.

### 5.5 Failures and edge cases
- **Page returns 404 or redirects elsewhere** → push alert ("page moved/removed"). Often means a feature was renamed or retired. Redirects within the same article (e.g. adding `?view=`) are ignored.
- **Transient fetch errors** → retry 3 times in the run. Alert only after 3 consecutive failed runs for the same page.
- **Workflow crash** → GitHub's own failure email. The Monday heartbeat catches silent breakage.
- **First run (baseline):** snapshot everything, send no change alerts, send one push: "Baseline complete: N pages watched."

### 5.6 Secrets (GitHub repo secrets)
`ANTHROPIC_API_KEY`, `NTFY_TOPIC`.

### 5.7 Testing
- Unit tests on saved HTML fixtures: normalization is stable across two fetches of an unchanged page; a whitespace-only edit → ignored; "90 days" → "180 days" → push via the safety net; a page removed → push.
- A dry-run mode prints what would be sent without notifying or committing.
- After setup: send one test push to confirm the phone receives it.

### 5.8 Budget check
116 pages × ~1 s plus overhead ≈ 3 min per run × 8 runs/day ≈ 720 min/month, within the 2,000 free minutes.

## 6. What the user must do (one-time, ~20 min)
1. Have a GitHub account (free).
2. Install the ntfy app on the phone and subscribe to the topic name the setup gives them.
3. Create a Claude API key and paste it as a repo secret. Set a $5/month spend cap in the console as a safeguard.

## 7. Calls made by Claude (not explicitly discussed; user may override)
- Check every **3 hours** (fits the free minutes; well within "same day").
- Digest on **Monday 08:00 Eastern**, with an empty-week heartbeat.
- **ntfy** for delivery, **Python** for the code.
- Ambiguous changes go **up** a level, never down.
- Page removed or moved = push alert.
- The AI can raise a level but never lower one the rules set.

## 8. Left to the builder
HTML extraction details, exact prompt wording, file formats, and diff library choice. Constraints: identical output on unchanged pages, and no personal data in requests.
