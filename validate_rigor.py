
import sys
import numpy as np
from pathlib import Path

sys.path.append("/home/gris/.hermes/workspace/protein-lab/src/metrics")
from tropical_metrics_v2 import BioMaterialCAD
from pdb_utils import extract_iron_network, generate_null_model

def rigor_check_v3():
    pdb_dir = Path("/home/gris/.hermes/workspace/protein-lab/data/pdb")
    mtrf_pdb = pdb_dir / "MtrF.pdb"
    mtra_pdb = pdb_dir / "MtrA.pdb"

    # Delta_max = 15 Angstroms (1.5 nm). Límite de tunelamiento biológico.
    cad = BioMaterialCAD(delta_max=15.0) 

    print("="*80)
    print("BIOMATERIAL CAD v3.0: ELECTRONIC WIRE VALIDATION (HEME-CENTERS)")
    print("="*80)
    print(f"{'Structure':<20} | {'Hemes':<6} | {'Tropical Connectivity':<22} | {'Conduction Ef.'}")
    print("-" * 80)

    for name, pdb in [("MtrF (Ext. Gate)", mtrf_pdb), ("MtrA (Int. Wire)", mtra_pdb)]:
        if not pdb.exists(): continue
        
        # 1. Extraer red de Hierros REAL
        fe_coords = extract_iron_network(pdb)
        adj_real = cad.get_tropical_adjacency(fe_coords)
        
        # Calculamos conectividad (grado promedio en la red de hemas)
        n_hemes = len(fe_coords)
        conn = np.sum(~np.isinf(adj_real)) / n_hemes
        eff = cad.tunnel_efficiency(adj_real)
        
        print(f"{name:<20} | {n_hemes:<6} | {conn:<22.2f} | {eff*1000:<.2f} meV")

        # 2. Control aleatorio (Null Hypothesis)
        # 10 puntos al azar en un volumen similar al de la proteína
        box = np.max(fe_coords, axis=0) - np.min(fe_coords, axis=0)
        null_coords = generate_null_model(n_hemes, box_size=np.max(box))
        adj_null = cad.get_tropical_adjacency(null_coords)
        
        conn_n = np.sum(~np.isinf(adj_null)) / n_hemes
        eff_n = cad.tunnel_efficiency(adj_null)
        
        print(f"{' -> NULL CONTROL':<20} | {n_hemes:<6} | {conn_n:<22.2f} | {eff_n*1000:<.2f} meV")
        print("-" * 80)

if __name__ == "__main__":
    rigor_check_v3()
