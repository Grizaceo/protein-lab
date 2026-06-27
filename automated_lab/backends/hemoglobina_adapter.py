#!/usr/bin/env python3
"""
automated_lab/backends/hemoglobina_adapter.py
==============================================
Adapter del automated_lab para la investigación hemoglobina-mtr (exp01).

Provee:
  - Target paths para MtrF, MtrA, MtrC, MtrB (sistema de transporte de electrones)
  - Config del experimento ELP/MtrF/CsgA
  - Parámetros para análisis de circuitos de hierro-sulfuro
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent.parent.parent
INVESTIGATION_DIR = LAB_DIR / "investigaciones" / "hemoglobina-mtr"
SCRIPTS_DIR = INVESTIGATION_DIR / "scripts"
DATA_DIR = INVESTIGATION_DIR / "data"


class HemoglobinaAdapter:
    """Adapter para experimentos de hemoglobina/Mtr."""

    INVESTIGATION_NAME = "hemoglobina-mtr"

    # Paths de datos principales
    MTRF_PDB = DATA_DIR / "pdb" / "MtrF.pdb"
    MTRA_PDB = DATA_DIR / "pdb" / "MtrA.pdb"
    MTRF_FASTA = DATA_DIR / "MtrF.fasta"
    MTRC_FASTA = DATA_DIR / "MtrC.fasta"
    V2SM_PDB = DATA_DIR / "pdb" / "2VSM.pdb"

    # Outputs del exp01
    OUTPUT_DIR = DATA_DIR / "output_exp01"

    SCRIPTS = {
        # Análisis de hierro-sulfuro
        "check_circuit": SCRIPTS_DIR / "check_circuit.py",
        "destroyer": SCRIPTS_DIR / "destroyer.py",
        "diagnose_chains": SCRIPTS_DIR / "diagnose_chains.py",
        "validate_rigor": SCRIPTS_DIR / "validate_rigor.py",
        "parallel_lab": SCRIPTS_DIR / "parallel_lab.py",
        "run_analysis": SCRIPTS_DIR / "run_analysis_v2.py",

        # Switches y compuertas
        "elp_switch": SCRIPTS_DIR / "elp_switch.py",
        "switching_test": SCRIPTS_DIR / "switching_test.py",

        # ESM2 / PLM
        "esm2_embeddings": SCRIPTS_DIR / "01_esm2_embeddings.py",
        "plm_test": SCRIPTS_DIR / "02_plm_test.py",
        "physicochemical": SCRIPTS_DIR / "03_physicochemical_analysis.py",
        "sequence_duel": SCRIPTS_DIR / "04_sequence_duel.py",
        "run_comparison": SCRIPTS_DIR / "run_comparison.py",
    }

    TARGETS = {
        "MtrF": {
            "pdb": MTRF_PDB,
            "fasta": MTRF_FASTA,
            "description": "MtrF — external gate ferric reductase",
        },
        "MtrA": {
            "pdb": MTRA_PDB,
            "fasta": DATA_DIR / "raw" / "MtrA_REAL.fasta" if (DATA_DIR / "raw" / "MtrA_REAL.fasta").exists() else MTRA_PDB,
            "description": "MtrA — periplasmic iron wire",
        },
        "2VSM": {
            "pdb": V2SM_PDB,
            "description": "2VSM — chain A hotspot analysis target",
        },
    }

    @classmethod
    def resolve_script(cls, name: str) -> Path | None:
        script = cls.SCRIPTS.get(name)
        if script and script.exists():
            return script
        return None

    @classmethod
    def resolve_data(cls, name: str) -> Path | None:
        target = cls.TARGETS.get(name)
        if target and target["pdb"].exists():
            return target["pdb"]
        return None

    @classmethod
    def get_target_config(cls, target: str) -> dict[str, Any]:
        return cls.TARGETS.get(target, {}).copy()

    @classmethod
    def validate_paths(cls) -> dict[str, bool]:
        return {
            "scripts_dir": SCRIPTS_DIR.exists(),
            "data_dir": DATA_DIR.exists(),
            "mtrf_pdb": cls.MTRF_PDB.exists(),
            "mtra_pdb": cls.MTRA_PDB.exists(),
            "output_exp01": cls.OUTPUT_DIR.exists(),
        }

    @classmethod
    def summary(cls) -> str:
        checks = cls.validate_paths()
        lines = [
            f"=== Hemoglobina/Mtr Adapter ===",
            f"Investigación: {cls.INVESTIGATION_NAME}",
            f"Scripts: {len([s for s in cls.SCRIPTS.values() if s.exists()])}/{len(cls.SCRIPTS)} encontrados",
            f"Targets: {len(cls.TARGETS)} configurados",
        ]
        for k, v in checks.items():
            status = "OK" if v else "MISSING"
            lines.append(f"  {k}: {status}")
        return "\n".join(lines)
