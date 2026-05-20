import os
import pandas as pd

import pathlib
geo_dir = str(pathlib.Path(__file__).resolve().parent.parent / "datos" / "geo" / "PBMC_FM_96patients_93controls")
data_file = os.path.join(geo_dir, "GSE221921_FM_ProcessedData.xlsx")

print("Loading 'Values (FPKM)' sheet...")
xl = pd.ExcelFile(data_file)
df = xl.parse('Values (FPKM)')

print(f"Loaded sheet with shape {df.shape}")
print(df.head())

# Genes of interest
mast_cell_genes = ['CPA3', 'MS4A2', 'FCER1A', 'HDC']
dopamine_network = ['DRD2', 'NCAM1', 'GPR52', 'CAMKV', 'CELF4', 'DCC', 'MDGA2', 'NPY', 'KYNU', 'SRD5A2', 'PPP2R2B', 'NPC1', 'HTT']

gene_col = None
for col in df.columns:
    if 'hugo' in col.lower() or 'symbol' in col.lower() or 'gene' in col.lower():
        gene_col = col
        break

if not gene_col:
    gene_col = df.columns[0]

print(f"Using column '{gene_col}' for gene symbols.")

mast_df = df[df[gene_col].isin(mast_cell_genes)]
da_df = df[df[gene_col].isin(dopamine_network)]

print("\n--- MAST CELL MARKERS ---")
if not mast_df.empty:
    print(mast_df[[gene_col] + list(df.columns[:5])])
else:
    print("None of the mast cell markers were found in this sheet.")

print("\n--- DOPAMINE NETWORK (GWAS) ---")
if not da_df.empty:
    print(da_df[[gene_col] + list(df.columns[:5])])
else:
    print("None of the dopamine network genes were found in this sheet.")
