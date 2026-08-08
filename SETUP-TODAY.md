# 🏗️ Business IT Solutions 2 — build the whole pipeline TODAY

Do all of this now (no camera). Tomorrow's video is just narrating the finished result (~4 min).
✅ Both scrapers are already verified end-to-end: **1,000 books, 100 quotes** (see `books.csv` / `quotes.csv`).

Work order: **① Supabase → ② run scrapers → ③ Looker dashboards → ④ GitHub Action**.

---

## ① Supabase (≈10 min)
1. Go to https://supabase.com → sign in → **New project** (name it `bis2`, pick a region near you, set a DB password — save it).
2. Left sidebar → **SQL Editor** → **New query** → paste the contents of `schema.sql` → **Run**. (Creates `books` + `quotes`.)
3. **Project Settings → API**: copy the **Project URL** and the **service_role** key.
4. In this folder, copy `.env.example` to `.env` and paste those two values in.

## ② Run the scrapers → populate the tables (≈5 min)
In PowerShell, in this `reference-base` folder:
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scraper_books.py      # -> "Upserted to Supabase table 'books'"  (1000 rows)
python scraper_quotes.py     # -> "Upserted to Supabase table 'quotes'" (100 rows)
```
Check in Supabase → **Table Editor** → `books` (1000) and `quotes` (100). ✅
*(The scrapers auto-read `.env`. Re-running never duplicates — they upsert on a unique key.)*

## ③ Looker Studio — 2 dashboards (≈60–75 min)
Go to https://lookerstudio.google.com → **Create → Data source → PostgreSQL**.

**Connection (from Supabase → Settings → Database → Connection info / Connection pooling):**
- Host: the **Session pooler** host, e.g. `aws-0-<region>.pooler.supabase.com`
- Port: `5432` · Database: `postgres` · Username: `postgres.<your-project-ref>` · Password: your DB password
- **Enable SSL** (tick it). Authorize → pick the `books` table → **Create report**.
> If the Postgres connector gives you trouble, fallback: Supabase Table Editor → **Export CSV**, upload to Google Sheets, and use the **Google Sheets** connector. (Still show the Supabase table in the video.)

**Dashboard A — Books** · business question: *"Does a higher rating cost more — and where's the value?"*
- **Scorecard (KPI):** Record Count → label "Books scraped" (1000). Add a second: AVG `price_gbp` (≈ **£35.07**).
- **Bar chart:** Dimension `rating`, Metric AVG `price_gbp`.
- **Table:** `title` + `price_gbp`, filter `rating = 5`, sort price ascending (the cheap 5★ gems).
- **Control:** add a **Slider** on `price_gbp` (or a drop-down on `rating`).
- **Insight text box (pre-written):** *"Rating barely moves price — every star level averages ~£35 — so the real value is the **42 five-star books priced under £20**, shown below."*

**Dashboard B — Quotes** · business question: *"Which authors and themes dominate?"*
- **Scorecard (KPI):** Record Count → "Quotes" (100); second: distinct `author` (50).
- **Bar chart:** Dimension `author`, Metric Record Count, sort desc, limit 10.
- **Second visual:** tags — quick option: a table of `tags` by count, or a bar of the top tags.
- **Control:** drop-down on `author`.
- **Insight text box (pre-written):** *"The collection skews to a few voices — **Einstein (10), Rowling (9), Monroe (7)** — and the dominant themes are **love, inspirational, life**."*

Name the reports `Guerreiro_Espindola_Books` / `_Quotes`.

## ④ GitHub Action — the automatic run (≈10 min)
In this `reference-base` folder (it already contains `.github/workflows/scrape.yml`):
```powershell
git init; git add .; git commit -m "BIS2 scraping pipeline"
gh repo create bis2-scraper --public --source=. --push
```
*(No `gh`? Create an empty repo `bis2-scraper` on github.com, then:)*
```powershell
git remote add origin https://github.com/LuisEduardoGE/bis2-scraper.git
git branch -M main; git push -u origin main
```
Then on GitHub: **Settings → Secrets and variables → Actions → New repository secret** — add `SUPABASE_URL` and `SUPABASE_KEY` (same values as `.env`).
Finally **Actions** tab → "Scheduled scrape (books + quotes)" → **Run workflow** → wait for the green ✓.

---

## ✅ Done-today checklist (no camera)
- [ ] Supabase project + `schema.sql` run
- [ ] `books` (1000) and `quotes` (100) populated
- [ ] Dashboard A (books) with KPI + 2 visuals + control + insight
- [ ] Dashboard B (quotes) with KPI + 2 visuals + control + insight
- [ ] Repo pushed, secrets added, **green** Action run

## 🎬 Tomorrow (camera only, ~4 min)
Read `TELEPROMPTER — record order (both sites).md`: for each site show **code → Supabase table → Looker dashboard (say the insight) → the green GitHub run**. Then upload + Submit (5 attempts).
