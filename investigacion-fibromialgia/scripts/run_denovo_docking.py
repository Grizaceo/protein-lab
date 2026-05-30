#!/usr/bin/env python3
"""
run_denovo_docking.py
Pipeline to select de novo candidates, prepare 3D conformers, convert to PDBQT,
execute AutoDock Vina docking against DRD2 and DRD3, and analyze contact interactions.
"""

import os
import sys
import math
import csv
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation
from vina import Vina

# Configuration
BASE_DIR = "/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia"
DOCKING_DIR = os.path.join(BASE_DIR, "docking_runs")
ADHOC_DIR = os.path.join(DOCKING_DIR, "ad_hoc_design")
SEL_DIR = os.path.join(DOCKING_DIR, "selectivity_mapping")

DATA_DIR = os.path.join(SEL_DIR, "data")
OUT_DIR = os.path.join(ADHOC_DIR, "results")
os.makedirs(OUT_DIR, exist_ok=True)

# Grid Box definition (from selectivity mapping)
BOX_CENTER = [109.365, 124.746, 100.388]
BOX_SIZE = [22.0, 22.0, 22.0]

# Key Receptors
DRD2_PDB = os.path.join(DATA_DIR, "drd2_aligned.pdb")
DRD3_PDB = os.path.join(DATA_DIR, "drd3_aligned.pdb")
DRD2_PDBQT = os.path.join(DATA_DIR, "drd2.pdbqt")
DRD3_PDBQT = os.path.join(DATA_DIR, "drd3.pdbqt")

def select_compounds():
    """
    Selects Top 5 by selectivity and Top 3 by CNS MPO >= 4.5 (excluding overlaps),
    and adds Pramipexole as control.
    """
    keys_csv = os.path.join(ADHOC_DIR, "generative_adhoc_keys.csv")
    profiles_csv = os.path.join(ADHOC_DIR, "generative_admet_bbb_profiles.csv")
    
    print("[INFO] Selecting candidates from CSV files...")
    df_keys = pd.read_csv(keys_csv)
    df_prof = pd.read_csv(profiles_csv)
    
    # 1. Top 5 by selectivity ratio
    df_keys_sorted = df_keys.sort_values(by="pred_selectivity_ratio", ascending=False)
    top5_sel = df_keys_sorted.head(5)
    
    # Extract smiles for top 5
    top5_smiles = top5_sel["smiles"].tolist()
    
    print("Top 5 by Selectivity Ratio:")
    for idx, row in top5_sel.iterrows():
        print(f"  - {row['smiles']} (Ratio: {row['pred_selectivity_ratio']:.2f}x)")
        
    # 2. Top 3 by CNS MPO >= 4.5 excluding overlaps and pramipexole
    pramipexole_smiles = "CCCNC1CCc2nc(N)sc2CC1"
    
    # Filter out top 5 smiles and pramipexole from profiles
    df_prof_filtered = df_prof[
        (~df_prof["smiles"].isin(top5_smiles)) & 
        (df_prof["smiles"] != pramipexole_smiles) &
        (df_prof["CNS_MPO"] >= 4.5)
    ]
    
    # Sort remaining by selectivity ratio (or CNS MPO) to get top 3
    df_prof_sorted = df_prof_filtered.sort_values(by="pred_selectivity_ratio", ascending=False)
    top3_cns = df_prof_sorted.head(3)
    
    top3_smiles = top3_cns["smiles"].tolist()
    
    print("\nTop 3 by CNS MPO (>=4.5, excluding overlaps):")
    for idx, row in top3_cns.iterrows():
        print(f"  - {row['smiles']} (CNS MPO: {row['CNS_MPO']:.2f}, Ratio: {row['pred_selectivity_ratio']:.2f}x)")
        
    # Combine list
    compounds = []
    
    # Add Top 5
    for rank, (idx, row) in enumerate(top5_sel.iterrows(), start=1):
        compounds.append({
            "name": f"Denovo_Sel_{rank}",
            "smiles": row["smiles"],
            "category": "Top Selectivity",
            "qsar_selectivity": row["pred_selectivity_ratio"],
            "qsar_d2_nm": row["pred_d2_affinity_nm"],
            "qsar_d3_nm": row["pred_d3_affinity_nm"]
        })
        
    # Add Top 3 CNS MPO
    for rank, (idx, row) in enumerate(top3_cns.iterrows(), start=1):
        compounds.append({
            "name": f"Denovo_CNS_{rank}",
            "smiles": row["smiles"],
            "category": "Top CNS MPO",
            "qsar_selectivity": row["pred_selectivity_ratio"],
            "qsar_d2_nm": row["pred_d2_affinity_nm"],
            "qsar_d3_nm": row["pred_d2_affinity_nm"] * row["pred_selectivity_ratio"] # reconstruct pred_d3
        })
        
    # Add Pramipexole Control
    compounds.append({
        "name": "Pramipexol_Control",
        "smiles": pramipexole_smiles,
        "category": "Control Positivo",
        "qsar_selectivity": 16.87,
        "qsar_d2_nm": 1.42,
        "qsar_d3_nm": 23.88
    })
    
    return compounds

