#!/usr/bin/env python3
"""
scripts/transformer_selective_generator.py
Diseño de la arquitectura del Transformer (Encoder-Decoder) con pérdida contrastiva 
para generación molecular de novo condicionada para selectividad DRD2>DRD3.
"""

import math
import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset

try:
    import selfies as sf
except ImportError:
    pass  # Se espera que se instale en el entorno

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=150):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(1)  # (max_len, 1, d_model)
        self.register_buffer('pe', pe)

    def forward(self, x):
        # x shape: (seq_len, batch_size, d_model)
        return x + self.pe[:x.size(0)]

class SelectivityEncoder(nn.Module):
    """
    Encoder de selectividad molecular.
    Input:
        - Morgan Fingerprint ECFP4 (2048 bits)
        - Secuencia de tokens SELFIES
    Une ambos descriptores proyectando el fingerprint como un token especial de inicio [FP] 
    y procesando la secuencia unificada con un Transformer Encoder.
    """
    def __init__(self, vocab_size, embed_dim=128, n_heads=4, n_layers=4, dim_feedforward=256, latent_dim=128):
        super().__init__()
        self.embed_dim = embed_dim
        self.token_embeddings = nn.Embedding(vocab_size, embed_dim)
        self.fp_projector = nn.Linear(2048, embed_dim)
        
        self.pos_encoder = PositionalEncoding(embed_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, 
            nhead=n_heads, 
            dim_feedforward=dim_feedforward,
            dropout=0.1
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        
        # Proyección final del token [FP] al espacio latente z
        self.fc_z = nn.Linear(embed_dim, latent_dim)

    def forward(self, selfies_seq, fp_bits):
        # selfies_seq: (batch_size, seq_len)
        # fp_bits: (batch_size, 2048)
        batch_size = selfies_seq.size(0)
        
        # 1. Embeddings de la secuencia
        seq_embed = self.token_embeddings(selfies_seq)  # (batch_size, seq_len, embed_dim)
        seq_embed = seq_embed.transpose(0, 1)  # (seq_len, batch_size, embed_dim)
        
        # 2. Embedding del fingerprint proyectado
        fp_embed = self.fp_projector(fp_bits)  # (batch_size, embed_dim)
        fp_embed = fp_embed.unsqueeze(0)  # (1, batch_size, embed_dim)
        
        # 3. Concatenación: prepended [FP] token
        full_embed = torch.cat([fp_embed, seq_embed], dim=0)  # (seq_len + 1, batch_size, embed_dim)
        
        # 4. Codificación posicional y Transformer
        full_embed = self.pos_encoder(full_embed)
        encoded = self.transformer_encoder(full_embed)  # (seq_len + 1, batch_size, embed_dim)
        
        # 5. Extraer el primer token [FP] como representación global latente z
        fp_latent = encoded[0]  # (batch_size, embed_dim)
        z = self.fc_z(fp_latent)  # (batch_size, latent_dim)
        return z

class ContrastiveLoss(nn.Module):
    """
    Contrastive Loss pairwise.
    Separa compuestos altamente selectivos (ratio >= 100) de los moderadamente o no selectivos.
    Fórmula:
        L = y * d^2 + (1 - y) * max(0, margin - d)^2
    Donde d es la distancia euclidiana entre z_i y z_j en el lote.
    - y_ij = 1 si ambos son altamente selectivos (ratio >= 100).
    - y_ij = 0 si uno es altamente selectivo (ratio >= 100) y el otro es bajo selectivo (ratio < 20).
    """
    def __init__(self, margin=1.0):
        super().__init__()
        self.margin = margin

    def forward(self, z, ratios):
        # z: (batch_size, latent_dim)
        # ratios: (batch_size) - ratios reales del dataset
        batch_size = z.size(0)
        if batch_size < 2:
            return torch.tensor(0.0, device=z.device, requires_grad=True)

        # Calcular distancias euclidianas por pares
        # dist_matrix[i, j] = sqrt(||z_i - z_j||_2^2 + eps)
        r2 = torch.sum(z*z, dim=1, keepdim=True)
        dist_sq = r2 - 2 * torch.matmul(z, z.t()) + r2.t()
        dist_matrix = torch.sqrt(torch.clamp(dist_sq, min=1e-8))

        # Crear máscaras para pares positivos y negativos
        # Compuestos altamente selectivos (High): ratio >= 100
        # Compuestos poco selectivos (Low): ratio < 20
        is_high = (ratios >= 100.0)
        is_low = (ratios < 25.0)

        # Matriz indicadora de similaridad (ambos altamente selectivos -> y = 1)
        # expand_dims para hacer producto cruzado lógico
        high_i = is_high.unsqueeze(1)
        high_j = is_high.unsqueeze(0)
        y_pos = (high_i & high_j).float()  # 1 si ambos son de alta selectividad

        # Matriz indicadora de disimilitud (uno alta y otro baja selectividad -> y = 0)
        low_i = is_low.unsqueeze(1)
        low_j = is_low.unsqueeze(0)
        y_neg = ((high_i & low_j) | (low_i & high_j)).float()

        # Evitar auto-comparaciones (diagonal a 0)
        diag_mask = 1.0 - torch.eye(batch_size, device=z.device)
        y_pos = y_pos * diag_mask
        y_neg = y_neg * diag_mask

        # Pérdida para pares similares (atraerlos)
        loss_pos = y_pos * torch.pow(dist_matrix, 2)
        
        # Pérdida para pares disimilares (repelerlos con margen)
        loss_neg = y_neg * torch.pow(torch.clamp(self.margin - dist_matrix, min=0.0), 2)

        # Normalización
        num_pos = torch.sum(y_pos)
        num_neg = torch.sum(y_neg)

        total_loss = 0.0
        if num_pos > 0:
            total_loss += torch.sum(loss_pos) / num_pos
        if num_neg > 0:
            total_loss += torch.sum(loss_neg) / num_neg

        return total_loss

class ConditionalDecoder(nn.Module):
    """
    Decoder molecular condicional.
    Input:
        - Latent vector z (del encoder)
        - Ratio de selectividad target y ruido controlado
        - Secuencia de tokens SELFIES (con teacher forcing)
    """
    def __init__(self, vocab_size, embed_dim=128, n_heads=4, n_layers=4, dim_feedforward=256, latent_dim=128, noise_dim=16):
        super().__init__()
        self.embed_dim = embed_dim
        self.token_embeddings = nn.Embedding(vocab_size, embed_dim)
        
        # Condicionamiento: z + log10(ratio) + ruido
        cond_in_dim = latent_dim + 1 + noise_dim
        self.cond_projector = nn.Linear(cond_in_dim, embed_dim)
        
        self.pos_encoder = PositionalEncoding(embed_dim)
        
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=embed_dim, 
            nhead=n_heads, 
            dim_feedforward=dim_feedforward,
            dropout=0.1
        )
        self.transformer_decoder = nn.TransformerDecoder(decoder_layer, num_layers=n_layers)
        
        self.fc_out = nn.Linear(embed_dim, vocab_size)

    def forward(self, target_seq, z, target_ratio, noise):
        # target_seq: (batch_size, seq_len)
        # z: (batch_size, latent_dim)
        # target_ratio: (batch_size) - log10(selectivity_ratio)
        # noise: (batch_size, noise_dim)
        batch_size = target_seq.size(0)
        
        # 1. Construir vector de condicionamiento y proyectar
        # target_ratio debe tener forma (batch_size, 1)
        target_ratio_in = torch.log10(torch.clamp(target_ratio, min=1.0)).unsqueeze(1)
        cond_vector = torch.cat([z, target_ratio_in, noise], dim=1)  # (batch_size, cond_in_dim)
        memory = self.cond_projector(cond_vector)  # (batch_size, embed_dim)
        memory = memory.unsqueeze(0)  # (1, batch_size, embed_dim) - memory para la atención cruzada
        
        # 2. Embeddings del target
        tgt_embed = self.token_embeddings(target_seq)  # (batch_size, seq_len, embed_dim)
        tgt_embed = tgt_embed.transpose(0, 1)  # (seq_len, batch_size, embed_dim)
        tgt_embed = self.pos_encoder(tgt_embed)
        
        # 3. Máscara causal del autoregresor
        seq_len = target_seq.size(1)
        device = target_seq.device
        # Mask shape: (seq_len, seq_len) con -inf en la parte superior derecha
        tgt_mask = nn.Transformer.generate_square_subsequent_mask(seq_len, device=device)
        
        # 4. Decodificación
        decoded = self.transformer_decoder(
            tgt=tgt_embed, 
            memory=memory, 
            tgt_mask=tgt_mask
        )  # (seq_len, batch_size, embed_dim)
        
        # 5. Proyección a logits
        logits = self.fc_out(decoded)  # (seq_len, batch_size, vocab_size)
        logits = logits.transpose(0, 1)  # (batch_size, seq_len, vocab_size)
        return logits

