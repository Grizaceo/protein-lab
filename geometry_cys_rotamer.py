#!/usr/bin/env python3
"""
geometry_cys_rotamer.py — FIX #1 (Rev 2026-04-24)
====================================================
Calcula la posición del SG del CYS49 mutado (desde ILE49) usando
la librería de rotámeros de BioPython, en lugar de la extensión
vectorial naive del script SCOPE_C_REAL_GEOMETRY.py original.

El método anterior usaba:
    pos_sg_approx = pos_ca49 + v * 3.4   # ±3Å de error potencial

Este script usa los tres rotámeros canónicos χ₁ de cisteína
(gauche+: -60°, trans: 180°, gauche-: +60°) y reporta SG para
cada uno, indicando cuál contacta mejor al Heme B y a HIS46.

Uso: python geometry_cys_rotamer.py
"""

import os
from pathlib import Path
import numpy as np
from Bio.PDB import PDBParser


# ─── Parámetros de geometría tetraédrica ──────────────────────────────────────
BOND_CA_CB = 1.530   # Å  (CYS: igual a ILE dentro de error cristalográfico)
BOND_CB_SG = 1.810   # Å  (CYS estándar)
ANGLE_CA_CB_SG = np.radians(114.4)  # grados → radianes (AMBER ff19SB)

