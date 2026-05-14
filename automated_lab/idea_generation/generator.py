#!/usr/bin/env python3
"""
automated_lab/idea_generation/generator.py
===========================================
Generador de ideas/experimentos para el Automated Lab.

Modo normal:
- Lee el campaign brief (targets, drugs_smiles, avoid, known_findings).
- Usa KISS Discovery Engine + cloud LLM si hay credenciales para rankear/proponer
  hipótesis con diversidad.
- Fallback determinista y reproducible si el LLM falla.

Importante: el LLM NO inventa SMILES ni secuencias ejecutables. Solo puede
reordenar/etiquetar combinaciones ya presentes en el brief local. Eso evita que
una alucinación se convierta en "experimento" biológico falso. Aburrido, pero
la biología no perdona poesía barata.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent.parent.parent
KISS_DIR = Path(os.getenv("KISS_DISCOVERY_ENGINE_DIR", "/home/gris/.hermes/workspace/repos/kiss_discovery_engine"))

# `fasta_key` debe calzar con el primer campo del header FASTA.
TARGETS = {
    "MOR": {"fasta_key": "MOR", "tier": "Tier2"},
    "NRF2": {"fasta_key": "NRF2", "tier": "Tier1"},
    "Nav1.8": {"fasta_key": "Nav1.8", "tier": "Tier1", "avoid_local_dti": True},
    "TLR4": {"fasta_key": "TLR4", "tier": "Tier2"},
    "TRPA1": {"fasta_key": "TRPA1", "tier": "Tier2"},
    "IL-1β": {"fasta_key": "IL-1β", "tier": "Tier1"},
    "IL-6": {"fasta_key": "IL-6", "tier": "Tier1"},
    "CPA3": {"fasta_key": "CPA3", "tier": "Tier3"},
    "MS4A2": {"fasta_key": "MS4A2/FcεRIβ", "tier": "Tier3"},
    "FCER1A": {"fasta_key": "FCER1A/FcεRIα", "tier": "Tier3"},
    "HDC": {"fasta_key": "HDC", "tier": "Tier3"},
}

DEFAULT_DRUGS = {
    "naltrexona_LDN": "C=CCN1CCC23C4C(=O)CCC2(C1CC5=C3C(=C(C=C5)O)O4)O",
    "dimetil_fumarato": "COC(=O)C=CC(=O)OC",
    "suzetrigine_VX548": "CC1=C(SC(=N1)NC(=O)C2=C(C=CC=C2F)F)C(=O)NCC(F)(F)F",
    "TAK242_resatorvid": "CC1=CC(=CC(=C1Cl)C(F)(F)F)NC(=O)C2=C(C=CC=C2F)F",
}

HYPOTHESIS_TEMPLATES = [
    "{drug} tiene afinidad significativa (pKd > 6) por {target}",
    "{drug} podría mostrar binding off-label contra {target}; verificar contra sesgo de promiscuidad",
    "Comparar {drug}×{target} contra hallazgos conocidos de la campaña",
    "Explorar si {drug} aporta señal poli-farmacológica en {target} sin elevarlo a conclusión clínica",
]


class IdeaGenerator:
    """Genera experimentos ejecutables + hipótesis rankeadas."""

    def __init__(self):
        self.fasta = self._load_fasta()

    def _load_fasta(self) -> dict[str, str]:
        fasta_file = LAB_DIR / "investigacion-fibromialgia" / "datos" / "target_sequences.fasta"
        if not fasta_file.exists():
            return {}
        sequences: dict[str, str] = {}
        name = None
        seq_parts: list[str] = []
        for line in fasta_file.read_text().splitlines():
            line = line.strip()
            if line.startswith(">"):
                if name:
                    sequences[name] = "".join(seq_parts)
                name = line[1:].split("|")[0]
                seq_parts = []
            elif line:
                seq_parts.append(line)
        if name:
            sequences[name] = "".join(seq_parts)
        return sequences

    def _sequence_for_target(self, target_name: str) -> str:
        meta = TARGETS.get(target_name, {"fasta_key": target_name})
        return self.fasta.get(meta["fasta_key"], "")

    def _ordered_targets(self, campaign_name: str, campaign: dict[str, Any]) -> list[str]:
        explicit = list(campaign.get("primary_targets", [])) + list(campaign.get("secondary_targets", []))
        if explicit:
            return [t for t in explicit if t in TARGETS]
        if "ruta_b" in campaign_name.lower() or "ldn" in campaign_name.lower():
            return ["MOR"] + [t for t in TARGETS if t != "MOR"]
        if "ruta_a" in campaign_name.lower() or "mastocito" in campaign_name.lower():
            return ["MS4A2", "FCER1A", "HDC", "CPA3", "MOR", "NRF2", "IL-1β", "IL-6"]
        return list(TARGETS.keys())

    @staticmethod
    def stable_id(payload: dict[str, Any]) -> str:
        raw = json.dumps(
            {k: payload.get(k) for k in ("type", "campaign", "drug_name", "target")},
            sort_keys=True, ensure_ascii=False,
        )
        return "exp_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]

    def _base_grid(self, campaign_name: str, campaign: dict[str, Any], count: int) -> list[dict[str, Any]]:
        drugs = dict(campaign.get("drugs_smiles") or DEFAULT_DRUGS)
        if campaign.get("use_pubchem_expansion", False):
            try:
                from idea_generation.ligand_library import resolve_ligands, DEFAULT_SEED_NAMES
                names = campaign.get("exploratory_drug_names") or DEFAULT_SEED_NAMES
                limit = campaign.get("pubchem_expansion_limit")
                drugs.update(resolve_ligands(names, limit=limit))
            except Exception as exc:
                print(f"[idea_generation] ⚠ PubChem expansion unavailable: {exc}")
        ordered_targets = self._ordered_targets(campaign_name, campaign)
        # Use explicit excluded_targets list when available; avoid fragile
        # substring match on the full avoid text (e.g. "MOR" inside a
        # caveat sentence should not kill the whole MOR row).
        excluded = set(campaign.get("excluded_targets", []))
        ideas: list[dict[str, Any]] = []
        template_count = len(HYPOTHESIS_TEMPLATES)
        for drug_index, (drug_name, drug_smiles) in enumerate(drugs.items()):
            for target_index, target_name in enumerate(ordered_targets):
                meta = TARGETS.get(target_name, {})
                if meta.get("avoid_local_dti") or target_name in excluded:
                    continue
                seq = self._sequence_for_target(target_name)
                if not seq:
                    continue
                template = HYPOTHESIS_TEMPLATES[(drug_index + target_index) % template_count]
                idea = {
                    "type": "dti_pkd",
                    "drug_name": drug_name,
                    "drug_smiles": drug_smiles,
                    "target": target_name,
                    "target_seq": seq,
                    "campaign": campaign_name,
                    "hypothesis": template.format(drug=drug_name, target=target_name),
                    "priority": "primary" if target_name in ordered_targets[:4] else "secondary",
                    "source": "deterministic_grid",
                }
                idea["id"] = self.stable_id(idea)
                ideas.append(idea)
        return ideas[:count]

    def _parse_llm_json(self, text: str) -> list[dict[str, Any]]:
        match = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.S)
        raw = match.group(1) if match else text
        try:
            data = json.loads(raw)
        except Exception:
            start, end = raw.find("["), raw.rfind("]")
            if start == -1 or end == -1 or end <= start:
                return []
            try:
                data = json.loads(raw[start:end + 1])
            except Exception:
                return []
        return data if isinstance(data, list) else []

    async def _kiss_rank(self, campaign_name: str, campaign: dict[str, Any], base: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if os.getenv("AUTOMATED_LAB_USE_KISS", "1") == "0" or not KISS_DIR.exists():
            return []
        if str(KISS_DIR) not in sys.path:
            sys.path.insert(0, str(KISS_DIR))

        # Force the user's requested investigator default when only Ollama is present.
        os.environ.setdefault("KISS_GENERATOR_PROVIDER", os.getenv("AUTOMATED_LAB_PROVIDER", "ollama-cloud"))
        os.environ.setdefault("KISS_GENERATOR_MODEL", os.getenv("AUTOMATED_LAB_MODEL", "nemotron-3-super"))
        os.environ.setdefault("KISS_MAX_TOKENS", "2200")
        os.environ.setdefault("KISS_MAX_CONCURRENT", "2")

        try:
            from src.generator import MercuryGenerator  # type: ignore
        except Exception:
            return []

        allowed_pairs = [{"drug_name": x["drug_name"], "target": x["target"]} for x in base[:200]]
        prompt = f"""
