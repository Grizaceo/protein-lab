
import numpy as np
import os

def get_center_of_mass(pdb_path, atom_filter="FE"):
    coords = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if atom_filter in line[12:16]:
                try:
                    coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                except: continue
    return np.mean(coords, axis=0) if coords else None

def scan_stepping_stones(pdb_path, center_point):
    stones = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and (" TRP " in line or " TYR " in line):
                if " CA " in line:
                    try:
                        pos = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                        dist = np.linalg.norm(pos - center_point)
                        res_name = line[17:20].strip()
                        res_num = line[22:26].strip()
                        chain = line[21]
                        stones.append({'name': res_name, 'num': res_num, 'chain': chain, 'dist': dist})
                    except: continue
    return stones

if __name__ == "__main__":
    from pathlib import Path
    _candidates = [
        Path(__file__).resolve().parent / "data/pdb/new_chassis/1BFR.pdb",
        Path(__file__).resolve().parent / "data/pdb/1BFR.pdb",
        Path(os.path.expanduser("~/.hermes/workspace/ACTIVE/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
        Path(os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
    ]
    bfr_path = str(next((p for p in _candidates if p.exists()), _candidates[0]))

    center = get_center_of_mass(bfr_path)
    
    print("--- 🪜 ESCANEO DE ESCALERA ELECTRÓNICA (TRP/TYR) ---")
    if center is not None:
        stones = scan_stepping_stones(bfr_path, center)
        # Clasificar por distancia al centro para ver la "escalera"
        stones.sort(key=lambda x: x['dist'])
        
        print(f"Encontrados {len(stones)} aminoácidos aromáticos candidatos.")
        print("\nTOP 5 MÁS CERCANOS AL CORE (Lumen Interno):")
        for s in stones[:5]:
            print(f"- {s['name']} {s['num']} (Chain {s['chain']}): a {s['dist']:.2f} A del centro")
            
        print("\nTOP 5 MÁS CERCANOS A LA SUPERFICIE (Cerca del Docking):")
        for s in stones[-5:]:
            print(f"- {s['name']} {s['num']} (Chain {s['chain']}): a {s['dist']:.2f} A del centro")
        
        # Análisis de densidad de la escalera
        diffs = np.diff([s['dist'] for s in stones])
        avg_step = np.mean(diffs)
        print(f"\nSalto promedio entre piedras: {avg_step:.2f} A")
