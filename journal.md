# Journal

One line per day, newest at the bottom. Format: `YYYY-MM-DD — what I learned or what confused me.`

Example: `2026-10-01 — A .gitignore rule without a leading / matches at any depth; anchor it.`

2026-10-01 — Created de-project-1 and de-notes and pushed the first commits. A .gitignore rule without a leading / matches at any depth, so I anchored /raw/ and /data/ and whitelisted dbt/seeds so seed CSVs can be committed.
2026-10-02 — Ran Postgres 17 in Docker Compose and loaded a 5-row CSV with \copy. Ports 5432 and 5433 were already used by two Postgres servers installed on my machine, so I mapped the container to 55432 via POSTGRES_PORT in .env. I forgot the ; in psql, got the -# prompt, and \copy ran before the table existed.
2026-10-02 — Q: Why a healthcheck? A: Started only means the process launched; Postgres may still be initializing. pg_isready says when it accepts connections, so services like Airflow can wait for "healthy".
2026-10-02 — Q: What does the named volume do? A: It stores /var/lib/postgresql/data outside the container, so my tables survive down and up. Only down -v deletes it.
2026-10-02 — Q: Why mount ./data? A: \copy runs inside the container and cannot see folders on my laptop. The bind mount shows my data/ folder there as /data, read-only.
2026-10-03 — Downloaded NYC taxi (3.7M rows, Parquet) and World Bank Cameroon (CSV) and profiled both with a small DuckDB script. Grain: taxi = one row per trip; World Bank = one row per indicator, with years as columns (wide format).
2026-10-03 — The World Bank year columns mix units (homicides per 100k, life expectancy, population, GDP), so min/max/averages per column mean nothing. About 55% of cells are empty and 117 indicators have no data at all.
2026-10-03 — Data quality = can I trust the data; wrangling = the work of fixing it. A data engineer automates the checks so bad data does not spread. To check in Week 1: negative fares, a 269,097-mile trip, five columns sharing the same 29.2% nulls.
2026-10-03 — GDP = total value of goods and services a country produces in a year. DuckDB reads Parquet/CSV files directly with SQL, no server or loading step.
