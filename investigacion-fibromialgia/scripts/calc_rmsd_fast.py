import os
import numpy as np
from rdkit import Chem

base_dir = "/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia/datos/pdb"
native_pdb = os.path.join(base_dir, "bromocriptine_native.pdb")
docked_sdf = os.path.join(base_dir, "bromocriptine_docked1.sdf")

native_mol = Chem.MolFromPDBFile(native_pdb, sanitize=False)
docked_mol = next(Chem.SDMolSupplier(docked_sdf))

# Smarts pattern for bromocriptine to match both molecules
# We use the SMILES but convert it to a template to ensure consistent matching
smiles = "CC(C)C1C(=O)N2CCCC2C3(O1)C(=O)N(C(O3)CC4=CC=CC=C4)C(=O)NC5CC6C(CC(N6C)C7=CC=CC=C75)C=C(Br)N"
template = Chem.MolFromSmiles(smiles)

native_match = native_mol.GetSubstructMatch(template)
docked_match = docked_mol.GetSubstructMatch(template)

if native_match and docked_match:
    conf_native = native_mol.GetConformer()
    conf_docked = docked_mol.GetConformer()
    
    sq_dist = 0.0
    for i in range(len(template.GetAtoms())):
        idx_n = native_match[i]
        idx_d = docked_match[i]
        pos_n = conf_native.GetAtomPosition(idx_n)
        pos_d = conf_docked.GetAtomPosition(idx_d)
        sq_dist += (pos_n.x - pos_d.x)**2 + (pos_n.y - pos_d.y)**2 + (pos_n.z - pos_d.z)**2
        
    rmsd = np.sqrt(sq_dist / len(template.GetAtoms()))
    print(f"RMSD: {rmsd:.2f} Angstroms")
else:
    print(f"Match failed. Native matched: {bool(native_match)}. Docked matched: {bool(docked_match)}")
