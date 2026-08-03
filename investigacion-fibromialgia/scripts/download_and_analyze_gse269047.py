#!/usr/bin/env python3
"""
Step 1: Download & Adversarial Replicability Analysis of GSE269047.
Fetches supplementary data matrix from GEO FTP and analyzes replication of Immune & Neural markers.
"""

import os
import gzip
import re
import urllib.request
import pathlib
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
import warnings
warnings.filterwarnings('ignore')

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / 'datos' / 'geo' / 'GSE269047'
OUTPUT_DIR = REPO_ROOT / 'analisis' / 'replicacion'
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPPL_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE269nnn/GSE269047/suppl/"
MATRIX_FILE = DATA_DIR / "GSE269047_series_matrix.txt.gz"


def list_suppl_files():
    """List supplementary files available on GEO FTP for GSE269047."""
    print(f"Checking supplementary files at {SUPPL_URL}...")
    try:
        req = urllib.request.Request(SUPPL_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            files = re.findall(r'href="([^"]+)"', html)
            suppl_files = [f for f in files if not f.startswith('?') and not f.startswith('/')]
            print(f"Found supplementary files: {suppl_files}")
            return suppl_files
    except Exception as e:
        print(f"Error listing suppl files: {e}")
        return []


def download_suppl_file(filename):
    """Download a specific supplementary file."""
    file_url = SUPPL_URL + filename
    local_path = DATA_DIR / filename
    if not local_path.exists():
        print(f"Downloading {filename} from {file_url}...")
        req = urllib.request.Request(file_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp, open(local_path, 'wb') as f:
            f.write(resp.read())
        print(f"Saved to {local_path}")
    else:
        print(f"File {local_path} already exists.")
    return local_path


def parse_sample_metadata():
    """Extract sample characteristics from series matrix header."""
    sample_ids = []
    sample_titles = []
    characteristics = []
    
    with gzip.open(MATRIX_FILE, 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith('!Sample_geo_accession'):
                sample_ids = [s.strip('"') for s in line.split('\t')[1:]]
            elif line.startswith('!Sample_title'):
                sample_titles = [s.strip('"') for s in line.split('\t')[1:]]
            elif line.startswith('!Sample_characteristics_ch1'):
                characteristics.append([s.strip('"') for s in line.split('\t')[1:]])
                
    meta_df = pd.DataFrame({'sample_id': sample_ids, 'title': sample_titles})
    
    # Parse characteristics (e.g. disease state: FM, ME/CFS, Control)
    is_fm = []
    disease_list = []
    for idx in range(len(sample_ids)):
        char_str = " ".join([c[idx] for c in characteristics if idx < len(c)])
        title_str = sample_titles[idx] if idx < len(sample_titles) else ""
        full = (title_str + " " + char_str).lower()
        
        if 'fibromyalgia' in full or 'fm' in full:
            dis = 'FM'
        elif 'cfs' in full or 'me/cfs' in full or 'encephalomyelitis' in full:
            dis = 'ME/CFS'
        elif 'control' in full or 'healthy' in full:
            dis = 'Control'
        else:
            dis = 'Other'
            
        disease_list.append(dis)
        
    meta_df['disease'] = disease_list
    print("\nSample Phenotype Distribution:")
    print(meta_df['disease'].value_counts())
    return meta_df


def main():
    print("=" * 70)
    print("REPLICABILITY AUDIT: GSE269047 (SUPPLEMENTARY DATA MINING)")
    print("=" * 70)
    
    meta_df = parse_sample_metadata()
    meta_df.to_csv(OUTPUT_DIR / 'gse269047_metadata.csv', index=False)
    
    suppl_files = list_suppl_files()
    for f in suppl_files:
        if any(ext in f.lower() for ext in ['.txt', '.csv', '.tsv', '.xlsx', '.gz']):
            download_suppl_file(f)


if __name__ == '__main__':
    main()
