#!/usr/bin/env python3
"""
Falsificación in silico — Ejecución real de métodos remanentes.

Methods run:
  1. Permutation testing (1000 iterations)
  2. Winsorization (5%/95%) re-analysis
  3. Leave-one-out cross-validation
  4. Housekeeper comparison (ACTB, GAPDH, B2M)

Target genes: COL9A1, PTN, MDGA2, DRD2
Target datasets: GSE221921 (PBMC, 96 FM / 93 HC)
"""

import pandas as pd
import numpy as np
from scipy import stats
import pathlib
import json

# Paths
DATA_DIR = pathlib.Path('/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/datos/geo/PBMC_FM_96patients_93controls')
EXPR_FILE = DATA_DIR / 'GSE221921_FM_ProcessedData.xlsx'
FRACTIONS_FILE = pathlib.Path('/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/analisis/deconvolution/gse221921_cell_fractions.csv')
OUT_DIR = pathlib.Path('/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/analisis/falsificacion')
OUT_DIR.mkdir(exist_ok=True)

TARGET_GENES = ['COL9A1', 'PTN', 'MDGA2', 'DRD2']
HOUSEKEEPERS = ['ACTB', 'GAPDH', 'B2M']
np.random.seed(42)

print("=" * 60)
print("IN-SILICO FALSIFICATION — EXECUTION")
print("=" * 60)

# 1. Load expression data
print("\n[1] Loading expression data...")
df_fpkm = pd.read_excel(EXPR_FILE, sheet_name='Values (FPKM)', index_col=0)
print(f"   Expression matrix: {df_fpkm.shape[0]} genes x {df_fpkm.shape[1]} columns")

# First 7 columns are gene metadata, rest are samples
gene_meta_cols = ['Hugo_Gene_Symbol', 'Gene_Description', 'Chromosome/scaff name', 
                  'Gene start (bp)', 'Gene end (bp)', 'Strand', 'Karyotype band']
# Find actual meta columns (some may be named differently)
meta_cols = [c for c in df_fpkm.columns if c.startswith('Hugo') or c.startswith('Gene ') or c.startswith('Chromosome') or c.startswith('Karyotype')]
sample_cols = [c for c in df_fpkm.columns if c.startswith('Sample_')]
print(f"   Gene metadata columns: {len(meta_cols)}")
print(f"   Sample columns: {len(sample_cols)}")

# Set Hugo_Symbol as index for easy lookup
df_fpkm = df_fpkm.set_index('Hugo_Gene_Symbol')
# Keep only sample columns
df_expr = df_fpkm[sample_cols]
df_expr.index.name = 'Gene'
# Convert to numeric
df_expr = df_expr.apply(pd.to_numeric, errors='coerce')
print(f"   Expression matrix (genes x samples): {df_expr.shape}")

# 2. Load sample metadata
print("\n[2] Loading sample metadata...")
df_samples = pd.read_excel(EXPR_FILE, sheet_name='Metadata (Samples)')
print(f"   Sample metadata: {df_samples.shape[0]} samples")
print(f"   Columns: {list(df_samples.columns)}")

# Map samples to disease and gender
sample_to_disease = dict(zip(df_samples['Sample'], df_samples['Etiology']))
sample_to_gender = dict(zip(df_samples['Sample'], df_samples['Gender']))

# Filter to samples present in expression matrix
valid_samples = [s for s in sample_cols if s in sample_to_disease]
df_expr = df_expr[valid_samples]
is_fm = np.array([sample_to_disease[s] == 'Fibromyalgia' for s in valid_samples])
is_hc = np.array([sample_to_disease[s] == 'Control' for s in valid_samples])
sex_vec = np.array([1 if sample_to_gender.get(s, 'Female') == 'Female' else 0 for s in valid_samples])

n_fm = is_fm.sum()
n_hc = is_hc.sum()
print(f"   Valid samples: {len(valid_samples)} (FM={n_fm}, HC={n_hc})")
print(f"   Female: {sex_vec.sum()}, Male: {len(sex_vec) - sex_vec.sum()}")

