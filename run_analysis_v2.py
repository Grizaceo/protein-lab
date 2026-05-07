
import sys
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# Agregar carpetas al path para importar el core
sys.path.append("/home/gris/.hermes/workspace/protein-lab/src/metrics")
from tropical_metrics_v2 import BioMaterialCAD, parse_fasta, generate_backbone

def run_professional_analysis():
    data_dir = Path("/home/gris/.hermes/workspace/protein-lab/data/raw")
    proteins = {
        "MtrF (Outer Gate)": data_dir / "MtrF.fasta",
        "MtrA (Inner Cable)": data_dir / "MtrA_SO1776.fasta"
    }

    # Instanciamos el CAD con umbral tropical de tunelamiento de rango largo (1.5nm = 15A)
    # Permite capturar la redundancia de caminos (Zeta)
    cad = BioMaterialCAD(delta_max=1.5) 

    print("="*80)
    print("BIOMATERIAL CAD v2.0 - TROPICAL MANIFOLD REPORT")
    print("="*80)
    header = f"{'Protein':<20} | {'AA':<5} | {'Zeta Complexity':<15} | {'GUE Beta':<10} | {'Conduction Efficiency'}"
    print(header)
    print("-" * len(header))

    results = []
    
    for name, path in proteins.items():
        if not path.exists():
            continue
            
        seq = parse_fasta(path)
        n = len(seq)
        
        # Simulación de estado "Nativo" (Folding factor 0.7 = Colapso parcial)
        coords = generate_backbone(n, folding_factor=0.7)
        adj = cad.get_tropical_adjacency(coords)
        
        zeta = cad.ihara_zeta_logdet(adj)
        beta = cad.spectral_beta(adj)
        eff = cad.tunnel_efficiency(adj)
        
        status = "GUE (Super-Conductor)" if beta > 0.51 else "Poisson (Insulator)"
        
        print(f"{name:<20} | {n:<5} | {zeta:<15.4f} | {beta:<12.4f} | {eff:<.6f} eV")
        results.append((name, beta, zeta, eff))

    print("\n" + "="*80)
    print("RESUMEN TERMODINÁMICO:")
    for name, beta, zeta, eff in results:
        v_eff = eff * 1000 # meV
        print(f" -> {name}: Estabilidad topológica de {zeta:.2f} log-units. Energía de acoplo promedio: {v_eff:.2f} meV.")
    print("="*80)

if __name__ == "__main__":
    run_professional_analysis()
