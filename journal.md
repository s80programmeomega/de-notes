# Journal

One line per day, newest at the bottom. Format: `YYYY-MM-DD — what I learned or what confused me.`

Example: `2026-10-01 — A .gitignore rule without a leading / matches at any depth; anchor it.`

2026-10-01 — Created de-project-1 and de-notes and pushed the first commits. A .gitignore rule without a leading / matches at any depth, so I anchored /raw/ and /data/ and whitelisted dbt/seeds so seed CSVs can be committed.
2026-10-02 — Ran Postgres 17 in Docker Compose and loaded a 5-row CSV with \copy. Ports 5432 and 5433 were already used by two Postgres servers installed on my machine, so I mapped the container to 55432 via POSTGRES_PORT in .env. I forgot the ; in psql, got the -# prompt, and \copy ran before the table existed.
2026-10-02 — Q: Why a healthcheck? A: Started only means the process launched; Postgres may still be initializing. pg_isready says when it accepts connections, so services like Airflow can wait for "healthy".
2026-10-02 — Q: What does the named volume do? A: It stores /var/lib/postgresql/data outside the container, so my tables survive down and up. Only down -v deletes it.
2026-10-02 — Q: Why mount ./data? A: \copy runs inside the container and cannot see folders on my laptop. The bind mount shows my data/ folder there as /data, read-only.