# 3. Load cell fractions
print("\n[3] Loading cell fractions...")
df_frac = pd.read_csv(FRACTIONS_FILE, index_col=0)
print(f"   Fractions: {df_frac.shape[0]} samples x {df_frac.shape[1]} cell types")

# Align samples
common_samples = list(set(df_expr.columns) & set(df_frac.index))
df_expr = df_expr[common_samples]
df_frac = df_frac.loc[common_samples]
is_fm = np.array([sample_to_disease[s] == 'Fibromyalgia' for s in common_samples])
is_hc = np.array([sample_to_disease[s] == 'Control' for s in common_samples])
sex_vec = np.array([1 if sample_to_gender.get(s, 'Female') == 'Female' else 0 for s in common_samples])
n_fm = is_fm.sum()
n_hc = is_hc.sum()
print(f"   Aligned: {len(common_samples)} samples (FM={n_fm}, HC={n_hc})")

# 4. Helper: run Model 6 (deconvolution-adjusted)
def run_model6(expression, case, sex_v, fractions):
    """Run model 6: log2(expr+1) ~ case + sex + cell fractions.
    Returns p-value for case coefficient."""
    # Prepare design matrix
    n = len(case)
    
    # One-hot encode fractions (drop first to avoid collinearity)
    frac_vals = fractions.values
    if frac_vals.shape[1] > 1:
        frac_design = frac_vals[:, :-1]  # drop last cell type as reference
    else:
        frac_design = frac_vals
    
    # Design: [intercept, case, sex, fractions]
    X = np.column_stack([
        np.ones(n),
        case.astype(float),
        sex_v.astype(float),
        frac_design
    ])
    
    # Response
    y = np.log2(expression + 1)
    
    # OLS via least squares
    try:
        beta, residuals, rank, sv = np.linalg.lstsq(X, y, rcond=None)
        # Compute p-value for case coefficient (beta[1])
        y_hat = X @ beta
        resid = y - y_hat
        dof = n - X.shape[1]
        if dof <= 0:
            return 1.0, 0.0
        sse = np.sum(resid**2)
        # Standard error of case coefficient
        XtX_inv = np.linalg.inv(X.T @ X)
        se = np.sqrt(sse / dof * XtX_inv[1, 1])
        if se == 0:
            return 1.0, 0.0
        t_stat = beta[1] / se
        p = 2 * stats.t.sf(abs(t_stat), dof)
        return p, beta[1]  # p-value and effect size (beta for case)
    except Exception:
        return 1.0, 0.0

# 5. Check target genes exist
print("\n[4] Checking target genes...")
all_genes = TARGET_GENES + HOUSEKEEPERS
for gene in all_genes:
    if gene in df_expr.index:
        print(f"   {gene}: FOUND")
    else:
        print(f"   {gene}: NOT FOUND (searching...)")
        # Try partial match
        matches = [g for g in df_expr.index if gene in str(g)]
        if matches:
            print(f"      Possible matches: {matches[:5]}")

# 6. Baseline analysis
print("\n" + "=" * 60)
print("[5] BASELINE ANALYSIS (unpermuted)")
print("=" * 60)
baseline_results = {}
for gene in all_genes:
    if gene in df_expr.index:
        expr = df_expr.loc[gene].values.astype(float)
        p, beta = run_model6(expr, is_fm.astype(int), sex_vec, df_frac)
        fc = np.mean(expr[is_fm]) / (np.mean(expr[is_hc]) + 1e-10)
        baseline_results[gene] = {'FC': fc, 'p': p, 'beta': beta}
        print(f"   {gene}: FC={fc:.3f}, p={p:.4e}, beta={beta:.3f}")
    else:
        print(f"   {gene}: NOT FOUND")

# 7. Permutation testing
print("\n" + "=" * 60)
print("[6] PERMUTATION TESTING (1000 iterations)")
print("=" * 60)
n_perm = 1000
perm_results = {gene: [] for gene in TARGET_GENES}

for i in range(n_perm):
    # Shuffle case labels
    perm_case = is_fm.copy()
    np.random.shuffle(perm_case)
    
    for gene in TARGET_GENES:
        if gene in df_expr.index:
            expr = df_expr.loc[gene].values.astype(float)
            p, _ = run_model6(expr, perm_case.astype(int), sex_vec, df_frac)
            perm_results[gene].append(p)

