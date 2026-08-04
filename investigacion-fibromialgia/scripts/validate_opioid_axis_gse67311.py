#!/usr/bin/env python3
"""
Validación del EJE OPIOIDE/TAQUIKININA completo en GSE67311 — whole blood Affymetrix.
Replica el análisis de GSE221921 (PBMC) para los receptores y ligandos del eje:
  TACR1 (NK1R), OPRM1 (mu), OPRK1 (kappa), TAC1 (Substance P), PENK (encefalinas).

Contexto PBMC (GSE221921): TACR1 FC=2.73 d=+0.60, OPRM1 FC=2.28 d=+0.53, TAC1 FC=2.10,
OPRK1 FC=1.78; co-expresión rho 0.31-0.63. Pregunta: ¿replica en whole blood?

Dataset: GSE67311 (GPL11532). Diagnosis GEO = 67 FM + 75 HC (paper declara 70/70).
Método idéntico a validate_fm_biomarkers_gse67311.py: Mann-Whitney + Bonf x5 + Cohen's d.
"""
import GEOparse
import numpy as np
from scipy import stats
from collections import Counter

GSE = 'GSE67311'
gse = GEOparse.get_GEO(geo=GSE, destdir='/tmp/gse67311')

states = {}
diags = Counter()
for gsm_id, gsm in gse.gsms.items():
    for ch in gsm.metadata.get('characteristics_ch1', []):
        if ch.lower().startswith('diagnosis:'):
            d = ch.split(':', 1)[1].strip()
            diags[d] += 1
            states[gsm_id] = 'FM' if 'fibromyalgia' in d.lower() else ('HC' if 'control' in d.lower() else 'OTHER')
print(f'Diagnosis en GEO: {dict(diags)}')
fm = [s for s, v in states.items() if v == 'FM']
hc = [s for s, v in states.items() if v == 'HC']
print(f'FM={len(fm)} HC={len(hc)}')

table = gse.pivot_samples('VALUE')
table.index = table.index.astype(int)

gpl = gse.gpls['GPL11532']
ann = gpl.table
id_col = ann.columns[0]

def parse_symbols(raw):
    syms = set()
    for part in str(raw).split('///'):
        fields = [f.strip() for f in part.split('//')]
        if len(fields) >= 2 and fields[1] and fields[1] != '---':
            syms.add(fields[1])
    return syms

probe2syms = {str(row[id_col]): parse_symbols(row.get('gene_assignment', '')) for _, row in ann.iterrows()}

targets = ['TACR1', 'OPRM1', 'OPRK1', 'TAC1', 'PENK']
print(f'\n{"Gen":8s} {"FC lineal":>9s} {"MWU p":>8s} {"Bonf x5":>8s} {"d":>7s}  probes')
results = {}
gene_vals = {}
for g in targets:
    probes = [int(p) for p, syms in probe2syms.items() if g in syms]
    probes = [p for p in probes if p in table.index]
    if not probes:
        print(f'{g:8s} AUSENTE')
        continue
    vals = table.loc[probes].mean(axis=0)
    fv = vals[[s for s in fm if s in vals.index]].values
    hv = vals[[s for s in hc if s in vals.index]].values
    fc_lin = 2 ** (fv.mean() - hv.mean())
    u, p = stats.mannwhitneyu(fv, hv, alternative='two-sided')
    p_bonf = min(1.0, p * 5)
    sp = np.sqrt(((len(fv) - 1) * fv.std(ddof=1) ** 2 + (len(hv) - 1) * hv.std(ddof=1) ** 2) / (len(fv) + len(hv) - 2))
    d = (fv.mean() - hv.mean()) / sp if sp > 0 else float('inf')
    results[g] = {'fc': fc_lin, 'p': p, 'p_bonf': p_bonf, 'd': d}
    gene_vals[g] = vals
    print(f'{g:8s} {fc_lin:9.3f} {p:8.4f} {p_bonf:8.4f} {d:+7.3f}  {len(probes)}')

# --- Co-expresión rho (Spearman) entre genes del eje, en FM y HC ---
print('\n=== Co-expresión Spearman entre genes del eje (GSE67311 whole blood) ===')
present = {g: v for g, v in gene_vals.items()}
genes = list(present.keys())
if len(genes) >= 2:
    for i in range(len(genes)):
        for j in range(i + 1, len(genes)):
            gi, gj = genes[i], genes[j]
            vi_fm = present[gi][[s for s in fm if s in present[gi].index]]
            vj_fm = present[gj][[s for s in fm if s in present[gj].index]]
            vi_hc = present[gi][[s for s in hc if s in present[gi].index]]
            vj_hc = present[gj][[s for s in hc if s in present[gj].index]]
            common_fm = [s for s in vi_fm.index if s in vj_fm.index]
            common_hc = [s for s in vi_hc.index if s in vj_hc.index]
            if len(common_fm) >= 5:
                rho_fm, p_fm = stats.spearmanr(vi_fm[common_fm], vj_fm[common_fm])
            else:
                rho_fm, p_fm = float('nan'), float('nan')
            if len(common_hc) >= 5:
                rho_hc, p_hc = stats.spearmanr(vi_hc[common_hc], vj_hc[common_hc])
            else:
                rho_hc, p_hc = float('nan'), float('nan')
            print(f'{gi:6s}-{gj:6s}  FM rho={rho_fm:+.3f} (p={p_fm:.3f})  HC rho={rho_hc:+.3f} (p={p_hc:.3f})')

print('\nReferencia PBMC (GSE221921): TACR1 d=+0.60, OPRM1 d=+0.53, TAC1 d=+0.47, OPRK1 FC=1.78; rho co-expresión 0.31-0.63')
