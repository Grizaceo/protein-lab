#!/usr/bin/env python3
"""
kiss_dgm.py — KISS Discovery Engine + Darwin Gödel Bridge (agnostic tools)

Dos herramientas independientes que trabajan juntas:

  KISS (Discovery Engine)
  ───────────────────────
  Generación bruta de código/ideas + verificación automática.
  Se usa vía MCP (stdio) o vía subprocess.

  Herramientas MCP expuestas (server: kiss-brainstorm):
    brainstorm(prompt, n, temperature, constraints, verifier_id, skip_verifier)
    record_feedback(run_id, useful_indices, feedback_text, save_verifier)
    list_verifiers()
    get_verifier(verifier_id)
    get_run(run_id)
    list_recent_runs(limit)
    health()

  DGM (Darwin Gödel Machine)
  ───────────────────────────
  Evolución dirigida de código: muta, selecciona, reproduce.
  Requiere Docker + API key (OpenAI/Anthropic).

  Uso agnóstico:
    KISS y DGM NO dependen de protein-lab.
    Desde cualquier repo:
      python kiss_dgm.py kiss --prompt "..." --topic python_code
      python kiss_dgm.py dgm --script ./my_script.py --generations 10
      python kiss_dgm.py evolve --prompt "..." --generations 5

  Como library:
    from kiss_dgm import KISS, DGM, Evolution

    # KISS: generar variantes
    variants = KISS.brainstorm("sort a list", n=10, topic="python_code")

    # KISS: verificar
    result = KISS.verify(code, topic="python_code")

    # DGM: evolucionar un script
    best = DGM.evolve(script_path="./analysis.py", metric="accuracy", generations=5)

    # Combinado: KISS genera población, DGM evoluciona
    best = Evolution.run(
        prompt="write a fast sorting function",
        topic="python_code",
        variants=20,
        generations=10,
    )
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

# ══════════════════════════════════════════════════════════════════════════════
# Rutas (agnosticas — no dependen de protein-lab)
# ══════════════════════════════════════════════════════════════════════════════

KISS_DIR = Path("/home/gris/.hermes/workspace/repos/kiss_discovery_engine")
KISS_MCP_ENTRY = KISS_DIR / "src" / "mcp_server.py"
KISS_ENGINE_ENTRY = KISS_DIR / "src" / "engine.py"
KISS_LEDGER = KISS_DIR / "artifacts" / "ledger.db"

DGM_DIR = Path("/home/gris/oss-science-agents/dgm")
DGM_ENTRY = DGM_DIR / "DGM_outer.py"


# ══════════════════════════════════════════════════════════════════════════════
# KISS Discovery Engine
# ══════════════════════════════════════════════════════════════════════════════

class KISS:
    """
    KISS Discovery Engine — brute-force code generation + verification.

    Two modes:
      1. Subprocess (default): runs KISS engine directly
      2. MCP (when mcporter is available): calls KISS MCP server tools

    Environment variables for API keys (any one suffices):
      MERCURY_API_KEY, OPENROUTER_API_KEY, OLLAMA_API_KEY, MISTRAL_API_KEY
    """

    # Supported topics
    TOPICS = [
        "python_code", "javascript_code", "sql_queries",
        "number_theory", "combinatorics", "graph_algorithms",
        "optimization", "data_analysis", "machine_learning",
        "bioinformatics", "chemistry", "physics",
        "mathematics", "statistics", "algorithm_design",
        "testing", "automation", "brainstorm",
    ]

    API_KEYS = ["MERCURY_API_KEY", "OPENROUTER_API_KEY", "OLLAMA_API_KEY", "MISTRAL_API_KEY"]

    @classmethod
    def _check_binary(cls) -> str | None:
        """Checks prerequisites. Returns error message or None."""
        if not KISS_DIR.exists():
            return f"KISS not found at {KISS_DIR}"
        if not KISS_ENGINE_ENTRY.exists():
            return f"KISS engine not found at {KISS_ENGINE_ENTRY}"
        for key in cls.API_KEYS:
            if os.environ.get(key):
                return None
        return f"No API key set. Need one of: {cls.API_KEYS}"

    # ── Direct engine (subprocess) ─────────────────────────────────────────

    @classmethod
    def generate(
        cls,
        prompt: str,
        topic: str = "python_code",
        variants: int = 10,
        temperature: float = 0.85,
        db_path: str | None = None,
    ) -> dict:
        """
        Generate and verify code variants via KISS engine.

        Args:
            prompt: what the code should do
            topic: domain (python_code, bioinformatics, chemistry, etc.)
            variants: number of variants to generate
            temperature: creativity (0.0-2.0)
            db_path: custom SQLite ledger path (optional)

        Returns:
            dict with candidates, each having:
              - candidate: the generated code
              - status: pass/fail
              - feedback: verifier feedback
              - execution_time_ms: sandbox execution time
        """
        err = cls._check_binary()
        if err:
            return {"success": False, "error": err}

        cmd = [
            "python", "-m", "src.engine",
            "--prompt", prompt,
            "--topic", topic,
            "--variants", str(variants),
        ]
        if db_path:
            cmd += ["--db-path", db_path]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=600, cwd=str(KISS_DIR)
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout[-2000:] if result.stdout else "",
                "stderr": result.stderr[-500:] if result.stderr else "",
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout (>10min)"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def verify(cls, code: str, topic: str = "python_code") -> dict:
        """Verify a single code snippet."""
        err = cls._check_binary()
        if err:
            return {"success": False, "error": err}

        tmp = Path(tempfile.mktemp(suffix=".py"))
        tmp.write_text(code)
        try:
            result = subprocess.run(
                ["python", "-c", f"""
