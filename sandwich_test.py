
import numpy as np
import sys
import os

# Import BioMaterialCAD logic
sys.path.append(os.path.expanduser("~/.hermes/workspace/protein-lab/src/metrics"))
from tropical_metrics_v2 import BioMaterialCAD

def run_sandwich_simulation():
    cad = BioMaterialCAD(delta_max=16.0) # Gap tolerable para tunelamiento asistido
    
    # 1. GENERAR CABLE ENTRADA (MtrA) - 10 Hemes lineales
    mtra_chain = np.zeros((10, 3))
    for i in range(10):
        mtra_chain[i] = [0, 0, i * 10.0] # 10A spacing
    
    # 2. GENERAR CORE PROCESADOR (Ferritina-Au) - Esfera de alta densidad
    # Ubicamos la Ferritina al final del MtrA (+15A de gap)
    offset = mtra_chain[-1] + [0, 0, 15.0]
    
    # Simulación de cluster de oro central + nube de hierro
    gold_cluster = []
    # 13 átomos de oro (Au13 cuboctahedron-like)
    for i in range(13):
        gold_cluster.append(offset + np.random.normal(0, 2.0, 3))
    gold_cluster = np.array(gold_cluster)
    
    # 3. GENERAR CABLE SALIDA (MtrF)
    # Sale de otro lado de la ferritina para forzar el paso por el core
    offset_out = offset + [15.0, 0, 15.0]
    mtrf_chain = np.zeros((5, 3))
    for i in range(5):
        mtrf_chain[i] = offset_out + [0, 0, i * 10.0]
        
    full_system = np.vstack([mtra_chain, gold_cluster, mtrf_chain])
    nodes_a = list(range(10))
    nodes_gold = list(range(10, 10+13))
    nodes_f = list(range(10+13, 10+13+5))
    
    print("--- 🥪 TEST DE FLUJO: SANDWICH FERRITINA-AU ---")
    
    def check_transmission(net, label):
        adj = cad.get_tropical_adjacency(net)
        # Caminos simples: ¿Hay conexión de Mtra[0] a Mtrf[last]?
        # Usamos potencias de la matriz de adyacencia (Tropical Matrix Multiplication)
        # Si (A^n)[start, end] < inf, hay camino.
        
        # Simplificación: Verificamos si el cluster de oro conecta los dos cables
        d_in = np.min([np.linalg.norm(mtra_chain[-1] - g) for g in gold_cluster])
        d_out = np.min([np.linalg.norm(mtrf_chain[0] - g) for g in gold_cluster])
        
        eff = cad.tunnel_efficiency(adj)
        
        print(f"[{label}]")
        print(f"Gap Input -> Gold:  {d_in:.2f} A")
        print(f"Gap Gold -> Output: {d_out:.2f} A")
        print(f"Eficiencia Global:  {eff:.6f} eV")
        
        if d_in < 16.0 and d_out < 16.0:
            print("ESTADO: TRANSMISIÓN EXITOSA (Core Redundante Activo)")
        else:
            print("ESTADO: FALLO DE CONEXIÓN (Alta Impedancia Interfacial)")

    check_transmission(full_system, "ESTADO INTEGRAL")
    
    # 4. TEST DE RESILIENCIA: Matamos el 50% de los nodos de ORO
    print("\n--- ☢️ ATAQUE AL CORE: 50% GOLD LOSS ---")
    kill_indices = nodes_gold[:len(nodes_gold)//2]
    damaged_system = np.delete(full_system, kill_indices, axis=0)
    
    # Re-evaluación rápida de distancias tras daño
    new_gold = np.delete(gold_cluster, range(len(gold_cluster)//2), axis=0)
    d_in_f = np.min([np.linalg.norm(mtra_chain[-1] - g) for g in new_gold])
    d_out_f = np.min([np.linalg.norm(mtrf_chain[0] - g) for g in new_gold])
    
    if d_in_f < 16.0 and d_out_f < 16.0:
         print(f"RESILIENCIA: OK. Gap final {max(d_in_f, d_out_f):.2f} A. El flujo persiste.")
    else:
         print("RESILIENCIA: FAILED. El core ha colapsado.")

if __name__ == "__main__":
    run_sandwich_simulation()
