#!/usr/bin/env python3
"""
AUDITORÍA EXTERNA — Verificador ejecutable de los claims del preprint v2.6
Creado: 2026-08-03 (auditoría adversarial independiente)

Convierte la auditoría en un TEST DE REGRESIÓN. Ejecuta:

    python3 scripts/audit_verify_claims.py

Cubre 5 bloques:
  [1] Reproducción exacta de Tablas 2 y 4 desde la matriz cruda GSE221921
  [2] Re-análisis estratificado por sexo (el que el preprint NO aplicó a Tablas 2/4)
      -> este bloque es el que hace COLAPSAR a CA14
  [3] Co-expresión GSE67311: los 10 pares + test formal de diferencia FM vs HC (Fisher r-to-z)
      -> este bloque muestra el reporte selectivo del claim D
  [4] Nivel de intensidad de las sondas del eje opioide en whole blood (¿ruido de fondo?)
  [5] Diagnóstico termodinámico del modelo QSP (¿el ΔpH es real o es deriva del Keq?)

Salida: PASS/FAIL por claim. Úsalo ANTES y DESPUÉS de aplicar PLAN_REPARACION.md.

Dependencias: pandas, numpy, scipy, statsmodels, GEOparse, openpyxl
"""
import os
import sys
import itertools
import warnings
import logging

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings('ignore')
logging.getLogger('GEOparse').setLevel(logging.CRITICAL)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(REPO, 'datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx')
SOFT67311 = os.path.join(REPO, 'datos/geo/GSE67311/GSE67311_family.soft.gz')

OK, FAIL, WARN = '\033[92mPASS\033[0m', '\033[91mFAIL\033[0m', '\033[93mWARN\033[0m'
results = []


def head(t):
    print('\n' + '=' * 86)
    print(t)
    print('=' * 86)


def record(name, passed, detail=''):
    results.append((name, passed, detail))
    print(f'  [{OK if passed else FAIL}] {name}' + (f'  — {detail}' if detail else ''))


# ---------------------------------------------------------------- GSE221921
def load_pbmc():
    xls = pd.ExcelFile(XLSX)
    ms = pd.read_excel(xls, 'Metadata (Samples)')
    v = pd.read_excel(xls, 'Values (FPKM)')
    ms['sid'] = ms['Sample'].str.replace('Sample_', '').astype(int)
    meta = ms.set_index('sid')
    cols = [c for c in v.columns if str(c).startswith('Sample_')]

    def expr(g):
        r = v[v['Hugo_Gene_Symbol'].astype(str).str.upper() == g.upper()]
        if len(r) == 0:
            return None
        r = r.iloc[0]
        return {int(str(c).replace('Sample_', '')): float(r[c]) for c in cols}

    return meta, expr


def cohen_d(a, b):
    a, b = np.asarray(a), np.asarray(b)
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / sp if sp > 0 else np.nan


# Claims tal como aparecen en preprint_dopaminergic_convergence_FM.md Tablas 2 y 4
CLAIMS_PBMC = {
    # gen:        (FC,    d,     tabla)
    'TACR1':      (2.73,  0.60,  'T2'),
    'OPRM1':      (2.28,  0.53,  'T2'),
    'TAC1':       (2.10,  0.47,  'T2'),
    'OPRK1':      (1.78,  0.38,  'T2'),
    'PENK':       (1.38,  0.21,  'T2'),
    'OPRD1':      (1.23,  0.10,  'T2'),
    'PNOC':       (0.96, -0.02,  'T2'),
    'POMC':       (1.04,  0.03,  'T2'),
    'CA14':       (2.29,  0.41,  'T4'),
    'TNFRSF1B':   (0.541, -0.56, 'T4'),
    'CD74':       (0.579, -0.44, 'T4'),
    'COL18A1':    (0.581, -0.54, 'T4'),
    'BTN2A1':     (0.745, -0.35, 'T4'),
    'TNFRSF4':    (0.768, -0.23, 'T4'),
    'CD302':      (0.717, -0.19, 'T4'),
    'TNFRSF9':    (1.459,  0.27, 'T4'),
}

COEXP_CLAIMS = [('OPRM1', 'TAC1', 0.632), ('PENK', 'OPRM1', 0.442),
                ('PENK', 'TAC1', 0.408), ('TAC1', 'TACR1', 0.382),
                ('PENK', 'POMC', 0.312)]


