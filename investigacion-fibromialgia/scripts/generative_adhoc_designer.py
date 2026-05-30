#!/usr/bin/env python3
"""
Diseñador Molecular de Novo (Generador Generativo Acoplado a QSAR y Verificación EAC)
Genera combinaciones químicas basadas en el andamio fijo del Pramipexol,
explota las divergencias Ser163 (D2) vs Ala161 (D3) e Ile183 (D2) vs Ser182 (D3),
aplica los filtros EAC del ChemicalVerifier y predice la selectividad 2D QSAR.
"""

import os
import pickle
import numpy as np
import pandas as pd
import time

from rdkit import Chem
from rdkit.Chem import AllChem

# Importar el verificador local
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from chemical_verifier import ChemicalVerifier

def smiles_to_fp(smiles, radius=2, n_bits=2048):
    """Convierte SMILES en Morgan fingerprint numpy array."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        arr = np.zeros((1,))
        Chem.DataStructs.ConvertToNumpyArray(fp, arr)
        return arr
    except Exception:
        return None

def generate_combinatorial_library():
    """
    Genera una librería combinatorial de análogos de Pramipexol.
    Mantiene el núcleo de tetrahydrobenzothiazole-2,6-diamine fijo (SMILES: NC1CCc2nc(N)sc2CC1)
    y acopla cadenas laterales en el nitrógeno del grupo amino en la posición 6.
    Usa índices de anillo independientes (3 y 4) en los R-groups para evitar colisiones
    con los índices (1 y 2) del andamio central.
    """
    print("[INFO] Generando librería combinatorial de análogos...")
    
    # Fragmentos laterales (R-groups) diseñados para:
    # 1. Conservar el puente con Asp114
    # 2. Explotar la polaridad de Ser163 (D2) mediante grupos hidroxilo, amida o amina.
    # 3. Explotar el parche hidrofóbico de Ile183 (D2) mediante grupos aromáticos/alquílicos.
    # 4. Integrar las diclorofenilpiperazinas del Pilar 2.
    # NOTA: Usar el número 3 y 4 para evitar colisiones de anillos.
    
    R_groups = [
        # 1. Cadenas alquílicas simples de control
        "CCC",        # Propilo (Pramipexol original)
        "CCCC",       # Butilo
        "CC(C)C",     # Isobutilo
        "CC(C)",      # Isopropilo
        
        # 2. R-groups polares orientados a la Ser163 de DRD2 (Enlaces de hidrógeno)
        "OCC",        # Etanolamina -> OCCN-scaffold
        "OCCC",       # Propanolamina
        "NC(=O)CC",   # Amida terminal
        "NC(=O)CCC",  # Amida extendida
        "NCC",        # Etilendiamina
        "OCC(O)CC",   # Diol polar
        
        # 3. R-groups hidrofóbicos/planos orientados a la Ile183 de DRD2 (Usar anillo 3)
        "c3ccccc3C",   # Bencil -> c3ccccc3CNC-scaffold
        "c3ccccc3CC",  # Fenetilo
        "C3CCCC3C",    # Ciclopentil-metil
        "C3CCCCC3C",   # Ciclohexil-metil
        
        # 4. Híbridos polares-hidrofóbicos (Selectividad Óptima)
        "Oc3ccc(CCN)cc3",       # Tiramina -> Oc3ccc(CCNC-scaffold)cc3
        "c3ccccc3CNC(=O)C",     # Amida con bencilo
        "C3CCCCC3NC(=O)CC",     # Amida ciclohexilo (rigidez del Pilar 2)
        "CCN(CC)CC3CCCCC3C",    # Terciaria ciclohexilo
        
        # 5. Scaffolds de Diclorofenilpiperazina curados de ChEMBL (Usar anillos 3 y 4)
        "Clc3cccc(Cl)c3N4CCN(CCC)CC4",  # Cadena diclorofenilpiperazina típica
        "Clc3cccc(Cl)c3N4CCN(CCCC)CC4", # Cadena extendida
        "Clc3cccc(Cl)c3N4CCN(CC(=O)CCC)CC4", # Conector carbonilo
        "Clc3cccc(Cl)c3N4CCN(CCN(CC)CCC)CC4", # Conector amina terciaria
        "COc3ccccc3N4CCN(CCC)CC4",      # Aripiprazol-like (orto-metoxifenilo)
        "c3ncccc3N4CCN(CCC)CC4"          # Nafadotride-like (piridin-piperazina)
    ]
    
    generated_compuestos = []
    
    # El scaffold base de Pramipexol es: R-NH-C1CCc2nc(N)sc2CC1.
    # En RDKit, acoplamos concatenando la cadena R con "NC1CCc2nc(N)sc2CC1".
    
    for r_smiles in R_groups:
        try:
            # Ensamblar SMILES con conectores de forma químicamente válida
            if "N4CCN" in r_smiles:
                # Para diclorofenilpiperazinas, acoplamos al nitrógeno terminal de la piperazina
                # Reemplazamos la colilla final de carbono o propilo "CCC)CC4" con el scaffold "NC1CCc2..."
                # p.ej., "Clc3cccc(Cl)c3N4CCN(CCC)CC4" -> "Clc3cccc(Cl)c3N4CCN(CCCNC1CCc2nc(N)sc2CC1)CC4"
                full_smiles = r_smiles.replace("CCC)CC4", "CCCNC1CCc2nc(N)sc2CC1)CC4")
                full_smiles = full_smiles.replace("CCCC)CC4", "CCCCNC1CCc2nc(N)sc2CC1)CC4")
            elif "Oc3ccc(CCN)cc3" in r_smiles:
                # Tiramina
                full_smiles = "Oc3ccc(CCNC1CCc2nc(N)sc2CC1)cc3"
            else:
                # Alquílicos, polares y cicloalcanos simples
                full_smiles = f"{r_smiles}NC1CCc2nc(N)sc2CC1"
                
            # Validar con RDKit
            mol = Chem.MolFromSmiles(full_smiles)
            if mol is not None:
                canonical_smiles = Chem.MolToSmiles(mol, canonical=True)
                generated_compuestos.append(canonical_smiles)
            else:
                print(f"[WARNING] Estructura inválida generada: {full_smiles}")
        except Exception as e:
            print(f"[WARNING] Error al ensamblar fragmento {r_smiles}: {str(e)}")
            
    # Remover duplicados
    generated_compuestos = list(set(generated_compuestos))
    print(f"[INFO] Librería de análogos generada: {len(generated_compuestos)} candidatos únicos.")
    return generated_compuestos

def design_and_screen():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "datos", "model", "d2_d3_qsar_predictor.pkl")
    output_csv = os.path.join(base_dir, "docking_runs", "ad_hoc_design", "generative_adhoc_keys.csv")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
    # 1. Cargar el predictor QSAR 2D
    print(f"[INFO] Cargando predictor QSAR 2D: {os.path.basename(model_path)}")
    if not os.path.exists(model_path):
        print(f"[ERROR] Modelo QSAR no encontrado en {model_path}. Por favor ejecuta train_qsar_selectivity.py primero.")
        return
        
    with open(model_path, 'rb') as f:
        qsar = pickle.load(f)
        
    rf_d2 = qsar["model_d2"]
    rf_d3 = qsar["model_d3"]
    r2_d2 = qsar.get("cv_r2_d2", 0.259)
    r2_d3 = qsar.get("cv_r2_d3", 0.159)
    
    print("\n" + "="*80)
    print("⚠️  ADVERTENCIA DE VALIDEZ PREDICTIVA (QSAR AUDIT)")
    print(f"   Los modelos Random Forest presentan una baja confianza estadística en validación cruzada:")
    print(f"   - DRD2 R² Medio: {r2_d2:.3f} (explica el {r2_d2*100:.1f}% de la varianza)")
    print(f"   - DRD3 R² Medio: {r2_d3:.3f} (explica el {r2_d3*100:.1f}% de la varianza)")
    print("   Las afinidades predichas en nM y ratios de selectividad derivados NO son constantes absolutas.")
    print("   Deben tratarse únicamente como ordenamientos cualitativos / cribados de prioridad.")
    print("="*80 + "\n")
    
    # 2. Inicializar el Verificador SOTA (EAC)
    verifier = ChemicalVerifier()
    
    # 3. Generar la librería de análogos combinatorios
    candidatos_smiles = generate_combinatorial_library()
    
    # 4. Filtrar y predecir en cascada
    resultados = []
    
    print("[INFO] Iniciando el embudo de Verificación SOTA en cascada...")
    
    total_compuestos = len(candidatos_smiles)
    verifier_times = []
    qsar_times = []
    
    for smiles in candidatos_smiles:
        # Paso A: Validación SOTA (Sanitización, Lipinski, QED, PAINS completo, sascorer real)
        t0 = time.perf_counter()
        verdict = verifier.verify_smiles(smiles)
        t1 = time.perf_counter()
        verifier_times.append(t1 - t0)
        
        if verdict["Verdict"] == "DISCARDED_HALLUCINATION":
            # Descartar alucinaciones de inmediato
            continue
            
        # Paso B: Predicción de Afinidad y Selectividad QSAR 2D
        t2 = time.perf_counter()
        fp = smiles_to_fp(smiles)
        if fp is None:
            continue
            
        # Predicción en escala logarítmica (pKi/pIC50)
        pki_d2 = rf_d2.predict(fp.reshape(1, -1))[0]
        pki_d3 = rf_d3.predict(fp.reshape(1, -1))[0]
        
        # Convertir de vuelta a nanomolar (Ki = 10^(9 - pKi))
        ki_d2_nm = 10.0 ** (9.0 - pki_d2)
        ki_d3_nm = 10.0 ** (9.0 - pki_d3)
        
        # Calcular el ratio de selectividad teórica (D3/D2). A mayor ratio, mayor afinidad por D2.
        # selectividad = Ki(D3) / Ki(D2)
        selectivity_ratio = ki_d3_nm / ki_d2_nm
        t3 = time.perf_counter()
        qsar_times.append(t3 - t2)
        
        resultados.append({
            "smiles": smiles,
            "qed_score": verdict["QED"],
            "sa_score": verdict["SAScore"],
            "pred_d2_affinity_nm": round(ki_d2_nm, 3),
            "pred_d3_affinity_nm": round(ki_d3_nm, 3),
            "pred_selectivity_ratio": round(selectivity_ratio, 2),
            "passed_pains": "Yes" if len(verdict["PAINS_Detected"]) == 0 else "No"
        })
        
    # 5. Crear DataFrame, ordenar y exportar
    df_res = pd.DataFrame(resultados)
    
    # Ordenar por el ratio de selectividad D2 (de mayor a menor)
    df_res = df_res.sort_values(by="pred_selectivity_ratio", ascending=False).reset_index(drop=True)
    
    print(f"[INFO] Compuestos supervivientes del embudo SOTA: {len(df_res)}")
    print(f"[INFO] Exportando los mejores candidatos a: {os.path.basename(output_csv)}")
    
    # Guardar las top 50
    df_top = df_res.head(50)
    df_top.to_csv(output_csv, index=False)
    
    # Reportar tiempos de ejecución con rigor matemático
    if verifier_times:
        avg_verifier_ms = (sum(verifier_times) / len(verifier_times)) * 1000
        avg_qsar_ms = (sum(qsar_times) / len(qsar_times)) * 1000 if qsar_times else 0
        total_time_s = sum(verifier_times) + sum(qsar_times)
        
        print("\n" + "-"*80)
        print("📊 CRONOMETRÍA Y PRUEBAS DE INFERENCIA IN SILICO (BENCHMARK)")
        print(f"   Compuestos evaluados: {total_compuestos} | Tiempo total: {total_time_s:.4f} s")
        print(f"   Velocidad del embudo de Verificación SOTA: {avg_verifier_ms * 1000:.2f} µs/moléc ({avg_verifier_ms:.4f} ms/moléc)")
        print(f"   Velocidad de Inferencia QSAR 2D:          {avg_qsar_ms * 1000:.2f} µs/moléc ({avg_qsar_ms:.4f} ms/moléc)")
        print("-"*80)
    
    # Imprimir los 5 mejores candidatos generados de novo
    print("\n=== TOP 5 LLAVES AD HOC GENERADAS DE NOVO ===")
    for i, row in df_top.head(5).iterrows():
        print(f"\nPosición #{i+1}:")
        print(f"   SMILES: {row['smiles']}")
        print(f"   Pred. D2 Afinidad: {row['pred_d2_affinity_nm']} nM")
        print(f"   Pred. D3 Afinidad: {row['pred_d3_affinity_nm']} nM")
        print(f"   Ratio Selectividad Teórica (D3/D2): {row['pred_selectivity_ratio']}x")
        print(f"   Drogabilidad QED: {row['qed_score']} | Sintetizabilidad SA Score: {row['sa_score']}")

if __name__ == "__main__":
    design_and_screen()
