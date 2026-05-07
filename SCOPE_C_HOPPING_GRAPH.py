#!/usr/bin/env python3
"""
SCOPE_C_HOPPING_GRAPH.py — Rev 2026-04-24 (Fix #8: pre-filtro por zona interfaz A-B)
Construye un grafo de hopping electrónico usando átomos potencialmente mediables
(S, N imidazol, anillos aromáticos Fe) y encuentra el camino más corto
entre CYS49 (rotámero gauche+) y HEM B FE usando saltos <= 8.0 Å.

OPTIMIZACIÓN (2026-04-24):
  El código original iteraba todos los átomos del 24-mer (~6000 átomos), lo que
  era O(n²) ≈ 36M pares. Se agrega un pre-filtro que restringe el grafo a:
    - Cadena A, residuos 35-60  (~35 residuos × ~8 átomos ≈ 280 átomos)
    - Cadena B completa (HEM 200 + entorno de hierro)
  Reducción: ~6000 → ~300 átomos → ~100× más rápido.
"""
import numpy as np, os, sys
import warnings
from Bio.PDB import PDBParser
from Bio.PDB.PDBExceptions import PDBConstructionWarning
warnings.filterwarnings('ignore', category=PDBConstructionWarning)

BFR = os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")

# ─── Cargar estructura con BioPython ─────────────────────────────────────────
_parser = PDBParser(QUIET=True)
_struct  = _parser.get_structure("1BFR", BFR)
_model   = _struct[0]

# ─── Pre-filtro de zona interfaz A-B (Fix #8) ────────────────────────────────
# Solo átomos de: cadena A residuos 35-60, + cadena B (HEM 200 completo)
CHAIN_A_RES_RANGE = range(35, 61)  # residuos del lumen donde ocurre el hopping
INTERFACE_CHAINS  = {'A', 'B'}

atoms = []
for chain in _model:
    cid = chain.id
    if cid not in INTERFACE_CHAINS:
        continue
    for res in chain:
        rid = res.get_id()
        rnum = rid[1]
        # Chain A: sólo residuos 35-60
        if cid == 'A' and rnum not in CHAIN_A_RES_RANGE:
            continue
        # Chain B: incluir todo (solo tiene HEM 200)
        for atom in res:
            try:
                atoms.append({
                    'chain': cid,
                    'resn':  res.resname,
                    'rnum':  rnum,
                    'name':  atom.get_name(),
                    'elem':  atom.element if atom.element else atom.get_name()[0],
                    'pos':   atom.get_vector().get_array(),
                })
            except Exception as e:
                print(f"  WARN: átomo no cargado ({cid}{rnum} {res.resname}): {e}", file=sys.stderr)

print(f"Átomos post-filtro (zona interfaz A[35-60]+B): {len(atoms)}")
print(f"  (vs ~{sum(1 for c in _model for r in c for a in r)} átomos totales en 24-mer)")

def get(c, rn, ri, name):
    """Busca átomo por chain/resname-no/nombre en lista pre-filtrada."""
    for a in atoms:
        if a['chain'] == c and a['rnum'] == ri and a['name'] == name:
            return a['pos']
    return None


# Candidates for ET hopping:
# - S in CYS, MET
# - NE2, ND1 in HIS
# - FE in HEM
# - Aromatic ring centroids: PHE, TYR, TRP
# - Maybe O in backbone? generally too high energy, skip
hopping_atoms = []
for a in atoms:
    if a['elem'] == 'FE':
        hopping_atoms.append(a)
    elif a['elem'] == 'S':
        hopping_atoms.append(a)
    elif a['resn'] == 'HIS' and a['name'] in ('NE2', 'ND1'):
        hopping_atoms.append(a)
    elif a['resn'] == 'TRP' and a['name'] == 'NE1':
        hopping_atoms.append(a)

# Add centroid of aromatic rings (simplified: use CZ for PHE/TYR or CG for TRP as proxy)
# Better: just use the CZ or centroid atom
aromatic_proxy_atoms = []
for a in atoms:
    if a['resn'] in ('PHE', 'TYR') and a['name'] == 'CZ':
        aromatic_proxy_atoms.append(a)
    elif a['resn'] == 'TRP' and a['name'] == 'CH2':
        aromatic_proxy_atoms.append(a)

