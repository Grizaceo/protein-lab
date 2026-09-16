#!/usr/bin/env python3
"""Diagnóstico: por qué el script de análisis no imprime resultados."""
import json

BASE = "/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/datos/geo/GSE334369"

tpm = json.load(open(f"{BASE}/mrgprx2_tpm.json"))
for g in tpm:
    vals = list(tpm[g].values())
    nz = sum(1 for v in vals if v > 0)
    print(f"{g}: n={len(vals)} nonzero={nz}")

groups = json.load(open(f"{BASE}/groups_gse334369.json"))
print("groups keys:", list(groups.keys()))
for k, v in groups.items():
    print(k, len(v))