#!/usr/bin/env python3
"""
automated_lab/backends/colab_bridge.py
=======================================
Bridge al loop viejo de Colab (RFdiffusion, per-residue embeddings, Nav1.8).
Lee ITERATION_STATE.json, detecta nuevos ZIPs, registra corridas.

Esto es un wrapper alrededor de lab_iterate.py existente.
"""

import sys, os, json, subprocess
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(LAB_DIR / "src"))


class ColabBridge:
    """Puente al loop de RFdiffusion/Colab existente."""

    def __init__(self):
        self.lab_dir = str(LAB_DIR)
        self.iteration_state = Path(self.lab_dir) / "colab_runs" / "ITERATION_STATE.json"
        self.state = {}

    def load_state(self):
        if self.iteration_state.exists():
            self.state = json.loads(self.iteration_state.read_text())
        return self.state

    def supports(self, experiment_type: str) -> bool:
        return experiment_type in {
            "rfdiffusion",       # Binder design
            "colabfold_multimer",# Complex validation
            "per_residue_esm2", # Per-residue embeddings (colab)
            "docking_gnina",    # Docking (si se configura)
        }

    def estimate_time(self, experiment: dict) -> float:
        return 3600  # Colab runs ~1h

    def run(self, experiment: dict) -> dict:
        """Genera instrucciones y PDBs para Colab."""
        target = experiment.get("target", "nipah")
        params = experiment.get("params", {})

        # Load state to get target_info
        from iteration.state_manager import load_state, get_target
        state = load_state()
        target_info = get_target(state, target)
        
        strategy = experiment.get("strategy", "explore")
        rationale_text = experiment.get("rationale", "EaC Bridged Exploration")

        # Usar colab_prep existente
        from iteration.colab_prep import prepare_next_run
        result = prepare_next_run(
            target_name=target,
            target_info=target_info,
            params=params,
            strategy=strategy,
            rationale_text=rationale_text
        )

        return {
            "status": "pending_manual",
            "message": f"Colab run preparada en next_run/{target}/",
            "instructions_file": str(Path(self.lab_dir) / "next_run" / target / "COLAB_INSTRUCTIONS.md"),
            "config_file": str(Path(self.lab_dir) / "next_run" / target / "colab_config.json"),
        }

    def process_zip(self, zip_path: str) -> dict:
        """Procesa un ZIP descargado de Colab."""
        from iteration.run_analyzer import analyze_run_folder
        from iteration.state_manager import register_run, load_state, save_state

        state = load_state()
        run_id = analyze_run_folder(str(zip_path))
        if run_id:
            register_run(state, run_id)
            save_state(state)
            return {"status": "ok", "run_id": run_id}
        return {"status": "error", "error": f"Could not process {zip_path}"}
