#!/usr/bin/env python3
"""
automated_lab/backends/bionemo_adapter.py
==========================================
Adapter del automated_lab para NVIDIA BioNeMo Agent Toolkit.

Provee acceso unificado a los NIM skills de BioNeMo:
  - RFdiffusion: diseño de novo de backbones y binders
  - DiffDock: docking molecular (protein-ligand)
  - ProteinMPNN: diseño de secuencias para un backbone
  - Boltz-2: predicción de estructura protein-ligand
  - OpenFold2/3: predicción de estructura
  - Evo2: modelo de lenguaje genómico
  - MolMIM: generación de moléculas
  - GenMol: generación de moléculas
  - MSA-Search: búsqueda de alineamientos

Modo de operación:
  - Hosted (NVIDIA API): requiere NVIDIA_API_KEY
  - Local Docker: requiere NGC_API_KEY + contenedores corriendo
"""

from __future__ import annotations

import os
import json
import subprocess
import time
from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().resolve().parent.parent.parent
BIONEMO_DIR = Path("/home/gris96/oss-science-agents/bionemo-agent-toolkit")

# ══════════════════════════════════════════════════════════════════════════════
# Configuración
# ══════════════════════════════════════════════════════════════════════════════

NVIDIA_HOSTED_BASE = "https://health.api.nvidia.com/v1/biology"
LOCAL_BASE = "http://localhost:8000"

NIM_ENDPOINTS = {
    "rfdiffusion": {
        "hosted": f"{NVIDIA_HOSTED_BASE}/ipd/rfdiffusion/generate",
        "local": f"{LOCAL_BASE}/biology/ipd/rfdiffusion/generate",
        "health": f"{LOCAL_BASE}/v1/health/ready",
        "description": "RFDiffusion protein backbone design",
    },
    "diffdock": {
        "hosted": f"{NVIDIA_HOSTED_BASE}/mit/diffdock",
        "local": f"{LOCAL_BASE}/molecular-docking/diffdock/generate",
        "health": f"{LOCAL_BASE}/v1/health/ready",
        "description": "DiffDock molecular docking",
    },
    "proteinmpnn": {
        "hosted": f"{NVIDIA_HOSTED_BASE}/ipd/proteinmpnn/predict",
        "local": f"{LOCAL_BASE}/biology/ipd/proteinmpnn/predict",
        "health": f"{LOCAL_BASE}/v1/health/ready",
        "description": "ProteinMPNN inverse folding",
    },
    "boltz2": {
        "hosted": f"{NVIDIA_HOSTED_BASE}/mit/boltz2/predict",
        "local": f"{LOCAL_BASE}/biology/mit/boltz2/predict",
        "health": f"{LOCAL_BASE}/v1/health/ready",
        "description": "Boltz-2 structure prediction",
    },
    "openfold2": {
        "hosted": f"{NVIDIA_HOSTED_BASE}/ipd/openfold2/predict",
        "local": f"{LOCAL_BASE}/biology/ipd/openfold2/predict",
        "health": f"{LOCAL_BASE}/v1/health/ready",
        "description": "OpenFold2 structure prediction",
    },
    "openfold3": {
        "hosted": f"{NVIDIA_HOSTED_BASE}/ipd/openfold3/predict",
        "local": f"{LOCAL_BASE}/biology/ipd/openfold3/predict",
        "health": f"{LOCAL_BASE}/v1/health/ready",
        "description": "OpenFold3 structure prediction",
    },
    "evo2": {
        "hosted": f"{NVIDIA_HOSTED_BASE}/arc/evo2/generate",
        "local": f"{LOCAL_BASE}/biology/arc/evo2/generate",
        "health": f"{LOCAL_BASE}/v1/health/ready",
        "description": "Evo2 genomic language model",
    },
    "molmim": {
        "hosted": f"{NVIDIA_HOSTED_BASE}/ipd/molmim/generate",
        "local": f"{LOCAL_BASE}/biology/ipd/molmim/generate",
        "health": f"{LOCAL_BASE}/v1/health/ready",
        "description": "MolMIM molecule generation",
    },
    "genmol": {
        "hosted": f"{NVIDIA_HOSTED_BASE}/ipd/genmol/generate",
        "local": f"{LOCAL_BASE}/biology/ipd/genmol/generate",
        "health": f"{LOCAL_BASE}/v1/health/ready",
        "description": "GenMol molecule generation",
    },
    "msa_search": {
        "hosted": f"{NVIDIA_HOSTED_BASE}/ipd/msa/search",
        "local": f"{LOCAL_BASE}/biology/ipd/msa/search",
        "health": f"{LOCAL_BASE}/v1/health/ready",
        "description": "MSA search",
    },
}

