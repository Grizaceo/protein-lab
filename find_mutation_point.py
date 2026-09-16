
import numpy as np
import os

def get_coords(pdb_path, residue_num, atom_name="CA", chain="A"):
    # ... (duplicated for script completeness) ...
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM"):
                try:
                    r_num = int(line[22:26])
                    c = line[21]
                    name = line[12:16].strip()
                    if r_num == residue_num and c == chain and name == atom_name:
                        return np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                except: continue
    return None

if __name__ == "__main__":
    from pathlib import Path
    _candidates = [
        Path(__file__).resolve().parent / "data/pdb/new_chassis/1BFR.pdb",
        Path(__file__).resolve().parent / "data/pdb/1BFR.pdb",
        Path(os.path.expanduser("~/.hermes/workspace/ACTIVE/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
        Path(os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
    ]
    bfr_path = str(next((p for p in _candidates if p.exists()), _candidates[0]))

    
    p1 = np.array([-10.608, -8.967, 43.839]) # MET 1 (A)
    p2 = np.array([-2.013, -15.754, 25.579]) # TYR 45 (H)
    
    mid_point = (p1 + p2) / 2.0
    
    print(f"Buscando residuos cerca del punto medio: {mid_point}\n")
    
    candidates = []
    with open(bfr_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and " CA " in line:
                pos = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                d1 = np.linalg.norm(pos - p1)
                d2 = np.linalg.norm(pos - p2)
                
                # Buscamos algo que esté a menos de 12A de ambos
                if d1 < 12.0 and d2 < 12.0:
                    res_name = line[17:20].strip()
                    res_num = line[22:26].strip()
                    chain = line[21]
                    dist_to_mid = np.linalg.norm(pos - mid_point)
                    candidates.append({'name': res_name, 'num': res_num, 'chain': chain, 'mid_dist': dist_to_mid, 'd1': d1, 'd2': d2})
                    
    candidates.sort(key=lambda x: x['mid_dist'])
    
    print("TOP CANDIDATOS PARA MUTACIÓN A TRP (REPETIDOR):")
    for c in candidates[:5]:
        print(f"- {c['name']} {c['num']} (Chain {c['chain']}):")
        print(f"  Distancia al Punto Medio: {c['mid_dist']:.2f} A")
        print(f"  Gap 1: {c['d1']:.2f} A | Gap 2: {c['d2']:.2f} A")
