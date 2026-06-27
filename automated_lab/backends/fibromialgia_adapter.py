#!/usr/bin/env python3
"""
automated_lab/backends/fibromialgia_adapter.py
================================================
Adapter del automated_lab para la investigación fibromialgia.

Provee:
  - Target paths para datasets GEO (GSE221921, GSE67311, etc.)
  - Config de docking runs (naltrexona, MOR, DRD2)
  - Parámetros de deconvolution celular, ESM2, FEP
  - Paths de literatura y reportes
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent.parent.parent
INVESTIGATION_DIR = LAB_DIR / "investigacion-fibromialgia"
SCRIPTS_DIR = INVESTIGATION_DIR / "scripts"
DATA_DIR = INVESTIGATION_DIR / "data"
DATOS_DIR = INVESTIGATION_DIR / "datos"
ANALISIS_DIR = INVESTIGATION_DIR / "analisis"
DOCKING_RUNS_DIR = INVESTIGATION_DIR / "docking_runs"
FEP_DIR = INVESTIGATION_DIR / "fep"
LITERATURA_DIR = INVESTIGATION_DIR / "literatura"
REPORTES_DIR = INVESTIGACION_DIR / "reportes" if False else INVESTIGATION_DIR / "reportes"


class FibromialgiaAdapter:
    """Adapter para experimentos de fibromialgia."""

    INVESTIGATION_NAME = "fibromialgia"

    # Datos GEO
    GEO_DATASETS = {
        "GSE221921": {
            "path": DATOS_DIR / "geo" / "PBMC_FM_96patients_93controls",
            "description": "PBMC Fibromyalgia 96 patients / 93 controls (microarray)",
        },
        "GSE67311": {
            "path": DATOS_DIR / "geo" / "GSE67311",
            "description": "Blood FM 70 patients / 70 controls",
        },
        "GSE229750": {
            "path": DATOS_DIR / "geo" / "Neutrophils_FM_tocilizumab_trial",
            "description": "Neutrophils FM tocilizumab trial",
        },
    }

    # AlphaFold structures
    ALPHAFOLD_DIR = DATA_DIR / "alphafold"

    # Docking targets
    DOCKING_TARGETS = {
        "MOR": {
            "dir": DOCKING_RUNS_DIR / "naltrexone_mor",
            "description": "Mu-opioid receptor (MOR) docking with naltrexone",
        },
        "DRD2": {
            "dir": DOCKING_RUNS_DIR / "selectivity_mapping",
            "description": "Dopamine D2 receptor selectivity mapping",
        },
        "ad_hoc": {
            "dir": DOCKING_RUNS_DIR / "ad_hoc_design",
            "description": "Ad hoc binding site analysis",
        },
    }

    SCRIPTS = {
        # Análisis de datos GEO
        "deconvolution": ANALISIS_DIR / "deconvolution" / "run_deconvolution.py" if (ANALISIS_DIR / "deconvolution" / "run_deconvolution.py").exists() else None,
        "esm2": ANALISIS_DIR / "esm2" / "run_esm2.py" if (ANALISIS_DIR / "esm2" / "run_esm2.py").exists() else None,
        "pk_pd": ANALISIS_DIR / "pk_pd_simulation" / "run_pkpd.py" if (ANALISIS_DIR / "pk_pd_simulation" / "run_pkpd.py").exists() else None,

        # Cross-context
        "cross_context_gwas": SCRIPTS_DIR / "cross_context_gwas_neural_genes.py" if (SCRIPTS_DIR / "cross_context_gwas_neural_genes.py").exists() else None,

        # Fibromialgia pipeline scripts
        "check_geo": SCRIPTS_DIR / "check_geo.py" if (SCRIPTS_DIR / "check_geo.py").exists() else None,
        "deg_analysis": SCRIPTS_DIR / "deg_gse221921.py" if (SCRIPTS_DIR / "deg_gse221921.py").exists() else None,

        # FEP
        "fep_calc": FEP_DIR / "scripts" / "run_fep.py" if (FEP_DIR / "scripts" / "run_fep.py").exists() else None,
    }

    LITERATURA_CATEGORIES = {
        "clinical_trials": LITERATURA_DIR / "clinical_trials",
        "omics": LITERATURA_DIR / "omics",
        "ml_approaches": LITERATURA_DIR / "ml_approaches",
        "redox_neuroinflammation": LITERATORA_DIR / "redox_neuroinflammation" if False else LITERATURA_DIR / "redox_neuroinflammation",
        "reviews": LITERATURA_DIR / "reviews",
        "pdfs": LITERATURA_DIR / "pdfs",
    }

    @classmethod
    def resolve_script(cls, name: str) -> Path | None:
        script = cls.SCRIPTS.get(name)
        if script is None:
            return None
        if script.exists():
            return script
        return None

    @classmethod
    def geo_dataset_path(cls, accession: str) -> Path | None:
        ds = cls.GEO_DATASETS.get(accession)
        if ds and ds["path"].exists():
            return ds["path"]
        return None

    @classmethod
    def docking_target_dir(cls, target: str) -> Path | None:
        t = cls.DOCKING_TARGETS.get(target)
        if t and t["dir"].exists():
            return t["dir"]
        return None

    @classmethod
    def validate_paths(cls) -> dict[str, bool]:
        return {
            "scripts_dir": SCRIPTS_DIR.exists(),
            "data_dir": DATA_DIR.exists(),
            "datos_dir": DATOS_DIR.exists(),
            "analisis_dir": ANALISIS_DIR.exists(),
            "docking_runs": DOCKING_RUNS_DIR.exists(),
            "fep_dir": FEP_DIR.exists(),
            "literatura_dir": LITERATURA_DIR.exists(),
            "reportes_dir": REPORTES_DIR.exists(),
            "alphafold": cls.ALPHAFOLD_DIR.exists(),
        }

    @classmethod
    def summary(cls) -> str:
        checks = cls.validate_paths()
        scripts_found = len([s for s in cls.SCRIPTS.values() if s is not None and s.exists()])
        scripts_total = len([s for s in cls.SCRIPTS.values() if s is not None])
        lines = [
            f"=== Fibromialgia Adapter ===",
            f"Investigación: {cls.INVESTIGATION_NAME}",
            f"Scripts: {scripts_found}/{scripts_total} encontrados",
            f"GEO datasets: {len(cls.GEO_DATASETS)} configurados",
            f"Docking targets: {len(cls.DOCKING_TARGETS)} configurados",
        ]
        for k, v in checks.items():
            status = "OK" if v else "MISSING"
            lines.append(f"  {k}: {status}")
        return "\n".join(lines)
