#!/usr/bin/env python3
"""FME ejercicio-sensible: project blunted-response module onto GSE111554 blood G2 (n=20, VO2 variability).
Test: Spearman( blunting_score_pre, delta_VO2 ) — kill rho<0.2 in both blood datasets."""
import gzip, re, json, os, urllib.request
import numpy as np
from collections import defaultdict
from scipy import stats

LPROOT = '/home/gris/.hermes/workspace/ACTIVE/protein-lab/'
BASE = LPROOT + 'investigacion-fibromialgia/datos/geo/'
gse = 'GSE111554'

# --- load series matrix ---
with gzip.open(BASE + f'{gse}_series_matrix.txt.gz', 'rt') as f:
    content = f.read()
lines = content.split('\n')

sample_ids, titles = None, None
platform = None
for l in lines:
    if l.startswith('!Sample_geo_accession'):
        sample_ids = [v.strip().strip('"') for v in l.split('\t')[1:]]
    elif l.startswith('!Sample_title'):
        titles = [v.strip().strip('"') for v in l.split('\t')[1:]]
    elif l.startswith('!Series_platform_id'):
        parts = l.split('\t')
        if len(parts) >= 2:
            platform = parts[1].strip().strip('"')
        else:
            p = l.split('=', 1)
            if len(p) == 2:
                platform = p[1].strip().strip('"')

n_subjects = 20
gsm_pre, gsm_post = {}, {}
for gid, t in zip(sample_ids, titles):
    m = re.match(r'(\d+)(T[ab]):', t)
    if m:
        subj, phase = int(m.group(1)), m.group(2)
        if phase == 'Ta':
            gsm_pre[subj] = gid
        elif phase == 'Tb':
            gsm_post[subj] = gid
print(f'Pre GSMs: {len(gsm_pre)}, Post GSMs: {len(gsm_post)}')

# --- VO2 response data ---
with open(BASE + f'{gse}_vo2_response.json') as f:
    vdata = json.load(f)
pairs = vdata['pairs']
delta_vo2 = {p['subject']: p['delta'] for p in pairs}
print(f'VO2 deltas: {len(delta_vo2)}')

# --- load expression table ---
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
            expr_probe_vals = parts[1:]
            expr_probe[probe] = [float(v) for v in expr_probe_vals]
        break

print(f'Probes: {len(expr_probe)}')

# --- sample-to-subject mapping: col order = sample_ids order ---
gsm2subject = {gsm_pre[s]: s for s in gsm_pre}
gsm2subject_post = {gsm_post[s]: s for s in gsm_post}
gsm_phase = {gsm_pre[s]: 'pre' for s in gsm_pre}
gsm_phase.update({gsm_post.get(s, None): 'post' for s in gsm_post if s in gsm_post})

# For each subject: sample for pre is at position i (i=0..19), column position matches
gsm_col = {gsm: idx for idx, gsm in enumerate(col_order) if gsm}

# Pre-expression matrix by subject
pre_expr = {}
for subj in range(1, n_subjects+1):
    gid = gsm_pre.get(subj)
    if gid and gid in gsm_phase:
        idx = col_order.index(gid)
        pre_expr[subj] = [expr_probe[p][idx] for p in expr_probe.keys()]
print(f'Pre expression loaded: {len(pre_expr)} subjects x ??? probes')

# Save progress so far
out = {
    'n_subjects': n_subjects,
    'platform': platform,
    'n_probes': len(expr_probe),
    'delta_vo2_mean': float(np.mean(list(delta_vo2.values()))),
    'note': 'Pre expression matrix extracted; next step is probe->gene mapping via GPL17586'
}
with open(BASE + f'{gse}_extraction_summary.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f'Saved {gse}_extraction_summary.json: {out}')