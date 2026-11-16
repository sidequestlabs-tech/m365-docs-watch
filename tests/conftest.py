from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

def read(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")
