#!/usr/bin/env python3
"""Extract probe->gene symbol mapping from GPL11532 annot.gz for GSE67311."""
import gzip, json, os

os.chdir('/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/datos/geo/GSE67311')

gene_map = {}
header = None
in_table = False

with gzip.open('GPL11532.annot.gz', 'rt') as f:
    for l in f:
        l = l.rstrip('\n')
        if l.startswith('!platform_table_begin'):
            in_table = True
            continue
        if l.startswith('!platform_table_end'):
            break
        if not in_table:
            continue
        if header is None:
            header = l.split('\t')
            print(f"Header: {header}")
            continue
        parts = l.split('\t')
        if len(parts) < len(header):
            continue
        probe = parts[0]
        try:
            idx = header.index('Gene symbol')
            gene_symbol = parts[idx] if idx < len(parts) else ''
        except ValueError:
            gene_symbol = ''
        if probe and gene_symbol:
            gene_map[probe] = gene_symbol

print(f"Mapped probes: {len(gene_map)}")
with open('probe2gene.json', 'w') as f:
    json.dump(gene_map, f)
print("Saved probe2gene.json")