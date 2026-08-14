#!/usr/bin/env python3
"""
REPLICACIÓN INDEPENDIENTE — COL9A1/PTN (hallazgo titular FM) en GSE67311 whole blood.

Línea C1 del plan LINEA_CANDIDATAS_2026-08-09.md (kanban t_b3702fcb).

CONTEXTO:
- GSE221921 (PBMC, discovery): COL9A1 FC=2.32 d=0.88, PTN FC=2.91 d=0.61, BPIFB2 FC=2.17.
  Ambos sobreviven 4/5 modelos del framework de 5 y la deconvolución composicional (4/4).
- COL9A1/PTN son proteínas MR-causales de dolor crónico generalizado (Chen 2025 PMID 41025730),
  pero JAMÁS se testearon en cohorte periférica independiente.
- GSE67311 = whole blood Affymetrix GPL11532, 67 FM vs 75 HC (diagnosis real en metadata).

PREGUNTA FALSABLE:
¿El hallazgo titular (COL9A1/PTN) replica en sangre periférica independiente?
Como el eje opioide falló en amplitud pero la co-expresión fue estable, medir AMBOS parámetros:
  (a) AMPLITUD: fold-change lineal, Mann-Whitney U + Bonferroni, Cohen's d.
  (b) ESTRUCTURA: co-expresión Spearman del módulo COL9A1-PTN-BPIFB2-ST3GAL1 en FM vs HC.

CONTROLES NEGATIVOS (fijar FDR empírico): genes de referencia conocidos NO-diferenciales en
FM inmunes/housekeeping (para medir la tasa de falsos positivos de la plataforma en ESTOS datos).

USO:
  /home/gris/.miniconda/envs/protein-lab/bin/python scripts/replicate_col9a1_ptn_gse67311.py
Output: stdout tabla + CSV analisis/C1_replication_col9a1_ptn_gse67311.csv
"""
import GEOparse
import numpy as np
import pandas as pd
from scipy import stats
from collections import Counter

GSE = 'GSE67311'
gse = GEOparse.get_GEO(geo=GSE, destdir='/tmp/gse67311_c1')

# ---- Etiquetado exacto por campo diagnosis (igual que scripts previos) ----
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

# ---- Genes objetivo ----
# Hipótesis + módulo (C1): COL9A1, PTN (titulares), BPIFB2, ST3GAL1 (módulo, ambos MR-CWP/immune)
# Controles negativos: genes inmunes/housekeeping NO-diferenciales para FDR empírico
targets = ['COL9A1', 'PTN', 'BPIFB2', 'ST3GAL1']           # hipótesis + módulo
neg_controls = ['GAPDH', 'ACTB', 'B2M', 'RPLP0', 'HPRT1', 'PPIA', 'TBP', 'YWHAZ']  # housekeeping
all_genes = targets + neg_controls

print(f'\n{"Gen":8s} {"FC lineal":>9s} {"MWU p":>9s} {"Bonf x12":>8s} {"d":>7s} {"n_probes":>9s} {"abs_level":>9s}  grupo')
results = {}
gene_vals = {}
fm_idx = [s for s in fm if s in table.columns]
hc_idx = [s for s in hc if s in table.columns]

for g in all_genes:
    probes = [int(p) for p, syms in probe2syms.items() if g in syms]
    probes = [p for p in probes if p in table.index]
    if not probes:
        print(f'{g:8s} AUSENTE')
        continue
    vals = table.loc[probes].mean(axis=0)
    fv = vals[fm_idx].values
    hv = vals[hc_idx].values
    fc_lin = 2 ** (fv.mean() - hv.mean())
    u, p = stats.mannwhitneyu(fv, hv, alternative='two-sided')
    p_bonf = min(1.0, p * len(all_genes))
    sp = np.sqrt(((len(fv) - 1) * fv.std(ddof=1) ** 2 + (len(hv) - 1) * hv.std(ddof=1) ** 2) / (len(fv) + len(hv) - 2))
    d = (fv.mean() - hv.mean()) / sp if sp > 0 else float('inf')
    results[g] = {'fc': fc_lin, 'p': p, 'p_bonf': p_bonf, 'd': d}
    gene_vals[g] = vals
    grp = 'HIPOTESIS' if g in targets else 'NEG_CTRL'
    print(f'{g:8s} {fc_lin:9.3f} {p:9.4f} {p_bonf:8.4f} {d:+7.3f} {len(probes):9d} {vals.mean():9.2f}  {grp}')

