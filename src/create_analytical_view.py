from pathlib import Path
import duckdb

DB_PATH = Path("data/db/staging.duckdb")

print(f"Connecting to DuckDB at {DB_PATH}...")
con = duckdb.connect(str(DB_PATH))

# Create SQL View that extracts 12-char PATIENT_IDs and finds the 3-way intersect
con.execute("""
CREATE OR REPLACE VIEW v_analytical_cohort AS
WITH clinical_pts AS (
    SELECT PATIENT_ID, AGE, OS_MONTHS, OS_STATUS
    FROM staged_tcga_clinical
),
-- Extract 12-character Patient IDs from mRNA sample columns
mrna_samples AS (
    SELECT column_name AS mrna_barcode,
           SUBSTRING(column_name, 1, 12) AS PATIENT_ID
    FROM (DESCRIBE staged_tcga_mrna)
    WHERE column_name != 'gene_symbol'
),
-- Extract 12-character Patient IDs from RPPA sample columns
rppa_samples AS (
    SELECT column_name AS rppa_barcode,
           SUBSTRING(column_name, 1, 12) AS PATIENT_ID
    FROM (DESCRIBE staged_tcga_rppa)
    WHERE column_name NOT IN ('protein_id', 'gene_symbol')
)
SELECT 
    c.PATIENT_ID,
    c.AGE,
    c.OS_MONTHS,
    c.OS_STATUS,
    m.mrna_barcode,
    r.rppa_barcode
FROM clinical_pts c
INNER JOIN mrna_samples m ON c.PATIENT_ID = m.PATIENT_ID
INNER JOIN rppa_samples r ON c.PATIENT_ID = r.PATIENT_ID;
""")

# Audit the View
cohort_count = con.execute("SELECT COUNT(*) FROM v_analytical_cohort").fetchone()[0]
print("\n--- Analytical View Verification ---")
print(f"[SUCCESS] v_analytical_cohort materialized with {cohort_count} multi-omics patients.")

con.close()