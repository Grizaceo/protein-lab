#!/usr/bin/env python3
"""
Pocket extraction and analysis pipeline for fibromyalgia targets.
Processes PDB structures to identify binding pockets, compute properties,
and generate comparative druggability table.

Requirements:
- biopython
- scipy
- numpy
- torch
- fair-esm
- pandas

Author: DAVI (Cristóbal)
Date: 2026-05-18
"""

import os
import argparse
import json
import numpy as np
from Bio import PDB
from scipy.spatial import ConvexHull
import torch
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# Check GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Using device: {device}")

# Mapping three-letter to one-letter for standard amino acids
THREE_TO_ONE = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}

# Hydrophobic amino acids (Kyte-Doolittle inspired, hydrophobic if index >= 1.0)
HYDROPHOBIC = set(['I', 'V', 'L', 'F', 'C', 'M', 'A'])

# ========================
# ESM2 embedding functions
# ========================

def load_esm2_model(model_name="esm2_t33_650M_UR50D"):
    """Load ESM2 model and alphabet."""
    import esm
    model, alphabet = getattr(esm.pretrained, model_name)()
    model = model.to(device).eval()
    return model, alphabet

def get_per_residue_embedding(sequence, model, alphabet, batch_converter, max_len=1022, stride=None):
    """
    Generate per-residue embeddings for a protein sequence using ESM2.
    Handles sequences longer than max_len via sliding window.
    Returns: numpy array of shape (L, embedding_dim)
    """
    if len(sequence) <= max_len:
        data = [("protein", sequence)]
        _, _, tokens = batch_converter(data)
        tokens = tokens.to(device)
        with torch.no_grad():
            results = model(tokens, repr_layers=[model.num_layers], return_contacts=False)
        # Extract per-residue representations (skip start/end tokens)
        emb = results["representations"][model.num_layers][0, 1:len(sequence)+1].cpu().numpy()
        return emb
    else:
        # Sliding window
        L = len(sequence)
        emb_dim = model.num_attention_heads * model.num_layers  # Actually embedding_dim = 1280
        # But we get model.embed_dim
        emb_dim = model.embed_dim
        sum_emb = np.zeros((L, emb_dim), dtype=np.float32)
        count = np.zeros(L, dtype=np.int32)
        if stride is None:
            stride = max_len // 2
        for start in range(0, L - max_len + 1, stride):
            end = start + max_len
            subseq = sequence[start:end]
            data = [("protein", subseq)]
            _, _, tokens = batch_converter(data)
            tokens = tokens.to(device)
            with torch.no_grad():
                results = model(tokens, repr_layers=[model.num_layers], return_contacts=False)
            sub_emb = results["representations"][model.num_layers][0, 1:len(subseq)+1].cpu().numpy()
            sum_emb[start:end] += sub_emb
            count[start:end] += 1
        # Handle tail
        if L > max_len and (L - max_len) % stride != 0:
            start = L - max_len
            subseq = sequence[start:]
            data = [("protein", subseq)]
            _, _, tokens = batch_converter(data)
            tokens = tokens.to(device)
            with torch.no_grad():
                results = model(tokens, repr_layers=[model.num_layers], return_contacts=False)
            sub_emb = results["representations"][model.num_layers][0, 1:len(subseq)+1].cpu().numpy()
            sum_emb[start:] += sub_emb
            count[start:] += 1
        # Average
        mask = count > 0
        sum_emb[mask] /= count[mask][:, None]
        return sum_emb

# ========================
# PDB processing functions
# ========================

def collect_protein_atoms(chain):
    """Collect all non-water atoms from a chain (protein backbone + sidechains)."""
    atoms = []
    for residue in chain.get_residues():
        # Skip water and HET atoms (we only want protein)
        rid = residue.get_id()
        if rid[0] != ' ':
            continue
        for atom in residue.get_atoms():
            atoms.append(atom)
    return atoms

def collect_het_atoms(chain, exclude_water=True):
    """Collect HET atoms (non-water) from a chain."""
    atoms = []
    for residue in chain.get_residues():
        rid = residue.get_id()
        if not rid[0].startswith('H'):
            continue
        if exclude_water and residue.get_resname() == 'HOH':
            continue
        for atom in residue.get_atoms():
            atoms.append(atom)
    return atoms