def pdb_to_pdbqt(pdb_path, pdbqt_path):
    """
    Converts receptor PDB to PDBQT format by stripping hydrogens,
    adding basic charges and Autodock atom types.
    """
    print(f"[INFO] Converting receptor: {os.path.basename(pdb_path)} -> {os.path.basename(pdbqt_path)}")
    with open(pdb_path, 'r') as f_in, open(pdbqt_path, 'w') as f_out:
        for line in f_in:
            if line.startswith(("ATOM", "HETATM")):
                name = line[12:16].strip()
                element = line[76:78].strip()
                if not element:
                    element = name[0]
                    if element in '123456789':
                        element = name[1]
                
                element = element.upper()
                if element == 'H':
                    continue
                
                charge = " 0.000"
                ad_type = element
                if element == 'C':
                    resname = line[17:20].strip()
                    if resname in ['PHE', 'TYR', 'TRP'] and name in ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'CH2']:
                        ad_type = 'A'
                
                base_line = line[:56].ljust(70)
                pdbqt_line = f"{base_line}{charge}    {ad_type:<2}\n"
                f_out.write(pdbqt_line)

def prepare_ligand(name, smiles, output_path):
    """
    Converts SMILES to 3D conformer and exports to PDBQT using RDKit and Meeko.
    """
    print(f"[INFO] Preparing ligand conformers for {name}...")
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Could not parse SMILES for {name}: {smiles}")
        
    mol = Chem.AddHs(mol)
    
    # Embed 3D conformer with a robust seed
    res = AllChem.EmbedMolecule(mol, randomSeed=42, maxAttempts=1000)
    if res == -1:
        # Fallback to random coordinates if standard embed fails
        res = AllChem.EmbedMolecule(mol, randomSeed=42, useRandomCoords=True)
        
    AllChem.MMFFOptimizeMolecule(mol)
    
    # Use meeko to prepare ligand
    preparator = MoleculePreparation()
    preparator.prepare(mol)
    pdbqt_str = preparator.write_pdbqt_string()
    
    with open(output_path, "w") as f:
        f.write(pdbqt_str)
        
    num_heavy = mol.GetNumHeavyAtoms()
    print(f"  Prepared {name}: {num_heavy} heavy atoms, written to {os.path.basename(output_path)}")
    return num_heavy

def dock_molecule(receptor_pdbqt, ligand_pdbqt, output_pose_pdbqt):
    """
    Runs Vina docking.
    """
    v = Vina(sf_name='vina', cpu=4, seed=42)
    v.set_receptor(receptor_pdbqt)
    v.set_ligand_from_file(ligand_pdbqt)
    
    v.compute_vina_maps(center=BOX_CENTER, box_size=BOX_SIZE)
    
    v.dock(exhaustiveness=8, n_poses=9)
    
    # Write poses
    v.write_poses(output_pose_pdbqt, n_poses=9, overwrite=True)
    
    energies = v.energies(n_poses=9)
    best_score = energies[0][0]
    return best_score

