"""
shinka_integration.py — Integración de ShinkaEvolve con automated_lab/param_generator.py

Usa ShinkaEvolve como motor de optimización evolutiva para los parámetros
de diseño de proteínas (RFdiffusion binder design), reemplazando la búsqueda
aleatoria/exploit-explore simple por evolución de código guiada por LLM.

Flujo:
  1. param_generator.py genera candidatos iniciales
  2. ShinkaEvolve evoluciona programas de evaluación de parámetros
  3. Los mejores parámetros se usan en la siguiente corrida Colab
"""

import os
import json
import tempfile
from pathlib import Path
from typing import Optional

# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

SHINKA_CONFIG = {
    "model": "anthropic/claude-sonnet-4-20250514",  # Modelo para mutaciones
    "population_size": 8,
    "max_generations": 10,
    "archive_size": 20,
    "mutation_rate": 0.3,
    "crossover_rate": 0.2,
    "novelty_weight": 0.3,
    "island_count": 2,
    "migration_interval": 3,
}

# API keys necesarios
REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "OPENROUTER_API_KEY"]  # OpenRouter compatible con OpenAI endpoint

# OpenRouter config (compatible con OpenAI SDK)
OPENROUTER_CONFIG = {
    "base_url": "https://openrouter.ai/api/v1",
    "api_key_env": "OPENROUTER_API_KEY",
    "default_model": "anthropic/claude-sonnet-4-20250514",  # o el que prefieras
}


def check_prerequisites() -> dict:
    """Verifica que ShinkaEvolve esté instalado y configurado."""
    result = {
        "shinka_installed": False,
        "api_key_set": False,
        "ready": False,
        "errors": [],
    }
    
    try:
        import shinka
        result["shinka_installed"] = True
        result["shinka_version"] = getattr(shinka, "__version__", "unknown")
    except ImportError:
        result["errors"].append("ShinkaEvolve no instalado. Ejecutar: pip install shinka-evolve")
        return result
    # Verificar API key (OpenAI, Anthropic, o OpenRouter)
    api_keys_found = []
    for var in REQUIRED_ENV_VARS:
        if os.environ.get(var):
            api_keys_found.append(var)
    
    if api_keys_found:
        result["api_key_set"] = True
        result["api_keys_found"] = api_keys_found
    else:
        result["errors"].append(f"Falta API key. Definir una de: {REQUIRED_ENV_VARS}")
        result["errors"].append("OpenRouter (OPENROUTER_API_KEY) es compatible con el endpoint de OpenAI")
    
    result["ready"] = result["shinka_installed"] and result["api_key_set"]
    return result


# ══════════════════════════════════════════════════════════════════════════════
# Función de fitness para parámetros de RFdiffusion
# ══════════════════════════════════════════════════════════════════════════════

def fitness_from_iteration_state(target_name: str, iteration_state_path: str) -> Optional[float]:
    """
    Extrae el composite score del ITERATION_STATE.json para usar como fitness.
    
    Returns:
        float: composite score del mejor run, o None si no hay datos.
    """
    try:
        with open(iteration_state_path) as f:
            state = json.load(f)
        
        target = state.get("targets", {}).get(target_name, {})
        return target.get("best_score", None)
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None


# ══════════════════════════════════════════════════════════════════════════════
# Wrapper de ShinkaEvolve para param_generator
# ══════════════════════════════════════════════════════════════════════════════

