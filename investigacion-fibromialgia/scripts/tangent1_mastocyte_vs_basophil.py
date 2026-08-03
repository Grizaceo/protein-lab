#!/usr/bin/env python3
"""
Tangente 1 - Phase 1: Fine-grained transcriptomic deconvolution & signature analysis.
Discriminates between circulating basophil depletion/exhaustion vs mast cell tissue migration/degranulation.
Analyzes GSE67311 (Whole Blood, microarray) and GSE221921 (PBMCs, RNA-seq).
"""

import os
import gzip
import pathlib
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu, spearmanr
def benjamini_hochberg(p_values):
    """Compute Benjamini-Hochberg FDR q-values."""
    p_values = np.asanyarray(p_values)
    by_descend = p_values.argsort()[::-1]
    by_orig = by_descend.argsort()
    steps = len(p_values) - np.arange(len(p_values))
    q_values = p_values[by_descend] * len(p_values) / steps
    q_values = np.minimum.accumulate(q_values)
    return np.minimum(q_values[by_orig], 1.0)
import warnings
warnings.filterwarnings('ignore')

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / 'analisis'
DATA_DIR = REPO_ROOT / 'datos'

MAST_CELL_SPECIFIC = ['CPA3', 'TPSAB1', 'TPSB2', 'KIT']
BASOPHIL_SPECIFIC = ['GATA2', 'CLC', 'PRG2']
SHARED_MAST_BASO = ['MS4A2', 'FCER1A', 'HDC']

ALL_TARGET_GENES = MAST_CELL_SPECIFIC + BASOPHIL_SPECIFIC + SHARED_MAST_BASO


def load_gse67311():
    """Load whole blood dataset GSE67311."""
    matrix_file = DATA_DIR / 'geo' / 'GSE67311' / 'GSE67311_series_matrix.txt.gz'
    degs_file = DATA_DIR / 'GSE67311_DEGs_all_named.csv'
    
    if not matrix_file.exists() or not degs_file.exists():
        raise FileNotFoundError(f"GSE67311 files missing at {matrix_file}")
        
    sample_ids = []
    sample_types = []
    expr_data = {}
    
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
    
    expr_df['gene_symbol'] = expr_df.index.map(lambda x: probe_to_gene.get(str(x), ''))
    expr_df = expr_df[expr_df['gene_symbol'] != '']
    
    expr_df['_mean'] = expr_df[sample_ids].mean(axis=1)
    expr_df = expr_df.sort_values('_mean', ascending=False)
    expr_df = expr_df[~expr_df['gene_symbol'].duplicated(keep='first')]
    expr_df = expr_df.drop('_mean', axis=1)
    expr_df = expr_df.set_index('gene_symbol')
    
    is_fm = ['Fibromyalgia' in s for s in sample_types]
    sample_info = pd.DataFrame({'sample_id': sample_ids, 'is_fm': is_fm})
    
    return expr_df, sample_info


def analyze_gene_panel(expr_df, sample_info, dataset_name):
    """Perform differential expression analysis on mastocyte and basophil gene panels."""
    fm_mask = sample_info['is_fm'].values
    hc_mask = ~fm_mask
    
    results = []
    available_genes = [g for g in ALL_TARGET_GENES if g in expr_df.index]
    
    for gene in available_genes:
        fm_vals = expr_df.loc[gene, fm_mask].values
        hc_vals = expr_df.loc[gene, hc_mask].values
        
        fm_mean = np.mean(fm_vals)
        hc_mean = np.mean(hc_vals)
        
        if expr_df.values.max() < 25:
            log2fc = fm_mean - hc_mean
        else:
            log2fc = np.log2(fm_mean + 1) - np.log2(hc_mean + 1)
            
        stat, pval = mannwhitneyu(fm_vals, hc_vals)
        
        category = "Mast_Cell_Specific" if gene in MAST_CELL_SPECIFIC else \
                   "Basophil_Specific" if gene in BASOPHIL_SPECIFIC else "Shared_Mast_Baso"
                   
        results.append({
            'dataset': dataset_name,
            'gene': gene,
            'category': category,
            'fm_mean': fm_mean,
            'hc_mean': hc_mean,
            'log2FC': log2fc,
            'p_value': pval,
        })
        
    res_df = pd.DataFrame(results)
    if not res_df.empty:
        qvals = benjamini_hochberg(res_df['p_value'].values)
        res_df['q_value'] = qvals
        res_df['significant'] = res_df['q_value'] < 0.05
        
    return res_df