# ---- Control empírico de FDR: permutación de etiquetas sobre los genes de hipótesis ----
print('\n=== FDR empírico (permutación x2000, label shuffle) ===')
rng = np.random.default_rng(42)
hyp_genes = [g for g in targets if g in gene_vals]
all_samples = fm_idx + hc_idx
perm_hits_bonf = 0
N_PERM = 2000
# Pre-generar todas las permutaciones de etiquetas (seed fija, reproducible)
base_labels = ['FM'] * len(fm_idx) + ['HC'] * len(hc_idx)
labels_pos = []
for _ in range(N_PERM):
    lab = base_labels.copy()
    rng.shuffle(lab)
    labels_pos.append(lab)
for idx in range(N_PERM):
    # fv = FM subset, hv = HC subset, indexado por nombre de muestra
    fm_perm = [all_samples[i] for i in range(len(all_samples)) if labels_pos[idx][i] == 'FM']
    hc_perm = [all_samples[i] for i in range(len(all_samples)) if labels_pos[idx][i] == 'HC']
    for g in hyp_genes:
        vals = gene_vals[g]
        fv = vals[[s for s in fm_perm if s in vals.index]].values
        hv = vals[[s for s in hc_perm if s in vals.index]].values
        if len(fv) < 5 or len(hv) < 5:
            continue
        u, p = stats.mannwhitneyu(fv, hv, alternative='two-sided')
        if p * len(all_genes) < 0.05:
            perm_hits_bonf += 1
fdr_est = perm_hits_bonf / (N_PERM * len(hyp_genes))
print(f'Permutaciones: {N_PERM}; hits Bonf en permutación: {perm_hits_bonf}; FDR empírico por gen ≈ {fdr_est:.4f}')

# ---- Estructura: co-expresión Spearman del módulo COL9A1-PTN-BPIFB2-ST3GAL1 (FM vs HC) ----
print('\n=== Co-expresión Spearman módulo (amplitud-independiente) ===')
mod = [g for g in ['COL9A1', 'PTN', 'BPIFB2', 'ST3GAL1'] if g in gene_vals]
if len(mod) >= 2:
    for i in range(len(mod)):
        for j in range(i + 1, len(mod)):
            gi, gj = mod[i], mod[j]
            for grp, sidx in [('FM', fm_idx), ('HC', hc_idx)]:
                common = [s for s in sidx if s in gene_vals[gi].index and s in gene_vals[gj].index]
                if len(common) >= 5:
                    rho, p = stats.spearmanr(gene_vals[gi][common], gene_vals[gj][common])
                    print(f'{gi:7s}-{gj:7s} {grp} rho={rho:+.3f} (p={p:.3f}, n={len(common)})')

# ---- Referencia hipótesis PBMC (GSE221921) para comparación honesta ----
print('\n=== Referencia PBMC (GSE221921, texto del repo, verificado) ===')
print('COL9A1: FC=2.32, d=0.88, p_MW_bonf18=1.6e-6, survive 4/5 modelos + deconvolución 4/4')
print('PTN:    FC=2.91, d=0.61, p_MW_bonf18=2.4e-5, survive 4/5 modelos + deconvolución 4/4')
print('BPIFB2: FC=2.17, d=0.60, p_MW_bonf18=5.8e-5, survive 4/5 modelos')
print('ST3GAL1:FC=0.77, d=-0.23, (anticorrela con módulo en PBMC)')

# ---- Guardar CSV ----
rows = []
for g in all_genes:
    if g in results:
        rows.append({
            'gene': g, 'fc_lineal': results[g]['fc'], 'mwu_p': results[g]['p'],
            'bonf_x12': results[g]['p_bonf'], 'cohen_d': results[g]['d'],
            'grupo': 'HIPOTESIS' if g in targets else 'NEG_CTRL',
            'n_probes': sum(1 for p in probe2syms if g in probe2syms[p])
        })
pd.DataFrame(rows).to_csv('analisis/C1_replication_col9a1_ptn_gse67311.csv', index=False)
print('\nCSV guardado: analisis/C1_replication_col9a1_ptn_gse67311.csv')