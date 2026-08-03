#!/usr/bin/env python3
"""
Pipeline de análisis para datos Olink NPX — Validación de proxies FM

Uso (cuando existan datos Olink):
    python3 analyze_olink_npx.py --npx samples.npx.csv --metadata metadata.csv \
        --targets IL6 PENK IL8 --group_col Group

Formato NPX Olink estándar (PRIDE/UKB):
    - Una fila por (assay, sample) o matriz wide con columnas = assays
    - NPX = Normalized Protein eXpression (log2-like, ya normalizado)
    - Metadata: columna de grupo (FM/Control), opcional columna CSF para correlación

Método (post adversarial verification 2026-08-03):
    - Mann-Whitney U (NPX no es normal) + Bonferroni sobre N targets
    - Cohen's d pooled (effect size)
    - AUC out-of-fold honesta (StratifiedKFold) — no in-sample
    - Correlación CSF↔plasma (Pearson) si hay pares
    - Veredicto por proxy: significativo + dirección + magnitud

Referencia: ADVERSARIAL_VERIFICATION_REPORT_2026-08-03.md (mismos fixes que GSE221921)
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score


def cohens_d(a, b):
    n1, n2 = len(a), len(b)
    sp = np.sqrt(((n1 - 1) * a.std(ddof=1) ** 2 + (n2 - 1) * b.std(ddof=1) ** 2) / (n1 + n2 - 2))
    return (a.mean() - b.mean()) / sp if sp > 0 else float('inf')


def auc_oof(X, y, seed=42):
    """AUC honesta out-of-fold (evita sesgo optimista de AUC in-sample)."""
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    oof = np.zeros(len(y))
    for tr, te in skf.split(X, y):
        m = LogisticRegression(max_iter=1000, random_state=seed)
        m.fit(X[tr], y[tr])
        oof[te] = m.predict_proba(X[te])[:, 1]
    if len(np.unique(y)) < 2:
        return float('nan')
    return roc_auc_score(y, oof)


def main():
    ap = argparse.ArgumentParser(description='Análisis Olink NPX — proxies FM')
    ap.add_argument('--npx', required=True, help='CSV NPX (wide: filas=samples, cols=assays)')
    ap.add_argument('--metadata', required=True, help='CSV metadata (sample_id, group, opcional csf_value)')
    ap.add_argument('--targets', nargs='+', required=True, help='Assays/proteínas objetivo (ej: IL6 PENK IL8)')
    ap.add_argument('--group_col', default='Group', help='Columna de grupo en metadata')
    ap.add_argument('--fm_label', default='FM', help='Etiqueta del grupo casos')
    ap.add_argument('--hc_label', default='Control', help='Etiqueta del grupo control')
    ap.add_argument('--sample_col', default='Sample', help='Columna ID de sample en metadata')
    ap.add_argument('--csf_col', default=None, help='Opcional: columna con valor CSF del mismo sujeto')
    ap.add_argument('--out', default='olink_validation_report.md', help='Reporte de salida')
    args = ap.parse_args()

    npx = pd.read_csv(args.npx)
    meta = pd.read_csv(args.metadata)

    # Alinear por sample
    assert args.sample_col in meta.columns, f'Falta {args.sample_col} en metadata'
    samples = meta[args.sample_col].astype(str).tolist()
    npx_idx = npx.iloc[:, 0].astype(str)
    if not set(samples).issubset(set(npx_idx)):
        # intentar columna 'Sample' explícita
        if 'Sample' in npx.columns:
            npx_idx = npx['Sample'].astype(str)
    npx = npx.set_index(npx_idx)

    groups = meta.set_index(meta[args.sample_col].astype(str))[args.group_col]
    fm_mask = (groups == args.fm_label).values
    hc_mask = (groups == args.hc_label).values
    print(f'Samples: {fm_mask.sum()} {args.fm_label} vs {hc_mask.sum()} {args.hc_label}')

    y = np.array([1 if g == args.fm_label else 0 for g in groups.values], dtype=int)
    n_targets = len(args.targets)

    rows = []
    print(f'\n=== Proxies ({n_targets} targets, Bonferroni x{n_targets}) ===')
    for t in args.targets:
        if t not in npx.columns:
            print(f'  [WARN] {t} no está en el CSV NPX — omitido')
            continue
        v = npx[t].astype(float).values[:len(groups)]
        fm_v = v[fm_mask]
        hc_v = v[hc_mask]
        fc = fm_v.mean() / hc_v.mean() if hc_v.mean() != 0 else float('inf')
        u_stat, p_u = stats.mannwhitneyu(fm_v, hc_v, alternative='two-sided')
        p_bonf = min(1.0, p_u * n_targets)
        d = cohens_d(fm_v, hc_v)
        auc = auc_oof(v.reshape(-1, 1), y)
        if p_bonf < 0.05 and abs(d) >= 0.3:
            verdict = 'proxy SIGNIFICATIVO (effect small-medium)'
        elif p_bonf < 0.05:
            verdict = 'proxy SIGNIFICATIVO (effect small)'
        else:
            verdict = 'no significativo (NS)'
        rows.append({'target': t, 'fm_mean': fm_v.mean(), 'hc_mean': hc_v.mean(),
                     'FC': fc, 'MWU_p': p_u, 'Bonf': p_bonf, 'cohen_d': d, 'AUC_oof': auc,
                     'verdict': verdict})
        print(f'  {t:8s} FM={fm_v.mean():8.3f} HC={hc_v.mean():8.3f} FC={fc:6.3f} '
              f'MWU_p={p_u:.4f} Bonf={p_bonf:.4f} d={d:+.3f} AUC={auc:.3f} | {verdict}')

    # Correlación CSF↔plasma si hay pares
    csf_note = ''
    if args.csf_col and args.csf_col in meta.columns:
        print('\n=== Correlación CSF↔plasma ===')
        csf_lines = []
        for t in args.targets:
            if t not in npx.columns:
                continue
            sub = meta[[args.sample_col, args.csf_col]].dropna()
            if len(sub) < 10:
                csf_lines.append(f'| {t} | n<10 insuficiente | — |')
                continue
            plasma_v = npx.loc[sub[args.sample_col].astype(str), t].astype(float).values
            csf_v = sub[args.csf_col].astype(float).values
            r, p_corr = stats.pearsonr(plasma_v, csf_v)
            csf_lines.append(f'| {t} | r={r:.3f} | p={p_corr:.4f} |')
            print(f'  {t}: r={r:.3f}, p={p_corr:.4f}')
        csf_note = '\n### Correlación CSF↔plasma\n| Target | r | p |\n|--------|-----|-----|\n' + '\n'.join(csf_lines)

    # Reporte
    md = f'''# Olink NPX Validation Report — Proxies FM

**Fecha:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
**Input:** {os.path.basename(args.npx)} + {os.path.basename(args.metadata)}
**Método:** Mann-Whitney U + Bonferroni ×{n_targets} | Cohen's d | AUC out-of-fold (5-fold)

### Proxies
| Target | FM mean | HC mean | FC | MWU p | Bonf ×{n_targets} | Cohen d | AUC OOF | Veredicto |
|--------|---------|---------|-----|-------|--------------------|---------|---------|-----------|
'''
    for r in rows:
        md += (f"| {r['target']} | {r['fm_mean']:.3f} | {r['hc_mean']:.3f} | {r['FC']:.3f} | "
               f"{r['MWU_p']:.4f} | {r['Bonf']:.4f} | {r['cohen_d']:+.3f} | {r['AUC_oof']:.3f} | {r['verdict']} |\n")
    md += '\n' + csf_note + '\n'
    md += '''
### Interpretación
- NPX es log2-like: FC > 1.2 ya es biológicamente relevante en Olink.
- AUC OOF ≈ 0.5-0.6 individual = NO sirve para diagnóstico individual; valor como proxy de mecanismo.
- Declarar siempre: significativo ≠ clínicamente grande (ver Cohen's d).
'''
    with open(args.out, 'w') as f:
        f.write(md)
    print(f'\n✅ Reporte: {args.out}')


if __name__ == '__main__':
    main()
