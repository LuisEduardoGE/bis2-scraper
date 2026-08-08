"""
Business IT Solutions 2 — SECOND site scraper: quotes.toscrape.com -> Supabase

This is your "own scraped website" pipeline (the brief wants two). quotes.toscrape.com
is the standard, scrape-safe companion to books.toscrape.com. Scrapes every quote
(text, author, tags) across all pages and upserts into a Supabase table.

    pip install -r requirements.txt          # same deps as the books scraper
    # run schema_quotes.sql in Supabase first
    # env: SUPABASE_URL, SUPABASE_KEY
    python scraper_quotes.py

Business question this feeds: "Which authors and themes (tags) dominate the collection?"
"""
from __future__ import annotations
import os
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from supabase import create_client
try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError:
    pass

BASE = "https://quotes.toscrape.com/"


def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=30, headers={"User-Agent": "ITID-workshop-scraper/1.0"})
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


def parse_quote(div) -> dict:
    text = div.select_one(".text").get_text(strip=True)
    author = div.select_one(".author").get_text(strip=True)
    tags = [t.get_text(strip=True) for t in div.select(".tags a.tag")]
    # stable id so re-runs upsert instead of duplicating
    qid = hashlib.sha1((author + "|" + text).encode("utf-8")).hexdigest()[:16]
    return {"quote_id": qid, "text": text, "author": author, "tags": tags}


def scrape_all() -> list[dict]:
    quotes: list[dict] = []
    url = BASE
    while url:
        soup = get_soup(url)
        for div in soup.select("div.quote"):
            quotes.append(parse_quote(div))
        nxt = soup.select_one("li.next a")
        url = urljoin(url, nxt["href"]) if nxt else None
        time.sleep(0.5)
    return quotes


def main() -> None:
    client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    quotes = scrape_all()
    print(f"Scraped {len(quotes)} quotes")
    for i in range(0, len(quotes), 100):
        client.table("quotes").upsert(quotes[i : i + 100], on_conflict="quote_id").execute()
    print("Upserted to Supabase table 'quotes'")


if __name__ == "__main__":
    main()
