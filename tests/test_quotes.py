import csv
import hashlib

import pytest
from conftest import ROOT, FakeClient, load_soup, without_next_link

import scraper_quotes


@pytest.fixture
def quotes():
    soup = load_soup("quotes_page1.html")
    return [scraper_quotes.parse_quote(div) for div in soup.select("div.quote")]


def test_parse_quote_reads_text_author_and_tags(quotes):
    assert len(quotes) == 3
    first = quotes[0]
    assert first["author"] == "Albert Einstein"
    assert first["text"].startswith("“The world as we have created it")
    assert first["tags"] == ["change", "deep-thoughts", "thinking", "world"]


def test_quote_id_is_a_stable_hash_of_author_and_text(quotes):
    for q in quotes:
        expected = hashlib.sha1((q["author"] + "|" + q["text"]).encode("utf-8")).hexdigest()[:16]
        assert q["quote_id"] == expected
    assert len({q["quote_id"] for q in quotes}) == len(quotes)


def test_parsed_rows_match_committed_sample_csv(quotes):
    with open(ROOT / "quotes.csv", encoding="utf-8", newline="") as fh:
        sample = list(csv.DictReader(fh))[: len(quotes)]
    for row, q in zip(sample, quotes):
        assert row["quote_id"] == q["quote_id"]
        assert row["text"] == q["text"]
        assert row["author"] == q["author"]
        assert row["tags"].split(",") == q["tags"]


def test_scrape_all_follows_pagination_until_last_page(monkeypatch):
    page = load_soup("quotes_page1.html")
    requested = []

    def fake_get_soup(url):
        requested.append(url)
        return page if len(requested) == 1 else without_next_link(page)

    monkeypatch.setattr(scraper_quotes, "get_soup", fake_get_soup)
    quotes = scraper_quotes.scrape_all()

    assert requested == ["https://quotes.toscrape.com/", "https://quotes.toscrape.com/page/2/"]
    assert len(quotes) == 6


def test_main_upserts_in_batches_on_quote_id(monkeypatch):
    client = FakeClient()
    rows = [{"quote_id": str(i)} for i in range(101)]
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "placeholder")
    monkeypatch.setattr(scraper_quotes, "create_client", lambda url, key: client)
    monkeypatch.setattr(scraper_quotes, "scrape_all", lambda: rows)

    scraper_quotes.main()

    assert [(name, len(batch), key) for name, batch, key in client.calls] == [
        ("quotes", 100, "quote_id"),
        ("quotes", 1, "quote_id"),
    ]
