
import numpy as np
import sys
import os
import scipy.linalg as la

# Import BioMaterialCAD
sys.path.append(os.path.expanduser("~/.hermes/workspace/protein-lab/src/metrics"))
from tropical_metrics_v2 import BioMaterialCAD

def extract_irons(pdb_path):
    irons = []
    with open(pdb_path, 'r') as f:
        for line in f:
            # Detect FE in Heme or direct FE (Ferritin core)
            if ("FE" in line[12:16]) and (line.startswith("HETATM") or line.startswith("ATOM")):
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    irons.append([x, y, z])
                except:
                    continue
    return np.array(irons)

def audit_chassis(pdb_path):
    cad = BioMaterialCAD(delta_max=15.0) # Standard tunnel threshold
    net = extract_irons(pdb_path)
    
    if len(net) == 0:
        print(f"Error: No iron centers found in {pdb_path}")
        return

    adj = cad.get_tropical_adjacency(net)
    zeta = cad.ihara_zeta_logdet(adj)
    beta = cad.spectral_beta(adj)
    eff = cad.tunnel_efficiency(adj)
    
    print(f"AUDITORIA DE CHASIS: {os.path.basename(pdb_path)}")
    print(f"------------------------------------------")
    print(f"Nodos de Hierro: {len(net)}")
    print(f"Ihara Zeta:      {zeta:.4f} {'(RED REAL!)' if zeta > 0 else '(LINEAL/FRAGMENTADO)'}")
    print(f"GUE Beta:        {beta:.4f}")
    print(f"Eficiencia:      {eff:.6f} eV")
    print("")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        audit_chassis(p)
