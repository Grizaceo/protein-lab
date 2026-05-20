import os
from rdkit import Chem

import pathlib
base_dir = str(pathlib.Path(__file__).resolve().parent.parent / "datos" / "pdb")
native_pdb = os.path.join(base_dir, "bromocriptine_native.pdb")
first_mode_sdf = os.path.join(base_dir, "bromocriptine_docked1.sdf")

native_mol = Chem.MolFromPDBFile(native_pdb, sanitize=False)
docked_mol = next(Chem.SDMolSupplier(first_mode_sdf))

if native_mol and docked_mol:
    native_heavy = sum(1 for atom in native_mol.GetAtoms() if atom.GetAtomicNum() > 1)
    docked_heavy = sum(1 for atom in docked_mol.GetAtoms() if atom.GetAtomicNum() > 1)
    print(f"Native heavy atoms: {native_heavy}")
    print(f"Docked heavy atoms: {docked_heavy}")
else:
    print("Could not load molecules.")
