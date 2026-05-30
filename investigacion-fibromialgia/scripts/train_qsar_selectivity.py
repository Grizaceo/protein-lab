#!/usr/bin/env python3
"""
Módulo de Entrenamiento de Predictor QSAR D2/D3 (Local Expert Model)
Entrena dos modelos Random Forest Regressor para predecir afinidades pKi/pIC50 en D2 y D3.
Genera la base predictiva para el pipeline generativo de de novo design.
"""

import os
import pickle
import numpy as np
import pandas as pd

from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, KFold

def smiles_to_fp(smiles, radius=2, n_bits=2048):
    """Convierte un SMILES en un Morgan Fingerprint (huella digital 2D) binario."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        # Convertir a ECFP4 fingerprint
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        arr = np.zeros((1,))
        Chem.DataStructs.ConvertToNumpyArray(fp, arr)
        return arr
    except Exception:
        return None

def train_and_evaluate():
    # Rutas
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "datos", "chembl_mining", "chembl_d2_selective_compounds.csv")
    model_dir = os.path.join(base_dir, "datos", "model")
    os.makedirs(model_dir, exist_ok=True)
    
    print(f"[INFO] Cargando base de datos curada de ChEMBL: {os.path.basename(data_path)}")
    if not os.path.exists(data_path):
        print(f"[ERROR] Archivo no encontrado en {data_path}")
        return
        
    df = pd.read_csv(data_path)
    print(f"[INFO] Registros iniciales cargados: {len(df)}")
    
    # Procesar características (SMILES -> Morgan Fingerprints)
    fps = []
    valid_indices = []
    
    for idx, row in df.iterrows():
        fp = smiles_to_fp(row['smiles'])
        if fp is not None:
            fps.append(fp)
            valid_indices.append(idx)
            
    df_clean = df.iloc[valid_indices].copy()
    X = np.array(fps)
    
    # Afinidades en pKi/pIC50 (escala logarítmica: -log10(affinity_nM * 1e-9))
    # affinity es en nM, entonces 1 nM = 1e-9 M. pKi = 9 - log10(affinity_nM)
    y_d2 = 9.0 - np.log10(df_clean['d2_affinity_nm'].values)
    y_d3 = 9.0 - np.log10(df_clean['d3_affinity_nm'].values)
    
    print(f"[INFO] Compuestos químicamente válidos procesados: {len(X)}")
    
    # Definir hiperparámetros de Random Forest
    rf_d2 = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf_d3 = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    
    # Validación cruzada K-Fold (5 pliegues)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    print("[INFO] Evaluando modelo QSAR para DRD2 mediante validación cruzada...")
    cv_scores_d2 = cross_val_score(rf_d2, X, y_d2, cv=kf, scoring='r2')
    print(f"   R2 medio (DRD2): {np.mean(cv_scores_d2):.3f} (SD: {np.std(cv_scores_d2):.3f})")
    
    print("[INFO] Evaluando modelo QSAR para DRD3 mediante validación cruzada...")
    cv_scores_d3 = cross_val_score(rf_d3, X, y_d3, cv=kf, scoring='r2')
    print(f"   R2 medio (DRD3): {np.mean(cv_scores_d3):.3f} (SD: {np.std(cv_scores_d3):.3f})")
    
    # Entrenar modelos finales con el 100% de los datos
    print("[INFO] Entrenando modelos QSAR finales...")
    rf_d2.fit(X, y_d2)
    rf_d3.fit(X, y_d3)
    
    # Guardar los modelos en un único archivo
    model_path = os.path.join(model_dir, "d2_d3_qsar_predictor.pkl")
    print(f"[INFO] Guardando modelos QSAR serializados en: {os.path.basename(model_path)}")
    
    payload = {
        "model_d2": rf_d2,
        "model_d3": rf_d3,
        "n_bits": 2048,
        "radius": 2,
        "cv_r2_d2": np.mean(cv_scores_d2),
        "cv_r2_d3": np.mean(cv_scores_d3)
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(payload, f)
        
    print("[INFO] Entrenamiento y guardado finalizados con éxito!")

if __name__ == "__main__":
    train_and_evaluate()