def parse_pdbqt_atoms(filepath):
    """
    Parses atoms from the FIRST MODEL of a PDBQT file.
    """
    atoms = []
    current_model = 1
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("MODEL"):
                parts = line.split()
                if len(parts) > 1:
                    current_model = int(parts[1])
                if current_model > 1:
                    break
            elif line.startswith("ENDMDL"):
                break
            elif line.startswith("ATOM") or line.startswith("HETATM"):
                try:
                    atom_id = int(line[6:11])
                    atom_name = line[12:16].strip()
                    res_name = line[17:20].strip()
                    chain = line[21]
                    res_num = int(line[22:26])
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    element = line[76:78].strip()
                    
                    atoms.append({
                        'atom_id': atom_id,
                        'atom_name': atom_name,
                        'res_name': res_name,
                        'chain': chain,
                        'res_num': res_num,
                        'x': x,
                        'y': y,
                        'z': z,
                        'element': element
                    })
                except Exception:
                    continue
    return atoms

def analyze_interactions(receptor_atoms, ligand_atoms, threshold=4.0):
    """
    Identifies contact residues within threshold of any ligand atom.
    Returns contact list sorted by res_num.
    """
    contacts = {}
    for r_atom in receptor_atoms:
        r_coord = (r_atom['x'], r_atom['y'], r_atom['z'])
        min_dist = float('inf')
        for l_atom in ligand_atoms:
            l_coord = (l_atom['x'], l_atom['y'], l_atom['z'])
            dist = math.sqrt(
                (r_coord[0] - l_coord[0])**2 +
                (r_coord[1] - l_coord[1])**2 +
                (r_coord[2] - l_coord[2])**2
            )
            if dist < min_dist:
                min_dist = dist
        
        if min_dist <= threshold:
            res_key = (r_atom['chain'], r_atom['res_num'], r_atom['res_name'])
            if res_key not in contacts:
                contacts[res_key] = min_dist
            else:
                contacts[res_key] = min(contacts[res_key], min_dist)
                
    sorted_contacts = sorted(contacts.items(), key=lambda x: x[0][1])
    return [
        {
            'chain': k[0],
            'res_num': k[1],
            'res_name': k[2],
            'distance': round(v, 2)
        } for k, v in sorted_contacts
    ]

def check_specific_interactions(contacts, key_residues):
    """
    Checks if specific key residues are in the contact list.
    key_residues: list of ints (residue numbers)
    """
    present = []
    for c in contacts:
        if c['res_num'] in key_residues:
            present.append(f"{c['res_name']}{c['res_num']} ({c['distance']}Å)")
    return ", ".join(present) if present else "Ninguna"

