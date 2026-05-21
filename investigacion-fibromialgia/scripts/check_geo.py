import os
import GEOparse

import pathlib
geo_dir = str(pathlib.Path(__file__).resolve().parent.parent / "datos" / "geo" / "PBMC_FM_96patients_93controls")
os.makedirs(geo_dir, exist_ok=True)

try:
    print("Fetching GSE221921...")
    gse = GEOparse.get_GEO(geo="GSE221921", destdir=geo_dir)
    print(f"Got {len(gse.gsms)} samples.")
    print("Supplementary files:")
    for file, url in gse.metadata.get("supplementary_file", []):
        print(file)
        
    print("\nMetadata values:")
    for k, v in gse.metadata.items():
        if k == "supplementary_file_1":
            print(f"Sup1: {v}")
        if k == "supplementary_file_2":
            print(f"Sup2: {v}")
            
except Exception as e:
    print("Error:", e)
