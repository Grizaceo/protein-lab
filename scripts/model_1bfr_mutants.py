#!/usr/bin/env python3
"""
model_1bfr_mutants.py
======================
Modelador estructural para el triple mutante (LEU40CYS, VAL43CYS, ILE49CYS) 
en la cadena A de Bacterioferritina de E. coli (1BFR.pdb).

Rotámeros seleccionados para evitar choques estéricos y maximizar el acoplamiento:
- CYS40: gauche+ (+60°)  --> Único rotámero viable sin choques con cadena B.
- CYS43: gauche+ (+60°)  --> Conformación estable luminal.
- CYS49: gauche- (-60°)  --> Rotámero óptimo para interactuar con Heme B FE y HIS46 NE2.
"""

import os
import sys
import numpy as np
from Bio.PDB import PDBParser, PDBIO
from Bio.PDB.Atom import Atom

# Ruta a la estructura original
BFR_IN = "data/pdb/new_chassis/1BFR.pdb"
BFR_OUT = "data/pdb/new_chassis/1BFR_mutant_A.pdb"

if not os.path.exists(BFR_IN):
    sys.exit(f"ERROR: No se encontró la estructura original en '{BFR_IN}'")

# Parámetros geométricos para modelar CYS
BOND_CB_SG = 1.810       # Å (Longitud de enlace estándar CYS)
ANGLE_CACBSG = np.radians(114.4) # Ángulo diedro de la cadena lateral

def rodrigues_rotation(vec, axis, theta):
    """Rota un vector `vec` sobre un eje `axis` por un ángulo `theta` (en radianes)."""
    axis = axis / np.linalg.norm(axis)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return (vec * cos_t
            + np.cross(axis, vec) * sin_t
            + axis * np.dot(axis, vec) * (1 - cos_t))

def mutate_to_cys(chain, resnum, chi1_deg, structure):
    """Mutación in-place de un residuo en la cadena especificada a CYS con rotámero chi1."""
    res_id = (" ", resnum, " ")
    if res_id not in chain:
        print(f"  [!] Advertencia: Residuo {resnum} no se encontró en la cadena {chain.id}")
        return None
    
    res = chain[res_id]
    orig_name = res.resname
    
    # 1. Renombrar el residuo
    res.resname = "CYS"
    
    # 2. Identificar y eliminar átomos de la cadena lateral original (no N, CA, C, O, CB)
    atoms_to_remove = [atom.get_id() for atom in res if atom.get_id() not in ["N", "CA", "C", "O", "CB"]]
    for atom_id in atoms_to_remove:
        res.detach_child(atom_id)
        
    # 3. Modelar la posición del azufre gamma (SG) usando el diedro chi1
    ca = res["CA"].get_vector().get_array()
    cb = res["CB"].get_vector().get_array()
    n = res["N"].get_vector().get_array()
    
    # Eje de rotación CB-CA
    axis_chi1 = ca - cb
    axis_chi1 /= np.linalg.norm(axis_chi1)
    
    # Vector perpendicular en el plano N-CA-CB
    perp = n - cb
    perp -= np.dot(perp, axis_chi1) * axis_chi1
    perp /= np.linalg.norm(perp)
    
    # Vector base de SG en chi1 = 0
    base_dir = (np.cos(np.pi - ANGLE_CACBSG) * (-axis_chi1)
                + np.sin(np.pi - ANGLE_CACBSG) * perp)
    base_dir /= np.linalg.norm(base_dir)
    
    # Aplicar la rotación del diedro chi1
    theta = np.radians(chi1_deg)
    sg_dir = rodrigues_rotation(base_dir, axis_chi1, theta)
    sg_pos = cb + BOND_CB_SG * sg_dir
    
    # 4. Crear e inyectar el átomo SG en el residuo
    max_serial = max(atom.serial_number for atom in structure.get_atoms())
    sg_atom = Atom(
        name="SG",
        coord=sg_pos,
        bfactor=20.0,
        occupancy=1.0,
        altloc=" ",
        fullname=" SG ",
        serial_number=max_serial + 1,
        element="S"
    )
    res.add(sg_atom)
    print(f"  -> Mutado {orig_name}{resnum:3d}A a CYS (χ₁={chi1_deg:+3.0f}°) | SG pos: [{sg_pos[0]:8.3f}, {sg_pos[1]:8.3f}, {sg_pos[2]:8.3f}]")
    return sg_pos

def main():
    print("=" * 70)
    print("MODELADOR ESTRUCTURAL DE TRIPLE MUTANTE 1BFR (Cadena A)")
    print("=" * 70)
    
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("1BFR", BFR_IN)
    model = structure[0]
    
    chain_A = model["A"]
    
    print(f"\nProcesando mutaciones en Cadena A:")
    # Mutaciones de diseño
    sg40 = mutate_to_cys(chain_A, 40,  60.0, structure) # CYS40: gauche+ (+60)
    sg43 = mutate_to_cys(chain_A, 43,  60.0, structure) # CYS43: gauche+ (+60)
    sg49 = mutate_to_cys(chain_A, 49, -60.0, structure) # CYS49: gauche- (-60)
    
    # 5. Guardar la estructura modificada
    io = PDBIO()
    io.set_structure(structure)
    io.save(BFR_OUT)
    
    print(f"\n[✓] Estructura mutada guardada exitosamente en: '{BFR_OUT}'")
    print("=" * 70)

if __name__ == "__main__":
    main()
