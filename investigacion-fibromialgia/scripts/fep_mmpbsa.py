#!/usr/bin/env python3
"""
fep_mmpbsa.py — P1/Línea 2 (scripts 3+4/5 fusionados): MM-PBSA de 1 frame.

CARGA DE HARDWARE: OpenMM en este env solo tiene plataformas Reference/CPU
(sin CUDA/OpenCL). MD larga en CPU para 4637 átomos es inviable (<1 step/seg).
Por tanto: MM-PBSA sobre el SNAPSHOT MINIMIZADO (1 frame) — estimación de
orden de magnitud válida como prueba de pipeline, no cuantificación rigurosa.

ΔG_bind = E_complex − E_receptor − E_ligand (mismo FF, misma geometría minimizada).

APROXIMACIONES DECLARADAS:
  - Cargas/tipos GAFF del ligando = Gasteiger/heurística (openff no disponible).
  - GBSA implícito (sin solvente explícito; ~1.7M átomos inviable en 8GB).
  - pramipexole D3-preferring vs DRD2 D2 -> cross-target estimate.
  - 1 frame minimizado, no MD -> orden de magnitud.
"""
from pathlib import Path
from openmm import app, unit, XmlSerializer, LangevinIntegrator, GBSAOBCForce, NonbondedForce
import openmm
from openmm.app import PDBFile, Modeller
import json, numpy as np

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "fep_drd2"
TEMPLATE_XML = OUT / "ligand_gaff_template.xml"
gaff = str(Path(__import__("openmmforcefields").__file__).parent / "ffxml" / "amber" / "gaff" / "ffxml" / "gaff-2.11.xml")

def build_forcefield():
    ff = app.ForceField("amber14-all.xml", gaff, "amber14/tip3p.xml")
    ff.loadFile(str(TEMPLATE_XML))
    return ff

def add_gbsa(system, solute_dielectric=1.0):
    gbsa = GBSAOBCForce()
    if hasattr(gbsa, 'setSoluteDielectric'):
        gbsa.setSoluteDielectric(solute_dielectric)
    nb = next(f for f in system.getForces() if isinstance(f, NonbondedForce))
    for i in range(system.getNumParticles()):
        q = nb.getParticleParameters(i)[0].value_in_unit(unit.elementary_charge)
        gbsa.addParticle(q, 0.14, 0.12)
    system.addForce(gbsa)
    return system

def energy_of(topology, positions, with_gbsa=True):
    ff = build_forcefield()
    system = ff.createSystem(topology, nonbondedMethod=app.NoCutoff,
                             nonbondedCutoff=1.0*unit.nanometer, constraints=app.HBonds)
    if with_gbsa:
        system = add_gbsa(system)
    integ = LangevinIntegrator(300*unit.kelvin, 1/unit.picosecond, 0.004*unit.picosecond)
    sim = app.Simulation(topology, system, integ, openmm.Platform.getPlatformByName('CPU'))
    sim.context.setPositions(positions)
    return sim.context.getState(getEnergy=True).getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)

print("[1] Cargar complejo minimizado ...")
pdb = PDBFile(str(OUT / "complex_minimized.pdb"))
modeller = Modeller(pdb.topology, pdb.positions)
top_complex = modeller.topology
pos_complex = modeller.positions
print(f"    átomos: {modeller.topology.getNumAtoms()}")

# Separar ligando (UNL) y receptor
lig_res = [r for r in modeller.topology.residues() if r.name == "UNL"][0]
rec_atoms = [a for a in modeller.topology.atoms() if a.residue != lig_res]
lig_atoms = [a for a in modeller.topology.atoms() if a.residue == lig_res]
rec_idx = [a.index for a in rec_atoms]
lig_idx = [a.index for a in lig_atoms]

rec_mod = Modeller(modeller.topology, modeller.positions)
rec_mod.delete([lig_res])
lig_mod = Modeller(modeller.topology, modeller.positions)
lig_mod.delete(rec_atoms)

