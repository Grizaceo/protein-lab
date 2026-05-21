#!/usr/bin/env python3
"""
Cell-type deconvolution of GSE67311 (whole blood) and GSE221921 (PBMCs).

Uses NNLS with curated marker gene signatures to estimate cell fractions.
"""

import pandas as pd
import numpy as np
from scipy.optimize import nnls
from scipy.stats import mannwhitneyu
import gzip
import os
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = '/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia/analisis/deconvolution'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# CELL-TYPE MARKER GENES (curated from LM22/CIBERSORT/xCell)
# ============================================================
CELL_MARKERS = {
    'B_cells': ['CD19', 'CD79A', 'MS4A1', 'FCER2', 'TCL1A', 'CD22'],
    'T_cells_CD4': ['CD4', 'IL7R', 'CCR7', 'LEF1', 'TCF7', 'SELL'],
    'T_cells_CD8': ['CD8A', 'CD8B', 'GZMK', 'GZMA', 'NKG7', 'GZMB'],
    'T_cells_Treg': ['FOXP3', 'IL2RA', 'CTLA4', 'TIGIT', 'IKZF2'],
    'NK_cells': ['NCAM1', 'NKG7', 'KLRD1', 'KLRB1', 'GNLY', 'GZMH'],
    'Monocytes': ['CD14', 'LYZ', 'S100A8', 'S100A9', 'FCGR3A', 'CD68'],
    'Dendritic_cells': ['CD1C', 'FCER1A', 'HLA-DRA', 'HLA-DRB1', 'ITGAX'],
    'Neutrophils': ['CSF3R', 'FCGR3B', 'CXCR2', 'S100A12', 'MMP9', 'ELANE'],
    'Eosinophils': ['SIGLEC8', 'CLC', 'PRG2', 'PRG3', 'EPX'],
    'Basophils': ['MS4A2', 'FCER1A', 'CPA3', 'HDC', 'GATA2'],
    'Mast_cells': ['CPA3', 'MS4A2', 'FCER1A', 'HDC', 'TPSAB1', 'TPSB2', 'KIT'],
    'Platelets': ['ITGA2B', 'GP1BA', 'PF4', 'PPBP', 'SELP'],
}

KEY_GENES = ['DRD2', 'MDGA2', 'CPA3', 'MS4A2', 'FCER1A', 'HDC']


# ============================================================
# LOAD GSE67311 (Whole Blood, Affymetrix array)
# ============================================================
def load_gse67311():
    print("Loading GSE67311 (whole blood)...")
    
    matrix_file = '/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia/datos/geo/GSE67311/GSE67311_series_matrix.txt.gz'
    degs_file = '/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia/datos/GSE67311_DEGs_all_named.csv'
    
    # Parse series matrix
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
    
    # Build expression DataFrame
    expr_df = pd.DataFrame(expr_data, index=sample_ids).T
    expr_df.index.name = 'probe_id'
    
    # Map probes to gene symbols using DEGs file (has probe_id -> gene_symbol)
    degs = pd.read_csv(degs_file)
    probe_to_gene = dict(zip(degs['gene_id'].astype(str), degs['gene_symbol']))
    
    expr_df['gene_symbol'] = expr_df.index.map(lambda x: probe_to_gene.get(str(x), ''))
    expr_df = expr_df[expr_df['gene_symbol'] != '']
    
    # For duplicate genes, keep probe with highest mean expression
    expr_df['_mean'] = expr_df[sample_ids].mean(axis=1)
    expr_df = expr_df.sort_values('_mean', ascending=False)
    expr_df = expr_df[~expr_df['gene_symbol'].duplicated(keep='first')]
    expr_df = expr_df.drop('_mean', axis=1)
    expr_df = expr_df.set_index('gene_symbol')
    
    # Sample info
    sample_info = pd.DataFrame({
        'sample_id': sample_ids,
        'is_fm': ['Fibromyalgia' in s for s in sample_types]
    })
    
    print(f"  {expr_df.shape[0]} genes x {expr_df.shape[1]} samples")
    print(f"  FM: {sample_info['is_fm'].sum()}, HC: {(~sample_info['is_fm']).sum()}")
    
    return expr_df, sample_info


