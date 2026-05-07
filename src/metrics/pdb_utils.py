
import numpy as np

def extract_iron_network_v4(pdb_path):
    """Extracted iron (FE) atoms from Heme (HEC) groups with Chain and B-factor info."""
    irons = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("HETATM") and "FE" in line[12:16] and "HEC" in line[17:20]:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                b_factor = float(line[60:66])
                chain = line[21]
                pos = [x, y, z, b_factor, ord(chain)]
                irons.append(pos)
    return np.array(irons)

def generate_null_model(n_points, box_size=50):
    """Generates a random cloud of points (Poisson process) as a Null Hypothesis."""
    return np.random.uniform(0, box_size, (n_points, 3))
