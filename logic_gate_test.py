
import numpy as np
import sys
import os

# Import BioMaterialCAD logic
sys.path.append(os.path.expanduser("~/.hermes/workspace/protein-lab/src/metrics"))
from tropical_metrics_v2 import BioMaterialCAD

def run_logic_gate_simulation():
    cad = BioMaterialCAD(delta_max=16.0)
    
    # 1. EL PROCESADOR (Ferritina-Au)
    # Centro de la esfera en (0,0,0)
    gold_cluster = []
    for i in range(55): # Au55 
        gold_cluster.append(np.random.normal(0, 3.0, 3))
    gold_cluster = np.array(gold_cluster)
    
    # 2. ENTRADAS (2 Cables MtrA)
    # Entrada A: desde la izquierda (-25, 0, 0)
    input_A = np.array([-25, 0, 0])
    # Entrada B: desde arriba (0, 25, 0)
    input_B = np.array([0, 25, 0])
    
    # 3. SALIDA (1 Cable MtrF)
    # Salida: hacia la derecha (25, 0, 0)
    output_Y = np.array([25, 0, 0])

    print("--- 🖥️ SIMULACIÓN DE PUERTA LÓGICA BIO-HÍBRIDA ---")
    print("Arquitectura: Ferritina como concentrador de señales (Sumador Tropical)")
    
    def get_signal_strength(active_inputs):
        # Unificamos puntos activos
        current_net = list(gold_cluster) + [output_Y]
        for inp in active_inputs:
            current_net.append(inp)
        current_net = np.array(current_net)
        
        # Calculamos la eficiencia de tunelamiento hacia la salida
        # En términos simples: ¿Cuál es el camino más corto que conecta las entradas activas con Y?
        dists_to_gold = [np.linalg.norm(inp - gold_cluster, axis=1).min() for inp in active_inputs]
        dist_to_output = np.linalg.norm(gold_cluster - output_Y, axis=1).min()
        
        # La señal es proporcional a la cercanía (Marcus Theory)
        if not active_inputs: return 0.0
        
        # Promedio de facilidad de entrada + facilidad de salida
        avg_input_gap = np.mean(dists_to_gold)
        total_gap = avg_input_gap + dist_to_output
        
        # Umbral arbitrario para "Señal ON" (ej. Gap total < 32A)
        return total_gap

    # Escenarios
    scenarios = [
        {"name": "0 0 (Sin señal)", "inputs": []},
        {"name": "1 0 (Solo A)  ", "inputs": [input_A]},
        {"name": "0 1 (Solo B)  ", "inputs": [input_B]},
        {"name": "1 1 (A y B)   ", "inputs": [input_A, input_B]}
    ]

    print(f"{'ESCENARIO':<20} | {'GAP TOTAL':<10} | {'RESULTADO'}")
    print("-" * 50)
    
    results = []
    for s in scenarios:
        gap = get_signal_strength(s['inputs'])
        # A menor gap, mayor señal.
        res = "OFF (Basal)"
        if 0 < gap < 28: # Ajustamos umbral de detección
            res = "ON (High)"
        elif gap > 0:
            res = "LOW (Leakage)"
            
        print(f"{s['name']:<20} | {gap:<10.2f} | {res}")
        results.append(gap)

    print("\n--- 🧠 DIAGNÓSTICO DE LA PUERTA ---")
    if results[3] < results[1] and results[3] < results[2]:
        print("COMPORTAMIENTO: PUERTA 'AND' (Sumadora)")
        print("La presión electrónica de dos entradas reduce la impedancia del core.")
    else:
        print("COMPORTAMIENTO: PUERTA 'OR' / SUMADOR")
        print("El núcleo de oro es tan eficiente que basta con una entrada para activar la salida.")

if __name__ == "__main__":
    run_logic_gate_simulation()