# ============================================================
# LOAD GSE221921 (PBMCs, RNA-seq)
# ============================================================
def load_gse221921():
    print("Loading GSE221921 (PBMCs)...")
    
    xlsx_file = '/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia/datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx'
    
    # Read FPKM values
    # First 7 columns are gene metadata, rest are samples
    expr_full = pd.read_excel(xlsx_file, sheet_name='Values (FPKM)', index_col=0)
    
    # Hugo_Gene_Symbol is the first column
    hugo_col = expr_full.columns[0]
    ensembl_to_hugo = expr_full[hugo_col].to_dict()
    
    # Drop metadata columns, keep only sample columns
    meta_cols = ['Hugo_Gene_Symbol', 'Gene_Description', 'Chromosome/scaffold name',
                 'Gene start (bp)', 'Gene end (bp)', 'Strand', 'Karyotype band']
    sample_cols = [c for c in expr_full.columns if c not in meta_cols]
    expr_df = expr_full[sample_cols]
    
    # Map Ensembl IDs to Hugo symbols
    expr_df.index = expr_df.index.map(lambda x: ensembl_to_hugo.get(x, ''))
    expr_df = expr_df[expr_df.index != '']
    
    # Remove duplicates
    expr_df['_mean'] = expr_df.mean(axis=1)
    expr_df = expr_df.sort_values('_mean', ascending=False)
    expr_df = expr_df[~expr_df.index.duplicated(keep='first')]
    expr_df = expr_df.drop('_mean', axis=1)
    
    # Read sample metadata
    sample_meta = pd.read_excel(xlsx_file, sheet_name='Metadata (Samples)')
    sample_meta = sample_meta.set_index('Sample')
    
    # Match columns
    sample_info_records = []
    for col in expr_df.columns:
        col_str = str(col)
        if col_str in sample_meta.index:
            etiology = str(sample_meta.loc[col_str, 'Etiology']).strip().lower()
            is_fm = 'fibro' in etiology
        else:
            is_fm = False
        sample_info_records.append({'sample_id': col_str, 'is_fm': is_fm})
    
    sample_info = pd.DataFrame(sample_info_records)
    
    print(f"  {expr_df.shape[0]} genes x {expr_df.shape[1]} samples")
    print(f"  FM: {sample_info['is_fm'].sum()}, HC: {(~sample_info['is_fm']).sum()}")
    
    return expr_df, sample_info


# ============================================================
# DECONVOLUTION
# ============================================================
def deconvolve(expr_df, cell_markers):
    """NNLS deconvolution."""
    
    # Build signature: for each cell type, mean expression of its markers
    frac_results = {}
    
    for sample in expr_df.columns:
        y = expr_df[sample].values
        gene_names = expr_df.index.tolist()
        
        # Build signature matrix
        sig_genes = []
        sig_celltypes = []
        for ct, markers in cell_markers.items():
            for m in markers:
                if m in expr_df.index:
                    sig_genes.append(m)
                    sig_celltypes.append(ct)
        
        if not sig_genes:
            frac_results[sample] = {ct: 0 for ct in cell_markets}
            continue
        
        S = np.array([expr_df.loc[g].values for g in sig_genes])  # n_markers x n_samples_for_this_gene
        # Actually we need: for each cell type, the mean expression profile of its markers
        # Simplified: use mean expression of markers per cell type as signature
        
        cell_types = list(cell_markers.keys())
        S_matrix = np.zeros((len(expr_df), len(cell_types)))
        
        for j, ct in enumerate(cell_types):
            ct_markers = [m for m in cell_markers[ct] if m in expr_df.index]
            if ct_markers:
                S_matrix[:, j] = expr_df.loc[ct_markers].mean(axis=0).values
        
        # NNLS for this sample
        y_vec = expr_df[sample].values
        y_vec = np.maximum(y_vec, 0)
        S_mat = np.maximum(S_matrix, 0)
        
        x, _ = nnls(S_mat, y_vec)
        if x.sum() > 0:
            x = x / x.sum()
        
        frac_results[sample] = {ct: x[i] for i, ct in enumerate(cell_types)}
    
    return pd.DataFrame(frac_results).T


def deconvolve_simple(expr_df, cell_markers):
    """Simplified deconvolution: use mean marker expression per cell type."""
    
    cell_types = list(cell_markers.keys())
    
    # Compute cell-type scores (mean of marker genes per cell type)
    scores = pd.DataFrame(index=expr_df.columns, columns=cell_types, dtype=float)
    
    for ct in cell_types:
        ct_markers = [m for m in cell_markers[ct] if m in expr_df.index]
        if ct_markers:
            scores[ct] = expr_df.loc[ct_markers].mean(axis=0)
        else:
            scores[ct] = 0.0
    
    # Normalize to sum to 1 per sample
    scores = scores.astype(float)
    row_sums = scores.sum(axis=1)
    scores = scores.div(row_sums, axis=0)
    
    return scores