import asyncio, json, sys
sys.path.insert(0, '{KISS_DIR}')
from src.engine import KissDiscoveryEngine

async def main():
    engine = KissDiscoveryEngine(db_path='{KISS_LEDGER}')
    result = await engine.expand_seed(
        seed={{'candidate': open('{tmp}').read()}},
        topic_name='{topic}',
    )
    print(json.dumps(result))

asyncio.run(main())
"""],
                capture_output=True, text=True, timeout=120,
            )
            if result.returncode == 0 and result.stdout.strip():
                return {"success": True, **json.loads(result.stdout.strip())}
            return {"success": False, "error": result.stderr[:500]}
        finally:
            tmp.unlink(missing_ok=True)

    # ── MCP tools (for use from any MCP-compatible agent) ──────────────────

    @classmethod
    def mcp_start_command(cls) -> str:
        """Returns the command to start the KISS MCP server."""
        return f"python {KISS_MCP_ENTRY}"

    @classmethod
    def mcp_tool_names(cls) -> list[str]:
        """Returns the MCP tool names exposed by KISS."""
        return [
            "brainstorm", "record_feedback", "list_verifiers",
            "get_verifier", "get_run", "list_recent_runs", "health",
        ]

    # ── Ledger ──────────────────────────────────────────────────────────────

    @classmethod
    def query_ledger(
        cls,
        topic: str | None = None,
        status: str | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """Query the KISS execution ledger."""
        if not KISS_LEDGER.exists():
            return []

        try:
            conn = sqlite3.connect(str(KISS_LEDGER))
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM executions WHERE 1=1"
            params: list[Any] = []
            if topic:
                query += " AND topic = ?"
                params.append(topic)
            if status:
                query += " AND status = ?"
                params.append(status)
            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            rows = conn.execute(query, params).fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            return [{"error": str(e)}]


# ══════════════════════════════════════════════════════════════════════════════
# DGM — Darwin Gödel Machine (generic code evolution)
# ══════════════════════════════════════════════════════════════════════════════

class DGM:
    """
    Darwin Gödel Machine — generic code evolution engine.

    Evolves code via LLM-guided mutation + empirical validation.
    Requires Docker + API key (OpenAI or Anthropic).

    Agnostic: works with any script in any repo.

    Usage:
        DGM.evolve(script_path="./train.py", metric="val_accuracy")
        DGM.evolve(script_path="./analysis.py", metric="f1_score", generations=10)
    """

    REQUIRED_ENV = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]

    @classmethod
    def _check_binary(cls) -> str | None:
        if not DGM_DIR.exists():
            return f"DGM not found at {DGM_DIR}"
        if not DGM_ENTRY.exists():
            return f"DGM entry not found at {DGM_ENTRY}"
        try:
            r = subprocess.run(
                ["docker", "info"], capture_output=True, text=True, timeout=10
            )
            if r.returncode != 0:
                return "Docker not available"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return "Docker not installed"
        for key in cls.REQUIRED_ENV:
            if os.environ.get(key):
                return None
        return f"No API key. Need one of: {cls.REQUIRED_ENV}"

    @classmethod
    def evolve(
        cls,
        script_path: str,
        metric: str = "score",
        output_dir: str | None = None,
        generations: int = 5,
    ) -> dict:
        """
        Evolve a script to improve a metric.

        Args:
            script_path: path to the script to evolve
            metric: name of the metric function in the script
            output_dir: directory for intermediate results
            generations: number of evolution generations

        Returns:
            dict with best_code, best_score, generation_history
        """
        err = cls._check_binary()
        if err:
            return {"success": False, "error": err}

        script = Path(script_path)
        if not script.exists():
            return {"success": False, "error": f"Script not found: {script_path}"}

        out = Path(output_dir) if output_dir else Path(tempfile.mkdtemp(prefix="dgm_"))
        out.mkdir(parents=True, exist_ok=True)

        # Prepare initial agent
        initial_dir = out / "initial"
        initial_dir.mkdir(exist_ok=True)
        shutil.copy2(script, initial_dir / script.name)

        # Write TASK.md with instructions
        (initial_dir / "TASK.md").write_text(f"""