def find_target_chains(structure):
    """
    Identify target chains as those with the most protein residues.
    Returns list of chain IDs.
    """
    chain_protein_counts = {}
    for model in structure:
        for chain in model:
            count = sum(1 for r in chain.get_residues() if r.get_id()[0]==' ')
            chain_protein_counts[chain.id] = count
    if not chain_protein_counts:
        return []
    max_count = max(chain_protein_counts.values())
    # Return all chains with count >= 0.9*max_count (to catch similar multi-subunit complexes)
    target_chains = [cid for cid, cnt in chain_protein_counts.items() if cnt >= 0.9*max_count]
    return target_chains

def find_best_protein_partner(structure, target_chain_ids, max_contact_dist=5.0):
    """
    Find a protein chain (not in target_chain_ids) that is closest to any target chain.
    Used when no HET ligand is found; extracts protein-protein interface.
    Returns: (best_chain_id, list_of_atoms) or (None, None)
    """
    # Gather all protein atoms from target chains
    target_protein_atoms = []
    for cid in target_chain_ids:
        chain = structure[0][cid]
        target_protein_atoms.extend(collect_protein_atoms(chain))
    if not target_protein_atoms:
        return None, None
    best_chain = None
    best_min_dist = float('inf')
    best_atoms = None
    for model in structure:
        for chain in model:
            cid = chain.id
            if cid in target_chain_ids:
                continue
            # Check if this chain has any protein residues
            prot_atoms = collect_protein_atoms(chain)
            if not prot_atoms:
                continue
            # Compute minimal distance between any atom in this chain and any target atom
            min_dist = float('inf')
            for pa in prot_atoms:
                pa_coord = pa.get_coord()
                for ta in target_protein_atoms:
                    d = np.linalg.norm(pa_coord - ta.get_coord())
                    if d < min_dist:
                        min_dist = d
                        if min_dist <= max_contact_dist:
                            break  # good enough
            if min_dist < best_min_dist:
                best_min_dist = min_dist
                best_chain = cid
                best_atoms = prot_atoms
    if best_chain is None or best_min_dist > max_contact_dist:
        return None, None
    return best_chain, best_atoms

def find_best_ligand(structure, target_chain_ids, max_contact_dist=5.0):
    """
    Find the HET ligand (group of HET residues) that has the most atomic contacts
    with any of the target chains.
    Returns: (ligand_atoms, ligand_residue) or (None, None)
    """
    # Gather protein atoms from target chains
    protein_atoms = []
    for cid in target_chain_ids:
        chain = structure[0][cid]
        protein_atoms.extend(collect_protein_atoms(chain))
    if not protein_atoms:
        return None, None
    # Gather all HET atoms (non-water) from all chains, grouped by residue
    het_residues = {}  # (chain_id, resname, resseq, icode) -> list of atoms
    for model in structure:
        for chain in model:
            for residue in chain.get_residues():
                rid = residue.get_id()
                if not rid[0].startswith('H'):
                    continue
                if residue.get_resname() == 'HOH':
                    continue
                key = (chain.id, residue.get_resname(), residue.get_id()[1], residue.get_id()[2])
                if key not in het_residues:
                    het_residues[key] = []
                het_residues[key].extend(residue.get_atoms())
    if not het_residues:
        return None, None
    # For each HET residue group, count how many protein atoms are within max_contact_dist
    best_key = None
    best_contact_count = -1
    best_min_dist = float('inf')
    for key, hatoms in het_residues.items():
        # Build KDTree or just compute distances (small numbers)
        counts = 0
        min_dist = float('inf')
        for ha in hatoms:
            ha_coord = ha.get_coord()
            for pa in protein_atoms:
                d = np.linalg.norm(ha_coord - pa.get_coord())
                if d <= max_contact_dist:
                    counts += 1
                if d < min_dist:
                    min_dist = d
        # We want the ligand with most contacts; tie-breaker: smallest min distance
        if counts > best_contact_count or (counts == best_contact_count and min_dist < best_min_dist):
            best_contact_count = counts
            best_min_dist = min_dist
            best_key = key
    if best_key is None or best_contact_count == 0:
        return None, None
    # Return all atoms of that residue(s) as ligand
    ligand_atoms = het_residues[best_key]
    # Also return the residue identifier
    ligand_residue = best_key
    return ligand_atoms, ligand_residue

