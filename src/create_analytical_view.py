from pathlib import Path
import duckdb

DB_PATH = Path("data/db/staging.duckdb")
SQL_PATH = Path("src/sql/v_analytical_cohort.sql")

print(f"Connecting to DuckDB at {DB_PATH}...")
con = duckdb.connect(str(DB_PATH))

# Read and execute SQL view definition
print(f"Executing SQL query from {SQL_PATH}...")
with open(SQL_PATH, "r") as f:
    sql_query = f.read()

con.execute(sql_query)

# Audit the View
cohort_count = con.execute("SELECT COUNT(*) FROM v_analytical_cohort").fetchone()[0]
print("\n--- Analytical View Verification ---")
print(f"[SUCCESS] v_analytical_cohort materialized with {cohort_count} multi-omics patients.")

con.close()