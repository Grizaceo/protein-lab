#!/usr/bin/env python3
"""
automated_lab/backends/local_mammal.py
======================================
Backend de ejecución local para MAMMAL (RTX 4060).
Ejecuta experimentos en lote vía subprocess con conda Python,
cargando el modelo UNA SOLA VEZ por lote.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

CONDA_PYTHON = os.getenv("PROTEIN_LAB_PYTHON", "/home/gris/.miniconda/envs/protein-lab/bin/python")
RUNNER_SCRIPT = str(Path(__file__).resolve().parent / "_run_dti.py")


class LocalMammalBackend:
    """Ejecuta experimentos MAMMAL DTI en lote (1 carga de modelo por batch)."""

    def supports(self, experiment_type: str) -> bool:
        return experiment_type in {"dti_pkd", "binding_class"}

    def estimate_time(self, experiment: dict) -> float:
        seq_len = len(experiment.get("target_seq", ""))
        return 0.2 + seq_len * 0.001

    def _preflight_error(self) -> str | None:
        if not Path(CONDA_PYTHON).exists():
            return f"Protein-lab Python not found: {CONDA_PYTHON}"
        if not Path(RUNNER_SCRIPT).exists():
            return f"DTI runner not found: {RUNNER_SCRIPT}"
        return None

    def run(self, experiment: dict) -> dict:
        results = self.run_batch([experiment])
        return results[0] if results else {"status": "error", "error": "empty result"}

    def run_batch(self, experiments: list[dict]) -> list[dict]:
        if not experiments:
            return []
        preflight = self._preflight_error()
        if preflight:
            return [{"status": "error", "error": preflight} for _ in experiments]

        batch_input = {"experiments": []}
        for exp in experiments:
            batch_input["experiments"].append({
                "type": exp.get("type", "dti_pkd"),
                "target_seq": exp.get("target_seq", ""),
                "drug_smiles": exp.get("drug_smiles", ""),
            })

        timeout_s = int(os.getenv("MAMMAL_BATCH_TIMEOUT", "600"))
        t0 = time.time()
        try:
            result = subprocess.run(
                [CONDA_PYTHON, RUNNER_SCRIPT],
                input=json.dumps(batch_input),
                capture_output=True,
                text=True,
                timeout=timeout_s,
            )
        except subprocess.TimeoutExpired:
            return [{"status": "error", "error": f"MAMMAL batch timeout after {timeout_s}s"} for _ in experiments]
        elapsed = time.time() - t0

        if result.returncode != 0:
            err = (result.stderr.strip() or result.stdout.strip())[-4000:]
            return [{"status": "error", "error": err, "elapsed_s": round(elapsed, 2)} for _ in experiments]

        try:
            stdout = result.stdout
            marker = "__MAMMAL_RESULT__"
            json_str = stdout[stdout.index(marker) + len(marker):].strip() if marker in stdout else stdout.strip()
            outputs = json.loads(json_str)
            if not isinstance(outputs, list):
                raise ValueError("runner returned non-list JSON")
            normalized = []
            for i, exp in enumerate(experiments):
                out: dict[str, Any] = outputs[i] if i < len(outputs) and isinstance(outputs[i], dict) else {"status": "error", "error": "missing runner output"}
                out["elapsed_s"] = round(elapsed, 2)
                out["drug_name"] = exp.get("drug_name", "")
                out["target"] = exp.get("target", "")
                normalized.append(out)
            return normalized
        except Exception as e:
            return [{"status": "error", "error": f"JSON parse: {e}; stdout_tail={result.stdout[-1000:]}"} for _ in experiments]
