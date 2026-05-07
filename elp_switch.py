
import sys
from pathlib import Path
sys.path.append("/home/gris/.hermes/workspace/protein-lab")
from tropical_metrics import BioMaterialCAD, parse_fasta
import numpy as np

# Definimos el "Bio-Interrupteur"
ELP_UNIT = "VPGVG"
ELP_SEQ = ELP_UNIT * 10  # 50 aa de Elastina
MTRF_PATH = Path("/home/gris/.hermes/workspace/protein-lab/exp01-hemoglobina/input/MtrF.fasta")

def simulate_switch():
    if not MTRF_PATH.exists():
        print("Error: MtrF sequence not found.")
        return

    mtrf_seq = parse_fasta(MTRF_PATH)
    # Hibridación: Elastina unida a la "puerta" MtrF
    hybrid_seq = ELP_SEQ + mtrf_seq
    
    print(f"Hybrid Material: Elastin({len(ELP_SEQ)}aa) + MtrF({len(mtrf_seq)}aa)")
    print("-" * 75)
    print(f"{'State':<15} | {'Delta Max':<10} | {'GUE Beta':<10} | {'Zeta (log)':<12} | {'Conduction'}")
    print("-" * 75)

    # Simulación de la Transición de Fase del Bio-Material
    states = [
        ("OFF (Linear)", 0.0, 1.5),
        ("Folding Start", 0.3, 1.5),
        ("Pre-Metal", 0.6, 1.5),
        ("ON (Globular)", 0.85, 1.5),
        ("Super-Conductor", 0.95, 1.5)
    ]

    for name, folding, d_max in states:
        cad = BioMaterialCAD(delta_max=d_max)
        coords = cad.sequence_to_mock_coords(hybrid_seq, folding=folding)
        adj = cad.get_tropical_adjacency(coords)
        
        beta = cad.gue_beta_stability(adj)
        
        n = adj.shape[0]
        deg = np.sum(~np.isinf(adj), axis=1) - 1
        avg_deg = np.mean(deg)
        
        regime = "ON (GUE/Conductor)" if beta > 0.48 else "OFF (Poisson/Aislante)"
        print(f"{name:<15} | {folding:<10.2f} | {beta:<10.4f} | {avg_deg:<12.2f} | {regime}")

if __name__ == "__main__":
    simulate_switch()
