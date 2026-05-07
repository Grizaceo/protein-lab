#!/usr/bin/env python3
"""
Exp 1a: Embeddings de hemoglobina con ESM2
============================================

Genera embeddings de secuencia proteica usando ESM2.
Seguro para RTX 4060 8GB — VRAM total <3GB.

Modelos disponibles:
- esm2_t6_8M_UR50D   (7.5M params, 0.03 GB VRAM)
- esm2_t12_35M_UR50D (34M params, 0.13 GB VRAM)
- esm2_t30_150M_UR50D (148M params, 0.59 GB VRAM)
- esm2_t33_650M_UR50D (651M params, 2.67 GB VRAM)
"""

import torch
import esm
import os
import pickle
from pathlib import Path

# Config
PROTEIN_SEQ = "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH"
PROTEIN_NAME = "HBB_human"  # Hemoglobin subunit beta
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "esm2_embeddings"
MODEL_SIZES = ["8M", "35M", "150M", "650M"]

def get_model_name(size):
    mapping = {
        "8M": "esm2_t6_8M_UR50D",
        "35M": "esm2_t12_35M_UR50D",
        "150M": "esm2_t30_150M_UR50D",
        "650M": "esm2_t33_650M_UR50D",
    }
    return mapping.get(size, "esm2_t6_8M_UR50D")

def run_embedding(model_size):
    model_name = get_model_name(model_size)
    print(f"\n{'='*50}")
    print(f"ESM2 {model_size} ({model_name})")
    print(f"{'='*50}")

    # Limpiar VRAM
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()

    # Cargar modelo
    model, alphabet = getattr(esm.pretrained, model_name)()
    model = model.cuda()
    batch_converter = alphabet.get_batch_converter()

    # Preparar secuencia
    data = [(PROTEIN_NAME, PROTEIN_SEQ)]

    # Generar embedding
    batch_labels, batch_strs, batch_tokens = batch_converter(data)
    batch_tokens = batch_tokens.cuda()
    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[model.model.num_layers], return_contacts=False)

    # Obtener embedding del último layer (representación CLS)
    rep = results["representations"][model.model.num_layers][0]  # [seq_len+2, hidden]
    cls_rep = rep[0].cpu().numpy()  # Solo el token CLS

    # Guardar
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"{PROTEIN_NAME}_{model_size}.pkl"

    with open(out_file, "wb") as f:
        pickle.dump({
            "protein": PROTEIN_NAME,
            "sequence": PROTEIN_SEQ,
            "model_size": model_size,
            "model_name": model_name,
            "embedding": cls_rep,
            "embedding_shape": cls_rep.shape,
            "vram_peak_gb": torch.cuda.max_memory_allocated() / 1e9,
        }, f)

    mem_peak = torch.cuda.max_memory_allocated() / 1e9
    print(f"Embedding shape: {cls_rep.shape}")
    print(f"VRAM peak: {mem_peak:.2f} GB")
    print(f"Guardado: {out_file}")

    del model, alphabet, results, rep
    torch.cuda.empty_cache()

    return cls_rep.shape, mem_peak

def main():
    print("="*60)
    print("Exp 1a: ESM2 Embeddings de Hemoglobina")
    print("="*60)
    print(f"Protein: {PROTEIN_NAME}")
    print(f"Length: {len(PROTEIN_SEQ)} residuos")
    print(f"VRAM libre disponible: {torch.cuda.mem_get_info()[0] / 1e9:.1f} GB")

    results = {}
    for size in MODEL_SIZES:
        try:
            shape, mem = run_embedding(size)
            results[size] = {"status": "OK", "shape": shape, "vram_gb": mem}
        except Exception as e:
            print(f"ERROR: {str(e)}")
            results[size] = {"status": "FAIL", "error": str(e)}
            torch.cuda.empty_cache()

    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    for size, res in results.items():
        if res["status"] == "OK":
            print(f"ESM2 {size}: OK — shape {res['shape']}, VRAM {res['vram_gb']:.2f} GB")
        else:
            print(f"ESM2 {size}: FAIL — {res['error'][:60]}")

if __name__ == "__main__":
    main()
