"""
Test de bimodalidad FME (sub-fenotipo FM por respuesta a ejercicio / EIH) en datos geómicos en disco.

Hipótesis FME (falsable): si la FM tiene dos sub-poblaciones definidas por analgesia
inducida por ejercicio intacta vs deteriorada (Sluka 2018 PMID 30113953; Lannersten 2010
PMID 20621420), y los proxies transcriptómicos COL9A1/PTN marcan el eje periférico/somático
(modulable), entonces la distribución del proxy COL9A1/PTN en FM debería ser BIMODAL
(subgrupo elevado vs subgrupo no-elevado) mientras que los controles HC serían unimodales.

Si NO hay bimodalidad → consistente con continuum → registered como negative/constraint honesto.

Método: Hartigan dip test (Hartigan & Hartigan 1985) + bootstrap p-value.
- Distribución: log2(FPKM+1) en GSE221921 (RNA-seq PBMC); log2 RMA ya transformado en GSE67311 (microarray whole blood).
- Null bootstrap: uniform null escalado al rango observado (canonical Hartigan) + null gaussiano (sensibilidad).
- Genes: COL9A1, PTN (titulares), BPIFB2, ST3GAL1 (módulo), controles negativos: GAPDH, ACTB, MDH1, LGALS3BP.
- Estratificación: FM vs HC por separado (la hipótesis predice bimodalidad DENTRO de FM, no HC).

Salidas:
  analisis/fme/dip_test_GSE221921.csv
  analisis/fme/dip_test_GSE67311.csv
  analisis/fme/dip_results.json (resumen métricas)
"""
import os, sys, json
import numpy as np
import pandas as pd
import diptest

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # investigacion-fibromialgia/
OUT = os.path.join(REPO, 'analisis', 'fme')
os.makedirs(OUT, exist_ok=True)

TARGETS = ['COL9A1', 'PTN', 'BPIFB2', 'ST3GAL1']
NEG_CTRLS = ['GAPDH', 'ACTB', 'MDH1', 'LGALS3BP']
N_BOOT = 5000
SEED = 112358


def dip_bootstrap_pvalue(x, n_boot=N_BOOT, null='uniform', seed=SEED):
    """p-value bootstrap de Hartigan dip: fracción de puntos null con dip >= dip observado.

    null='uniform': muestras uniformes escaladas al rango de x (canonical Hartigan-Hartigan H0).
    null='gaussian': muestras normales con mu/sd de x (sensibilidad para formas no-uniformes).
    """
    rng = np.random.default_rng(seed + (0 if null == 'uniform' else 1))
    n = len(x)
    d_obs = diptest.dipstat(x)
    if null == 'uniform':
        lo, hi = float(np.min(x)), float(np.max(x))
        null_dips = np.array([diptest.dipstat(rng.uniform(lo, hi, n)) for _ in range(n_boot)])
    else:
        mu, sd = float(np.mean(x)), float(np.std(x, ddof=1))
        null_dips = np.array([diptest.dipstat(rng.normal(mu, sd, n)) for _ in range(n_boot)])
    p = float(np.mean(null_dips >= d_obs))
    return d_obs, p, float(np.percentile(null_dips, 95))


def extract_gse221921():
    """Extrae matriz log2(FPKM+1) de genes objetivo + metadatos desde XLSX en disco."""
    import openpyxl
    p = os.path.join(REPO, 'datos', 'geo', 'PBMC_FM_96patients_93controls', 'GSE221921_FM_ProcessedData.xlsx')
    wb = openpyxl.load_workbook(p, read_only=True)

    # Metadatos de muestras
    meta = {}
    ws = wb['Metadata (Samples)']
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue
        meta[row[0]] = {'etiology': row[1], 'gender': row[2]}

    # Buscar fila de cada gen en Values (FPKM)
    gene_rows = {}
    ws2 = wb['Values (FPKM)']
    sample_ids = None
    wanted = set(TARGETS + NEG_CTRLS)
    for i, row in enumerate(ws2.iter_rows(values_only=True)):
        if i == 0:
            sample_ids = list(row)
        else:
            sym = row[1]
            if sym in wanted and sym not in gene_rows:
                gene_rows[sym] = list(row)
        if len(gene_rows) == len(wanted):
            break
    wb.close()
    assert sample_ids is not None, 'header no encontrado'

    data = {}
    for g, vals in gene_rows.items():
        # primeras columnas son anotación (Ensembl, symbol, desc, ...) — alinear con sample_ids
        expr = {sample_ids[j]: vals[j] for j in range(len(sample_ids)) if sample_ids[j] in meta}
        data[g] = pd.Series(expr)

    df = pd.DataFrame(data)
    df.index.name = 'sample'
    return df, pd.DataFrame(meta).T


