import os
import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import diptest

# Setup paths
base_dir = pathlib.Path(__file__).resolve().parent.parent
geo_dir = base_dir / "datos" / "geo" / "PBMC_FM_96patients_93controls"
data_file = geo_dir / "GSE221921_FM_ProcessedData.xlsx"
out_dir = base_dir / "results"
os.makedirs(out_dir, exist_ok=True)

print("Loading GSE221921 FPKM matrix...")
xl = pd.ExcelFile(data_file)
meta_samples = xl.parse('Metadata (Samples)')
df = xl.parse('Values (FPKM)')

# Get Sample labels
group_col = None
for col in meta_samples.columns:
    if any(x in str(col).lower() for x in ['group', 'disease', 'condition', 'status', 'diagnosis']):
        group_col = col
        break
if not group_col:
    group_col = meta_samples.columns[1]
sample_col = meta_samples.columns[0]

fm_samples = []
hc_samples = []
for idx, row in meta_samples.iterrows():
    val = str(row[group_col]).lower()
    if 'fm' in val or 'fibro' in val or 'patient' in val or val == '1':
        fm_samples.append(row[sample_col])
    elif 'hc' in val or 'control' in val or 'healthy' in val or val == '0':
        hc_samples.append(row[sample_col])

# Match columns
gene_col = 'Hugo_Gene_Symbol'
if gene_col not in df.columns:
    gene_col = df.columns[0]

df_sample_cols = [c for c in df.columns if 'Sample' in c or 'GSM' in c]
fm_cols = [c for c in df_sample_cols if c in fm_samples]
hc_cols = [c for c in df_sample_cols if c in hc_samples]

print(f"Matched {len(fm_cols)} FM samples and {len(hc_cols)} HC samples from matrix.")
all_cols = fm_cols + hc_cols

# Define genes
genes_of_interest = ['DRD2', 'MDGA2']
housekeeping = ['ACTB', 'GAPDH']

# Gene lengths in kb
lengths = {
    'DRD2': 2.4,
    'MDGA2': 4.2
}
TOTAL_MAPPED_READS_M = 30  # Assumed 30 million reads

results = []
for gene in genes_of_interest + housekeeping:
    gene_row = df[df[gene_col] == gene]
    if gene_row.empty:
        print(f"{gene} not found.")
        continue
    
    vals_fm = pd.to_numeric(gene_row[fm_cols].iloc[0], errors='coerce').dropna().values
    vals_hc = pd.to_numeric(gene_row[hc_cols].iloc[0], errors='coerce').dropna().values
    vals_all = np.concatenate([vals_fm, vals_hc])
    
    # Basic counts
    n_fm = len(vals_fm)
    n_hc = len(vals_hc)
    
    fm_gt_0 = np.sum(vals_fm > 0)
    hc_gt_0 = np.sum(vals_hc > 0)
    all_gt_0 = fm_gt_0 + hc_gt_0
    
    # Stats
    def get_stats(v):
        if len(v) == 0: return (0,0,0,0,0,0)
        return (np.mean(v), np.median(v), np.std(v), np.min(v), np.max(v), np.percentile(v, 75) - np.percentile(v, 25))
    
    stat_fm = get_stats(vals_fm)
    stat_hc = get_stats(vals_hc)
    
    # Estimate counts
    est_counts_all = []
    if gene in lengths:
        l = lengths[gene]
        est_counts_all = vals_all * l * TOTAL_MAPPED_READS_M
    
    mean_count = np.mean(est_counts_all) if len(est_counts_all) > 0 else 0
    max_count = np.max(est_counts_all) if len(est_counts_all) > 0 else 0
    
    # Hartigan's Dip Test
    # dip is the dip statistic, pval is p-value
    dip, pval_dip = diptest.diptest(vals_all) if len(vals_all) > 3 else (0, 1)
    
    res = {
        'Gene': gene,
        'Samples_N': len(vals_all),
        'Samples_>0': all_gt_0,
        'Samples_=0': len(vals_all) - all_gt_0,
        'FM_>0_%': (fm_gt_0 / n_fm * 100) if n_fm > 0 else 0,
        'HC_>0_%': (hc_gt_0 / n_hc * 100) if n_hc > 0 else 0,
        'FM_mean': stat_fm[0],
        'FM_med': stat_fm[1],
        'FM_max': stat_fm[4],
        'HC_mean': stat_hc[0],
        'HC_med': stat_hc[1],
        'HC_max': stat_hc[4],
        'Est_Mean_Count': mean_count,
        'Est_Max_Count': max_count,
        'Dip_Test_p': pval_dip
    }
    results.append(res)
    
    # Plotting for genes of interest
    if gene in genes_of_interest:
        plt.figure(figsize=(8,5))
        sns.histplot(data={'FM': vals_fm, 'HC': vals_hc}, bins=30, kde=True)
        plt.title(f"{gene} FPKM Distribution")
        plt.xlabel("FPKM")
        plt.ylabel("Count")
        plt.savefig(out_dir / f"{gene}_fpkm_hist.png")
        plt.close()

res_df = pd.DataFrame(results)
print("\n--- ANALYSIS RESULTS ---")
print(res_df.to_string(index=False))