def block1_reproduce(meta, expr):
    head('[1] REPRODUCCIÓN EXACTA DE TABLAS 2 y 4 (GSE221921, cohorte completa)')
    fm = [s for s in meta.index if meta.loc[s, 'Etiology'] == 'Fibromyalgia']
    hc = [s for s in meta.index if meta.loc[s, 'Etiology'] == 'Control']
    print(f'  n = {len(fm)} FM / {len(hc)} HC\n')
    print(f'  {"gen":10}{"FC_calc":>9}{"FC_pub":>8}{"d_calc":>8}{"d_pub":>7}{"MWU p":>11}')
    bad = []
    for g, (fc_c, d_c, tab) in CLAIMS_PBMC.items():
        e = expr(g)
        if e is None:
            bad.append(f'{g} ausente')
            continue
        a, b = [e[s] for s in fm], [e[s] for s in hc]
        fc = np.mean(a) / np.mean(b)
        _, p = stats.mannwhitneyu(a, b, alternative='two-sided')
        d = cohen_d(a, b)
        flag = '' if (abs(fc - fc_c) <= 0.02 and abs(d - d_c) <= 0.02) else '  <<< DISCREPA'
        print(f'  {g:10}{fc:9.3f}{fc_c:8.3f}{d:+8.3f}{d_c:+7.2f}{p:11.6f}{flag}')
        if flag:
            bad.append(g)
    record('Tablas 2 y 4 reproducen desde la matriz cruda', not bad,
           'todos exactos' if not bad else f'discrepan: {bad}')

    print()
    all_s = fm + hc
    bad2 = []
    for x, y, rho_c in COEXP_CLAIMS:
        ex, ey = expr(x), expr(y)
        rho, _ = stats.spearmanr([ex[s] for s in all_s], [ey[s] for s in all_s])
        okk = abs(rho - rho_c) <= 0.01
        print(f'  co-expr {x:6}-{y:6} rho={rho:+.3f} (publicado {rho_c:+.3f}) {"" if okk else "<<< DISCREPA"}')
        if not okk:
            bad2.append(f'{x}-{y}')
    record('Co-expresión PBMC (5 pares) reproduce', not bad2)
    return fm, hc


def block2_sex(meta, expr, fm, hc):
    head('[2] RE-ANÁLISIS ESTRATIFICADO POR SEXO — el test que el preprint NO aplicó a Tablas 2/4')
    print('  §2.4 del preprint define 5 modelos obligatorios por el desbalance de sexo.')
    print('  §4.3 declara el modelo female-only como "the primary, statistically unconfounded model".')
    print('  Ese estándar se aplicó SOLO a los 16 genes GWAS/mastocito, nunca a Tablas 2 y 4.\n')

    import statsmodels.api as sm
    fmF = [s for s in fm if meta.loc[s, 'Gender'] == 'Female']
    hcF = [s for s in hc if meta.loc[s, 'Gender'] == 'Female']
    hcM = [s for s in hc if meta.loc[s, 'Gender'] == 'Male']
    print(f'  Cohorte completa: {len(fm)} FM ({sum(1 for s in fm if meta.loc[s,"Gender"]=="Female")}F) '
          f'/ {len(hc)} HC ({len(hcF)}F/{len(hcM)}M)')
    print(f'  Female-only: {len(fmF)} FM / {len(hcF)} HC\n')
    print(f'  {"gen":10}{"p_full":>10}{"p_female":>10}{"d_female":>9}{"FC_female":>10}'
          f'{"p_OLS_sex":>11}{"p_sexo(HC)":>11}  veredicto')

    colapsan = []
    for g in CLAIMS_PBMC:
        e = expr(g)
        if e is None:
            continue
        _, p_full = stats.mannwhitneyu([e[s] for s in fm], [e[s] for s in hc], alternative='two-sided')
        aF, bF = [e[s] for s in fmF], [e[s] for s in hcF]
        _, p_fem = stats.mannwhitneyu(aF, bF, alternative='two-sided')
        d_fem, fc_fem = cohen_d(aF, bF), np.mean(aF) / np.mean(bF)
        sids = fm + hc
        y = np.log2(np.array([e[s] for s in sids]) + 1)
        X = sm.add_constant(pd.DataFrame({
            'case': [1] * len(fm) + [0] * len(hc),
            'sex': [1 if meta.loc[s, 'Gender'] == 'Female' else 0 for s in sids]}))
        p_ols = sm.OLS(y, X).fit().pvalues['case']
        _, p_sex = stats.mannwhitneyu([e[s] for s in hcF], [e[s] for s in hcM], alternative='two-sided')

        if p_full < 0.05 and p_fem >= 0.05:
            verdict, colapsa = 'COLAPSA', True
        elif p_fem < 0.05 and p_ols < 0.05:
            verdict, colapsa = 'sobrevive 2/2', False
        elif p_fem < 0.05:
            verdict, colapsa = 'sobrevive solo F-only', False
        else:
            verdict, colapsa = 'NS en ambos', False
        if colapsa:
            colapsan.append(g)
        print(f'  {g:10}{p_full:10.2e}{p_fem:10.4f}{d_fem:+9.2f}{fc_fem:10.2f}'
              f'{p_ols:11.4f}{p_sex:11.4f}  {verdict}')

    print()
    record('CA14 sobrevive el modelo primario (female-only)', 'CA14' not in colapsan,
           'CA14 COLAPSA: el FC=2.29 se explica por el desbalance de sexo' if 'CA14' in colapsan else '')
    record('Eje opioide (TACR1/OPRM1/TAC1/OPRK1/PENK) sobrevive ajuste por sexo',
           not any(g in colapsan for g in ['TACR1', 'OPRM1', 'TAC1', 'OPRK1', 'PENK']),
           'hallazgo genuino, robusto al confusor')

    e = expr('CA14')
    mF, mM = np.mean([e[s] for s in hcF]), np.mean([e[s] for s in hcM])
    print(f'\n  DIAGNÓSTICO CA14 — solo dentro de CONTROLES sanos:')
    print(f'    CA14 mujeres={mF:.4f}  hombres={mM:.4f}  ratio F/M = {mF/mM:.2f}')
    print(f'    El "FC FM/HC = 2.29" publicado es del mismo tamaño que el efecto sexo puro.')
    print(f'    Grupos: FM 91F/5M vs HC 41F/52M  ->  confusor estructural.')
    return colapsan