hopping_atoms += aromatic_proxy_atoms

print(f"Graph nodes (potential hopping centers): {len(hopping_atoms)}")

# Build edges: distance < 8.0 Å between any pair
MAX_HOP = 8.0  # Å — generous but realistic for non-bonded ET
beta = 1.4
k0 = 1e13

class Node:
    def __init__(self, atom, idx):
        self.atom = atom
        self.idx = idx
        self.label = f"{atom['chain']} {atom['resn']} {atom['rnum']} {atom['name']}"

nodes = [Node(a, i) for i, a in enumerate(hopping_atoms)]
edges = []  # list of (i, j, distance, k_rate)

for i in range(len(nodes)):
    for j in range(i+1, len(nodes)):
        d = np.linalg.norm(nodes[i].atom['pos'] - nodes[j].atom['pos'])
        if d <= MAX_HOP:
            k = k0 * np.exp(-beta * d)
            edges.append((i, j, d, k))

print(f"Edges (d <= {MAX_HOP} Å): {len(edges)}")

# Dijkstra's algorithm: minimize total "cost" where cost = -log(k) ~ β * d
# This is equivalent to minimizing sum of distances
import heapq

# Build adjacency list with -log(k) as weight
adj = {i: [] for i in range(len(nodes))}
for i, j, d, k in edges:
    cost = -np.log(k) if k > 0 else 1e9
    adj[i].append((j, cost, d))
    adj[j].append((i, cost, d))

# Define source: approximate CYS49 SG (we mutate ILE49)
# Use the CB + direction from earlier or just create a synthetic node at ILE49 CA + sidechain vector
# We will model the synthetic CYS49 SG as an isolated node

source_atoms = []
# CYS49 SG — rotámero gauche+(+60°) confirmado óptimo (geometry_cys_rotamer.py, 2026-04-24)
# Coordenadas verificadas: SG = [14.722, 7.977, 49.444] (error aprox anterior = 2.0 Å)
ca49 = get('A', None, 49, 'CA')
cb49 = get('A', None, 49, 'CB')
n49  = get('A', None, 49, 'N')
if ca49 is not None and cb49 is not None and n49 is not None:
    BOND_CB_SG   = 1.810
    ANGLE_CACBSG = np.radians(114.4)
    axis_chi1 = ca49 - cb49;  axis_chi1 /= np.linalg.norm(axis_chi1)
    perp = n49 - cb49;  perp -= np.dot(perp, axis_chi1) * axis_chi1;  perp /= np.linalg.norm(perp)
    base_dir = np.cos(np.pi - ANGLE_CACBSG) * (-axis_chi1) + np.sin(np.pi - ANGLE_CACBSG) * perp
    base_dir /= np.linalg.norm(base_dir)
    def _rot(v, ax, th): return v*np.cos(th) + np.cross(ax,v)*np.sin(th) + ax*np.dot(ax,v)*(1-np.cos(th))
    sg49 = cb49 + BOND_CB_SG * _rot(base_dir, axis_chi1, np.radians(60.0))  # gauche+
    source_atoms.append({'chain': 'A', 'resn': 'CYS', 'rnum': 49, 'name': 'SG', 'elem': 'S', 'pos': sg49})
    print(f"CYS49 SG (gauche+, revisión 2026-04-24): {np.round(sg49,3)}")
elif ca49 is not None and cb49 is not None:
    # Fallback: aprox CA→CB extendida (±2.0 Å de error)
    v = cb49 - ca49;  v = v / np.linalg.norm(v)
    sg49 = cb49 + v * 1.81
    source_atoms.append({'chain': 'A', 'resn': 'CYS', 'rnum': 49, 'name': 'SG', 'elem': 'S', 'pos': sg49})
    print(f"WARN: CYS49 SG aproximado (N49 falta) — error posicional ~2Å")

# Target: B HEM200 FE
target_pos = get('B', None, 200, 'FE')

if target_pos is None:
    print("ERROR: No heme B found")
    sys.exit(1)

# Build full graph including synthetic source and target
all_nodes = nodes.copy()
source_idx = len(all_nodes)
all_nodes.append(Node(source_atoms[0], source_idx))
target_idx = len(all_nodes)
all_nodes.append(Node({'chain': 'B', 'resn': 'HEM', 'rnum': 200, 'name': 'FE', 'elem': 'FE', 'pos': target_pos}, target_idx))

