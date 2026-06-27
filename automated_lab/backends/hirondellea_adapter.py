#!/usr/bin/env python3
"""
automated_lab/backends/hirondellea_adapter.py
==============================================
Adapter del automated_lab para la investigación hirondellea-gigas.

Provee:
  - Target paths para datos genómicos (FASTA, raw)
  - Config de análisis (BLAST, embeddings, proteoma)
  - Paths de baroresistencia GH7
  - Referencias y literatura
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent.parent.parent
INVESTIGATION_DIR = LAB_DIR / "hirondellea-gigas"
DATOS_DIR = INVESTIGATION_DIR / "datos"
ANALISIS_DIR = INVESTIGATION_DIR / "analisis"
BARO_DIR = INVESTIGATION_DIR / "investigacion-baroresistencia-gh7"


class HirondelleaAdapter:
    """Adapter para experimentos de hirondellea-gigas."""

    INVESTIGATION_NAME = "hirondellea-gigas"

    # Datos principales
    DATA_FILES = {
        "proteins_faa": DATOS_DIR / "fasta" / "hirondellea_gigas_proteins.faa",
        "proteins_psq": DATOS_DIR / "fasta" / "hirondellea_gigas_proteins.psq",
        "proteins_phr": DATOS_DIR / "fasta" / "hirondellea_gigas_proteins.phr",
        "transcriptome_faa": DATOS_DIR / "fasta" / "hg_transcriptome_proteins.faa",
        "transcriptome_psq": DATOS_DIR / "fasta" / "hg_transcriptome_proteins.psq",
        "transcriptome_phr": DATOS_DIR / "fasta" / "hg_transcriptome_proteins.phr",
        "contigs": DATOS_DIR / "raw" / "GEZX01000000_contigs.fa",
    }

    # Análisis
    ANALYSIS_DIRS = {
        "blast": ANALISIS_DIR / "blast",
        "embeddings": ANALISIS_DIR / "embeddings",
        "proteoma": ANALISIS_DIR / "proteoma",
        "metricas": ANALISIS_DIR / "metricas",
        "vias": ANALISIS_DIR / "vias",
        "aplicaciones": ANALISIS_DIR / "aplicaciones",
        "scripts": ANALISIS_DIR / "scripts",
    }

    # Sub-investigaciones
    SUBINVESTIGATIONS = {
        "baroresistencia_gh7": {
            "dir": BARO_DIR,
            "description": "Baroresistencia GH7 — protein adaptation to deep-sea pressure",
            "resultados": BARO_DIR / "resultados",
            "scripts": BARO_DIR / "scripts",
            "publicacion": BARO_DIR / "publicacion",
            "roadmap": BARO_DIR / "roadmap",
        },
    }

    # Colab AlphaFold
    COLAB_AF_DIR = INVESTIGATION_DIR / "colab_alphafold"

    # Referencias
    LITERATURA_DIR = INVESTIGATION_DIR / "literatura"
    PAPERS_DIR = INVESTIGATION_DIR / "papers"
    REFERENCE_DIR = INVESTIGATION_DIR / "references"
    REPORTES_DIR = INVESTIGATION_DIR / "reportes"
    PROTEINAS_DIR = INVESTIGATION_DIR / "proteinas"

    @classmethod
    def resolve_data(cls, name: str) -> Path | None:
        f = cls.DATA_FILES.get(name)
        if f and f.exists():
            return f
        return None

    @classmethod
    def resolve_analysis_dir(cls, name: str) -> Path | None:
        d = cls.ANALYSIS_DIRS.get(name)
        if d and d.exists():
            return d
        return None

    @classmethod
    def validate_paths(cls) -> dict[str, bool]:
        return {
            "datos_dir": DATOS_DIR.exists(),
            "analisis_dir": ANALISIS_DIR.exists(),
            "baroresistencia": BARO_DIR.exists(),
            "colab_alphafold": cls.COLAB_AF_DIR.exists(),
            "literatura": cls.LITERATURA_DIR.exists(),
            "papers": cls.PAPERS_DIR.exists(),
        }

    @classmethod
    def summary(cls) -> str:
        checks = cls.validate_paths()
        data_found = len([f for f in cls.DATA_FILES.values() if f.exists()])
        lines = [
            f"=== Hirondellea Adapter ===",
            f"Investigación: {cls.INVESTIGATION_NAME}",
            f"Data files: {data_found}/{len(cls.DATA_FILES)} encontrados",
            f"Sub-investigaciones: {len(cls.SUBINVESTIGATIONS)}",
        ]
        for k, v in checks.items():
            status = "OK" if v else "MISSING"
            lines.append(f"  {k}: {status}")
        return "\n".join(lines)