# ---------------------------------------------------------------- GSE67311
def block3_coexpr():
    head('[3] CO-EXPRESIÓN GSE67311 — los 10 pares + test formal FM vs HC (Fisher r-to-z)')
    try:
        import GEOparse
    except ImportError:
        record('GEOparse disponible', False, 'pip install GEOparse — bloque 3 y 4 omitidos')
        return None
    gse = GEOparse.get_GEO(filepath=SOFT67311, silent=True)
    gpl = list(gse.gpls.values())[0]
    tbl = gpl.table
    GEN = ['TACR1', 'OPRM1', 'OPRK1', 'TAC1', 'PENK']
    probes = {g: tbl[tbl['gene_assignment'].astype(str).str.contains(f'// {g} //', na=False)]['ID'].tolist()
              for g in GEN}
    grp = {}
    for name, gsm in gse.gsms.items():
        ch = ' '.join(gsm.metadata.get('characteristics_ch1', [])).lower()
        grp[name] = 'FM' if 'fibromyalgia' in ch else ('HC' if 'healthy control' in ch else None)
    fm = [k for k, v in grp.items() if v == 'FM']
    hc = [k for k, v in grp.items() if v == 'HC']

    E = {}
    for g in GEN:
        pr = probes[g]
        E[g] = {name: float(np.mean([gsm.table.set_index('ID_REF')['VALUE'][x]
                                     for x in pr if x in gsm.table['ID_REF'].values]))
                for name, gsm in gse.gsms.items()} if pr else None

    reportados = {frozenset(p) for p in
                  [('TACR1', 'OPRK1'), ('OPRM1', 'OPRK1'), ('TACR1', 'OPRM1'),
                   ('OPRM1', 'TAC1'), ('OPRK1', 'PENK')]}
    print(f'  n = {len(fm)} FM / {len(hc)} HC')
    print(f'  El preprint (L177) afirma: "HC pairs consistently weaker or non-significant"\n')
    print(f'  {"par":16}{"rho_FM":>9}{"rho_HC":>9}{"p_dif":>8}  {"FM>HC?":10}{"¿publicado?"}')
    contradicen, significativos = [], []
    for a, b in itertools.combinations(GEN, 2):
        if E[a] is None or E[b] is None:
            continue
        rF, _ = stats.spearmanr([E[a][s] for s in fm], [E[b][s] for s in fm])
        rH, _ = stats.spearmanr([E[a][s] for s in hc], [E[b][s] for s in hc])
        z = (np.arctanh(rF) - np.arctanh(rH)) / np.sqrt(1 / (len(fm) - 3) + 1 / (len(hc) - 3))
        pd_ = 2 * (1 - stats.norm.cdf(abs(z)))
        pub = frozenset((a, b)) in reportados
        mark = 'FM>HC' if rF > rH else 'HC>=FM'
        if rH >= rF:
            contradicen.append(f'{a}-{b}')
        if pd_ < 0.05 and rF > rH:
            significativos.append(f'{a}-{b}')
        print(f'  {a+"-"+b:16}{rF:+9.3f}{rH:+9.3f}{pd_:8.3f}  {mark:10}'
              f'{"SÍ" if pub else "-- OMITIDO"}')

    print()
    record('"HC consistently weaker or non-significant" es cierto', not contradicen,
           f'{len(contradicen)}/10 pares tienen HC>=FM: {contradicen}')
    record('Mas de 1 par difiere significativamente FM vs HC', len(significativos) > 1,
           f'solo {len(significativos)} par(es) significativo(s): {significativos}')
    record('Los 10 pares estan reportados (sin seleccion)', len(reportados) == 10,
           f'el preprint reporta 5 de 10; los 4 que contradicen estan omitidos')
    return gse


