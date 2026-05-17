import os
import pandas as pd
from scipy.stats import ttest_ind

geo_dir = "/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia/datos/geo/PBMC_FM_96patients_93controls"
data_file = os.path.join(geo_dir, "GSE221921_FM_ProcessedData.xlsx")

print("Loading data...")
xl = pd.ExcelFile(data_file)
meta_samples = xl.parse('Metadata (Samples)')
df = xl.parse('Values (FPKM)')

# Get Sample labels
# The 'Metadata (Samples)' sheet probably has Sample ID and a grouping variable
# Let's see its columns first.
print("Sample Metadata columns:", meta_samples.columns.tolist())
# Find grouping column (contains 'group', 'disease', 'condition', 'status')
group_col = None
for col in meta_samples.columns:
    if any(x in str(col).lower() for x in ['group', 'disease', 'condition', 'status', 'diagnosis']):
        group_col = col
        break

if not group_col:
    # If not obvious, let's just assume the second column is the group if first is sample ID
    group_col = meta_samples.columns[1]

sample_col = meta_samples.columns[0]
print(f"Using '{sample_col}' for samples and '{group_col}' for groups.")

# Get lists of samples
fm_samples = []
hc_samples = []
for idx, row in meta_samples.iterrows():
    val = str(row[group_col]).lower()
    if 'fm' in val or 'fibro' in val or 'patient' in val or val == '1':
        fm_samples.append(row[sample_col])
    elif 'hc' in val or 'control' in val or 'healthy' in val or val == '0':
        hc_samples.append(row[sample_col])

print(f"Found {len(fm_samples)} FM samples and {len(hc_samples)} HC samples.")

# Filter genes
mast_cell_genes = ['CPA3', 'MS4A2', 'FCER1A', 'HDC']
dopamine_network = ['DRD2', 'NCAM1', 'GPR52', 'CAMKV', 'CELF4', 'DCC', 'MDGA2', 'NPY', 'KYNU', 'SRD5A2', 'PPP2R2B', 'NPC1', 'HTT']

gene_col = 'Hugo_Gene_Symbol'

def test_genes(gene_list, name):
    print(f"\n--- {name} ---")
    sub_df = df[df[gene_col].isin(gene_list)]
    
    results = []
    for idx, row in sub_df.iterrows():
        gene = row[gene_col]
        # Some sample columns might have prefix or suffix. Let's match by intersection
        fm_cols = [c for c in df.columns if c in fm_samples]
        hc_cols = [c for c in df.columns if c in hc_samples]
        
        if not fm_cols and not hc_cols:
            # Maybe the columns are just 'Sample_123' instead of 'GSM...'
            # We need to map
            pass
            
        fm_vals = pd.to_numeric(row[fm_cols], errors='coerce').dropna()
        hc_vals = pd.to_numeric(row[hc_cols], errors='coerce').dropna()
        
        if len(fm_vals) > 0 and len(hc_vals) > 0:
            stat, pval = ttest_ind(fm_vals, hc_vals, equal_var=False)
            log2fc = np.log2(fm_vals.mean() + 1e-6) - np.log2(hc_vals.mean() + 1e-6)
            results.append({
                'Gene': gene,
                'FM_mean': fm_vals.mean(),
                'HC_mean': hc_vals.mean(),
                'Log2FC': log2fc,
                'p_value': pval
            })
    
    if results:
        res_df = pd.DataFrame(results)
        res_df = res_df.sort_values('p_value')
        print(res_df.to_string(index=False))
    else:
        print("No valid columns found for testing.")

import numpy as np

# Before testing, let's fix the column matching just in case
meta_sample_ids = meta_samples[sample_col].astype(str).tolist()
df_sample_cols = [c for c in df.columns if 'Sample' in c or 'GSM' in c]

# if the metadata sample ids don't match the df columns, we need to map them
# e.g., metadata has "Sample_1", but df has "Sample_1"
fm_cols = [c for c in df_sample_cols if c in fm_samples]
hc_cols = [c for c in df_sample_cols if c in hc_samples]

if not fm_cols or not hc_cols:
    print("Column names don't exactly match. Attempting fuzzy match...")
    # This might happen if meta has 'GSM123' and df has 'Sample_123'. We would need to map them.
    # For now let's print a few to see
    print("Meta IDs:", meta_sample_ids[:5])
    print("DF Cols:", df_sample_cols[:5])

test_genes(mast_cell_genes, "MAST CELL MARKERS")
test_genes(dopamine_network, "DOPAMINE NETWORK (GWAS)")
