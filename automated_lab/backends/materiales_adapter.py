#!/usr/bin/env python3
"""
automated_lab/backends/materiales_adapter.py
=============================================
Adapter del automated_lab para la investigación materiales-avanzados-chile.

Provee:
  - Target paths para catalizadores de renio (UndA_HEC904, MtrF_HEC676)
  - Config de docking phase4, MD, APBS
  - Paths de análisis, figuras, publicación
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent.parent.parent
INVESTIGATION_DIR = LAB_DIR / "materiales-avanzados-chile"
CATALYSIS_DIR = INVESTIGATION_DIR / "02_catalizadores_renio"
DOCKING_DIR = CATALYSIS_DIR / "docking"
PHASE4_DIR = DOCKING_DIR / "phase4"


class MaterialesAdapter:
    """Adapter para experimentos de materiales avanzados (catalizadores de renio)."""

    INVESTIGATION_NAME = "materiales-avanzados-chile"

    # Targets de docking/MD
    TARGETS = {
        "UndA_HEC904": {
            "md_dir": PHASE4_DIR / "md" / "UndA_HEC904",
            "description": "UndA-HEC904 complex MD trajectory",
            "system_xml": PHASE4_DIR / "md" / "UndA_HEC904" / "system.xml",
        },
        "MtrF_HEC676": {
            "md_dir": PHASE4_DIR / "md" / "MtrF_HEC676",
            "description": "MtrF-HEC676 complex MD trajectory",
            "system_xml": PHASE4_DIR / "md" / "MtrF_HEC676" / "system.xml",
        },
    }

    # Sub-proyectos
    SUBPROJECTS = {
        "01_membranas_lisa": INVESTIGATION_DIR / "01_membranas_lisa",
        "02_catalizadores_renio": CATALYSIS_DIR,
        "03_nanocompuestos_antifouling": INVESTIGATION_DIR / "03_nanocompuestos_antifouling",
        "04_envases_activos": INVESTIGATION_DIR / "04_envases_activos",
        "05_metamateriales_sismicos": INVESTIGATION_DIR / "05_metamateriales_sismicos",
        "roadmap": INVESTIGATION_DIR / "roadmap",
    }

    # Directorios de resultados
    RESULTS_DIRS = {
        "docking_results": DOCKING_DIR / "results",
        "docking_results_ad4": DOCKING_DIR / "results_ad4",
        "phase4_results": PHASE4_DIR / "results",
        "vina_poses": PHASE4_DIR / "results" / "vina_poses",
        "figures": DOCKING_DIR / "figures",
        "figures_publication": DOCKING_DIR / "figures_publication",
        "apbs": DOCKING_DIR / "apbs",
        "esm2": DOCKING_DIR / "esm2",
        "analisis": CATALYSIS_DIR / "analisis",
        "proteinas": CATALYSIS_DIR / "proteinas",
        "papers": CATALYSIS_DIR / "papers",
        "experimento_biosintesis": CATALYSIS_DIR / "experimento_variante_1_biosintesis",
    }

    # Colab MD runs
    COLAB_MD_DIR = INVESTIGATION_DIR / "colab_renewio_md"

    @classmethod
    def resolve_target(cls, name: str) -> dict[str, Any] | None:
        target = cls.TARGETS.get(name)
        if target:
            return target.copy()
        return None

    @classmethod
    def resolve_results_dir(cls, name: str) -> Path | None:
        d = cls.RESULTS_DIRS.get(name)
        if d and d.exists():
            return d
        return None

    @classmethod
    def validate_paths(cls) -> dict[str, bool]:
        return {
            "investigation_dir": INVESTIGATION_DIR.exists(),
            "catalysis_dir": CATALYSIS_DIR.exists(),
            "docking_dir": DOCKING_DIR.exists(),
            "phase4_dir": PHASE4_DIR.exists(),
            "undA_md": cls.TARGETS["UndA_HEC904"]["md_dir"].exists(),
            "mtrf_md": cls.TARGETS["MtrF_HEC676"]["md_dir"].exists(),
            "colab_md": cls.COLAB_MD_DIR.exists(),
        }

    @classmethod
    def summary(cls) -> str:
        checks = cls.validate_paths()
        lines = [
            f"=== Materiales Avanzados Adapter ===",
            f"Investigación: {cls.INVESTIGATION_NAME}",
            f"Targets MD: {len(cls.TARGETS)} configurados",
            f"Sub-proyectos: {len(cls.SUBPROJECTS)}",
        ]
        for k, v in checks.items():
            status = "OK" if v else "MISSING"
            lines.append(f"  {k}: {status}")
        return "\n".join(lines)
