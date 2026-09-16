
import numpy as np
import os

def get_center_of_mass(pdb_path, atom_filter="FE"):
    coords = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if atom_filter in line[12:16]:
                try:
                    x, y, z = line[30:38], line[38:46], line[46:54]
                    if x.strip(): coords.append([float(x), float(y), float(z)])
                except: continue
    return np.mean(coords, axis=0) if coords else None

def find_closest_sulfur(pdb_path, target_point):
    best_dist = float('inf')
    best_res = None
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and (" CYS " in line or " MET " in line):
                if " SG " in line or " SD " in line:
                    try:
                        pos = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                        d = np.linalg.norm(pos - target_point)
                        if d < best_dist:
                            best_dist = d
                            best_res = f"{line[17:20]} {line[22:26]} (Chain {line[21]})"
                    except: continue
    return best_res, best_dist

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
    
    print("--- 🔬 BÚSQUEDA DE PUERTO 'DE PROFUNDIDAD' EN 1BFR ---")
    if center is not None:
        res, dist = find_closest_sulfur(bfr_path, center)
        print(f"Mejor candidato: {res}")
        print(f"Distancia al centro: {dist:.2f} A")
        
        # El cluster Au55 tiene un radio de ~14A. 
        # La distancia efectiva (Gap de tunelamiento) sería:
        effective_gap = dist - 14.0
        print(f"Gap efectivo al core de ORO (Au55): {effective_gap:.2f} A")
        
        if effective_gap < 15.0:
            print("ESTADO: EXCELENTE. Conector directo al core.")
        elif effective_gap < 25.0:
            print("ESTADO: VIABLE. Requiere puente de triptófano (hopping).")
        else:
            print("ESTADO: CRÍTICO. Demasiado profundo.")