def main():
    print("="*80)
    print("           PIPELINE DE DOCKING MOLECULAR Y ANALISIS BIOFISICO")
    print("="*80)
    
    # 1. Selection
    compounds = select_compounds()
    print(f"\n[INFO] Selected {len(compounds)} compounds for validation.\n")
    
    # 2. Receptors
    if not os.path.exists(DRD2_PDBQT):
        pdb_to_pdbqt(DRD2_PDB, DRD2_PDBQT)
    if not os.path.exists(DRD3_PDBQT):
        pdb_to_pdbqt(DRD3_PDB, DRD3_PDBQT)
        
    print(f"[INFO] Receptor DRD2: {DRD2_PDBQT}")
    print(f"[INFO] Receptor DRD3: {DRD3_PDBQT}")
    
    receptor_atoms_d2 = parse_pdbqt_atoms(DRD2_PDBQT)
    receptor_atoms_d3 = parse_pdbqt_atoms(DRD3_PDBQT)
    print(f"  Parsed {len(receptor_atoms_d2)} atoms from DRD2.")
    print(f"  Parsed {len(receptor_atoms_d3)} atoms from DRD3.")
    
    results = []
    
    # Key residues to search for in contacts
    # DRD2: Asp114 (Anchor), Ser163 (TM4 selectivity), Ile183 (ECL2 selectivity), Ile109 (TM3 selectivity), His106 (ECL1 selectivity)
    d2_keys = [106, 109, 114, 163, 183]
    # DRD3: Asp110 (Anchor), Ala161 (TM4 selectivity), Ser182 (ECL2 selectivity), Val105 (TM3 selectivity), Cys102 (ECL1 selectivity)
    d3_keys = [102, 105, 110, 161, 182]
    
    # 3. Docking loop
    for cp in compounds:
        name = cp["name"]
        smiles = cp["smiles"]
        category = cp["category"]
        
        lig_pdbqt = os.path.join(OUT_DIR, f"{name.lower()}.pdbqt")
        num_heavy = prepare_ligand(name, smiles, lig_pdbqt)
        
        # DRD2 Docking
        d2_poses = os.path.join(OUT_DIR, f"{name.lower()}_docked_drd2.pdbqt")
        print(f"  [DOCK] Running docking against DRD2...")
        score_d2 = dock_molecule(DRD2_PDBQT, lig_pdbqt, d2_poses)
        
        # Analyze DRD2 contacts
        lig_atoms_d2 = parse_pdbqt_atoms(d2_poses)
        contacts_d2 = analyze_interactions(receptor_atoms_d2, lig_atoms_d2)
        d2_interactions = check_specific_interactions(contacts_d2, d2_keys)
        
        # DRD3 Docking
        d3_poses = os.path.join(OUT_DIR, f"{name.lower()}_docked_drd3.pdbqt")
        print(f"  [DOCK] Running docking against DRD3...")
        score_d3 = dock_molecule(DRD3_PDBQT, lig_pdbqt, d3_poses)
        
        # Analyze DRD3 contacts
        lig_atoms_d3 = parse_pdbqt_atoms(d3_poses)
        contacts_d3 = analyze_interactions(receptor_atoms_d3, lig_atoms_d3)
        d3_interactions = check_specific_interactions(contacts_d3, d3_keys)
        
        # Compute calculations
        le_d2 = -score_d2 / num_heavy
        le_d3 = -score_d3 / num_heavy
        delta_g = score_d2 - score_d3  # Negative value means selective for DRD2
        
        results.append({
            "Name": name,
            "SMILES": smiles,
            "Category": category,
            "Heavy_Atoms": num_heavy,
            "Affinity_D2": round(score_d2, 2),
            "LE_D2": round(le_d2, 3),
            "Affinity_D3": round(score_d3, 2),
            "LE_D3": round(le_d3, 3),
            "Delta_G_Selectivity": round(delta_g, 2),
            "D2_Contacts": d2_interactions,
            "D3_Contacts": d3_interactions,
            "QSAR_Ratio": round(cp["qsar_selectivity"], 2),
            "QSAR_D2_nM": round(cp["qsar_d2_nm"], 3)
        })
        
        print(f"  [RESULT] DRD2: {score_d2:.2f} (LE: {le_d2:.3f}) | DRD3: {score_d3:.2f} (LE: {le_d3:.3f}) | DeltaG: {delta_g:.2f} kcal/mol\n")
        
    # Write to CSV
    results_csv = os.path.join(ADHOC_DIR, "drd2_vs_drd3_denovo_docking_results.csv")
    with open(results_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\n[INFO] Docking completed successfully. Results saved in: {results_csv}\n")
    
    # Generate Markdown table
    print("\n" + "="*80)
    print("                          TABLA RESUMEN DE RESULTADOS")
    print("="*80)
    print("| Compuesto | Át. Pesados | ΔG DRD2 | LE DRD2 | ΔG DRD3 | LE DRD3 | ΔΔG (D2-D3) | Contactos Clave DRD2 | Contactos Clave DRD3 | QSAR Ratio |")
    print("|---|:---:|:---:|:---:|:---:|:---:|:---:|---|---|:---:|")
    for r in results:
        print(f"| **{r['Name']}** | {r['Heavy_Atoms']} | {r['Affinity_D2']} | {r['LE_D2']} | {r['Affinity_D3']} | {r['LE_D3']} | **{r['Delta_G_Selectivity']}** | {r['D2_Contacts']} | {r['D3_Contacts']} | {r['QSAR_Ratio']}x |")
    print("="*80)

if __name__ == "__main__":
    main()
