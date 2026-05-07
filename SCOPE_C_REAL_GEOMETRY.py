#!/usr/bin/env python3
"""
SCOPE_C_REAL_GEOMETRY.py
Extrae coordenadas reales del PDB 1BFR y calcula hopping gaps exactos.
NO estimaciones a ojo. Datos puros.

REVISIÓN 2026-04-24:
- Parser reemplazado por BioPython (elimina except silencioso, detecto HETATM correctamente)
- SG de CYS49 calculado con los 3 rotámeros canónicos χ₁ (ver geometry_cys_rotamer.py)
  en lugar de la extensión vectorial naive CA+v*3.4 (error ~2.0 Å confirmado)
- Propagación de incertidumbre en β: rango [1.0, 1.4, 1.6] Å⁻¹
"""
import os
import numpy as np
from Bio.PDB import PDBParser

BFR = os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")

# ── Cargar con BioPython — errores de formato visibles, no silenciados ─────────
_parser = PDBParser(QUIET=True)  # QUIET=True solo suprime warnings de cadenas discontinuas (esperados en 24-mer)
_structure = _parser.get_structure("1BFR", BFR)
_model = _structure[0]

def get_atom(chain: str, resn: str, rnum: int, name: str) -> np.ndarray | None:
    """Devuelve coordenadas (x,y,z) del átomo especificado o None si no existe."""
    try:
        ch = _model[chain]
        # Residuos HETATM tienen clave compuesta en BioPython
        if resn == "HEM":
            res = ch[("H_HEM", rnum, " ")]
        else:
            res = ch[rnum]
        if res.resname.strip() != resn and resn != "HEM":
            return None
        return res[name].get_vector().get_array()
    except (KeyError, AttributeError):
        return None

print("=== PDB 1BFR: Coordenadas Relevantes (Angstrom) ===\n")
print("=== PDB 1BFR: Coordenadas Relevantes (Angstrom) ===\n")
entries = [
    ('A', 'ILE', 49, 'CA'), ('A', 'ILE', 49, 'CB'), ('A', 'ILE', 49, 'CG2'),
    ('A', 'MET', 52, 'CA'), ('A', 'MET', 52, 'CB'), ('A', 'MET', 52, 'SD'),
    ('A', 'HIS', 46, 'CA'), ('A', 'HIS', 46, 'CB'), ('A', 'HIS', 46, 'NE2'),
    ('A', 'VAL', 43, 'CA'), ('A', 'LEU', 40, 'CA'),
    ('B', 'HEM', 200, 'FE'),
]
for entry in entries:
    pos = get_atom(*entry)
    if pos is not None:
        print(f"  {entry[0]} {entry[1]} {entry[2]} {entry[3]:>4s}  :  [{pos[0]:8.3f}, {pos[1]:8.3f}, {pos[2]:8.3f}]")
    else:
        print(f"  {entry[0]} {entry[1]} {entry[2]} {entry[3]:>4s}  :  NOT FOUND")

pos_fe   = get_atom('B', 'HEM', 200, 'FE')
pos_sd52 = get_atom('A', 'MET', 52, 'SD')
pos_ne46 = get_atom('A', 'HIS', 46, 'NE2')
pos_ca49 = get_atom('A', 'ILE', 49, 'CA')
pos_cb49 = get_atom('A', 'ILE', 49, 'CB')
pos_n49  = get_atom('A', 'ILE', 49, 'N')

print("\n=== Distancias Exactas entre Átomos Reales ===")
if all(x is not None for x in [pos_sd52, pos_ne46, pos_ca49, pos_fe]):
    print(f"MET52 SD  →  HIS46 NE2 : {np.linalg.norm(pos_sd52 - pos_ne46):.3f} Å")
    print(f"HIS46 NE2 →  ILE49 CA   : {np.linalg.norm(pos_ne46 - pos_ca49):.3f} Å")
    print(f"MET52 SD  →  HEM B FE   : {np.linalg.norm(pos_sd52 - pos_fe):.3f} Å")
    print(f"HIS46 NE2 →  HEM B FE   : {np.linalg.norm(pos_ne46 - pos_fe):.3f} Å")
    print(f"ILE49 CA  →  HEM B FE   : {np.linalg.norm(pos_ca49 - pos_fe):.3f} Å")
    print(f"MET52 SD  →  ILE49 CA   : {np.linalg.norm(pos_sd52 - pos_ca49):.3f} Å")

# ── CYS49 SG: calculado con rotámeros canónicos χ₁ (REVISIÓN 2026-04-24) ──────
# La aproximación anterior (CA + v*3.4) tenía error posicional ~2.0 Å (confirmado
# por geometry_cys_rotamer.py). Aquí se usan los 3 rotámeros canónicos de CYS.
BOND_CB_SG    = 1.810           # Å  (CYS estándar, AMBER ff19SB)
ANGLE_CACBSG  = np.radians(114.4)  # ángulo C-CB-SG

def _rodrigues(vec, axis, theta):
    axis = axis / np.linalg.norm(axis)
    return (vec * np.cos(theta)
            + np.cross(axis, vec) * np.sin(theta)
            + axis * np.dot(axis, vec) * (1 - np.cos(theta)))

