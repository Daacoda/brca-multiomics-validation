from pathlib import Path
import pandas as pd
import duckdb

DATA_DIR = Path("data")
RPPA_FILE = DATA_DIR / "raw" / "tcga_pancan" / "brca_tcga_pan_can_atlas_2018" / "data_rppa.txt"
DB_PATH = DATA_DIR / "db" / "staging.duckdb"

print(f"Reading RPPA protein matrix from {RPPA_FILE}...")
df_rppa = pd.read_csv(RPPA_FILE, sep="\t")

# Positional rename: force the first column to 'protein_id' regardless of '.' vs '_'
first_col = df_rppa.columns[0]
print(f"Renaming first column '{first_col}' -> 'protein_id'")
df_rppa = df_rppa.rename(columns={first_col: "protein_id"})

# Clean secondary gene symbol column if present
gene_symbol_cols = [c for c in df_rppa.columns if "HUGO" in c.upper() or "GENE" in c.upper()]
if gene_symbol_cols:
    df_rppa = df_rppa.rename(columns={gene_symbol_cols[0]: "gene_symbol"})

print(f"Matrix Loaded: {df_rppa.shape[0]:,} proteins across {df_rppa.shape[1] - 1:,} sample columns.")

# Re-stage into DuckDB
con = duckdb.connect(str(DB_PATH))
con.execute("CREATE OR REPLACE TABLE staged_tcga_rppa AS SELECT * FROM df_rppa")
con.close()

print("[SUCCESS] Re-staged staged_tcga_rppa with standardized 'protein_id' column!")