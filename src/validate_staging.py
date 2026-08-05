from pathlib import Path
import duckdb

DB_PATH = Path("data/db/staging.duckdb")

assert DB_PATH.exists(), f"Database missing at {DB_PATH}"

con = duckdb.connect(str(DB_PATH))

print("--- STAGING DATABASE VERIFICATION SUITE ---\n")

# 1. Verify Clinical Table
clinical_count = con.execute("SELECT COUNT(*) FROM staged_tcga_clinical").fetchone()[0]
clinical_cols = [col[0] for col in con.execute("DESCRIBE staged_tcga_clinical").fetchall()]

assert clinical_count == 1066, f"Expected 1066 clinical rows, got {clinical_count}"
assert "PATIENT_ID" in clinical_cols, "PATIENT_ID column missing in staged_tcga_clinical"
print(f"[PASSED] Clinical Table: {clinical_count:,} rows, {len(clinical_cols)} columns.")

# 2. Verify mRNA Table
mrna_count = con.execute("SELECT COUNT(*) FROM staged_tcga_mrna").fetchone()[0]
mrna_cols = [col[0] for col in con.execute("DESCRIBE staged_tcga_mrna").fetchall()]

assert mrna_count == 20518, f"Expected 20518 mRNA rows, got {mrna_count}"
assert "gene_symbol" in mrna_cols, "gene_symbol column missing in staged_tcga_mrna"
# 1082 samples + 1 gene_symbol column = 1083 total columns
assert len(mrna_cols) == 1083, f"Expected 1083 mRNA columns, got {len(mrna_cols)}"
print(f"[PASSED] mRNA Table: {mrna_count:,} genes across {len(mrna_cols)-1:,} sample columns.")

# 3. Verify RPPA Table
rppa_count = con.execute("SELECT COUNT(*) FROM staged_tcga_rppa").fetchone()[0]
rppa_cols = [col[0] for col in con.execute("DESCRIBE staged_tcga_rppa").fetchall()]

assert rppa_count == 198, f"Expected 198 RPPA rows, got {rppa_count}"
assert "protein_id" in rppa_cols, "protein_id column missing in staged_tcga_rppa"
print(f"[PASSED] RPPA Table: {rppa_count:,} proteins across {len(rppa_cols)-2:,} sample columns.")

# 4. Check Null Integrity on Primary Keys
null_pts = con.execute("SELECT COUNT(*) FROM staged_tcga_clinical WHERE PATIENT_ID IS NULL").fetchone()[0]
assert null_pts == 0, f"Found {null_pts} NULL PATIENT_IDs in clinical table"

null_genes = con.execute("SELECT COUNT(*) FROM staged_tcga_mrna WHERE gene_symbol IS NULL").fetchone()[0]
assert null_genes == 0, f"Found {null_genes} NULL gene_symbols in mRNA table"

print(f"[PASSED] Primary key null checks: 0 NULL keys found across tables.")

con.close()
print("\n[ALL ASSERTS PASSED] Database state is verified.")