#!/usr/bin/env python3
"""
Generar SDF + PDBQT de ligandos validados desde SMILES para Paper 2 Docking.
Método: RDKit (SDF) + obabel (PDBQT, como paper original naloxone).
"""
import os, json, subprocess, pathlib
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

os.environ["PATH"] = "/home/gris/.miniconda/envs/protein-lab/bin:" + os.environ["PATH"]

BASE = pathlib.Path.home() / ".hermes" / "workspace" / "ACTIVE" / "protein-lab"
LIGAND_DIR = BASE / "investigacion-fibromialgia" / "estructuras" / "ligandos_validados"
DOCKING_DIR = BASE / "investigacion-fibromialgia" / "estructuras" / "dockings"

LIGAND_DIR.mkdir(parents=True, exist_ok=True)

# SMILES canónicos validados (fórmulas confirmadas vía PubChem)
LIGANDS = {
    "dopamine": "C1=CC(=C(C=C1CCN)O)O",
    "pramipexole": "CCCN[C@H]1CCC2=C(C1)SC(=N2)N",
    "bromocriptine": "[C@@H]12C[C@H](C(=O)N1C(=O)[C@@H]3[C@@]2(O3)CC4=CC=CC=C4)NC(=O)[C@@]56C[C@@H]([C@@H]([C@H]5N6C(=O)CC7=CC=CC=C7)O)Br",
    "rolapitant": "C[C@]12C[C@@H]([C@H]([C@@]1(C)C(=O)N2C)N(C3=CC=CC=C3)C(=O)C)C4=CC(=C(C=C4)F)F",
    "aprepitant": "C[C@@H](C1=CC(=CC=C1)F)N2C[C@H](C[C@]3(C2)CCN(C3=O)C4=CC(=C(C=C4F)F)F)O",
    "morphine": "CN1CC[C@]23[C@@H]4[C@H]1CC5=C2C(=C(C=C5)O)O[C@H]3[C@@H](C=C4)O",
    "fentanyl": "CCC(=O)N(C1CCN(CC1)CCC2=CC=CC=C2)C3=CC=CC=C3",
    "naloxone": "C=CCN1CC[C@]23[C@H]4C(=O)CC[C@@]2([C@H]1CC5=C3C(=C(C=C5)O)O4)O",
}

EXPECTED_FORMULAS = {
    "dopamine": "C8H11NO2",
    "pramipexole": "C10H17N3S",
    "bromocriptine": "C32H40BrN5O5",
    "rolapitant": "C25H26F6N2O2",
    "aprepitant": "C23H21F7N4O3",
    "morphine": "C17H19NO3",
    "fentanyl": "C22H28N2O",
    "naloxone": "C19H21NO4",
}

def generate_sdf(name, smiles, outdir):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, f"SMILES inválido: {smiles}"
    
    mol_h = Chem.AddHs(mol)
    # ETKDGv3 embedding con fallback a random
    try:
        ps = AllChem.ETKDGv3()
        ps.randomSeed = 42
        ps.maxIterations = 1000
        ret = AllChem.EmbedMolecule(mol_h, ps)
        if ret == -1:
            AllChem.EmbedMolecule(mol_h, randomSeed=42, useRandomCoords=True, maxIters=2000)
    except Exception as e:
        return None, f"Embedding failed: {e}"
    
    try:
        AllChem.MMFFOptimizeMolecule(mol_h, maxIters=500)
    except:
        try:
            AllChem.UFFOptimizeMolecule(mol_h, maxIters=500)
        except:
            pass
    
    formula = rdMolDescriptors.CalcMolFormula(mol_h)
    expected = EXPECTED_FORMULAS[name]
    if formula != expected:
        return None, f"Fórmula mismatch: {formula} != {expected}"
    
    sdf_path = outdir / f"{name}_validated.sdf"
    writer = Chem.SDWriter(str(sdf_path))
    writer.write(mol_h)
    writer.close()
    
    # PDBQT via obabel (mismo protocolo naloxone)
    pdbqt_path = outdir / f"{name}_validated.pdbqt"
    cmd = f"obabel {sdf_path} -O {pdbqt_path} -xr -p 7.4"
    subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    
    ok = pdbqt_path.exists()
    return {
        "name": name,
        "formula": formula,
        "sdf": str(sdf_path),
        "pdbqt": str(pdbqt_path) if ok else None,
        "pdbqt_ok": ok,
    }, None

results = {}
for name, smiles in LIGANDS.items():
    print(f"\n=== {name} ===")
    res, err = generate_sdf(name, smiles, LIGAND_DIR)
    if err:
        print(f"  ERROR: {err}")
        results[name] = {"error": err}
    else:
        print(f"  Formula: {res['formula']} ✓")
        print(f"  SDF: {res['sdf']}")
        print(f"  PDBQT: {res['pdbqt']} {'✓' if res['pdbqt_ok'] else '✗'}")
        results[name] = res

manifest = BASE / "investigacion-fibromialgia" / "scripts" / "docking_ligand_manifest.json"
with open(manifest, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n=== RESUMEN ===")
ok_count = sum(1 for v in results.values() if "error" not in v and v.get("pdbqt_ok"))
print(f"SDF generados: {len([v for v in results.values() if 'error' not in v])}/{len(LIGANDS)}")
print(f"PDBQT OK: {ok_count}")
print(f"Manifest: {manifest}")
