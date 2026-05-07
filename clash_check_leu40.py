#!/usr/bin/env python3
"""
clash_check_leu40.py — FIX #5 (Rev 2026-04-24)
================================================
Verifica si la mutación LEU40→CYS en la cadena A de 1BFR genera un choque
estérico con átomos de la subunidad vecina (interfaz A-B del dímero).

CONTEXTO:
  El lumen de BFR está formado por 12 dímeros. La interfaz A-B (antiparallel
  helix bundle) tiene contactos en los residuos 38-55. LEU40 está en esta
  interfaz. Un SG de CYS modelado con distintos rotámeros χ₁ podría clash con:
    - Cadena B (subunidad vecina)
    - Cadena A en empaque simétrico

CRITERIO DE CLASH:
  d < 2.5 Å entre átomos pesados distintos (umbral conservador).
  d < 3.0 Å para H-bond o Au-S neighbors (warning suave).

REFERENCIA:
  1BFR: resolucion 2.9Å — las coordenadas tienen incertidumbre ~0.3Å.
  Clashs reales se definen con d < vdW_sum - 0.5 Å (Probe/MolProbity def).

Uso: python clash_check_leu40.py
"""

import sys
import numpy as np
from pathlib import Path

# Buscar 1BFR.pdb en ubicaciones conocidas
_bfr_candidates = [
    Path("data/pdb/new_chassis/1BFR.pdb"),
    Path("data/pdb/1BFR.pdb"),
    Path("alphafold/1BFR.pdb"),
]
BFR = next((p for p in _bfr_candidates if p.exists()), None)
if BFR is None:
    sys.exit("ERROR: No se encontró 1BFR.pdb. Descargarlo con:\n"
             "  wget -O data/pdb/new_chassis/1BFR.pdb "
             "https://files.rcsb.org/download/1BFR.pdb")

if not BFR.exists():
    sys.exit("ERROR: No se encontró 1BFR.pdb. Descargarlo con:\n"
             "  wget -O data/pdb/1BFR.pdb https://files.rcsb.org/download/1BFR.pdb")

# Van der Waals radii (Å)
VDW = {'C': 1.70, 'N': 1.55, 'O': 1.52, 'S': 1.80, 'FE': 1.25, 'H': 1.20}

def get_vdw(atom_name):
    for symbol in ['FE', 'S', 'N', 'O', 'C']:
        if atom_name.startswith(symbol):
            return VDW[symbol]
    return 1.70

# ─── Cargar estructura con BioPython ─────────────────────────────────────────
from Bio.PDB import PDBParser, Selection
import warnings
from Bio.PDB.PDBExceptions import PDBConstructionWarning
warnings.filterwarnings('ignore', category=PDBConstructionWarning)

parser  = PDBParser(QUIET=True)
struct  = parser.get_structure("1BFR", BFR)
model   = struct[0]

print("=" * 64)
print("CLASH CHECK: LEU40→CYS en interfaz dímero A-B de 1BFR")
print("Rev: 2026-04-24 | Fix #5 V4b Eccentric Design Validation")
print("=" * 64)

# ─── Constantes de geometría CYS ─────────────────────────────────────────────
BOND_CA_CB  = 1.530
BOND_CB_SG  = 1.810
ANGLE_CACBSG = np.radians(114.4)

def rodrigues(vec, axis, theta):
    axis = axis / np.linalg.norm(axis)
    return (vec * np.cos(theta)
            + np.cross(axis, vec) * np.sin(theta)
            + axis * np.dot(axis, vec) * (1 - np.cos(theta)))

def model_cys_sg(chain_id, resnum, chi1_deg):
    """Modela SG de CYS en posición resnum de chain_id con rotámero chi1."""
    chain = model[chain_id]
    try:
        res = chain[(" ", resnum, " ")]
    except KeyError:
        return None, None
    try:
        ca = res["CA"].get_vector().get_array()
        cb = res["CB"].get_vector().get_array()
    except KeyError:
        return None, None
    # Necesitamos N para definir el plano de chi1
    try:
        n = res["N"].get_vector().get_array()
    except KeyError:
        return None, None
    axis_chi1 = ca - cb
    axis_chi1 /= np.linalg.norm(axis_chi1)
    perp = n - cb
    perp -= np.dot(perp, axis_chi1) * axis_chi1
    if np.linalg.norm(perp) < 1e-6:
        return None, None
    perp /= np.linalg.norm(perp)
    base_dir = (np.cos(np.pi - ANGLE_CACBSG) * (-axis_chi1)
                + np.sin(np.pi - ANGLE_CACBSG) * perp)
    base_dir /= np.linalg.norm(base_dir)
    sg = cb + BOND_CB_SG * rodrigues(base_dir, axis_chi1, np.radians(chi1_deg))
    return sg, cb

