# Data Engineering Tracker

Copy this file into your `de-notes` repo. Tick boxes as you finish (`- [x]`). GitHub renders the checkboxes and lets you tick them in the web UI.

Week 0 starts Sep 29, 2026; Week 1 starts Oct 5; Week 12 ends Dec 27.

# Setup

## Week 0 · Setup (Sep 29–Oct 4)

- [x] **Tue** (1.5h) — Install Docker, Python env, packages
- [x] **Thu** (1h) — Create GitHub repos; configure ruff
- [x] **Fri** (1.5h) — Postgres via Compose; load a CSV
- [ ] **Sat** (2h) — Download datasets; DuckDB; data dictionary
- [ ] ★ **Deliverable:** Environment ready (Docker, Python, Postgres, repos)

Notes:


# Phase 1 · SQL & data modeling

## Week 1 · SQL core (Oct 5–11)

- [ ] **Mon** (2h) — Query order, joins, fan-out (SQLBolt)
- [ ] **Tue** (2h) — NULLs, GROUP BY, CTEs; pgexercises
- [ ] **Wed** (1.5h) — 8 join/aggregation problems
- [ ] **Thu** (2h) — Window functions; dedupe from memory
- [ ] **Fri** (2h) — Kaggle window lesson; load taxi data
- [ ] **Sat** (4h) — Write 10 analytical queries on taxi data
- [ ] **Sun** (1h) — Checkpoint questions; commit
- [ ] ★ **Deliverable:** queries/week1.sql with 10 analytical queries

Notes:


## Week 2 · Query performance (Oct 12–18)

- [ ] **Mon** (2h) — EXPLAIN on 3 queries
- [ ] **Tue** (2h) — Indexes + Use The Index, Luke
- [ ] **Wed** (1.5h) — Generate 5–10M rows; baseline timings
- [ ] **Thu** (2h) — Stats, join algorithms, partitioning
- [ ] **Fri** (2h) — Tune queries 1–2; capture plans
- [ ] **Sat** (4h) — Tune query 3; partial/covering index; write-up
- [ ] **Sun** (1h) — Checkpoint questions; commit
- [ ] ★ **Deliverable:** docs/performance-notes.md (before/after plans)

Notes:


## Week 3 · Dimensional modeling I (Oct 19–25)

- [ ] **Mon** (2h) — Kimball steps, grain, OLTP vs OLAP
- [ ] **Tue** (2h) — Fact types, additivity, surrogate keys
- [ ] **Wed** (1.5h) — Sketch a model from ScheduleSync/GreatKart
- [ ] **Thu** (2h) — Star vs snowflake; finalize ER diagram
- [ ] **Fri** (2h) — Write star schema DDL
- [ ] **Sat** (4h) — Seed data (Faker); 5 business queries
- [ ] **Sun** (1h) — Checkpoint questions; commit
- [ ] ★ **Deliverable:** Star schema DDL, ER diagram, seed script

Notes:


## Week 4 · Modeling II + mini project (Oct 26–Nov 1)

- [ ] **Mon** (2h) — SCD types; design Type 2 dimension
- [ ] **Tue** (2h) — Medallion, ETL vs ELT, Parquet, DuckDB
- [ ] **Wed** (1.5h) — CSV to Parquet; compare size and speed
- [ ] **Thu** (2h) — Bronze and silver layers
- [ ] **Fri** (2h) — Gold layer + Type 2 load
- [ ] **Sat** (4h) — Test SCD2; 3 business queries; README
- [ ] **Sun** (1h) — Checkpoint questions; tag repo
- [ ] ★ **Deliverable:** Mini project 1 tagged and published

Notes:


# Phase 2 · Pipelines & orchestration

## Week 5 · Ingestion patterns (Nov 2–8)

- [ ] **Mon** (2h) — Idempotency, incremental loads; pick API
- [ ] **Tue** (2h) — Extract: pagination, retries, raw JSON
- [ ] **Wed** (1.5h) — Validate (Pydantic/Pandera); quarantine
- [ ] **Thu** (2h) — Upsert load + watermark
- [ ] **Fri** (2h) — Package, config, pytest
- [ ] **Sat** (4h) — Dockerize; prove idempotency; README
- [ ] **Sun** (1h) — Checkpoint questions; commit
- [ ] ★ **Deliverable:** Idempotent pipeline: run twice, same counts

Notes:


## Week 6 · Airflow (Nov 9–15)

