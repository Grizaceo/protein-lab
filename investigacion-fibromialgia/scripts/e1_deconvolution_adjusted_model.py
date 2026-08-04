#!/usr/bin/env python3
"""
E1 (reconstruido) — modelo ajustado por composicion celular, GSE221921.

CONTEXTO: el commit 03b4609 ("exp: E1 — deconvolucion eje opioide GSE221921")
anadio SOLO el CSV analisis/E1_deconvolution_opioid_axis.csv, sin codigo. Este
script reconstruye la metodologia, la valida contra ese CSV, y la extiende al
modulo COL9A1/PTN, que nunca fue probado bajo ajuste composicional.

Modelos anidados sobre log2(FPKM+1):
  M1  expr ~ grupo
  M2  expr ~ grupo + sexo
  M3  expr ~ grupo + sexo + fracciones celulares       <- p_full_adj

Las fracciones son los scores de marcadores normalizados de
scripts/deconvolution_cell_types.py (score_signature_enrichment), que suman 1
por muestra. Al ser composicionales se descarta un tipo celular como referencia
para evitar colinealidad perfecta.

CONTROL NEGATIVO (bloque 3): el mismo modelo aplicado a genes al azar con un
efecto de grupo comparable antes de ajustar. Si casi ningun gen sobrevive M3,
la "muerte" del eje opioide es sobreajuste, no biologia.

BARRIDO DE VARIANTES (bloque 4): el veredicto no debe depender de como se
estiman las fracciones. Se cruzan 2 estimadores (NNLS canonico del repo vs
marker-scores recalculados) x 2 codificaciones (descartar referencia vs las 12),
y se reporta VIF.
"""

import pathlib
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif

warnings.filterwarnings('ignore')

REPO = pathlib.Path(__file__).resolve().parent.parent
XLSX = REPO / 'datos' / 'geo' / 'PBMC_FM_96patients_93controls' / 'GSE221921_FM_ProcessedData.xlsx'
E1_REF = REPO / 'analisis' / 'E1_deconvolution_opioid_axis.csv'
OUT = REPO / 'analisis' / 'E1b_deconvolution_col9a1_ptn.csv'
OUT_NULL = REPO / 'analisis' / 'E1b_negative_control_random_genes.csv'

SEED = 20260804

# Mismos marcadores que scripts/deconvolution_cell_types.py
CELL_MARKERS = {
    'B_cells': ['CD19', 'CD79A', 'MS4A1', 'FCER2', 'TCL1A', 'CD22'],
    'T_cells_CD4': ['CD4', 'IL7R', 'CCR7', 'LEF1', 'TCF7', 'SELL'],
    'T_cells_CD8': ['CD8A', 'CD8B', 'GZMK', 'GZMA', 'NKG7', 'GZMB'],
    'T_cells_Treg': ['FOXP3', 'IL2RA', 'CTLA4', 'TIGIT', 'IKZF2'],
    'NK_cells': ['NCAM1', 'NKG7', 'KLRD1', 'KLRB1', 'GNLY', 'GZMH'],
    'Monocytes': ['CD14', 'LYZ', 'S100A8', 'S100A9', 'FCGR3A', 'CD68'],
    'Dendritic_cells': ['CD1C', 'FCER1A', 'HLA-DRA', 'HLA-DRB1', 'ITGAX'],
    'Neutrophils': ['CSF3R', 'FCGR3B', 'CXCR2', 'S100A12', 'MMP9', 'ELANE'],
    'Eosinophils': ['SIGLEC8', 'CLC', 'PRG2', 'PRG3', 'EPX'],
    'Basophils': ['MS4A2', 'FCER1A', 'CPA3', 'HDC', 'GATA2'],
    'Mast_cells': ['CPA3', 'MS4A2', 'FCER1A', 'HDC', 'TPSAB1', 'TPSB2', 'KIT'],
    'Platelets': ['ITGA2B', 'GP1BA', 'PF4', 'PPBP', 'SELP'],
}

OPIOID_AXIS = ['OPRM1', 'OPRK1', 'OPRD1', 'TACR1', 'TAC1', 'PENK', 'POMC']
ECM_MODULE = ['COL9A1', 'PTN']


def load():
    """Devuelve (expr log2(FPKM+1) genes x muestras, metadata alineada)."""
    xls = pd.ExcelFile(XLSX)
    raw = pd.read_excel(xls, sheet_name='Values (FPKM)', index_col=0)
    meta_cols = ['Hugo_Gene_Symbol', 'Gene_Description', 'Chromosome/scaffold name',
                 'Gene start (bp)', 'Gene end (bp)', 'Strand', 'Karyotype band']
    hugo = raw[raw.columns[0]]
    sample_cols = [c for c in raw.columns if c not in meta_cols]

    expr = raw[sample_cols].copy()
    expr.index = expr.index.map(lambda x: hugo.get(x, ''))
    expr = expr[expr.index != '']
    expr = expr.apply(pd.to_numeric, errors='coerce')

    # duplicados: conservar el de mayor expresion media (igual que el script base)
    order = expr.mean(axis=1).sort_values(ascending=False).index
    expr = expr.loc[order]
    expr = expr[~expr.index.duplicated(keep='first')]

    sm_meta = pd.read_excel(xls, sheet_name='Metadata (Samples)').set_index('Sample')
    keep = [c for c in expr.columns if str(c) in sm_meta.index]
    expr = expr[keep]
    md = sm_meta.loc[[str(c) for c in keep]]

    design = pd.DataFrame({
        'group': (md['Etiology'].astype(str).str.lower().str.contains('fibro')).astype(int).values,
        'sex_f': (md['Gender'].astype(str).str.lower().str.startswith('f')).astype(int).values,
    }, index=[str(c) for c in keep])

    return np.log2(expr + 1), design