# ─── Recolectar átomos de cadenas vecinas (B, C) y cadena A residuos ~35-55 ─
def collect_nearby_atoms(src_pos, radius=12.0):
    """Colecta todos los átomos dentro de radio Å del punto src_pos."""
    atoms = []
    for chain in model:
        for res in chain:
            for atom in res:
                p = atom.get_vector().get_array()
                if np.linalg.norm(p - src_pos) < radius:
                    atoms.append({
                        'chain': chain.id,
                        'resnum': res.get_id()[1],
                        'resname': res.resname,
                        'atom': atom.get_name(),
                        'pos': p,
                    })
    return atoms

# ─── Análisis de clash para cada rotámero ────────────────────────────────────
ROTAMERS = [("gauche-(-60°)", -60),
            ("trans  (180°)", 180),
            ("gauche+(+60°)",  60)]

CLASH_HARD = 2.5   # Å — clash real
CLASH_SOFT = 3.0   # Å — contacto apretado

print(f"\nModelo: 1BFR cadena A, residuo 40 (LEU→CYS)")
print(f"Cadenas vecinas evaluadas: B, C (dímero y subunidad adyacente)\n")

for rotname, chi1 in ROTAMERS:
    sg_pos, cb_pos = model_cys_sg('A', 40, chi1)
    if sg_pos is None:
        print(f"  {rotname}: No se pudo modelar SG (átomos faltantes)")
        continue

    # Colectar átomos cercanos
    nearby = collect_nearby_atoms(sg_pos, radius=10.0)

    hard_clashes = []
    soft_contacts = []

    for at in nearby:
        # Excluir: mismo residuo A-40, átomos CB de A-40, el CB propio
        if at['chain'] == 'A' and at['resnum'] == 40:
            continue
        d = np.linalg.norm(at['pos'] - sg_pos)
        vdw_sum = get_vdw('S') + get_vdw(at['atom'])
        overlap = vdw_sum - d
        if d < CLASH_HARD:
            hard_clashes.append((d, at, overlap))
        elif d < CLASH_SOFT:
            soft_contacts.append((d, at, overlap))

    # Resultado
    if hard_clashes:
        print(f"  {rotname}  ✗  {len(hard_clashes)} CLASH(S) DURO(S):")
        for d, at, ov in sorted(hard_clashes):
            print(f"       SG↔ {at['chain']}{at['resnum']:4d}-{at['resname']}-{at['atom']:<4s}"
                  f"  d={d:.2f}Å  overlap={ov:.2f}Å")
    elif soft_contacts:
        print(f"  {rotname}  ⚠  OK (sin clash duro) | {len(soft_contacts)} contactos apretados (2.5–3.0Å):")
        for d, at, ov in sorted(soft_contacts)[:3]:
            print(f"       SG↔ {at['chain']}{at['resnum']:4d}-{at['resname']}-{at['atom']:<4s}"
                  f"  d={d:.2f}Å")
    else:
        print(f"  {rotname}  ✓  Sin clashes — espacio libre (>3.0Å de todos los vecinos)")

# ─── Check adicional: LAT40C SG cerca de VAL43C o ILE49C (synergy check) ─────
print(f"\n─── Sinergía de mutaciones: LEU40C + VAL43C + ILE49C ───────────────────")
print("    Verificando que los 3 SG no choquen entre sí (cadena A):")

pos_test = {}
for (resnum, chi1) in [(40, 60), (43, 60), (49, 60)]:
    sg, _ = model_cys_sg('A', resnum, chi1)
    if sg is not None:
        pos_test[resnum] = sg

for i, (r1, sg1) in enumerate(pos_test.items()):
    for r2, sg2 in list(pos_test.items())[i+1:]:
        d = np.linalg.norm(sg1 - sg2)
        status = "✓" if d > 4.0 else ("⚠ muy cercanos" if d > 2.5 else "✗ CLASH")
        print(f"    CYS{r1:3d} SG ↔ CYS{r2:3d} SG : {d:.2f} Å  {status}")

print(f"""
INTERPRETACIÓN:
  - Clash duro (d < 2.5Å): la mutación no es viable sin remodelado del backbone.
  - Contacto apretado (2.5–3.0Å): posiblemente tolerable, confirmar con Rosetta.
  - Sin clash: la mutación es geométricamente viable en este rotámero.

  IMPORTANTE: La resolución de 1BFR es 2.9Å. Los errores posicionales pueden
  ser ±0.3Å. Los clashs limítrofes requieren remodelado con minimización energética
  (Rosetta FastRelax o AMBER minimization).

  ACCIÓN SI CLASH: probar rotámero alternativo o usar FoldX BuildModel
  para optimizar sidechain packing con la mutación.
""")