def get_pocket_residues(structure, target_chain_ids, ligand_atoms, max_dist=5.0):
    """
    For each target chain, find protein residues with any atom within max_dist of any ligand atom.
    Returns: list of Residue objects (from the target chains).
    """
    ligand_coords = np.array([a.get_coord() for a in ligand_atoms])
    pocket_residues = []
    for cid in target_chain_ids:
        chain = structure[0][cid]
        for residue in chain.get_residues():
            rid = residue.get_id()
            if rid[0] != ' ':
                continue
            # Check if any atom in this residue is within max_dist
            for atom in residue.get_atoms():
                coord = atom.get_coord()
                if np.any(np.linalg.norm(ligand_coords - coord, axis=1) <= max_dist):
                    pocket_residues.append(residue)
                    break
    return pocket_residues

def compute_convex_hull_volume(pocket_residues):
    """Compute convex hull volume (Å^3) of all atoms in pocket residues."""
    coords = []
    for res in pocket_residues:
        for atom in res.get_atoms():
            coords.append(atom.get_coord())
    if len(coords) < 4:
        return 0.0
    points = np.array(coords)
    hull = ConvexHull(points)
    return hull.volume

def compute_composition(pocket_residues):
    """
    Compute hydrophobic vs polar composition in pocket residues.
    Returns: (hydrophobic_count, polar_count, total)
    """
    counts = {'hydro':0, 'polar':0}
    for res in pocket_residues:
        resname = res.get_resname()
        oneletter = THREE_TO_ONE.get(resname, 'X')  # default to 'X' for non-standard
        if oneletter in HYDROPHOBIC:
            counts['hydro'] += 1
        else:
            counts['polar'] += 1
    total = len(pocket_residues)
    return counts['hydro'], counts['polar'], total

def get_sequence_from_chain(chain):
    """Get amino acid sequence (one-letter) from a protein chain."""
    from Bio.PDB import Polypeptide
    seq = []
    for residue in chain.get_residues():
        rid = residue.get_id()
        if rid[0] != ' ':
            continue
        try:
            aa = Polypeptide.three_to_one(residue.get_resname())
            seq.append(aa)
        except Exception:
            # Unknown or non-standard, skip or use X
            seq.append('X')
    return ''.join(seq)

# ========================
# Main processing
# ========================

