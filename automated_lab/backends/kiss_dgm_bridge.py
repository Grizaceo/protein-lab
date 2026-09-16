#!/usr/bin/env python3
"""
automated_lab/backends/kiss_dgm_bridge.py
==========================================
Puente KISS + DGM: evolución guiada de código científico.

KISS Discovery Engine genera variantes de código + las verifica.
DGM toma esas variantes como población inicial y las evoluciona
por generaciones, usando el verifier de KISS como función de fitness.

Flujo:
  1. KISS genera N variantes de un prompt (población inicial)
  2. El verifier de KISS puntúa cada variante (fitness)
  3. DGM toma las mejores, las muta via LLM, verifica con KISS
  4. Repite por G generaciones
  5. Retorna el mejor código encontrado + su score

Esto es esencialmente un "search + evolve" loop:
  - KISS = search amplio (brute-force generation + verify)
  - DGM = evolución dirigida (mutation + selection + breeding)
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

LAB_DIR = Path(__file__).resolve().parent.parent.parent
KISS_DIR = Path("/home/gris96/.hermes/workspace/repos/kiss_discovery_engine")
DGM_DIR = Path("/home/gris96/oss-science-agents/dgm")

# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

DEFAULT_TOPIC = "python_code"
DEFAULT_VARIANTS = 10
DEFAULT_GENERATIONS = 5
DEFAULT_TEMPERATURE = 0.85

# Topics disponibles en KISS
KISS_TOPICS = [
    "python_code", "javascript_code", "sql_queries",
    "number_theory", "combinatorics", "graph_algorithms",
    "optimization", "data_analysis", "machine_learning",
    "bioinformatics", "chemistry", "physics",
    "mathematics", "statistics", "algorithm_design",
    "testing", "automation", "brainstorm",
]


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _run_kiss_generation(
    prompt: str,
    topic: str = DEFAULT_TOPIC,
    variants: int = DEFAULT_VARIANTS,
    temperature: float = DEFAULT_TEMPERATURE,
) -> list[dict]:
    """Corre KISS para generar variantes de código."""
    cmd = [
        "python", "-m", "src.engine",
        "--prompt", prompt,
        "--topic", topic,
        "--variants", str(variants),
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=300, cwd=str(KISS_DIR)
    )
    # Parsear output de KISS (JSON lines o stdout)
    candidates = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            candidates.append(data)
        except json.JSONDecodeError:
            # Si no es JSON, tratar como texto plano
            candidates.append({"candidate": line, "status": "raw"})
    return candidates


def _kiss_verify(
    candidate: str,
    topic: str = DEFAULT_TOPIC,
) -> dict:
    """Verifica un candidato con el verifier de KISS."""
    # Escribir candidato temporal
    tmp = Path(tempfile.mktemp(suffix=".py"))
    tmp.write_text(candidate)
    try:
        cmd = [
            "python", "-c",
            f"""
import asyncio, json, sys
sys.path.insert(0, '{KISS_DIR}')
from src.engine import KissDiscoveryEngine
from src.topics import get_topic_config

async def main():
    engine = KissDiscoveryEngine()
    result = await engine.expand_seed(
        seed={{'candidate': open('{tmp}').read()}},
        topic_name='{topic}',
    )
    print(json.dumps(result))

