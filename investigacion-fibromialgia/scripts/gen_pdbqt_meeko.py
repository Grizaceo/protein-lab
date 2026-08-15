#!/usr/bin/env python3
"""Generar PDBQT con Meeko para Vina"""
import os, pathlib
import meeko
from rdkit import Chem

BASE = pathlib.Path.home() / ".hermes" / "workspace" / "ACTIVE" / "protein-lab"
LIGAND_DIR = BASE / "investigacion-fibromialgia" / "estructuras" / "ligandos_validados"

LIGANDS = ["dopamine", "pramipexole", "bromocriptine", "rolapitant", "aprepitant",
           "morphine", "fentanyl", "naloxone"]

for name in LIGANDS:
    sdf_path = LIGAND_DIR / f"{name}_validated.sdf"
    pdbqt_path = LIGAND_DIR / f"{name}_validated.pdbqt"
    
    mol = Chem.MolFromMolFile(str(sdf_path), removeHs=False)
    if mol is None:
        print(f"  {name}: SDF read FAILED")
        continue
    
    try:
        preparator = meeko.MoleculePreparation()
        mol_setups = preparator.prepare(mol)
        for setup in mol_setups:
            pdbqt_str, is_ok, error_msg = meeko.PDBQTWriterLegacy.write_string(setup)
            if is_ok:
                with open(pdbqt_path, 'w') as f:
                    f.write(pdbqt_str)
                print(f"  {name}: OK ({len(pdbqt_str.splitlines())} lines)")
            else:
                print(f"  {name}: Meeko ERROR: {error_msg}")
    except Exception as e:
        print(f"  {name}: Exception: {e}")

print("\n=== Verificación ROOT ===")
for name in LIGANDS:
    pdbqt_path = LIGAND_DIR / f"{name}_validated.pdbqt"
    if pdbqt_path.exists():
        text = pdbqt_path.read_text()
        has_root = "ROOT" in text
        has_endroot = "ENDROOT" in text
        print(f"  {name:18s}: ROOT={'Y' if has_root else 'N'} ENDROOT={'Y' if has_endroot else 'N'}")
