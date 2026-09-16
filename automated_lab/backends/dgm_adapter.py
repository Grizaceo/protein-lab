#!/usr/bin/env python3
"""
automated_lab/backends/dgm_adapter.py
======================================
Adapter del automated_lab para Darwin Gödel Machine (DGM).

DGM es un sistema de auto-mejora de código: toma un agente inicial,
lo hace evolucionar mediante mutaciones LLM-guiadas, y valida cada
generación contra un benchmark (SWE-bench o Polyglot).

Uso en protein-lab:
  - Evolucionar scripts de análisis para mejorar métricas
  - Auto-mejorar pipelines de docking/MD
  - Generar variantes de código y quedarse con las mejores

Requiere: Docker, API key (OpenAI/Anthropic), SWE-bench dataset.
"""

from __future__ import annotations

import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent.parent.parent
DGM_DIR = Path("/home/gris96/oss-science-agents/dgm")

# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

DGM_REQUIRED_ENV = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
DGM_ENTRY = DGM_DIR / "DGM_outer.py"

# Prompts disponibles
DGM_PROMPTS_DIR = DGM_DIR / "prompts"
DGM_PROMPTS = {
    "self_improvement": DGM_PROMPTS_DIR / "self_improvement_prompt.py",
    "tooluse": DGM_PROMPTS_DIR / "tooluse_prompt.py",
    "testrepo": DGM_PROMPTS_DIR / "testrepo_prompt.py",
    "diagnose": DGM_PROMPTS_DIR / "diagnose_improvement_prompt.py",
}

# Tools disponibles para el agente
DGM_TOOLS_DIR = DGM_DIR / "tools"
DGM_TOOLS = {
    "bash": DGM_TOOLS_DIR / "bash.py",
    "edit": DGM_TOOLS_DIR / "edit.py",
}


# ══════════════════════════════════════════════════════════════════════════════
# Adapter
# ══════════════════════════════════════════════════════════════════════════════

