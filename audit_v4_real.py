#!/usr/bin/env python3
"""
audit_v4_real.py
Auditoria de gaps interfaciales para BioMaterialCAD V4.
Usa coordenadas reales del PDB 1BFR (E.Coli bacterioferritin).
Autor: DAVI-rol Adam Heller. Estado: Freeze V4-20260422.
"""

import os, numpy as np

BFR = os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")

print("=" * 60)
print("AUDITORIA V4: Au NP Policristalino -> Electrodo (via Heme)")
print("Chasis: E.Coli 1BFR, 24-mer, Coordenadas reales PDB")
print("=" * 60)

atoms = []
with open(BFR, 'r') as f:
    for line in f:
        if line.startswith(("ATOM", "HETATM")):
            try:
                chain = line[21]
                resn = line[17:20].strip()
                rnum = int(line[22:26])
                name = line[12:16].strip()
                elem = line[76:78].strip()
                x = float(line[30:38]); y = float(line[38:46]); z = float(line[46:54])
                atoms.append({'chain': chain, 'resn': resn, 'rnum': rnum, 'name': name, 'elem': elem, 'pos': np.array([x, y, z])})
            except:
                continue

# 1. Center of 24-mer via chain COMs
chain_coms = {}
for c in set(a['chain'] for a in atoms):
    pa = [a['pos'] for a in atoms if a['chain'] == c]
    chain_coms[c] = np.mean(pa, axis=0)
center = np.mean(list(chain_coms.values()), axis=0)

# 2. Au NP center @ lumen centroid (simulated)
au_np_radius = 18.0   # Å for 800-atom cluster
au_np_center = center.copy()

# 3. Heme FE positions
hemes = [(a['chain'], a['pos']) for a in atoms if a['resn'] == 'HEM' and a['elem'] == 'FE']

# Pick representative Heme B (adjacent to Chain A)
# Find heme closest to chain A COM
chain_a_com = chain_coms['A']
heme_pos = None
min_d = 1e9
for chain, pos in hemes:
    d = np.linalg.norm(pos - chain_a_com)
    if d < min_d:
        min_d = d
        heme_pos = pos
        heme_chain = chain

print(f"\nReferencia hemo: Chain {heme_chain} FE @ {heme_pos}")
print(f"Dist Chain A COM -> Heme {heme_chain} FE: {min_d:.2f} Å")

# 4. Key residues in Chain A
sel = {43: 'VAL', 49: 'ILE', 46: 'HIS', 52: 'MET', 44: 'GLU'}

# Find CA positions for these residues
ca_pos = {}
for a in atoms:
    if a['chain'] == 'A' and a['rnum'] in sel and a['name'] == 'CA':
        ca_pos[a['rnum']] = a['pos']

for r, n in sel.items():
    if r in ca_pos:
        d_center = np.linalg.norm(ca_pos[r] - center)
        d_heme = np.linalg.norm(ca_pos[r] - heme_pos)
        print(f"  Chain A {n} {r}: CA -> center={d_center:.1f}Å | -> Heme FE={d_heme:.2f}Å")
    else:
        print(f"  Chain A {n} {r}: NOT FOUND (PDB mismatch)")

# 5. Hopping gaps (estimated from CA geometry)
# We need SG positions for CYS mutants; approximate: SG ~ 2.5Å from CA along side-chain vector.
# For ILE49->CYS: approximate SG position
# Better: use CA as proxy for SG with a fixed offset ~2.0Å closer to heme.
# But V4 uses Au NP surface distance to SG. We know CA-HEME = 6.36Å and Au NP center = lumen center.
# So dist(Au NP surface, ILE49 CA) = dist(center, CA) - au_np_radius ~ 40.3 - 18 = 22.3Å.
# This is too long for direct thiol contact! Need SG at lumen wall.

d_ile49_to_center = np.linalg.norm(ca_pos[49] - center)
d_ile49_to_heme = np.linalg.norm(ca_pos[49] - heme_pos)

