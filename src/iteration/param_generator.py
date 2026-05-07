"""
param_generator.py — Generador adaptativo de parámetros para la próxima corrida Colab.

Estrategia:
  - EXPLOIT: Si la última corrida mejoró >5% el composite score, perturba
             ±1 paso alrededor de los mejores parámetros conocidos.
  - EXPLORE: Si stuck_count >= 2 o iteration % 4 == 0, salta a una región
             no explorada del espacio de parámetros.

Anti-repetición: nunca devuelve una combinación ya presente en param_history.
"""

import random
from copy import deepcopy
from itertools import product


# ══════════════════════════════════════════════════════════════════════════════
# Espacios de parámetros por target
# ══════════════════════════════════════════════════════════════════════════════

PARAM_SPACES = {
    "nipah": {
        "contigs": ["70-90", "90-90", "90-110", "70-110", "100-100", "80-100"],
        "hotspot_variant": ["focal", "broad", "mixed"],
        "hotspot_map": {
            "focal":  "A489,A504,A505,A506",
            "broad":  "A239,A241,A489,A491,A505,A558",
            "mixed":  "A241,A489,A504,A505,A558",
        },
        "guide_scale": [5, 7, 10, 15],
        "T":            [25, 50, 100],
        "num_designs":  [4, 8, 16],
    },
    "ferritin": {
        # Diseño de novo alrededor del sitio de mutación CYS (res 35-60 chain A)
        "contigs":       ["[A35-60/0 25-35]", "[A35-60/0 35-45]", "[A40-55/0 30-40]"],
        "hotspot_variant": ["heme_coord", "surface_only"],
        "hotspot_map": {
            "heme_coord":   "A46,A52",          # HIS46, MET52 (coordinación hemo)
            "surface_only": "A40,A43,A49",       # sitios de mutación CYS
        },
        "guide_scale": [5, 10, 15],
        "T":            [50, 100],
        "num_designs":  [4, 8],
    },
}

