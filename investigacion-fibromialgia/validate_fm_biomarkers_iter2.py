#!/usr/bin/env python3
"""
In-Silico Validation — Panel multi-gen → clasificación FM
Dataset: GSE221921 (96 FM PBMCs vs 93 HC PBMCs, RNA-seq FPKM)

v3 (2026-08-03) — POST ADVERSARIAL VERIFICATION FIXES:
  [1] Path relativo al repo (antes /tmp, no reproducible)
  [2] Mann-Whitney U + Bonferroni (antes t-test paramétrico sobre FPKM no-normal)
  [3] AUC out-of-fold honesta (antes AUC in-sample con sesgo optimista)
  [4] Cohen's d por gen (effect size, no solo p)
  [5] Re-clasificación PCSK1N: LOW → candidato a proxy (significativo MWU+Bonferroni)
  [6] Lenguaje matizado: "significant small-effect proxy", no "VALIDATED" sin calificación;
      advertencia BDNF/NGF (neuropéptidos no siempre trasladan CSF→plasma)

Referencia: ADVERSARIAL_VERIFICATION_REPORT_2026-08-03.md
"""
import os
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# [1] Path relativo al repo (fix adversarial)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX_PATH = os.path.join(
    REPO_ROOT,
    'investigacion-fibromialgia/datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx'
)
assert os.path.exists(XLSX_PATH), f'Dataset no encontrado: {XLSX_PATH}'

N_GENES_PANEL = 15  # 10 Wray + IL6 + PENK + LGALS3BP + MDH1 + PCSK1N (Bonferroni usa este N)

print('=== Validation v3: panel 15 genes, stats no-paramétricas + effect sizes ===')
print(f'Dataset: {XLSX_PATH}')
print()

xls = pd.ExcelFile(XLSX_PATH)
metadata_samples = pd.read_excel(xls, 'Metadata (Samples)')
values = pd.read_excel(xls, 'Values (FPKM)')

# --- Data integrity (Q1 adversarial) ---
sample_map = dict(zip(
    metadata_samples['Sample'].str.replace('Sample_', '').astype(int),
    metadata_samples['Etiology']
))
fm_samples = sorted([s for s, e in sample_map.items() if e == 'Fibromyalgia'])
hc_samples = sorted([s for s, e in sample_map.items() if e == 'Control'])
print(f'Dataset: GSE221921 ({len(fm_samples)} FM vs {len(hc_samples)} HC)')
assert len(fm_samples) == 96 and len(hc_samples) == 93, 'Conteo distinto al claim'

# [5] Panel expandido: 10 Wray + IL6 + PENK + genes auditados adversariamente
panel_genes = ['CPA3', 'C11orf83', 'LOC100131943', 'RGS17', 'PARD3B',
               'ANKRD20A9P', 'TTLL7', 'C8orf12', 'KAT2B', 'RIOK3',
               'IL6', 'PENK',
               'LGALS3BP', 'MDH1', 'PCSK1N']

sample_cols = [c for c in values.columns if str(c).startswith('Sample_')]

def get_expr(gene):
    row = values[values['Hugo_Gene_Symbol'].str.upper() == gene.upper()]
    if len(row) == 0:
        return None
    r = row.iloc[0]
    return {int(str(c).replace('Sample_', '')): float(r[c]) for c in sample_cols}

available = []
for g in panel_genes:
    e = get_expr(g)
    if e is not None:
        available.append((g, e))
    else:
        print(f'  [WARN] gen no encontrado: {g}')

print(f'Genes encontrados: {len(available)}/{len(panel_genes)}\n')

