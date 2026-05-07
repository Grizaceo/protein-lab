
import numpy as np
import os

if __name__ == "__main__":
    bfr_path = os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")
    
    p1 = np.array([-10.608, -8.967, 43.839]) # MET 1 (A)
    p2 = np.array([-2.013, -15.754, 25.579]) # TYR 45 (H)
    mid_point = (p1 + p2) / 2.0
    
    candidates = []
    with open(bfr_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and " CA " in line:
                pos = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                dist_to_mid = np.linalg.norm(pos - mid_point)
                
                res_name = line[17:20].strip()
                res_num = line[22:26].strip()
                chain = line[21]
                candidates.append({'name': res_name, 'num': res_num, 'chain': chain, 'mid_dist': dist_to_mid, 'pos': pos})
                    
    candidates.sort(key=lambda x: x['mid_dist'])
    
    print(f"--- 🧬 CANDIDATOS RELAJADOS PARA REPETIDOR ---")
    print(f"Punto medio buscado: {mid_point}\n")
    for c in candidates[:5]:
        d1 = np.linalg.norm(c['pos'] - p1)
        d2 = np.linalg.norm(c['pos'] - p2)
        print(f"- {c['name']} {c['num']} (Chain {c['chain']}):")
        print(f"  Distancia al Punto Medio: {c['mid_dist']:.2f} A")
        print(f"  Segmento 1: {d1:.2f} A | Segmento 2: {d2:.2f} A")
        print(f"  GAP TOTAL VÍA ESTE NODO: {d1+d2:.2f} A")
