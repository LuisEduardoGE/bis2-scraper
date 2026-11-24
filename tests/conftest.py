"""Shared fixtures. Tests run fully offline: no HTTP requests and no Supabase client."""

import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

sys.path.insert(0, str(ROOT))


def load_soup(name: str) -> BeautifulSoup:
    return BeautifulSoup((FIXTURES / name).read_text(encoding="utf-8"), "html.parser")


def without_next_link(soup: BeautifulSoup) -> BeautifulSoup:
    """Same page, but as the last page: no `li.next` pager link."""
    copy = BeautifulSoup(str(soup), "html.parser")
    for li in copy.select("li.next"):
        li.decompose()
    return copy


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    """Fail loudly if any test tries to reach the network or Supabase."""

    def blocked(*args, **kwargs):
        raise AssertionError("tests must not make network calls")

    monkeypatch.setattr("requests.get", blocked)
    monkeypatch.setattr("time.sleep", lambda _seconds: None)


class FakeTable:
    def __init__(self, calls, name):
        self.calls, self.name = calls, name

    def upsert(self, rows, on_conflict):
        self.calls.append((self.name, list(rows), on_conflict))
        return self

    def execute(self):
        return None


class FakeClient:
    """Records `client.table(name).upsert(rows, on_conflict=...).execute()` calls."""

    def __init__(self):
        self.calls = []

    def table(self, name):
        return FakeTable(self.calls, name)
