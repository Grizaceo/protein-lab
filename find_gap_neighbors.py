
import numpy as np
import sys

def find_gap_residues(pdb_path, pos1, pos2, radius=10.0):
    midpoint = (pos1 + pos2) / 2
    residues = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and "CA" in line[12:16]:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                pos = np.array([x, y, z])
                dist = np.linalg.norm(pos - midpoint)
                if dist < radius:
                    res_name = line[17:20].strip()
                    res_num = int(line[22:26])
                    chain = line[21]
                    residues.append({'name': res_name, 'num': res_num, 'chain': chain, 'dist': dist})
    
    return sorted(residues, key=lambda x: x['dist'])

if __name__ == "__main__":
    # Positions extracted from previous run for Heme 910A and 805C
    # I need to get their actual coordinates first
    import numpy as np
    
    def get_coords(path, chain, res):
        with open(path, 'r') as f:
            for line in f:
                if line.startswith("HETATM") and "FE" in line[12:16] and line[21] == chain and int(line[22:26]) == res:
                     return np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
        return None

    path = sys.argv[1]
    p1 = get_coords(path, 'A', 910)
    p2 = get_coords(path, 'C', 805)
    
    print(f"Gap midpoint neighbors in {path}:")
    neighbors = find_gap_residues(path, p1, p2)
    for n in neighbors[:10]:
        print(f"Residue {n['name']} {n['num']} (Chain {n['chain']}) - Distance to midpoint: {n['dist']:.2f}A")
