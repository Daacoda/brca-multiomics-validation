from pathlib import Path
import requests
from tqdm import tqdm

# 1. Define base directories as Path objects
DATA_DIR = Path("data") / "raw"
EXTRACT_DIR = DATA_DIR / "tcga_pancan"
TAR_PATH = DATA_DIR / "brca_tcga_pan_can_atlas_2018.tar.gz"

# 2. Create directories directly off the Path objects
DATA_DIR.mkdir(parents=True, exist_ok=True)
EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

# 3. Check if file exists using Path methods
if TAR_PATH.exists() and TAR_PATH.stat().st_size == 509019117:
    print(f"Archive already fully downloaded at {TAR_PATH}. Stopping here to save time!")
else:
    print(f"Ready to download to {TAR_PATH}")



URL = "https://datahub.assets.cbioportal.org/brca_tcga_pan_can_atlas_2018.tar.gz"

# 4. Open the HTTP connection in streaming mode
print(f"Connecting to cBioPortal...")
response = requests.get(URL, stream=True)

# 5 Ensure HTTP response is 200 OK
response.raise_for_status()

# 6 . Read content-length header (size in bytes)
total_size_bytes = int(response.headers.get('content-length', 0))
total_size_mb = total_size_bytes / (1024 * 1024)

print(f"Connection successful! Status code: {response.status_code}")
print(f"Dataset File Size: {total_size_mb:.2f} MB ({total_size_bytes:,} bytes)")



# Open the Path file in Write-Binary ('wb') mode
print(f"Downloading to {TAR_PATH}...")
with TAR_PATH.open('wb') as file, tqdm(
    desc="brca_tcga_pan_can_atlas_2018.tar.gz",
    total=total_size_bytes,
    unit='B',
    unit_scale=True,
    unit_divisor=1024,
) as bar:
    for chunk in response.iter_content(chunk_size=1024 * 1024):  # Read in 1 MB chunks
        if chunk:
            size = file.write(chunk)
            bar.update(size)

print(f"\n[SUCCESS] Download complete! Saved to {TAR_PATH}")