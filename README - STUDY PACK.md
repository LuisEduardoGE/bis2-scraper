# Business IT Solutions 2 — reference base + dashboard/video guide (draft)

> ⚠️ Learning reference. The scraper is a working starting point for the **demo bookstore**
> (books.toscrape.com). Do your **own** second site, connect your **own** Supabase, build the
> dashboard yourself, and record your **own** screen. Send me your version and I'll validate it.

## What's here
```
reference-base/
├── scraper_books.py            # demo scraper -> Supabase (upsert)
├── requirements.txt
├── schema.sql                  # run in Supabase SQL editor first
└── .github/workflows/scrape.yml# daily GitHub Actions cron (the "automatic execution")
```

## Deliverables the brief wants (both sites)
For **the demo bookstore** AND **your own scraped website**, the video must show:
1. the **scraping code**, 2. the **data in Supabase**, 3. the **Looker Studio dashboard**
(with the business-question answer explained), 4. the **GitHub workflow** running the scraper automatically.

## Setup (demo site)
1. In Supabase: create a project, open **SQL editor**, run `schema.sql`.
2. Get your **Project URL** and a **service_role key** (Settings → API).
3. Locally: `pip install -r requirements.txt`, set `SUPABASE_URL` / `SUPABASE_KEY`, run `python scraper_books.py`.
4. Push this folder to a GitHub repo; add `SUPABASE_URL` + `SUPABASE_KEY` as **repo secrets** (Settings → Secrets → Actions). The workflow then runs daily and via "Run workflow".

## Your own second website
Pick something with listings you can legally scrape (respect robots.txt / ToS). Good fits for your skills:
- a real-estate site (you've built House Hunter) → columns: price, bedrooms, city, url
- a job board → title, company, location, salary
Copy `scraper_books.py`, change the parser + table, add a second workflow (or a second step).

## Looker Studio dashboard — build recipe (meets the rubric)
**Business question (demo):** *"Where's the value — are higher-rated books priced higher, and where are the cheap 5-star buys?"*

Connect Looker Studio → **PostgreSQL** connector → your Supabase host/db/user/password (Supabase gives these under Settings → Database).

Build these (the brief requires ≥1 KPI, ≥2 visuals, ≥1 control, 1 insight):
- **KPI scorecard** — total books scraped (and/or average price). *(≥1 KPI ✓)*
- **Visual 1** — bar chart: average `price_gbp` by `rating`. *(answers the question)*
- **Visual 2** — scatter or table: cheapest books at rating = 5 (sort price ascending). *(≥2 visuals ✓)*
- **Control** — a slider/range filter on `price_gbp`, or a drop-down on `rating`. *(≥1 control ✓)*
- **Layout** — title, aligned tiles, not overloaded.
- **Insight text box** — e.g. *"Rating barely tracks price here, so the best value is 5-star books under £20 — highlighted below."* *(1 clear insight ✓)*

## 🎬 Video walkthrough script (~4–5 min, cover BOTH sites)
```
[INTRO 15s] "Hi, I'm Luis — Business IT Solutions 2 retake. I built two scraping
pipelines into Supabase with Looker Studio dashboards, and both run automatically on GitHub."

[DEMO SITE — CODE 45s] "Here's the scraper for books.toscrape.com. It walks every page,
parses title, price, rating, availability, and upserts into Supabase on the URL so re-runs
don't duplicate." (show scraper_books.py)

[DEMO SITE — SUPABASE 30s] "Here's the data in Supabase — [N] rows in the books table."
(show table)

[DEMO SITE — DASHBOARD 45s] "My business question was [question]. This KPI shows [x];
this chart shows average price by rating; and with this filter I can [do x]. The insight:
[your one-line insight]." (show Looker Studio, move the control live)

[DEMO SITE — GITHUB 30s] "And it runs itself — this GitHub Actions workflow scrapes on a
daily cron. Here's a successful run." (show Actions tab, green run)

[YOUR SITE 90s] Repeat the four beats for your own website: code, Supabase data,
dashboard + insight, workflow.

[WRAP 15s] "That's two end-to-end data pipelines — scrape, store, visualise, automate.
Thanks for watching."
```

## Checklist
- [ ] Demo + own site scraped, both tables populated in Supabase
- [ ] 2 Looker dashboards: KPI + 2 visuals + control + insight each
- [ ] Both GitHub Actions workflows show a green run
- [ ] Video covers all 4 beats for BOTH sites → **Submit** (5 attempts)
