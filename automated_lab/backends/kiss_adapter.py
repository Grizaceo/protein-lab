#!/usr/bin/env python3
"""
automated_lab/backends/kiss_adapter.py
=======================================
Adapter del automated_lab para KISS Discovery Engine.

KISS tiene dos motores:
  1. Code brute-force engine: genera N variantes de código en paralelo,
     las verifica en sandbox, y guarda las que pasan en SQLite.
  2. Brainstorm MCP server: generación rápida de ideas sobre cualquier
     tema, expuesto como MCP tools.

Uso en protein-lab:
  - Generar múltiples variantes de scripts de análisis
  - Brainstorming de hipótesis experimentales
  - Verificación automática de código generado
"""

from __future__ import annotations

import os
import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent.parent.parent
KISS_DIR = Path("/home/gris96/.hermes/workspace/repos/kiss_discovery_engine")

# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

KISS_ENGINE_ENTRY = KISS_DIR / "src" / "engine.py"
KISS_MCP_ENTRY = KISS_DIR / "src" / "mcp_server.py"
KISS_LEDGER = KISS_DIR / "artifacts" / "ledger.db"

# Topics soportados por el engine
KISS_TOPICS = [
    "python_code",
    "javascript_code",
    "sql_queries",
    "number_theory",
    "combinatorics",
    "graph_algorithms",
    "optimization",
    "data_analysis",
    "machine_learning",
    "bioinformatics",
    "chemistry",
    "physics",
    "mathematics",
    "statistics",
    "algorithm_design",
    "testing",
    "automation",
    "brainstorm",
]

# API keys soportados
KISS_API_KEYS=["MERC...EY", "OPENROUTER_API_KEY", "OLLAMA_API_KEY", "MISTRAL_API_KEY"]


# ══════════════════════════════════════════════════════════════════════════════
# Adapter
# ══════════════════════════════════════════════════════════════════════════════

class KISSAdapter:
    """Adapter para KISS Discovery Engine."""

    PROVIDER_NAME = "kiss"

    @classmethod
    def check_prerequisites(cls) -> dict:
        """Verifica que KISS esté instalado y configurado."""
        result = {
            "kiss_installed": False,
            "api_key_set": False,
            "ledger_exists": False,
            "mcp_available": False,
            "ready": False,
            "errors": [],
        }

        # Verificar repo
        if KISS_DIR.exists() and KISS_ENGINE_ENTRY.exists():
            result["kiss_installed"] = True
        else:
            result["errors"].append(f"KISS no encontrado en {KISS_DIR}")

        # Verificar API key
        for var in KISS_API_KEYS:
            if os.environ.get(var):
                result["api_key_set"] = True
                break
        if not result["api_key_set"]:
            result["errors"].append(f"Falta API key. Definir una de: {KISS_API_KEYS}")

        # Verificar ledger
        result["ledger_exists"] = KISS_LEDGER.exists()

        # Verificar MCP server
        result["mcp_available"] = KISS_MCP_ENTRY.exists()

        result["ready"] = result["kiss_installed"] and result["api_key_set"]
        return result

    @classmethod
    def brute_force(
        cls,
        prompt: str,
        topic: str = "python_code",
        variants: int = 10,
        db_path: str | None = None,
    ) -> dict:
        """
        Genera y verifica múltiples variantes de código.

        Args:
            prompt: descripción de lo que debe hacer el código
            topic: dominio (python_code, sql_queries, etc.)
            variants: número de variantes a generar
            db_path: path al ledger SQLite (opcional)

        Returns:
            dict con las variantes generadas y su estado
        """
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
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
                cwd=str(KISS_DIR),
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
    def brainstorm(
        cls,
        prompt: str,
        n: int = 10,
        temperature: float = 0.9,
        constraints: str | None = None,
        verifier_id: str | None = None,
        skip_verifier: bool = False,
    ) -> dict:
        """
        Genera N ideas diversas sobre un tema vía MCP.

        Este método invoca el MCP server de KISS como subprocess.
        Para uso interactivo, es mejor conectar el MCP server directamente.

        Args:
            prompt: tema sobre el que brainstormear
            n: número de ideas
            temperature: creatividad (0.0-1.0)
            constraints: restricciones opcionales
            verifier_id: ID de verificador pre-guardado
            skip_verifier: saltar verificación

        Returns:
            dict con las ideas generadas
        {
            "status": "pending_mcp",
            "message": "Conectar MCP server para brainstorming",
            "mcp_entry": str,
            "suggested_prompt": str,
        }
        """
        return {
            "status": "pending_mcp",
            "message": "KISS brainstorm requiere conexión MCP directa",
            "mcp_entry": str(KISS_MCP_ENTRY),
            "suggested_prompt": prompt,
            "n": n,
            "temperature": temperature,
            "constraints": constraints,
            "verifier_id": verifier_id,
            "skip_verifier": skip_verifier,
            "start_command": f"fastmcp run {KISS_MCP_ENTRY}:mcp --transport stdio",
        }

    @classmethod
    def query_ledger(
        cls,
        topic: str | None = None,
        status: str | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """
        Consulta el ledger de ejecuciones pasadas.

        Args:
            topic: filtrar por topic
            status: filtrar por status (pass/fail)
            limit: máximo de resultados

        Returns:
            lista de registros del ledger
        """
        if not KISS_LEDGER.exists():
            return []

        db_path = str(KISS_LEDGER)
        try:
            conn = sqlite3.connect(db_path)
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

    @classmethod
    def list_topics(cls) -> list[str]:
        """Lista los topics soportados."""
        return KISS_TOPICS

    @classmethod
    def summary(cls) -> str:
        """Resumen del estado del adapter."""
        checks = cls.check_prerequisites()
        lines = [
            "=== KISS Discovery Engine Adapter ===",
            f"KISS: {'OK' if checks['kiss_installed'] else 'MISSING'}",
            f"API Key: {'OK' if checks['api_key_set'] else 'MISSING'}",
            f"Ledger: {'OK' if checks['ledger_exists'] else 'MISSING'}",
            f"MCP Server: {'OK' if checks['mcp_available'] else 'MISSING'}",
            f"Topics: {len(KISS_TOPICS)}",
        ]
        if checks["errors"]:
            lines.append(f"Errores: {', '.join(checks['errors'])}")
        return "\n".join(lines)