# Task: Improve this code

Metric to optimize: {metric}

Current script: {script.name}

## Instructions
Improve the code meaningfully. Possible directions:
- Make it more efficient (faster, less memory)
- Handle edge cases
- Improve accuracy of {metric}
- Add error handling
- Make it more general or reusable

## Evaluation
The metric function `{metric}(output) -> float` will be called.
Higher scores are better (0.0 = fails, 1.0 = perfect).
""")

        cmd = [
            "python", str(DGM_ENTRY),
            "--output-dir", str(out),
            "--selfimprove-size", str(generations),
            "--method", "random",
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=7200, cwd=str(DGM_DIR)
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout[-1000:] if result.stdout else "",
                "stderr": result.stderr[-500:] if result.stderr else "",
                "output_dir": str(out),
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout (>2h)"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def run_evolution(
        cls,
        output_dir: str,
        prevrun_dir: str | None = None,
        polyglot: bool = False,
        selfimprove_size: int = 4,
        method: str = "random",
    ) -> dict:
        """Run a full DGM evolution (advanced usage)."""
        err = cls._check_binary()
        if err:
            return {"success": False, "error": err}

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

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=7200, cwd=str(DGM_DIR)
            )
            return {
                "success": result.returncode == 0,
                "output_dir": output_dir,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout (>2h)"}


# ══════════════════════════════════════════════════════════════════════════════
# Evolution — KISS + DGM combined
# ══════════════════════════════════════════════════════════════════════════════

class Evolution:
    """
    KISS + DGM combined evolution loop.

    1. KISS generates seed population
    2. Fitness function scores each candidate (KISS verifier by default)
    3. DGM mutates the best candidates via LLM
    4. Repeat for N generations

    Agnostic: works with any prompt, any topic, any repo.
    """

    @classmethod
    def run(
        cls,
        prompt: str,
        topic: str = "python_code",
        variants: int = 20,
        generations: int = 5,
        temperature: float = 0.85,
        fitness_func: Callable[[str], float] | None = None,
        output_dir: str | None = None,
    ) -> dict:
        """
        Full evolution loop.

        Args:
            prompt: what code to evolve
            topic: domain for KISS
            variants: seed population size
            generations: number of evolution rounds
            temperature: mutation creativity
            fitness_func: custom fitness function (default: KISS verifier pass/fail)
            output_dir: directory for results

        Returns:
            dict with best_code, best_score, generation_history
        """
        out = Path(output_dir) if output_dir else Path(tempfile.mkdtemp(prefix="kiss_dgm_"))
        out.mkdir(parents=True, exist_ok=True)

        history = []
        total_evaluated = 0

        # Phase 1: KISS generates seeds
        print(f"[Evolution] Phase 1: generating {variants} seeds with KISS...")
        seed_result = KISS.generate(prompt, topic, variants, temperature)
        if not seed_result["success"]:
            return {"success": False, "error": seed_result.get("error")}

        # Parse seeds
        candidates = []
        for line in seed_result.get("stdout", "").strip().split("\n"):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                candidates.append(data)
            except json.JSONDecodeError:
                candidates.append({"candidate": line.strip(), "status": "raw"})

        print(f"[Evolution] KISS generated {len(candidates)} candidates")

        # Phase 2: Score seed population
        print(f"[Evolution] Phase 2: scoring seed population...")
        evaluated = []
        for cand in candidates:
            code = cand.get("candidate", "")
            if not code:
                continue

            if fitness_func:
                score = fitness_func(code)
            else:
                v = KISS.verify(code, topic)
                score = 1.0 if v.get("status") == "pass" else 0.0

            evaluated.append({"code": code, "score": score, "generation": 0})
            total_evaluated += 1

        if not evaluated:
            return {"success": False, "error": "No valid candidates generated"}

        best = max(evaluated, key=lambda x: x["score"])
        history.append({
            "generation": 0,
            "population_size": len(evaluated),
            "best_score": best["score"],
        })
        print(f"[Evolution] Best seed: score={best['score']:.3f}")

        # Phase 3: DGM-style evolution
        for gen in range(1, generations + 1):
            print(f"[Evolution] Generation {gen}/{generations}...")

            parents = evaluated[: max(2, len(evaluated) // 2)]

            # Mutate: ask KISS to improve each parent
            mutated = []
            for parent in parents:
                mutation_prompt = f"""Improve this {topic} code. Make one meaningful change.