# Skills disponibles en el toolkit
SKILLS = {
    "rfdiffusion": BIONEMO_DIR / "nim-skills" / "rfdiffusion-nim" / "SKILL.md",
    "diffdock": BIONEMO_DIR / "nim-skills" / "diffdock-nim" / "SKILL.md",
    "proteinmpnn": BIONEMO_DIR / "nim-skills" / "proteinmpnn-nim" / "SKILL.md",
    "boltz2": BIONEMO_DIR / "nim-skills" / "boltz2-nim" / "SKILL.md",
    "openfold2": BIONEMO_DIR / "nim-skills" / "openfold2-nim" / "SKILL.md",
    "openfold3": BIONEMO_DIR / "nim-skills" / "openfold3-nim" / "SKILL.md",
    "evo2": BIONEMO_DIR / "nim-skills" / "evo2-nim" / "SKILL.md",
    "molmim": BIONEMO_DIR / "nim-skills" / "molmim-nim" / "SKILL.md",
    "genmol": BIONEMO_DIR / "nim-skills" / "genmol-nim" / "SKILL.md",
    "msa_search": BIONEMO_DIR / "nim-skills" / "msa-search-nim" / "SKILL.md",
    "drug_discovery": BIONEMO_DIR / "nim-skills" / "drug-discovery-pipeline" / "SKILL.md",
    "msa_structure": BIONEMO_DIR / "nim-skills" / "msa-structure-prediction-pipeline" / "SKILL.md",
    "genomics": BIONEMO_DIR / "library-skills" / "genomics-workflow-acceleration" / "SKILL.md",
    "nvMolKit": BIONEMO_DIR / "library-skills" / "nvMolKit" / "SKILL.md",
    "cuEquivariance": BIONEMO_DIR / "library-skills" / "cuEquivariance" / "SKILL.md",
    "parabricks": BIONEMO_DIR / "library-skills" / "parabricks" / "SKILL.md",
    "complexa_setup": BIONEMO_DIR / "open-models-skills" / "proteina-complexa" / "complexa-setup" / "SKILL.md",
    "complexa_design": BIONEMO_DIR / "open-models-skills" / "proteina-complexa" / "complexa-design" / "SKILL.md",
    "complexa_target": BIONEMO_DIR / "open-models-skills" / "proteina-complexa" / "complexa-target" / "SKILL.md",
    "complexa_evaluate": BIONEMO_DIR / "open-models-skills" / "proteina-complexa" / "complexa-evaluate-pdbs" / "SKILL.md",
    "kermt_setup": BIONEMO_DIR / "open-models-skills" / "kermt" / "kermt-setup" / "SKILL.md",
    "kermt_infer": BIONEMO_DIR / "open-models-skills" / "kermt" / "kermt-infer" / "SKILL.md",
    "kermt_embed": BIONEMO_DIR / "open-models-skills" / "kermt" / "kermt-embed" / "SKILL.md",
}