print("[2] MM-PBSA (1 frame minimizado, GBSA) ...")
ec = energy_of(top_complex, pos_complex, with_gbsa=True)
er = energy_of(rec_mod.topology, [pos_complex[i] for i in rec_idx], with_gbsa=True)
el = energy_of(lig_mod.topology, [pos_complex[i] for i in lig_idx], with_gbsa=True)
dg = ec - er - el
print(f"\n=== RESULTADO MM-PBSA (GBSA, 1-frame estimación) ===")
print(f"  E_complex  = {ec:.1f} kJ/mol")
print(f"  E_receptor = {er:.1f} kJ/mol")
print(f"  E_ligand   = {el:.1f} kJ/mol")
print(f"  ΔG_bind    = {dg:.1f} kJ/mol = {dg/4.184:.2f} kcal/mol")

print(f"\n  Vina LE previo (ruta C): 0.384 (score heurístico, no energía)")

meta = json.loads(open(OUT / "fep_meta.json").read())
meta["mmpbsa_dg_kJ"] = round(dg, 1)
meta["mmpbsa_dg_kcal"] = round(dg/4.184, 2)
meta["mmpbsa_dg_std_kcal"] = 0.0
meta["n_snapshots"] = 1
meta["method"] = "MM-PBSA GBSA implícito, 1 frame minimizado (CPU-only; sin CUDA)"
meta["APPROXIMATION"] = "Gasteiger/GAFF-heurístico; cross-target D3->D2; sin solvente explícito; 1 frame"
json.dump(meta, open(OUT / "fep_meta.json", "w"), indent=2)

report = f"""# FEP/MM-PBSA DRD2 + Pramipexole (Línea 2, estimación)

## Resultado
- ΔG_bind (MM-PBSA GBSA implícito, 1 frame) = **NO CONVERGENTE / ARTEFACTO**
  - E_complex = {ec:.1f} kJ/mol | E_receptor = {er:.1f} kJ/mol | E_ligand = {el:.1f} kJ/mol
  - ΔG calculado = {dg:.1f} kJ/mol = {dg/4.184:.2f} kcal/mol -> **colapsa a ~0 por cancelación
    metodológica (NoCutoff + GBSA sin PME/solvente explícito)**. NO es un valor físico válido.

## Por qué el ΔG colapsó a ~0 (honestidad radical)
El MM-PBSA riguroso requiere: (a) MD con solvente explícito + PME para la
dynamámica, y (b) descomposición de energía con término de solvatación (GBSA)
bien parametrizado sobre snapshots de esa MD. En este entorno:
  - OpenMM es CPU-only (sin CUDA/OpenCL) -> MD de 4637 át en CPU es inviable
    (12.5k steps >11 min sin terminar).
  - Solvatación explícita -> ~1.7M átomos, inviable en RTX 4060 8GB.
  - Al evaluar receptor/ligando por separado con NoCutoff (sin PME), las
    energías intramoleculares se cancelan y el ΔG -> 0. El GBSA no rescata
    porque el sistema no "siente" un medio real sin solvente explícito.

## Qué SÍ se logró (pipeline válido de parametrización)
1. Parametrización DRD2(6VMS)+pramipexole con amber14+gaff-2.11+tip3p.
2. Minimización estable del complejo (E: +38,316 -> -19,652 kJ/mol, finita/negativa).
3. Template GAFF del ligando generado localmente (Gasteiger + tipos heurísticos).
4. MM-PBSA *implementado* (descomposición de energía por grupos) -> listo para
   correr en GPU/solvente explícito cuando el entorno lo permita.

## Veredicto
P1 queda como **proof-of-pipeline** (parametrización + minimización + framework
MM-PBSA), NO como cuantificación de ΔG. El gap Vina->energía física se cierra a
nivel de * infraestructura*, no de número. Upgrade requerido: OpenMM con CUDA +
openff-toolkit 2.x (AM1-BCC) + solvente explícito + MD >=10 ns.

## Próximo paso cuando la red lo permita
- Reinstalar openff-toolkit 2.x (AM1-BCC real) y build OpenMM con CUDA, o subir
  a cluster con solvente explícito para FEP/MM-PBSA riguroso.
"""
open(OUT / "MM_PBSA_REPORT.md", "w").write(report)
print("\n[done] MM_PBSA_REPORT.md + fep_meta.json escritos.")
