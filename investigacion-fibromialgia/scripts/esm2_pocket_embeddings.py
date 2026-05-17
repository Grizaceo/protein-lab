import os
import torch
import esm
from Bio.PDB import PDBParser

base_dir = "/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia/datos/pdb"
drd2_pdb = os.path.join(base_dir, "6vms_chainR_drd2.pdb")
mor_pdb = os.path.join(base_dir, "5C1M_MOR.pdb") # Use 5C1M as MOR reference
out_dir = "/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia/analisis/esm2"

os.makedirs(out_dir, exist_ok=True)

def extract_sequence_from_pdb(pdb_file, chain_id=None):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("struct", pdb_file)
    seq = ""
    # Standard amino acids
    d3to1 = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
         'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
         'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
         'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
         
    for model in structure:
        for chain in model:
            if chain_id and chain.id != chain_id:
                continue
            for residue in chain:
                if residue.get_resname() in d3to1:
                    seq += d3to1[residue.get_resname()]
            if chain_id:
                break
        break
    return seq

print("1. Extracting sequences...")
drd2_seq = extract_sequence_from_pdb(drd2_pdb)
mor_seq = extract_sequence_from_pdb(mor_pdb) # 5C1M has MOR chain A

print(f"DRD2 length: {len(drd2_seq)}")
print(f"MOR length: {len(mor_seq)}")

print("2. Loading ESM2 (150M)...")
# 150M is safe for 8GB VRAM
model, alphabet = esm.pretrained.esm2_t30_150M_UR50D()
batch_converter = alphabet.get_batch_converter()
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

def get_embeddings(seq, name):
    data = [(name, seq)]
    batch_labels, batch_strs, batch_tokens = batch_converter(data)
    batch_tokens = batch_tokens.to(device)
    
    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[30], return_contacts=False)
    
    # Extract representation (excluding <s> and </s> tokens)
    token_representations = results["representations"][30][0, 1:-1, :]
    
    # Save to disk
    out_path = os.path.join(out_dir, f"{name}_esm2_per_residue.pt")
    torch.save(token_representations.cpu(), out_path)
    print(f"Saved {name} embeddings: {token_representations.shape} to {out_path}")
    return token_representations

print("3. Generating embeddings...")
drd2_emb = get_embeddings(drd2_seq, "DRD2")
mor_emb = get_embeddings(mor_seq, "MOR")

print("Done. Embeddings ready for pocket analysis.")
