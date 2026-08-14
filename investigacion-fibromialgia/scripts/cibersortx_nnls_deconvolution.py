#!/usr/bin/env python3
"""
CIBERSORTx-equivalent local deconvolution using NNLS.

Algorithm: Non-Negative Least Squares (NNLS) with immune cell markers.
This is the same core algorithm used by CIBERSORT (Newman 2015) and CIBERSORTx,
but implemented locally with publicly available marker genes.

Steps:
1. Build signature matrix S from marker genes (genes x cell types)
2. For each sample, solve: min ||S*f - x||^2 subject to f >= 0, sum(f) = 1
3. Use NNLS from scipy.optimize
4. Re-run Model 6 with NNLS-derived fractions
5. Test if COL9A1/PTN signal survives
"""

import pandas as pd
import numpy as np
from scipy.optimize import nnls
import pathlib
import json

REPO = pathlib.Path('/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia')
XLSX = REPO / 'datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx'
OUT_DIR = REPO / 'analisis' / 'falsificacion'
OUT_DIR.mkdir(exist_ok=True)

# Immune cell markers (from public sources: Abbas 2009, Bindea 2013, DICE database)
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

def load_data():
    """Load expression data and metadata."""
    raw = pd.read_excel(XLSX, sheet_name='Values (FPKM)', index_col=0)
    hugo = raw['Hugo_Gene_Symbol']
    meta_cols = ['Hugo_Gene_Symbol','Gene_Description','Chromosome/scaffold name',
                 'Gene start (bp)','Gene end (bp)','Strand','Karyotype band']
    sample_cols = [c for c in raw.columns if c not in meta_cols]
    
    expr = raw[sample_cols].copy()
    expr.index = hugo.values
    expr.index.name = 'Gene'
    expr = expr[expr.index.notna() & (expr.index != '')]
    expr = expr.apply(pd.to_numeric, errors='coerce')
    
    # Remove duplicates (keep highest mean)
    expr['mean'] = expr.mean(axis=1)
    expr = expr.sort_values('mean', ascending=False)
    expr = expr[~expr.index.duplicated(keep='first')]
    expr = expr.drop(columns=['mean'])
    
    # Load metadata
    sm_meta = pd.read_excel(XLSX, sheet_name='Metadata (Samples)').set_index('Sample')
    keep = [c for c in expr.columns if str(c) in sm_meta.index]
    expr = expr[keep]
    
    design = pd.DataFrame({
        'group': (sm_meta.loc[[str(c) for c in keep], 'Etiology']
                  .str.lower().str.contains('fibro').astype(int).values),
        'sex_f': (sm_meta.loc[[str(c) for c in keep], 'Gender']
                  .str.lower().str.startswith('f').astype(int).values),
    }, index=[str(c) for c in keep])
    
    return expr, design

def build_signature_matrix(expr, markers):
    """Build binary signature matrix S (genes x cell types) from marker genes."""
    all_markers = set()
    for genes in markers.values():
        all_markers.update([g for g in genes if g in expr.index])
    
    sig = pd.DataFrame(0, index=list(all_markers), columns=list(markers.keys()), dtype=float)
    for ct, genes in markers.items():
        for g in genes:
            if g in sig.index:
                sig.loc[g, ct] = 1.0
    
    # Normalize columns to sum to 1
    sig = sig.div(sig.sum(axis=0), axis=1)
    return sig

def nnls_deconvolution(expr, signature):
    """
    NNLS deconvolution for each sample.
    Solves: min ||x - S@f||^2 subject to f >= 0
    Then normalizes fractions to sum to 1.
    """
    fractions = pd.DataFrame(index=expr.columns, columns=signature.columns, dtype=float)
    
    # Align signature genes with expression matrix
    common_genes = [g for g in signature.index if g in expr.index]
    sig_aligned = signature.loc[common_genes]
    
    print(f"   Common genes for NNLS: {len(common_genes)}")
    print(f"   Signature matrix: {sig_aligned.shape[0]} genes x {sig_aligned.shape[1]} cell types")
    
    for sample in expr.columns:
        x = expr[sample].reindex(common_genes).values.astype(float)
        S = sig_aligned.values
        
        # Remove genes with NaN
        valid = ~np.isnan(x)
        x_valid = x[valid]
        S_valid = S[valid, :]
        
        # NNLS: min ||S@f - x||
        f, _ = nnls(S_valid, x_valid)
        
        # Normalize to sum to 1
        if f.sum() > 0:
            f = f / f.sum()
        
        fractions.loc[sample] = f
    
    return fractions