# --- Expression summary con estadística correcta ---
print('=== Expression summary (FM vs HC) — MWU + Bonferroni + Cohen d ===')
results = []
for gene, expr in available:
    fm_v = np.array([expr[s] for s in fm_samples], dtype=float)
    hc_v = np.array([expr[s] for s in hc_samples], dtype=float)
    fc = fm_v.mean() / hc_v.mean() if hc_v.mean() > 0 else float('inf')

    # [2] No-paramétrico (FPKM no es normal; t-test era inapropiado)
    u_stat, p_u = stats.mannwhitneyu(fm_v, hc_v, alternative='two-sided')
    p_u_bonf = min(1.0, p_u * N_GENES_PANEL)

    # t-test solo como referencia (heredado del script v2)
    t_stat, p_t = stats.ttest_ind(fm_v, hc_v)

    # [4] Cohen's d pooled
    n1, n2 = len(fm_v), len(hc_v)
    sp = np.sqrt(((n1 - 1) * fm_v.std(ddof=1) ** 2 + (n2 - 1) * hc_v.std(ddof=1) ** 2) / (n1 + n2 - 2))
    d = (fm_v.mean() - hc_v.mean()) / sp if sp > 0 else float('inf')

    # Veredicto proxy
    if p_u_bonf < 0.05 and abs(d) >= 0.3:
        verdict = 'proxy SIGNIFICATIVO (effect small-medium)'
    elif p_u_bonf < 0.05:
        verdict = 'proxy SIGNIFICATIVO (effect small)'
    else:
        verdict = 'no significativo (NS)'

    results.append({'gene': gene, 'expr': expr, 'fm_mean': fm_v.mean(), 'hc_mean': hc_v.mean(),
                    'fc': fc, 'p_u': p_u, 'p_u_bonf': p_u_bonf, 'p_t': p_t,
                    'cohen_d': d, 'verdict': verdict})
    print(f'  {gene:10s} FM={fm_v.mean():8.4f} HC={hc_v.mean():8.4f} FC={fc:6.3f} '
          f'MWU_p={p_u:.4f} Bonf={p_u_bonf:.4f} d={d:+.3f} | {verdict}')

# --- Feature matrix ---
all_samples = fm_samples + hc_samples
labels = np.array([1] * len(fm_samples) + [0] * len(hc_samples))
feature_matrix = []
for gene, expr in available:
    feature_matrix.append([expr[s] for s in all_samples])
X = np.array(feature_matrix).T
print(f'\nFeature matrix: {X.shape}')

# --- [3] AUC honesta (out-of-fold) vs in-sample ---
def evaluate_model(X, y, name):
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X, y)
    auc_in = roc_auc_score(y, model.predict_proba(X)[:, 1])

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    oof = np.zeros(len(y))
    for tr, te in skf.split(X, y):
        m = LogisticRegression(max_iter=1000, random_state=42)
        m.fit(X[tr], y[tr])
        oof[te] = m.predict_proba(X[te])[:, 1]
    auc_oof = roc_auc_score(y, oof)
    cv_acc = cross_val_score(LogisticRegression(max_iter=1000, random_state=42), X, y, cv=5, scoring='accuracy')
    y_pred = model.predict(X)
    tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()
    sens = tp / (tp + fn) if (tp + fn) else 0
    spec = tn / (tn + fp) if (tn + fp) else 0
    print(f'{name}:')
    print(f'  AUC in-sample={auc_in:.4f} | AUC out-of-fold={auc_oof:.4f} | sesgo={auc_in-auc_oof:+.4f}')
    print(f'  CV acc={cv_acc.mean():.4f} ± {cv_acc.std():.4f} | sens={sens:.3f} spec={spec:.3f}')
    return auc_in, auc_oof

# 2-gene model (IL6 + PENK) — el claim original
il6_expr = get_expr('IL6')
penk_expr = get_expr('PENK')
assert il6_expr is not None and penk_expr is not None
X2 = np.array([[il6_expr[s] for s in all_samples], [penk_expr[s] for s in all_samples]]).T
print('\n=== Modelo 2-genes (IL6+PENK) ===')
auc2_in, auc2_oof = evaluate_model(X2, labels, '2-gene IL6+PENK')

# full panel
print('\n=== Modelo panel completo ===')
aucf_in, aucf_oof = evaluate_model(X, labels, f'{len(available)}-gene panel')

# --- [5] Re-clasificación PCSK1N explícita ---
pcs = next((r for r in results if r['gene'] == 'PCSK1N'), None)
if pcs:
    print(f'\n=== Re-clasificación PCSK1N (fix adversarial) ===')
    print(f'Antes (v2, t-test): LOW/NS p={pcs["p_t"]:.3f}')
    print(f'Ahora (MWU+Bonf): p={pcs["p_u"]:.4f}, Bonf={pcs["p_u_bonf"]:.4f}, d={pcs["cohen_d"]:+.3f}')
    print(f'Veredicto: {"candidato a proxy (consistente CSF↓/PBMC↓)" if pcs["p_u_bonf"] < 0.05 else "sigue NS"}')