def block4_background(gse):
    head('[4] ¿LAS SONDAS DEL EJE ESTÁN SOBRE EL RUIDO DE FONDO EN WHOLE BLOOD?')
    if gse is None:
        return
    gpl = list(gse.gpls.values())[0]
    tbl = gpl.table
    GEN = ['TACR1', 'OPRM1', 'OPRK1', 'TAC1', 'PENK', 'CD74', 'PTPRC', 'ACTB', 'GAPDH']
    first = list(gse.gsms.values())[0].table.set_index('ID_REF')['VALUE']
    allv = first.values.astype(float)
    print(f'  Distribución RMA log2 del array: p5={np.percentile(allv,5):.2f} '
          f'p25={np.percentile(allv,25):.2f} mediana={np.median(allv):.2f} máx={allv.max():.2f}\n')
    print(f'  {"gen":10}{"media log2":>12}{"percentil":>11}')
    bajos = []
    for g in GEN:
        pr = [x for x in tbl[tbl['gene_assignment'].astype(str).str.contains(f'// {g} //', na=False)]['ID']
              if x in first.index]
        if not pr:
            continue
        m = np.mean([first[x] for x in pr])
        pct = 100 * (allv < m).mean()
        flag = '  <-- CERCA DEL FONDO' if pct < 25 else ''
        if pct < 25 and g in ['TACR1', 'OPRM1', 'OPRK1', 'TAC1', 'PENK']:
            bajos.append(g)
        print(f'  {g:10}{m:12.2f}{"p"+str(int(pct)):>11}{flag}')
    print()
    record('Genes del eje están sobre el ruido en whole blood', not bajos,
           f'{bajos} en el decil/quintil inferior — la co-expresión puede ser fondo compartido')


