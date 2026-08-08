#!/usr/bin/env python3
"""
fep_solvate.py — P1/Línea 2 (script 2/5): Minimizar complejo (sin solvente explícito).

DECISIÓN DE HARDWARE: DRD2 6VMS + pramipexole ~4637 átomos. Solvatación
explícita completa -> ~1.7M átomos (inviable en RTX 4060 8GB). Para una
estimación de orden de magnitud de ΔG usamos MM-PBSA con GBSA IMPLÍCITO
sobre el complejo minimizado (snapshot único). Cabe en GPU, es honesto como
estimación; no sustituye MD con solvente explícito cuando haya hardware.

Reconstruye ForceField (amber14 + gaff-2.11 + tip3p + template UNL), carga
complex.pdb, minimiza con L-BFGS. Verifica estabilidad (energía finita/negativa).

APROXIMACIÓN: cargas/tipos GAFF del ligando = Gasteiger/heurística (ver fep_meta.json).
"""
from pathlib import Path
from openmm import app, unit, XmlSerializer, LangevinIntegrator
from openmm.app import PDBFile, Modeller
import json, numpy as np

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "fep_drd2"
TEMPLATE_XML = OUT / "ligand_gaff_template.xml"
gaff = str(Path(__import__("openmmforcefields").__file__).parent / "ffxml" / "amber" / "gaff" / "ffxml" / "gaff-2.11.xml")

print("[1] Reconstruir ForceField ...")
ff = app.ForceField("amber14-all.xml", gaff, "amber14/tip3p.xml")
ff.loadFile(str(TEMPLATE_XML))

print("[2] Cargar complex.pdb (receptor+ligando) ...")
pdb = PDBFile(str(OUT / "complex.pdb"))
modeller = Modeller(pdb.topology, pdb.positions)
print(f"    átomos complejo: {modeller.topology.getNumAtoms()}")

print("[3] Crear system (NoCutoff; GBSA implícito se añade en fep_mmpbsa) ...")
system = ff.createSystem(modeller.topology, nonbondedMethod=app.NoCutoff,
                         nonbondedCutoff=1.0 * unit.nanometer, constraints=app.HBonds)

print("[4] Minimizar (L-BFGS, tol 10 kJ/mol/nm) ...")
integrator = LangevinIntegrator(300 * unit.kelvin, 1 / unit.picosecond,
                                     0.004 * unit.picosecond)
sim = app.Simulation(modeller.topology, system, integrator)
sim.context.setPositions(modeller.positions)
e0 = sim.context.getState(getEnergy=True).getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
print(f"    E inicial: {e0:.1f} kJ/mol")
sim.minimizeEnergy(maxIterations=5000, tolerance=10 * unit.kilojoules_per_mole / unit.nanometer)
st = sim.context.getState(getEnergy=True, getPositions=True)
e1 = st.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
print(f"    E minimizada: {e1:.1f} kJ/mol")

print("[5] Guardar complejo minimizado ...")
with open(OUT / "system_minimized.xml", "w") as f:
    f.write(XmlSerializer.serialize(system))
with open(OUT / "complex_minimized.pdb", "w") as f:
    app.PDBFile.writeFile(modeller.topology, st.getPositions(), f)

stable = np.isfinite(e1) and (e1 < 0)
meta = json.loads(open(OUT / "fep_meta.json").read())
meta["minimized_atoms"] = modeller.topology.getNumAtoms()
meta["E_initial_kJ"] = round(e0, 1)
meta["E_minimized_kJ"] = round(e1, 1)
meta["minimization_stable"] = bool(stable)
meta["solvent"] = "NONE (GBSA implícito en fep_mmpbsa); solvente explícito inviable en 8GB"
json.dump(meta, open(OUT / "fep_meta.json", "w"), indent=2)
print(f"[done] stable={stable}; system_minimized.xml + complex_minimized.pdb escritos.")
if not stable:
    print("  WARNING: energía no finita/negativa -> revisar template GAFF del ligando.")
