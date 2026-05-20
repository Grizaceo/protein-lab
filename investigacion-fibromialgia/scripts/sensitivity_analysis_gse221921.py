"""
Comprehensive sensitivity analysis for GSE221921 addressing peer review.
Runs: original Welch FPKM, log2(FPKM+1), Mann-Whitney, OLS sex-adjusted,
female-only subgroup. Reports all results in a single table.
"""
import os, warnings
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, mannwhitneyu
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm

warnings.filterwarnings('ignore')

# ── Config ─────────────────────────────────────────────────────────────────
import pathlib
GEO_DIR = str(pathlib.Path(__file__).resolve().parent.parent / "datos" / "geo" / "PBMC_FM_96patients_93controls")
DATA_FILE = os.path.join(GEO_DIR, "GSE221921_FM_ProcessedData.xlsx")
OUT_DIR = str(pathlib.Path(__file__).resolve().parent.parent / "analisis")

mast_cell_genes  = ['CPA3', 'MS4A2', 'FCER1A', 'HDC']
gwas_neural_genes = ['DRD2', 'NCAM1', 'GPR52', 'CAMKV', 'CELF4',
                    'DCC', 'MDGA2', 'NPY', 'KYNU', 'SRD5A2',
                    'PPP2R2B', 'NPC1', 'HTT']
all_genes = mast_cell_genes + gwas_neural_genes

# ── Load data ──────────────────────────────────────────────────────────────
print("Loading GSE221921...")
xl = pd.ExcelFile(DATA_FILE)
meta = xl.parse('Metadata (Samples)')
df   = xl.parse('Values (FPKM)')

# ── Parse metadata ─────────────────────────────────────────────────────────
print("\n=== METADATA COLUMNS ===")
print(list(meta.columns))
print()

# Find group column
group_col = None
for col in meta.columns:
    vals = meta[col].astype(str).str.lower()
    if vals.str.contains('fibro|fm|patient|control|healthy|hc').any():
        group_col = col
        break
if not group_col:
    group_col = meta.columns[1]

# Find sex column
sex_col = None
for col in meta.columns:
    vals = meta[col].astype(str).str.lower()
    if vals.str.contains('female|male|[mf]$').any():
        n_unique = vals.nunique()
        if 2 <= n_unique <= 3:
            sex_col = col
            break

sample_col = meta.columns[0]

# Classify samples
fm_ids, hc_ids = [], []
sample_sex = {}
for _, row in meta.iterrows():
    val = str(row[group_col]).lower()
    sid = row[sample_col]
    if any(x in val for x in ['fm','fibro','patient']) or val == '1':
        fm_ids.append(sid)
    elif any(x in val for x in ['hc','control','healthy']) or val == '0':
        hc_ids.append(sid)
    if sex_col:
        sample_sex[sid] = str(row[sex_col]).lower()

print(f"Group column: '{group_col}'")
print(f"Sex column: '{sex_col}'")
print(f"FM samples: {len(fm_ids)}, HC samples: {len(hc_ids)}")

# ── SEX DISTRIBUTION TABLE ────────────────────────────────────────────────
print("\n=== SEX × GROUP DISTRIBUTION ===")
if sex_col:
    fm_female = sum(1 for s in fm_ids if 'female' in sample_sex.get(s,'') or sample_sex.get(s,'') == 'f')
    fm_male   = sum(1 for s in fm_ids if 'male' in sample_sex.get(s,'') and 'female' not in sample_sex.get(s,'') or sample_sex.get(s,'') == 'm')
    hc_female = sum(1 for s in hc_ids if 'female' in sample_sex.get(s,'') or sample_sex.get(s,'') == 'f')
    hc_male   = sum(1 for s in hc_ids if 'male' in sample_sex.get(s,'') and 'female' not in sample_sex.get(s,'') or sample_sex.get(s,'') == 'm')
    print(f"  FM:  {fm_female} female, {fm_male} male")
    print(f"  HC:  {hc_female} female, {hc_male} male")
    print(f"  *** SEVERE SEX IMBALANCE ***" if abs(fm_female/(len(fm_ids)+1e-9) - hc_female/(len(hc_ids)+1e-9)) > 0.3 else "")

    # Build female-only lists
    fm_female_ids = [s for s in fm_ids if 'female' in sample_sex.get(s,'') or sample_sex.get(s,'') == 'f']
    hc_female_ids = [s for s in hc_ids if 'female' in sample_sex.get(s,'') or sample_sex.get(s,'') == 'f']
    print(f"  Female-only subsample: {len(fm_female_ids)} FM, {len(hc_female_ids)} HC")