def run_model6_nnls(expression, case, sex_v, fractions):
    """Run Model 6 with NNLS-derived fractions."""
    n = len(case)
    frac_vals = fractions.values
    if frac_vals.shape[1] > 1:
        frac_design = frac_vals[:, :-1]
    else:
        frac_design = frac_vals
    
    X = np.column_stack([np.ones(n), case.astype(float), sex_v.astype(float), frac_design])
    y = np.log2(expression + 1)
    
    try:
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        y_hat = X @ beta
        resid = y - y_hat
        dof = n - X.shape[1]
        if dof <= 0:
            return 1.0, 0.0
        sse = np.sum(resid**2)
        XtX_inv = np.linalg.inv(X.T @ X)
        se = np.sqrt(sse / dof * XtX_inv[1, 1])
        if se == 0:
            return 1.0, 0.0
        t_stat = beta[1] / se
        from scipy import stats
        p = 2 * stats.t.sf(abs(t_stat), dof)
        return p, beta[1]
    except:
        return 1.0, 0.0

def main():
    print("=" * 60)
    print("CIBERSORTx-EQUIVALENT NNLS DECONVOLUTION")
    print("=" * 60)
    
    # Load data
    print("\n[1] Loading data...")
    expr, design = load_data()
    print(f"   Expression: {expr.shape[0]} genes x {expr.shape[1]} samples")
    print(f"   FM: {design['group'].sum()}, HC: {(1-design['group']).sum()}")
    
    # Build signature matrix
    print("\n[2] Building signature matrix from marker genes...")
    sig = build_signature_matrix(expr, CELL_MARKERS)
    print(f"   Signature: {sig.shape[0]} genes x {sig.shape[1]} cell types")
    
    # Run NNLS deconvolution
    print("\n[3] Running NNLS deconvolution (CIBERSORTx-equivalent)...")
    fractions = nnls_deconvolution(expr, sig)
    print(f"   Fractions: {fractions.shape[0]} samples x {fractions.shape[1]} cell types")
    print(f"   Mean fractions:\n{fractions.mean().to_string()}")
    
    # Save fractions
    fractions.to_csv(OUT_DIR / 'cibersortx_nnls_fractions.csv')
    
    # Test target genes
    print("\n[4] Testing target genes with NNLS-derived fractions...")
    targets = ['COL9A1', 'PTN', 'MDGA2', 'DRD2']
    results = {}
    
    for gene in targets:
        if gene in expr.index:
            y = expr.loc[gene].values.astype(float)
            p, beta = run_model6_nnls(y, design['group'].values, design['sex_f'].values, fractions)
            fc = np.mean(y[design['group']==1]) / (np.mean(y[design['group']==0]) + 1e-10)
            results[gene] = {'FC': float(fc), 'p': float(p), 'beta': float(beta)}
            print(f"   {gene}: FC={fc:.3f}, p={p:.4e}, beta={beta:.3f}")
        else:
            print(f"   {gene}: NOT FOUND")
    
    # Save results
    with open(OUT_DIR / 'cibersortx_nnls_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Verdict
    print("\n" + "=" * 60)
    print("VERDICT")
    print("=" * 60)
    for gene in targets:
        if gene in results:
            status = "SURVIVES" if results[gene]['p'] < 0.05 else "FALSIFIED"
            print(f"   {gene}: {status} (p={results[gene]['p']:.4e})")
    
    return results

if __name__ == '__main__':
    main()
