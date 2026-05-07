
import sys
import numpy as np
from pathlib import Path
import scipy.sparse.csgraph as csgraph

sys.path.append("/home/gris/.hermes/workspace/protein-lab/src/metrics")
from tropical_metrics_v2 import BioMaterialCAD
from pdb_utils import extract_iron_network

def analyze_path_network():
    pdb_dir = Path("/home/gris/.hermes/workspace/protein-lab/data/pdb")
    mtrf_pdb = pdb_dir / "MtrF.pdb"
    mtra_pdb = pdb_dir / "MtrA.pdb"

    # Delta_max = 15A es el estándar para saltos de electrones en cytochromes
    cad = BioMaterialCAD(delta_max=15.0) 

    print("="*80)
    print("ANÁLISIS DE CONTINUIDAD TROPICAL (CIRCUIT CHECK)")
    print("="*80)

    for name, pdb in [("MtrF (Ext. Gate)", mtrf_pdb), ("MtrA (Int. Wire)", mtra_pdb)]:
        fe_coords = extract_iron_network(pdb)
        adj = cad.get_tropical_adjacency(fe_coords)
        
        # Usamos Dijkstra (Tropical sum over paths) para ver si los hemas extremos están conectados
        # Convertimos inf a 0 para el grafo esparso
        matrix = np.where(np.isinf(adj), 0, adj)
        dist_matrix = csgraph.dijkstra(matrix, directed=False)
        
        # Medimos la distancia entre los dos hemas más alejados en la secuencia
        # para ver si la señal puede atravesar la proteína de punta a punta.
        start_node = 0
        end_node = len(fe_coords) - 1
        path_len = dist_matrix[start_node, end_node]
        
        status = "OPEN CIRCUIT (CONNECTED)" if not np.isinf(path_len) else "BROKEN CIRCUIT (DISCONNECTED)"
        
        print(f"Structure: {name}")
        print(f" -> Hemes detectados: {len(fe_coords)}")
        print(f" -> Distancia Tropical (Min-Plus Path): {path_len:.2f} Angstroms")
        print(f" -> Status: {status}")
        
        if not np.isinf(path_len):
            # Eficiencia de transporte a través de todo el cable
            # H_total approx product of internal H_abs (or min in tropical)
            # Simplificamos: Eficiencia = exp(-dist_tropical)
            eff_total = np.exp(-0.7 * (path_len/10)) # factor beta=1.4, half is 0.7
            print(f" -> Eficiencia del Canal de Datos: {eff_total:.4e} relative units")
        print("-" * 80)

if __name__ == "__main__":
    analyze_path_network()
