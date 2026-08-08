-- Run this in the Supabase SQL editor before the first scrape.
create table if not exists books (
    id           bigint generated always as identity primary key,
    title        text not null,
    price_gbp    numeric(6,2),
    rating       int,
    in_stock     boolean,
    detail_url   text unique not null,     -- upsert key
    scraped_at   timestamptz not null default now()
);

-- Helpful index for the dashboard's category/price queries
create index if not exists books_rating_idx on books (rating);
create index if not exists books_price_idx  on books (price_gbp);

-- Second site (your own): quotes.toscrape.com
create table if not exists quotes (
    id          bigint generated always as identity primary key,
    quote_id    text unique not null,        -- upsert key (hash of author+text)
    text        text not null,
    author      text not null,
    tags        text[],                      -- Postgres array; Looker can UNNEST or count
    scraped_at  timestamptz not null default now()
);
create index if not exists quotes_author_idx on quotes (author);
