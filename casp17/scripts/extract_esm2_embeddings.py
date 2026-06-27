#!/usr/bin/env python3
"""
extract_esm2_embeddings.py — Generador de embeddings con ESM2-650M
"""
import os
import sys
import time
import torch
import esm
import subprocess

def get_vram_info():
    """Consulta la VRAM libre usando nvidia-smi."""
    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free,memory.total", "--format=csv,noheader,nounits"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        free, total = map(int, res.stdout.strip().split(","))
        return free, total
    except Exception as e:
        print(f"Advertencia: No se pudo consultar nvidia-smi ({e})")
        return None, None

def main():
    target_id = "T1364"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    casp_dir = os.path.dirname(script_dir)
    fasta_path = os.path.join(casp_dir, "targets", f"{target_id}.fasta")
    out_dir = os.path.join(casp_dir, "predictions")
    out_path = os.path.join(out_dir, f"{target_id}_esm2_embeddings.pt")

    os.makedirs(out_dir, exist_ok=True)

    print("=" * 60)
    print("ESM2 Embedding Extractor")
    print("=" * 60)

    # 1. Monitoreo de VRAM antes de empezar
    free, total = get_vram_info()
    if free is not None:
        print(f"VRAM libre inicial: {free} MB / {total} MB")
        if free < 3000:
            print("VRAM libre < 3 GB, liberando caché de PyTorch...")
            torch.cuda.empty_cache()
    else:
        print("Monitoreo de VRAM no disponible (¿no hay GPU o drivers?).")

    # 2. Leer archivo FASTA
    if not os.path.exists(fasta_path):
        print(f"Error: El archivo FASTA no existe: {fasta_path}")
        sys.exit(1)

    with open(fasta_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    header = lines[0].strip()
    sequence = "".join(l.strip() for l in lines[1:] if l.strip())
    seq_len = len(sequence)

    print(f"Secuencia: {header}")
    print(f"Longitud: {seq_len} residuos")

    if seq_len > 500:
        print("ERROR: La secuencia excede 500 residuos (Regla de seguridad).")
        sys.exit(1)

    # 3. Cargar el modelo ESM2
    # Cargar esm2_t33_650M_UR50D (33 capas, 650M params)
    model_name = "esm2_t33_650M_UR50D"
    print(f"Cargando modelo preentrenado {model_name}...")
    start_time = time.time()
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    print(f"Modelo cargado en {time.time() - start_time:.2f} segundos.")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Usando dispositivo: {device}")
    model = model.to(device)
    model.eval()

    # 4. Procesar la secuencia
    batch_converter = alphabet.get_batch_converter()
    data = [(target_id, sequence)]
    batch_labels, batch_strs, batch_tokens = batch_converter(data)
    batch_tokens = batch_tokens.to(device)

    # Medir VRAM después de cargar el modelo en GPU
    free, total = get_vram_info()
    if free is not None:
        print(f"VRAM libre con modelo cargado: {free} MB")

    print("Generando embeddings...")
    start_inference = time.time()
    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[33], return_contacts=False)
    
    # Extraer la última capa (representación per-residuo)
    token_representations = results["representations"][33] # [batch, seq_len_with_special_tokens, embed_dim]
    
    # Quitar los tokens especiales de inicio/fin (<cls>, <eos>)
    # batch_tokens tiene el formato: [cls] residuo1 residuo2 ... [eos] [pad] ...
    # batch_lens tiene el número de tokens sin padding, pero con special tokens
    tokens_len = (batch_tokens[0] != alphabet.padding_idx).sum().item()
    
    # Quitar cls (index 0) y eos (index tokens_len - 1)
    sequence_representations = token_representations[0, 1 : tokens_len - 1].cpu()
    
    inference_time = time.time() - start_inference
    print(f"Inferencia completada en {inference_time:.4f} segundos.")
    print(f"Dimensiones del tensor final: {sequence_representations.shape}")

    # Guardar en archivo
    torch.save(sequence_representations, out_path)
    print(f"Tensor guardado exitosamente en: {out_path}")

    # 5. Limpieza y monitoreo final
    del model
    del results
    del token_representations
    torch.cuda.empty_cache()
    
    free, total = get_vram_info()
    if free is not None:
        print(f"VRAM libre final: {free} MB")

if __name__ == "__main__":
    main()
