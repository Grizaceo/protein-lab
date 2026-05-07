#!/usr/bin/env python3
"""
Test de Estabilidad Protein Lab v2.0
CsgA (Curli) y ELP (Elastina) - Secuencias de Joshi et al. (Nature 2024)
"""
import torch
import esm
import os
import pickle
from pathlib import Path

# Secuencias del Articulo 1: Mechanically Tunable PLMs
SEQUENCES = {
    "CsgA_mature": "GVVPQVGPGGNASVDAAVASSSAVTVGQVGAVSNAVAQDSSVKVGLTDITAYGNGPNANSVIALANQSNVKVGMTTVVAYGNGPNASNIYALANQSNVEVGMTTIVSYGNGANASAVVALSQQTNVSVGMTTVTAYGNGPN",
    "ELP_10x": "VPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVG",
    "CsgA_ELP_Fusion": "GVVPQVGPGGNASVDAAVASSSAVTVGQVGAVSNAVAQDSSVKVGLTDITAYGNGPNANSVIALANQSNVKVGMTTVVAYGNGPNASNIYALANQSNVEVGMTTIVSYGNGANASAVVALSQQTNVSVGMTTVTAYGNGPNVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVG"
}

OUTPUT_DIR = Path("/home/gris/.hermes/workspace/protein-lab/exp01-hemoglobina/output/plm_test")
MODEL_NAME = "esm2_t33_650M_UR50D" # El modelo mas grande seguro (2.7GB VRAM)

def run_test():
    print(f"Iniciando test de estabilidad con {MODEL_NAME}...")
    torch.cuda.empty_cache()
    
    # Cargar modelo
    model, alphabet = getattr(esm.pretrained, MODEL_NAME)()
    model = model.cuda()
    batch_converter = alphabet.get_batch_converter()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    for name, seq in SEQUENCES.items():
        print(f"\nProcesando: {name} (L={len(seq)})")
        data = [(name, seq)]
        batch_labels, batch_strs, batch_tokens = batch_converter(data)
        batch_tokens = batch_tokens.cuda()
        
        with torch.no_grad():
            results = model(batch_tokens, repr_layers=[model.num_layers])
            
        rep = results["representations"][model.num_layers][0, 1 : len(seq) + 1].cpu().numpy()
        
        out_file = OUTPUT_DIR / f"{name}_esm2.pkl"
        with open(out_file, "wb") as f:
            pickle.dump({"name": name, "seq": seq, "embeddings": rep}, f)
            
        print(f"OK: Embedding generado. VRAM actual: {torch.cuda.memory_allocated() / 1e9:.2f} GB")

    print("\n" + "="*40)
    print("TEST COMPLETADO EXITOSAMENTE")
    print("="*40)

if __name__ == "__main__":
    run_test()
