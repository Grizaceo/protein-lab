
import numpy as np

class BioMaterialCAD:
    def __init__(self, delta_max=4.0, e_max=1.0):
        self.delta_max = delta_max
        self.e_max = e_max

    def sequence_to_mock_coords(self, sequence, folding=0.0):
        # folding=0.0 es una cadena lineal (Poisson)
        # folding=1.0 es un glóbulo colapsado (GUE)
        n = len(sequence)
        coords = np.zeros((n, 3))
        
        # Base: Cadena semi-lineal
        for i in range(1, n):
            coords[i] = coords[i-1] + np.array([0.38, 0, 0])
            
        if folding > 0:
            # Simulamos el colapso hacia el centro
            center = np.mean(coords, axis=0)
            for i in range(n):
                # Desplazamos los puntos hacia el centro proporcional al factor de folding
                # y añadimos ruido para crear contactos no locales
                pull = (center - coords[i]) * folding
                noise = np.random.normal(0, 0.1 * folding, 3)
                coords[i] += pull + noise
                
        return coords

    def get_tropical_adjacency(self, coords):
        n = len(coords)
        adj = np.full((n, n), np.inf)
        for i in range(n):
            for j in range(i + 1, n):
                dist = np.linalg.norm(coords[i] - coords[j])
                if dist <= self.delta_max:
                    adj[i, j] = adj[j, i] = dist
        np.fill_diagonal(adj, 0)
        return adj

    def ihara_zeta_complexity(self, adj, k_truncate=8):
        # Topological complexity (Loops/Redundancy)
        current_adj = np.where(np.isinf(adj), 0, 1)
        n = adj.shape[0]
        paths = np.eye(n)
        zeta_sum = 0
        for k in range(1, k_truncate + 1):
            paths = np.dot(paths, current_adj)
            zeta_sum += np.trace(paths) / k
        return np.exp(zeta_sum)

    def gue_beta_stability(self, adj):
        # Conduction regime: ~0.38 (Poisson/Insulator), ~0.53 (GUE/Conductor)
        clean_adj = np.where(np.isinf(adj), 0, adj)
        degree_matrix = np.diag(np.sum(clean_adj, axis=1))
        laplacian = degree_matrix - clean_adj
        eigenvalues = np.sort(np.linalg.eigvalsh(laplacian))
        diffs = np.diff(eigenvalues)
        diffs = diffs[diffs > 1e-7]
        if len(diffs) < 2: return 0
        r_n = diffs[1:] / diffs[:-1]
        return np.mean(np.minimum(r_n, 1/r_n))

def parse_fasta(path):
    with open(path, 'r') as f:
        return "".join([line.strip() for line in f if not line.startswith(">")])