class SelectiveTransformer(nn.Module):
    """
    Pipeline Generativo Transformer Completo.
    """
    def __init__(self, vocab_size, pad_idx, start_idx, end_idx, embed_dim=128, n_heads=4, n_layers=4, dim_feedforward=256, latent_dim=128, noise_dim=16):
        super().__init__()
        self.pad_idx = pad_idx
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.vocab_size = vocab_size
        self.latent_dim = latent_dim
        self.noise_dim = noise_dim
        
        self.encoder = SelectivityEncoder(
            vocab_size=vocab_size,
            embed_dim=embed_dim,
            n_heads=n_heads,
            n_layers=n_layers,
            dim_feedforward=dim_feedforward,
            latent_dim=latent_dim
        )
        
        self.decoder = ConditionalDecoder(
            vocab_size=vocab_size,
            embed_dim=embed_dim,
            n_heads=n_heads,
            n_layers=n_layers,
            dim_feedforward=dim_feedforward,
            latent_dim=latent_dim,
            noise_dim=noise_dim
        )

    def forward(self, seq_in, fp_bits, seq_tgt, selectivity_ratio, noise):
        # Codificar
        z = self.encoder(seq_in, fp_bits)
        # Decodificar
        logits = self.decoder(seq_in, z, selectivity_ratio, noise)
        return logits, z

    def generate(self, z, target_ratio, max_len=60, temperature=0.8, top_k=10, device="cpu"):
        """
        Generación condicional paso a paso (Autoregresiva).
        z: (batch_size, latent_dim) o None (si es None, generamos z aleatorio a partir de selectividad target)
        """
        batch_size = z.size(0)
        self.eval()
        
        # Ruido para generación
        noise = torch.randn(batch_size, self.noise_dim, device=device) * 0.05
        
        # Inicializar secuencias con token de inicio [START]
        generated = torch.full((batch_size, 1), self.start_idx, dtype=torch.long, device=device)
        
        # Vector de condicionamiento
        target_ratio_in = torch.log10(torch.clamp(target_ratio, min=1.0)).unsqueeze(1)
        cond_vector = torch.cat([z, target_ratio_in, noise], dim=1)  # (batch_size, cond_in_dim)
        memory = self.decoder.cond_projector(cond_vector).unsqueeze(0)  # (1, batch_size, embed_dim)
        
        finished = torch.zeros(batch_size, dtype=torch.bool, device=device)
        
        with torch.no_grad():
            for step in range(max_len - 1):
                # Embeddings del target generado hasta ahora
                tgt_embed = self.decoder.token_embeddings(generated).transpose(0, 1)
                tgt_embed = self.decoder.pos_encoder(tgt_embed)
                
                # Máscara causal para autoregresión
                tgt_mask = nn.Transformer.generate_square_subsequent_mask(generated.size(1), device=device)
                
                # Decodificar
                decoded = self.decoder.transformer_decoder(tgt=tgt_embed, memory=memory, tgt_mask=tgt_mask)
                logits = self.decoder.fc_out(decoded[-1])  # Tomar el último paso temporal: (batch_size, vocab_size)
                
                # Modulación por temperatura
                logits = logits / max(temperature, 1e-5)
                
                # Aplicar filtrado Top-K para evitar colas de baja probabilidad
                if top_k > 0:
                    v, _ = torch.topk(logits, min(top_k, self.vocab_size))
                    min_values = v[:, -1].unsqueeze(1)
                    logits = torch.where(logits < min_values, torch.full_like(logits, -float("Inf")), logits)
                
                # Muestrear token de la distribución multinomial
                probs = F.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)  # (batch_size, 1)
                
                # Reemplazar tokens para secuencias ya terminadas con [PAD]
                next_token = torch.where(finished.unsqueeze(1), torch.full_like(next_token, self.pad_idx), next_token)
                
                # Concatenar al historial
                generated = torch.cat([generated, next_token], dim=1)
                
                # Actualizar máscara de finalizados
                finished |= (next_token.squeeze(1) == self.end_idx)
                
                if finished.all():
                    break
                    
        return generated

class MolecularDataset(Dataset):
    """
    Dataset para entrenamiento con SELFIES y Fingerprints.
    """
    def __init__(self, selfies_list, fp_list, selectivity_list, char_to_idx, max_len=60):
        self.selfies_list = selfies_list
        self.fp_list = fp_list
        self.selectivity_list = selectivity_list
        self.char_to_idx = char_to_idx
        self.max_len = max_len
        self.pad_idx = char_to_idx["[PAD]"]
        self.start_idx = char_to_idx["[START]"]
        self.end_idx = char_to_idx["[END]"]

    def __len__(self):
        return len(self.selfies_list)

    def __getitem__(self, idx):
        selfie_str = self.selfies_list[idx]
        fp = self.fp_list[idx]
        ratio = self.selectivity_list[idx]
        
        # Tokenizar SELFIES
        tokens = list(sf.split_selfies(selfie_str))
        
        # Truncar si es necesario
        if len(tokens) > self.max_len - 2:
            tokens = tokens[:self.max_len - 2]
            
        # Mapear a índices
        token_indices = [self.char_to_idx.get(t, self.char_to_idx["[UNK]"]) for t in tokens]
        
        # Crear secuencias de entrada y objetivo
        # Entrada: [START] t1 t2 ... tn [PAD] [PAD]
        # Objetivo: t1 t2 ... tn [END] [PAD] [PAD]
        seq_in = [self.start_idx] + token_indices
        seq_tgt = token_indices + [self.end_idx]
        
        # Rellenar con PAD
        padding_len = self.max_len - len(seq_in)
        if padding_len > 0:
            seq_in = seq_in + [self.pad_idx] * padding_len
            seq_tgt = seq_tgt + [self.pad_idx] * padding_len
            
        return (
            torch.tensor(seq_in, dtype=torch.long),
            torch.tensor(fp, dtype=torch.float32),
            torch.tensor(seq_tgt, dtype=torch.long),
            torch.tensor(ratio, dtype=torch.float32)
        )
