"""
state_manager.py — Gestión del estado persistente del loop Lab ↔ Colab.

Responsabilidades:
- Cargar y guardar ITERATION_STATE.json
- Registrar nuevas corridas con sus métricas
- Calcular y actualizar composite_score
- Manejar stuck_count (detección de estancamiento)
"""

import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path

STATE_FILE = Path(__file__).parent.parent.parent / "colab_runs" / "ITERATION_STATE.json"

# Composite score = 0.4*pLDDT + 0.3*ipTM + 0.3*(1 - pAE/30)
# Si ipTM no disponible (binder-only run): composite = 0.5*pLDDT + 0.5*(1 - pAE/30)
EXPLOIT_THRESHOLD = 0.05   # mejora >5% → explotar
STUCK_THRESHOLD   = 2      # N iteraciones sin mejora → explorar


def compute_composite(mean_pLDDT, mean_ipTM, mean_pAE):
    """
    Calcula composite score priorizando ipTM (afinidad real).
    Si ipTM no está disponible, el score se penaliza masivamente para forzar la validación de complejo.
    """
    plddt = float(mean_pLDDT) if mean_pLDDT is not None else 0.0
    iptm  = float(mean_ipTM)  if mean_ipTM  is not None else 0.0
    pae   = float(mean_pAE)   if mean_pAE   is not None else 30.0

    pae_term = max(0.0, 1.0 - pae / 30.0)

    if mean_ipTM is None:
        # Penalización masiva: un run sin ipTM nunca superará a uno validado.
        score = 0.1 * plddt 
    else:
        # Nuevo balance: ipTM es el rey (70%), pLDDT (20%), pAE (10%)
        score = 0.7 * iptm + 0.2 * plddt + 0.1 * pae_term

    return round(min(1.0, max(0.0, score)), 4)


def load_state() -> dict:
    """Carga ITERATION_STATE.json. Retorna dict con el estado completo."""
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"State file not found: {STATE_FILE}")
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(state: dict) -> None:
    """Guarda el estado a disco, actualizando el timestamp."""
    state = deepcopy(state)
    state["_meta"]["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_target(state: dict, target_name: str) -> dict:
    """Retorna el sub-dict de un target (nipah o ferritin). KeyError si no existe."""
    if target_name not in state["targets"]:
        raise KeyError(f"Target '{target_name}' no encontrado en el estado. "
                       f"Disponibles: {list(state['targets'].keys())}")
    return state["targets"][target_name]


def register_run(state: dict, target_name: str, run_record: dict) -> dict:
    """
    Registra una nueva corrida en el estado y actualiza best_score / stuck_count.

    run_record debe tener:
      run_id, params, metrics (dict con mean_pLDDT, mean_ipTM, mean_pAE, n_designs),
      complex_scored (bool), notes (str)

    Retorna el state modificado (también modifica in-place).
    """
    target = get_target(state, target_name)

    # Calcular composite score
    m = run_record.get("metrics", {})
    score = compute_composite(
        m.get("mean_pLDDT"),
        m.get("mean_ipTM"),
        m.get("mean_pAE"),
    )
    run_record["composite_score"] = score
    run_record.setdefault("promoted", False)
    run_record.setdefault("target", target_name)

    # Determinar si mejoró
    prev_best = target.get("best_score", 0.0) or 0.0
    improvement = (score - prev_best) / max(prev_best, 1e-6)

    if score > prev_best:
        target["best_score"] = score
        target["best_run"] = run_record["run_id"]

    if improvement > EXPLOIT_THRESHOLD:
        target["stuck_count"] = 0
    else:
        target["stuck_count"] = target.get("stuck_count", 0) + 1

    # Añadir al historial
    target["runs"].append(run_record)
    target["param_history"].append(run_record.get("params", {}))
    target["iteration"] = target.get("iteration", 0) + 1

    return state


def get_strategy(target: dict) -> str:
    """
    Determina estrategia para la próxima iteración.
    Returns: 'exploit' | 'explore'
    """
    stuck = target.get("stuck_count", 0)
    iteration = target.get("iteration", 0)

    if stuck >= STUCK_THRESHOLD or (iteration > 0 and iteration % 4 == 0):
        return "explore"
    return "exploit"


def summary_table(state: dict) -> str:
    """Genera tabla de resumen markdown para todos los targets y runs."""
    lines = [
        "# Estado del Loop Lab ↔ Colab",
        f"Actualizado: {state['_meta']['updated']}",
        "",
    ]
    for tname, target in state["targets"].items():
        lines += [
            f"## {target['display_name']}",
            f"- Iteración: {target['iteration']}",
            f"- Mejor score: {target['best_score']:.4f} ({target['best_run'] or 'ninguno'})",
            f"- Stuck count: {target['stuck_count']}",
            f"- Estrategia próxima iteración: **{get_strategy(target).upper()}**",
            "",
            "| Run | pLDDT | ipTM | pAE | Score | Complejo | Notas |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for run in target["runs"]:
            m = run.get("metrics", {})
            plddt = f"{m.get('mean_pLDDT', '?'):.3f}" if isinstance(m.get('mean_pLDDT'), float) else "?"
            iptm  = f"{m.get('mean_ipTM', '?'):.3f}"  if isinstance(m.get('mean_ipTM'), float) else "N/A"
            pae   = f"{m.get('mean_pAE', '?'):.1f}"   if isinstance(m.get('mean_pAE'), float) else "?"
            score = f"{run.get('composite_score', '?'):.4f}" if isinstance(run.get('composite_score'), float) else "?"
            compl = "✓" if run.get("complex_scored") else "—"
            notes = (run.get("notes") or "")[:60]
            lines.append(f"| {run['run_id']} | {plddt} | {iptm} | {pae} | {score} | {compl} | {notes} |")

        if not target["runs"]:
            lines.append("| (sin runs) | — | — | — | — | — | — |")
        lines.append("")

    return "\n".join(lines)
