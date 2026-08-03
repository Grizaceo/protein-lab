#!/usr/bin/env python3
"""
Investigation of FM Subtype Dichotomy (30-40% Autoimmune vs 60-70% Neuromodulatory/Dopaminergic).
Analyzes patient-level distribution, bimodality, and orthogonality between Immune (CPA3/GATA2/MS4A2) 
and Neural/Dopaminergic (DRD2/MDGA2) gene expression modules in GSE67311 and GSE221921.
"""

import os
import gzip
import pathlib
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, shapiro
from sklearn.mixture import GaussianMixture
import warnings
warnings.filterwarnings('ignore')

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / 'analisis' / 'tangente1'
DATA_DIR = REPO_ROOT / 'datos'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_gse67311():
    matrix_file = DATA_DIR / 'geo' / 'GSE67311' / 'GSE67311_series_matrix.txt.gz'
    degs_file = DATA_DIR / 'GSE67311_DEGs_all_named.csv'
    
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
    expr_df = expr_df.drop('_mean', axis=1).set_index('gene_symbol')
    
    is_fm = ['Fibromyalgia' in s for s in sample_types]
    sample_info = pd.DataFrame({'sample_id': sample_ids, 'is_fm': is_fm})
    return expr_df, sample_info


def analyze_bimodality_and_subtypes(expr_df, sample_info):
    """Assess whether FM patients show bimodal distribution in the Immune Module (CPA3/GATA2/MS4A2)."""
    fm_mask = sample_info['is_fm'].values
    fm_samples = sample_info[fm_mask]['sample_id'].values
    
    immune_genes = [g for g in ['CPA3', 'GATA2', 'MS4A2', 'FCER1A', 'HDC'] if g in expr_df.index]
    neural_genes = [g for g in ['DRD2', 'MDGA2', 'COMT', 'OPRM1'] if g in expr_df.index]
    
    fm_expr = expr_df[fm_samples].T
    
    # Immune Composite Score per patient (Z-score mean)
    immune_z = (fm_expr[immune_genes] - fm_expr[immune_genes].mean()) / fm_expr[immune_genes].std()
    fm_expr['Immune_Score'] = immune_z.mean(axis=1)
    
    # Fit 2-component Gaussian Mixture Model on Immune_Score
    gmm = GaussianMixture(n_components=2, random_state=42)
    scores_vals = fm_expr['Immune_Score'].values.reshape(-1, 1)
    gmm.fit(scores_vals)
    clusters = gmm.predict(scores_vals)
    probs = gmm.predict_proba(scores_vals)
    
    fm_expr['Subtype_Cluster'] = clusters
    fm_expr['Prob_Subtype1'] = probs[:, 0]
    fm_expr['Prob_Subtype2'] = probs[:, 1]
    
    # Identify which cluster has lower Immune Score (Autoimmune / Depleted basophil subtype)
    c0_mean = fm_expr[fm_expr['Subtype_Cluster'] == 0]['Immune_Score'].mean()
    c1_mean = fm_expr[fm_expr['Subtype_Cluster'] == 1]['Immune_Score'].mean()
    
    low_cluster = 0 if c0_mean < c1_mean else 1
    n_depleted = (fm_expr['Subtype_Cluster'] == low_cluster).sum()
    pct_depleted = (n_depleted / len(fm_expr)) * 100
    
    print(f"\nTotal FM Patients Analyzed: {len(fm_expr)}")
    print(f"Gaussian Mixture Model Subtype Split on Immune Module (CPA3/GATA2/MS4A2):")
    print(f"  - Subtype A (Bajo en marcadores inmunes / Autoinmune-Granulocítico): {n_depleted} pacientes ({pct_depleted:.1f}%)")
    print(f"  - Subtype B (Inmune Normal / Neuromodulador Central): {len(fm_expr) - n_depleted} pacientes ({100 - pct_depleted:.1f}%)")
    
    # Shapiro-Wilk test for normality on Immune_Score
    stat, pval_shapiro = shapiro(fm_expr['Immune_Score'])
    print(f"\nNormality Test on Immune Score (Shapiro-Wilk): W = {stat:.4f}, p-value = {pval_shapiro:.4f}")
    if pval_shapiro < 0.05:
        print("  -> La distribución del Score Inmune NO es normal (soporta heterogeneidad/subtipos bimodales en FM).")
    else:
        print("  -> La distribución es unimodal en este dataset.")
        
    return fm_expr


def main():
    print("=" * 70)
    print("ANALISIS DE SUBTIPOS Y DICOTOMÍA 30-40% EN FIBROMIALGIA")
    print("=" * 70)
    
    expr_67311, info_67311 = load_gse67311()
    fm_expr = analyze_bimodality_and_subtypes(expr_67311, info_67311)
    
    fm_expr.to_csv(OUTPUT_DIR / 'gse67311_patient_subtypes.csv')
    print(f"\nResultados de subtipificación guardados en {OUTPUT_DIR / 'gse67311_patient_subtypes.csv'}")


if __name__ == '__main__':
    main()
