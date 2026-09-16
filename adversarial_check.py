
import numpy as np
import os

def get_center_of_mass_chain(pdb_path, chain):
    coords = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and line[21] == chain:
                try:
                    coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                except: continue
    return np.mean(coords, axis=0) if coords else None

if __name__ == "__main__":
    from pathlib import Path
    _script_dir = Path(__file__).resolve().parent
    _candidates = [
        _script_dir / "data/pdb/new_chassis/1BFR.pdb",
        _script_dir / "data/pdb/1BFR.pdb",
        Path(os.path.expanduser("~/.hermes/workspace/ACTIVE/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
        Path(os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
    ]
    bfr_path = str(next((p for p in _candidates if p.exists()), _candidates[0]))

    
    # 1. TEST DE GEOGRAFÍA (Ataque 3)
    c_a = get_center_of_mass_chain(bfr_path, "A")
    c_h = get_center_of_mass_chain(bfr_path, "H")
    
    print("--- 💣 TEST ADVERSARIAL 1: GEOPOLÍTICA DE CADENAS ---")
    if c_a is not None and c_h is not None:
        dist = np.linalg.norm(c_a - c_h)
        print(f"Distancia entre el centro de Cadena A y Cadena H: {dist:.2f} A")
        # El diámetro total de la BFR es ~120A.
        if dist < 40.0:
            print("ESTADO: SOBREVIVE (Son vecinas).")
        else:
            print("ESTADO: MUERTO (Están en lados opuestos de la pelota).")

    # 2. TEST DE ESTABILIDAD DEL CORE (Ataque 2)
    # Calculamos el volumen del lumen vs volumen del cluster
    # Radio lumen ~41A, Radio Au55 ~14A
    vol_lumen = (4/3) * np.pi * (41**3)
    vol_gold = (4/3) * np.pi * (14**3)
    ratio = (vol_gold / vol_lumen) * 100
    
    print("\n--- 💣 TEST ADVERSARIAL 2: ESTABILIDAD MECÁNICA ---")
    print(f"El oro solo ocupa el {ratio:.2f}% del espacio disponible.")
    print("Probabilidad de contacto espontáneo: Muy baja.")
    print("DIAGNÓSTICO: El sistema fallará por ruido térmico a menos que propongamos un anclaje.")