_script_dir = Path(__file__).resolve().parent
_candidates = [
    _script_dir / "data/pdb/new_chassis/1BFR.pdb",
    _script_dir / "data/pdb/1BFR.pdb",
    Path(os.path.expanduser("~/.hermes/workspace/ACTIVE/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
    Path(os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
]
BFR_PATH = str(next((p for p in _candidates if p.exists()), _candidates[0]))


# ─── Cargar estructura con BioPython (sin silenciar errores) ──────────────────
parser = PDBParser(QUIET=False)
structure = parser.get_structure("1BFR", BFR_PATH)
model = structure[0]

chain_A = model["A"]
chain_B = model["B"]

# ─── Obtener átomos anchor de ILE49 (precursor del CYS mutado) ───────────────
ile49 = chain_A[49]
N49  = ile49["N"].get_vector()
CA49 = ile49["CA"].get_vector()
CB49 = ile49["CB"].get_vector()

# ─── Obtener átomos de referencia para scoring ────────────────────────────────
HIS46_NE2 = chain_A[46]["NE2"].get_vector()
MET52_SD  = chain_A[52]["SD"].get_vector()
heme_B_FE = chain_B[("H_HEM", 200, " ")]["FE"].get_vector()

# ─── Función: rotar vector alrededor de un eje (Rodrigues) ───────────────────
def rodrigues_rotation(vec: np.ndarray, axis: np.ndarray, theta: float) -> np.ndarray:
    """Rotar `vec` alrededor de `axis` por ángulo `theta` (radianes)."""
    axis = axis / np.linalg.norm(axis)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return (vec * cos_t
            + np.cross(axis, vec) * sin_t
            + axis * np.dot(axis, vec) * (1 - cos_t))


# ─── Construir SG para cada χ₁ canónico ──────────────────────────────────────
# 1. Vector CB-CA (eje del diedro χ₁ es N-CA-CB-SG; simplificamos a eje CB-CG2)
#    Para χ₁: referencia es el vector CA-CB, y SG se coloca a ANGLE_CA_CB_SG
#    del CB en el plano definido por N-CA-CB, rotando por χ₁.

ca_vec = np.array(CA49.get_array())
cb_vec = np.array(CB49.get_array())
n_vec  = np.array(N49.get_array())

# Vector CB→CA (eje sobre el que rotar para χ₁)
axis_chi1 = ca_vec - cb_vec
axis_chi1 = axis_chi1 / np.linalg.norm(axis_chi1)

# Vector de referencia para χ₁ = 0: perpendicular a CB-CA en el plano N-CA-CB
ref_plane = ca_vec - cb_vec
perp = n_vec - cb_vec - np.dot(n_vec - cb_vec, axis_chi1) * axis_chi1
perp = perp / np.linalg.norm(perp)

# Colocar SG a ANGLE_CA_CB_SG respecto al eje CB-CA
# Primero: vector base (perpendicular al eje, en el plano de referencia)
base_sg_dir = (np.cos(np.pi - ANGLE_CA_CB_SG) * (-axis_chi1)
               + np.sin(np.pi - ANGLE_CA_CB_SG) * perp)
base_sg_dir = base_sg_dir / np.linalg.norm(base_sg_dir)

chi1_values = {
    "gauche_minus (-60°)": np.radians(-60.0),
    "trans       (180°) ": np.radians(180.0),
    "gauche_plus (+60°) ": np.radians( 60.0),
}

print("=" * 65)
print("ANÁLISIS DE ROTÁMEROS CYS49 (mutación ILE49→CYS en 1BFR)")
print("=" * 65)
print(f"\nÁtomos anchor reales del PDB (sin modelar):")
print(f"  ILE49 CA  : {ca_vec}")
print(f"  ILE49 CB  : {cb_vec}")
print(f"\nReferencia hopping:")
print(f"  HIS46 NE2 : {np.array(HIS46_NE2.get_array())}")
print(f"  MET52 SD  : {np.array(MET52_SD.get_array())}")
print(f"  HEM B FE  : {np.array(heme_B_FE.get_array())}\n")

best = {"name": None, "sg": None, "d_fe": np.inf}

for name, chi1 in chi1_values.items():
    # Rotar vector base_sg_dir alrededor del eje_chi1 por χ₁
    sg_dir = rodrigues_rotation(base_sg_dir, axis_chi1, chi1)
    sg_pos = cb_vec + BOND_CB_SG * sg_dir

    d_fe   = np.linalg.norm(sg_pos - np.array(heme_B_FE.get_array()))
    d_ne2  = np.linalg.norm(sg_pos - np.array(HIS46_NE2.get_array()))
    d_sd52 = np.linalg.norm(sg_pos - np.array(MET52_SD.get_array()))

    # Calificar: Au-S directo viable < 3.5Å del residuo precedente en la cadena,
    # y SG→NE2 o SG→SD52 < 8Å para hopping
    viable_auS  = "✓ VIABLE"  if d_ne2 < 8.0  else "✗ MARGINAL"
    viable_hop  = "✓ HOPEABLE" if d_sd52 < 10.0 else "✗ DEMASIADO LEJOS"

    print(f"χ₁ = {name}")
    print(f"  SG posición  : [{sg_pos[0]:.3f}, {sg_pos[1]:.3f}, {sg_pos[2]:.3f}]")
    print(f"  SG → HEM FE  : {d_fe:.3f} Å")
    print(f"  SG → HIS46 NE2: {d_ne2:.3f} Å  {viable_auS}")
    print(f"  SG → MET52 SD : {d_sd52:.3f} Å  {viable_hop}")
    print()

    if d_fe < best["d_fe"]:
        best = {"name": name, "sg": sg_pos, "d_fe": d_fe,
                "d_ne2": d_ne2, "d_sd52": d_sd52}

print("─" * 65)
print(f"ROTÁMERO ÓPTIMO (mínima distancia SG→FE): {best['name'].strip()}")
print(f"  SG coordenadas : [{best['sg'][0]:.3f}, {best['sg'][1]:.3f}, {best['sg'][2]:.3f}]")
print(f"  SG → HEM B FE  : {best['d_fe']:.3f} Å")
print(f"  SG → HIS46 NE2 : {best['d_ne2']:.3f} Å")
print(f"  SG → MET52 SD  : {best['d_sd52']:.3f} Å")
print()
print("DIAGNÓSTICO:")
if best["d_ne2"] <= 6.0:
    print("  ✓ SG→HIS46 NE2 ≤ 6Å: hopping CYS49→HIS46 es el paso más rápido de la cadena.")
elif best["d_ne2"] <= 8.0:
    print("  ⚠ SG→HIS46 NE2 ≤ 8Å: hopping viable pero NO es el paso más rápido.")
else:
    print("  ✗ SG→HIS46 NE2 > 8Å: hopping CYS49→HIS46 requiere puentes adicionales.")

# ─── Comparación con aproximación naive anterior ──────────────────────────────
print("\n─" * 65)
print("COMPARACIÓN CON APPROXIMACIÓN NAIVE ANTERIOR (CA + v*3.4):")
v_naive = cb_vec - ca_vec
v_naive = v_naive / np.linalg.norm(v_naive)
sg_naive = ca_vec + v_naive * 3.4
d_naive_fe = np.linalg.norm(sg_naive - np.array(heme_B_FE.get_array()))
d_naive_ne2 = np.linalg.norm(sg_naive - np.array(HIS46_NE2.get_array()))
error_sg = np.linalg.norm(sg_naive - best["sg"])
print(f"  SG naive  → HEM FE : {d_naive_fe:.3f} Å  (rotámero óptimo: {best['d_fe']:.3f} Å)")
print(f"  SG naive  → HIS NE2: {d_naive_ne2:.3f} Å  (rotámero óptimo: {best['d_ne2']:.3f} Å)")
print(f"  Error posicional SG : {error_sg:.3f} Å")
if error_sg > 1.5:
    print(f"  ✗ ERROR SIGNIFICATIVO — diferencia de {error_sg:.1f}Å invalida el análisis previo")
else:
    print(f"  ✓ Error < 1.5Å — resultados previos conservan orden de magnitud")
