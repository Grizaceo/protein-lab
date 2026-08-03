#!/usr/bin/env python3
"""
Step 1 Analysis: High-throughput parsing and replicability testing on GSE269047.
Parses the high-density microarray probes (e.g., DRD2-opti_at, GATA2-bgrd_at) and tests differential expression.
"""

import os
import gzip
import pathlib
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
import warnings
warnings.filterwarnings('ignore')

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / 'datos' / 'geo' / 'GSE269047'
OUTPUT_DIR = REPO_ROOT / 'analisis' / 'replicacion'
os.makedirs(OUTPUT_DIR, exist_ok=True)

EXPRS_FILE = DATA_DIR / "GSE269047_exprs_data.txt.gz"
META_FILE = OUTPUT_DIR / "gse269047_metadata.csv"

TARGET_GENES = ['CPA3', 'GATA2', 'MS4A2', 'FCER1A', 'HDC', 'DRD2', 'MDGA2', 'COMT', 'MAOA', 'TPSAB1', 'KIT']


def analyze():
    print(f"Parsing GSE269047 matrix from {EXPRS_FILE}...")
    meta_df = pd.read_csv(META_FILE)
    
    # Disease mapping
    fm_samples = meta_df[meta_df['disease'].isin(['FM', 'ME/CFS'])]['sample_id'].tolist()
    hc_samples = meta_df[meta_df['disease'] == 'Control']['sample_id'].tolist()
    
    print(f"Sample Group Counts: FM/ME-CFS = {len(fm_samples)}, Control = {len(hc_samples)}")
    
    extracted_data = []
    
    with gzip.open(EXPRS_FILE, 'rt', encoding='utf-8', errors='ignore') as f:
        header_line = f.readline().strip()
        # Header line starts with ID_REF or probe names
        # Parse samples from meta_df order
        sample_list = meta_df['sample_id'].tolist()
        
        row_count = 0
        for line in f:
            row_count += 1
            line_str = line.strip()
            if not line_str:
                continue
                
            # Line format is: "PROBE_NAME" val1 val2 val3 ...
            # Split by whitespace or quote
            parts = line_str.split()
            probe_id = parts[0].strip('"')
            probe_upper = probe_id.upper()
            
            for tg in TARGET_GENES:
                if tg in probe_upper:
                    vals = []
                    for v in parts[1:]:
                        try:
                            vals.append(float(v))
                        except ValueError:
                            pass
                    if len(vals) == len(meta_df):
                        extracted_data.append({
                            'probe_id': probe_id,
                            'target_gene': tg,
                            'vals': vals
                        })
                        
    print(f"Processed {row_count} total probes. Found {len(extracted_data)} target gene probes.")
    
    results = []
    for item in extracted_data:
        probe_id = item['probe_id']
        gene = item['target_gene']
        vals = item['vals']
        
        # Map values to sample indices
        val_df = pd.DataFrame({'sample_id': meta_df['sample_id'], 'disease': meta_df['disease'], 'val': vals})
        
        fm_vals = val_df[val_df['disease'].isin(['FM', 'ME/CFS'])]['val'].values
        hc_vals = val_df[val_df['disease'] == 'Control']['val'].values
        
        if len(fm_vals) > 0 and len(hc_vals) > 0:
            fm_m = np.mean(fm_vals)
            hc_m = np.mean(hc_vals)
            log2fc = fm_m - hc_m
            stat, pval = mannwhitneyu(fm_vals, hc_vals)
            
            results.append({
                'probe_id': probe_id,
                'gene': gene,
                'fm_mean': fm_m,
                'hc_mean': hc_m,
                'log2FC': log2fc,
                'p_value': pval
            })
            
    if results:
        res_df = pd.DataFrame(results).sort_values('p_value')
        print("\n--- Replication Probe Analysis in Independent Cohort GSE269047 ---")
        print(res_df[['probe_id', 'gene', 'fm_mean', 'hc_mean', 'log2FC', 'p_value']].to_string(index=False))
        res_df.to_csv(OUTPUT_DIR / 'gse269047_replication_degs.csv', index=False)
        print(f"\nSaved replication results to {OUTPUT_DIR / 'gse269047_replication_degs.csv'}")
    else:
        print("No probe matching required complete sample length.")


if __name__ == '__main__':
    analyze()
