"""Turn a Learn page into stable Markdown of just the article body."""
import re

from bs4 import BeautifulSoup
from markdownify import markdownify

from notifier.fetch import FetchError

MIN_ARTICLE_CHARS = 200
STRIP_SELECTORS = [
    "nav", "footer", "aside", "script", "style", "noscript",
    "#article-metadata", "#article-metadata-footer", "#user-feedback", "#site-user-feedback-footer",
    "#center-doc-outline", "#ms--additional-resources-mobile", ".page-metadata", "[data-bi-name='feedback']",
]
DYNAMIC_LINE = re.compile(r"(minutes? to read|\b\d+ contributors?\b)", re.I)


def parse_dates(html: str) -> tuple[str | None, str | None]:
    soup = BeautifulSoup(html, "html.parser")

    def meta(name):
        tag = soup.find("meta", attrs={"name": name})
        return tag.get("content") if tag else None

    return meta("ms.date"), meta("updated_at")


def extract_article(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    if main is None:
        raise FetchError("no <main> element")
    for sel in STRIP_SELECTORS:
        for el in main.select(sel):
            el.decompose()
    blocks = main.select("div.content")
    if not blocks:
        raise FetchError("no article content")
    body = max(blocks, key=lambda b: len(b.get_text()))
    h1 = main.find("h1")
    md = markdownify(str(body), heading_style="ATX", bullets="-")
    if h1 and h1.get_text(strip=True) not in md[:300]:
        md = f"# {h1.get_text(strip=True)}\n\n{md}"
    lines = [ln.rstrip() for ln in md.splitlines() if not DYNAMIC_LINE.search(ln)]
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"
    if len(text) < MIN_ARTICLE_CHARS:
        raise FetchError(f"article too short ({len(text)} chars)")
    return text
