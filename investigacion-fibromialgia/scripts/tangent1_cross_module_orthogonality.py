#!/usr/bin/env python3
"""
Tangente 1 x Tangente 3/Fase 2: Cross-Module Orthogonality & Subtype Partitioning Analysis in Silico.
Evaluates whether the Immune/Granulocytic module (CPA3/GATA2/MS4A2) and the Dopaminergic/Neural module (DRD2/MDGA2)
are mutually exclusive, independent, or co-occurring in FM patients across GSE67311 and GSE221921.
"""

import os
import gzip
import pathlib
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, fisher_exact, chi2_contingency
import warnings
warnings.filterwarnings('ignore')

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / 'analisis' / 'tangente1'
DATA_DIR = REPO_ROOT / 'datos'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_gse67311():
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
    
    expr_df['gene_symbol'] = expr_df.index.map(lambda x: probe_to_gene.get(str(x), ''))
    expr_df = expr_df[expr_df['gene_symbol'] != '']
    expr_df['_mean'] = expr_df[sample_ids].mean(axis=1)
    expr_df = expr_df.sort_values('_mean', ascending=False)
    expr_df = expr_df[~expr_df['gene_symbol'].duplicated(keep='first')]
    expr_df = expr_df.drop('_mean', axis=1).set_index('gene_symbol')
    
    is_fm = ['Fibromyalgia' in s for s in sample_types]
    sample_info = pd.DataFrame({'sample_id': sample_ids, 'is_fm': is_fm})
    return expr_df, sample_info


def load_gse221921():
    xlsx_file = DATA_DIR / 'geo' / 'PBMC_FM_96patients_93controls' / 'GSE221921_FM_ProcessedData.xlsx'
    if not xlsx_file.exists():
        return None, None
    try:
        expr_full = pd.read_excel(xlsx_file, sheet_name='Values (FPKM)', index_col=0)
    except Exception as e:
        print(f"Warning: could not parse excel {xlsx_file}: {e}")
        return None, None
    hugo_col = expr_full.columns[0]
    ensembl_to_hugo = expr_full[hugo_col].to_dict()
    meta_cols = ['Hugo_Gene_Symbol', 'Gene_Description', 'Chromosome/scaffold name',
                 'Gene start (bp)', 'Gene end (bp)', 'Strand', 'Karyotype band']
    sample_cols = [c for c in expr_full.columns if c not in meta_cols]
    expr_df = expr_full[sample_cols]
    expr_df.index = expr_df.index.map(lambda x: ensembl_to_hugo.get(x, ''))
    expr_df = expr_df[expr_df.index != '']
    expr_df['_mean'] = expr_df.mean(axis=1)
    expr_df = expr_df.sort_values('_mean', ascending=False)
    expr_df = expr_df[~expr_df.index.duplicated(keep='first')]
    expr_df = expr_df.drop('_mean', axis=1)
    
    sample_meta = pd.read_excel(xlsx_file, sheet_name='Metadata (Samples)').set_index('Sample')
    sample_info_records = []
    for col in expr_df.columns:
        col_str = str(col)
        if col_str in sample_meta.index:
            etiology = str(sample_meta.loc[col_str, 'Etiology']).strip().lower()
            is_fm = 'fibro' in etiology
        else:
            is_fm = False
        sample_info_records.append({'sample_id': col_str, 'is_fm': is_fm})
    return expr_df, pd.DataFrame(sample_info_records)