Code:
```python
{parent['code']}
```
Output ONLY the improved code, no explanations."""
                mut_result = KISS.generate(mutation_prompt, topic, variants=2, temperature=temperature)
                if mut_result["success"]:
                    for line in mut_result.get("stdout", "").strip().split("\n"):
                        if line.strip():
                            try:
                                mutated.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass

            # Score mutations
            for mut in mutated:
                code = mut.get("candidate", "")
                if not code or len(code) < 10:
                    continue
                if fitness_func:
                    score = fitness_func(code)
                else:
                    v = KISS.verify(code, topic)
                    score = 1.0 if v.get("status") == "pass" else 0.0
                evaluated.append({"code": code, "score": score, "generation": gen})
                total_evaluated += 1

            # Select best
            evaluated.sort(key=lambda x: x["score"], reverse=True)
            evaluated = evaluated[: variants]
            current_best = evaluated[0]

            if current_best["score"] > best["score"]:
                best = current_best
                print(f"[Evolution] New best! score={best['score']:.3f} (gen {gen})")

            history.append({
                "generation": gen,
                "population_size": len(evaluated),
                "best_score": best["score"],
                "mutations_tried": len(mutated),
            })

        result = {
            "success": True,
            "best_code": best["code"],
            "best_score": best["score"],
            "best_generation": best["generation"],
            "generation_history": history,
            "total_evaluated": total_evaluated,
            "output_dir": str(out),
        }

        (out / "result.json").write_text(json.dumps(result, indent=2, default=str))
        (out / "best_code.py").write_text(best["code"])

        print(f"[Evolution] Done. Best score={best['score']:.3f} after {total_evaluated} evaluations")
        return result


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="KISS + DGM — Agnostic code evolution tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # KISS: generate 10 Python sorting functions
  %(prog)s kiss generate --prompt "sort a list" --topic python_code --variants 10

  # KISS: verify a code snippet
  %(prog)s kiss verify --code "def sort(lst): return sorted(lst)" --topic python_code

  # DGM: evolve a script
  %(prog)s dgm evolve --script ./train.py --metric val_accuracy --generations 5

  # Combined: KISS seeds + evolution
  %(prog)s evolve --prompt "fast matrix multiplication" --generations 5 --variants 20

  # KISS MCP: start server (for any MCP client)
  %(prog)s kiss mcp
        """,
    )

    sub = parser.add_subparsers(dest="tool")

    # ── kiss ──────────────────────────────────────────────────────────────
    kiss_parser = sub.add_parser("kiss", help="KISS Discovery Engine")
    kiss_sub = kiss_parser.add_subparsers(dest="action")

    gen = kiss_sub.add_parser("generate", help="Generate code variants")
    gen.add_argument("--prompt", required=True)
    gen.add_argument("--topic", default="python_code")
    gen.add_argument("--variants", type=int, default=10)
    gen.add_argument("--temperature", type=float, default=0.85)

    ver = kiss_sub.add_parser("verify", help="Verify code")
    ver.add_argument("--code", required=True)
    ver.add_argument("--topic", default="python_code")

    mcp = kiss_sub.add_parser("mcp", help="Start MCP server")
    mcp.add_argument("--transport", default="stdio", choices=["stdio", "http"])

    # ── dgm ───────────────────────────────────────────────────────────────
    dgm_parser = sub.add_parser("dgm", help="Darwin Gödel Machine")
    dgm_sub = dgm_parser.add_subparsers(dest="action")

    evo = dgm_sub.add_parser("evolve", help="Evolve a script")
    evo.add_argument("--script", required=True)
    evo.add_argument("--metric", default="score")
    evo.add_argument("--generations", type=int, default=5)
    evo.add_argument("--output-dir")

    # ── evolve ────────────────────────────────────────────────────────────
    ce = sub.add_parser("evolve", help="KISS + DGM combined evolution")
    ce.add_argument("--prompt", required=True)
    ce.add_argument("--topic", default="python_code")
    ce.add_argument("--variants", type=int, default=20)
    ce.add_argument("--generations", type=int, default=5)
    ce.add_argument("--temperature", type=float, default=0.85)
    ce.add_argument("--output-dir")

    args = parser.parse_args()

    if args.tool == "kiss":
        if args.action == "generate":
            result = KISS.generate(args.prompt, args.topic, args.variants, args.temperature)
            print(json.dumps(result, indent=2))
        elif args.action == "verify":
            result = KISS.verify(args.code, args.topic)
            print(json.dumps(result, indent=2))
        elif args.action == "mcp":
            cmd = ["python", str(KISS_MCP_ENTRY)]
            if args.transport == "http":
                cmd += ["--transport", "http"]
            os.execvp(cmd[0], cmd)

    elif args.tool == "dgm":
        if args.action == "evolve":
            result = DGM.evolve(
                args.script, args.metric,
                output_dir=args.output_dir,
                generations=args.generations,
            )
            print(json.dumps(result, indent=2))

    elif args.tool == "evolve":
        result = Evolution.run(
            args.prompt, args.topic,
            variants=args.variants,
            generations=args.generations,
            temperature=args.temperature,
            output_dir=args.output_dir,
        )
        print(json.dumps(result, indent=2, default=str))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
