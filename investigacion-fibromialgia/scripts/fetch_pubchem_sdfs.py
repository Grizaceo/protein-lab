#!/usr/bin/env python3
"""Descargar SDF desde PubChem para los 3 ligandos problemáticos y extraer SMILES"""
import urllib.request, os, pathlib
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def download_pubchem_sdf(cid, outpath):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/record/SDF?record_type=3d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        with open(outpath, 'wb') as f:
            f.write(resp.read())
    return True

def extract_smiles(sdf_path):
    suppl = Chem.SDMolSupplier(sdf_path, removeHs=False)
    for mol in suppl:
        if mol is None:
            continue
        smiles = Chem.MolToSmiles(mol)
        formula = rdMolDescriptors.CalcMolFormula(mol)
        return smiles, formula
    return None, None

cids = {
    "rolapitant": 10311306,
    "aprepitant": 135413536,
    "bromocriptine": 31101,
}

BASE = pathlib.Path.home() / ".hermes" / "workspace" / "ACTIVE" / "protein-lab"
LIGAND_DIR = BASE / "investigacion-fibromialgia" / "estructuras" / "ligandos_validados"

for name, cid in cids.items():
    print(f"\n=== {name} (CID {cid}) ===")
    sdf_path = LIGAND_DIR / f"{name}_pubchem.sdf"
    try:
        download_pubchem_sdf(cid, sdf_path)
        smiles, formula = extract_smiles(sdf_path)
        if smiles:
            print(f"  Formula: {formula}")
            print(f"  SMILES: {smiles}")
        else:
            print(f"  No mol found in SDF")
    except Exception as e:
        print(f"  ERROR: {e}")
