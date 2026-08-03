#!/usr/bin/env python3
"""
Validación cruzada GSE67311 — whole blood Affymetrix (70 FM vs 70 HC declarados)
Replica el análisis de GSE221921 (Mann-Whitney + Bonferroni + Cohen's d) en cohorte independiente.

Dataset: GSE67311 "Peripheral Blood Gene Expression in Fibromyalgia Patients Reveals
         Potential Biological Markers and Physiological Pathways" (GPL11532)
Nota metadata: diagnosis en GEO = 67 fibromyalgia + 75 healthy control (142 total;
el paper declara 70/70 — diferencia reportada, no ocultada).
"""
import GEOparse
import numpy as np
from scipy import stats
from collections import Counter

GSE = 'GSE67311'
gse = GEOparse.get_GEO(geo=GSE, destdir='/tmp/gse67311')

# --- Etiquetado exacto por campo diagnosis: ---
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
print(f'FM={len(fm)} HC={len(hc)} (paper declara 70/70)')

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

targets = ['TAC1', 'PENK', 'IL6', 'OPRM1', 'CXCL8', 'LGALS3BP', 'PCSK1N', 'MDH1']
print(f'\n{"Gen":8s} {"FC lineal":>9s} {"MWU p":>8s} {"Bonf x8":>8s} {"d":>7s}  probes')
results = {}
for g in targets:
    probes = [int(p) for p, syms in probe2syms.items() if g in syms]
    probes = [p for p in probes if p in table.index]
    if not probes:
        print(f'{g:8s} AUSENTE')
        continue
    vals = table.loc[probes].mean(axis=0)
    fv = vals[[s for s in fm if s in vals.index]].values
    hv = vals[[s for s in hc if s in vals.index]].values
    fc_lin = 2 ** (fv.mean() - hv.mean())  # Affymetrix RMA en log2
    u, p = stats.mannwhitneyu(fv, hv, alternative='two-sided')
    p_bonf = min(1.0, p * 8)
    sp = np.sqrt(((len(fv) - 1) * fv.std(ddof=1) ** 2 + (len(hv) - 1) * hv.std(ddof=1) ** 2) / (len(fv) + len(hv) - 2))
    d = (fv.mean() - hv.mean()) / sp if sp > 0 else float('inf')
    results[g] = {'fc': fc_lin, 'p': p, 'p_bonf': p_bonf, 'd': d}
    print(f'{g:8s} {fc_lin:9.3f} {p:8.4f} {p_bonf:8.4f} {d:+7.3f}  {len(probes)}')
