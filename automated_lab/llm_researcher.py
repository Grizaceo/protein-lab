#!/usr/bin/env python3
"""
Cloud LLM researcher for automated_lab.

Provider order is explicit and boring on purpose:
1. OpenRouter (default model: NVIDIA Nemotron 3 Super 120B if key exists)
2. Ollama Cloud (default model: nemotron-3-super if OLLAMA_API_KEY exists)
3. NVIDIA NIM (if NVIDIA_API_KEY/NIM_API_KEY exists)

The researcher is NOT used for numeric DTI inference. It only proposes/ranks
hypotheses and writes the morning interpretation so the local scientific backend
stays reproducible.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str
    api_key: str
    model: str


def _env_first(*names: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return ""


def resolve_provider(preferred: str | None = None) -> ProviderConfig | None:
    """Resolve the cloud provider for the investigator.

    `AUTOMATED_LAB_PROVIDER` can be one of: ollama-cloud, ollama, openrouter,
    nvidia-nim, nim, auto. In auto mode we prefer OpenRouter if available for
    Nemotron 3 Super 120B, otherwise Ollama Cloud, then NIM.
    """

    pref = (preferred or os.getenv("AUTOMATED_LAB_PROVIDER", "auto")).strip().lower()

    candidates: list[ProviderConfig] = []
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
    if openrouter_key:
        candidates.append(
            ProviderConfig(
                name="openrouter",
                base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
                api_key=openrouter_key,
                model=os.getenv(
                    "AUTOMATED_LAB_MODEL",
                    os.getenv("OPENROUTER_GENERATOR_MODEL", "nvidia/nemotron-3-super-120b-a12b:free"),
                ),
            )
        )

    ollama_key = os.getenv("OLLAMA_API_KEY", "")
    if ollama_key:
        candidates.append(
            ProviderConfig(
                name="ollama-cloud",
                base_url=os.getenv("OLLAMA_BASE_URL", "https://ollama.com/v1"),
                api_key=ollama_key,
                model=os.getenv("AUTOMATED_LAB_MODEL", os.getenv("OLLAMA_GENERATOR_MODEL", "nemotron-3-super")),
            )
        )

    nim_key = _env_first("NVIDIA_API_KEY", "NIM_API_KEY")
    if nim_key:
        candidates.append(
            ProviderConfig(
                name="nvidia-nim",
                base_url=os.getenv("NVIDIA_NIM_BASE_URL", os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")),
                api_key=nim_key,
                model=os.getenv("AUTOMATED_LAB_MODEL", os.getenv("NIM_MODEL", "nvidia/nemotron-3-super-120b-a12b")),
            )
        )

    if pref in {"ollama", "ollama-cloud"}:
        return next((c for c in candidates if c.name == "ollama-cloud"), None)
    if pref in {"openrouter", "open-router"}:
        return next((c for c in candidates if c.name == "openrouter"), None)
    if pref in {"nim", "nvidia", "nvidia-nim"}:
        return next((c for c in candidates if c.name == "nvidia-nim"), None)
    return candidates[0] if candidates else None


class CloudResearcher:
    """Small OpenAI-compatible client implemented with curl.

    Curl is used intentionally because Ollama Cloud endpoint handling has been
    more reliable with `-L` than Python urllib/http stacks in this WSL setup.
    """

    def __init__(self, provider: ProviderConfig | None = None):
        self.provider = provider or resolve_provider()

    @property
    def available(self) -> bool:
        return self.provider is not None

    def chat(self, prompt: str, *, system: str | None = None, max_tokens: int = 1800,
             temperature: float = 0.2, timeout: int = 90) -> str | None:
        if not self.provider:
            return None
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": self.provider.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        cmd = [
            "curl", "-s", "-L", "--max-time", str(timeout),
            f"{self.provider.base_url.rstrip('/')}/chat/completions",
            "-H", f"Authorization: Bearer {self.provider.api_key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload),
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        except Exception:
            return None
        if proc.returncode != 0 or not proc.stdout.strip():
            return None
        try:
            data = json.loads(proc.stdout)
            return data["choices"][0]["message"].get("content") or None
        except Exception:
            return None

    def summarize_results(self, campaign: dict[str, Any], results: list[dict[str, Any]]) -> str | None:
        top = sorted(
            [r for r in results if r.get("status") == "ok" and "pkd" in r],
            key=lambda r: r.get("pkd", 0), reverse=True,
        )[:25]
        provider = self.provider.name + "/" + self.provider.model if self.provider else "none"
        prompt = f"""
Eres el investigador nocturno de DAVI para protein-lab. No inventes papers ni afirmes causalidad clínica.
Campaña: {campaign.get('title') or campaign.get('campaign')}
Objetivo: {campaign.get('objective')}
Provider/modelo: {provider}

Resultados DTI top (modelo MAMMAL; pKd predicho, no validación experimental):
{json.dumps(top, ensure_ascii=False, indent=2)[:12000]}

Escribe una revisión breve en español con:
1. Hallazgos robustos dentro de esta corrida.
2. Señales sospechosas / posibles sesgos del modelo.
3. 5 próximos experimentos computacionales concretos.
4. Qué NO concluir todavía.
""".strip()
        return self.chat(prompt, max_tokens=2200, temperature=0.15)