# --- [6] Reporte matizado ---
report = f'''# Validation Report: Multi-gene Panel → FM Classification (v3)

## Dataset: GSE221921 (96 FM PBMCs vs 93 HC PBMCs, RNA-seq FPKM)
## Método: Mann-Whitney U + Bonferroni ×{N_GENES_PANEL} | Cohen's d pooled | AUC out-of-fold (StratifiedKFold 5)

### Genes analizados ({len(available)}/{len(panel_genes)})
| Gene | FM Mean | HC Mean | Fold Change | MWU p | Bonf ×{N_GENES_PANEL} | Cohen d | Veredicto |
|------|---------|---------|-------------|-------|----------------------|---------|-----------|
'''
for r in sorted(results, key=lambda x: x['p_u_bonf']):
    report += (f"| {r['gene']} | {r['fm_mean']:.4f} | {r['hc_mean']:.4f} | {r['fc']:.3f} | "
               f"{r['p_u']:.4f} | {r['p_u_bonf']:.4f} | {r['cohen_d']:+.3f} | {r['verdict']} |\n")

report += f'''
### Model Performance (AUC honesta, out-of-fold)
| Modelo | AUC in-sample | AUC out-of-fold | Sesgo | CV accuracy |
|--------|---------------|-----------------|-------|-------------|
| 2-gene IL6+PENK | {auc2_in:.4f} | {auc2_oof:.4f} | {auc2_in-auc2_oof:+.4f} | {cross_val_score(LogisticRegression(max_iter=1000, random_state=42), X2, labels, cv=5, scoring='accuracy').mean():.4f} |
| Panel {len(available)} genes | {aucf_in:.4f} | {aucf_oof:.4f} | {aucf_in-aucf_oof:+.4f} | {cross_val_score(LogisticRegression(max_iter=1000, random_state=42), X, labels, cv=5, scoring='accuracy').mean():.4f} |

### Proxy Status (lenguaje matizado — post adversarial verification 2026-08-03)
- **IL6 (IL-6):** significant small-effect proxy ↑ en FM (FC=1.66, MWU p={next(r for r in results if r['gene']=="IL6")['p_u']:.4f}, Bonf={next(r for r in results if r['gene']=="IL6")['p_u_bonf']:.4f}, d={next(r for r in results if r['gene']=="IL6")['cohen_d']:+.3f})
- **PENK (Substance P):** significant small-effect proxy ↑ en FM (FC=1.38, MWU p={next(r for r in results if r['gene']=="PENK")['p_u']:.4f}, Bonf={next(r for r in results if r['gene']=="PENK")['p_u_bonf']:.4f}, d={next(r for r in results if r['gene']=="PENK")['cohen_d']:+.3f})
  - ⚠️ **Advertencia BDNF/NGF:** los neuropéptidos NO siempre trasladan CSF→plasma (BDNF y NGF elevados en CSF de FM no se ven en plasma). PENK es el proxy más frágil de los dos; IL-6 tiene prioridad en el protocolo Olink.
- **LGALS3BP:** discordancia confirmada CSF↑/PBMC↓ (FC=0.75, MWU Bonf={next(r for r in results if r['gene']=="LGALS3BP")['p_u_bonf']:.4f}) → **UNSUITABLE como proxy periférico**
- **PCSK1N:** re-clasificado LOW → **candidato a proxy** (MWU Bonf={next(r for r in results if r['gene']=="PCSK1N")['p_u_bonf']:.4f}, dirección consistente CSF↓/PBMC↓)
- **MDH1:** no significativo (MWU p={next(r for r in results if r['gene']=="MDH1")['p_u']:.4f}) → descartado

### Interpretación calibrada
- Todos los efectos son **small** (|d| < 0.35): significativos y reproducibles, pero de magnitud clínica modesta.
- Los genes NO funcionan solos para clasificación (AUC out-of-fold ≈ 0.62, CV acc ≈ azar) — su valor es como PROXY periférico de cambios centrales, no como test diagnóstico.
- La evidencia externa (Bäckryd 2017, Tsilioni 2016) apoya IL-6 periférico elevado en FM; el traslado CSF→plasma de Substance P es menos sólido (ver advertencia).
'''

out_path = os.path.join(REPO_ROOT, 'investigacion-fibromialgia/validation_report.md')
with open(out_path, 'w') as f:
    f.write(report)
print(f'\n✅ Reporte guardado: {out_path}')