asyncio.run(main())
"""
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout.strip())
        return {"status": "error", "feedback": result.stderr[:500]}
    finally:
        tmp.unlink(missing_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
# Adapter
# ══════════════════════════════════════════════════════════════════════════════

class KissDgmBridge:
    """
    Puente KISS + DGM para evolución de código científico.

    Combina la generación bruta de KISS con la evolución dirigida de DGM
    para encontrar implementaciones óptimas de funciones/problemas.
    """

    @classmethod
    def check_prerequisites(cls) -> dict:
        """Verifica que KISS y DGM estén disponibles."""
        result = {
            "kiss_installed": KISS_DIR.exists(),
            "dgm_installed": DGM_DIR.exists(),
            "docker_available": False,
            "kiss_api_key": bool(
                os.environ.get("MERCURY_API_KEY")
                or os.environ.get("OPENROUTER_API_KEY")
            ),
            "ready": False,
            "errors": [],
        }

        # Docker
        try:
            r = subprocess.run(
                ["docker", "info"], capture_output=True, text=True, timeout=10
            )
            result["docker_available"] = r.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            result["errors"].append("Docker no disponible (requerido por DGM)")

        result["ready"] = (
            result["kiss_installed"]
            and result["dgm_installed"]
            and result["docker_available"]
            and result["kiss_api_key"]
        )
        return result

    @classmethod
    def evolve(
        cls,
        prompt: str,
        topic: str = DEFAULT_TOPIC,
        variants: int = DEFAULT_VARIANTS,
        generations: int = DEFAULT_GENERATIONS,
        temperature: float = DEFAULT_TEMPERATURE,
        fitness_func: Callable[[str], float] | None = None,
        output_dir: str | None = None,
    ) -> dict:
        """
        Loop completo KISS → DGM → evolución.

        Args:
            prompt: descripción del código a generar/optimizar
            topic: dominio (python_code, bioinformatics, etc.)
            variants: variantes iniciales que genera KISS
            generaciones: generaciones de evolución DGM
            temperature: creatividad de las mutaciones
            fitness_func: función custom de fitness (opcional).
                          Si no se pasa, usa el verifier de KISS.
            output_dir: directorio para resultados intermedios

        Returns:
            dict con:
                - best_code: el mejor código encontrado
                - best_score: su score de fitness
                - generation_history: historia por generación
                - total_evaluated: total de variantes evaluadas
        """
        out = Path(output_dir) if output_dir else Path(tempfile.mkdtemp(prefix="kiss_dgm_"))
        out.mkdir(parents=True, exist_ok=True)

        history = []
        total_evaluated = 0

        # ══════════════════════════════════════════════════════════════════
        # FASE 1: KISS genera población inicial
        # ══════════════════════════════════════════════════════════════════
        print(f"[KISS+DGM] Fase 1: generando {variantes} variantes con KISS...")
        seed_candidates = _run_kiss_generation(
            prompt=prompt, topic=topic, variants=variants, temperature=temperature
        )
        print(f"[KISS+DGM] KISS generó {len(seed_candidates)} variantes")

        # ══════════════════════════════════════════════════════════════════
        # FASE 2: Verificar población inicial (fitness)
        # ══════════════════════════════════════════════════════════════════
        print(f"[KISS+DGM] Fase 2: verificando población inicial...")
        evaluated = []
        for i, cand in enumerate(seed_candidates):
            code = cand.get("candidate", "")
            if not code:
                continue

            if fitness_func:
                score = fitness_func(code)
            else:
                # Usar verifier de KISS
                verification = _kiss_verify(code, topic)
                score = 1.0 if verification.get("status") == "pass" else 0.0

            evaluated.append({
                "code": code,
                "score": score,
                "generation": 0,
                "source": "kiss_seed",
            })
            total_evaluated += 1

        if not evaluated:
            return {
                "success": False,
                "error": "No se generaron candidatos válidos",
                "generation_history": [],
            }

        # Ordenar por score
        evaluated.sort(key=lambda x: x["score"], reverse=True)
        best = evaluated[0]

        history.append({
            "generation": 0,
            "population_size": len(evaluated),
            "best_score": best["score"],
            "mean_score": sum(e["score"] for e in evaluated) / len(evaluated),
        })

        print(f"[KISS+DGM] Mejor seed: score={best['score']:.3f}")

        # ══════════════════════════════════════════════════════════════════
        # FASE 3: DGM evoluciona la población
        # ══════════════════════════════════════════════════════════════════
        pop_dir = out / "population"
        pop_dir.mkdir(exist_ok=True)

        for gen in range(1, generations + 1):
            print(f"[KISS+DGM] Generación {gen}/{generations}...")

            # Seleccionar padres (top 50%)
            parents = evaluated[: max(2, len(evaluated) // 2)]

            # Escribir Dockerfile para esta generación
            gen_dir = pop_dir / f"gen_{gen}"
            gen_dir.mkdir(exist_ok=True)

            # Preparar "agente" para DGM = el mejor código + instrucciones de mutación
            best_parent = parents[0]
            agent_dir = gen_dir / "initial"
            agent_dir.mkdir(exist_ok=True)

            # Escribir el código como "main.py"
            (agent_dir / "main.py").write_text(best_parent["code"])

            # Escribir instrucciones de mejora
            (agent_dir / "TASK.md").write_text(f"""
# Task: Improve this {topic} code

## Original Prompt
{prompt}

## Current Best Code (score={best_parent['score']:.3f})
```python
{best_parent['code']}
```

