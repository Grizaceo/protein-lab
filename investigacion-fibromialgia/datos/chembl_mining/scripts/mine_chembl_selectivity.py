import json
import os
import csv
import subprocess

# Paths
WORKSPACE_DIR = r"\\wsl.localhost\Ubuntu\home\gris\.hermes\workspace\protein-lab"
SCRATCH_DIR = r"C:\Users\usuario\.gemini\antigravity\scratch"
MINING_DIR = os.path.join(WORKSPACE_DIR, "investigacion-fibromialgia", "datos", "chembl_mining")
os.makedirs(MINING_DIR, exist_ok=True)

CHEMBL_API = r"C:\Users\usuario\.gemini\config\plugins\science\skills\chembl_database\scripts\chembl_api.py"

def load_json(filename):
    path = os.path.join(SCRATCH_DIR, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def get_median(values):
    if not values:
        return None
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n % 2 == 1:
        return sorted_vals[n // 2]
    else:
        return (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2.0

def process_selectivity():
    print("Loading activities...")
    drd2_ki = load_json("CHEMBL217_Ki.json")
    drd2_ic50 = load_json("CHEMBL217_IC50.json")
    drd2_ec50 = load_json("CHEMBL217_EC50.json")
    
    drd3_ki = load_json("CHEMBL234_Ki.json")
    drd3_ic50 = load_json("CHEMBL234_IC50.json")
    drd3_ec50 = load_json("CHEMBL234_EC50.json")
    
    print(f"Loaded DRD2 activities: Ki={len(drd2_ki)}, IC50={len(drd2_ic50)}, EC50={len(drd2_ec50)}")
    print(f"Loaded DRD3 activities: Ki={len(drd3_ki)}, IC50={len(drd3_ic50)}, EC50={len(drd3_ec50)}")
    
    # Organize by compound and activity type
    # {molecule_id: {type: [values]}}
    def group_by_molecule(activities):
        grouped = {}
        for act in activities:
            mol_id = act.get("molecule_chembl_id")
            if not mol_id:
                continue
            
            # Use normalized_value_nM if available
            val = act.get("normalized_value_nM")
            if val is None:
                # Fallback to standard_value
                val_str = act.get("standard_value")
                if val_str is not None:
                    try:
                        val = float(val_str)
                    except ValueError:
                        continue
            
            if val is None or val <= 0:
                continue
                
            # Filter for exact binding values (relation '=' or similar)
            relation = act.get("standard_relation") or act.get("relation") or "="
            if relation not in ["=", "<", "<="]:
                continue
                
            grouped.setdefault(mol_id, []).append({
                "value": val,
                "smiles": act.get("canonical_smiles"),
                "relation": relation
            })
        return grouped

    d2_ki_mols = group_by_molecule(drd2_ki)
    d2_ic50_mols = group_by_molecule(drd2_ic50)
    d2_ec50_mols = group_by_molecule(drd2_ec50)
    
    d3_ki_mols = group_by_molecule(drd3_ki)
    d3_ic50_mols = group_by_molecule(drd3_ic50)
    d3_ec50_mols = group_by_molecule(drd3_ec50)
    
    selective_compounds = []
    
    # Types to process
    types_config = [
        ("Ki", d2_ki_mols, d3_ki_mols),
        ("IC50", d2_ic50_mols, d3_ic50_mols),
        ("EC50", d2_ec50_mols, d3_ec50_mols)
    ]
    
    all_selective_mol_ids = set()
    raw_results = []
    
    for act_type, d2_dict, d3_dict in types_config:
        common_mols = set(d2_dict.keys()).intersection(set(d3_dict.keys()))
        print(f"Common molecules for {act_type}: {len(common_mols)}")
        
        for mol_id in common_mols:
            d2_entry = d2_dict[mol_id]
            d3_entry = d3_dict[mol_id]
            
            d2_val = get_median([x["value"] for x in d2_entry])
            d3_val = get_median([x["value"] for x in d3_entry])
            
            if d2_val is None or d3_val is None:
                continue
                
            # Affinity ratio: D3_affinity / D2_affinity
            # Since Ki/IC50/EC50 are concentrations, higher value = lower affinity.
            # Selectivity for D2 over D3 means: D3 value is larger than D2 value.
            # Ratio = Value(D3) / Value(D2) >= 10
            ratio = d3_val / d2_val
            
            if ratio >= 10.0:
                # Find best SMILES
                smiles = next((x["smiles"] for x in d2_entry if x.get("smiles")), None) or \
                         next((x["smiles"] for x in d3_entry if x.get("smiles")), "")
                
                raw_results.append({
                    "chembl_id": mol_id,
                    "smiles": smiles,
                    "affinity_type": act_type,
                    "d2_affinity_nm": d2_val,
                    "d3_affinity_nm": d3_val,
                    "selectivity_ratio": ratio
                })
                all_selective_mol_ids.add(mol_id)
                
    print(f"Total selective compounds before metadata: {len(raw_results)}")
    
    # Batch fetch molecular weights from ChEMBL to avoid incomplete records
    # We can fetch molecules in batches of 20 to get their properties
    mol_properties = {}
    mol_list = list(all_selective_mol_ids)
    batch_size = 20
    
    print("Fetching molecular properties from ChEMBL...")
    for i in range(0, len(mol_list), batch_size):
        batch = mol_list[i:i+batch_size]
        batch_str = ";".join(batch)
        temp_out = os.path.join(SCRATCH_DIR, f"temp_properties_{i}.json")
        cmd = [
            "uv", "run", CHEMBL_API, "molecule",
            "--ids", batch_str,
            "--limit", str(batch_size),
            "--output", temp_out
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(temp_out):
            with open(temp_out, "r") as f:
                try:
                    data = json.load(f)
                    mols = data.get("molecules", [])
                    for m in mols:
                        m_id = m.get("molecule_chembl_id")
                        props = m.get("molecule_properties") or {}
                        mw = props.get("mw_freebase") or m.get("molecule_properties", {}).get("full_mwt")
                        mol_properties[m_id] = {
                            "mw": mw,
                            "pref_name": m.get("pref_name") or ""
                        }
                except Exception as e:
                    print(f"Error parsing properties batch {i}: {e}")
            try:
                os.remove(temp_out)
            except Exception:
                pass
                
    # Classify scaffolds using simple structural/substructural heuristics on SMILES
    def classify_scaffold(smiles):
        if not smiles:
            return "Unknown"
        smiles_lower = smiles.lower()
        # Heuristics based on structural patterns
        if "c1ccc2c(c1)cc(=o)[nH]c2" in smiles_lower or "c(=o)[nH]c1ccc" in smiles_lower or "c(=o)[nH]c2" in smiles_lower:
            if "n1ccn(cc1)" in smiles_lower or "n1ccn(c1)" in smiles_lower:
                return "Aripiprazole-like (Quinolone-piperazine)"
            return "Quinolone / Dihydroquinolone"
        if "c(=o)c1ccc(F)cc1" in smiles_lower or "c(ccc(F)cc1)" in smiles_lower:
            if "c(=o)ccc" in smiles_lower:
                return "Butyrophenone (Haloperidol-like)"
        if "c1cc(c(c(c1)OC)N)" in smiles_lower or "c1cc(c(cc1OC)C(=O)N)" in smiles_lower or "c(=o)n[C@@H]" in smiles_lower:
            return "Benzamide (Sulpiride/Eticlopride-like)"
        if "c1ccc2c(c1)sc3ccccc23" in smiles_lower or "c1ccc2c(c1)oc3ccccc23" in smiles_lower or "c1ccc2c(c1)nc3ccccc23" in smiles_lower:
            return "Tricyclic (Phenothiazine/Thioxanthene-like)"
        if "c1cc2c(c(c1)CCCN)cccc2" in smiles_lower or "c1ccc2[nH]c3ccccc3c2c1" in smiles_lower:
            return "Ergoline / Indole derivative"
        if "n1ccn(cc1)" in smiles_lower or "n1ccn(" in smiles_lower:
            return "Phenylpiperazine derivative"
        if "nc1nc2scc(c2c(=o)[nH]1)" in smiles_lower or "nc1nc(sc1)" in smiles_lower or "c1cc2c(cc1)nc(s2)" in smiles_lower:
            return "Aminothiazole (Pramipexole-like)"
        return "Other Aliphatic/Heterocyclic"

    # Merge properties
    final_compounds = []
    for item in raw_results:
        m_id = item["chembl_id"]
        props = mol_properties.get(m_id, {"mw": None, "pref_name": ""})
        item["molecular_weight"] = props["mw"]
        item["pref_name"] = props["pref_name"]
        item["scaffold"] = classify_scaffold(item["smiles"])
        final_compounds.append(item)
        
    # Sort by selectivity ratio descending
    final_compounds.sort(key=lambda x: x["selectivity_ratio"], reverse=True)
    
    # Save CSV
    csv_file = os.path.join(MINING_DIR, "chembl_d2_selective_compounds.csv")
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "chembl_id", "pref_name", "smiles", "molecular_weight",
            "affinity_type", "d2_affinity_nm", "d3_affinity_nm",
            "selectivity_ratio", "scaffold"
        ])
        for c in final_compounds:
            writer.writerow([
                c["chembl_id"],
                c["pref_name"],
                c["smiles"],
                c["molecular_weight"],
                c["affinity_type"],
                f"{c['d2_affinity_nm']:.3f}",
                f"{c['d3_affinity_nm']:.3f}",
                f"{c['selectivity_ratio']:.2f}",
                c["scaffold"]
            ])
            
    print(f"Saved {len(final_compounds)} selective compounds to {csv_file}")
    
    # Print summary statistics for markdown report
    scaffolds_count = {}
    for c in final_compounds:
        scaffolds_count[c["scaffold"]] = scaffolds_count.get(c["scaffold"], 0) + 1
        
    print("Scaffold Counts:")
    for sc, count in sorted(scaffolds_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {sc}: {count}")

if __name__ == "__main__":
    process_selectivity()