# Workflows compuestos
WORKFLOWS = {
    "generative_protein_binder_design": {
        "description": "RFdiffusion -> ProteinMPNN -> Boltz2/OpenFold3 pipeline",
        "steps": ["rfdiffusion", "proteinmpnn", "boltz2"],
        "skill": BIONEMO_DIR / "workflows" / "generative_protein_binder_design" / "SKILL.md",
    },
    "complexa_binder_design": {
        "description": "Proteina-Complexa reward-guided co-design + Boltz2/OpenFold3",
        "steps": ["complexa_design", "boltz2"],
        "skill": BIONEMO_DIR / "workflows" / "generative_protein_binder_design" / "complexa-binder-design" / "SKILL.md",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _get_api_key() -> str | None:
    """Obtiene API key de NVIDIA (NGC_API_KEY > NVIDIA_API_KEY)."""
    return os.environ.get("NGC_API_KEY") or os.environ.get("NVIDIA_API_KEY")


def _extract_atom_records(pdb_content: str) -> str:
    """Extrae solo registros ATOM de un PDB (requerido por DiffDock)."""
    return "\n".join(line for line in pdb_content.splitlines() if line.startswith("ATOM"))


# ══════════════════════════════════════════════════════════════════════════════
# Adapter
# ══════════════════════════════════════════════════════════════════════════════

class BioNeMoAdapter:
    """Adapter para NVIDIA BioNeMo Agent Toolkit."""

    PROVIDER_NAME = "bionemo"

    @classmethod
    def check_prerequisites(cls) -> dict:
        """Verifica que el toolkit esté disponible y configurado."""
        result = {
            "toolkit_installed": False,
            "api_key_set": False,
            "ready": False,
            "errors": [],
            "skills_found": 0,
            "skills_total": len(SKILLS),
            "workflows_found": 0,
            "workflows_total": len(WORKFLOWS),
        }

        # Verificar que el repo existe
        if BIONEMO_DIR.exists():
            result["toolkit_installed"] = True
        else:
            result["errors"].append(f"BioNeMo toolkit no encontrado en {BIONEMO_DIR}")

        # Contar skills encontrados
        result["skills_found"] = sum(1 for p in SKILLS.values() if p.exists())

        # Contar workflows encontrados
        result["workflows_found"] = sum(1 for w in WORKFLOWS.values() if w["skill"].exists())

        # Verificar API key
        if _get_api_key():
            result["api_key_set"] = True
        else:
            result["errors"].append("Falta API key. Definir NGC_API_KEY o NVIDIA_API_KEY")

        result["ready"] = result["toolkit_installed"] and result["api_key_set"]
        return result

    # ── RFdiffusion ──────────────────────────────────────────────────────────

    @classmethod
    def rfdiffusion_design(
        cls,
        contigs: str,
        input_pdb: str | None = None,
        hotspot_res: list[str] | None = None,
        diffusion_steps: int = 50,
        random_seed: int | None = None,
        mode: str = "hosted",
    ) -> dict:
        """
        Diseña un backbone de proteína con RFdiffusion.

        Args:
            contigs: especificación de contigs (ej: "80-120", "A1-100/0 50-100")
            input_pdb: contenido del PDB (para scaffolding/binder design)
            hotspot_res: residuos hotspot (ej: ["A50", "A51"])
            diffusion_steps: pasos de difusión (1-50)
            random_seed: semilla para reproducibilidad
            mode: "hosted" o "local"

        Returns:
            dict con output_pdb y elapsed_ms
        """
        import requests

        endpoint = NIM_ENDPOINTS["rfdiffusion"][mode]
        api_key = _get_api_key()

        payload: dict[str, Any] = {
            "contigs": contigs,
            "diffusion_steps": diffusion_steps,
        }

        if input_pdb:
            payload["input_pdb"] = input_pdb
        else:
            # Dummy PDB para de novo
            payload["input_pdb"] = (
                "CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1\n"
                "ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C\n"
                "END\n"
            )

        if hotspot_res:
            payload["hotspot_res"] = hotspot_res
        if random_seed is not None:
            payload["random_seed"] = random_seed

        headers = {"Content-Type": "application/json"}
        if mode == "hosted" and api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        resp = requests.post(endpoint, json=payload, headers=headers, timeout=600)
        resp.raise_for_status()
        return resp.json()

    # ── DiffDock ─────────────────────────────────────────────────────────────

    @classmethod
    def diffdock(
        cls,
        protein_pdb: str,
        ligand_smiles: str | None = None,
        ligand_sdf: str | None = None,
        ligand_file_type: str = "txt",
        num_poses: int = 10,
        time_divisions: int = 20,
        steps: int = 18,
        mode: str = "hosted",
    ) -> dict:
        """
        Docking molecular con DiffDock.

        Args:
            protein_pdb: contenido del PDB (solo ATOM records)
            ligand_smiles: SMILES del ligando (usar con ligand_file_type="txt")
            ligand_sdf: contenido SDF del ligando
            ligand_file_type: "txt" (SMILES), "sdf", "mol2"
            num_poses: número de poses (≤100)
            time_divisions: divisiones de tiempo (≤20)
            steps: pasos de difusión (≤18)
            mode: "hosted" o "local"

        Returns:
            dict con ligand_positions (poses SDF) y position_confidence
        """
        import requests

        endpoint = NIM_ENDPOINTS["diffdock"][mode]
        api_key = _get_api_key()

        # Extraer solo ATOM records
        protein = _extract_atom_records(protein_pdb)

        if ligand_smiles:
            ligand = ligand_smiles
            ligand_file_type = "txt"
        elif ligand_sdf:
            ligand = ligand_sdf
            ligand_file_type = "sdf"
        else:
            raise ValueError("Debe proporcionar ligand_smiles o ligand_sdf")

        payload = {
            "protein": protein,
            "ligand": ligand,
            "ligand_file_type": ligand_file_type,
            "num_poses": num_poses,
            "time_divisions": time_divisions,
            "steps": steps,
        }

        headers = {"Content-Type": "application/json"}
        if mode == "hosted" and api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        resp = requests.post(endpoint, json=payload, headers=headers, timeout=600)
        resp.raise_for_status()
        return resp.json()

    # ── ProteinMPNN ──────────────────────────────────────────────────────────

    @classmethod
    def proteinmpnn_design(
        cls,
        input_pdb: str,
        num_seq_per_target: int = 8,
        sampling_temp: list[float] | None = None,
        fixed_chains: list[str] | None = None,
        omit_AAs: list[str] | None = None,
        use_soluble_model: bool = False,
        random_seed: int | None = None,
        mode: str = "hosted",
    ) -> dict:
        """
        Diseña secuencias para un backbone con ProteinMPNN.

        Args:
            input_pdb: contenido del PDB del backbone
            num_seq_per_target: secuencias a generar (1-100)
            sampling_temp: temperaturas de muestreo (0.0-1.0)
            fixed_chains: cadenas a no rediseñar (ej: ["A"])
            omit_AAs: aminoácidos a excluir (ej: ["C", "M"])
            use_soluble_model: usar modelo soluble
            random_seed: semilla para reproducibilidad
            mode: "hosted" o "local"

        Returns:
            dict con mfasta (secuencias), scores, probs
        """
        import requests

        endpoint = NIM_ENDPOINTS["proteinmpnn"][mode]
        api_key = _get_api_key()

        payload: dict[str, Any] = {
            "input_pdb": input_pdb,
            "num_seq_per_target": num_seq_per_target,
        }

        if sampling_temp:
            payload["sampling_temp"] = sampling_temp
        if fixed_chains:
            payload["input_pdb_chains"] = fixed_chains
        if omit_AAs:
            payload["omit_AAs"] = omit_AAs
        if use_soluble_model:
            payload["use_soluble_model"] = True
        if random_seed is not None:
            payload["random_seed"] = random_seed

        headers = {"Content-Type": "application/json"}
        if mode == "hosted" and api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        resp = requests.post(endpoint, json=payload, headers=headers, timeout=300)
        resp.raise_for_status()
        return resp.json()

    # ── Boltz-2 ──────────────────────────────────────────────────────────────

    @classmethod
    def boltz2_predict(
        cls,
        polymers: list[dict],
        ligands: list[dict] | None = None,
        recycling_steps: int = 3,
        sampling_steps: int = 50,
        diffusion_samples: int = 1,
        mode: str = "hosted",
    ) -> dict:
        """
        Predicción de estructura con Boltz-2.

        Args:
            polymers: lista de cadenas [{"molecule_type": "protein", "sequence": "...", "id": "A"}]
            ligands: lista de ligandos [{"smiles": "...", "id": "LIG"}]
            recycling_steps: pasos de reciclaje (1-10)
            sampling_steps: pasos de muestreo (10-1000)
            diffusion_samples: estructuras a generar (1-25)
            mode: "hosted" o "local"

        Returns:
            dict con estructura predicha en formato mmCIF
        """
        import requests

        endpoint = NIM_ENDPOINTS["boltz2"][mode]
        api_key = _get_api_key()

        payload: dict[str, Any] = {
            "polymers": polymers,
            "recycling_steps": recycling_steps,
            "sampling_steps": sampling_steps,
            "diffusion_samples": diffusion_samples,
            "output_format": "mmcif",
        }
        if ligands:
            payload["ligands"] = ligands

        headers = {"Content-Type": "application/json"}
        if mode == "hosted" and api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        resp = requests.post(endpoint, json=payload, headers=headers, timeout=600)
        resp.raise_for_status()
        return resp.json()

    # ── Utilidades ───────────────────────────────────────────────────────────

    @classmethod
    def list_nims(cls) -> list[dict]:
        """Lista todos los NIMs disponibles."""
        return [
            {"name": k, "description": v["description"], "hosted": v["hosted"], "local": v["local"]}
            for k, v in NIM_ENDPOINTS.items()
        ]

    @classmethod
    def list_skills(cls) -> list[dict]:
        """Lista todos los skills disponibles."""
        return [
            {"name": k, "path": str(v), "exists": v.exists()}
            for k, v in SKILLS.items()
        ]

    @classmethod
    def list_workflows(cls) -> list[dict]:
        """Lista todos los workflows compuestos."""
        return [
            {"name": k, "description": v["description"], "steps": v["steps"], "exists": v["skill"].exists()}
            for k, v in WORKFLOWS.items()
        ]

    @classmethod
    def get_skill_md(cls, skill_name: str) -> str | None:
        """Lee el contenido de un SKILL.md."""
        path = SKILLS.get(skill_name)
        if path and path.exists():
            return path.read_text()
        return None

    @classmethod
    def summary(cls) -> str:
        """Resumen del estado del adapter."""
        checks = cls.check_prerequisites()
        lines = [
            "=== BioNeMo Agent Toolkit Adapter ===",
            f"Toolkit: {'OK' if checks['toolkit_installed'] else 'MISSING'}",
            f"API Key: {'OK' if checks['api_key_set'] else 'MISSING'}",
            f"Skills: {checks['skills_found']}/{checks['skills_total']}",
            f"Workflows: {checks['workflows_found']}/{checks['workflows_total']}",
            f"NIMs: {len(NIM_ENDPOINTS)} configurados",
        ]
        if checks["errors"]:
            lines.append(f"Errores: {', '.join(checks['errors'])}")
        return "\n".join(lines)
