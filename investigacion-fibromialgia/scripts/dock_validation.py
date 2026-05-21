import os
import subprocess
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

import pathlib
base_dir = str(pathlib.Path(__file__).resolve().parent.parent / "datos" / "pdb")
native_pdb = os.path.join(base_dir, "bromocriptine_native.pdb")
dock_sdf = os.path.join(base_dir, "bromocriptine_clean.sdf")
dock_pdbqt = os.path.join(base_dir, "bromocriptine_clean.pdbqt")
receptor_pdbqt = os.path.join(base_dir, "drd2_receptor.pdbqt")
docked_pdbqt = os.path.join(base_dir, "bromocriptine_docked.pdbqt")
docked_sdf = os.path.join(base_dir, "bromocriptine_docked.sdf")

smiles = "CC(C)C1C(=O)N2CCCC2C3(O1)C(=O)N(C(O3)CC4=CC=CC=C4)C(=O)NC5CC6C(CC(N6C)C7=CC=CC=C75)C=C(Br)N"

def run():
    print("1. Preparing ligand with Meeko...")
    subprocess.run(f"mk_prepare_ligand.py -i {dock_sdf} -o {dock_pdbqt}", shell=True)

    print("2. Running Vina docking...")
    cmd_vina = (
        f"vina --receptor {receptor_pdbqt} --ligand {dock_pdbqt} "
        f"--center_x 109.5 --center_y 127.4 --center_z 93.6 "
        f"--size_x 25 --size_y 25 --size_z 25 "
        f"--exhaustiveness 32 --num_modes 10 --out {docked_pdbqt}"
    )
    subprocess.run(cmd_vina, shell=True)

    print("3. Calculating in-place RMSD...")
    # Convert docked PDBQT to SDF for parsing
    os.system(f"obabel {docked_pdbqt} -O {docked_sdf} -m")

    # Load native PDB (even without bond orders, we can just extract coordinates)
    native_mol = Chem.MolFromPDBFile(native_pdb, sanitize=False)
    if not native_mol:
        print("Failed to load native PDB.")
        return

    first_mode_sdf = os.path.join(base_dir, "bromocriptine_docked1.sdf")
    if not os.path.exists(first_mode_sdf):
        print("Docked output not found.")
        return

    docked_mol = next(Chem.SDMolSupplier(first_mode_sdf))
    if not docked_mol:
        print("Failed to load docked SDF.")
        return

    # To compute in-place RMSD, we need a common atom mapping.
    # Since native_mol has no bond orders, we can use Maximum Common Substructure (MCS)
    # or just match the SMILES template to both to get atom orderings.
    template = Chem.MolFromSmiles(smiles)
    
    # Try AllChem.AssignBondOrdersFromTemplate on native_mol to get a clean molecule
    try:
        native_clean = AllChem.AssignBondOrdersFromTemplate(template, native_mol)
    except Exception as e:
        print("AssignBondOrdersFromTemplate failed:", e)
        return

    # Now both native_clean and docked_mol should match the template
    match_native = native_clean.GetSubstructMatch(template)
    match_docked = docked_mol.GetSubstructMatch(template)

    if not match_native or not match_docked:
        print("Substructure match failed.")
        return

    # Extract coordinates
    conf_native = native_clean.GetConformer()
    conf_docked = docked_mol.GetConformer()

    dist_sq_sum = 0.0
    count = 0
    for idx_template in range(template.GetNumAtoms()):
        idx_n = match_native[idx_template]
        idx_d = match_docked[idx_template]
        
        pos_n = conf_native.GetAtomPosition(idx_n)
        pos_d = conf_docked.GetAtomPosition(idx_d)
        
        dist_sq_sum += (pos_n.x - pos_d.x)**2 + (pos_n.y - pos_d.y)**2 + (pos_n.z - pos_d.z)**2
        count += 1

    rmsd = np.sqrt(dist_sq_sum / count)
    print(f"In-place Heavy-Atom RMSD of Top Pose vs Crystal: {rmsd:.2f} Angstroms")

if __name__ == "__main__":
    run()
