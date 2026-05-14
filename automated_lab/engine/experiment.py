#!/usr/bin/env python3
"""
automated_lab/engine/experiment.py
==================================
Ejecutor de experimentos individuales/lotes.
"""

from __future__ import annotations

import json
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(LAB_DIR / "automated_lab"))
sys.path.insert(0, str(LAB_DIR / "src"))


class ExperimentRunner:
    """Ejecuta experimentos seleccionando automáticamente el backend."""

    def __init__(self):
        self.backends = {}
        self._register_backends()

    def _register_backends(self):
        try:
            from backends.local_mammal import LocalMammalBackend
            self.backends["local_mammal"] = LocalMammalBackend()
        except ImportError as e:
            print(f"[experiment] ⚠ local_mammal no disponible: {e}")
        try:
            from backends.colab_bridge import ColabBridge
            self.backends["colab_bridge"] = ColabBridge()
        except ImportError as e:
            print(f"[experiment] ⚠ colab_bridge no disponible: {e}")

    def select_backend(self, experiment: dict) -> str:
        exp_type = experiment.get("type", "")
        backend_map = {
            "dti_pkd": "local_mammal",
            "binding_class": "local_mammal",
            "protein_solubility": "local_mammal",
            "rfdiffusion": "colab_bridge",
            "colabfold_multimer": "colab_bridge",
            "per_residue_esm2": "colab_bridge",
        }
        preferred = backend_map.get(exp_type)
        if preferred and preferred in self.backends:
            return preferred
        for name, backend in self.backends.items():
            if hasattr(backend, "supports") and backend.supports(exp_type):
                return name
        raise ValueError(f"No backend available for experiment type: {exp_type}")

    def _write_result(self, experiment: dict, result: dict, results_dir: Path | None) -> None:
        if not results_dir:
            return
        results_dir.mkdir(parents=True, exist_ok=True)
        out = results_dir / f"{experiment['id']}.json"
        with open(out, "w") as f:
            json.dump({"experiment": experiment, "result": result}, f, indent=2, ensure_ascii=False)

    def run(self, experiment: dict, results_dir: Path | None = None) -> dict:
        if "id" not in experiment or not experiment["id"]:
            experiment["id"] = f"exp_{uuid.uuid4().hex[:8]}"
        backend_name = self.select_backend(experiment)
        backend = self.backends[backend_name]
        print(f"[experiment] {experiment['id']} → {backend_name} ({experiment.get('type')})")
        estimated = backend.estimate_time(experiment) if hasattr(backend, "estimate_time") else 60
        print(f"[experiment]   Tiempo estimado: {estimated:.1f}s")
        t0 = time.time()
        try:
            result = backend.run(experiment)
            elapsed = time.time() - t0
            result.setdefault("elapsed_s", round(elapsed, 2))
            result["backend"] = backend_name
            result["experiment_id"] = experiment["id"]
            result["timestamp"] = datetime.now().isoformat()
            self._write_result(experiment, result, results_dir)
            return result
        except Exception as e:
            elapsed = time.time() - t0
            print(f"[experiment]   ❌ Error tras {elapsed:.1f}s: {e}")
            result = {
                "status": "error",
                "experiment_id": experiment["id"],
                "backend": backend_name,
                "elapsed_s": round(elapsed, 2),
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
            self._write_result(experiment, result, results_dir)
            return result

    def run_batch(self, experiments: list[dict], results_dir: Path | None = None,
                  sequential: bool = True) -> list[dict]:
        if not experiments:
            return []

        # Group by backend so mixed future queues do not accidentally send all work
        # to the first experiment's backend.
        grouped: dict[str, list[dict]] = {}
        for exp in experiments:
            if "id" not in exp or not exp["id"]:
                exp["id"] = f"exp_{uuid.uuid4().hex[:8]}"
            grouped.setdefault(self.select_backend(exp), []).append(exp)

        all_results: list[dict] = []
        for backend_name, batch in grouped.items():
            backend = self.backends[backend_name]
            batch_run = getattr(backend, "run_batch", None)
            if batch_run and not sequential:
                print(f"[experiment] Batch: {len(batch)} experimentos → {backend_name}")
                t0 = time.time()
                results = batch_run(batch)
                elapsed = round(time.time() - t0, 2)
                for exp, res in zip(batch, results):
                    res.setdefault("elapsed_s", elapsed)
                    res["backend"] = backend_name
                    res["experiment_id"] = exp["id"]
                    res["timestamp"] = datetime.now().isoformat()
                    self._write_result(exp, res, results_dir)
                    all_results.append(res)
                continue

            for i, exp in enumerate(batch):
                print(f"\n[experiment] --- [{i+1}/{len(batch)}] ---")
                all_results.append(self.run(exp, results_dir))
        return all_results
