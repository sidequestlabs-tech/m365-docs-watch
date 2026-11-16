"""Paragraph/table-row level diffs between two snapshots."""
import difflib
import re
from dataclasses import dataclass

LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


@dataclass(frozen=True)
class Hunk:
    old_text: str
    new_text: str


def _units(text: str) -> list[str]:
    units = []
    for para in re.split(r"\n\s*\n", text.strip()):
        lines = [ln for ln in para.splitlines() if ln.strip()]
        if lines and all(ln.lstrip().startswith(("|", "- ", "* ")) or re.match(r"\s*\d+\.\s", ln) for ln in lines):
            units.extend(ln.strip() for ln in lines)      # table rows / list items stand alone
        elif lines:
            units.append("\n".join(lines).strip())
    return units


def diff_hunks(old: str, new: str) -> list[Hunk]:
    a, b = _units(old), _units(new)
    hunks = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != "equal":
            hunks.append(Hunk("\n".join(a[i1:i2]), "\n".join(b[j1:j2])))
    return hunks


def _canon(s: str) -> str:
    return re.sub(r"[\W_]+", "", LINK.sub(r"\1", s).lower())


def is_trivial(h: Hunk) -> bool:
    return _canon(h.old_text) == _canon(h.new_text)