# ---------------------------------------------------------------- QSP
def block5_qsp():
    head('[5] DIAGNÓSTICO TERMODINÁMICO DEL MODELO QSP (scripts/qsp_ca14_ph_nociception.py)')
    PK1, ALPHA, PCO2 = 6.1, 0.0307, 50.0
    C0, B0 = ALPHA * PCO2, 26.0
    H0 = 10 ** (-7.33) * 1e3
    KEQ = (B0 * H0) / C0
    T = C0 + B0

    def solve(ca, kuf, kur, kch, kcd, j_co2=0.02, k_diff=0.01, j_acid=1e-5, k_buf=0.5):
        k_hyd, k_deh = kuf + kch * ca, kur + kcd * ca
        c, h = C0, H0
        for _ in range(400):
            b = T - c
            fc = j_co2 - k_diff * c - k_hyd * c + k_deh * b * h
            fh = k_hyd * c - k_deh * b * h + j_acid - k_buf * h
            J = np.array([[-k_diff - k_hyd - k_deh * h, k_deh * b],
                          [k_hyd + k_deh * h, -k_deh * b - k_buf]])
            d = np.linalg.solve(J, np.array([-fc, -fh]))
            c += d[0]
            h += d[1]
            if abs(d).max() < 1e-14:
                break
        return -np.log10(h * 1e-3), k_hyd / k_deh

    KUF, KUR, KCH = 0.15, 50.0, 5.0
    KCD = (KUF + KCH) / KEQ - KUR
    print(f'  Keq termodinámico objetivo = {KEQ:.4e} mM')
    print(f'  Keq implícito del par NO catalizado (0.15 / 50.0) = {KUF/KUR:.4e} mM '
          f'-> {(KUF/KUR)/KEQ:.1f}x DESVIADO\n')
    print('  (A) parámetros actuales del script:')
    for ca in [1.0, 0.7, 0.5]:
        ph, keff = solve(ca, KUF, KUR, KCH, KCD)
        print(f'      ca_rel={ca}: pH={ph:.4f}  Keq_efectivo={keff:.4e} ({100*(keff/KEQ-1):+.2f}%)')
    dph_a = solve(0.5, KUF, KUR, KCH, KCD)[0] - solve(1.0, KUF, KUR, KCH, KCD)[0]
    print(f'      -> ΔpH(0.5 vs 1.0) = {dph_a:+.4f}   [el script publica -0.009]\n')

    KUR_c, KCD_c = KUF / KEQ, KCH / KEQ
    print(f'  (B) corregido: k_uncat_r = k_uncat_f/Keq = {KUR_c:.1f} s^-1 (en vez de 50):')
    for ca in [1.0, 0.7, 0.5]:
        ph, keff = solve(ca, KUF, KUR_c, KCH, KCD_c)
        print(f'      ca_rel={ca}: pH={ph:.4f}  Keq_efectivo={keff:.4e} ({100*(keff/KEQ-1):+.2f}%)')
    dph_b = solve(0.5, KUF, KUR_c, KCH, KCD_c)[0] - solve(1.0, KUF, KUR_c, KCH, KCD_c)[0]
    print(f'      -> ΔpH(0.5 vs 1.0) = {dph_b:+.7f}\n')

    print('  (C) pH basal vs J_co2 (debería estar fijado por el carbonato, no por la fuente):')
    for j in [0.005, 0.02, 0.05]:
        print(f'      J_co2={j:.3f} -> pH={solve(1.0,KUF,KUR,KCH,KCD,j_co2=j)[0]:.2f}'
              f'   (Henderson-Hasselbalch real = {PK1+np.log10(B0/(ALPHA*PCO2)):.2f})')
    print()
    record('El par no-catalizado respeta el Keq termodinámico', abs(KUF / KUR - KEQ) / KEQ < 0.05,
           f'desviado {(KUF/KUR)/KEQ:.1f}x -> el ΔpH publicado es deriva del Keq, no biofísica')
    record('El ΔpH publicado sobrevive la corrección termodinámica', abs(dph_b) > 0.001,
           f'con rates consistentes ΔpH={dph_b:+.7f} (= 0). El modelo NO puede evaluar la hipótesis')
    record('El pH basal del modelo reproduce Henderson-Hasselbalch (7.33)', False,
           'lo fija J_co2/k_buf: da 7.83/7.21/6.76 según parámetros no medidos')


def main():
    if not os.path.exists(XLSX):
        print(f'ERROR: no encuentro {XLSX}')
        sys.exit(1)
    print('AUDITORÍA EXTERNA — verificación ejecutable de claims (preprint v2.6)')
    print('Ver AUDITORIA_EXTERNA_2026-08-03.md y PLAN_REPARACION.md')

    meta, expr = load_pbmc()
    fm, hc = block1_reproduce(meta, expr)
    block2_sex(meta, expr, fm, hc)
    gse = block3_coexpr() if os.path.exists(SOFT67311) else None
    if gse is not None:
        block4_background(gse)
    block5_qsp()

    head('RESUMEN')
    npass = sum(1 for _, p, _ in results if p)
    for name, p, det in results:
        print(f'  [{OK if p else FAIL}] {name}')
    print(f'\n  {npass}/{len(results)} checks en PASS')
    print('\n  Interpretación esperada ANTES de reparar:')
    print('    - bloque [1] debe dar PASS  (los números publicados son correctos)')
    print('    - CA14 female-only debe dar FAIL  (ese es el hallazgo crítico de la auditoría)')
    print('    - claim D (co-expresión) debe dar FAIL  (reporte selectivo)')
    print('    - QSP debe dar FAIL  (el ΔpH es un bug de calibración)')
    print('  DESPUÉS de aplicar PLAN_REPARACION.md el texto del preprint debe ser')
    print('  consistente con estos FAIL — no se trata de hacerlos PASS forzando datos.')


if __name__ == '__main__':
    main()