def extract_gse67311():
    """GSE67311: series matrix con la tabla de expresión completa; GPL via family.soft local."""
    import gzip
    p = os.path.join(REPO, 'datos', 'geo', 'GSE67311', 'GSE67311_series_matrix.txt.gz')
    series = {}
    table_rows, in_table = {}, False
    with gzip.open(p, 'rt') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('!Sample_title'):
                series['titles'] = line.split('\t')[1:]
            elif line.startswith('!Sample_source_name_ch1'):
                series['sources'] = line.split('\t')[1:]
            elif line.startswith('!Sample_characteristics_ch1'):
                series.setdefault('chars', []).append(line.split('\t')[1:])
            elif line.startswith('!series_matrix_table_begin'):
                in_table = True
                continue
            elif line.startswith('!series_matrix_table_end'):
                in_table = False
            elif in_table:
                parts = line.split('\t')
                table_rows[parts[0].strip('"')] = parts[1:]

    titles = [t.strip().strip('"') for t in series['titles']]
    chars = series.get('chars', [])
    # diagnosis vector
    diag = None
    for c in chars:
        vals = [v.strip().strip('"').lower() for v in c]
        if any('fibromyalgia' in v or 'control' in v for v in vals):
            diag = ['fibromyalgia' if 'fibromyalgia' in v else ('control' if 'control' in v else '?') for v in vals]
            break
    assert diag is not None, 'no diagnosis characteristic found'

    probes = list(table_rows.keys())[1:]  # skip ID_REF header
    expr = pd.DataFrame(table_rows).T.iloc[1:]
    expr.columns = titles
    expr = expr.apply(pd.to_numeric, errors='coerce')
    expr.index = expr.index.astype(int).astype(str)

    # Anotación de sondas se hace aparte en gpl_annotation_gse67311()
    return expr, diag, titles


def gpl_annotation_gse67311():
    """Parsea la tabla GPL11532 desde el family.soft local → probe_id -> symbol(s)."""
    import gzip
    soft = os.path.join(REPO, 'datos', 'geo', 'GSE67311', 'GSE67311_family.soft.gz')
    probe2syms = {}
    in_table = False
    cols = None
    with gzip.open(soft, 'rt') as f:
        for line in f:
            if line.startswith('!platform_table_begin'):
                in_table = True
                cols = None
                continue
            if not in_table:
                continue
            if line.startswith('!platform_table_end'):
                break
            parts = line.rstrip('\n').split('\t')
            if cols is None:
                cols = {c: i for i, c in enumerate(parts)}
                continue
            rec = dict(zip([None] + list(cols.values()), [''] + parts))
            idx = parts[cols.get('ID', 0)]
            ga = parts[cols['gene_assignment']] if 'gene_assignment' in cols and cols['gene_assignment'] < len(parts) else ''
            syms = set()
            for part in str(ga).split('///'):
                fields = [fd.strip() for fd in part.split('//')]
                if len(fields) >= 2 and fields[1] and fields[1] != '---':
                    syms.add(fields[1])
            probe2syms[str(idx)] = syms
    return probe2syms


