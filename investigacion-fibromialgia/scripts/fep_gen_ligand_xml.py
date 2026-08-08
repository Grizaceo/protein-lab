#!/usr/bin/env python3
"""
fep_gen_ligand_xml.py — Genera template GAFF del ligando para OpenMM app.ForceField.

APROXIMACIÓN DECLARADA (honestidad):
  - Cargas: Gasteiger (RDKit), NO AM1-BCC (openff-toolkit no disponible en este
    entorno por proxy de red que solo sirve openff 0.18 yanked).
  - Tipos GAFF: asignados por regla elemental (elemento + hibridación), mapeados
    a nombres de gaff-2.11.xml. Es una aproximación de orden de magnitud, no rigor
    de Antechamber/resp.
  - Uso: MM-PBSA de orden de magnitud para cerrar Línea 2 (gap Vina->energía física).
    No sustituir por AM1-BCC cuando la red lo permita.

Mol: pramipexole (D3-preferring). DRD2 es D2 -> cross-target estimate.
"""
import json
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem

OUT = Path(__file__).resolve().parent.parent / "fep_drd2"
OUT.mkdir(exist_ok=True)
SMI = "CC(C)NCCc1c[nH]c2ccc(CCO)cc12"
mol = Chem.MolFromSmiles(SMI)
mol = Chem.AddHs(mol, addCoords=True)
AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
AllChem.MMFFOptimizeMolecule(mol)
AllChem.ComputeGasteigerCharges(mol)

# Mapeo elemental->tipo GAFF (solo C,N,O,H; pramipexole no tiene otros)
def gaff_type(atom):
    sym = atom.GetSymbol()
    hyb = atom.GetHybridization()
    deg = atom.GetDegree()
    if sym == "C":
        if hyb == Chem.HybridizationType.SP2:
            return "c2" if deg == 2 else "ca"
        return "c3"
    if sym == "N":
        if hyb == Chem.HybridizationType.SP2:
            return "n2" if atom.GetTotalNumHs() == 1 else "na"
        return "n3"
    if sym == "O":
        return "oh" if atom.GetTotalNumHs() == 1 else "os"
    if sym == "H":
        # hidrógeno unido a N/O vs C
        nbr = atom.GetNeighbors()[0] if atom.GetDegree() else None
        if nbr and nbr.GetSymbol() in ("N", "O"):
            return "hn"
        return "hc"
    return "du"  # dummy fallback (no debería ocurrir)

atoms = []
for i, a in enumerate(mol.GetAtoms()):
    gtype = gaff_type(a)
    chg = float(a.GetProp("_GasteigerCharge"))
    atoms.append((i, a.GetSymbol(), gtype, chg, [n.GetIdx() for n in a.GetNeighbors()]))

# Escribir XML de template (OpenMM ForceField residue template)
lines = []
lines.append('<?xml version="1.0"?>')
lines.append('<ForceField>')
lines.append('  <Residues>')
lines.append('    <Residue name="UNL">')
for idx, sym, gtype, chg, _ in atoms:
    lines.append(f'      <Atom name="A{idx}" type="{gtype}" charge="{chg:.4f}"/>')
# bonds (OpenMM template expects integer indices, not atom names)
for b in mol.GetBonds():
    i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
    lines.append(f'      <Bond from="{i}" to="{j}"/>')
lines.append('    </Residue>')
lines.append('  </Residues>')
lines.append('</ForceField>')

xml = "\n".join(lines)
(OUT / "ligand_gaff_template.xml").write_text(xml)
print(f"[ok] ligand_gaff_template.xml escrito: {len(atoms)} átomos")
print("  tipos GAFF:", sorted(set(a[2] for a in atoms)))
# dump atoms for debug
json.dump([{"i": i, "sym": s, "type": t, "q": round(q, 4), "nbr": n}
           for i, s, t, q, n in atoms],
          open(OUT / "ligand_atoms.json", "w"), indent=2)