- [ ] **Mon** (2h) — Concepts; run Airflow in Docker
- [ ] **Tue** (2h) — Tutorial + TaskFlow API
- [ ] **Wed** (1.5h) — Toy DAG using the data interval
- [ ] **Thu** (2h) — Connections, XCom rules, sensors, backfill
- [ ] **Fri** (2h) — Port Week 5 pipeline into a DAG
- [ ] **Sat** (4h) — Quality task; break/fix; 7-day backfill
- [ ] **Sun** (1h) — Checkpoint questions; commit
- [ ] ★ **Deliverable:** DAG with retries + 7-day backfill screenshots

Notes:


## Week 7 · dbt (Nov 16–22)

- [ ] **Mon** (2h) — Install dbt; start Fundamentals course
- [ ] **Tue** (2h) — Sources, staging, ref(), materializations
- [ ] **Wed** (1.5h) — 2 staging models + 1 mart, basic tests
- [ ] **Thu** (2h) — Incremental, snapshots, macros
- [ ] **Fri** (2h) — Rebuild Week 4 gold layer in dbt
- [ ] **Sat** (4h) — Snapshot, 10+ tests, docs, dbt in Airflow
- [ ] **Sun** (1h) — Fundamentals quiz; checkpoint
- [ ] ★ **Deliverable:** dbt project: 10+ tests, docs, snapshot

Notes:


## Week 8 · Quality, CI, wrap-up (Nov 23–29)

- [ ] **Mon** (2h) — Freshness/row-count checks; failure policy
- [ ] **Tue** (2h) — Secrets scan; PII masking
- [ ] **Wed** (1.5h) — Test coverage; pre-commit + ruff
- [ ] **Thu** (2h) — GitHub Actions: ruff, pytest, dbt build
- [ ] **Fri** (2h) — Update CV (fix TDR dates) and LinkedIn
- [ ] **Sat** (4h) — Project 1 README + demo video
- [ ] **Sun** (1h) — Send first 3–5 applications
- [ ] ★ **Deliverable:** Project 1 published, CV updated, first applications sent

Notes:


# Phase 3 · Cloud & capstone

## Week 9 · AWS storage + Athena (Nov 30–Dec 6)

- [ ] **Mon** (2h) — Budget alert, IAM, S3 layout
- [ ] **Tue** (2h) — Write partitioned Parquet to S3 (boto3)
- [ ] **Wed** (1.5h) — Least-privilege policy; test denials
- [ ] **Thu** (2h) — Glue Catalog tables + partitions
- [ ] **Fri** (2h) — Athena: CSV vs Parquet vs partitioned
- [ ] **Sat** (4h) — Results table; small-files test; clean up
- [ ] **Sun** (1h) — Checkpoint; check AWS bill
- [ ] ★ **Deliverable:** docs/athena-experiment.md

Notes:


## Week 10 · Redshift + Spark basics (Dec 7–13)

- [ ] **Mon** (2h) — MPP, dist/sort keys, COPY; Athena vs Redshift
- [ ] **Tue** (2h) — Optional Redshift test (or docs-only); delete after
- [ ] **Wed** (1.5h) — Spark concepts; local PySpark quickstart
- [ ] **Thu** (2h) — Transform in PySpark; spot the shuffle
- [ ] **Fri** (2h) — Same in Polars + DuckDB; time all
- [ ] **Sat** (4h) — Comparison write-up + decision table
- [ ] **Sun** (1h) — Checkpoint questions; commit
- [ ] ★ **Deliverable:** docs/engine-comparison.md

Notes:


## Week 11 · Capstone build (Dec 14–20)

- [ ] **Mon** (2h) — Sources, questions, architecture, contracts
- [ ] **Tue** (2h) — Scaffold repo; ingest source 1
- [ ] **Wed** (1.5h) — Ingest source 2 with validation
- [ ] **Thu** (2h) — Silver layer + tests
- [ ] **Fri** (2h) — Gold star schema + Type 2 dimension
- [ ] **Sat** (4h) — Orchestrate in Airflow; full run; alerts
- [ ] **Sun** (1h) — List what remains; commit
- [ ] ★ **Deliverable:** Capstone runs end to end

Notes:


## Week 12 · Polish + interview prep (Dec 21–27)

- [ ] **Mon** (2h) — Dashboard (Metabase/Streamlit)
- [ ] **Tue** (2h) — README, diagram, cost notes
- [ ] **Wed** (1.5h) — Walkthrough video + post draft
- [ ] **Thu** (2h) — 10 SQL drills; concept Qs 1–4 aloud
- [ ] **Fri** (2h) — Concept Qs 5–7; mock design; 3 stories
- [ ] **Sat** (4h) — Cleanup; update CV/LinkedIn; publish; apply
- [ ] **Sun** (1h) — Retrospective; plan next 4 weeks
- [ ] ★ **Deliverable:** Capstone published, applications sent

Notes:


# Job applications log

| Date | Company | Role | Link | Status | Follow-up | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |
