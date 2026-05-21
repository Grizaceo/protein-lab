#!/usr/bin/env python3
"""
Generate ESM2 per-residue embeddings for all FM-relevant protein targets.
Uses explicit PDB mapping to avoid naming issues.
"""

import os
import torch
import esm
from pathlib import Path
from Bio.PDB import PDBParser

# === CONFIGURATION ===
BASE_DIR = Path(__file__).resolve().parent.parent
PDB_DIR = BASE_DIR / "datos" / "pdb"
OUT_DIR = BASE_DIR / "analisis" / "esm2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ESM2 model: 150M safe for 8GB VRAM
MODEL_NAME = "esm2_t30_150M_UR50D"

# Explicit mapping: target standard name → PDB file (and optional chain)
TARGETS = {
    "DRD2": {"pdb": "6vms_chainR_drd2.pdb", "chain": "R"},
    "IL1B": {"pdb": "4G6J_IL1B.pdb", "chain": None},  # Use first chain
    # Already done: Nav1.8, TRPA1, NRF2, MOR, TLR4, IL-6
}

# Amino acid mapping
D3TO1 = {
    'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
    'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
    'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
    'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'
}

def extract_sequence(pdb_path, chain_id=None):
    """Extract amino acid sequence from a PDB file."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("struct", pdb_path)
    seq = ""
    for model in structure:
        for chain in model:
            if chain_id and chain.id != chain_id:
                continue
            for residue in chain:
                resname = residue.get_resname()
                if resname in D3TO1:
                    seq += D3TO1[resname]
            if chain_id:
                break
        break
    return seq

def generate_embedding(seq, name, model, batch_converter, device):
    """Generate per-residue embeddings for a sequence."""
    data = [(name, seq)]
    batch_labels, batch_strs, batch_tokens = batch_converter(data)
    batch_tokens = batch_tokens.to(device)

    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[30], return_contacts=False)

    token_representations = results["representations"][30][0, 1:-1, :]
    return token_representations

def main():
    print(f"Loading ESM2 model: {MODEL_NAME}...")
    # Cargar modelo usando la función específica de fair-esm
    model, alphabet = esm.pretrained.esm2_t30_150M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    print(f"Model loaded on device: {device}")

    for target, info in TARGETS.items():
        pdb_file = PDB_DIR / info["pdb"]
        chain = info.get("chain")

        print(f"\nProcessing {target}: {pdb_file.name} (chain={chain})")

        if not pdb_file.exists():
            print(f"  WARNING: PDB not found, skipping {target}")
            continue

        try:
            seq = extract_sequence(pdb_file, chain)
            print(f"  Sequence length: {len(seq)}")

            if len(seq) == 0:
                print(f"  ERROR: Empty sequence extracted, skipping {target}")
                continue

            emb = generate_embedding(seq, target, model, batch_converter, device)
            out_path = OUT_DIR / f"{target}_esm2_per_residue.pt"
            torch.save(emb.cpu(), out_path)
            print(f"  Saved embeddings: {emb.shape} → {out_path}")

        except Exception as e:
            print(f"  ERROR processing {target}: {e}")

    print("\nDone.")

if __name__ == "__main__":
    main()