#!/usr/bin/env python3
"""
Regenerar SDF + PDBQT de rolapitant, aprepitant, bromocriptine
usando SMILES canónicos de PubChem (fórmulas verificadas).
"""
import os, json, subprocess, pathlib
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

os.environ["PATH"] = "/home/gris/.miniconda/envs/protein-lab/bin:" + os.environ["PATH"]

BASE = pathlib.Path.home() / ".hermes" / "workspace" / "ACTIVE" / "protein-lab"
LIGAND_DIR = BASE / "investigacion-fibromialgia" / "estructuras" / "ligandos_validados"

# SMILES con H explícitos de PubChem — limpiar con RDKit
RAW = {
    "rolapitant": "[H]c1c([H])c([H])c([C@@]2(C([H])([H])O[C@@]([H])(c3c([H])c(C(F)(F)F)c([H])c(C(F)(F)F)c3[H])C([H])([H])[H])N([H])C([H])([H])[C@]3(N([H])C(=O)C([H])([H])C3([H])[H])C([H])([H])C2([H])[H])c([H])c1[H]",
    "aprepitant": "[H]c1c([H])c([C@]2([H])N(C([H])([H])c3nn([H])c(=O)n3[H])C([H])([H])C([H])([H])O[C@]2([H])O[C@@]([H])(c2c([H])c(C(F)(F)F)c([H])c(C(F)(F)F)c2[H])C([H])([H])[H])c([H])c([H])c1F",
    "bromocriptine": "[H]O[C@@]12O[C@](N([H])C(=O)[C@]3([H])C([H])=C4c5c([H])c([H])c([H])c6c5c(c(Br)n6[H])C([H])([H])[C@@]4([H])N(C([H])([H])[H])C3([H])[H])(C([H])(C([H])([H])[H])C([H])([H])[H])C(=O)N1[C@@]([H])(C([H])([H])C([H])(C([H])([H])[H])C([H])([H])[H])C(=O)N1C([H])([H])C([H])([H])C([H])([H])[C@]12[H]",
}

EXPECTED = {
    "rolapitant": "C25H26F6N2O2",
    "aprepitant": "C23H21F7N4O3",
    "bromocriptine": "C32H40BrN5O5",
}

def clean_smiles(raw):
    """Remove explicit H and re-sanitize"""
    mol = Chem.MolFromSmiles(raw, sanitize=False)
    if mol is None:
        return None
    mol = Chem.RemoveHs(mol)
    try:
        Chem.SanitizeMol(mol)
    except:
        pass
    return Chem.MolToSmiles(mol)

def generate(name, raw_smiles, expected_formula):
    smiles = clean_smiles(raw_smiles)
    if smiles is None:
        return None, "clean_smiles failed"
    
    mol = Chem.MolFromSmiles(smiles)
    mol_h = Chem.AddHs(mol)
    
    # Embedding robusto
    ps = AllChem.ETKDGv3()
    ps.randomSeed = 42
    ps.maxIterations = 2000
    ps.useRandomCoords = True
    ret = AllChem.EmbedMolecule(mol_h, ps)
    if ret == -1:
        AllChem.EmbedMolecule(mol_h, randomSeed=42, useRandomCoords=True, maxIters=5000)
    
    try:
        AllChem.MMFFOptimizeMolecule(mol_h, maxIters=1000)
    except:
        AllChem.UFFOptimizeMolecule(mol_h, maxIters=1000)
    
    formula = rdMolDescriptors.CalcMolFormula(mol_h)
    if formula != expected_formula:
        return None, f"Formula mismatch: {formula} != {expected_formula}"
    
    sdf_path = LIGAND_DIR / f"{name}_validated.sdf"
    writer = Chem.SDWriter(str(sdf_path))
    writer.write(mol_h)
    writer.close()
    
    pdbqt_path = LIGAND_DIR / f"{name}_validated.pdbqt"
    cmd = f"obabel {sdf_path} -O {pdbqt_path} -xr -p 7.4"
    subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    
    return {
        "name": name,
        "formula": formula,
        "smiles": smiles,
        "sdf": str(sdf_path),
        "pdbqt": str(pdbqt_path) if pdbqt_path.exists() else None,
        "pdbqt_ok": pdbqt_path.exists(),
    }, None

results = {}
for name, raw in RAW.items():
    print(f"\n=== {name} ===")
    res, err = generate(name, raw, EXPECTED[name])
    if err:
        print(f"  ERROR: {err}")
        results[name] = {"error": err}
    else:
        print(f"  Formula: {res['formula']} ✓")
        print(f"  SMILES: {res['smiles']}")
        print(f"  PDBQT: {res['pdbqt_ok']}")
        results[name] = res

# Update manifest
manifest_path = BASE / "investigacion-fibromialgia" / "scripts" / "docking_ligand_manifest.json"
with open(manifest_path) as f:
    manifest = json.load(f)
manifest.update(results)
with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)

ok_count = sum(1 for v in manifest.values() if "error" not in v and v.get("pdbqt_ok"))
print(f"\n=== RESUMEN: {ok_count}/8 ligandos con PDBQT listos ===")
