
import numpy as np
import sys

def extract_irons(pdb_path):
    irons = []
    with open(pdb_path, 'r') as f:
        for line in f:
            # Look for Iron in Heme C
            if line.startswith("HETATM") and "FE" in line[12:16] and "HEC" in line[17:20]:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                chain = line[21]
                res_num = int(line[22:26])
                irons.append({'pos': np.array([x, y, z]), 'chain': chain, 'res': res_num})
    return irons

def analyze_redundancy(irons):
    chain_a = [i for i in irons if i['chain'] == 'A']
    chain_c = [i for i in irons if i['chain'] == 'C']
    
    print(f"Irons in Chain A: {len(chain_a)}")
    print(f"Irons in Chain C: {len(chain_c)}")
    
    min_dist = float('inf')
    best_pair = None
    
    for i in chain_a:
        for j in chain_c:
            dist = np.linalg.norm(i['pos'] - j['pos'])
            if dist < min_dist:
                min_dist = dist
                best_pair = (i, j)
    
    print(f"\nMinimum distance between Chain A and Chain C: {min_dist:.2f} Angstroms")
    if best_pair:
        print(f"Best Bridge point: Heme {best_pair[0]['res']} (A) <-> Heme {best_pair[1]['res']} (C)")

if __name__ == "__main__":
    path = sys.argv[1]
    irons = extract_irons(path)
    analyze_redundancy(irons)
