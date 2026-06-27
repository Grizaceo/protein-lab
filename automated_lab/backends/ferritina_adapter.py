#!/usr/bin/env python3
"""
automated_lab/backends/ferritina_adapter.py
============================================
Adapter del automated_lab para la investigación ferritina-biomaterial (1BFR).

Provee:
  - Target paths para PDBs de ferritina (1BFR, mutantes)
  - Config de scopes (A/B/C) para iteración
  - Parámetros de mutación y validación de diseño
  - Verificación de gaps interficiales (A-B subunit)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# Raíz del repositorio protein-lab
LAB_DIR = Path(__file__).resolve().parent.parent.parent

# Raíz de la investigación
INVESTIGATION_DIR = LAB_DIR / "investigaciones" / "ferritina-biomaterial"
SCRIPTS_DIR = INVESTIGATION_DIR / "scripts"
DATA_DIR = INVESTIGATION_DIR / "data"


class FerritinaAdapter:
    """Adapter para experimentos de diseño de ferritina/biomaterial."""

    INVESTIGATION_NAME = "ferritina-biomaterial"

    # Paths de datos principales
    PDB_1BFR = DATA_DIR / "pdb" / "new_chassis" / "1BFR.pdb"
    PDB_1BFR_MUTANT_A = DATA_DIR / "pdb" / "new_chassis" / "1BFR_mutant_A.pdb"
    PDB_1WAD = DATA_DIR / "pdb" / "new_chassis" / "1WAD.pdb"

    # Scripts principales por categoría
    SCRIPTS = {
        # Diseño y mutación
        "design_core": SCRIPTS_DIR / "design_ferritin_core.py",
        "audit_v4": SCRIPTS_DIR / "audit_v4_real.py",
        "audit_synapse": SCRIPTS_DIR / "audit_synapse.py",
        "geometry_cys": SCRIPTS_DIR / "geometry_cys_rotamer.py",
        "clash_check": SCRIPTS_DIR / "clash_check_leu40.py",
        "conservation": SCRIPTS_DIR / "conservation_analysis.py",
        "optimize_core": SCRIPTS_DIR / "optimize_core.py",

        # Hopping / electron transfer
        "hopping_graph": SCRIPTS_DIR / "SCOPE_C_HOPPING_GRAPH.py",
        "real_geometry": SCRIPTS_DIR / "SCOPE_C_REAL_GEOMETRY.py",
        "relay_network": SCRIPTS_DIR / "SCOPE_C_RELAY_NETWORK.py",
        "redox_correction": SCRIPTS_DIR / "au_np_redox_correction.py",
        "tropical_metrics": SCRIPTS_DIR / "tropical_metrics.py",

        # Búsqueda de sitios
        "find_docking": SCRIPTS_DIR / "find_docking_ports.py",
        "find_mutation": SCRIPTS_DIR / "find_mutation_point_v2.py",
        "find_manifold": SCRIPTS_DIR / "find_manifold.py",
        "find_deep_port": SCRIPTS_DIR / "find_deep_port.py",

        # Simulación / bridges
        "simulate_bridge": SCRIPTS_DIR / "simulate_bridge_v2.py",
        "sandwich": SCRIPTS_DIR / "sandwich_test.py",

        # IA/LLM review
        "moe_review": SCRIPTS_DIR / "moe_review.py",

        # Scopes paper
        "scope_a": INVESTIGATION_DIR / "docs" / "SCOPE_A_MINIMAL.md",
        "scope_b_paper": INVESTIGATION_DIR / "docs" / "SCOPE_B_PAPER_OUTLINE.md",
        "scope_c": INVESTIGATION_DIR / "docs" / "SCOPE_C_NUMERIC_BIOSENSOR.md",
    }

    # Targets para diseño de ferritina
    TARGETS = {
        "1BFR": {
            "pdb": PDB_1BFR,
            "description": "Bacterioferritin wild-type (E. coli), 24-mer",
            "chain_focus": "A",
            "key_residues": [40, 49],  # LEU40, ILE49
            "unit_cells": 4,  # subunidades A-B interfase
        },
        "1BFR_mutant_A": {
            "pdb": PDB_1BFR_MUTANT_A,
            "description": "1BFR con mutación LEU40→CYS en chain A",
            "chain_focus": "A",
            "mutations": ["LEU40CYS"],
        },
    }

    @classmethod
    def resolve_script(cls, name: str) -> Path | None:
        """Resuelve path de un script por nombre."""
        script = cls.SCRIPTS.get(name)
        if script and script.exists():
            return script
        return None

    @classmethod
    def resolve_data(cls, name: str) -> Path | None:
        """Resuelve path de un archivo de datos por nombre."""
        target = cls.TARGETS.get(name)
        if target and target["pdb"].exists():
            return target["pdb"]
        return None

    @classmethod
    def get_target_config(cls, target: str) -> dict[str, Any]:
        """Retorna configuración de un target."""
        return cls.TARGETS.get(target, {}).copy()

    @classmethod
    def validate_paths(cls) -> dict[str, bool]:
        """Valida que existan los paths críticos."""
        docs_dir = INVESTIGATION_DIR / "docs"
        return {
            "scripts_dir": SCRIPTS_DIR.exists(),
            "data_dir": DATA_DIR.exists(),
            "pdb_1bfr": cls.PDB_1BFR.exists(),
            "docs_dir": docs_dir.exists(),
        }

    @classmethod
    def summary(cls) -> str:
        """Resumen del estado del adapter."""
        checks = cls.validate_paths()
        lines = [
            f"=== Ferritina Adapter ===",
            f"Investigación: {cls.INVESTIGATION_NAME}",
            f"Scripts: {len([s for s in cls.SCRIPTS.values() if s.exists()])}/{len(cls.SCRIPTS)} encontrados",
            f"Targets: {len(cls.TARGETS)} configurados",
        ]
        for k, v in checks.items():
            status = "OK" if v else "MISSING"
            lines.append(f"  {k}: {status}")
        return "\n".join(lines)
