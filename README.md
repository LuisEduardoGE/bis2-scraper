# bis2-scraper

**A small scrape-to-dashboard data pipeline.** Two Python scrapers collect structured data from public practice sites and upsert it into Supabase (Postgres), ready for a BI dashboard such as Looker Studio.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Postgres-3FCF8E?style=flat-square&logo=supabase&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-555?style=flat-square)

| Scraper | Source | Table | Rows |
|---|---|---|---|
| `scraper_books.py` | [books.toscrape.com](https://books.toscrape.com) | `books`: title, price, rating, stock, url | 1,000 |
| `scraper_quotes.py` | [quotes.toscrape.com](https://quotes.toscrape.com) | `quotes`: text, author, tags[] | 100 |

Both sites are sandboxes built for scraping practice. Sample output is committed as `books.csv` and `quotes.csv`.

## How it works

```
toscrape site ──requests──▶ BeautifulSoup parse ──▶ rows ──upsert──▶ Supabase (Postgres) ──▶ dashboard
```

- Follows pagination until the last page; polite timeouts and an explicit User-Agent.
- **Idempotent**: upserts on a natural key (`detail_url` for books, a hash of author + text for quotes), so re-running never duplicates rows.
- Tags are stored as a Postgres `text[]` array; indexes on rating, price and author support dashboard queries.

## Setup

1. Create a Supabase project and run [`schema.sql`](schema.sql) in its SQL editor.
2. Install and configure:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (never commit it):

```
SUPABASE_URL=https://<project>.supabase.co
SUPABASE_KEY=<service-role key>
```

3. Run:

```bash
python scraper_books.py
python scraper_quotes.py
```

## License

[MIT](LICENSE)