else:
    print("  Sex column not found in metadata.")
    fm_female_ids, hc_female_ids = [], []

# ── Match data columns ────────────────────────────────────────────────────
gene_col = 'Hugo_Gene_Symbol'
df_cols  = [c for c in df.columns if 'Sample' in c or 'GSM' in c]
fm_cols  = [c for c in df_cols if c in fm_ids]
hc_cols  = [c for c in df_cols if c in hc_ids]
fm_f_cols = [c for c in df_cols if c in fm_female_ids]
hc_f_cols = [c for c in df_cols if c in hc_female_ids]

print(f"\nMatched columns: {len(fm_cols)} FM, {len(hc_cols)} HC")
print(f"Female-only cols: {len(fm_f_cols)} FM, {len(hc_f_cols)} HC")

# ── Check NPY ─────────────────────────────────────────────────────────────
missing_genes = [g for g in all_genes if g not in df[gene_col].values]
present_genes = [g for g in all_genes if g in df[gene_col].values]
print(f"\nPre-specified genes: {len(all_genes)}")
print(f"Present in matrix: {len(present_genes)}")
print(f"MISSING: {missing_genes}")

# ── Build sex vector for OLS ──────────────────────────────────────────────
all_sample_cols = fm_cols + hc_cols
case_vec = [1]*len(fm_cols) + [0]*len(hc_cols)
sex_vec  = []
for c in all_sample_cols:
    s = sample_sex.get(c, '')
    if 'female' in s or s == 'f':
        sex_vec.append(0)
    else:
        sex_vec.append(1)

# ── Analysis functions ─────────────────────────────────────────────────────
def welch_fpkm(row, fm_c, hc_c):
    fm_v = pd.to_numeric(row[fm_c], errors='coerce').dropna()
    hc_v = pd.to_numeric(row[hc_c], errors='coerce').dropna()
    if len(fm_v) < 5 or len(hc_v) < 5:
        return np.nan, np.nan, np.nan, np.nan
    stat, p = ttest_ind(fm_v, hc_v, equal_var=False)
    return fm_v.mean(), hc_v.mean(), np.log2(fm_v.mean()+1e-6) - np.log2(hc_v.mean()+1e-6), p

def welch_log2(row, fm_c, hc_c):
    fm_v = np.log2(pd.to_numeric(row[fm_c], errors='coerce').dropna() + 1)
    hc_v = np.log2(pd.to_numeric(row[hc_c], errors='coerce').dropna() + 1)
    if len(fm_v) < 5 or len(hc_v) < 5:
        return np.nan, np.nan
    stat, p = ttest_ind(fm_v, hc_v, equal_var=False)
    fc = fm_v.mean() - hc_v.mean()
    return fc, p

def mann_whitney(row, fm_c, hc_c):
    fm_v = pd.to_numeric(row[fm_c], errors='coerce').dropna()
    hc_v = pd.to_numeric(row[hc_c], errors='coerce').dropna()
    if len(fm_v) < 5 or len(hc_v) < 5:
        return np.nan
    stat, p = mannwhitneyu(fm_v, hc_v, alternative='two-sided')
    return p

def ols_sex_adjusted(row, sample_cols, case_v, sex_v):
    vals = pd.to_numeric(row[sample_cols], errors='coerce')
    mask = vals.notna()
    y = np.log2(vals[mask].values + 1)
    c = np.array(case_v)[mask.values]
    s = np.array(sex_v)[mask.values]
    X = sm.add_constant(np.column_stack([c, s]))
    try:
        res = sm.OLS(y, X).fit()
        return res.params[1], res.pvalues[1]  # case coefficient and p-value
    except:
        return np.nan, np.nan

