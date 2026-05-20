#!/usr/bin/env python3
"""
calculate_au_np_position.py
===========================
Calcula la posición geométrica óptima (centroide 3D) de la nanopartícula de oro (Au NP)
excéntrica de 2.0 nm (radio de 10.0 Å) en el lumen de BFR_mutant_A.pdb.

Aplica un algoritmo de optimización numérica (SciPy) para hallar la posición del centro
del Au NP tal que las distancias de contacto a los azufres (SG) de CYS40, CYS43 y CYS49
de la cadena A sean lo más cercanas posible a las distancias de anclaje de diseño:
  - CYS43 SG -> Au surface = 1.9 Å (covalente fuerte, distancia al centro = 11.9 Å)
  - CYS49 SG -> Au surface = 3.1 Å (covalente medio, distancia al centro = 13.1 Å)
  - CYS40 SG -> Au surface = 5.3 Å (anclaje marginal, distancia al centro = 15.3 Å)

Además, valida la excentricidad del Au NP midiendo su distancia al centro de masa global
del 24-mer de BFR, y reporta la distancia a la superficie metálica desde el Heme B FE
adyacente (Cadena B HEM 200).
"""

import os
import sys
import numpy as np
from Bio.PDB import PDBParser
from scipy.optimize import minimize

BFR_MUT = "data/pdb/new_chassis/1BFR_mutant_A.pdb"

if not os.path.exists(BFR_MUT):
    sys.exit(f"ERROR: No se encontró la estructura mutada en '{BFR_MUT}'. Ejecutar primero 'model_1bfr_mutants.py'")

def main():
    print("=" * 75)
    print("OPTIMIZACIÓN GEOMÉTRICA DE NANOPARTÍCULA DE ORO EXCÉNTRICA V4b")
    print("=" * 75)
    
    # 1. Cargar estructura mutada
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("1BFR_mut", BFR_MUT)
    model = structure[0]
    
    # 2. Obtener átomos de interés
    chain_A = model["A"]
    
    try:
        sg40 = chain_A[(" ", 40, " ")]["SG"].get_vector().get_array()
        sg43 = chain_A[(" ", 43, " ")]["SG"].get_vector().get_array()
        sg49 = chain_A[(" ", 49, " ")]["SG"].get_vector().get_array()
    except KeyError as e:
        sys.exit(f"ERROR: No se encontraron los átomos SG de CYS en la cadena A ({e}).")
        
    # Obtener Heme B FE (Cadena B, Residuo HEM 200)
    try:
        chain_B = model["B"]
        heme_fe = chain_B[("H_HEM", 200, " ")]["FE"].get_vector().get_array()
    except KeyError as e:
        sys.exit(f"ERROR: No se encontró el Heme B FE en la cadena B ({e}).")
        
    # 3. Calcular el centro de masa global del 24-mer
    # (Promedio de los centros de masa de todas las subunidades para determinar el centro del lumen)
    chain_coms = []
    for chain in model:
        # Solo usar átomos pesados de proteína para el centro del 24-mer
        coords = [atom.get_vector().get_array() for res in chain for atom in res if atom.get_name() == "CA"]
        if coords:
            chain_coms.append(np.mean(coords, axis=0))
            
    lumen_center = np.mean(chain_coms, axis=0)
    print(f"\nCentro de masa global de BFR (Lumen center):")
    print(f"  [{lumen_center[0]:8.3f}, {lumen_center[1]:8.3f}, {lumen_center[2]:8.3f}]")
    
    # 4. Formulación de la Optimización para el Centroide de Au NP
    # Radio de la NP de oro = 10.0 Å (2.0 nm de diámetro)
    R_NP = 10.0
    
    # Coordenadas de los anclajes SG
    anchors = {
        "CYS40 SG": sg40,
        "CYS43 SG": sg43,
        "CYS49 SG": sg49
    }
    
    # Distancias de diseño objetivo desde el centroide (10 Å de radio + gap deseado)
    target_distances = {
        "CYS40 SG": 10.0 + 5.34, # 15.34 Å
        "CYS43 SG": 10.0 + 1.89, # 11.89 Å
        "CYS49 SG": 10.0 + 3.13  # 13.13 Å
    }
    
    def loss_function(P):
        loss = 0.0
        for name, coord in anchors.items():
            dist = np.linalg.norm(P - coord)
            target = target_distances[name]
            loss += (dist - target) ** 2
        return loss
    
    # Conjetura inicial: Promedio de los 3 SG, ligeramente desplazado hacia el centro del lumen
    avg_sg = np.mean([sg40, sg43, sg49], axis=0)
    dir_to_center = lumen_center - avg_sg
    dir_to_center /= np.linalg.norm(dir_to_center)
    initial_guess = avg_sg + dir_to_center * 10.0 # Desplazar 10 Å hacia el interior
    
    # Minimización
    res = minimize(loss_function, initial_guess, method="L-BFGS-B")
    au_center = res.x
    
    print(f"\nCentroide optimizado del Au NP (2.0 nm):")
    print(f"  [{au_center[0]:8.3f}, {au_center[1]:8.3f}, {au_center[2]:8.3f}]")
    print(f"  Pérdida residual de la optimización: {res.fun:.6f}")
    
    # 5. Análisis Geométrico de Resultados
    print(f"\n=== Distancias del Au NP a los Anclajes CYS ===")
    for name, coord in anchors.items():
        dist_centroid = np.linalg.norm(au_center - coord)
        dist_surface = dist_centroid - R_NP
        target_surf = target_distances[name] - R_NP
        print(f"  {name:<10}  |  Al Centroide: {dist_centroid:5.2f} Å  |  A la Superficie: {dist_surface:5.2f} Å (Objetivo: {target_surf:5.2f} Å)")
        
    # Excentricidad
    dist_to_lumen = np.linalg.norm(au_center - lumen_center)
    print(f"\nExcentricidad del Nanoelectrodo:")
    print(f"  Distancia Au NP centro -> Centro del Lumen: {dist_to_lumen:.2f} Å")
    print(f"  (Rango óptimo excéntrico de diseño: 25.0 - 32.0 Å)")
    if 25.0 <= dist_to_lumen <= 32.0:
        print("  [✓] CUMPLE CON EL CRITERIO DE EXCENTRICIDAD V4b")
    else:
        print("  [!] Advertencia: Fuera del rango típico de diseño (25-32 Å)")
        
    # Acoplamiento a Heme B FE
    dist_to_fe = np.linalg.norm(au_center - heme_fe)
    dist_surf_to_fe = dist_to_fe - R_NP
    print(f"\nDistancia de Hopping de Marcus (Canal del Hemo):")
    print(f"  Heme B FE coord                  : [{heme_fe[0]:8.3f}, {heme_fe[1]:8.3f}, {heme_fe[2]:8.3f}]")
    print(f"  Au NP Centroide -> Heme B FE     : {dist_to_fe:.2f} Å")
    print(f"  Au NP Superficie -> Heme B FE    : {dist_surf_to_fe:.2f} Å  (Objetivo V4b: ~9.87 Å)")
    
    # Diagnóstico
    print(f"\nDiagnóstico de Hopping:")
    if dist_surf_to_fe < 15.0:
        print(f"  [✓] Hopping directo Au NP -> Heme FE es altamente viable ({dist_surf_to_fe:.2f} Å < 15 Å).")
    else:
        print(f"  [!] Hopping requiere relays adicionales ({dist_surf_to_fe:.2f} Å > 15 Å).")
        
    print("=" * 75)

if __name__ == "__main__":
    main()
