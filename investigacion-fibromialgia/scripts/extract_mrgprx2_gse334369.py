#!/usr/bin/env python3
"""Extract MRGPRX2 (and control genes) TPMs from GSE334369 RAW tar and run the
blunting analysis (paired LPS-response, Welch case vs control).

Falsifies or confirms the handoff from @eidos: is the MRGPRX2/TAC1 axis
differentially responsive in FM neutrophils after LPS? TAC1 is already known
null (p=0.907). MRGPRX2 was NOT in the 19-gene panel.

Pre-registered kill criterion (same as ichor-fme-gse334369-blunted-response-v1):
at least 1 gene with blunting p<0.05 after Bonferroni (n_genes tested).
"""
import json
import tarfile
import gzip
import os

BASE = "/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/datos/geo/GSE334369"
GENES = ["MRGPRX2", "TAC1", "TACR1", "CMA1", "IL1B", "CXCL8"]  # IL1B/CXCL8 positive controls from prior run

groups = json.load(open(os.path.join(BASE, "groups_gse334369.json")))
# groups keys: Case_NAR, Case_NNAR, Control_NAR, Control_NNAR (GSM IDs)

# Build map: GSM -> tar member name
tar = tarfile.open(os.path.join(BASE, "GSE334369_RAW.tar"), "r")
member_by_gsm = {}
for m in tar.getmembers():
    name = m.name  # e.g. GSM9786802_processed_NEBNext_dual_i5_288.E02NARAligned.tsv.gz
    gsm = name.split("_")[0]
    member_by_gsm[gsm] = m.name

print(f"members: {len(member_by_gsm)}")

tpm = {g: {} for g in GENES}
tar_iter = tarfile.open(os.path.join(BASE, "GSE33436802" if False else "GSE334369_RAW.tar"), "r")
for gsm, member_name in member_by_gsm.items():
    f = tar_iter.extractfile(member_name)
    if f is None:
        continue
    data = gzip.decompress(f.read()).decode("utf-8", errors="replace")
    lines = data.splitlines()
    header = lines[0].split("\t")
    # column 1 is TPM value
    idx_tpm = 1
    gene_col = 0
    vals = {}
    for line in lines[1:]:
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        gid = parts[gene_col].strip()
        if gid in GENES:
            try:
                vals[gid] = float(parts[idx_tpm])
            except ValueError:
                pass
    for g in GENES:
        if g in vals:
            tpm[g][gsm] = vals[g]

tar.close()

json.dump(tpm, open(os.path.join(BASE, "mrgprx2_tpm.json"), "w"), indent=1)
print("extracted:", {g: len(tpm[g]) for g in GENES})