def process_target(target_name, pdb_path, model, alphabet, batch_converter):
    """
    Process a single target PDB: identify ligand, extract pocket, compute properties.
    Returns dict with results.
    """
    print(f"[INFO] Processing {target_name} from {pdb_path}")
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure(target_name, pdb_path)

    # Identify target chains
    target_chain_ids = find_target_chains(structure)
    if not target_chain_ids:
        print(f"[WARN] No target chains identified in {pdb_path}")
        return None
    print(f"  Target chains: {target_chain_ids}")

    # Find best ligand (HET) that touches target chains
    ligand_atoms, ligand_residue = find_best_ligand(structure, target_chain_ids, max_contact_dist=5.0)
    ligand_type = 'small_molecule'
    if ligand_atoms is None:
        # Try to find protein partner interface (heterodimeric complex)
        partner_chain, partner_atoms = find_best_protein_partner(structure, target_chain_ids, max_contact_dist=5.0)
        if partner_chain is not None:
            ligand_atoms = partner_atoms
            ligand_residue = (partner_chain, 'PROTEIN_PARTNER', None, None)
            ligand_type = 'protein_interface'
        else:
            print(f"[WARN] No suitable ligand or protein partner found in {pdb_path}")
            # Return placeholder with no ligand
            return {
                'target': target_name,
                'pdb': os.path.basename(pdb_path),
                'ligand_chain': None,
                'ligand_resname': None,
                'ligand_resseq': None,
                'n_residues': 0,
                'n_hydrophobic': 0,
                'n_polar': 0,
                'hydrophobic_fraction': 0.0,
                'volume': 0.0,
                'pocket_embedding': None,
                'embedding_dim': 0,
                'has_ligand': False,
                'ligand_type': 'none'
            }
    ligand_chain, lig_resname, lig_seq, lig_icode = ligand_residue
    print(f"  Ligand: chain {ligand_chain}, resname {lig_resname}, seq {lig_seq}, type: {ligand_type}")

    # Get pocket residues (protein residues within 5Å of ligand)
    pocket_residues = get_pocket_residues(structure, target_chain_ids, ligand_atoms, max_dist=5.0)
    if not pocket_residues:
        print(f"[WARN] No pocket residues found")
        return None
    print(f"  Pocket residues count: {len(pocket_residues)}")

    # Compute volume (convex hull)
    volume = compute_convex_hull_volume(pocket_residues)

    # Compute composition
    n_hydro, n_polar, total = compute_composition(pocket_residues)
    hydro_frac = n_hydro / total if total > 0 else 0.0

    # Embedding per residue
    # Need full sequences of each target chain, then collect embeddings for the residues in pocket
    # We'll generate per-residue embeddings for each chain and map by residue number (resseq)
    chain_embeddings = {}
    for cid in target_chain_ids:
        chain = structure[0][cid]
        seq = get_sequence_from_chain(chain)
        if not seq:
            print(f"[WARN] Chain {cid} has no protein sequence")
            continue
        print(f"  Chain {cid} sequence length: {len(seq)}")
        emb = get_per_residue_embedding(seq, model, alphabet, batch_converter, max_len=1022, stride=512)
        # Align emb with residues: need to map index in seq to residue object
        # We'll create a mapping: for each residue with (resseq, icode) -> index in seq
        res_to_index = {}
        idx = 0
        for res in chain.get_residues():
            rid = res.get_id()
            if rid[0] != ' ':
                continue
            # Skip non-standard amino acids that we mapped to 'X' - still store index
            res_to_index[(rid[1], rid[2])] = idx
            idx += 1
        chain_embeddings[cid] = (emb, res_to_index)
        if emb.shape[0] != len(seq):
            print(f"[WARN] Embedding length mismatch: {emb.shape[0]} vs {len(seq)} for chain {cid}")

    # Collect embeddings for pocket residues
    pocket_embs = []
    for res in pocket_residues:
        cid = res.get_parent().id
        if cid not in chain_embeddings:
            continue
        emb, res_to_index = chain_embeddings[cid]
        key = (res.get_id()[1], res.get_id()[2])
        if key not in res_to_index:
            # Possibly non-standard residue not in seq mapping
            continue
        seq_idx = res_to_index[key]
        if seq_idx < emb.shape[0]:
            pocket_embs.append(emb[seq_idx])
    if not pocket_embs:
        print(f"[WARN] No embedding vectors extracted for pocket residues")
        pocket_embedding = None
    else:
        pocket_embedding = np.mean(pocket_embs, axis=0).tolist()  # convert to list for JSON

    # Additional properties: number of residues, fraction hydrophobic, volume
    results = {
        'target': target_name,
        'pdb': os.path.basename(pdb_path),
        'ligand_chain': ligand_chain,
        'ligand_resname': lig_resname,
        'ligand_resseq': lig_seq,
        'n_residues': total,
        'n_hydrophobic': n_hydro,
        'n_polar': n_polar,
        'hydrophobic_fraction': hydro_frac,
        'volume': float(volume),
        'pocket_embedding': pocket_embedding,
        'embedding_dim': len(pocket_embedding) if pocket_embedding else 0
    }
    return results

# ========================
# Configuration
# ========================

def get_targets_config(base_dir):
    """
    Define which PDB to use for each target based on availability.
    This is a manual selection; adjust as needed.
    """
    # Mapping: target -> PDB filename (relative to datos/pdb/)
    config = {
        'DRD2': '6vms_chainR_drd2.pdb',
        'Nav1.8': '7WFW_Nav1.8.pdb',  # o 7WE4? vamos a usar 7WFW
        'NRF2': '6LRZ_NRF2.pdb',
        'TRPA1': '6PQQ_TRPA1.pdb',
        'MOR': '8EF6_chainR_MOR.pdb',  # puede no tener ligando; intentar
        'TLR4': '4G8A_TLR4.pdb',
        'IL6': '5FUC_IL6.pdb',
        'IL1B': '2NVH_IL1B.pdb'
    }
    # Absolute paths
    pdb_dir = os.path.join(base_dir, 'datos', 'pdb')
    targets = []
    for name, fname in config.items():
        path = os.path.join(pdb_dir, fname)
        if os.path.exists(path):
            targets.append((name, path))
        else:
            print(f"[WARN] PDB not found for {name}: {path}")
    return targets

