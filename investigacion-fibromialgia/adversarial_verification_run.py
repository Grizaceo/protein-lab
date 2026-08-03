#!/usr/bin/env python3
"""
ADVERSARIAL VERIFICATION — FM biomarkers (GSE221921)
Re-audita los claims de validate_fm_biomarkers_iter2.py con rigor:
  Q1: Data integrity (mapping, conteo, outliers)
  Q2: Statistical robustness (normalidad, Mann-Whitney, Bonferroni, AUC honesta)
  Q4: LGALS3BP discordancia (recalculada desde cero)
  Q5: Effect size (Cohen's d)
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score

XLSX = 'datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx'
xls = pd.ExcelFile(XLSX)
meta = pd.read_excel(xls, 'Metadata (Samples)')
values = pd.read_excel(xls, 'Values (FPKM)')

print('=' * 72)
print('Q1: DATA INTEGRITY')
print('=' * 72)

# 1a. Sample mapping
sample_map = dict(zip(
    meta['Sample'].str.replace('Sample_', '').astype(int),
    meta['Etiology']
))
fm = sorted([s for s, e in sample_map.items() if e == 'Fibromyalgia'])
hc = sorted([s for s, e in sample_map.items() if e == 'Control'])
other = {s: e for s, e in sample_map.items() if e not in ('Fibromyalgia', 'Control')}
print(f'FM samples: {len(fm)} | HC samples: {len(hc)} | otros: {len(other)}')
assert len(fm) == 96 and len(hc) == 93, 'CONTAJE DISTINTO AL CLAIM'

# 1b. ¿Coinciden las columnas del xlsx con los samples mapeados?
sample_cols = [c for c in values.columns if str(c).startswith('Sample_')]
col_nums = sorted(int(str(c).replace('Sample_', '')) for c in sample_cols)
mapped_nums = sorted(sample_map.keys())
print(f'Columnas Sample_ en Values: {len(col_nums)} | samples mapeados: {len(mapped_nums)}')
print(f'Columnas sin metadata: {set(col_nums) - set(mapped_nums)}')
print(f'Metadata sin columna: {set(mapped_nums) - set(col_nums)}')

# 1c. Outliers (>3 SD) por gen y grupo
GENES = ['IL6', 'PENK', 'LGALS3BP', 'MDH1', 'PCSK1N']
def get_expr(gene):
    row = values[values['Hugo_Gene_Symbol'].str.upper() == gene.upper()]
    assert len(row) == 1, f'{gene}: {len(row)} filas'
    r = row.iloc[0]
    return {int(str(c).replace('Sample_', '')): float(r[c]) for c in sample_cols}

print('\n-- Outliers (>3 SD) por gen/grupo --')
for g in GENES:
    expr = get_expr(g)
    for name, grp in [('FM', fm), ('HC', hc)]:
        v = np.array([expr[s] for s in grp])
        mean, sd = v.mean(), v.std()
        n_out = int((np.abs(v - mean) > 3 * sd).sum())
        print(f'  {g:9s} {name}: n={len(v)}, mean={mean:.4f}, sd={sd:.4f}, outliers={n_out}')

print()
print('=' * 72)
print('Q2 + Q5: STATISTICAL ROBUSTNESS & EFFECT SIZE (IL6, PENK, LGALS3BP, MDH1, PCSK1N)')
print('=' * 72)

N_GENES_TESTED = 12  # los 10 de Wray + IL6 + PENK (como en el script original)
results = []
for g in GENES:
    expr = get_expr(g)
    fm_v = np.array([expr[s] for s in fm], dtype=float)
    hc_v = np.array([expr[s] for s in hc], dtype=float)
    fc = fm_v.mean() / hc_v.mean() if hc_v.mean() > 0 else float('inf')

    # normalidad
    sh_fm = stats.shapiro(fm_v)
    sh_hc = stats.shapiro(hc_v)

    # paramétrico (como el script) y no paramétrico
    t_stat, p_t = stats.ttest_ind(fm_v, hc_v)
    u_stat, p_u = stats.mannwhitneyu(fm_v, hc_v, alternative='two-sided')

    # Bonferroni (n=12 genes)
    p_t_bonf = min(1.0, p_t * N_GENES_TESTED)
    p_u_bonf = min(1.0, p_u * N_GENES_TESTED)

    # Cohen's d (pooled)
    n1, n2 = len(fm_v), len(hc_v)
    sp = np.sqrt(((n1 - 1) * fm_v.std(ddof=1) ** 2 + (n2 - 1) * hc_v.std(ddof=1) ** 2) / (n1 + n2 - 2))
    d = (fm_v.mean() - hc_v.mean()) / sp if sp > 0 else float('inf')

    results.append({
        'gene': g, 'FC': fc, 'p_t': p_t, 'p_u': p_u,
        'p_t_bonf': p_t_bonf, 'p_u_bonf': p_u_bonf,
        'shapiro_fm': sh_fm.pvalue, 'shapiro_hc': sh_hc.pvalue,
        'cohen_d': d, 'fm_mean': fm_v.mean(), 'hc_mean': hc_v.mean()
    })
    print(f'\n{g}:')
    print(f'  FC={fc:.3f} (FM {fm_v.mean():.4f} vs HC {hc_v.mean():.4f})')
    print(f'  t-test: p={p_t:.4f} | Bonferroni x{N_GENES_TESTED}: {p_t_bonf:.4f}')
    print(f'  Mann-Whitney: p={p_u:.4f} | Bonferroni x{N_GENES_TESTED}: {p_u_bonf:.4f}')
    print(f'  Shapiro-Wilk: FM p={sh_fm.pvalue:.2e} ({"NO normal" if sh_fm.pvalue < 0.05 else "normal"}), HC p={sh_hc.pvalue:.2e} ({"NO normal" if sh_hc.pvalue < 0.05 else "normal"})')
    print(f'  Cohen d={d:.3f} -> {"large" if abs(d) >= 0.8 else "medium" if abs(d) >= 0.5 else "small"}')

print()
print('=' * 72)
print('Q2b: AUC HONESTA — 2-gene model (IL6+PENK) y full panel')
print('      (script original: AUC in-sample => sesgo optimista)')
print('=' * 72)

# Reproducir el análisis del script para IL6+PENK
X2 = np.column_stack([get_expr('IL6'), get_expr('PENK')])
X2 = np.array([[expr[s] for s in fm + hc] for expr in [get_expr('IL6'), get_expr('PENK')]]).T
y = np.array([1] * len(fm) + [0] * len(hc))

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X2, y)
auc_insample = roc_auc_score(y, model.predict_proba(X2)[:, 1])

# AUC out-of-fold (honesta)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
oof = np.zeros(len(y))
for tr, te in skf.split(X2, y):
    m = LogisticRegression(max_iter=1000, random_state=42)
    m.fit(X2[tr], y[tr])
    oof[te] = m.predict_proba(X2[te])[:, 1]
auc_oof = roc_auc_score(y, oof)
cv_acc = cross_val_score(LogisticRegression(max_iter=1000, random_state=42), X2, y, cv=5, scoring='accuracy')

print(f'2-gene IL6+PENK:')
print(f'  AUC in-sample (como reportó el script): {auc_insample:.4f}')
print(f'  AUC out-of-fold (honesta): {auc_oof:.4f}')
print(f'  CV accuracy: {cv_acc.mean():.4f} ± {cv_acc.std():.4f}')
print(f'  Delta (sesgo optimista): {auc_insample - auc_oof:.4f}')

print()
print('=' * 72)
print('Q4: LGALS3BP DISCORDANCIA — recalculada')
print('=' * 72)
expr = get_expr('LGALS3BP')
fm_v = np.array([expr[s] for s in fm], dtype=float)
hc_v = np.array([expr[s] for s in hc], dtype=float)
fc = fm_v.mean() / hc_v.mean()
t_stat, p_t = stats.ttest_ind(fm_v, hc_v)
u_stat, p_u = stats.mannwhitneyu(fm_v, hc_v)
print(f'LGALS3BP: FC={fc:.3f} (FM {fm_v.mean():.4f} vs HC {hc_v.mean():.4f})')
print(f'  t-test p={p_t:.4f} | Mann-Whitney p={p_u:.4f}')
print(f'  Claim original (sesión): FC=0.75, p=0.034')
print(f'  Reproducible? FC={"SI" if abs(fc-0.75) < 0.05 else "NO"} | p={"SI" if abs(p_t-0.034) < 0.01 else "NO"}')