pos_sg_by_rotamer = {}
if pos_ca49 is not None and pos_cb49 is not None and pos_n49 is not None:
    axis_chi1 = pos_ca49 - pos_cb49
    axis_chi1 /= np.linalg.norm(axis_chi1)
    perp = pos_n49 - pos_cb49
    perp -= np.dot(perp, axis_chi1) * axis_chi1
    perp /= np.linalg.norm(perp)
    base_dir = (np.cos(np.pi - ANGLE_CACBSG) * (-axis_chi1)
                + np.sin(np.pi - ANGLE_CACBSG) * perp)
    base_dir /= np.linalg.norm(base_dir)
    for name, chi1 in [("gauche-(-60°)", np.radians(-60)),
                        ("trans  (180°)", np.radians(180)),
                        ("gauche+(+60°)", np.radians( 60))]:
        sg = pos_cb49 + BOND_CB_SG * _rodrigues(base_dir, axis_chi1, chi1)
        pos_sg_by_rotamer[name] = sg

    print(f"\n=== CYS49 SG — Rotámeros Canónicos χ₁ (BioPython, revisión 2026-04-24) ===")
    print(f"{'Rotámero':<18} {'SG→HEM FE':>10} {'SG→HIS NE2':>12} {'SG→MET SD':>12}")
    best_sg, best_d = None, np.inf
    for nm, sg in pos_sg_by_rotamer.items():
        d_fe  = np.linalg.norm(sg - pos_fe)
        d_ne2 = np.linalg.norm(sg - pos_ne46)
        d_sd  = np.linalg.norm(sg - pos_sd52)
        print(f"  {nm:<16} {d_fe:>9.3f} Å {d_ne2:>10.3f} Å {d_sd:>10.3f} Å")
        if d_fe < best_d:
            best_d, best_sg = d_fe, sg
    print(f"\n  ► Rotámero óptimo (min SG→FE): d = {best_d:.3f} Å")
    pos_sg_best = best_sg
else:
    print("\n  ⚠ No se pudo calcular rotámeros CYS49 (falta N49, CA49 o CB49)")
    pos_sg_best = None

# ── Tasas de hopping con propagación de incertidumbre en β ────────────────────
k0 = 1e13   # s⁻¹  (frecuencia nuclear límite)
BETA_VALUES = {"β=1.0 (mín)": 1.0, "β=1.4 (nominal)": 1.4, "β=1.6 (máx)": 1.6}

if all(x is not None for x in [pos_sd52, pos_ne46, pos_fe]) and pos_sg_best is not None:
    gaps_labeled = [
        ("Au NP surf → CYS49 SG†",  None,     pos_sg_best,  "† Distancia Au NP surface→SG depende del tamaño del cluster"),
        ("CYS49 SG  → HIS46 NE2",   pos_sg_best, pos_ne46,  ""),
        ("HIS46 NE2 → MET52 SD",    pos_ne46, pos_sd52,     "← Paso limitante de la cadena"),
        ("MET52 SD  → Heme B FE",   pos_sd52, pos_fe,       ""),
    ]

    print(f"\n=== Tasas de Hopping — Propagación β ∈ [1.0, 1.4, 1.6] Å⁻¹ (k0={k0:.0e} s⁻¹) ===")
    print(f"{'Tramo':<30} {'d (Å)':>7}  {'k β=1.0':>12}  {'k β=1.4':>12}  {'k β=1.6':>12}  {'τ β=1.4':>10}  {'τ β=1.6':>10}")

    k_limits = {}
    for label, p1, p2, note in gaps_labeled:
        if p1 is None:
            # Para el tramo Au→CYS, la distancia depende del cluster; mostrar rango 2-5Å
            for d_au in [2.5, 5.0]:
                row_label = f"  Au NP→SG (d={d_au:.1f}Å)"
                ks = {b: k0 * np.exp(-b * d_au) for b in BETA_VALUES.values()}
                tau14 = 1/ks[1.4]
                tau16 = 1/ks[1.6]
                print(f"  {row_label:<28} {d_au:>7.2f}  {ks[1.0]:>12.2e}  {ks[1.4]:>12.2e}  {ks[1.6]:>12.2e}  {tau14:>10.2e}  {tau16:>10.2e}")
        else:
            d = np.linalg.norm(p2 - p1)
            ks = {b: k0 * np.exp(-b * d) for b in BETA_VALUES.values()}
            tau14 = 1/ks[1.4]
            tau16 = 1/ks[1.6]
            flag = "⚠ LIMITANTE" if "HIS46" in label and "MET52" in label else ""
            print(f"  {label:<30} {d:>7.3f}  {ks[1.0]:>12.2e}  {ks[1.4]:>12.2e}  {ks[1.6]:>12.2e}  {tau14:>10.2e}  {tau16:>10.2e}  {note} {flag}")
            if p1 is pos_ne46 and p2 is pos_sd52:
                k_limits = ks

    if k_limits:
        print(f"\n  TASA GLOBAL (paso limitante HIS46→MET52):")
        print(f"    β=1.0 → k = {k_limits[1.0]:.2e} s⁻¹  τ = {1/k_limits[1.0]:.2e} s")
        print(f"    β=1.4 → k = {k_limits[1.4]:.2e} s⁻¹  τ = {1/k_limits[1.4]:.2e} s  ← nominal")
        print(f"    β=1.6 → k = {k_limits[1.6]:.2e} s⁻¹  τ = {1/k_limits[1.6]:.2e} s")
        print(f"  ✓ Incertidumbre de 2 órdenes de magnitud en τ — SIEMPRE reportar como rango.")