def analyze_signatures_and_ratios(expr_df, sample_info, dataset_name):
    """Compute score signatures and cell-type specific ratios."""
    fm_mask = sample_info['is_fm'].values
    hc_mask = ~fm_mask
    
    mast_genes = [g for g in MAST_CELL_SPECIFIC if g in expr_df.index]
    baso_genes = [g for g in BASOPHIL_SPECIFIC if g in expr_df.index]
    shared_genes = [g for g in SHARED_MAST_BASO if g in expr_df.index]
    
    scores = {}
    if mast_genes:
        scores['Mast_Cell_Signature'] = expr_df.loc[mast_genes].mean(axis=0)
    if baso_genes:
        scores['Basophil_Signature'] = expr_df.loc[baso_genes].mean(axis=0)
    if shared_genes:
        scores['Shared_Mast_Baso_Signature'] = expr_df.loc[shared_genes].mean(axis=0)
        
    sig_df = pd.DataFrame(scores)
    
    sig_results = []
    for sig_name in sig_df.columns:
        fm_vals = sig_df.loc[fm_mask, sig_name].values
        hc_vals = sig_df.loc[hc_mask, sig_name].values
        
        diff = np.mean(fm_vals) - np.mean(hc_vals)
        stat, pval = mannwhitneyu(fm_vals, hc_vals)
        
        sig_results.append({
            'signature': sig_name,
            'fm_mean': np.mean(fm_vals),
            'hc_mean': np.mean(hc_vals),
            'diff': diff,
            'p_value': pval
        })
        
    res_sig_df = pd.DataFrame(sig_results)
    if not res_sig_df.empty:
        qvals = benjamini_hochberg(res_sig_df['p_value'].values)
        res_sig_df['q_value'] = qvals
        
    ratios = {}
    if 'CPA3' in expr_df.index and 'GATA2' in expr_df.index:
        ratios['CPA3_minus_GATA2'] = expr_df.loc['CPA3'] - expr_df.loc['GATA2']
    if 'CPA3' in expr_df.index and 'MS4A2' in expr_df.index:
        ratios['CPA3_minus_MS4A2'] = expr_df.loc['CPA3'] - expr_df.loc['MS4A2']
    if 'KIT' in expr_df.index and 'GATA2' in expr_df.index:
        ratios['KIT_minus_GATA2'] = expr_df.loc['KIT'] - expr_df.loc['GATA2']
        
    ratio_df = pd.DataFrame(ratios)
    ratio_results = []
    for r_name in ratio_df.columns:
        fm_vals = ratio_df.loc[fm_mask, r_name].values
        hc_vals = ratio_df.loc[hc_mask, r_name].values
        diff = np.mean(fm_vals) - np.mean(hc_vals)
        stat, pval = mannwhitneyu(fm_vals, hc_vals)
        ratio_results.append({
            'ratio': r_name,
            'fm_mean': np.mean(fm_vals),
            'hc_mean': np.mean(hc_vals),
            'diff': diff,
            'p_value': pval
        })
        
    res_ratio_df = pd.DataFrame(ratio_results)
    return res_sig_df, res_ratio_df


def main():
    print("=" * 70)
    print("TANGENTE 1 - TRANSCRIPTOMIC DECONVOLUTION & CELL TYPE DISCRIMINATION")
    print("=" * 70)
    
    expr_67311, info_67311 = load_gse67311()
    print(f"\nLoaded GSE67311: {expr_67311.shape[0]} genes x {expr_67311.shape[1]} samples")
    print(f"FM: {info_67311['is_fm'].sum()}, HC: {(~info_67311['is_fm']).sum()}")
    
    gene_degs = analyze_gene_panel(expr_67311, info_67311, "GSE67311_WholeBlood")
    print("\n--- Individual Marker DEGs (GSE67311 Whole Blood) ---")
    print(gene_degs[['gene', 'category', 'fm_mean', 'hc_mean', 'log2FC', 'p_value', 'q_value', 'significant']].to_string(index=False))
    
    sig_res, ratio_res = analyze_signatures_and_ratios(expr_67311, info_67311, "GSE67311_WholeBlood")
    print("\n--- Cell-Type Signatures ---")
    print(sig_res.to_string(index=False))
    
    print("\n--- Marker Expression Ratios ---")
    print(ratio_res.to_string(index=False))
    
    os.makedirs(OUTPUT_DIR / 'tangente1', exist_ok=True)
    gene_degs.to_csv(OUTPUT_DIR / 'tangente1' / 'gse67311_mast_vs_baso_genes.csv', index=False)
    sig_res.to_csv(OUTPUT_DIR / 'tangente1' / 'gse67311_signatures.csv', index=False)
    ratio_res.to_csv(OUTPUT_DIR / 'tangente1' / 'gse67311_ratios.csv', index=False)
    
    print(f"\nSaved CSV results to {OUTPUT_DIR / 'tangente1'}/")


if __name__ == '__main__':
    main()
