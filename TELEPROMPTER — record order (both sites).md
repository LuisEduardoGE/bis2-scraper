# 🎬 Business IT Solutions 2 — record-order teleprompter (both sites)

Both scraper pipelines are written for you (books = demo, quotes = your own site). The video
must show, **for each site**: code → data in Supabase → Looker dashboard (with the answer) → the
GitHub workflow running it. 5 attempts.

## Setup once (before recording)
1. Supabase → SQL editor → run `schema.sql` (creates `books` + `quotes`).
2. Get Project URL + service_role key → set `SUPABASE_URL`, `SUPABASE_KEY`.
3. `pip install -r requirements.txt`, then `python scraper_books.py` and `python scraper_quotes.py`.
4. Push the repo; add the two secrets in GitHub → Settings → Secrets → Actions; run the workflow once.
5. In Looker Studio, connect the PostgreSQL connector to Supabase and build the two dashboards
   (recipe in `README - STUDY PACK.md`).

---

## [0:00] INTRO · 15s
"Hi, I'm Luis — Business IT Solutions 2 retake. I built two scraping pipelines into Supabase,
each with a Looker Studio dashboard, and both run automatically on GitHub Actions."

## [0:15] DEMO SITE — books.toscrape.com · ~90s
- **Code:** show `scraper_books.py` — "walks every page, parses title, price, rating, availability, upserts into Supabase on the URL so re-runs don't duplicate."
- **Supabase:** show the `books` table — "[N] rows."
- **Dashboard:** open your Looker report — "My business question: are higher-rated books priced higher, and where are the cheap 5-star buys? This KPI shows total books / average price; this chart is average price by rating; and with this filter I can narrow the price range." Move the control live. State the **insight**.
- **GitHub:** show the Actions tab → a green run of "Scrape demo bookstore."

## [1:45] YOUR SITE — quotes.toscrape.com · ~90s
- **Code:** show `scraper_quotes.py` — "same pattern on my own chosen site; parses quote text, author and tags, upserts on a hash of author+text."
- **Supabase:** show the `quotes` table — "[N] rows, tags stored as a Postgres array."
- **Dashboard:** open the second Looker report — "Business question: which authors and themes dominate? KPI = total quotes; bar chart = quotes per author (top 10); the tags feed a second visual; this control filters by author." State the **insight**.
- **GitHub:** show the same workflow's "Scrape quotes (own site)" step running green.

## [3:15] WRAP · 15s
"That's two end-to-end pipelines — scrape, store in Supabase, visualise in Looker, and automate
with GitHub Actions. Thanks for watching."

---

## Each dashboard must have (rubric)
- [ ] ≥1 KPI scorecard
- [ ] ≥2 analytical visuals
- [ ] ≥1 slicer / filter / control (move it on camera)
- [ ] readable, aligned layout
- [ ] ≥1 clear insight tying back to the business question
- [ ] both GitHub steps show a green run → **Submit**
