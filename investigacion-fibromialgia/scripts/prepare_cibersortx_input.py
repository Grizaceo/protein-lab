#!/usr/bin/env python3
"""Prepare CIBERSORTx input file from GSE221921 data."""
import pandas as pd
import numpy as np
import pathlib

REPO = pathlib.Path('/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia')
XLSX = REPO / 'datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx'

raw = pd.read_excel(XLSX, sheet_name='Values (FPKM)', index_col=0)
hugo = raw['Hugo_Gene_Symbol']
meta_cols = ['Hugo_Gene_Symbol','Gene_Description','Chromosome/scaffold name','Gene start (bp)','Gene end (bp)','Strand','Karyotype band']
sample_cols = [c for c in raw.columns if c not in meta_cols]

expr = raw[sample_cols].copy()
expr.index = hugo.values
expr.index.name = 'Gene'
expr = expr[expr.index.notna() & (expr.index != '')]
expr = expr.apply(pd.to_numeric, errors='coerce')

sm_meta = pd.read_excel(XLSX, sheet_name='Metadata (Samples)').set_index('Sample')
keep = [c for c in expr.columns if str(c) in sm_meta.index]
expr = expr[keep]

# Remove duplicates (keep highest mean)
expr['mean'] = expr.mean(axis=1)
expr = expr.sort_values('mean', ascending=False)
expr = expr[~expr.index.duplicated(keep='first')]
expr = expr.drop(columns=['mean'])

out_path = REPO / 'analisis' / 'falsificacion' / 'cibersortx_input_GSE221921.txt'
expr.to_csv(out_path, sep='\t')

print(f'Saved: {out_path}')
print(f'Shape: {expr.shape}')
print(f'First genes: {list(expr.index[:5])}')
print(f'Samples: {list(expr.columns[:5])}')
