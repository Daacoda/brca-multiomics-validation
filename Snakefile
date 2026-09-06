# Snakefile - Stage 0 Pipeline Automation

TARBALL = "data/raw/brca_tcga_pan_can_atlas_2018.tar.gz"
RAW_DIR = "data/raw/tcga_pancan/brca_tcga_pan_can_atlas_2018"
DB_PATH = "data/db/staging.duckdb"

rule all:
    input:
        DB_PATH

# 1. Download raw tarball directly from cBioPortal source
rule download_raw_data:
    output:
        TARBALL
    shell:
        "uv run src/download_data.py"

# 2. Extract downloaded archive
rule extract_raw_data:
    input:
        TARBALL
    output:
        directory(RAW_DIR)
    shell:
        "uv run src/extract_downl.py"

# 3. Stage tables into DuckDB, build 859-patient view, and validate assertions
rule stage_and_validate_duckdb:
    input:
        raw_dir = RAW_DIR,
        s1      = "src/filt_to_duckdb.py",
        s2      = "src/stage_mrna.py",
        s3      = "src/stage_rppa.py",
        s4      = "src/create_analytical_view.py",
        s5      = "src/validate_staging.py"
    output:
        db = DB_PATH
    shell:
        """
        uv run src/filt_to_duckdb.py
        uv run src/stage_mrna.py
        uv run src/stage_rppa.py
        uv run src/create_analytical_view.py
        uv run src/validate_staging.py
        """