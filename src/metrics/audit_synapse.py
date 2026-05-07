import numpy as np
import sys
import os
import scipy.linalg as la

# Agregar src al path
sys.path.append("/home/gris/.hermes/workspace/protein-lab/src/metrics")
from pdb_utils import extract_iron_network_v4

def get_adjacency_matrix(coords, threshold=15.0):
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    dist = np.sqrt(np.sum(diff**2, axis=-1))
    adj = (dist <= threshold).astype(float)
    np.fill_diagonal(adj, 0)
    return adj

def get_GUE_beta(adj):
    if adj.size == 0 or np.sum(adj) == 0: return 0.0
    eigvals = np.linalg.eigvalsh(adj)
    # RMT r-parameter: GUE=0.599, Poisson=0.386
    spacings = np.diff(np.sort(eigvals))
    if len(spacings) < 2: return 0.0
    r = spacings[1:] / (spacings[:-1] + 1e-9)
    return np.mean(np.minimum(r, 1.0/r))

def run_audit():
    f_path = "/home/gris/.hermes/workspace/protein-lab/data/pdb/MtrF.pdb"
    a_path = "/home/gris/.hermes/workspace/protein-lab/data/pdb/MtrA.pdb"
    
    fe_f = extract_iron_network_v4(f_path)
    fe_a = extract_iron_network_v4(a_path)
    
    # Extraer solo coords x,y,z
    cf = fe_f[:, :3]
    ca = fe_a[:, :3]
    
    cf -= np.mean(cf, axis=0)
    ca -= np.mean(ca, axis=0)
    
    print(f"Audit: MtrF hemes={len(cf)}, MtrA hemes={len(ca)}")
    print(f"{'GAP (A)':<10} | {'Beta':<6} | {'Status'}")
    print("-" * 35)
    
    for gap in np.linspace(80, 25, 12):
        # MOver MtrA en Z
        temp_a = ca + np.array([0, 0, gap])
        full = np.vstack([cf, temp_a])
        adj = get_adjacency_matrix(full)
        
        # Conectividad entre F y A
        # Bloque superior derecho de la matriz de adyacencia
        cross = adj[:len(cf), len(cf):]
        conn = np.any(cross > 0)
        beta = get_GUE_beta(adj)
        
        status = "CONNECTED" if conn else "ISOLATED"
        print(f"{gap:<10.1f} | {beta:5.3f} | {status}")

if __name__ == "__main__":
    run_audit()
