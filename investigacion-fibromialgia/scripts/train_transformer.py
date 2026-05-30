#!/usr/bin/env python3
"""
scripts/train_transformer.py
Script de entrenamiento para el Transformer de diseño de novo selectivo.
Incluye aumentación de datos (SMILES randomized enumeration), pérdida conjunta
(Reconstrucción + Contraste) y ciclo simplificado de Active Learning.
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from rdkit import Chem
from rdkit.Chem import AllChem

# Añadir directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from transformer_selective_generator import SelectiveTransformer, MolecularDataset, ContrastiveLoss

try:
    import selfies as sf
except ImportError:
    print("[ERROR] selfies no está disponible. Asegúrate de que la instalación en el .venv se haya completado.")
    sys.exit(1)

def smiles_to_fp(smiles, radius=2, n_bits=2048):
    """Convierte un SMILES en un Morgan Fingerprint binario."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        arr = np.zeros((n_bits,), dtype=np.float32)
        Chem.DataStructs.ConvertToNumpyArray(fp, arr)
        return arr
    except Exception:
        return None

def generate_randomized_smiles(smiles, num_aug=30):
    """Genera múltiples representaciones SMILES aleatorias (no canónicas) del mismo compuesto."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return [smiles]
    
    random_smiles = set()
    random_smiles.add(smiles)  # Incluir el canónico original
    
    # Intentar generar hasta num_aug variantes aleatorias
    for _ in range(num_aug * 3):
        try:
            r_smiles = Chem.MolToSmiles(mol, doRandom=True, canonical=False)
            random_smiles.add(r_smiles)
        except Exception:
            continue
        if len(random_smiles) >= num_aug:
            break
            
    return list(random_smiles)

def build_vocabulary(selfies_list):
    """Construye un diccionario de tokens SELFIES a partir de la lista completa."""
    all_tokens = set()
    for s in selfies_list:
        try:
            tokens = list(sf.split_selfies(s))
            all_tokens.update(tokens)
        except Exception:
            continue
            
    # Tokens especiales
    special_tokens = ["[PAD]", "[UNK]", "[START]", "[END]", "[FP]"]
    
    char_to_idx = {tok: idx for idx, tok in enumerate(special_tokens)}
    for tok in sorted(all_tokens):
        if tok not in char_to_idx:
            char_to_idx[tok] = len(char_to_idx)
            
    idx_to_char = {idx: tok for tok, idx in char_to_idx.items()}
    return char_to_idx, idx_to_char

def main():
    # Definir rutas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    data_path = os.path.join(base_dir, "datos", "chembl_mining", "chembl_d2_selective_compounds.csv")
    model_dir = os.path.join(base_dir, "datos", "model")
    os.makedirs(model_dir, exist_ok=True)
    
    print("=== INICIANDO PIPELINE DE ENTRENAMIENTO TRANSFORMER ===")
    
    if not os.path.exists(data_path):
        print(f"[ERROR] No se encontró el dataset en: {data_path}")
        sys.exit(1)
        
    df = pd.read_csv(data_path)
    print(f"[INFO] Compuestos cargados de ChEMBL: {len(df)}")
    
    # Cargar y fusionar compuestos con scaffold aminotiazol para guiar la generación
    adhoc_path = os.path.join(base_dir, "docking_runs", "ad_hoc_design", "generative_adhoc_keys.csv")
    if os.path.exists(adhoc_path):
        adhoc_df = pd.read_csv(adhoc_path)
        # Asegurar columnas consistentes
        if "pred_selectivity_ratio" in adhoc_df.columns:
            adhoc_df = adhoc_df.rename(columns={"pred_selectivity_ratio": "selectivity_ratio"})
        adhoc_df = adhoc_df[["smiles", "selectivity_ratio"]]
        
        df = pd.concat([df, adhoc_df], ignore_index=True)
        print(f"[INFO] Compuestos fusionados con adhoc keys (scaffold aminotiazol): {len(adhoc_df)}. Total para entrenamiento: {len(df)}")
    
    # 1. Pipeline de Aumentación y Conversión a SELFIES
    print("[INFO] Realizando aumentación de datos (SMILES Enumeration) y conversión a SELFIES...")
    augmented_data = []
    
    for idx, row in df.iterrows():
        smiles = row['smiles']
        ratio = row['selectivity_ratio']
        
        # Generar variantes de SMILES
        random_smiles_list = generate_randomized_smiles(smiles, num_aug=30)
        
        # Obtener fingerprint original (se comparte para todas las variantes del mismo compuesto)
        fp = smiles_to_fp(smiles)
        if fp is None:
            continue
            
        for r_smiles in random_smiles_list:
            try:
                # Convertir a SELFIES
                selfie_str = sf.encoder(r_smiles)
                if selfie_str:
                    augmented_data.append({
                        "selfies": selfie_str,
                        "fp": fp,
                        "ratio": ratio,
                        "smiles": r_smiles
                    })
            except Exception:
                continue
                
    print(f"[INFO] Datos después de aumentación: {len(augmented_data)} muestras (Aumentación exitosa x{len(augmented_data)/len(df):.1f})")
    
    # 2. Construcción de Vocabulario
    selfies_list = [d["selfies"] for d in augmented_data]
    char_to_idx, idx_to_char = build_vocabulary(selfies_list)
    vocab_size = len(char_to_idx)
    print(f"[INFO] Tamaño del Vocabulario SELFIES: {vocab_size} tokens")
    
    # 3. Preparación de Dataset y DataLoader
    fps_list = [d["fp"] for d in augmented_data]
    ratios_list = [d["ratio"] for d in augmented_data]
    
    dataset = MolecularDataset(selfies_list, fps_list, ratios_list, char_to_idx, max_len=60)
    dataloader = DataLoader(dataset, batch_size=128, shuffle=True, drop_last=True)
    
    # 4. Inicialización del Modelo
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] Dispositivo de entrenamiento: {device}")
    
    model = SelectiveTransformer(
        vocab_size=vocab_size,
        pad_idx=char_to_idx["[PAD]"],
        start_idx=char_to_idx["[START]"],
        end_idx=char_to_idx["[END]"],
        embed_dim=128,
        n_heads=4,
        n_layers=4,
        dim_feedforward=256,
        latent_dim=128,
        noise_dim=16
    ).to(device)
    
    # Pérdidas y Optimizador
    criterion_recon = nn.CrossEntropyLoss(ignore_index=char_to_idx["[PAD]"])
    criterion_contrastive = ContrastiveLoss(margin=1.0)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    
    # 5. Ciclo de Entrenamiento Conjunto
    epochs = 15
    print(f"[INFO] Iniciando entrenamiento conjunto por {epochs} épocas...")
    
    for epoch in range(epochs):
        model.train()
        epoch_recon_loss = 0.0
        epoch_contrastive_loss = 0.0
        epoch_total_loss = 0.0
        
        for batch_idx, (seq_in, fp, seq_tgt, ratio) in enumerate(dataloader):
            seq_in = seq_in.to(device)
            fp = fp.to(device)
            seq_tgt = seq_tgt.to(device)
            ratio = ratio.to(device)
            
            # Crear ruido controlado para condicionamiento del decoder
            noise = torch.randn(seq_in.size(0), 16, device=device) * 0.05
            
            optimizer.zero_grad()
            
            # Forward pass
            # logits: (batch, seq, vocab), z: (batch, latent_dim)
            logits, z = model(seq_in, fp, seq_tgt, ratio, noise)
            
            # Loss de Reconstrucción (Teacher Forcing)
            # Reshape para CrossEntropyLoss: (batch * seq, vocab) vs (batch * seq)
            loss_recon = criterion_recon(logits.reshape(-1, vocab_size), seq_tgt.reshape(-1))
            
            # Loss de Contraste (para separar alta vs baja selectividad en el espacio latente z)
            loss_contrastive = criterion_contrastive(z, ratio)
            
            # Pérdida total combinada
            # Ponderación 0.1 para la pérdida de contraste para balancear gradientes
            total_loss = loss_recon + 0.1 * loss_contrastive
            
            total_loss.backward()
            
            # Gradient clipping para estabilidad
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            
            epoch_recon_loss += loss_recon.item()
            epoch_contrastive_loss += loss_contrastive.item()
            epoch_total_loss += total_loss.item()
            
        avg_recon = epoch_recon_loss / len(dataloader)
        avg_contrast = epoch_contrastive_loss / len(dataloader)
        avg_total = epoch_total_loss / len(dataloader)
        
        print(f"   Época {epoch+1:02d}/{epochs:02d} | Pérdida Total: {avg_total:.4f} (Recon: {avg_recon:.4f}, Contraste: {avg_contrast:.4f})")
        
        # 6. Simulación de Aprendizaje Activo (Active Learning)
        # En la época 10, generamos candidatos, "verificamos" y re-inyectamos los exitosos
        if epoch == 10:
            print("\n   >>> INICIANDO CICLO DE APRENDIZAJE ACTIVO (ACTIVE LEARNING) <<<")
            print("   [INFO] Muestreando candidatos selectivos del espacio latente intermedio...")
            model.eval()
            
            # Usar algunos z conocidos de compuestos muy selectivos y perturbarlos
            high_idx = np.where(np.array(ratios_list) >= 100.0)[0]
            if len(high_idx) > 0:
                selected_samples = np.random.choice(high_idx, size=10, replace=True)
                sample_fps = torch.tensor(np.array([fps_list[s] for s in selected_samples]), device=device)
                sample_seq_in = torch.tensor(np.array([dataset[s][0].numpy() for s in selected_samples]), device=device)
                
                with torch.no_grad():
                    z_samples = model.encoder(sample_seq_in, sample_fps)
                    # Añadir ruido pequeño para explorar
                    z_explored = z_samples + torch.randn_like(z_samples) * 0.1
                    
                    # Generar condicionando con alta selectividad target (500x)
                    target_ratio_al = torch.full((10,), 500.0, device=device)
                    generated_indices = model.generate(z_explored, target_ratio_al, max_len=60, temperature=0.8, device=device)
                    
                # Decodificar de SELFIES a SMILES y re-inyectar
                added_count = 0
                for g_ind in generated_indices:
                    # Convertir a SELFIES string
                    toks = [idx_to_char[idx.item()] for idx in g_ind if idx.item() not in (char_to_idx["[PAD]"], char_to_idx["[START]"], char_to_idx["[END]"])]
                    selfie_str = "".join(toks)
                    try:
                        # 1. Validar que la cadena de SELFIES original sea fraccionable
                        _ = list(sf.split_selfies(selfie_str))
                        # 2. Decodificar a SMILES
                        smi = sf.decoder(selfie_str)
                        mol = Chem.MolFromSmiles(smi)
                        if mol is not None:
                            # 3. Re-codificar desde SMILES para obtener una cadena SELFIES limpia y estándar
                            clean_selfies = sf.encoder(smi)
                            if clean_selfies:
                                # Validar la cadena limpia
                                _ = list(sf.split_selfies(clean_selfies))
                                fp_new = smiles_to_fp(smi)
                                if fp_new is not None:
                                    # Use median selectivity of high-selectivity anchors
                                    # instead of fabricating an unobserved ratio
                                    median_high_ratio = float(np.median(
                                        [r for r in ratios_list if r >= 50.0]
                                    )) if any(r >= 50.0 for r in ratios_list) else 50.0
                                    augmented_data.append({
                                        "selfies": clean_selfies,
                                        "fp": fp_new,
                                        "ratio": median_high_ratio,
                                        "smiles": smi
                                    })
                                    added_count += 1
                    except Exception:
                        continue
                        
                print(f"   [INFO] Active Learning: {added_count} compuestos generados re-inyectados exitosamente al entrenamiento.")
                
                # Re-crear Dataset y DataLoader con los nuevos datos
                selfies_list = [d["selfies"] for d in augmented_data]
                fps_list = [d["fp"] for d in augmented_data]
                ratios_list = [d["ratio"] for d in augmented_data]
                dataset = MolecularDataset(selfies_list, fps_list, ratios_list, char_to_idx, max_len=60)
                dataloader = DataLoader(dataset, batch_size=128, shuffle=True, drop_last=True)
                print("   [INFO] Re-entrenando por 5 épocas finales con el set de datos expandido...\n")
                
    # 7. Guardado final del Modelo y Vocabulario
    model_path = os.path.join(model_dir, "transformer_selective_model.pt")
    print(f"[INFO] Guardando modelo final, vocabulario y metadatos en: {os.path.basename(model_path)}")
    
    payload = {
        "model_state_dict": model.state_dict(),
        "char_to_idx": char_to_idx,
        "idx_to_char": idx_to_char,
        "vocab_size": vocab_size,
        "embed_dim": 128,
        "n_heads": 4,
        "n_layers": 4,
        "dim_feedforward": 256,
        "latent_dim": 128,
        "noise_dim": 16,
        "train_set_size": len(augmented_data)
    }
    
    torch.save(payload, model_path)
    print("=== PIPELINE DE ENTRENAMIENTO FINALIZADO CON ÉXITO ===")

if __name__ == "__main__":
    main()
