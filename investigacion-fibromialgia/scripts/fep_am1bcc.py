#!/usr/bin/env python3
"""
fep_am1bcc.py — P1/Línea 2: Cargas AM1-BCC REALES (AmberTools) para el ligando.

CAMINO CORRECTO: en lugar de Gasteiger heurístico, usa antechamber/sqm de
AmberTools 22 (instalado manualmente en /home/gris/.local/ambertools) para
calcular cargas AM1-BCC estándar académico + tipos GAFF del pramipexole.

Flujo:
  1. RDKit: SMILES -> mol2 3D (coordenadas) del ligando.
  2. antechamber -c bcc -nc 0 -> ligando_gaff.mol2 con cargas AM1-BCC + tipos GAFF.
  3. parmchk2 -> frcmod (params faltantes).
  4. Convierte mol2 (tipos+GG) -> template XML OpenMM (reemplaza Gasteiger).

Requiere AMBERTOOLS_PREFIX (bin/antechamber, bin/sqm, bin/parmchk2).
Si no disponible, falla explícitamente (no fallback silencioso a Gasteiger).
"""
from pathlib import Path
import os, subprocess, sys, tempfile
from openmm import unit
from rdkit import Chem
from rdkit.Chem import AllChem

AMBER = Path(os.environ.get("AMBERTOOLS_PREFIX", "/home/gris/.mamba/envs/amber"))
BIN = AMBER / "bin"
OUT = Path(__file__).resolve().parent.parent / "fep_drd2"
OUT.mkdir(parents=True, exist_ok=True)

# Pramipexole dihydrochloride SMILES (base libre, sin HCl)
SMILES = "CC(C)(C)C1=NCC(C2=CC=C(C=C2)O)N1"

def run(cmd, **kw):
    env = dict(os.environ)
    env["PATH"] = str(BIN) + ":" + env.get("PATH", "")
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, **kw)
    if r.returncode != 0:
        print("STDERR:", r.stderr[-800:])
        sys.exit(f"FAIL: {' '.join(cmd)} rc={r.returncode}")
    return r

print("[1] Extraer ligando UNL de ligand_raw.pdb (el mismo que usa fep_prep.py)")
lig_src = OUT / "ligand_raw.pdb"
lines = open(lig_src).read().splitlines()
unl = [ln for ln in lines if "UNL" in ln and ln.startswith(("ATOM", "HETATM"))]
with tempfile.TemporaryDirectory() as td:
    lig3d = Path(td) / "ligand_raw.pdb"
    with open(lig3d, "w") as f:
        f.write("REMARK extracted UNL from ligand_raw.pdb\n")
        for ln in unl:
            f.write(ln + "\n")
        f.write("END\n")
    print(f"    átomos UNL extraídos: {len(unl)}")

    print("[2] antechamber: AM1-BCC (sqm) + tipos GAFF (desde PDB)")
    out_mol2 = OUT / "ligand_gaff_am1bcc.mol2"
    run([str(BIN/"antechamber"), "-i", str(lig3d), "-fi", "pdb",
         "-o", str(out_mol2), "-fo", "mol2", "-c", "bcc", "-nc", "0",
         "-at", "gaff", "-dr", "no", "-s", "1"])
    print("    AM1-BCC calculado ->", out_mol2.name)

    print("[3] parmchk2: frcmod")
    frcmod = OUT / "ligand_gaff_am1bcc.frcmod"
    run([str(BIN/"parmchk2"), "-i", str(out_mol2), "-f", "mol2",
         "-o", str(frcmod), "-a", "yes"])

# Parsear mol2 -> (name, element, gaff_type, charge) y bonds para XML
def parse_mol2(path):
    lines = open(path).read().splitlines()
    atoms, bonds = [], []
    sec = None
    for ln in lines:
        if ln.startswith("@<TRIPOS>ATOM"):
            sec = "atom"; continue
        if ln.startswith("@<TRIPOS>BOND"):
            sec = "bond"; continue
        if ln.startswith("@<TRIPOS>"):
            sec = None; continue
        if sec == "atom" and ln.strip():
            p = ln.split()
            atoms.append({"idx": int(p[0]), "name": p[1], "el": p[1][0].upper(),
                           "type": p[5], "charge": float(p[8]) if len(p) > 8 else 0.0})
        elif sec == "bond" and ln.strip():
            p = ln.split()
            bonds.append((int(p[1]), int(p[2])))
    return atoms, bonds

print("[4] mol2 -> template XML OpenMM (tipos GAFF + cargas AM1-BCC)")
atoms, bonds = parse_mol2(out_mol2)
# Los tipos GAFF (c3, n3, oh, hc...) YA están definidos en gaff-2.11.xml.
# El template solo declara el residuo UNL con sus átomos/cargas; no redefine tipos.
lines = ['<?xml version="1.0"?>', '<ForceField name="gaff-ligand-am1bcc">',
         ' <Residues>', '  <Residue name="UNL">']
for a in atoms:
    lines.append(f'   <Atom name="{a["name"]}" type="{a["type"]}" charge="{a["charge"]:.4f}"/>')
for i, j in bonds:
    lines.append(f'   <Bond from="{i-1}" to="{j-1}"/>')
lines += ['  </Residue>', ' </Residues>', '</ForceField>']
xml = "\n".join(lines)
xml_path = OUT / "ligand_gaff_template.xml"
xml_path.write_text(xml)
charges = [a["charge"] for a in atoms]
print(f"    átomos: {len(atoms)} | tipos GAFF: {sorted(set(a['type'] for a in atoms))}")
print(f"    carga total ligando: {sum(charges):.3f} e | rango: [{min(charges):.3f}, {max(charges):.3f}]")
print(f"    template -> {xml_path.name}")

# Verificar que el template carga en OpenMM ForceField
from openmm import app
ff = app.ForceField("amber14-all.xml",
                    str(Path(__import__("openmmforcefields").__file__).parent/"ffxml"/"amber"/"gaff"/"ffxml"/"gaff-2.11.xml"),
                    "amber14/tip3p.xml", str(xml_path))
print("[5] ForceField carga template AM1-BCC OK")
print("\n[done] AM1-BCC real listo. Re-correr fep_prep.py + fep_solvate.py + fep_mmpbsa.py.")
