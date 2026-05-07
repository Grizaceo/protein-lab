#!/usr/bin/env python3
"""
SCOPE_C_RELAY_NETWORK.py
Construye la red de hopping real entre subunidades A y B en 1BFR.
Busca todos los átomos redox candidatos (Fe, S de Met/Cys, N de His/Trp)
y calcula la red de distancias entre ellos en la interfaz A-B.
"""
import os, numpy as np

BFR = os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")

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
                atoms.append({'chain': chain, 'resn': resn, 'rnum': rnum, 'name': name, 'elem': elem, 'pos': np.array([x,y,z])})
            except:
                continue

# Define redox-relevant atoms by element and residue
redox_elements = {'FE', 'S', 'CU', 'SE'}  # Metal centers, Sulfur in Met/Cys
# Also N in His imidazole (NE2, ND1) and Trp (NE1)
redox_atoms = []
for a in atoms:
    if a['elem'] in redox_elements:
        redox_atoms.append(a)
    if a['resn'] == 'HIS' and a['name'] in ('NE2','ND1'):
        redox_atoms.append(a)
    if a['resn'] == 'TRP' and a['name'] == 'NE1':
        redox_atoms.append(a)

print(f"Total redox-relevant atoms in PDB: {len(redox_atoms)}")

# Focus: interface between chain A residues 40-52 and chain B heme
# Collect candidates
chain_A_candidates = [a for a in redox_atoms if a['chain']=='A' and a['rnum'] in [40,43,46,49,52]]
chain_B_candidates = [a for a in redox_atoms if a['chain']=='B' and a['rnum'] in [i for i in range(195,205)]] # heme neighborhood
# Actually include all B atoms
chain_B_candidates = [a for a in redox_atoms if a['chain']=='B']

print(f"\nChain A candidates (res 40-52): {len(chain_A_candidates)}")
print(f"Chain B candidates (all): {len(chain_B_candidates)}")

# Get Heme B FE specifically
heme_fe = next((a for a in atoms if a['chain']=='B' and a['resn']=='HEM' and a['elem']=='FE'), None)
if heme_fe:
    print(f"Heme B FE found at res {heme_fe['rnum']} pos {heme_fe['pos']}")

# Find the histidine coordinating the Heme B in chain B (His axial ligand)
# Typically within ~2.5 Å of FE
if heme_fe:
    print("\n--- Atoms within 3.0 Å of Heme B FE (coordination sphere) ---")
    near_fe = []
    for a in atoms:
        if a is heme_fe: continue
        d = np.linalg.norm(a['pos'] - heme_fe['pos'])
        if d < 3.0:
            near_fe.append((a, d))
    near_fe.sort(key=lambda x: x[1])
    for a, d in near_fe[:10]:
        print(f"  {a['chain']} {a['resn']} {a['rnum']} {a['name']:4s} ({a['elem']:2s})  d={d:.3f} Å")

# Build inter-chain distance matrix between A redox and B redox
print("\n--- Distances between Chain A redox atoms and Chain B Heme/neighbors ---")

distances = []
for a in chain_A_candidates:
    for b in chain_B_candidates:
        d = np.linalg.norm(a['pos'] - b['pos'])
        distances.append((a['chain'], a['resn'], a['rnum'], a['name'], b['chain'], b['resn'], b['rnum'], b['name'], d))

distances.sort(key=lambda x: x[-1])
print("\nTop 15 shortest A-B redox distances:")
for entry in distances[:15]:
    print(f"  A {entry[1]} {entry[2]} {entry[3]:4s}  <->  B {entry[5]} {entry[6]} {entry[7]:4s}  = {entry[8]:.2f} Å")

# Find specific relay path: what connects Heme B Fe to MET52 SD with shortest total path?
# Build graph: all redox atoms in chains A and B
all_candidates = chain_A_candidates + chain_B_candidates
# Filter to reasonable range (within 15 Å of each other to speed up)
print(f"\n--- Graph edges (d < 8.0 Å, reasonable hopping) ---")
edges = []
for i, a in enumerate(all_candidates):
    for j in range(i+1, len(all_candidates)):
        b = all_candidates[j]
        d = np.linalg.norm(a['pos'] - b['pos'])
        if d < 8.0:
            edges.append((a, b, d))

print(f"Total edges under 8.0 Å: {len(edges)}")
for e in edges[:20]:
    a, b, d = e
    print(f"  {a['chain']} {a['resn']} {a['rnum']} {a['name']:4s} -- {d:.2f} Å -- {b['chain']} {b['resn']} {b['rnum']} {b['name']:4s}")