def analyze_cross_module(expr_df, sample_info, dataset_name):
    print(f"\n{'='*70}\nCROSS-MODULE ANALYSIS: {dataset_name}\n{'='*70}")
    fm_mask = sample_info['is_fm'].values
    fm_samples = sample_info[fm_mask]['sample_id'].values
    
    immune_genes = [g for g in ['CPA3', 'GATA2', 'MS4A2', 'FCER1A', 'HDC'] if g in expr_df.index]
    neural_genes = [g for g in ['DRD2', 'MDGA2', 'COMT', 'MAOA', 'RGS17'] if g in expr_df.index]
    
    print(f"Immune Genes Available ({len(immune_genes)}): {immune_genes}")
    print(f"Neural/Dopaminergic Genes Available ({len(neural_genes)}): {neural_genes}")
    
    fm_expr = expr_df[fm_samples].T
    
    # Standardized Module Scores
    immune_z = (fm_expr[immune_genes] - fm_expr[immune_genes].mean()) / fm_expr[immune_genes].std()
    neural_z = (fm_expr[neural_genes] - fm_expr[neural_genes].mean()) / fm_expr[neural_genes].std()
    
    fm_expr['Immune_Score'] = immune_z.mean(axis=1)
    fm_expr['Neural_Score'] = neural_z.mean(axis=1)
    
    # Correlation Analysis
    r_pearson, p_pearson = pearsonr(fm_expr['Immune_Score'], fm_expr['Neural_Score'])
    r_spearman, p_spearman = spearmanr(fm_expr['Immune_Score'], fm_expr['Neural_Score'])
    
    print(f"\nModule Correlation (Immune vs Neural):")
    print(f"  Pearson r  = {r_pearson:.4f} (p = {p_pearson:.4f})")
    print(f"  Spearman ρ = {r_spearman:.4f} (p = {p_spearman:.4f})")
    
    # 2x2 Subtype Partitioning (Median split)
    imm_median = fm_expr['Immune_Score'].median()
    neu_median = fm_expr['Neural_Score'].median()
    
    fm_expr['Immune_Status'] = np.where(fm_expr['Immune_Score'] < imm_median, 'Immune_Depleted', 'Immune_Normal')
    fm_expr['Neural_Status'] = np.where(fm_expr['Neural_Score'] >= neu_median, 'Neural_High', 'Neural_Low')
    
    contingency_tab = pd.crosstab(fm_expr['Immune_Status'], fm_expr['Neural_Status'])
    odds_ratio, p_fisher = fisher_exact(contingency_tab)
    
    print("\n2x2 Subtype Contingency Table (Patient Counts):")
    print(contingency_tab.to_string())
    print(f"\nFisher's Exact Test: Odds Ratio = {odds_ratio:.4f}, p-value = {p_fisher:.4f}")
    
    if p_fisher > 0.05:
        print("  -> LOS MÓDULOS SON ESTADÍSTICAMENTE INDEPENDIENTES / ORTOGONALES.")
        print("  -> Esto confirma que el perfil autoinmune periférico (Tangente 1) y el perfil neurológico (Tangente 3) ocurren de forma INDEPENDIENTE en la población FM.")
    else:
        print("  -> Existe dependencia/co-ocurrencia estadísticamente significativa entre los módulos.")
        
    return {
        'dataset': dataset_name,
        'r_pearson': r_pearson,
        'p_pearson': p_pearson,
        'r_spearman': r_spearman,
        'p_spearman': p_spearman,
        'odds_ratio': odds_ratio,
        'p_fisher': p_fisher,
        'contingency': contingency_tab
    }


def main():
    results = []
    
    # 1. GSE67311 Whole Blood
    expr_67311, info_67311 = load_gse67311()
    res_67311 = analyze_cross_module(expr_67311, info_67311, "GSE67311_WholeBlood")
    results.append(res_67311)
    
    # 2. GSE221921 PBMCs
    expr_221921, info_221921 = load_gse221921()
    if expr_221921 is not None:
        res_221921 = analyze_cross_module(expr_221921, info_221921, "GSE221921_PBMCs")
        results.append(res_221921)
        
    summary_df = pd.DataFrame([{
        'dataset': r['dataset'],
        'r_pearson': r['r_pearson'],
        'p_pearson': r['p_pearson'],
        'r_spearman': r['r_spearman'],
        'p_spearman': r['p_spearman'],
        'odds_ratio': r['odds_ratio'],
        'p_fisher': r['p_fisher']
    } for r in results])
    
    summary_df.to_csv(OUTPUT_DIR / 'cross_module_orthogonality_summary.csv', index=False)
    print(f"\nResumen de ortogonalidad guardado en {OUTPUT_DIR / 'cross_module_orthogonality_summary.csv'}")


if __name__ == '__main__':
    main()