# ── Run all analyses ───────────────────────────────────────────────────────
results = []
for gene in present_genes:
    rows = df[df[gene_col] == gene]
    if rows.empty:
        continue
    row = rows.iloc[0]
    cat = 'Mast Cell' if gene in mast_cell_genes else 'GWAS Neural'

    # 1. Original Welch FPKM
    fm_mean, hc_mean, lfc_raw, p_raw = welch_fpkm(row, fm_cols, hc_cols)

    # 2. Welch log2(FPKM+1)
    lfc_log, p_log = welch_log2(row, fm_cols, hc_cols)

    # 3. Mann-Whitney
    p_mw = mann_whitney(row, fm_cols, hc_cols)

    # 4. OLS sex-adjusted
    beta_sex, p_sex = ols_sex_adjusted(row, all_sample_cols, case_vec, sex_vec)

    # 5. Female-only Welch log2(FPKM+1)
    lfc_fem, p_fem = welch_log2(row, fm_f_cols, hc_f_cols)

    results.append({
        'Gene': gene, 'Category': cat,
        'FM_mean': round(fm_mean, 3) if not np.isnan(fm_mean) else np.nan,
        'HC_mean': round(hc_mean, 3) if not np.isnan(hc_mean) else np.nan,
        'Log2FC_raw': round(lfc_raw, 3) if not np.isnan(lfc_raw) else np.nan,
        'p_Welch_FPKM': p_raw,
        'Log2FC_log': round(lfc_log, 3) if not np.isnan(lfc_log) else np.nan,
        'p_Welch_log2': p_log,
        'p_MannWhitney': p_mw,
        'beta_case_sexadj': round(beta_sex, 4) if not np.isnan(beta_sex) else np.nan,
        'p_OLS_sexadj': p_sex,
        'Log2FC_femonly': round(lfc_fem, 3) if not np.isnan(lfc_fem) else np.nan,
        'p_femonly': p_fem,
    })

res_df = pd.DataFrame(results)

# ── Apply FDR to each column ──────────────────────────────────────────────
for pcol, qcol in [
    ('p_Welch_FPKM', 'q_Welch_FPKM'),
    ('p_Welch_log2', 'q_Welch_log2'),
    ('p_MannWhitney', 'q_MannWhitney'),
    ('p_OLS_sexadj', 'q_OLS_sexadj'),
    ('p_femonly', 'q_femonly'),
]:
    pvals = res_df[pcol].values
    mask = ~np.isnan(pvals)
    q = np.full(len(pvals), np.nan)
    if mask.sum() > 0:
        _, q_vals, _, _ = multipletests(pvals[mask], alpha=0.05, method='fdr_bh')
        q[mask] = q_vals
    res_df[qcol] = q

# ── Print results ──────────────────────────────────────────────────────────
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', lambda x: f'{x:.4g}')

res_df_sorted = res_df.sort_values('p_Welch_FPKM')

print("\n" + "=" * 120)
print("SENSITIVITY ANALYSIS: GSE221921 (96 FM / 93 HC)")
print("=" * 120)

# Compact display
display_cols = ['Gene', 'Category', 'FM_mean', 'HC_mean',
                'q_Welch_FPKM', 'q_Welch_log2', 'q_MannWhitney',
                'q_OLS_sexadj', 'q_femonly']
print(res_df_sorted[display_cols].to_string(index=False))

# ── Robustness classification ─────────────────────────────────────────────
print("\n" + "=" * 120)
print("ROBUSTNESS CLASSIFICATION")
print("=" * 120)
for _, row in res_df_sorted.iterrows():
    gene = row['Gene']
    tests_sig = sum([
        row.get('q_Welch_FPKM', 1) < 0.05,
        row.get('q_Welch_log2', 1) < 0.05,
        row.get('q_MannWhitney', 1) < 0.05,
        row.get('q_OLS_sexadj', 1) < 0.05,
        row.get('q_femonly', 1) < 0.05,
    ])
    if tests_sig == 5:
        label = "ROBUST (5/5)"
    elif tests_sig >= 3:
        label = f"SUPPORTED ({tests_sig}/5)"
    elif tests_sig >= 1:
        label = f"MODEL-SENSITIVE ({tests_sig}/5)"
    else:
        label = "NOT SIGNIFICANT"
    print(f"  {gene:10s} [{row['Category']:12s}]  {label}")

# ── Save ───────────────────────────────────────────────────────────────────
out_path = os.path.join(OUT_DIR, "sensitivity_analysis_GSE221921.csv")
res_df_sorted.to_csv(out_path, index=False)
print(f"\nFull table saved → {out_path}")