def cell_scores(expr_log):
    """Scores de marcadores normalizados (suman 1 por muestra)."""
    sc = pd.DataFrame(index=expr_log.columns, dtype=float)
    for ct, markers in CELL_MARKERS.items():
        present = [m for m in markers if m in expr_log.index]
        sc[ct] = expr_log.loc[present].mean(axis=0) if present else 0.0
    sc.index = [str(i) for i in sc.index]
    return sc.div(sc.sum(axis=1), axis=0)


def fit_gene(y, design, frac):
    """Ajusta M1/M2/M3 y devuelve el registro con la semantica de E1."""
    out = {}
    X1 = sm.add_constant(design[['group']])
    out['p_group_only'] = sm.OLS(y, X1).fit().pvalues['group']

    X2 = sm.add_constant(design[['group', 'sex_f']])
    out['p_group_sex'] = sm.OLS(y, X2).fit().pvalues['group']

    X3 = sm.add_constant(pd.concat([design[['group', 'sex_f']], frac], axis=1))
    m3 = sm.OLS(y, X3).fit()
    out['p_full_adj'] = m3.pvalues['group']
    out['beta_group_full'] = m3.params['group']

    cell_p = m3.pvalues[frac.columns]
    out['top_cell_type'] = cell_p.idxmin()
    out['top_cell_p'] = cell_p.min()
    out['survives'] = 'SI' if out['p_full_adj'] < 0.05 else 'NO'
    return out


def report(genes, expr_log, design, frac, title):
    print(f"\n{'='*94}\n{title}\n{'='*94}")
    print(f"{'gen':10}{'M1 p_grupo':>13}{'M2 +sexo':>12}{'M3 +celulas':>14}"
          f"{'beta':>9}{'tipo celular top':>20}{'sobrevive':>12}")
    print('-' * 94)
    rows = []
    for g in genes:
        if g not in expr_log.index:
            print(f"{g:10}  AUSENTE DE LA MATRIZ")
            continue
        r = fit_gene(expr_log.loc[g].values.astype(float), design, frac)
        r['Gene'] = g
        rows.append(r)
        print(f"{g:10}{r['p_group_only']:13.2e}{r['p_group_sex']:12.2e}"
              f"{r['p_full_adj']:14.3f}{r['beta_group_full']:+9.3f}"
              f"{r['top_cell_type']:>20}{r['survives']:>12}")
    return pd.DataFrame(rows)


