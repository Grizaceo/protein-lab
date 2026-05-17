import pandas as pd
import numpy as np
from statsmodels.stats.multitest import multipletests

# ── Paths ──────────────────────────────────────────────────────────────────
base = "/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia/datos"
gse67311_file  = f"{base}/GSE67311_DEGs_all_named.csv"
gse221921_file = f"{base}/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx"
out_dir        = f"{base}/../analisis"

# ── Gene lists (GWAS Kerrebijn 2025 – neural/synaptic prioritized genes) ──
mast_cell_genes   = ['CPA3', 'MS4A2', 'FCER1A', 'HDC']
gwas_neural_genes = ['DRD2', 'NCAM1', 'GPR52', 'CAMKV', 'CELF4',
                     'DCC', 'MDGA2', 'NPY', 'KYNU', 'SRD5A2',
                     'PPP2R2B', 'NPC1', 'HTT']
all_genes = mast_cell_genes + gwas_neural_genes

# ══════════════════════════════════════════════════════════════════════════
# DATASET 1: GSE67311 (whole blood, microarray, 70 FM + 70 HC)
# Already has gene_symbol column and FDR-corrected p_adj
# ══════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("DATASET 1: GSE67311 — Whole Blood (70 FM / 70 HC)")
print("=" * 65)

df67 = pd.read_csv(gse67311_file)
df67.columns = df67.columns.str.strip()

# Keep only probes that map to our target genes
gse67_hits = df67[df67['gene_symbol'].isin(all_genes)].copy()

# If a gene has multiple probes, keep the one with the smallest p_value (most significant)
gse67_hits = (gse67_hits
              .sort_values('p_value')
              .drop_duplicates(subset='gene_symbol', keep='first'))

# Re-apply FDR within this targeted gene list for a fair comparison
pvals = gse67_hits['p_value'].values
_, qvals, _, _ = multipletests(pvals, alpha=0.05, method='fdr_bh')
gse67_hits = gse67_hits.copy()
gse67_hits['q_value (FDR)'] = qvals
gse67_hits['Significant'] = qvals < 0.05
gse67_hits['Category'] = gse67_hits['gene_symbol'].apply(
    lambda g: 'Mast Cell' if g in mast_cell_genes else 'GWAS Neural')

result67 = (gse67_hits[['gene_symbol', 'Category',
                         'log2FC', 'p_value', 'q_value (FDR)', 'Significant']]
            .sort_values('p_value'))

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)
print(result67.to_string(index=False))

# ══════════════════════════════════════════════════════════════════════════
# DATASET 2: GSE221921 (PBMCs, RNA-seq FPKM, 96 FM + 93 HC)
# Raw computation (replicates deg_gse221921_fdr.py for clean output)
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("DATASET 2: GSE221921 — PBMCs (96 FM / 93 HC)")
print("=" * 65)

from scipy.stats import ttest_ind
xl = pd.ExcelFile(gse221921_file)
meta = xl.parse('Metadata (Samples)')
df221 = xl.parse('Values (FPKM)')

gene_col   = 'Hugo_Gene_Symbol'
sample_col = meta.columns[0]
group_col  = None
for col in meta.columns:
    if any(x in str(col).lower() for x in ['group','disease','condition','status','diagnosis']):
        group_col = col; break
if not group_col:
    group_col = meta.columns[1]

fm_ids, hc_ids = [], []
for _, row in meta.iterrows():
    val = str(row[group_col]).lower()
    if any(x in val for x in ['fm','fibro','patient']) or val == '1':
        fm_ids.append(row[sample_col])
    elif any(x in val for x in ['hc','control','healthy']) or val == '0':
        hc_ids.append(row[sample_col])

df_cols    = [c for c in df221.columns if 'Sample' in c or 'GSM' in c]
fm_cols    = [c for c in df_cols if c in fm_ids]
hc_cols    = [c for c in df_cols if c in hc_ids]

rows221 = []
for gene in all_genes:
    hits = df221[df221[gene_col] == gene]
    if hits.empty: continue
    row = hits.iloc[0]
    fm_v = pd.to_numeric(row[fm_cols], errors='coerce').dropna()
    hc_v = pd.to_numeric(row[hc_cols], errors='coerce').dropna()
    if len(fm_v) > 10 and len(hc_v) > 10:
        stat, pval = ttest_ind(fm_v, hc_v, equal_var=False)
        log2fc = np.log2(fm_v.mean() + 1e-6) - np.log2(hc_v.mean() + 1e-6)
        rows221.append({
            'gene_symbol': gene,
            'Category': 'Mast Cell' if gene in mast_cell_genes else 'GWAS Neural',
            'FM_mean': round(fm_v.mean(), 3),
            'HC_mean': round(hc_v.mean(), 3),
            'log2FC': round(log2fc, 3),
            'p_value': pval,
        })

df221_res = pd.DataFrame(rows221)
_, qvals221, _, _ = multipletests(df221_res['p_value'].values, alpha=0.05, method='fdr_bh')
df221_res['q_value (FDR)'] = qvals221
df221_res['Significant'] = qvals221 < 0.05
df221_res = df221_res.sort_values('p_value')
print(df221_res.to_string(index=False))

# ══════════════════════════════════════════════════════════════════════════
# CROSS-CONTEXT SUMMARY
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 65)
print("CROSS-CONTEXT SUMMARY")
print("=" * 65)

sig67  = set(result67[result67['Significant']]['gene_symbol'])
sig221 = set(df221_res[df221_res['Significant']]['gene_symbol'])
both   = sig67 & sig221
only67 = sig67 - sig221
only221= sig221 - sig67

print(f"\nSignificant in GSE67311 (whole blood):  {sorted(sig67)}")
print(f"Significant in GSE221921 (PBMCs):       {sorted(sig221)}")
print(f"\n★  REPLICATED IN BOTH datasets:         {sorted(both)}")
print(f"   Only in GSE67311:                    {sorted(only67)}")
print(f"   Only in GSE221921:                   {sorted(only221)}")

# Direction check for replicated genes
if both:
    print("\n--- Direction concordance for replicated genes ---")
    for g in sorted(both):
        fc67  = result67[result67['gene_symbol'] == g]['log2FC'].values[0]
        fc221 = df221_res[df221_res['gene_symbol'] == g]['log2FC'].values[0]
        concordant = (fc67 > 0) == (fc221 > 0)
        print(f"  {g:10s}  GSE67311 Log2FC={fc67:+.3f}  |  GSE221921 Log2FC={fc221:+.3f}  {'✓ concordant' if concordant else '✗ DISCORDANT'}")

# Save combined table
combined = pd.merge(
    result67[['gene_symbol','Category','log2FC','q_value (FDR)','Significant']].rename(
        columns={'log2FC':'Log2FC_67311', 'q_value (FDR)':'q_67311', 'Significant':'Sig_67311'}),
    df221_res[['gene_symbol','log2FC','q_value (FDR)','Significant']].rename(
        columns={'log2FC':'Log2FC_221921', 'q_value (FDR)':'q_221921', 'Significant':'Sig_221921'}),
    on='gene_symbol', how='outer'
).sort_values('q_221921')

out_path = f"{out_dir}/cross_context_gwas_neural_genes.csv"
combined.to_csv(out_path, index=False)

print(f"\nFull table saved → {out_path}")
