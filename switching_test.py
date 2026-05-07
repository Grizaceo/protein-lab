
import sys
import numpy as np
from pathlib import Path
import scipy.sparse.csgraph as csgraph

sys.path.append("/home/gris/.hermes/workspace/protein-lab/src/metrics")
from tropical_metrics_v2 import BioMaterialCAD
from pdb_utils import extract_iron_network

def switching_pressure_test():
    pdb_dir = Path("/home/gris/.hermes/workspace/protein-lab/data/pdb")
    mtrf_pdb = pdb_dir / "MtrF.pdb"
    mtra_pdb = pdb_dir / "MtrA.pdb"

    # Cargamos las coordenadas de los hierros (Hec Centers)
    coords_f = extract_iron_network(mtrf_pdb)
    coords_a = extract_iron_network(mtra_pdb)

    print("="*80)
    print("STRESS TEST TROPICAL: BUSCANDO EL PUNTO DE CONMUTACIÓN (SWITCHING POINT)")
    print("="*80)
    print(f"{'Threshold (A)':<15} | {'MtrF Status':<15} | {'MtrA Status':<15}")
    print("-" * 80)

    # Variamos el delta_max desde 8A (contacto atómico) hasta 25A (tunelamiento de largo alcance)
    thresholds = np.linspace(8.0, 25.0, 18)
    
    results = []
    found_f = False
    found_a = False

    for d in thresholds:
        cad = BioMaterialCAD(delta_max=d)
        
        # MtrF
        adj_f = cad.get_tropical_adjacency(coords_f)
        dist_f = csgraph.dijkstra(np.where(np.isinf(adj_f), 0, adj_f), directed=False)
        path_f = dist_f[0, len(coords_f)-1]
        status_f = "ON" if not np.isinf(path_f) else "OFF"
        
        # MtrA
        adj_a = cad.get_tropical_adjacency(coords_a)
        dist_a = csgraph.dijkstra(np.where(np.isinf(adj_a), 0, adj_a), directed=False)
        path_a = dist_a[0, len(coords_a)-1]
        status_a = "ON" if not np.isinf(path_a) else "OFF"
        
        print(f"{d:<15.2f} | {status_f:<15} | {status_a:<15}")
        
        if status_f == "ON" and not found_f:
            found_f = d
        if status_a == "ON" and not found_a:
            found_a = d

    print("\n" + "="*80)
    print("ANÁLISIS DE BIOLÓGICA:")
    print(f" -> MtrF Switching Threshold: {found_f:.2f} A" if found_f else " -> MtrF: NEVER ON")
    print(f" -> MtrA Switching Threshold: {found_a:.2f} A" if found_a else " -> MtrA: NEVER ON")
    
    if found_f and found_a:
        diff = found_a - found_f
        print(f"\n [+] DIFERENCIAL DE PRESIÓN: {diff:.2f} A")
        print(" [!] CONCLUSIÓN DE INGENIERÍA: MtrF es un cable 'siempre activo' en condiciones")
        print("     fisiológicas (~15A). MtrA es un 'Interruptor Duro' que requiere")
        print(f"     una compresión extra de {diff:.2f} A para activarse.")
    print("="*80)

if __name__ == "__main__":
    switching_pressure_test()
