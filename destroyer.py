
import sys
import numpy as np
from pathlib import Path
import scipy.sparse.csgraph as csgraph

sys.path.append("/home/gris/.hermes/workspace/protein-lab/src/metrics")
from tropical_metrics_v2 import BioMaterialCAD
from pdb_utils import extract_iron_network_v4

def destructor_check():
    pdb_dir = Path("/home/gris/.hermes/workspace/protein-lab/data/pdb")
    
    print("="*80)
    print("OPERACIÓN DESTRUIDOR: BUSCANDO EL ERROR EN EL MODELO")
    print("="*80)

    for name, pdb_file in [("MtrF", "MtrF.pdb"), ("MtrA", "MtrA.pdb")]:
        data = extract_iron_network_v4(pdb_dir / pdb_file)
        coords = data[:, :3]
        b_factors = data[:, 3]
        chains = data[:, 4]
        
        # --- TEST 1: El Error del Dímero ---
        # ¿Está MtrA desconectado solo porque estamos midiendo a través de dos cadenas?
        unique_chains = np.unique(chains)
        print(f"\nAnalizando {name} ({pdb_file}):")
        print(f" -> Cadenas detectadas: {[chr(int(c)) for c in unique_chains]}")
        
        cad = BioMaterialCAD(delta_max=15.0)
        
        for c_val in unique_chains:
            mask = chains == c_val
            c_coords = coords[mask]
            adj = cad.get_tropical_adjacency(c_coords)
            dist = csgraph.dijkstra(np.where(np.isinf(adj), 0, adj), directed=False)
            path = dist[0, -1]
            status = "CONECTADO" if not np.isinf(path) else "ROTO"
            print(f"    * Cadena {chr(int(c_val))} ({len(c_coords)} hemes): {status} (Dist: {path:.2f}A)")

        # --- TEST 2: Sensibilidad al Ruido Térmico (Monte Carlo) ---
        # Las posiciones en PDB tienen incertidumbre (B-factors).
        # Vamos a ver si el estado ON/OFF sobrevive a 1000 vibraciones térmicas.
        n_trials = 500
        on_count = 0
        
        # Usamos la primera cadena para el test térmico
        mask = chains == unique_chains[0]
        base_coords = coords[mask]
        current_b = b_factors[mask]
        # B = 8*pi^2 * <u^2> -> rmsd = sqrt(B / (8*pi^2))
        rmsd = np.sqrt(current_b / (8 * np.pi**2))
        
        for _ in range(n_trials):
            # Añadimos ruido gaussiano basado en el B-factor de cada átomo
            noise = np.random.normal(0, rmsd[:, None], base_coords.shape)
            noisy_coords = base_coords + noise
            
            adj = cad.get_tropical_adjacency(noisy_coords)
            dist = csgraph.dijkstra(np.where(np.isinf(adj), 0, adj), directed=False)
            if not np.isinf(dist[0, -1]):
                on_count += 1
        
        stability = (on_count / n_trials) * 100
        print(f" -> Estabilidad Térmica (15A): {stability:.1f}% de confianza")
        
        if stability < 80:
            print(f" [!] MODELO DESTRUIDO: {name} no es un conductor fiable, es un efecto estadístico.")
        else:
            print(f" [+] MODELO RESISTENTE: {name} mantiene su estado bajo vibración térmica.")

if __name__ == "__main__":
    destructor_check()
