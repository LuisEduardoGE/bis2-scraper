import csv

import pytest
from conftest import ROOT, FakeClient, load_soup, without_next_link

import scraper_books

PAGE_URL = "https://books.toscrape.com/catalogue/page-1.html"


@pytest.fixture
def books():
    soup = load_soup("books_page1.html")
    return [scraper_books.parse_book(a, PAGE_URL) for a in soup.select("article.product_pod")]


def test_parse_book_reads_every_field(books):
    assert len(books) == 5
    assert books[0] == {
        "title": "A Light in the Attic",
        "price_gbp": 51.77,
        "rating": 3,
        "in_stock": True,
        "detail_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    }


def test_title_comes_from_the_untruncated_title_attribute(books):
    # The link text is "Sapiens: A Brief History ..."; the title attribute is complete.
    assert books[4]["title"] == "Sapiens: A Brief History of Humankind"


def test_star_rating_words_map_to_numbers(books):
    assert [b["rating"] for b in books] == [3, 1, 1, 4, 5]


def test_rating_defaults_to_zero_for_unknown_word():
    soup = load_soup("books_page1.html")
    article = soup.select_one("article.product_pod")
    article.select_one(".star-rating")["class"] = ["star-rating", "Zero"]
    assert scraper_books.parse_book(article, PAGE_URL)["rating"] == 0


def test_out_of_stock_is_detected():
    soup = load_soup("books_page1.html")
    article = soup.select_one("article.product_pod")
    article.select_one(".availability").string = "Out of stock"
    assert scraper_books.parse_book(article, PAGE_URL)["in_stock"] is False


def test_parsed_rows_match_committed_sample_csv(books):
    with open(ROOT / "books.csv", encoding="utf-8", newline="") as fh:
        sample = list(csv.DictReader(fh))[: len(books)]
    for row, book in zip(sample, books):
        assert row["title"] == book["title"]
        assert float(row["price_gbp"]) == book["price_gbp"]
        assert int(row["rating"]) == book["rating"]
        assert (row["in_stock"] == "True") == book["in_stock"]
        assert row["detail_url"] == book["detail_url"]


def test_scrape_all_follows_pagination_until_last_page(monkeypatch):
    page = load_soup("books_page1.html")
    requested = []

    def fake_get_soup(url):
        requested.append(url)
        return page if len(requested) == 1 else without_next_link(page)

    monkeypatch.setattr(scraper_books, "get_soup", fake_get_soup)
    books = scraper_books.scrape_all()

    assert requested == [PAGE_URL, "https://books.toscrape.com/catalogue/page-2.html"]
    assert len(books) == 10


def test_main_upserts_in_batches_on_detail_url(monkeypatch):
    client = FakeClient()
    rows = [{"detail_url": f"u{i}"} for i in range(250)]
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "placeholder")
    monkeypatch.setattr(scraper_books, "create_client", lambda url, key: client)
    monkeypatch.setattr(scraper_books, "scrape_all", lambda: rows)

    scraper_books.main()

    assert [(name, len(batch), key) for name, batch, key in client.calls] == [
        ("books", 100, "detail_url"),
        ("books", 100, "detail_url"),
        ("books", 50, "detail_url"),
    ]
