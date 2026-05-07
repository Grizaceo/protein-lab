
import numpy as np
import sys
import os

def check_exposed_sulfurs(pdb_path):
    """Busca Cisteínas o Metioninas en la superficie."""
    exposed = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and (" CYS " in line or " MET " in line):
                if " SG " in line or " SD " in line: # Átomos de Azufre
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    res_name = line[17:20].strip()
                    res_num = int(line[22:26])
                    chain = line[21]
                    exposed.append({'name': res_name, 'num': res_num, 'chain': chain, 'pos': np.array([x, y, z])})
    return exposed

if __name__ == "__main__":
    bfr_path = os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")
    mtra_path = os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/MtrA.pdb")
    
    print("--- 🔍 AUDITORÍA DE PUERTOS DE CONEXIÓN (AZUFRE) ---")
    
    bfr_sulfurs = check_exposed_sulfurs(bfr_path)
    mtra_sulfurs = check_exposed_sulfurs(mtra_path)
    
    print(f"Ferritina (1BFR): {len(bfr_sulfurs)} potenciales puertos S-S.")
    print(f"MtrA (MtrA.pdb): {len(mtra_sulfurs)} potenciales puertos S-S.")
    
    if mtra_sulfurs and bfr_sulfurs:
        print("\nPuertos sugeridos para el Docking:")
        print(f"MtrA: {mtra_sulfurs[0]['name']} {mtra_sulfurs[0]['num']} (Chain {mtra_sulfurs[0]['chain']})")
        print(f"BFR:  {bfr_sulfurs[0]['name']} {bfr_sulfurs[0]['num']} (Chain {bfr_sulfurs[0]['chain']})")
