#!/usr/bin/env python3
"""
Adversarial Audit & Methodological Stress-Test for Tangente 1 & Subtype Orthogonality.
Evaluates probe-level signal-to-noise ratio (SNR), background noise floor for DRD2/MDGA2,
unimodality/multimodality tests, and potential technical artifacts in GSE67311.
"""

import os
import gzip
import pathlib
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr, shapiro
import warnings
warnings.filterwarnings('ignore')

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / 'analisis'
DATA_DIR = REPO_ROOT / 'datos'


def load_gse67311_probes():
    """Load GSE67311 with full probe-level resolution."""
    matrix_file = DATA_DIR / 'geo' / 'GSE67311' / 'GSE67311_series_matrix.txt.gz'
    degs_file = DATA_DIR / 'GSE67311_DEGs_all_named.csv'
    
    sample_ids, sample_types, expr_data = [], [], {}
    with gzip.open(matrix_file, 'rt') as f:
        in_table = False
        for line in f:
            line = line.strip()
            if line.startswith('!Sample_geo_accession'):
                sample_ids = [s.strip('"') for s in line.split('\t')[1:]]
            elif line.startswith('!Sample_source_name_ch1'):
                sample_types = [s.strip('"') for s in line.split('\t')[1:]]
            elif line.startswith('!series_matrix_table_begin'):
                in_table = True
                continue
            elif line.startswith('!series_matrix_table_end'):
                break
            elif in_table:
                parts = line.split('\t')
                if parts[0] == '"ID_REF"':
                    continue
                probe_id = parts[0].strip('"')
                values = [float(v) for v in parts[1:]]
                expr_data[probe_id] = values
                
    expr_df = pd.DataFrame(expr_data, index=sample_ids).T
    degs = pd.read_csv(degs_file)
    probe_to_gene = dict(zip(degs['gene_id'].astype(str), degs['gene_symbol']))
    
    is_fm = ['Fibromyalgia' in s for s in sample_types]
    sample_info = pd.DataFrame({'sample_id': sample_ids, 'is_fm': is_fm})
    
    return expr_df, probe_to_gene, sample_info


def audit_signal_to_noise(expr_df, probe_to_gene):
    """Audit Test 1: Probe expression vs Overall Array Percentiles (Background Floor)."""
    print("\n" + "="*70)
    print("AUDIT TEST 1: SIGNAL-TO-NOISE RATIO & BACKGROUND NOISE FLOOR")
    print("="*70)
    
    # Calculate overall array expression percentiles
    all_means = expr_df.mean(axis=1).values
    p5 = np.percentile(all_means, 5)
    p10 = np.percentile(all_means, 10)
    p25 = np.percentile(all_means, 25)
    p50 = np.percentile(all_means, 50)
    p75 = np.percentile(all_means, 75)
    p90 = np.percentile(all_means, 90)
    
    print(f"Overall Array Quantiles (Affymetrix log2 expression):")
    print(f"  5th percentile  (Noise Floor): {p5:.4f}")
    print(f"  10th percentile (Low limit)  : {p10:.4f}")
    print(f"  25th percentile (Q1)         : {p25:.4f}")
    print(f"  50th percentile (Median)     : {p50:.4f}")
    print(f"  75th percentile (Q3)         : {p75:.4f}")
    print(f"  90th percentile (High)       : {p90:.4f}")
    
    target_genes = ['DRD2', 'MDGA2', 'CPA3', 'GATA2', 'MS4A2', 'FCER1A', 'HDC', 'COMT', 'MAOA', 'RGS17']
    
    audit_rows = []
    print(f"\nTarget Gene Probe Inspection:")
    print(f"{'Probe ID':<15} {'Gene':<10} {'Mean Expr':>10} {'Std Dev':>10} {'Percentile':>12} {'Status / Risk'}")
    print("-" * 75)
    
    for probe_id, gene in probe_to_gene.items():
        if gene in target_genes and probe_id in expr_df.index:
            vals = expr_df.loc[probe_id].values
            mean_val = np.mean(vals)
            std_val = np.std(vals)
            
            # Find percentile rank of this probe mean in the array
            pct = (all_means < mean_val).mean() * 100
            
            if pct < 15:
                status = "CRITICAL: NOISE FLOOR (Non-detectable)"
            elif pct < 35:
                status = "WARNING: Low Signal"
            else:
                status = "PASS: Robust Signal"
                
            print(f"{probe_id:<15} {gene:<10} {mean_val:>10.4f} {std_val:>10.4f} {pct:>11.1f}% {status}")
            audit_rows.append({
                'probe_id': probe_id,
                'gene': gene,
                'mean_expr': mean_val,
                'std_dev': std_val,
                'percentile_rank': pct,
                'status': status
            })
            
    return pd.DataFrame(audit_rows)


