import os
from rdkit import Chem
from rdkit.Chem import AllChem
import urllib.request

import pathlib
base_dir = str(pathlib.Path(__file__).resolve().parent.parent / "datos" / "pdb")
native_pdb = os.path.join(base_dir, "bromocriptine_native.pdb")
dock_sdf = os.path.join(base_dir, "bromocriptine_clean.sdf")

# Bromocriptine SMILES from PubChem
smiles = "CC(C)C1C(=O)N2CCCC2C3(O1)C(=O)N(C(O3)CC4=CC=CC=C4)C(=O)NC5CC6C(CC(N6C)C7=CC=CC=C75)C=C(Br)N"

def prepare_ligand():
    # Load template from SMILES
    template = Chem.MolFromSmiles(smiles)
    if not template:
        print("Invalid SMILES.")
        return

    # Load PDB (without sanitization to avoid errors on missing bond orders)
    mol = Chem.MolFromPDBFile(native_pdb, sanitize=False)
    if not mol:
        print("Could not read native PDB.")
        return
        
    # Remove disconnected components if any (like waters, though we used grep to only get 08Y)
    
    # Assign bond orders
    try:
        mol = Chem.AssignBondOrdersFromTemplate(template, mol)
        Chem.SanitizeMol(mol)
        print("Bond orders assigned and sanitized.")
    except Exception as e:
        print(f"AssignBondOrdersFromTemplate failed: {e}")
        # Let's try downloading the ideal SDF directly from PubChem
        print("Downloading SDF from PubChem...")
        url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/bromocriptine/SDF"
        try:
            urllib.request.urlretrieve(url, dock_sdf)
            print("Downloaded SDF.")
            # Ensure it has hydrogens and 3D
            m = next(Chem.SDMolSupplier(dock_sdf))
            m = Chem.AddHs(m)
            AllChem.EmbedMolecule(m, randomSeed=42)
            AllChem.UFFOptimizeMolecule(m)
            w = Chem.SDWriter(dock_sdf)
            w.write(m)
            w.close()
            return
        except Exception as dl_e:
            print(f"Download failed: {dl_e}")
            return

    # Add Hydrogens and preserve 3D coordinates
    mol = Chem.AddHs(mol, addCoords=True)
    
    # Save to SDF
    writer = Chem.SDWriter(dock_sdf)
    writer.write(mol)
    writer.close()
    print(f"Saved cleaned ligand to {dock_sdf}")

if __name__ == "__main__":
    prepare_ligand()