# Analyze permutation results
print("\n   Permutation results (proportion of iterations with p < 0.05):")
permutation_summary = {}
for gene in TARGET_GENES:
    if perm_results[gene]:
        prop_sig = np.mean(np.array(perm_results[gene]) < 0.05)
        permutation_summary[gene] = {
            'prop_sig': float(prop_sig),
            'mean_p': float(np.mean(perm_results[gene])),
            'median_p': float(np.median(perm_results[gene])),
            'falsifies': bool(prop_sig > 0.10)
        }
        status = "FALSIFIES" if permutation_summary[gene]['falsifies'] else "OK"
        print(f"   {gene}: {prop_sig:.3f} permutations significant (mean p={permutation_summary[gene]['mean_p']:.3f}) -> {status}")

# 8. Winsorization (5%/95%)
print("\n" + "=" * 60)
print("[7] WINSORIZATION (5%/95%)")
print("=" * 60)

def winsorize_expr(expr, lower=0.05, upper=0.95):
    """Winsorize expression values."""
    vals = expr.copy()
    low = np.quantile(vals, lower)
    high = np.quantile(vals, upper)
    vals = np.clip(vals, low, high)
    return vals

winsor_results = {}
print("\n   Winsorized analysis:")
for gene in all_genes:
    if gene in df_expr.index:
        expr = df_expr.loc[gene].values.astype(float)
        expr_w = winsorize_expr(expr)
        p, beta = run_model6(expr_w, is_fm.astype(int), sex_vec, df_frac)
        fc = np.mean(expr_w[is_fm]) / (np.mean(expr_w[is_hc]) + 1e-10)
        winsor_results[gene] = {'FC': float(fc), 'p': float(p), 'beta': float(beta), 'falsifies': bool(fc < 1.5 and p > 0.05)}
        status = "FALSIFIES" if winsor_results[gene]['falsifies'] else "OK"
        print(f"   {gene}: FC={fc:.3f}, p={p:.4e} -> {status}")

# 9. Leave-one-out cross-validation
print("\n" + "=" * 60)
print("[8] LEAVE-ONE-OUT CROSS-VALIDATION")
print("=" * 60)

loo_results = {}
for gene in TARGET_GENES:
    if gene in df_expr.index:
        expr = df_expr.loc[gene].values.astype(float)
        n = len(expr)
        loo_ps = []
        loo_fcs = []
        loo_betas = []
        
        for i in range(n):
            # Remove sample i
            expr_loo = np.delete(expr, i)
            case_loo = np.delete(is_fm, i)
            sex_loo = np.delete(sex_vec, i)
            frac_loo = df_frac.drop(df_frac.index[i])
            
            p, beta = run_model6(expr_loo, case_loo.astype(int), sex_loo, frac_loo)
            fc = np.mean(expr_loo[case_loo]) / (np.mean(expr_loo[~case_loo]) + 1e-10)
            loo_ps.append(p)
            loo_fcs.append(fc)
            loo_betas.append(beta)
        
        loo_ps = np.array(loo_ps)
        loo_fcs = np.array(loo_fcs)
        loo_betas = np.array(loo_betas)
        
        # Check if any single sample drives the result
        prop_sig_without = np.mean(loo_ps < 0.05)
        
        loo_results[gene] = {
            'full_p': float(baseline_results[gene]['p']),
            'mean_loo_p': float(np.mean(loo_ps)),
            'median_loo_p': float(np.median(loo_ps)),
            'prop_sig_without': float(prop_sig_without),
            'min_loo_p': float(np.min(loo_ps)),
            'max_loo_p': float(np.max(loo_ps)),
            'mean_loo_fc': float(np.mean(loo_fcs)),
            'std_loo_fc': float(np.std(loo_fcs)),
            'mean_loo_beta': float(np.mean(loo_betas)),
            'falsifies': bool(prop_sig_without < 0.80)
        }
        
        status = "FALSIFIES" if loo_results[gene]['falsifies'] else "OK"
        print(f"   {gene}: full p={baseline_results[gene]['p']:.4e}, mean LOO p={loo_results[gene]['mean_loo_p']:.4e}")
        print(f"      {prop_sig_without:.1%} of LOO iterations remain significant (FC range: {loo_fcs.min():.2f}-{loo_fcs.max():.2f}) -> {status}")