def main():
    if not XLSX.exists():
        sys.exit(f"FALTA la matriz: {XLSX}\nDescargala de GEO (ver README.md, seccion 'Data Download').")

    expr_log, design = load()
    frac_all = cell_scores(expr_log).loc[design.index]

    # compositional: descartar el tipo de mayor media como referencia
    ref = frac_all.mean().idxmax()
    frac = frac_all.drop(columns=[ref])
    print(f"Matriz: {expr_log.shape[0]} genes x {expr_log.shape[1]} muestras "
          f"| FM={int(design['group'].sum())} HC={int((1-design['group']).sum())}")
    print(f"Fracciones celulares: {frac_all.shape[1]} tipos, referencia descartada = {ref}")

    # ---- 1. validacion contra E1 ----
    df_axis = report(OPIOID_AXIS, expr_log, design, frac,
                     "[1] VALIDACION — eje opioide (reproduce E1, commit 03b4609)")

    if E1_REF.exists():
        ref_df = pd.read_csv(E1_REF).set_index('Gene')
        merged = df_axis.set_index('Gene').join(ref_df, rsuffix='_E1')
        agree = ((merged['p_full_adj'] < 0.05) == (merged['p_full_adj_E1'] < 0.05)).sum()
        rho = merged[['p_full_adj', 'p_full_adj_E1']].corr(method='spearman').iloc[0, 1]
        print(f"\n  Concordancia con E1: {agree}/{len(merged)} genes con el mismo veredicto"
              f" | rho(Spearman) de p_full_adj = {rho:.3f}")

    # ---- 2. la pregunta: COL9A1 / PTN ----
    df_ecm = report(ECM_MODULE, expr_log, design, frac,
                    "[2] NUEVO — modulo ECM/neurita COL9A1-PTN (nunca probado bajo E1)")

    pd.concat([df_axis, df_ecm]).to_csv(OUT, index=False)

    # ---- 3. control negativo: ¿cuanto destruye el ajuste? ----
    print(f"\n{'='*94}\n[3] CONTROL NEGATIVO — ¿el modelo M3 mata todo indiscriminadamente?"
          f"\n{'='*94}")
    marker_genes = {m for ms in CELL_MARKERS.values() for m in ms}
    expressed = expr_log[(expr_log > 0).sum(axis=1) >= 0.5 * expr_log.shape[1]]
    pool = [g for g in expressed.index if g not in marker_genes]

    rng = np.random.default_rng(SEED)
    sample = list(rng.choice(pool, size=min(600, len(pool)), replace=False))

    recs = []
    for g in sample:
        try:
            r = fit_gene(expr_log.loc[g].values.astype(float), design, frac)
        except Exception:
            continue
        r['Gene'] = g
        recs.append(r)
    null_df = pd.DataFrame(recs)
    null_df.to_csv(OUT_NULL, index=False)

    sig2 = null_df[null_df['p_group_sex'] < 0.05]
    surv = (sig2['p_full_adj'] < 0.05).sum()
    print(f"  Genes al azar evaluados: {len(null_df)} (marcadores excluidos)")
    print(f"  Con efecto de grupo tras ajustar por sexo (M2 p<0.05): {len(sig2)}")
    if len(sig2):
        print(f"  De esos, sobreviven M3 (+composicion celular): {surv}/{len(sig2)} "
              f"= {100*surv/len(sig2):.0f}%")
        print(f"  Mediana p_full_adj en ese subconjunto: {sig2['p_full_adj'].median():.3f}")
    # ---- 4. barrido de variantes de implementacion ----
    print(f"\n{'='*94}\n[4] BARRIDO DE VARIANTES — ¿el veredicto depende de como se estiman"
          f" las fracciones?\n{'='*94}")
    nnls_path = REPO / 'analisis' / 'deconvolution' / 'gse221921_cell_fractions.csv'
    variants = {}
    sources = [('scores', frac_all)]
    if nnls_path.exists():
        nn = pd.read_csv(nnls_path, index_col=0)
        nn.index = [str(i) for i in nn.index]
        sources.insert(0, ('NNLS', nn.loc[design.index]))

    for src_name, src in sources:
        for drop_ref in (True, False):
            F = src.drop(columns=[src.mean().idxmax()]) if drop_ref else src
            key = f"{src_name}/{'ref-drop' if drop_ref else 'las-12'}"
            variants[key] = {}
            for g in OPIOID_AXIS + ECM_MODULE:
                X = sm.add_constant(pd.concat([design[['group', 'sex_f']], F], axis=1))
                variants[key][g] = sm.OLS(expr_log.loc[g].values.astype(float), X).fit().pvalues['group']

    print(f"{'gen':9}{'E1 pub':>9}", end='')
    for k in variants:
        print(f"{k:>18}", end='')
    print(f"{'veredicto':>18}")
    print('-' * (9 + 9 + 18 * len(variants) + 18))
    ref_df = pd.read_csv(E1_REF).set_index('Gene') if E1_REF.exists() else pd.DataFrame()
    rows = []
    for g in OPIOID_AXIS + ECM_MODULE:
        ps = [variants[k][g] for k in variants]
        n = sum(p < 0.05 for p in ps)
        tag = f'SOBREVIVE {n}/{len(ps)}' if n == len(ps) else (
            f'muere 0/{len(ps)}' if n == 0 else f'inestable {n}/{len(ps)}')
        e1v = ref_df.loc[g, 'p_full_adj'] if g in ref_df.index else np.nan
        print(f"{g:9}{e1v:9.3f}" if not np.isnan(e1v) else f"{g:9}{'--':>9}", end='')
        for p in ps:
            print(f"{p:18.3f}", end='')
        print(f"{tag:>18}")
        rows.append({'Gene': g, 'p_E1_publicado': e1v,
                     **{k: variants[k][g] for k in variants}, 'veredicto': tag})
    pd.DataFrame(rows).to_csv(REPO / 'analisis' / 'E1b_variant_sweep.csv', index=False)

    if not ref_df.empty:
        print("\n  ¿que variante reproduce E1? (veredictos identicos sobre el eje opioide)")
        ax = [g for g in OPIOID_AXIS if g in ref_df.index]
        for k, v in variants.items():
            agree = sum((v[g] < 0.05) == (ref_df.loc[g, 'p_full_adj'] < 0.05) for g in ax)
            print(f"    {k:22} {agree}/{len(ax)}")

    print("\n  colinealidad del bloque de fracciones (VIF):")
    for src_name, src in sources:
        F = src.drop(columns=[src.mean().idxmax()])
        Xv = sm.add_constant(pd.concat([design[['group', 'sex_f']], F], axis=1)).values
        vs = [vif(Xv, i) for i in range(1, Xv.shape[1])]
        print(f"    {src_name:14} max={max(vs):7.1f}  mediana={np.median(vs):5.1f}"
              f"   (>10 = colinealidad seria)")

    print(f"\n  Guardado: {OUT.name}, {OUT_NULL.name}, E1b_variant_sweep.csv")
    return df_axis, df_ecm, sig2, surv


if __name__ == '__main__':
    main()
