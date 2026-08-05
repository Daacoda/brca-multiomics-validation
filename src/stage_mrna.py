from pathlib import Path
import pandas as pd
import duckdb

# 1. Define Paths
DATA_DIR = Path("data")
MRNA_FILE = DATA_DIR / "raw" / "tcga_pancan" / "brca_tcga_pan_can_atlas_2018" / "data_mrna_seq_v2_rsem.txt"
DB_PATH = DATA_DIR / "db" / "staging.duckdb"

print(f"Reading mRNA matrix from {MRNA_FILE}...")

# 2. Read mRNA data with pandas
df_mrna = pd.read_csv(MRNA_FILE, sep="\t")

if "Entrez_Gene_Id" in df_mrna.columns:
    df_mrna = df_mrna.drop(columns=["Entrez_Gene_Id"])

# Clean gene column name
df_mrna = df_mrna.rename(columns={"Hugo_Symbol": "gene_symbol"})

# Drop rows with missing gene symbols
df_mrna = df_mrna.dropna(subset=["gene_symbol"])

print(f"Matrix Loaded: {df_mrna.shape[0]:,} genes across {df_mrna.shape[1] - 1:,} samples.")

# 3. Stage into DuckDB
print(f"Writing staged_tcga_mrna table to {DB_PATH}...")
con = duckdb.connect(str(DB_PATH))

con.execute("CREATE OR REPLACE TABLE staged_tcga_mrna AS SELECT * FROM df_mrna")

# 4. Verify table state in DuckDB
row_count = con.execute("SELECT COUNT(*) FROM staged_tcga_mrna").fetchone()[0]
cols = con.execute("DESCRIBE staged_tcga_mrna").df()

print("\n--- DuckDB mRNA Staging Audit ---")
print(f"Total Gene Rows in Database: {row_count:,}")
print(f"Total Columns (Gene Symbol + Samples): {len(cols):,}")

con.close()
print("[SUCCESS] mRNA Expression data staged successfully in DuckDB!")