# Rebuild adjacency with source and target
adj_full = {i: [] for i in range(len(all_nodes))}
for i, j, d, k in edges:
    cost = -np.log(k) if k > 0 else 1e9
    adj_full[i].append((j, cost, d))
    adj_full[j].append((i, cost, d))

# Connect source synthetic SG to nearby hopping atoms within 8A
for i in range(len(nodes)):
    d = np.linalg.norm(all_nodes[source_idx].atom['pos'] - all_nodes[i].atom['pos'])
    if d <= MAX_HOP:
        k = k0 * np.exp(-beta * d)
        cost = -np.log(k) if k > 0 else 1e9
        adj_full[source_idx].append((i, cost, d))
        adj_full[i].append((source_idx, cost, d))
        print(f"Source connected to: {all_nodes[i].label} at d={d:.2f} A (k={k:.2e})")

# Connect target FE to nearby hopping atoms within 8A
for i in range(len(nodes)):
    d = np.linalg.norm(all_nodes[target_idx].atom['pos'] - all_nodes[i].atom['pos'])
    if d <= MAX_HOP:
        k = k0 * np.exp(-beta * d)
        cost = -np.log(k) if k > 0 else 1e9
        adj_full[target_idx].append((i, cost, d))
        adj_full[i].append((target_idx, cost, d))
        print(f"Target connected to: {all_nodes[i].label} at d={d:.2f} A (k={k:.2e})")

# Dijkstra from source to target
INF = 1e18
dist = [INF] * len(all_nodes)
prev = [None] * len(all_nodes)
dist[source_idx] = 0.0
pq = [(0.0, source_idx)]
visited = set()

while pq:
    d_u, u = heapq.heappop(pq)
    if u in visited: continue
    visited.add(u)
    if u == target_idx:
        break
    for v, cost, physical_dist in adj_full[u]:
        if dist[v] > dist[u] + cost:
            dist[v] = dist[u] + cost
            prev[v] = u
            heapq.heappush(pq, (dist[v], v))

if prev[target_idx] is None:
    print("\nNO PATH FOUND within d <= 8.0 Å hopping limit.")
    print("This means the proposed CYS49->Heme relay CANNOT be bridged with realistic ET hopping distances.")
    sys.exit(0)

# Reconstruct path
path = []
node = target_idx
while node is not None:
    path.append(node)
    node = prev[node]
path.reverse()

print(f"\n=== SHORTEST HOPPING PATH (<= {MAX_HOP}A per hop) ===")
total_d = 0.0
total_cost = 0.0
min_k = 1e99
print(f"{'Step':>4} {'From':35} {'To':35} {'d(A)':>7} {'k(s-1)':>12} {'tau(s)':>10}")
print("-" * 105)
for idx in range(len(path)-1):
    u, v = path[idx], path[idx+1]
    # find physical distance
    d = np.linalg.norm(all_nodes[u].atom['pos'] - all_nodes[v].atom['pos'])
    k = k0 * np.exp(-beta * d)
    tau = 1.0/k
    if k < min_k: min_k = k
    total_d += d
    total_cost += -np.log(k) if k > 0 else 1e9
    f = all_nodes[u].label
    t = all_nodes[v].label
    if u == source_idx: f = "A CYS 49 SG (synthetic target)"
    if v == target_idx: t = "B HEM 200 FE (target)"
    print(f"{idx+1:>4} {f:35} {t:35} {d:>7.2f} {k:>12.2e} {tau:>10.2e}")
    
print("-" * 105)
print(f"TOTAL physical distance: {total_d:.2f} A")
print(f"Overall rate bottleneck (slowest hop): k = {min_k:.2e} s-1, tau = {1/min_k:.2e} s")
print(f"Estimated throughput (sequential hops, limited by slowest): {min_k:.2e} e-/s")
print(f"\nIf we assume 1000 electrons (from Au nanocluster saturation): total discharge time ~ {1000/min_k:.2e} s")
print(f"Current equivalent (single electron charge 1.6e-19 C): I = {1.6e-19 * min_k:.2e} A = {1.6e-19 * min_k * 1e12:.2f} pA")
