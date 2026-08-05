from pathlib import Path
import pandas as pd
import duckdb

# 1. Define PathBs using pathlib
DATA_DIR = Path("data")
RAW_STUDY_DIR = DATA_DIR / "raw" / "tcga_pancan" / "brca_tcga_pan_can_atlas_2018"
CLINICAL_FILE = RAW_STUDY_DIR / "data_clinical_patient.txt"
DB_PATH = DATA_DIR / "db" / "staging.duckdb"

# Ensure database directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# 2. Read Clinical Patient Table
print(f"Reading clinical data from {CLINICAL_FILE}...")
# comment='#' tells pandas to skip cBioPortal metadata lines
df_patient = pd.read_csv(CLINICAL_FILE, sep="\t", comment="#")

raw_count = len(df_patient)
print(f"[RAW PATIENTS]: {raw_count} (Expected: 1,084)")

# 3. Identify Filter Columns Case-Insensitively
sex_col = [c for c in df_patient.columns if "SEX" in c.upper()][0]
neo_col = [c for c in df_patient.columns if "NEOADJUVANT" in c.upper()][0]

print(f"Using columns: Sex -> '{sex_col}', Neoadjuvant -> '{neo_col}'")

# 4. Apply Filters
filtered_df = df_patient[
    (df_patient[sex_col].astype(str).str.upper() == "FEMALE") &
    (df_patient[neo_col].astype(str).str.upper() != "YES")
].copy()

filtered_count = len(filtered_df)
print(f"[FILTERED PATIENTS]: {filtered_count} (Expected Paper Target: ~859)")

# 5. Ingest into DuckDB
print(f"Connecting to DuckDB at {DB_PATH}...")
con = duckdb.connect(str(DB_PATH))

con.execute("CREATE OR REPLACE TABLE staged_tcga_clinical AS SELECT * FROM filtered_df")

# Query DuckDB directly to verify database state
db_count = con.execute("SELECT COUNT(*) FROM staged_tcga_clinical").fetchone()[0]
print(f"[DUCKDB VERIFICATION]: Staging table contains {db_count} rows.")

con.close()