# Defaults razonables para primera iteración (ferritin no tiene historial)
FIRST_RUN_DEFAULTS = {
    "nipah": {
        "contigs": "90-90",
        "hotspot_variant": "focal",
        "guide_scale": 15,
        "T": 50,
        "num_designs": 8,
    },
    "ferritin": {
        "contigs": "[A35-60/0 30-40]",
        "hotspot_variant": "heme_coord",
        "guide_scale": 10,
        "T": 50,
        "num_designs": 8,
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _params_to_key(params: dict) -> tuple:
    """Convierte params a clave comparable (hashable) para detectar repeticiones."""
    return (
        params.get("contigs", ""),
        params.get("hotspot_variant", params.get("hotspot", "")),
        str(params.get("guide_scale", "")),
        str(params.get("T", "")),
        str(params.get("num_designs", "")),
    )


def _history_keys(param_history: list) -> set:
    """Retorna conjunto de claves ya exploradas."""
    keys = set()
    for p in param_history:
        keys.add(_params_to_key(p))
    return keys


def _step_index(space_list: list, current_val, delta: int) -> int:
    """Mueve delta pasos desde current_val en space_list; hace wrap."""
    try:
        idx = space_list.index(current_val)
    except ValueError:
        idx = 0
    return (idx + delta) % len(space_list)


def _build_params(target_name: str, contigs: str, hotspot_variant: str,
                  guide_scale: int, T: int, num_designs: int) -> dict:
    """Construye el dict de params completo con el hotspot resuelto."""
    hmap = PARAM_SPACES[target_name]["hotspot_map"]
    hotspot = hmap.get(hotspot_variant, "")
    return {
        "contigs":         contigs,
        "hotspot":         hotspot,
        "hotspot_variant": hotspot_variant,
        "guide_scale":     guide_scale,
        "T":               T,
        "num_designs":     num_designs,
    }


# ══════════════════════════════════════════════════════════════════════════════
# Estrategia EXPLOIT
# ══════════════════════════════════════════════════════════════════════════════

def _exploit(target_name: str, best_params: dict,
             history_keys: set, max_tries: int = 20) -> dict:
    """
    Perturba ±1 paso en los ejes del espacio de parámetros alrededor de best_params.
    Varía exactamente 1 parámetro a la vez (mutación puntual).
    """
    space = PARAM_SPACES[target_name]
    axes = ["contigs", "guide_scale", "T", "num_designs", "hotspot_variant"]

    # Candidatos: variar cada eje ±1 partiendo de la base COMPLETA
    base = {
        "contigs":         best_params.get("contigs", space["contigs"][0]),
        "hotspot_variant": best_params.get("hotspot_variant", space["hotspot_variant"][0]),
        "guide_scale":     best_params.get("guide_scale", space["guide_scale"][0]),
        "T":               best_params.get("T", space["T"][0]),
        "num_designs":     best_params.get("num_designs", space["num_designs"][0]),
    }
    candidates = []
    for axis in axes:
        vals = space[axis]
        for delta in (-1, +1):
            new_params = deepcopy(base)
            idx = _step_index(vals, base[axis], delta)
            new_params[axis] = vals[idx]
            # Resolver hotspot si cambió la variante
            if axis == "hotspot_variant":
                new_params["hotspot"] = space["hotspot_map"][vals[idx]]
            else:
                new_params["hotspot"] = space["hotspot_map"].get(
                    new_params["hotspot_variant"], "")
            key = _params_to_key(new_params)
            if key not in history_keys:
                candidates.append(new_params)

    if candidates:
        random.shuffle(candidates)
        return candidates[0]

    # Si todos los vecinos están explorados → caer en explore
    return _explore(target_name, history_keys)


# ══════════════════════════════════════════════════════════════════════════════
# Estrategia EXPLORE
# ══════════════════════════════════════════════════════════════════════════════

def _explore(target_name: str, history_keys: set) -> dict:
    """
    Elige una combinación no explorada del espacio de parámetros.
    Prioriza combinaciones con guide_scale y hotspot_variant distintos al último run.
    """
    space = PARAM_SPACES[target_name]

    # Generar todas las combinaciones posibles
    all_combos = list(product(
        space["contigs"],
        space["hotspot_variant"],
        space["guide_scale"],
        space["T"],
        space["num_designs"],
    ))
    random.shuffle(all_combos)

    for contigs, hv, gs, T, nd in all_combos:
        params = _build_params(target_name, contigs, hv, gs, T, nd)
        if _params_to_key(params) not in history_keys:
            return params

    # Si el espacio está saturado (muy raro), elegir aleatoriamente
    contigs, hv, gs, T, nd = random.choice(all_combos)
    return _build_params(target_name, contigs, hv, gs, T, nd)


# ══════════════════════════════════════════════════════════════════════════════
# API pública
# ══════════════════════════════════════════════════════════════════════════════

def generate_next_params(target: dict, target_name: str) -> tuple[dict, str]:
    """
    Genera los parámetros para la próxima corrida.

    Args:
        target: sub-dict del target desde ITERATION_STATE.json
        target_name: "nipah" o "ferritin"

    Returns:
        (params_dict, strategy_str) donde strategy_str es "exploit" o "explore"
    """
    from .state_manager import get_strategy

    iteration    = target.get("iteration", 0)
    param_history = target.get("param_history", [])
    history_keys = _history_keys(param_history)

    # Primera iteración: usar defaults
    if iteration == 0 or not param_history:
        defaults = deepcopy(FIRST_RUN_DEFAULTS[target_name])
        hmap = PARAM_SPACES[target_name]["hotspot_map"]
        defaults["hotspot"] = hmap.get(defaults.get("hotspot_variant", ""), "")
        return defaults, "explore"

    strategy = get_strategy(target)

    # Obtener mejores parámetros conocidos (de best_run si existe)
    best_run_id = target.get("best_run")
    best_params = None
    if best_run_id:
        for run in target.get("runs", []):
            if run["run_id"] == best_run_id:
                best_params = deepcopy(run.get("params", {}))
                break

    if not best_params and param_history:
        best_params = deepcopy(param_history[-1])

    if not best_params:
        best_params = deepcopy(FIRST_RUN_DEFAULTS[target_name])

    # Rellenar claves faltantes con defaults para que _exploit tenga base completa
    defaults = FIRST_RUN_DEFAULTS[target_name]
    for k, v in defaults.items():
        if k not in best_params or best_params[k] is None:
            best_params[k] = v

    if strategy == "exploit":
        params = _exploit(target_name, best_params, history_keys)
    else:
        params = _explore(target_name, history_keys)

    return params, strategy


def rationale(params: dict, strategy: str, target: dict) -> str:
    """Genera un texto explicativo de por qué se eligieron estos parámetros."""
    stuck = target.get("stuck_count", 0)
    best_score = target.get("best_score", 0.0)
    iteration  = target.get("iteration", 0)

    if strategy == "explore":
        if stuck >= 2:
            reason = f"EXPLORAR: {stuck} iteraciones sin mejora (stuck_count={stuck})"
        elif iteration % 4 == 0 and iteration > 0:
            reason = f"EXPLORAR: ciclo de exploración forzada (iteración {iteration} % 4 == 0)"
        else:
            reason = "EXPLORAR: primera iteración — inicializando búsqueda"
    else:
        reason = f"EXPLOTAR: última corrida mejoró el score (mejor actual: {best_score:.4f})"

    lines = [
        f"**Estrategia:** {strategy.upper()} — {reason}",
        "",
        "| Parámetro | Valor | Razón |",
        "| --- | --- | --- |",
        f"| contigs | {params.get('contigs')} | Longitud del binder |",
        f"| hotspot | {params.get('hotspot') or '(ninguno)'} | Residuos de interfaz objetivo |",
        f"| guide_scale | {params.get('guide_scale')} | Fuerza del guidance de hotspot |",
        f"| T | {params.get('T')} | Pasos de difusión |",
        f"| num_designs | {params.get('num_designs')} | Secuencias por backbone |",
    ]
    return "\n".join(lines)
