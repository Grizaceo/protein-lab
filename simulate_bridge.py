
import numpy as np
import sys
import os

# Import tropical metrics logic from existing project
sys.path.append(os.path.expanduser("~/.hermes/workspace/protein-lab/src/metrics"))
from tropical_metrics_v2 import compute_ihara_zeta, compute_gue_beta

def get_coords(path, chain, res, atom="FE"):
    with open(path, 'r') as f:
        for line in f:
            if line.startswith("HETATM") or line.startswith("ATOM"):
                if atom in line[12:16] and line[21] == chain and int(line[22:26]) == res:
                     return np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return None

def run_simulation(pdb_path):
    # Extract Original Irons
    irons = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("HETATM") and "FE" in line[12:16] and "HEC" in line[17:20]:
                irons.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    
    original_net = np.array(irons)
    
    # Mutation: Add PHE 218 center as a node (Simulating TRP bridge)
    phe218_pos = get_coords(pdb_path, 'B', 218, "CA")
    bridge_net = np.vstack([original_net, phe218_pos])
    
    print("--- SIMULACION DE REDUNDANCIA LATERAL ---")
    print(f"Original Nodes: {len(original_net)}")
    print(f"Mutated Nodes: {len(bridge_net)} (1 TRP Bridge added)\n")
    
    # 1. IHARA ZETA (Higher = More Redundancy)
    u = 0.1
    zeta_orig = compute_ihara_zeta(original_net, u=u)
    zeta_mut = compute_ihara_zeta(bridge_net, u=u)
    
    # 2. GUE BETA (Higher = Better Conductivity/Coherence)
    beta_orig = compute_gue_beta(original_net)
    beta_mut = compute_gue_beta(bridge_net)
    
    # 3. ROBUSTEZ (Ataque Adversarial)
    # Deactivate one central node and check if the graph still connects A and C
    # This is a simplified "path-finding" check
    
    print(f"METRICA        | ORIGINAL | MUTADA (Bridge) | CAMBIO")
    print(f"---------------|----------|-----------------|-------")
    print(f"Ihara Zeta (u) | {zeta_orig:.4f}   | {zeta_mut:.4f}          | {((zeta_mut/zeta_orig)-1)*100:+.1f}%")
    print(f"GUE Beta       | {beta_orig:.4f}   | {beta_mut:.4f}          | {((beta_mut/beta_orig)-1)*100:+.1f}%")
    
    print("\n--- ANALISIS DE FALLO ---")
    print("Simulando perdida de Heme-5A (Nodo critico)")
    orig_fail = compute_ihara_zeta(np.delete(original_net, 4, axis=0), u=u)
    mut_fail = compute_ihara_zeta(np.delete(bridge_net, 4, axis=0), u=u)
    
    print(f"Impacto de fallo en Original: {((orig_fail/zeta_orig)-1)*100:+.1f}%")
    print(f"Impacto de fallo en Mutada:   {((mut_fail/zeta_mut)-1)*100:+.1f}%")

if __name__ == "__main__":
    run_simulation(sys.argv[1])
