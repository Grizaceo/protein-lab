#!/usr/bin/env python3
"""
FASE 2: DUELO DE SECUENCIAS (Joshi vs Rice)
Comparamos el Chasis E. coli (Curli) vs Chasis Caulobacter (S-layer)
Usando ESM2-650M.
"""
import torch
import esm
import numpy as np
import pickle
from pathlib import Path

# --- SECUENCIAS ---
# Joshi Lab (Nature Comm 2024)
CSGA_N = "GVVPQVGPGGNASVDAAVASSSAVTVGQVGAVSNAVAQDSSVKVGLTDITAYGNGPNANSVIALANQSNVKVGMTTVVAYGNGPNASNIYALANQSNVEVGMTTIVSYGNGANASAVVALSQQTNVSVGMTTVTAYGNGPN"
ELP_UNIT = "VPGVG"

# Rice University (Nature Comm 2022 / News 2025)
RSAA_N = "MAYTTAQLVTAYTNANLGKAPDAATTLTLDAYATQTQTGGLSDAAALTNTLKLVNSTTAVAIQTYQFFTGVAPSAAGLDFLVDSTTNTNDLNDAYYSKFAQENRFINFSINLATGAGAGATAFAAAYTGVSYAQTVATAYDKIIGNAVATAAGVDVAAAVAFLSRQANIDYLTAFVRANTPFTAAADIDLAVKAALIGTILNAATVSGIGGYATATAAMINDLSDGALSTDNAAGVNLFTAYPSSGV"
RSAA_C = "AFGAAVTLGAAATLAQYLDAAAAGDGSGTSVAKWFQFGGDTYVVVDSSAGATFVSGADAVIKLTGLVTLTTSAFATEVLTLA"

DUEL_SEQS = {
    "JOSHI_CSGA_ELP10": CSGA_N + (ELP_UNIT * 10),
    "RICE_BUD40": RSAA_N + (ELP_UNIT * 40) + RSAA_C,
    "RICE_BUD60": RSAA_N + (ELP_UNIT * 60) + RSAA_C,
    "RICE_BUD80": RSAA_N + (ELP_UNIT * 80) + RSAA_C
}

MODEL_NAME = "esm2_t33_650M_UR50D"
OUTPUT_DIR = Path("/home/gris/.hermes/workspace/protein-lab/exp01-hemoglobina/output/duel_results")

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def run_duel():
    print(f"--- Iniciando Duelo de Secuencias (ESM2-650M) ---")
    torch.cuda.empty_cache()
    
    model, alphabet = getattr(esm.pretrained, MODEL_NAME)()
    model = model.cuda()
    batch_converter = alphabet.get_batch_converter()
    
    embs = {}
    
    for name, seq in DUEL_SEQS.items():
        print(f"Analizando: {name} | Longitud: {len(seq)} residues")
        data = [(name, seq)]
        _, _, batch_tokens = batch_converter(data)
        batch_tokens = batch_tokens.cuda()
        
        with torch.no_grad():
            results = model(batch_tokens, repr_layers=[model.num_layers])
            
        # Tomamos el vector promedio de la secuencia completa (Global Representation)
        rep = results["representations"][model.num_layers][0, 1 : len(seq) + 1].mean(0).cpu().numpy()
        embs[name] = rep
        
        print(f"  OK. VRAM peak: {torch.cuda.max_memory_allocated() / 1e9:.2f} GB")

    # Analisis de Similitud
    print("\n--- Resultados de Similitud Semantica (Cosine Similarity) ---")
    keys = list(embs.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            sim = cosine_sim(embs[keys[i]], embs[keys[j]])
            print(f"{keys[i]} vs {keys[j]}: {sim:.4f}")

    # Guardar
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "duel_data.pkl", "wb") as f:
        pickle.dump(embs, f)
    
    print(f"\nDatos guardados en {OUTPUT_DIR}")

if __name__ == "__main__":
    run_duel()