# 10. Housekeeper comparison
print("\n" + "=" * 60)
print("[9] HOUSEKEEPER COMPARISON (ACTB, GAPDH, B2M)")
print("=" * 60)

housekeeper_results = {}
print("\n   Housekeeper analysis:")
for gene in HOUSEKEEPERS:
    if gene in df_expr.index:
        expr = df_expr.loc[gene].values.astype(float)
        p, beta = run_model6(expr, is_fm.astype(int), sex_vec, df_frac)
        fc = np.mean(expr[is_fm]) / (np.mean(expr[is_hc]) + 1e-10)
        housekeeper_results[gene] = {'FC': float(fc), 'p': float(p), 'beta': float(beta), 'is_significant': bool(p < 0.05)}
        status = "SIGNIFICANT" if p < 0.05 else "NS"
        print(f"   {gene}: FC={fc:.3f}, p={p:.4e} -> {status}")
    else:
        print(f"   {gene}: NOT FOUND")

# 11. Summary
print("\n" + "=" * 60)
print("SUMMARY — FALSIFICATION AUDIT")
print("=" * 60)

falsification_matrix = []
for gene in TARGET_GENES:
    row = {'Gene': gene}
    if gene in baseline_results:
        row['Baseline_p'] = f"{baseline_results[gene]['p']:.4e}"
        row['Baseline_FC'] = f"{baseline_results[gene]['FC']:.3f}"
    if gene in permutation_summary:
        row['Perm_%_sig'] = f"{permutation_summary[gene]['prop_sig']:.3f}"
        row['Perm_falsifies'] = "YES" if permutation_summary[gene]['falsifies'] else "NO"
    if gene in winsor_results:
        row['Wins_p'] = f"{winsor_results[gene]['p']:.4e}"
        row['Wins_FC'] = f"{winsor_results[gene]['FC']:.3f}"
        row['Wins_falsifies'] = "YES" if winsor_results[gene]['falsifies'] else "NO"
    if gene in loo_results:
        row['LOO_%_sig'] = f"{loo_results[gene]['prop_sig_without']:.1%}"
        row['LOO_falsifies'] = "YES" if loo_results[gene]['falsifies'] else "NO"
    falsification_matrix.append(row)

df_matrix = pd.DataFrame(falsification_matrix)
print("\n" + df_matrix.to_string(index=False))

# Save results
results = {
    'metadata': {
        'n_perm': n_perm,
        'n_samples': len(common_samples),
        'n_fm': int(n_fm),
        'n_hc': int(n_hc),
        'genes': TARGET_GENES,
        'housekeepers': HOUSEKEEPERS,
        'dataset': 'GSE221921',
        'method': 'Model 6 (deconvolution-adjusted)'
    },
    'baseline': baseline_results,
    'permutation': permutation_summary,
    'winsorization': winsor_results,
    'leave_one_out': loo_results,
    'housekeepers': housekeeper_results
}

with open(OUT_DIR / 'falsification_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to {OUT_DIR / 'falsification_results.json'}")

# Determine overall verdict
any_falsified = any(
    permutation_summary.get(g, {}).get('falsifies', False) or
    winsor_results.get(g, {}).get('falsifies', False) or
    loo_results.get(g, {}).get('falsifies', False)
    for g in TARGET_GENES
)

# Check if housekeepers are significant (would falsify platform)
housekeeper_sig = any(
    housekeeper_results.get(g, {}).get('is_significant', False)
    for g in HOUSEKEEPERS
)

print("\n" + "=" * 60)
if any_falsified:
    print("VERDICT: SOME CLAIMS FALSIFIED — SEE DETAILS ABOVE")
else:
    print("VERDICT: NO CLAIMS FALSIFIED BY THESE METHODS")
if housekeeper_sig:
    print("WARNING: Housekeepers are significant — platform noise detected")
else:
    print("HOUSEKEEPERS: All NS — platform noise not detected")
print("=" * 60)