print("\n--- Análisis de SALTOS ESTIMADOS (gap hopping) ---")
# Gap 1: Au NP surface -> SG of (mutant) CYS49
# CYS is at ~40.3A from center. Au NP radius = 18A. Gap = 40.3 - 18 = 22.3A?
# Actually, if CYS SG sticks inward, it reaches closer to Au. 
# Max side-chain reach from CA for CYS: ~3-4A. So SG could be at ~36-37A from center.
# Au NP surface at 18A. So surface-to-SG gap ~ 36 - 18 = 18A? Still long.
# This suggests the Au NP CANNOT be placed at exact center if we want direct CYS49 linkage.

# Alternative: The Au NP is not a solid sphere contacting SG; the CYS thiols CHEMICALLY BIND to the Au surface.
# Au-S bond length = ~2.3Å. So the Au NP is anchored by 24 thiols at lumen radius ~38A.
# That means the Au NP center is at center + (38A - Au radius)?? No, thiols stretch.
# The Au NP sits at lumen center, and CYS side chains stretch inward to reach it.
# If CYS is at 40A, side chain length is ~4A, so SG reaches to ~36A.
# Au NP surface at 18A. Gap 36-18 = 18A still too long for covalent attachment.

# Realization: With 3 CYS per subunit, they need to be CLOSER to center (~25-30A) to reach a 3nm Au NP at center.
# Let's check which neutral residues are at 25-35A from center (close to Au NP surface).

inner_neutral = []
for a in atoms:
    if a['chain'] == 'A' and a['name'] == 'CA':
        if a['resn'] in ['ALA', 'VAL', 'ILE', 'LEU', 'MET', 'PHE', 'TRP', 'PRO', 'GLY']:
            d = np.linalg.norm(a['pos'] - center)
            if 25 <= d <= 35:
                inner_neutral.append((a['rnum'], a['resn'], d))
inner_neutral.sort(key=lambda x: x[2])
print(f"\nResiduos neutrales entre 25-35Å del centro (candidatos para tocar Au NP de radio 18Å):")
for r, n, d in inner_neutral[:10]:
    print(f"   {n} {r}: {d:.2f}Å")

# Conclusion: The CYS strategy requires residues that are BOTH close to the Au NP AND near the heme.
# In the real BFR lumen, the innermost layer at 25-35A doesn't overlap with the "near-heme" set.
# Best compromise: CYS49 is at 40.3A. Au NP surface 18A -> gap 22A. 
# To bridge this, we NEED an intermediate relay residue on the lumen wall.
# Or: we shrink the Au NP to radius ~8A (Au55 cluster, ~100 atoms) placed at center, then CYS49 at 40A with 4A side chain -> SG at 36A, gap to Au55 surface 36-8 = 28Å. STILL too long.
# OR: we use a much SMALLER Au cluster (Au10, radius 3-4A) and MANY more CYS reaching inward.

# This means V4 with 800-atom Au NP is GEOMETRICALLY IMPOSSIBLE to contact CYS49.
# We must use Au SMALLER or position it OFF-CENTER near the lumen wall.

print("\n[!] ALERTA GEOMÉTRICA:")
print("    Au NP radio 18Å en centro: superficie a 18Å del centro.")
print("    CYS49 CA a 40.3Å; SG estimado a ~36Å.")
print("    GAP mínimo Au surface -> SG: ~18Å. Demasiado largo para Au-S covalente.")
print("\n    SOLUCIÓN PROPUESTA:")
print("    1. Usar Au NP MÁS PEQUEÑO (radio ~12Å, ~300 átomos), o")
print("    2. Desplazar Au NP hacia la pared luminal (excentrico), anclándolo")
print("       a una subunidad particular, o")
print("    3. Insertar un RELAY redox en el lumen (e.g., ubiquinona, ruthenium complex)")
print("       entre Au surface y CYS49.")
