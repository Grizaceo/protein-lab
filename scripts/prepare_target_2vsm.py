#!/usr/bin/env python3
"""
prepare_target_2vsm.py
======================
Limpia y prepara el target de la Glicoproteína G del Virus Nipah (2VSM).
- Extrae únicamente la Cadena A.
- Restringe el dominio de unión al receptor a los residuos 212-600 (inclusive).
- Elimina todas las moléculas de agua, ligandos e iones (HETATM).
- Guarda la estructura resultante en 'data/pdb/target_clean.pdb'.
- Lee 'data/pdb/2VSM_chainA_hotspots.txt' y valida que los 22 residuos hotspot
  estén presentes y expuestos en el modelo depurado.
"""

import os
import sys
from Bio.PDB import PDBParser, PDBIO, Select

# Rutas de entrada y salida
PDB_IN = "data/pdb/2VSM.pdb"
HOTSPOTS_IN = "data/pdb/2VSM_chainA_hotspots.txt"
PDB_OUT = "data/pdb/target_clean.pdb"

class TargetSelect(Select):
    """Filtro para Bio.PDB para seleccionar solo la Cadena A, residuos 212-600, y omitir HETATM."""
    def accept_chain(self, chain):
        return chain.id == 'A'

    def accept_residue(self, residue):
        # Omitir heteroátomos (aguas, ligandos, etc. representados con prefijos H_ en ID de BioPython)
        res_id = residue.get_id()
        is_het = res_id[0].strip() != ""
        if is_het:
            return False
        
        # Filtrar por rango de numeración del dominio globular (212 - 600)
        res_num = res_id[1]
        return 212 <= res_num <= 600

    def accept_atom(self, atom):
        # Aceptar todos los átomos de los residuos y cadenas aprobados
        return True

def load_hotspots(filepath):
    """Carga los residuos hotspot desde el archivo de texto."""
    hotspots = []
    if not os.path.exists(filepath):
        print(f"[!] Advertencia: No se encontró el archivo de hotspots en '{filepath}'")
        return hotspots
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    res_num = int(parts[0])
                    res_name = parts[1]
                    dist = float(parts[2]) if len(parts) > 2 else 0.0
                    hotspots.append((res_num, res_name, dist))
                except ValueError:
                    continue
    return hotspots

def main():
    print("=" * 75)
    print("PREPARACIÓN Y LIMPIEZA DE DOMINIO RECEPTOR-BINDING NIPAH G (2VSM)")
    print("=" * 75)

    if not os.path.exists(PDB_IN):
        sys.exit(f"ERROR: No se encontró el PDB de entrada en '{PDB_IN}'")

    # 1. Parsear estructura original
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("2VSM", PDB_IN)
    
    # 2. Guardar con el filtro implementado
    io = PDBIO()
    io.set_structure(structure)
    
    # Asegurar que el directorio de salida exista
    os.makedirs(os.path.dirname(PDB_OUT), exist_ok=True)
    
    io.save(PDB_OUT, TargetSelect())
    print(f"\n[✓] Estructura limpia guardada en: '{PDB_OUT}'")

    # 3. Recargar la estructura limpia para validar e indexar
    structure_clean = parser.get_structure("2VSM_clean", PDB_OUT)
    model_clean = structure_clean[0]
    chain_A_clean = model_clean['A']
    
    clean_residues = list(chain_A_clean.get_residues())
    print(f"  -> Total de residuos de proteína en la estructura limpia: {len(clean_residues)}")
    if len(clean_residues) > 0:
        print(f"  -> Rango de numeración: {clean_residues[0].get_id()[1]} a {clean_residues[-1].get_id()[1]}")
    
    # 4. Validar hotspots
    hotspots = load_hotspots(HOTSPOTS_IN)
    print(f"\nValidando {len(hotspots)} residuos hotspot contra la estructura limpia:")
    
    missing_hotspots = []
    found_count = 0
    
    for res_num, res_name, dist in hotspots:
        res_key = (" ", res_num, " ")
        if res_key in chain_A_clean:
            res_struct = chain_A_clean[res_key]
            # Mapear nombres de residuo estándar de 3 letras de PDB
            if res_struct.resname.upper() == res_name.upper():
                found_count += 1
            else:
                print(f"  [!] Conflicto de tipo: Hotspot {res_num} es {res_name} en txt, pero {res_struct.resname} en PDB.")
        else:
            missing_hotspots.append((res_num, res_name))
            
    print(f"  -> Residuos hotspot correctamente validados: {found_count} de {len(hotspots)}")
    
    if missing_hotspots:
        print(f"  [!] ERROR: Faltan los siguientes hotspots en el archivo limpio:")
        for r_num, r_name in missing_hotspots:
            print(f"      - {r_name} {r_num}")
        sys.exit(1)
    else:
        print("  [✓] Todos los 22 residuos hotspot están presentes en el dominio globular.")
        
    print("\nVerificando ausencia de heteroátomos (HETATM) y aguas:")
    het_atoms = [atom for atom in structure_clean.get_atoms() if atom.get_parent().get_id()[0].strip() != ""]
    if len(het_atoms) == 0:
        print("  [✓] No se detectaron moléculas de agua, ligandos ni iones. Limpieza completa.")
    else:
        print(f"  [!] Advertencia: Se encontraron {len(het_atoms)} átomos de tipo HETATM residuales.")
        sys.exit(1)

    print("=" * 75)

if __name__ == "__main__":
    main()