def analyze(frac_df, sample_info, expr_df, dataset_name):
    """Analyze deconvolution results."""
    print(f"\n{'='*60}")
    print(f"{dataset_name} — Cell-type deconvolution")
    print(f"{'='*60}")
    
    merged = frac_df.copy()
    merged['is_fm'] = sample_info['is_fm'].values
    
    print(f"\n{'Cell Type':<20} {'FM mean':>10} {'HC mean':>10} {'Diff':>10} {'p-value':>10} {'Sig':>5}")
    print("-" * 70)
    
    results = []
    for ct in frac_df.columns:
        fm = merged[merged['is_fm'] == True][ct]
        hc = merged[merged['is_fm'] == False][ct]
        stat, pval = mannwhitneyu(fm, hc, alternative='two-sided')
        diff = fm.mean() - hc.mean()
        sig = '*' if pval < 0.05 else ''
        print(f"{ct:<20} {fm.mean():>10.4f} {hc.mean():>10.4f} {diff:>10.4f} {pval:>10.4f} {sig:>5}")
        results.append({'cell_type': ct, 'fm_mean': fm.mean(), 'hc_mean': hc.mean(),
                        'diff': diff, 'p_value': pval, 'significant': pval < 0.05})
    
    # Key gene analysis
    print(f"\n\nKey gene expression (FM vs HC):")
    print(f"{'Gene':<10} {'FM mean':>10} {'HC mean':>10} {'log2FC':>10} {'p-value':>10}")
    print("-" * 55)
    
    for gene in KEY_GENES:
        if gene in expr_df.index:
            fm_mask = merged['is_fm'] == True
            fm_vals = expr_df.loc[gene, fm_mask.values]
            hc_vals = expr_df.loc[gene, ~fm_mask.values]
            log2fc = np.log2(fm_vals.mean() + 1) - np.log2(hc_vals.mean() + 1)
            _, pval = mannwhitneyu(fm_vals, hc_vals)
            print(f"{gene:<10} {fm_vals.mean():>10.2f} {hc_vals.mean():>10.2f} {log2fc:>10.4f} {pval:>10.4f}")
    
    # Correlation: key genes vs cell fractions
    print(f"\n\nCorrelation: Key genes vs cell fractions:")
    for gene in KEY_GENES:
        if gene not in expr_df.index:
            continue
        gene_expr = expr_df.loc[gene]
        for ct in frac_df.columns:
            r = np.corrcoef(gene_expr, frac_df[ct])[0, 1]
            if abs(r) > 0.3:
                print(f"  {gene} vs {ct}: r={r:.4f}")
    
    return pd.DataFrame(results).sort_values('p_value')


# ============================================================
# MAIN
# ============================================================
def main():
    print("="*60)
    print("CELL-TYPE DECONVOLUTION — FM TRANSCRIPTOMICS")
    print("="*60)
    
    # Load data
    expr_67311, info_67311 = load_gse67311()
    expr_221921, info_221921 = load_gse221921()
    
    # Deconvolve
    print("\nDeconvolving GSE67311...")
    frac_67311 = deconvolve_simple(expr_67311, CELL_MARKERS)
    results_67311 = analyze(frac_67311, info_67311, expr_67311, "GSE67311 (Whole Blood)")
    
    print("\n\nDeconvolving GSE221921...")
    frac_221921 = deconvolve_simple(expr_221921, CELL_MARKERS)
    results_221921 = analyze(frac_221921, info_221921, expr_221921, "GSE221921 (PBMCs)")
    
    # Save
    frac_67311.to_csv(f'{OUTPUT_DIR}/gse67311_cell_fractions.csv')
    frac_221921.to_csv(f'{OUTPUT_DIR}/gse221921_cell_fractions.csv')
    results_67311.to_csv(f'{OUTPUT_DIR}/gse67311_deconv_results.csv', index=False)
    results_221921.to_csv(f'{OUTPUT_DIR}/gse221921_deconv_results.csv', index=False)
    
    print(f"\n\nResults saved to {OUTPUT_DIR}/")
    print("Done.")


if __name__ == '__main__':
    main()