Eres el investigador nocturno de protein-lab. Debes mejorar la cola de experimentos DTI sin inventar SMILES ni targets.
Campaña: {campaign.get('title', campaign_name)}
Objetivo: {campaign.get('objective', '')}
Hallazgos conocidos: {campaign.get('known_findings', [])}
Pares ejecutables permitidos: {json.dumps(allowed_pairs, ensure_ascii=False)}

Devuelve SOLO JSON: una lista de objetos con claves exactas:
- drug_name: uno de los pares permitidos
- target: uno de los pares permitidos
- hypothesis: hipótesis breve, cautelosa y verificable
- rationale: por qué conviene testearlo ahora
- priority_score: número 0-100

Reglas: no inventes literatura; no concluyas eficacia clínica; prioriza controles contra sesgo MOR/promiscuidad y ruta mastocito/inflamación.
""".strip()
        try:
            gen = MercuryGenerator()
            variants = await gen.generate_variants(prompt, num_variants=1, temperature=0.4)
        except Exception:
            return []
        for variant in variants:
            ranked = self._parse_llm_json(variant)
            if ranked:
                return ranked
        return []

    def _merge_ranked(self, base: list[dict[str, Any]], ranked: list[dict[str, Any]], count: int) -> list[dict[str, Any]]:
        by_pair = {(x["drug_name"], x["target"]): x for x in base}
        merged: list[dict[str, Any]] = []
        used: set[tuple[str, str]] = set()
        for item in sorted(ranked, key=lambda x: x.get("priority_score", 0), reverse=True):
            drug_name = item.get("drug_name")
            target = item.get("target")
            if not isinstance(drug_name, str) or not isinstance(target, str):
                continue
            pair = (drug_name, target)
            if pair in used or pair not in by_pair:
                continue
            idea = dict(by_pair[pair])
            if item.get("hypothesis"):
                idea["hypothesis"] = str(item["hypothesis"])
            idea["rationale"] = str(item.get("rationale", ""))
            idea["priority_score"] = float(item.get("priority_score", 0) or 0)
            idea["source"] = "kiss_llm_ranked"
            idea["id"] = self.stable_id(idea)
            merged.append(idea)
            used.add(pair)
        for idea in base:
            pair = (idea["drug_name"], idea["target"])
            if pair not in used:
                merged.append(idea)
                used.add(pair)
        return merged[:count]

    def generate(self, campaign_name: str, brief_md: str = "", count: int = 50,
                 campaign: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        campaign = dict(campaign or {})
        if brief_md and not campaign:
            campaign = {"brief_md": brief_md}
        base = self._base_grid(campaign_name, campaign, count=max(count, 200))
        if not base:
            return []
        ranked: list[dict[str, Any]] = []
        try:
            ranked = asyncio.run(self._kiss_rank(campaign_name, campaign, base))
        except RuntimeError:
            # If called from an existing event loop, skip LLM ranking; deterministic is safe.
            ranked = []
        return self._merge_ranked(base, ranked, count=count) if ranked else base[:count]