def dip_table(df_expr, groups, label, log_transform):
    rows = []
    all_genes = TARGETS + NEG_CTRLS
    for gene in all_genes:
        if gene not in df_expr.columns:
            rows.append({'dataset': label, 'gene': gene, 'error': 'gene absent'})
            continue
        for grp in ['FM', 'HC']:
            idx = [s for s in df_expr.index if groups[s] == grp]
            x = df_expr.loc[idx, gene].astype(float)
            if log_transform:
                x = np.log2(x + 1.0)
            x = x.dropna().values
            if len(np.unique(x)) < 10 or len(x) < 30:
                rows.append({'dataset': label, 'gene': gene, 'group': grp, 'n': len(x), 'error': 'insuficiente'})
                continue
            d_u, p_u, crit_u = dip_bootstrap_pvalue(x, null='uniform')
            d_g, p_g, crit_g = dip_bootstrap_pvalue(x, null='gaussian')
            rows.append({
                'dataset': label, 'gene': gene, 'group': grp, 'n': len(x),
                'mean_expr': float(np.mean(x)), 'sd_expr': float(np.std(x, ddof=1)),
                'skew': float(pd.Series(x).skew()),
                'dip': round(d_u, 5), 'p_uniform': p_u, 'crit95_uniform': round(crit_u, 5),
                'dip_gauss': round(d_g, 5), 'p_gaussian': p_g, 'crit95_gaussian': round(crit_g, 5),
            })
    return pd.DataFrame(rows)


def main():
    # ============ GSE221921 ============
    df, meta = extract_gse221921()
    groups = meta['etiology'].to_dict()
    groups = {k: ('FM' if v == 'Fibromyalgia' else 'HC') for k, v in groups.items()}
    t221 = dip_table(df, groups, 'GSE221921(log2FPKM+1)', log_transform=True)
    t221.to_csv(os.path.join(OUT, 'dip_test_GSE221921.csv'), index=False)
    print('=== GSE221921 ===')
    print(t221.to_string())

    # ============ GSE67311 ============
    expr, diag, titles = extract_gse67311()
    p2s = gpl_annotation_gse67311()
    gene2probes = {}
    for pr, syms in p2s.items():
        for g in TARGETS + NEG_CTRLS:
            if g in syms:
                gene2probes.setdefault(g, []).append(pr)

    # pacientes duplicados (C009 y C009_2) — conservar ambas columnas (no afectan dip por grupo)
    groups673 = {t: ('HC' if diag[j] == 'control' else 'FM') for j, t in enumerate(titles)}
    # promediar sondas co-mapeadas al gen (promedio en espacio log2)
    df673 = {}
    for g, probes in gene2probes.items():
        probes = [p for p in probes if p in expr.index]
        if len(probes) == 1:
            df673[g] = expr.loc[probes[0]]
        elif len(probes) > 1:
            df673[g] = expr.loc[probes].mean(axis=0)
    df673 = pd.DataFrame(df673)
    t673 = dip_table(df673, groups673, 'GSE67311(log2RMA)', log_transform=False)
    t673.to_csv(os.path.join(OUT, 'dip_test_GSE67311.csv'), index=False)
    print('=== GSE67311 ===')
    print(t673.to_string())
    print('probes mapeadas:', {g: v for g, v in gene2probes.items()})

    # ============ Resumen JSON ============
    def verdicts(t):
        out = {}
        for gene in TARGETS:
            sub = t[(t.gene == gene)]
            out[gene] = {}
            for _, r in sub.iterrows():
                if 'error' in r and pd.notna(r.get('error')):
                    out[gene][str(r.get('group', '?'))] = {'error': r['error']}
                    continue
                out[gene][r['group']] = {
                    'dip': r['dip'] if pd.notna(r.get('dip')) else None,
                    'p_uniform': r['p_uniform'] if pd.notna(r.get('p_uniform')) else None,
                    'p_gaussian': r['p_gaussian'] if pd.notna(r.get('p_gaussian')) else None,
                }
        return out

    res = {
        'spec': 'test bimodalidad FME (Hartigan dip + bootstrap 5000, null uniforme y gaussiano) en proxies COL9A1/PTN/modulo',
        'semilla': SEED, 'n_boot': N_BOOT,
        'GSE221921_cases': int(sum(1 for v in meta['etiology'] if v == 'Fibromyalgia')),
        'GSE221921_controls': int(sum(1 for v in meta['etiology'] if v == 'Control')),
        'GSE67311_FM': int(sum(1 for v in groups673.values() if v == 'FM')),
        'GSE67311_HC': int(sum(1 for v in groups673.values() if v == 'HC')),
        'verdict_221921': verdicts(t221),
        'verdict_67311': verdicts(t673),
    }
    with open(os.path.join(OUT, 'dip_results.json'), 'w') as f:
        json.dump(res, f, indent=2, default=str)
    print('OK — salidas en', OUT)


if __name__ == '__main__':
    main()