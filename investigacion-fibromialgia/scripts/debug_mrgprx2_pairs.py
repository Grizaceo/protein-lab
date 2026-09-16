#!/usr/bin/env python3
"""Debug del bucle principal: cuántos pares arma cada gen y por qué falla."""
import json
import math
import os

BASE = "/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/datos/geo/GSE334369"
GENES = ["MRGPRX2", "TAC1", "TACR1", "CMA1", "IL1B", "CXCL8"]

groups = json.load(open(f"{BASE}/groups_gse334369.json"))
tpm = json.load(open(f"{BASE}/mrgprx2_tpm.json"))

# Recreate gsm_to_ecode from tar (same logic as analyzer)
import tarfile
BASE_TAR = os.path.join(BASE, "GSE334369_RAW.tar")
gsm_to_ecode = {}
tar = tarfile.open(BASE_TAR, "r")
for m in tar.getmembers():
    gsm = m.name.split("_")[0]
    stem = m.name.rsplit(".", 2)[0]
    ecode = stem.split(".")[-1]
    gsm_to_ecode[gsm] = ecode
tar.close()

print("gsm_to_ecode sample:", dict(list(gsm_to_ecode.items())[:3]))

# Case_NAR pairing
ok, no_partner, no_tpm = 0, 0, 0
for gsm in groups["Case_NAR"]:
    e = gsm_to_ecode.get(gsm)
    if e is None:
        no_tpm += 1
        continue
    donor = e[:-3]
    partner = ecode_to_gsm_local = None
    # find partner
    target = donor + "NNAR"
    found = [g2 for g2, e2 in gsm_to_ecode.items() if e2 == target]
    if not found:
        no_partner += 1
    else:
        p = found[0]
        if gsm in tpm["IL1B"] and p in tpm["IL1B"]:
            ok += 1
        else:
            no_tpm += 1
print(f"Case_NAR: ok={ok} no_partner={no_partner} no_tpm={no_tpm} of {len(groups['Case_NAR'])}")