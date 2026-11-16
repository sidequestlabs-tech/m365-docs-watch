"""Deterministic safety net: changes that must always reach the phone."""
import re
from collections import Counter

from notifier.diff import Hunk

UNITS = r"days?|months?|years?|hours?|GB|TB|MB|items|rows|results|records"
NUM_UNIT = re.compile(rf"(\d[\d,.]*)\s*-?\s*({UNITS})\b", re.I)
LIFECYCLE = re.compile(r"retire|retirement|deprecat|end of support|no longer|removed|replaced by", re.I)
LICENSE = re.compile(r"\b(E3|E5|A3|A5|G3|G5|P1|P2|Premium|Standard|add-on)\b")


def _num_units(s: str) -> Counter:
    return Counter((n.replace(",", ""), u.lower().rstrip("s")) for n, u in NUM_UNIT.findall(s))


def rule_floor(h: Hunk) -> str:
    old, new = h.old_text, h.new_text
    if _num_units(old) != _num_units(new):
        return "push"
    if {m.lower() for m in LIFECYCLE.findall(old)} != {m.lower() for m in LIFECYCLE.findall(new)}:
        return "push"
    if set(LICENSE.findall(old)) != set(LICENSE.findall(new)):
        return "push"
    return "digest"
