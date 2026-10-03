"""Print a paste-ready profile of a Parquet or CSV file for a data dictionary.

Run it from the de-project-1 folder:
    python ../de-notes/week-00/profile_dataset.py data/<taxi-file>.parquet
    python ../de-notes/week-00/profile_dataset.py data/<worldbank-file>.csv --skip 4

--skip N: for CSV files only, the number of lines before the real header
(World Bank files have 4 description lines first).
"""
import argparse

import duckdb


def source(path: str, skip: int) -> str:
    if path.lower().endswith(".parquet"):
        return f"read_parquet('{path}')"
    return f"read_csv('{path}', skip={skip}, header=true, sample_size=-1)"


def clip(value, width=40) -> str:
    text = "" if value is None else str(value)
    return text if len(text) <= width else text[: width - 1] + "…"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("path")
    parser.add_argument("--skip", type=int, default=0, help="CSV only: lines to skip before the header")
    parser.add_argument("--rows", type=int, default=3, help="how many sample rows to show")
    args = parser.parse_args()

    con = duckdb.connect()
    src = source(args.path, args.skip)

    n_rows = con.sql(f"SELECT count(*) FROM {src}").fetchone()[0]
    print(f"# Profile of {args.path}\n")
    print(f"- **Rows:** {n_rows:,}")

    summary = con.sql(
        "SELECT column_name, column_type, null_percentage, approx_unique, min, max "
        f"FROM (SUMMARIZE SELECT * FROM {src})"
    ).fetchall()
    print(f"- **Columns:** {len(summary)}\n")

    print("| Column | Type | Meaning | Nulls? | Notes |")
    print("|---|---|---|---|---|")
    for name, ctype, null_pct, uniq, lo, hi in summary:
        notes = f"~{uniq:,} distinct; min {clip(lo, 25)}; max {clip(hi, 25)}"
        print(f"| {name} | {ctype} | _fill in_ | {float(null_pct):.1f}% null | {notes} |")

    print(f"\n## First {args.rows} rows\n")
    cur = con.sql(f"SELECT * FROM {src} LIMIT {args.rows}")
    cols = cur.columns
    for i, row in enumerate(cur.fetchall(), 1):
        print(f"Row {i}:")
        for col, val in zip(cols, row):
            print(f"  {col}: {clip(val)}")
        print()


if __name__ == "__main__":
    main()