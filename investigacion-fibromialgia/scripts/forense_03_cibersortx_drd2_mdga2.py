#!/usr/bin/env python3

import pathlib
import sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
from scipy.stats import pearsonr
import warnings

warnings.filterwarnings('ignore')

REPO = pathlib.Path(__file__).resolve().parent.parent
XLSX = REPO / 'datos' / 'geo' / 'PBMC_FM_96patients_93controls' / 'GSE221921_FM_ProcessedData.xlsx'

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

def load():
    xls = pd.ExcelFile(XLSX)
    raw = pd.read_excel(xls, sheet_name='Values (FPKM)', index_col=0)
    meta_cols = ['Hugo_Gene_Symbol', 'Gene_Description', 'Chromosome/scaffold name',
                 'Gene start (bp)', 'Gene end (bp)', 'Strand', 'Karyotype band']
    hugo = raw[raw.columns[0]]
    sample_cols = [c for c in raw.columns if c not in meta_cols]

    expr = raw[sample_cols].copy()
    expr.index = expr.index.map(lambda x: hugo.get(x, ''))
    expr = expr[expr.index != '']
    expr = expr.apply(pd.to_numeric, errors='coerce')

    order = expr.mean(axis=1).sort_values(ascending=False).index
    expr = expr.loc[order]
    expr = expr[~expr.index.duplicated(keep='first')]

    sm_meta = pd.read_excel(xls, sheet_name='Metadata (Samples)').set_index('Sample')
    keep = [c for c in expr.columns if str(c) in sm_meta.index]
    
    expr = expr[keep]
    md = sm_meta.loc[[str(c) for c in keep]]

    design = pd.DataFrame({
        'group': (md['Etiology'].astype(str).str.lower().str.contains('fibro')).astype(int).values,
        'sex_f': (md['Gender'].astype(str).str.lower().str.startswith('f')).astype(int).values,
    }, index=[str(c) for c in keep])

    return np.log2(expr + 1), design

def cell_scores(expr_log):
    sc = pd.DataFrame(index=expr_log.columns, dtype=float)
    for ct, markers in CELL_MARKERS.items():
        present = [m for m in markers if m in expr_log.index]
        sc[ct] = expr_log.loc[present].mean(axis=0) if present else 0.0
    sc.index = [str(i) for i in sc.index]
    return sc.div(sc.sum(axis=1), axis=0)

def main():
    print("Loading data...")
    expr_log, design = load()
    frac_all = cell_scores(expr_log).loc[design.index]
    
    ref = frac_all.mean().idxmax()
    frac = frac_all.drop(columns=[ref])
    print(f"Reference dropped: {ref}")

    targets = ['DRD2', 'MDGA2']
    
    for g in targets:
        print(f"\n{'='*50}\nANALYSIS FOR {g}\n{'='*50}")
        if g not in expr_log.index:
            print(f"{g} NOT in matrix.")
            continue
            
        y = expr_log.loc[g].values.astype(float)
        
        print("Pearson correlations with cell types:")
        for ct in frac_all.columns:
            r, p = pearsonr(y, frac_all[ct])
            print(f"  {ct:15} r = {r:+.4f}, p = {p:.4e}")
            
        X1 = sm.add_constant(design[['group']])
        m1 = sm.OLS(y, X1).fit()
        
        X2 = sm.add_constant(design[['group', 'sex_f']])
        m2 = sm.OLS(y, X2).fit()
        
        X3 = sm.add_constant(pd.concat([design[['group', 'sex_f']], frac], axis=1))
        m3 = sm.OLS(y, X3).fit()
        
        print(f"\nModel M1 (case):                p_group = {m1.pvalues['group']:.4e}, beta = {m1.params['group']:+.4f}")
        print(f"Model M2 (case+sex):            p_group = {m2.pvalues['group']:.4e}, beta = {m2.params['group']:+.4f}")
        print(f"Model M3 (case+sex+cell_fracs): p_group = {m3.pvalues['group']:.4e}, beta = {m3.params['group']:+.4f}")
        
        survives = m3.pvalues['group'] < 0.05
        print(f"SURVIVES DECONVOLUTION ADJUSTMENT: {'YES' if survives else 'NO'}\n")
        
        print(f"VIF in M3 for {g}:")
        vifs = []
        for i, col in enumerate(X3.columns):
            if col != 'const':
                v = vif(X3.values, i)
                vifs.append((col, v))
                print(f"  {col:15} {v:.2f}")

if __name__ == '__main__':
    main()
