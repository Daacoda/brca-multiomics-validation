from pathlib import Path
import tarfile

# 1. Define the  paths so THIS script knows where to look
DATA_DIR = Path("data") / "raw"
EXTRACT_DIR = DATA_DIR / "tcga_pancan"
TAR_PATH = DATA_DIR / "brca_tcga_pan_can_atlas_2018.tar.gz"

STUDY_DIR = EXTRACT_DIR / "brca_tcga_pan_can_atlas_2018"

print(f"Extracting archive to {EXTRACT_DIR}...")
with tarfile.open(TAR_PATH, "r:gz") as tar:
    tar.extractall(path=EXTRACT_DIR, filter='data')

print("[SUCCESS] Extraction complete!")

# Step-by-step verification
print("\n--- Extraction Audit ---")
print(f"Extracted folder exists: {STUDY_DIR.exists()}")

# List the key files we will need for clinical & expression data
files_in_dir = [f.name for f in STUDY_DIR.iterdir()]
print(f"Total files unpacked: {len(files_in_dir)}")

# Check for clinical and mRNA files specifically
clinical_file = STUDY_DIR / "data_clinical_patient.txt"
mrna_file = STUDY_DIR / "data_mrna_seq_v2_rsem.txt"

print(f"Clinical file found: {clinical_file.exists()}")
print(f"mRNA file found: {mrna_file.exists()}")