def generate_with_shinka(
    target_name: str,
    param_history: list,
    best_score: float,
    iteration_state_path: str,
    output_dir: str = "/tmp/shinka_evolve",
) -> dict:
    """
    Usa ShinkaEvolve para generar la siguiente combinación de parámetros.
    
    Args:
        target_name: "nipah" o "ferritin"
        param_history: lista de params ya explorados
        best_score: mejor composite score actual
        iteration_state_path: path al ITERATION_STATE.json
        output_dir: directorio para resultados de Shinka
    
    Returns:
        dict con los parámetros generados
    """
    from shinka import ShinkaEvolveRunner
    
    # Crear programa inicial basado en param_generator.py
    initial_program = _build_initial_program(target_name, param_history)
    
    # Configurar ShinkaEvolve
    config = {
        "experiment": {
            "name": f"protein_lab_{target_name}",
            "program": initial_program,
            "evaluate": "evaluate_params",
            "fitness_function": "maximize_composite_score",
        },
        "evolution": {
            "population_size": SHINKA_CONFIG["population_size"],
            "max_generations": SHINKA_CONFIG["max_generations"],
            "archive_size": SHINKA_CONFIG["archive_size"],
            "mutation_rate": SHINKA_CONFIG["mutation_rate"],
            "crossover_rate": SHINKA_CONFIG["crossover_rate"],
            "novelty_weight": SHINKA_CONFIG["novelty_weight"],
            "island_count": SHINKA_CONFIG["island_count"],
            "migration_interval": SHINKA_CONFIG["migration_interval"],
        },
        "model": {
            "name": SHINKA_CONFIG["model"],
        },
        "output": {
            "dir": output_dir,
        },
    }
    
    # Ejecutar evolución
    runner = ShinkaEvolveRunner(config)
    result = runner.run()
    
    # Extraer mejores parámetros
    best_params = _extract_params_from_result(result, target_name)
    
    return best_params


def _build_initial_program(target_name: str, param_history: list) -> str:
    """
    Construye el programa inicial para ShinkaEvolve basado en el espacio
    de parámetros de param_generator.py y el historial de corridas.
    """
    from src.iteration.param_generator import PARAM_SPACES, FIRST_RUN_DEFAULTS
    
    space = PARAM_SPACES.get(target_name, {})
    defaults = FIRST_RUN_DEFAULTS.get(target_name, {})
    
    program = f'''
"""
Parameter generator for {target_name} RFdiffusion binder design.
Evolved by ShinkaEvolve to maximize composite score (pLDDT, ipTM, PAE).
"""

PARAM_SPACE = {json.dumps(space, indent=2)}
DEFAULTS = {json.dumps(defaults, indent=2)}
PARAM_HISTORY = {json.dumps(param_history[-10:], indent=2)}  # Last 10 runs

def generate_params() -> dict:
    """Generate next parameter combination to try."""
    # TODO: ShinkaEvolve will mutate this function
    import random
    
    # Simple strategy: vary one parameter at a time from best known
    if PARAM_HISTORY:
        base = PARAM_HISTORY[-1].copy()
    else:
        base = DEFAULTS.copy()
    
    # Vary guide_scale
    guide_options = PARAM_SPACE["guide_scale"]
    base["guide_scale"] = random.choice(guide_options)
    
    return base

if __name__ == "__main__":
    params = generate_params()
    print(json.dumps(params, indent=2))
'''
    return program


def _extract_params_from_result(result: dict, target_name: str) -> dict:
    """Extrae los mejores parámetros del resultado de ShinkaEvolve."""
    try:
        best = result.get("best_program", {})
        if isinstance(best, dict) and "params" in best:
            return best["params"]
        # Fallback: usar el último programa evolucionado
        archive = result.get("archive", [])
        if archive:
            latest = archive[-1]
            return latest.get("params", {})
    except (KeyError, IndexError, TypeError):
        pass
    
    # Fallback a param_generator estándar
    from src.iteration.param_generator import FIRST_RUN_DEFAULTS
    return FIRST_RUN_DEFAULTS.get(target_name, {})


# ══════════════════════════════════════════════════════════════════════════════
# API pública: reemplazo drop-in para generate_next_params()
# ══════════════════════════════════════════════════════════════════════════════

def generate_next_params_shinka(target: dict, target_name: str) -> tuple:
    """
    Drop-in replacement for param_generator.generate_next_params().
    
    Usa ShinkaEvolve si está disponible y configurado, 
    fallback a param_generator estándar si no.
    
    Returns:
        (params_dict, strategy_str)
    """
    prereqs = check_prerequisites()
    
    if not prereqs["ready"]:
        # Fallback a param_generator estándar
        from src.iteration.param_generator import generate_next_params
        return generate_next_params(target, target_name)
    
    # Usar ShinkaEvolve
    param_history = target.get("param_history", [])
    best_score = target.get("best_score", 0.0)
    iteration_state = os.path.join(
        os.path.dirname(__file__), "..", "..", "colab_runs", "ITERATION_STATE.json"
    )
    
    params = generate_with_shinka(
        target_name=target_name,
        param_history=param_history,
        best_score=best_score,
        iteration_state_path=iteration_state,
    )
    
    return params, "shinka_evolve"
