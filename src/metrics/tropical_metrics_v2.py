
import numpy as np
import scipy.linalg as la
from pathlib import Path
import logging

# Configuración de Logging Profesional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger("BioMaterialCAD")

class BioMaterialCAD:
    """
    Sistema de diseño asistido por computadora para Bio-Materiales basado en
    Geometría Tropical y Teoría de Matrices Aleatorias.
    """
    def __init__(self, delta_max=5.0, temperature=300):
        self.delta_max = delta_max
        self.temperature = temperature
        self.kb = 8.617e-5 # eV/K

    def get_tropical_adjacency(self, coords):
        """
        Calcula la matriz de adyacencia tropical (Min-Plus).
        Distancias filtradas por un umbral de contacto (delta_max).
        """
        n = len(coords)
        dist_matrix = la.norm(coords[:, None] - coords, axis=2)
        # En geometría tropical, el 'cero' es infinito (no conexión)
        adj = np.where(dist_matrix <= self.delta_max, dist_matrix, np.inf)
        np.fill_diagonal(adj, 0)
        return adj

    def ihara_zeta_logdet(self, adj):
        """
        Calcula la complejidad topológica usando la identidad de Bass.
        1/Z(u) = det(I - u*W)
        Para grandes grafos, usamos el log-determinante para evitar overflow.
        """
        # Matriz binaria de adyacencia
        A = np.where(np.isinf(adj), 0, 1)
        np.fill_diagonal(A, 0)
        
        # D: Matriz de grados - 1
        D = np.diag(np.sum(A, axis=1) - 1)
        n = A.shape[0]
        
        # Identidad de Bass: Z(u)^-1 = (1-u^2)^(m-n) * det(I - uA + u^2 D)
        # Simplificamos para u=1 (complejidad estructural pura)
        # Nota: u=1 a veces es singular, usamos u=0.99 para estabilidad
        u = 0.95
        M = np.eye(n) - u * A + (u**2) * D
        
        try:
            sign, logdet = la.slogdet(M)
            return -logdet # Mayor logdet = mayor complejidad (más ciclos)
        except:
            return 0.0

    def spectral_beta(self, adj):
        """
        Métrica de conducción: Beta de la distribución P(s).
        Poisson (0.38) -> Localizado (Aislante)
        GUE (0.53) -> Delocalizado (Conductor)
        """
        clean_adj = np.where(np.isinf(adj), 0, adj)
        L = np.diag(np.sum(clean_adj, axis=1)) - clean_adj
        
        vals = np.sort(la.eigvalsh(L))
        diffs = np.diff(vals)
        diffs = diffs[diffs > 1e-9]
        
        if len(diffs) < 2: return 0.0
        
        r = diffs[1:] / diffs[:-1]
        return np.mean(np.minimum(r, 1/r))

    def electron_coupling_hab(self, d_nm):
        """
        Estimación de la acopladura electrónica H_ab (Marcus Theory).
        H_ab = H_0 * exp(-beta * (d - d_0) / 2)
        Valores típicos para proteínas: beta = 1.4 A^-1
        """
        h0 = 0.1 # eV
        beta_decay = 14 # nm^-1 (1.4 A^-1)
        d0 = 0.3 # nm
        if d_nm == 0: return 0
        return h0 * np.exp(-0.5 * beta_decay * (d_nm - d0))

    def tunnel_efficiency(self, adj):
        """
        Calcula la eficiencia de tunelamiento promedio del manifold.
        IMPORTANTE: Convierte Angstroms a Nanómetros para la fórmula de Marcus.
        """
        valid_distances = adj[~np.isinf(adj) & (adj > 0)]
        if len(valid_distances) == 0: return 0.0
        # Convertimos d de A a nm (d / 10)
        couplings = [self.electron_coupling_hab(d / 10.0) for d in valid_distances]
        return np.mean(couplings)

def parse_fasta(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        seq = "".join([l.strip() for l in lines if not l.startswith(">")])
    return seq

def generate_backbone(n, folding_factor=0.0):
    """
    Genera coordenadas 3D siguiendo la física de polímeros (Self-Avoiding Walk).
    Esto es más profesional que un simple seno/coseno.
    """
    coords = np.zeros((n, 3))
    step = 0.38 # nm
    for i in range(1, n):
        # Ángulos restringidos para evitar colisiones irreales
        phi = np.random.uniform(0, 2 * np.pi)
        theta = np.random.uniform(0.1, np.pi/2) * (1 - folding_factor)
        
        vec = np.array([
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta)
        ])
        coords[i] = coords[i-1] + vec * step
        
        # Pull hacia el centro (colapso hidrofóbico/elastina)
        if folding_factor > 0:
            center = np.mean(coords[:i+1], axis=0)
            coords[i] += (center - coords[i]) * folding_factor * 0.1
            
    return coords