def audit_clustering_fragility(expr_df, probe_to_gene, sample_info):
    """Audit Test 2: Clustering Fragility & Unimodality Evaluation."""
    print("\n" + "="*70)
    print("AUDIT TEST 2: CLUSTERING STABILITY & HETEROGENEITY ASSESSMENT")
    print("="*70)
    
    fm_mask = sample_info['is_fm'].values
    fm_samples = sample_info[fm_mask]['sample_id'].values
    
    # Map best probe per target gene
    gene_to_probe = {}
    for probe_id, gene in probe_to_gene.items():
        if gene in ['CPA3', 'GATA2', 'MS4A2', 'FCER1A', 'HDC', 'DRD2', 'MDGA2']:
            if gene not in gene_to_probe:
                gene_to_probe[gene] = probe_id
            else:
                # Keep probe with higher mean
                if expr_df.loc[probe_id].mean() > expr_df.loc[gene_to_probe[gene]].mean():
                    gene_to_probe[gene] = probe_id
                    
    # Extract gene expression for FM samples
    gene_df = pd.DataFrame()
    for g, p in gene_to_probe.items():
        gene_df[g] = expr_df.loc[p, fm_samples]
        
    immune_genes = ['CPA3', 'GATA2', 'MS4A2', 'FCER1A', 'HDC']
    immune_score = gene_df[immune_genes].apply(lambda x: (x - x.mean()) / x.std()).mean(axis=1)
    
    stat, pval = shapiro(immune_score)
    skewness = float(pd.Series(immune_score).skew())
    kurt = float(pd.Series(immune_score).kurt())
    
    print(f"Immune Score Distribution Metrics (N={len(fm_samples)} FM Patients):")
    print(f"  Shapiro-Wilk W Statistic: {stat:.4f} (p-value = {pval:.4f})")
    print(f"  Skewness: {skewness:.4f}")
    print(f"  Kurtosis: {kurt:.4f}")
    
    if pval < 0.05:
        print("  -> EVALUATION: Significant departure from normality (Heterogeneity confirmed).")
    else:
        print("  -> EVALUATION: Distribution does NOT significantly depart from normality.")
        
    # Check DRD2 signal specifically
    drd2_mean = gene_df['DRD2'].mean() if 'DRD2' in gene_df else 0
    print(f"\nDRD2 Signal Evaluation in GSE67311:")
    print(f"  DRD2 Mean Log2 Intensity: {drd2_mean:.4f}")
    
    return immune_score


def main():
    print("="*70)
    print("ADVERSARIAL AUDIT & METHODOLOGICAL STRESS-TEST — FIBROMYALGIA LAB")
    print("="*70)
    
    expr_df, probe_to_gene, sample_info = load_gse67311_probes()
    snr_audit = audit_signal_to_noise(expr_df, probe_to_gene)
    immune_score = audit_clustering_fragility(expr_df, probe_to_gene, sample_info)
    
    os.makedirs(OUTPUT_DIR / 'tangente1', exist_ok=True)
    snr_audit.to_csv(OUTPUT_DIR / 'tangente1' / 'adversarial_snr_audit.csv', index=False)
    print(f"\nSaved adversarial SNR audit table to {OUTPUT_DIR / 'tangente1' / 'adversarial_snr_audit.csv'}")


if __name__ == '__main__':
    main()
