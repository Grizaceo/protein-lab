import os
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdFMCS

base_dir = "/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia/datos/pdb"
native_pdb = os.path.join(base_dir, "bromocriptine_native.pdb")
docked_sdf = os.path.join(base_dir, "bromocriptine_docked1.sdf")

native_mol = Chem.MolFromPDBFile(native_pdb, sanitize=False)
docked_mol = next(Chem.SDMolSupplier(docked_sdf))

# Remove hydrogens if any
native_heavy = Chem.RemoveHs(native_mol, sanitize=False)
docked_heavy = Chem.RemoveHs(docked_mol, sanitize=False)

# Find MCS to get mapping
mcs = rdFMCS.FindMCS([native_heavy, docked_heavy], atomCompare=rdFMCS.AtomCompare.CompareElements)
if not mcs.canceled:
    patt = Chem.MolFromSmarts(mcs.smartsString)
    match_native = native_heavy.GetSubstructMatch(patt)
    match_docked = docked_heavy.GetSubstructMatch(patt)
    
    if len(match_native) == native_heavy.GetNumAtoms() and len(match_docked) == docked_heavy.GetNumAtoms():
        conf_native = native_heavy.GetConformer()
        conf_docked = docked_heavy.GetConformer()
        
        sq_dist = 0.0
        for i, idx_n in enumerate(match_native):
            idx_d = match_docked[i]
            pos_n = conf_native.GetAtomPosition(idx_n)
            pos_d = conf_docked.GetAtomPosition(idx_d)
            sq_dist += (pos_n.x - pos_d.x)**2 + (pos_n.y - pos_d.y)**2 + (pos_n.z - pos_d.z)**2
            
        rmsd = np.sqrt(sq_dist / len(match_native))
        print(f"RMSD: {rmsd:.2f} Angstroms")
    else:
        print(f"MCS size mismatch. Native match: {len(match_native)}, Docked match: {len(match_docked)}")
        print(f"Total atoms - Native: {native_heavy.GetNumAtoms()}, Docked: {docked_heavy.GetNumAtoms()}")
else:
    print("MCS failed.")