class DGMAdapter:
    """Adapter para Darwin Gödel Machine."""

    PROVIDER_NAME = "dgm"

    @classmethod
    def check_prerequisites(cls) -> dict:
        """Verifica que DGM esté instalado y configurado."""
        result = {
            "dgm_installed": False,
            "docker_available": False,
            "api_key_set": False,
            "swe_bench_ready": False,
            "ready": False,
            "errors": [],
        }

        # Verificar repo
        if DGM_DIR.exists() and DGM_ENTRY.exists():
            result["dgm_installed"] = True
        else:
            result["errors"].append(f"DGM no encontrado en {DGM_DIR}")

        # Verificar Docker
        try:
            r = subprocess.run(
                ["docker", "info"], capture_output=True, text=True, timeout=10
            )
            result["docker_available"] = r.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            result["errors"].append("Docker no disponible")

        # Verificar API key
        for var in DGM_REQUIRED_ENV:
            if os.environ.get(var):
                result["api_key_set"] = True
                break
        if not result["api_key_set"]:
            result["errors"].append(f"Falta API key. Definir una de: {DGM_REQUIRED_ENV}")

        # Verificar SWE-bench
        swe_dir = DGM_DIR / "swe_bench" / "SWE-bench"
        result["swe_bench_ready"] = swe_dir.exists()

        result["ready"] = (
            result["dgm_installed"]
            and result["docker_available"]
            and result["api_key_set"]
        )
        return result

    @classmethod
    def run_evolution(
        cls,
        output_dir: str,
        prevrun_dir: str | None = None,
        polyglot: bool = False,
        selfimprove_size: int = 4,
        method: str = "random",
        run_baseline: bool | None = None,
    ) -> dict:
        """
        Ejecuta una corrida de evolución DGM.

        Args:
            output_dir: directorio de salida
            prevrun_dir: directorio de corrida previa (para continuar)
            polyglot: usar benchmark Polyglot en vez de SWE-bench
            selfimprove_size: número de self-improves por generación
            method: método de selección ('random', 'best', etc.)
            run_baseline: ejecutar baseline

        Returns:
            dict con resultado de la ejecución
        """
        cmd = [
            "python", str(DGM_ENTRY),
            "--output-dir", output_dir,
            "--selfimprove-size", str(selfimprove_size),
            "--method", method,
        ]

        if prevrun_dir:
            cmd += ["--prevrun-dir", prevrun_dir]
        if polyglot:
            cmd.append("--polyglot")
        if run_baseline is not None:
            cmd += ["--run-baseline", str(run_baseline)]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=7200,  # 2 horas max
                cwd=str(DGM_DIR),
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout[-1000:] if result.stdout else "",
                "stderr": result.stderr[-500:] if result.stderr else "",
                "output_dir": output_dir,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout (>2h)", "output_dir": output_dir}
        except Exception as e:
            return {"success": False, "error": str(e), "output_dir": output_dir}

    @classmethod
    def evolve_script(
        cls,
        script_path: str,
        metric_func: str,
        output_dir: str = "/tmp/dgm_evolve",
        generations: int = 5,
    ) -> dict:
        """
        Evoluciona un script del lab para mejorar una métrica.

        Este es el wrapper de alto nivel para usar DGM con scripts
        de protein-lab. Prepara el entorno, copia el script como
        "initial agent", y lanza la evolución.

        Args:
            script_path: path al script a evolucionar
            metric_func: nombre de la función de métrica
            output_dir: directorio de salida
            generaciones: número de generaciones

        Returns:
            dict con el mejor script encontrado
        """
        script = Path(script_path)
        if not script.exists():
            return {"success": False, "error": f"Script no encontrado: {script_path}"}

        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        # Copiar script como "initial"
        initial_dir = out / "initial"
        initial_dir.mkdir(exist_ok=True)
        shutil.copy2(script, initial_dir / script.name)

        # Crear eval stub
        eval_script = initial_dir / "evaluate.py"
        eval_script.write_text(f'''
import subprocess
import sys

def evaluate(script_path: str) -> float:
    """Evalúa un script y retorna un score (mayor = mejor)."""
    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode != 0:
            return 0.0
        # Métrica personalizada
        return {metric_func}(result.stdout)
    except Exception:
        return 0.0

if __name__ == "__main__":
    score = evaluate(sys.argv[1])
    print(f"{{score}}")
''')

        return cls.run_evolution(output_dir=output_dir)

    @classmethod
    def get_prompts(cls) -> list[dict]:
        """Lista los prompts disponibles."""
        return [
            {"name": k, "path": str(v), "exists": v.exists()}
            for k, v in DGM_PROMPTS.items()
        ]

    @classmethod
    def get_tools(cls) -> list[dict]:
        """Lista los tools disponibles para el agente."""
        return [
            {"name": k, "path": str(v), "exists": v.exists()}
            for k, v in DGM_TOOLS.items()
        ]

    @classmethod
    def summary(cls) -> str:
        """Resumen del estado del adapter."""
        checks = cls.check_prerequisites()
        lines = [
            "=== Darwin Gödel Machine Adapter ===",
            f"DGM: {'OK' if checks['dgm_installed'] else 'MISSING'}",
            f"Docker: {'OK' if checks['docker_available'] else 'MISSING'}",
            f"API Key: {'OK' if checks['api_key_set'] else 'MISSING'}",
            f"SWE-bench: {'OK' if checks['swe_bench_ready'] else 'MISSING'}",
            f"Prompts: {len([p for p in DGM_PROMPTS.values() if p.exists()])}/{len(DGM_PROMPTS)}",
            f"Tools: {len([t for t in DGM_TOOLS.values() if t.exists()])}/{len(DGM_TOOLS)}",
        ]
        if checks["errors"]:
            lines.append(f"Errores: {', '.join(checks['errors'])}")
        return "\n".join(lines)