## Instructions
Improve this code. Possible directions:
- Make it more efficient
- Handle edge cases
- Add error handling
- Improve readability
- Make it more general

## Evaluation
Your code will be tested by running it and checking if it produces correct output.
The fitness function scores from 0.0 (fails) to 1.0 (perfect).
""")

            # Mutar vía LLM (simulación del paso DGM)
            # En DGM real esto corre en Docker con el agente completo
            # Aquí usamos KISS para mutar el código de los padres
            mutated = []
            for parent in parents:
                mutation_prompt = f"""
Improve this {topic} code. Make a meaningful change that could improve its functionality or performance.

Original code:
```python
{parent['code']}
```

Generate ONE improved version. Only output the code, no explanations.
"""
                mut_candidates = _run_kiss_generation(
                    prompt=mutation_prompt,
                    topic=topic,
                    variants=2,
                    temperature=temperature,
                )
                mutated.extend(mut_candidates)

            # Verificar mutaciones
            gen_evaluated = []
            for mut in mutated:
                code = mut.get("candidate", "")
                if not code or len(code) < 10:
                    continue

                if fitness_func:
                    score = fitness_func(code)
                else:
                    verification = _kiss_verify(code, topic)
                    score = 1.0 if verification.get("status") == "pass" else 0.0

                gen_evaluated.append({
                    "code": code,
                    "score": score,
                    "generation": gen,
                    "source": f"dgm_mutation_gen{gen}",
                })
                total_evaluated += 1

            # Combinar población anterior + mutaciones, seleccionar mejores
            evaluated = sorted(
                evaluated + gen_evaluated,
                key=lambda x: x["score"],
                reverse=True
            )[: variants]  # mantener tamaño de población

            current_best = evaluated[0]
            if current_best["score"] > best["score"]:
                best = current_best
                print(f"[KISS+DGM] ¡Nuevo mejor! score={best['score']:.3f} (gen {gen})")

            history.append({
                "generation": gen,
                "population_size": len(evaluated),
                "best_score": best["score"],
                "mean_score": sum(e["score"] for e in evaluated) / len(evaluated),
                "mutations_tried": len(mutated),
            })

        # ══════════════════════════════════════════════════════════════════
        # Resultado
        # ══════════════════════════════════════════════════════════════════
        result = {
            "success": True,
            "best_code": best["code"],
            "best_score": best["score"],
            "best_generation": best["generation"],
            "generation_history": history,
            "total_evaluated": total_evaluated,
            "output_dir": str(out),
            "topic": topic,
            "prompt": prompt,
        }

        # Guardar resultado
        (out / "result.json").write_text(json.dumps(result, indent=2, default=str))
        (out / "best_code.py").write_text(best["code"])

        print(f"[KISS+DGM] Listo. Mejor score={best['score']:.3f} después de {total_evaluated} evaluaciones")

        return result

    @classmethod
    def quick_search(
        cls,
        prompt: str,
        topic: str = DEFAULT_TOPIC,
        variants: int = 20,
    ) -> dict:
        """
        Solo KISS (sin evolución DGM). Útil para exploración rápida.

        Args:
            prompt: qué código necesitás
            topic: dominio
            variants: cuántas variantes generar

        Returns:
            dict con los mejores candidatos
        """
        candidates = _run_kiss_generation(prompt, topic, variants)

        results = []
        for cand in candidates:
            code = cand.get("candidate", "")
            if not code:
                continue
            verification = _kiss_verify(code, topic)
            score = 1.0 if verification.get("status") == "pass" else 0.0
            results.append({"code": code, "score": score})

        results.sort(key=lambda x: x["score"], reverse=True)

        return {
            "success": True,
            "candidates": results,
            "best": results[0] if results else None,
            "total": len(results),
        }

    @classmethod
    def summary(cls) -> str:
        """Resumen del estado."""
        checks = cls.check_prerequisites()
        lines = [
            "=== KISS + DGM Bridge ===",
            f"KISS: {'OK' if checks['kiss_installed'] else 'MISSING'}",
            f"DGM: {'OK' if checks['dgm_installed'] else 'MISSING'}",
            f"Docker: {'OK' if checks['docker_available'] else 'MISSING'}",
            f"KISS API Key: {'OK' if checks['kiss_api_key'] else 'MISSING'}",
            f"Topics: {len(KISS_TOPICS)}",
        ]
        if checks["errors"]:
            lines.append(f"Errores: {', '.join(checks['errors'])}")
        return "\n".join(lines)
