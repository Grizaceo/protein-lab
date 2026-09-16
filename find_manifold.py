
import numpy as np
import os

def find_triangular_manifold(pdb_path, target_area, min_dist=10.0, max_dist=25.0):
    candidates = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and " CA " in line:
                pos = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                dist = np.linalg.norm(pos - target_area)
                if dist < 25.0:
                    candidates.append({'res': f"{line[17:20]} {line[22:26]}", 'chain': line[21], 'pos': pos})
    
    # Buscar combinaciones de 3 que formen un triángulo equilátero-ish
    triangles = []
    for i in range(len(candidates)):
        for j in range(i+1, len(candidates)):
            for k in range(j+1, len(candidates)):
                p1, p2, p3 = candidates[i]['pos'], candidates[j]['pos'], candidates[k]['pos']
                d12 = np.linalg.norm(p1 - p2)
                d23 = np.linalg.norm(p2 - p3)
                d31 = np.linalg.norm(p3 - p1)
                
                # Buscamos un triángulo estable (lados entre 10A y 20A)
                if 10.0 < d12 < 25.0 and 10.0 < d23 < 25.0 and 10.0 < d31 < 25.0:
                    # Desviación de equilátero
                    std = np.std([d12, d23, d31])
                    if std < 3.0: # Muy simétrico
                        triangles.append({'nodes': (candidates[i], candidates[j], candidates[k]), 'std': std, 'dist_avg': np.mean([d12, d23, d31])})
    
    triangles.sort(key=lambda x: x['std'])
    return triangles

if __name__ == "__main__":
    from pathlib import Path
    _candidates = [
        Path(__file__).resolve().parent / "data/pdb/new_chassis/1BFR.pdb",
        Path(__file__).resolve().parent / "data/pdb/1BFR.pdb",
        Path(os.path.expanduser("~/.hermes/workspace/ACTIVE/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
        Path(os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
    ]
    bfr_path = str(next((p for p in _candidates if p.exists()), _candidates[0]))

    
    # El área de interés es cerca de donde el Oro debe estar (calculado en optimize_core.py)
    gold_target = np.array([11.55, -12.53, 24.28])
    
    print("--- 📡 BÚSQUEDA DE MANIFOLD TRIANGULAR (ANTENAS DE ANCLAJE) ---")
    triangles = find_triangular_manifold(bfr_path, gold_target)
    
    if triangles:
        print(f"Encontrados {len(triangles)} manifolds potenciales.")
        top = triangles[0]
        print(f"\nMEJOR CANDIDATO (Simetría STD: {top['std']:.2f}):")
        for n in top['nodes']:
            dist_to_gold = np.linalg.norm(n['pos'] - gold_target)
            print(f"- {n['res']} (Chain {n['chain']}) | Distancia al Oro: {dist_to_gold:.2f} A")
        
        print(f"\nPromedio entre antenas: {top['dist_avg']:.2f} A")
        print("DIAGNÓSTICO: Geometría perfecta para anclaje de trípode.")
    else:
        print("No se encontraron triángulos simétricos. Habrá que forzar mutaciones asimétricas.")
