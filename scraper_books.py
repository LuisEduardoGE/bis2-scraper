"""
Business IT Solutions 2 — demo scraper: books.toscrape.com -> Supabase

The workshop's "demo bookstore" is the standard practice site books.toscrape.com
(safe to scrape). This scrapes every book (title, price, rating, availability,
category) across all pages and upserts them into a Supabase (Postgres) table.

Setup:
    pip install -r requirements.txt
    # create table first: run schema.sql in the Supabase SQL editor
    # set env vars (or a .env): SUPABASE_URL, SUPABASE_KEY

Run:
    python scraper_books.py
"""
from __future__ import annotations
import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from supabase import create_client
try:
    from dotenv import load_dotenv; load_dotenv()   # reads .env if present
except ImportError:
    pass

BASE = "https://books.toscrape.com/"
RATING = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=30, headers={"User-Agent": "ITID-workshop-scraper/1.0"})
    resp.raise_for_status()
    resp.encoding = "utf-8"  # site declares UTF-8 in <meta> but not the HTTP header
    return BeautifulSoup(resp.text, "html.parser")


def parse_book(article, page_url: str) -> dict:
    title = article.h3.a["title"]
    price = float(re.sub(r"[^0-9.]", "", article.select_one(".price_color").text))
    rating = RATING.get(article.select_one(".star-rating")["class"][1], 0)
    in_stock = "In stock" in article.select_one(".availability").text
    detail_url = urljoin(page_url, article.h3.a["href"])
    return {
        "title": title,
        "price_gbp": price,
        "rating": rating,
        "in_stock": in_stock,
        "detail_url": detail_url,
    }


def scrape_all() -> list[dict]:
    books: list[dict] = []
    url = urljoin(BASE, "catalogue/page-1.html")
    while url:
        soup = get_soup(url)
        for art in soup.select("article.product_pod"):
            books.append(parse_book(art, url))
        nxt = soup.select_one("li.next a")
        url = urljoin(url, nxt["href"]) if nxt else None
        time.sleep(0.5)  # be polite
    return books


def main() -> None:
    supabase_url = os.environ["SUPABASE_URL"]
    supabase_key = os.environ["SUPABASE_KEY"]
    client = create_client(supabase_url, supabase_key)

    books = scrape_all()
    print(f"Scraped {len(books)} books")

    # upsert in batches on the unique detail_url
    for i in range(0, len(books), 100):
        batch = books[i : i + 100]
        client.table("books").upsert(batch, on_conflict="detail_url").execute()
    print("Upserted to Supabase table 'books'")


if __name__ == "__main__":
    main()
