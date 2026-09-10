#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extraer vo2peak pre/post por sujeto + expresión pre-training de GSE111552 (PBMC).
Mismo pipeline que analyze_gse111554_blunting.py pero para GSE111552.
"""
import gzip, re, json, os
import numpy as np
from scipy import stats

LP_ROOT = '/home/gris/.hermes/workspace/ACTIVE/protein-lab/'
BASE = LP_ROOT + 'investigacion-fibromialgia/datos/geo/'
GSE = 'GSE111552'

# --- 1. Parse series matrix: samples, titles, vo2peak, expression ---
with gzip.open(f'/tmp/{GSE}_sm.txt.gz', 'rt') as f:
    content = f.read()
lines = content.split('\n')

sample_ids, titles = None, None
vo2_ml = None  # vo2peak (ml/min/kg) per sample
for l in lines:
    if l.startswith('!Sample_geo_accession'):
        sample_ids = [v.strip().strip('"') for v in l.split('\t')[1:]]
    elif l.startswith('!Sample_title'):
        titles = [v.strip().strip('"') for v in l.split('\t')[1:]]
    elif l.startswith('!Sample_characteristics_ch1') and 'vo2peak (ml/min/kg)' in l:
        vo2_ml = [v.strip().strip('"') for v in l.split('\t')[1:]]

print(f"samples: {len(sample_ids)}")
print("titles sample:", titles[:6])
print("vo2 sample:", vo2_ml[:6])

# --- 2. Map subject + phase from titles ---
# Formato esperado: "1Ta" / "1Tb" o similar (como GSE111554)
subj_phase = {}
for gid, t in zip(sample_ids, titles):
    m = re.match(r'(\d+)(Pa|Pb)', t)
    if m:
        subj_phase[gid] = (int(m.group(1)), m.group(2))
    else:
        # probar otros formatos
        m2 = re.match(r'(\d+)[-_ ]?(pre|post|PRE|POST)', t)
        if m2:
            ph = 'Pa' if m2.group(2).lower().startswith('pre') else 'Pb'
            subj_phase[gid] = (int(m2.group(1)), ph)
        else:
            print("NO MATCH:", repr(t))

print(f"parsed subjects: {len(subj_phase)}")

# --- 3. vo2peak por sujeto (pre=Pa, post=Pb) ---
vo2_by_subj = {}
for gid, (subj, phase) in subj_phase.items():
    if gid in sample_ids:
        idx = sample_ids.index(gid)
        v = vo2_ml[idx] if idx < len(vo2_ml) else None
        if v and v != '--' and v != '""':
            try:
                num = v.split(':')[-1].strip()
                vo2_by_subj.setdefault(subj, {})[phase] = float(num)
            except ValueError:
                pass

print(f"subjects with vo2: {len(vo2_by_subj)}")
deltas = {}
for subj, phases in sorted(vo2_by_subj.items()):
    if 'Pa' in phases and 'Pb' in phases:
        deltas[subj] = phases['Pb'] - phases['Pa']
print(f"subjects with delta: {len(deltas)}")
print("delta sample:", {k: round(v, 2) for k, v in list(deltas.items())[:5]})

# --- 4. Expresión pre-training (Ta) ---
# Cargar expresión
expr_probe = {}
col_order = None
for i, l in enumerate(lines):
    if l.startswith('!series_matrix_table_begin'):
        header = [c.strip().strip('"') for c in lines[i+1].split('\t')[1:]]
        col_order = header
        for j in range(i+2, len(lines)):
            if lines[j].startswith('!series_matrix_table_end'):
                break
            parts = lines[j].split('\t')
            probe = parts[0].strip().strip('"')
            try:
                expr_probe[probe] = [float(v) for v in parts[1:]]
            except ValueError:
                pass
        break
print(f"probes: {len(expr_probe)}, cols: {len(col_order)}")

# --- 5. probe->gene (GPL17586 ya en disco) ---
probe_to_gene = json.load(open(BASE + 'GPL17586_probe2gene.json'))
print(f"probe->gene map: {len(probe_to_gene)}")

# --- 6. Módulo blunting (mismos 4 genes que GSE111554) ---
blunting_genes = ['CXCL8', 'IL6', 'IL1B', 'TNFAIP3']

gsm2col = {gsm: idx for idx, gsm in enumerate(col_order)}
gsm_pre = {subj: gid for gid, (subj, ph) in subj_phase.items() if ph == 'Pa'}

subject_gene_expr = {gene: {} for gene in blunting_genes}
for gene in blunting_genes:
    for subj, gid in gsm_pre.items():
        if gid not in gsm2col:
            continue
        col = gsm2col[gid]
        vals = []
        for probe, gs in probe_to_gene.items():
            if gs == gene.upper() or gs.startswith(gene + ' ') or gs.startswith(gene + ',') or gs == gene:
                if probe in expr_probe:
                    v = expr_probe[probe][col]
                    if v > 0:
                        vals.append(v)
        subject_gene_expr[gene][subj] = np.mean(vals) if vals else np.nan

# --- 7. Blunting score por sujeto (media de genes) ---
subjects = sorted(gsm_pre.keys())
blunting_scores = {}
for subj in subjects:
    gene_means = [subject_gene_expr[g].get(subj, np.nan) for g in blunting_genes]
    gene_means = [v for v in gene_means if not np.isnan(v)]
    blunting_scores[subj] = np.mean(gene_means) if gene_means else np.nan

# --- 8. Spearman(blunting_pre, delta_vo2) ---
xs = [blunting_scores[s] for s in subjects if not np.isnan(blunting_scores[s]) and s in deltas]
ys = [deltas[s] for s in subjects if not np.isnan(blunting_scores[s]) and s in deltas]
print(f"\n=== Spearman(blunting_pre, ΔVO2) — {GSE} n={len(xs)} ===")
if len(xs) >= 5:
    rho, p = stats.spearmanr(xs, ys)
    print(f"rho = {rho:.4f}")
    print(f"p = {p:.4f}")
    print(f"kill threshold: rho < 0.2 = FAIL, > 0.4 = PASS")
    out = {'rho': float(rho), 'p': float(p), 'n': len(xs), 'genetic_module': blunting_genes,
           'dataset': GSE, 'tissue': 'PBMC'}
    with open(BASE + f'{GSE}_blunting_vo2.json', 'w') as f:
        json.dump(out, f, indent=2)
    print(f"Saved {GSE}_blunting_vo2.json")
else:
    print("n demasiado pequeño para test")
