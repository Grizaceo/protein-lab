
import numpy as np
import os

def get_coords(pdb_path, residue_num, atom_name="CA", chain="A"):
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                try:
                    r_num = int(line[22:26])
                    c = line[21]
                    name = line[12:16].strip()
                    if r_num == residue_num and c == chain and name == atom_name:
                        return np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                except: continue
    return None

if __name__ == "__main__":
    from pathlib import Path
    _candidates = [
        Path(__file__).resolve().parent / "data/pdb/new_chassis/1BFR.pdb",
        Path(__file__).resolve().parent / "data/pdb/1BFR.pdb",
        Path(os.path.expanduser("~/.hermes/workspace/ACTIVE/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
        Path(os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
    ]
    bfr_path = str(next((p for p in _candidates if p.exists()), _candidates[0]))

    
    # Supongamos que nuestro puerto de entrada es MET 1 en la cadena A
    port_pos = get_coords(bfr_path, 1, "SD", "A")
    
    # Buscamos el TYR 45 más cercano a ese puerto (cara interna)
    # TYR 45 está en todas las cadenas (A-X...)
    best_tyr = None
    min_dist = float('inf')
    
    with open(bfr_path, 'r') as f:
        for line in f:
            if " TYR " in line and " 45 " in line and " CA " in line:
                pos = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                d = np.linalg.norm(pos - port_pos)
                if d < min_dist:
                    min_dist = d
                    best_tyr = (line[21], pos)
    
    print("--- 🎯 OPTIMIZACIÓN DE POSICIÓN DEL CORE ---")
    if port_pos is not None and best_tyr is not None:
        chain, tyr_pos = best_tyr
        print(f"Puerto Entrada (MET 1, Chain A) pos: {port_pos}")
        print(f"Piedra Interna más cercana (TYR 45, Chain {chain}) pos: {tyr_pos}")
        print(f"Distancia Interfacial (Piel de la proteína): {min_dist:.2f} A")
        
        # El vector de "empuje" para el oro:
        # Queremos que el borde del cluster (radio 14) toque la TYR 45.
        # El centro del oro debería estar a 14A de la TYR 45 en dirección al centro global.
        
        center_global = np.array([0, 0, 0]) # Aproximado, el script anterior lo calculó
        # Recalculamos centro real para precisión
        coords = []
        with open(bfr_path, 'r') as f:
            for line in f:
                if "FE" in line[12:16]:
                    try: coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                    except: continue
        center_global = np.mean(coords, axis=0)
        
        vector_to_center = center_global - tyr_pos
        unit_vec = vector_to_center / np.linalg.norm(vector_to_center)
        
        optimal_gold_center = tyr_pos + (unit_vec * 14.0)
        
        print(f"\nPOSICIÓN ÓPTIMA DEL CENTRO DEL AU55: {optimal_gold_center}")
        print(f"Esto deja el Oro a 14.00 A de la TYR interna.")
        print(f"Gap total desde el MtrA (vía MET 1 -> TYR 45 -> ORO):")
        print(f"1. MtrA -> MET 1:  (Docking Externo)")
        print(f"2. MET 1 -> TYR 45: {min_dist:.2f} A")
        print(f"3. TYR 45 -> ORO:   14.00 A")
        
        if min_dist < 15.0:
            print("\nRESULTADO: ¡SISTEMA CONECTADO! La cascada de electrones es posible.")
        else:
            print("\nRESULTADO: SIGUE SIENDO LARGO. Necesitamos mutar un TRP intermedio entre MET 1 y TYR 45.")
