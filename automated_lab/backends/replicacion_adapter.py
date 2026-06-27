#!/usr/bin/env python3
"""
automated_lab/backends/replicacion_adapter.py
==============================================
Adapter del automated_lab para replicación de datasets GSE274134
y análisis de competencias CASP.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent.parent.parent


class ReplicacionGSE274134Adapter:
    """Adapter para replicación de GSE274134."""

    INVESTIGATION_NAME = "replicacion-gse274134"

    INVESTIGATION_DIR = LAB_DIR / "replicacion_gse274134"
    DATOS_DIR = INVESTIGATION_DIR / "datos"
    ANALISIS_DIR = INVESTIGATION_DIR / "analisis"
    SCRIPTS_DIR = INVESTIGATION_DIR / "scripts"

    @classmethod
    def validate_paths(cls) -> dict[str, bool]:
        return {
            "investigation_dir": cls.INVESTIGATION_DIR.exists(),
            "datos": cls.DATOS_DIR.exists(),
            "analisis": cls.ANALISIS_DIR.exists(),
            "scripts": cls.SCRIPTS_DIR.exists(),
        }

    @classmethod
    def summary(cls) -> str:
        checks = cls.validate_paths()
        return f"=== Replicacion GSE274134 ===\n" + "\n".join(
            f"  {k}: {'OK' if v else 'MISSING'}" for k, v in checks.items()
        )


class CASP17Adapter:
    """Adapter para análisis CASP17."""

    INVESTIGATION_NAME = "casp17"

    INVESTIGATION_DIR = LAB_DIR / "casp17"
    TARGETS_DIR = INVESTIGATION_DIR / "targets"
    PREDICTIONS_DIR = INVESTIGATION_DIR / "predictions"
    SUBMISSIONS_DIR = INVESTIGATION_DIR / "submissions"
    REPORTS_DIR = INVESTIGATION_DIR / "reports"
    SCRIPTS_DIR = INVESTIGATION_DIR / "scripts"

    @classmethod
    def validate_paths(cls) -> dict[str, bool]:
        return {
            "investigation_dir": cls.INVESTIGATION_DIR.exists(),
            "targets": cls.TARGETS_DIR.exists(),
            "predictions": cls.PREDICTIONS_DIR.exists(),
            "submissions": cls.SUBMISSIONS_DIR.exists(),
            "reports": cls.REPORTS_DIR.exists(),
            "scripts": cls.SCRIPTS_DIR.exists(),
        }

    @classmethod
    def summary(cls) -> str:
        checks = cls.validate_paths()
        return f"=== CASP17 ===\n" + "\n".join(
            f"  {k}: {'OK' if v else 'MISSING'}" for k, v in checks.items()
        )
