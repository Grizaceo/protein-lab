
import sys
sys.path.append("/home/gris/.hermes/workspace/protein-lab")
from tropical_metrics import BioMaterialCAD, parse_fasta
from pathlib import Path

# Config
input_dir = Path("/home/gris/.hermes/workspace/protein-lab/exp01-hemoglobina/input")
cad = BioMaterialCAD(delta_max=6.0) # Increased to allow some mock connectivity

print(f"{'Structure':<10} | {'Length':<6} | {'Zeta Complexity':<15} | {'GUE Beta':<10} | {'Status'}")
print("-" * 65)

for fasta in ["MtrC.fasta", "MtrF.fasta"]:
    path = input_dir / fasta
    if path.exists():
        seq = parse_fasta(path)
        coords = cad.sequence_to_mock_coords(seq)
        adj = cad.get_tropical_adjacency(coords)
        zeta = cad.ihara_zeta_complexity(adj)
        beta = cad. gue_beta_stability(adj)
        
        regime = "CONDUCTOR" if beta > 0.5 else "INSULATOR"
        print(f"{fasta:<10} | {len(seq):<6} | {zeta:<15.4f} | {beta:<10.4f} | {regime}")
