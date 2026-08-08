#!/usr/bin/env python3
"""
fep_prep.py — P1/Línea 2: Preparación DRD2 + pramipexole para FEP/MM-PBSA.

Receptor DRD2 (6VMS, D2) + pramipexole (D3-preferring agonist).
Parametrización: amber14-all (proteína) + gaff-2.11 (ligando) + TIP3P.
Ligando: template GAFF generado por fep_am1bcc.py con cargas
AM1-BCC reales (AmberTools 22: antechamber + sqm). CAMINO CORRECTO
(en reemplazo de Gasteiger heurístico, bloqueado por proxy de red para openff).

CAVEAT: pramipexole es D3-preferring; DRD2 es D2. ΔG = cross-target estimate.
"""
from pathlib import Path
from openmm import app, unit, XmlSerializer
from pdbfixer import PDBFixer
from rdkit import Chem
from rdkit.Chem import AllChem
import json, os

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "fep_drd2"
RECEPTOR_PDB = BASE / "estructuras" / "drd2_receptor_6VMS.pdb"
LIGAND_PDB = OUT / "ligand_raw.pdb"
LIGAND_PDB = OUT / "ligand_raw.pdb"
TEMPLATE_XML = OUT / "ligand_gaff_template.xml"

print("[1] Fix receptor (remove ions/water) ...")
fixer = PDBFixer(str(RECEPTOR_PDB))
fixer.removeHeterogens(keepWater=False)
fixer.findMissingResidues(); fixer.findNonstandardResidues()
fixer.replaceNonstandardResidues(); fixer.findMissingAtoms(); fixer.addMissingAtoms()
rec_fixed = OUT / "receptor_fixed.pdb"
with open(rec_fixed, "w") as f:
    app.PDBFile.writeFile(fixer.topology, fixer.positions, f)

print("[2] Build ligand 3D + Gasteiger (done by fep_gen_ligand_xml.py) ...")
assert LIGAND_PDB.exists() and TEMPLATE_XML.exists(), "run fep_gen_ligand_xml.py first"

print("[3] Load receptor, add H ...")
rec = app.PDBFile(str(rec_fixed))
rec_mod = app.Modeller(rec.topology, rec.positions)
rec_mod.addHydrogens()

print("[4] Load ligand PDB ...")
lig = app.PDBFile(str(LIGAND_PDB))

print("[5] Merge complex ...")
modeller = app.Modeller(rec_mod.topology, rec_mod.positions)
modeller.add(lig.topology, lig.positions)

print("[6] ForceField: amber14-all + gaff-2.11 + tip3p + ligand template ...")
gaff = str(Path(__import__("openmmforcefields").__file__).parent / "ffxml" / "amber" / "gaff" / "ffxml" / "gaff-2.11.xml")
ff = app.ForceField("amber14-all.xml", gaff, "amber14/tip3p.xml")
ff.loadFile(str(TEMPLATE_XML))  # registra residuo UNL con tipos/cargas GAFF

print("[7] Create system ...")
system = ff.createSystem(modeller.topology, nonbondedMethod=app.NoCutoff,
                         nonbondedCutoff=1.0 * unit.nanometer, constraints=app.HBonds)
print(f"    system OK: {system.getNumParticles()} partículas")

print("[8] Write system.xml + complex.pdb ...")
with open(OUT / "system.xml", "w") as f:
    f.write(XmlSerializer.serialize(system))
with open(OUT / "complex.pdb", "w") as f:
    app.PDBFile.writeFile(modeller.topology, modeller.positions, f)

meta = {
    "receptor": "6VMS (DRD2, D2)",
    "ligand": "pramipexole (D3-preferring agonist)",
    "caveat": "cross-target estimate: pramipexole is D3-preferring; DRD2 is D2",
    "protein_ff": "amber14-all", "ligand_ff": "gaff-2.11",
    "ligand_charges": "AM1-BCC (AmberTools 22 antechamber/sqm) — CAMINO CORRECTO",
    "ligand_types": "GAFF 2.11 assigned by antechamber",
    "water": "tip3p", "n_atoms": system.getNumParticles(),
}
(OUT / "fep_meta.json").write_text(json.dumps(meta, indent=2))
print("[done] system.xml + complex.pdb + fep_meta.json written.")