# ========================
# Main
# ========================

def main():
    import pathlib
    base_dir = str(pathlib.Path(__file__).resolve().parent.parent)
    output_dir = os.path.join(base_dir, 'analisis', 'pockets')
    os.makedirs(output_dir, exist_ok=True)
    report_dir = os.path.join(base_dir, 'reportes')
    os.makedirs(report_dir, exist_ok=True)

    # Load ESM2 model once
    print("[INFO] Loading ESM2 model...")
    model, alphabet = load_esm2_model()
    batch_converter = alphabet.get_batch_converter()
    print("[INFO] Model loaded.")

    # Get targets list
    targets = get_targets_config(base_dir)
    print(f"[INFO] Will process {len(targets)} targets: {[t[0] for t in targets]}")

    results = []
    for name, pdb_path in targets:
        try:
            res = process_target(name, pdb_path, model, alphabet, batch_converter)
            if res:
                results.append(res)
        except Exception as e:
            print(f"[ERROR] Failed processing {name}: {e}")
            import traceback
            traceback.print_exc()

    # Create table
    if not results:
        print("[ERROR] No results to report.")
        return

    # Normalize for druggability score
    df = pd.DataFrame(results)
    # Ensure columns exist
    for col in ['volume', 'hydrophobic_fraction', 'n_residues']:
        if col not in df.columns:
            df[col] = 0
    scaler = MinMaxScaler()
    df['volume_norm'] = scaler.fit_transform(df[['volume']])
    df['count_norm'] = scaler.fit_transform(df[['n_residues']])
    # hydro_fraction already 0-1
    df['druggability'] = (0.4*df['volume_norm'] + 0.4*df['hydrophobic_fraction'] + 0.2*df['count_norm']).round(3)

    # Save CSV
    csv_path = os.path.join(report_dir, 'pocket_druggability_table.csv')
    df.to_csv(csv_path, index=False)
    print(f"[INFO] Table saved to {csv_path}")

    # Save JSON with full details (including embeddings)
    json_path = os.path.join(output_dir, 'pockets_analysis_results.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"[INFO] Detailed results saved to {json_path}")

    # Generate markdown report
    md_path = os.path.join(report_dir, 'pocket_analysis_report.md')
    generate_report(df, md_path)
    print(f"[INFO] Markdown report saved to {md_path}")

    # Mark completion-ready
    completion_marker = os.path.join(base_dir, 'COMPLETION_READY_POCKETS.md')
    with open(completion_marker, 'w') as f:
        f.write(f"# Pocket analysis complete\n\nDate: 2026-05-18\n\nTargets processed: {len(results)}\n\nTable: {csv_path}\nReport: {md_path}\n")
    print(f"[INFO] Completion marker created at {completion_marker}")

def generate_report(df, out_path):
    with open(out_path, 'w') as f:
        f.write("# Pocket Analysis Report — Fibromyalgia Targets\n\n")
        f.write(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## Summary\n\n")
        f.write(f"Total targets analyzed: {len(df)}\n\n")
        f.write("## Comparative Druggability Table\n\n")
        # Write markdown table
        columns = ['target', 'pdb', 'ligand_resname', 'n_residues', 'volume', 'hydrophobic_fraction', 'druggability']
        f.write("| " + " | ".join(columns) + " |\n")
        f.write("|" + "---|" * len(columns) + "\n")
        for _, row in df.iterrows():
            vals = [str(row[col])[:5] if isinstance(row[col], float) else str(row[col]) for col in columns]
            f.write("| " + " | ".join(vals) + " |\n")
        f.write("\n## Notes\n\n")
        f.write("- Pocket residues: protein residues within 5Å of the co-crystallized ligand.\n")
        f.write("- Volume: convex hull volume (Å³) of pocket atoms.\n")
        f.write("- Hydrophobic fraction: fraction of residues classified as hydrophobic (A,V,L,I,P,F,W,M,C).\n")
        f.write("- Druggability score: composite (0-1) with 40% volume, 40% hydrophobicity, 20% residue count.\n")
        f.write("- Embeddings: per-residue ESM2-650M embeddings averaged over pocket residues (stored in JSON).\n")

if __name__ == "__main__":
    main()
