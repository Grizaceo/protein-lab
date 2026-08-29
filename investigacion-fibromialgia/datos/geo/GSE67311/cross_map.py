#!/usr/bin/env python3
"""Cross-map the FME exercise-response module + LPS blunting onto GSE67311 (FM vs HC blood).
Uses the DE results from GSE67311 (ID_REF key → probe), gene mapping from GPL11532,
and our key-gene list from GSE324210 (exercise) + GSE334369 (LPS blunting).
"""
import json, csv

BASE = '/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/datos/geo/GSE67311/'

with open(BASE + 'probe2gene.json') as f:
    probe2gene = json.load(f)

# Load DE results
rows = []
with open(BASE + 'GSE67311_all_results.txt') as f:
    r = csv.DictReader(f, delimiter='\t')
    for row in r:
        rows.append(row)

print(f"GSE67311 DE rows: {len(rows)}")

# Map probe -> gene
for row in rows:
    row['gene'] = probe2gene.get(row['ID_REF'], '')

# Now look up our key genes from the previous experiments
key_genes = [
    # From GSE324210 (exercise acute response — healthy monocytes)
    'IL1B', 'TAC1', 'MRGPRX2', 'CA14', 'CRH', 'TLR4', 'OPRM1',
    # From GSE334369 (LPS blunted response in FM neutrophils)
    'CXCL8', 'IL6', 'TNFAIP3', 'IL1RN', 'NLRP3', 'IL6R', 'TACR1',
    'ISG15', 'IFI44L', 'IFIT1', 'OAS1', 'MX1', 'IFITM1', 'SOCS3',
    'OPRD1', 'OPRK1', 'DRD2',
]

# Build results for key genes
result = {}
for row in rows:
    gene = row.get('gene', '')
    if gene in key_genes:
        # Keep best (lowest p-val) if multiple probes
        d = {
            'probe': row['ID_REF'],
            'log2FC': float(row['log2FC']),
            'pval': float(row['pval']),
            'adj_pval': float(row['adj.pval']),
            'FM_mean': float(row['FM_mean']),
            'HC_mean': float(row['HC_mean']),
        }
        if gene not in result or result[gene]['pval'] > d['pval']:
            result[gene] = d

print(f"\n=== Key gene expression in GSE67311 FM vs HC peripheral blood ===")
print(f"{'Gene':10} {'probe':10} {'log2FC':10} {'pval':12} {'adj_pval':12} {'FM':10} {'HC':10} {'dir'}")
for g in key_genes:
    if g in result:
        r = result[g]
        flag = '**' if r['adj_pval'] < 0.05 else ('*' if r['pval'] < 0.05 else '')
        direction = 'UP' if r['log2FC'] > 0 else ('DOWN' if r['log2FC'] < 0 else 'FLAT')
        print(f"{g:10} {r['probe']:10} {r['log2FC']:+.3f}     {r['pval']:.5f}     {r['adj_pval']:.5f}     {r['FM_mean']:6.2f}  {r['HC_mean']:6.2f} {direction} {flag}")
    else:
        print(f"{g:10} {'N/A':10} — probe not mapped")

with open(BASE + 'key_genes_in_gse67311.json', 'w') as f:
    json.dump(result, f, indent=2)
print("\nSaved key_genes_in_gse67311.json")