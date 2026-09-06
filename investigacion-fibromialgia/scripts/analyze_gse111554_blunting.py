#!/usr/bin/env python3
"""Download GPL17586 annotation and map probes -> gene symbols for GSE111554."""
import gzip, re, json, os, urllib.request
import numpy as np
from scipy import stats
from collections import defaultdict

LP_ROOT = '/home/gris/.hermes/workspace/ACTIVE/protein-lab/'
BASE = LP_ROOT + 'investigacion-fibromialgia/datos/geo/'
GSE = 'GSE111554'

# Download annotation
gpl_path = BASE + 'GPL17586_family.soft.gz'
if not os.path.exists(gpl_path) or os.path.getsize(gpl_path) < 1_000_000:
    url = "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL17nnn/GPL17586/soft/GPL17586_family.soft.gz"
    print(f"Downloading GPL17586_family.soft.gz...")
    urllib.request.urlretrieve(url, gpl_path)
    print(f"OK: {os.path.getsize(gpl_path)/1e6:.1f} MB")

# Parse soft file: probe -> gene_symbol
probe_to_gene = {}
print("Parsing annotation table...")
with gzip.open(gpl_path, 'rt', errors='ignore') as f:
    in_table = False
    header = None
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('!platform_table_begin'):
            in_table = True
            continue
        if line.startswith('!platform_table_end'):
            break
        if not in_table:
            continue
        if header is None:
            header = line.split('\t')
            print(f"Header columns: {len(header)}")
            continue
        parts = line.split('\t')
        if len(parts) < len(header):
            continue
        probe = parts[0]
        # Find gene symbol column
        try:
            idx = header.index('Gene Symbol')
        except ValueError:
            try:
                idx = header.index('gene_assignment')
            except ValueError:
                idx = None
        if idx is not None and idx < len(parts):
            gene_info = parts[idx]
            # gene_assignment format: "accession /// symbol /// description"  OR  "symbol // desc // acc"
            # Try to find gene symbol from ilmn gene format: "ID // symbol // description"
            if '//' in gene_info:
                pieces = [p.strip() for p in gene_info.split('//')]
                if len(pieces) >= 2:
                    gene_symbol = pieces[1]
                    if gene_symbol and gene_symbol != '---':
                        probe_to_gene[probe] = gene_symbol
            
with open(BASE + 'GPL17586_probe2gene.json', 'w') as f:
    json.dump(probe_to_gene, f)
print(f"Mapped probes: {len(probe_to_gene)}")

# --- Now compute the blunting score on pre-training samples ---
# Load series matrix (pre subjects)
with gzip.open(BASE + f'{GSE}_series_matrix.txt.gz', 'rt') as f:
    content = f.read()
lines = content.split('\n')

sample_ids, titles = None, None
for l in lines:
    if l.startswith('!Sample_geo_accession'):
        sample_ids = [v.strip().strip('"') for v in l.split('\t')[1:]]
    elif l.startswith('!Sample_title'):
        titles = [v.strip().strip('"') for v in l.split('\t')[1:]]

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

# Load expression
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

print(f"Probes: {len(expr_probe)}")
gsm2col = {gsm: idx for idx, gsm in enumerate(col_order)}

# Blunting module genes from GSE334369 (FM neutrophils LPS response, all DOWN in FM = blunted)
blunting_genes = {
    'CXCL8': 'IL8 / IL-8 (blunted in FM, p=0.0096)',
    'IL6':   'IL-6 (blunted, p=0.036)',
    'IL1B':  'IL-1β (blunted, p=0.055)',
    'TNFAIP3': 'A20 (blunted, p=0.045)',
}

# Compute per-subject baseline expression of each blunting gene
subject_gene_expr = {gene: {} for gene in blunting_genes}
for gene in blunting_genes:
    for subj in range(1, n_subjects+1):
        gid = gsm_pre.get(subj)
        if not (gid and gid in gsm2col):
            continue
        col = gsm2col[gid]
        # Find probe(s) mapped to gene
        vals = []
        for probe, gs in probe_to_gene.items():
            if gs == gene.upper() or gs.startswith(gene + ' ') or gs.startswith(gene + ',') or gs == gene:
                if probe in expr_probe:
                    v = expr_probe[probe][col]
                    if v > 0:  # skip zero/missing
                        vals.append(v)
        subject_gene_expr[gene][subj] = np.mean(vals) if vals else np.nan

# Z-score blunting score per subject: mean of the 4 genes (higher = more responsive = NOT blunted)
subjects = sorted(gsm_pre.keys())
blunting_scores = {}
for subj in subjects:
    vals_raw = []
    for gene, raw in subject_gene_expr[gene].items():
        pass
    # For each gene: higher expression pre-training = more responsive
    gene_means = []
    for gene in blunting_genes:
        v = subject_gene_expr[gene].get(subj, np.nan)
        if not np.isnan(v):
            gene_means.append(v)
    blunting_scores[subj] = np.mean(gene_means) if gene_means else np.nan

# Load VO2 deltas
with open(BASE + f'{GSE}_vo2_response.json') as f:
    vdata = json.load(f)
delta_vo2 = {p['subject']: p['delta'] for p in vdata['pairs']}

# Correlation test
xs = [blunting_scores[s] for s in subjects if not np.isnan(blunting_scores[s])]
ys = [delta_vo2[s] for s in subjects if not np.isnan(blunting_scores[s])]
rho, p = stats.spearmanr(xs, ys)
print(f"\n=== Spearman( blunting_pre, ΔVO2 ) — GSE111554 n={len(xs)} ===")
print(f"rho = {rho:.4f}")
print(f"p = {p:.4f}")
print(f"kill threshold: rho < 0.2 = FAIL, > 0.4 = PASS")

with open(BASE + f'{GSE}_blunting_vo2.json', 'w') as f:
    json.dump({'rho': float(rho), 'p': float(p), 'n': len(xs), 'genetic_module': list(blunting_genes.keys())}, f, indent=2)
print(f"Saved {GSE}_blunting_vo2.json")