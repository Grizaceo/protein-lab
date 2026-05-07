
import numpy as np
import sys
import os
import scipy.linalg as la

# Import tropical metrics logic from existing project
sys.path.append(os.path.expanduser("~/.hermes/workspace/protein-lab/src/metrics"))
from tropical_metrics_v2 import BioMaterialCAD

def get_coords(path, chain, res, atom="FE"):
    with open(path, 'r') as f:
        for line in f:
            if line.startswith("HETATM") or line.startswith("ATOM"):
                if atom in line[12:16] and line[21] == chain and int(line[22:26]) == res:
                     return np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return None

def run_simulation(pdb_path):
    cad = BioMaterialCAD(delta_max=15.5) # Aumentamos umbral para ver el gap
    
    # Extract Original Irons
    irons = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("HETATM") and "FE" in line[12:16] and "HEC" in line[17:20]:
                irons.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    
    original_net = np.array(irons)
    
    # ---------------------------------------------------------
    # PROPUESTA 1: TRP BRIDGE (PHE 218 -> TRP)
    # ---------------------------------------------------------
    phe218_pos = get_coords(pdb_path, 'B', 218, "CA")
    bridge_net = np.vstack([original_net, phe218_pos])
    
    # ---------------------------------------------------------
    # PROPUESTA 2: GOLD NANOPARTICLE (Doping)
    # ---------------------------------------------------------
    # Simulamos un nodo central perfecto en el gap
    pA = get_coords(pdb_path, 'A', 910)
    pC = get_coords(pdb_path, 'C', 805)
    gold_pos = (pA + pC) / 2
    gold_net = np.vstack([original_net, gold_pos])

    print("--- RESULTADOS DE SIMULACION PROTEIN-LAB ---")
    
    def get_stats(net, label):
        adj = cad.get_tropical_adjacency(net)
        zeta = cad.ihara_zeta_logdet(adj)
        beta = cad.spectral_beta(adj)
        eff = cad.tunnel_efficiency(adj)
        return {"label": label, "zeta": zeta, "beta": beta, "eff": eff}

    results = [
        get_stats(original_net, "ORIGINAL"),
        get_stats(bridge_net, "TRP-BRIDGE"),
        get_stats(gold_net, "GOLD-DOPING")
    ]

    print(f"{'DISEÑO':<15} | {'IHARA ZETA':<10} | {'GUE BETA':<10} | {'TUNNEL EFF'}")
    print("-" * 60)
    for r in results:
        print(f"{r['label']:<15} | {r['zeta']:<10.4f} | {r['beta']:<10.4f} | {r['eff']:.6f} eV")

    # Analisis de Fallo (Robustez)
    print("\n--- ANALISIS DE FAIL-SAFE (Loss of Heme 5A) ---")
    fail_idx = 4
    for r_net, label in [(original_net, "ORIGINAL"), (bridge_net, "TRP-BRIDGE")]:
        net_failed = np.delete(r_net, fail_idx, axis=0)
        adj_fail = cad.get_tropical_adjacency(net_failed)
        zeta_fail = cad.ihara_zeta_logdet(adj_fail)
        print(f"{label:<15} -> Zeta tras fallo: {zeta_fail:.4f}")

if __name__ == "__main__":
    run_simulation(sys.argv[1])
