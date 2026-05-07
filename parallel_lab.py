
import numpy as np
import sys
import os
import scipy.linalg as la

# Import tropical metrics logic
sys.path.append(os.path.expanduser("~/.hermes/workspace/protein-lab/src/metrics"))
from tropical_metrics_v2 import BioMaterialCAD

def extract_irons(pdb_path):
    irons = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("HETATM") and "FE" in line[12:16] and "HEC" in line[17:20]:
                irons.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return np.array(irons)

def run_parallel_experiments(pdb_path):
    cad = BioMaterialCAD(delta_max=12.0) # Umbral estricto para detectar conectividad real
    original_net = extract_irons(pdb_path)
    
    experiments = {}
    
    # 1. BASELINE
    experiments["BASELINE"] = original_net
    
    # 2. DIMERIZATION (Parallel Bus)
    # Clonamos la red y la desplazamos 10 A en el eje X (distancia de empaquetamiento típica)
    dimer_offset = np.array([10.0, 0, 0])
    clon = original_net + dimer_offset
    # Agregamos puentes de Cisteína (nodos virtuales) cada 3 Hemes para interconexión
    bridges = []
    for i in range(0, len(original_net), 4):
        bridge_pos = (original_net[i] + clon[i]) / 2
        bridges.append(bridge_pos)
    experiments["DIMER_LATTICE"] = np.vstack([original_net, clon, np.array(bridges)])
    
    # 3. QUANTUM REPEATER (Hybrid Cluster)
    # Insertamos 3 clusters de Oro en puntos estratégicos del túnel longitudinal
    p_start = original_net[0]
    p_end = original_net[-1]
    repeaters = [
        p_start + (p_end - p_start) * 0.25,
        p_start + (p_end - p_start) * 0.50,
        p_start + (p_end - p_start) * 0.75
    ]
    experiments["QM_REPEATER"] = np.vstack([original_net, np.array(repeaters)])
    
    # 4. TRIANGULAR MESH (Topo-Mutation)
    # Simulamos una mutación donde los Hemes no están en línea, sino en zig-zag 
    # para forzar triangulaciones (Ihara Zeta focus)
    mesh_net = original_net.copy()
    for i in range(len(mesh_net)):
        if i % 2 == 0:
            mesh_net[i] += [2.0, 2.0, 0] # Desplazamiento lateral
    experiments["TRI_MESH"] = mesh_net

    print("--- 🧪 PROTEIN-LAB: EXP. PARALELOS (REDUNDANCIA) ---")
    print(f"{'DISEÑO':<15} | {'NODOS':<5} | {'ZETA':<10} | {'BETA':<10} | {'TUNNEL (eV)'}")
    print("-" * 75)
    
    for name, net in experiments.items():
        adj = cad.get_tropical_adjacency(net)
        zeta = cad.ihara_zeta_logdet(adj)
        beta = cad.spectral_beta(adj)
        eff = cad.tunnel_efficiency(adj)
        print(f"{name:<15} | {len(net):<5} | {zeta:<10.4f} | {beta:<10.4f} | {eff:.6f}")

    # Análisis de Robustez: Apagamos el 20% de los nodos al azar
    print("\n--- 🛡️ TEST DE RESILIENCIA (20% Node Failure) ---")
    for name, net in experiments.items():
        n_kill = int(len(net) * 0.2)
        indices = np.random.choice(len(net), len(net) - n_kill, replace=False)
        failed_net = net[indices]
        adj = cad.get_tropical_adjacency(failed_net)
        zeta = cad.ihara_zeta_logdet(adj)
        print(f"{name:<15} -> Zeta tras fallo: {zeta:.4f}")

if __name__ == "__main__":
    run_parallel_experiments(sys.argv[1])
