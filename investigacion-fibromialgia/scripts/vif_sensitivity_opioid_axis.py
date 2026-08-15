#!/usr/bin/env python3
"""
VIF sensitivity (AUDIT 2.7) — eje opioide GSE221921.

PREGUNTA: el claim 2 ("eje opioide es composicional, no transcripcional")
depende de que las fracciones celulares de alta colinealidad no cambien
el veredicto en Model 6 (expr ~ grupo + sexo + fracciones).

HALLAZGO (2026-08-15): las fracciones tienen VIF severo
(T_cells_CD8=27.8, NK_cells=27.2, Mast_cells=21.2, Basophils=13.6).
Con TODAS las fracciones, 0/4 genes del eje opioide son significativos
(efecto enmascarado por colinealidad). AL QUITAR las fracciones de
VIF>5, 3/4 genes (TACR1/OPRM1/TAC1) se vuelven significativos (p<0.05).

CONCLUSION: la colinealidad NO inventaba el efecto, lo enmascaraba.
El claim 2 debe re-framearse: el eje opioide NO sobrevive al ajuste
celular COMPLETO (colineal), pero SÍ a un ajuste con fracciones
ortogonales. No es "puramente composicional" en sentido estricto.
"""
import pathlib
import pandas as pd, numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif_fn
import warnings; warnings.filterwarnings('ignore')

REPO = pathlib.Path(__file__).resolve().parent.parent
FRAC = REPO / 'analisis' / 'deconvolution' / 'gse221921_cell_fractions.csv'
XLSX = REPO / 'datos' / 'geo' / 'PBMC_FM_96patients_93controls' / 'GSE221921_FM_ProcessedData.xlsx'

frac = pd.read_csv(FRAC, index_col=0)
md = pd.read_excel(XLSX, sheet_name='Metadata (Samples)')
expr = pd.read_excel(XLSX, sheet_name='Values (FPKM)', index_col=0)
sample_cols = [c for c in expr.columns if c.startswith('Sample_')]
expr = expr.set_index('Hugo_Gene_Symbol')[sample_cols].apply(pd.to_numeric, errors='coerce')
samp = dict(zip(md['Sample'], md['Etiology'])); sex = dict(zip(md['Sample'], md['Gender']))
valid = [s for s in sample_cols if s in samp and s in frac.index]
expr = expr[valid]
is_fm = np.array([samp[s] == 'Fibromyalgia' for s in valid])
is_f = np.array([sex.get(s, 'Female') == 'Female' for s in valid])
frac = frac.loc[valid]

print("=== VIF por fraccion celular (n=%d)" % len(valid))
for i, c in enumerate(frac.columns):
    print(f"  {c:18s} VIF={vif_fn(frac.values, i):.2f}")

opioid = ['TACR1', 'OPRM1', 'TAC1', 'OPRK1']
high_vif = [c for i, c in enumerate(frac.columns) if vif_fn(frac.values, i) > 5]
ref = 'B_cells'  # drop reference to avoid perfect collinearity (sum=1)

def run_model(genes, drop_high):
    keep = [c for c in frac.columns if c != ref and (c not in high_vif if drop_high else True)]
    X = frac[keep].values.astype(float)
    out = {}
    for g in genes:
        if g not in expr.index:
            out[g] = {'note': 'absent'}; continue
        y = np.log2(expr.loc[g].values + 1)
        Xm = np.column_stack([np.ones(len(y)), is_fm.astype(float), is_f.astype(float), X])
        m = sm.OLS(y, Xm, missing='drop').fit()
        out[g] = {'n': int(m.nobs), 'beta': round(m.params[1], 3),
                  'p': round(m.pvalues[1], 4), 'sig': bool(m.pvalues[1] < 0.05)}
    return out

print("\n=== EJE OPIOIDE M3 FULL (todas fracciones):")
print(run_model(opioid, False))
print("\n=== EJE OPIOIDE M3 DROP high-VIF (>5):")
print(run_model(opioid, True))
