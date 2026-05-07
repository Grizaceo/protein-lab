#!/usr/bin/env python3
"""
Mixture of Experts (MoE) Peer Review para Protein Lab
====================================================
Envía un artefacto de diseño a múltiples modelos LLM como "expertos"
y recopila sus opiniones/críticas/mejoras de forma estructurada.

Uso:
  source ~/.hermes/.env
  python3 moe_review.py --artefact DESIGN_ARTEFACT_V3_TRIPODE.md --rounds 1
"""

import os
import sys
import json
import argparse
import requests
import time
from datetime import datetime
from pathlib import Path

# --- Configuración de Expertos ---
EXPERTS = [
    {
        "name": "Prof. Nemotron (NVIDIA NIM)",
        "role": "Biofísico computacional - especialista en simulación molecular y dinámica de proteínas",
        "provider": "nvidia",
        "model": "nvidia/llama-3.3-nemotron-super-49b-v1",
        "base_url": "https://integrate.api.nvidia.com/v1",
        "api_key_env": "NVIDIA_API_KEY",
    },
    {
        "name": "Dra. DeepSeek (Ollama Cloud)",
        "role": "Química inorgánica y nanomateriales - experta en clusters metálicos y autofinidades Au-S",
        "provider": "ollama",
        "model": "deepseek-v3.2",
        "base_url": "https://ollama.com/v1",
        "api_key_env": "OLLAMA_API_KEY",
    },
    {
        "name": "Dr. Qwen (Ollama Cloud)",
        "role": "Ingeniero de materiales bio-híbridos - especialista en interfaces proteína-metal y viabilidad experimental",
        "provider": "ollama",
        "model": "glm-5.1",
        "base_url": "https://ollama.com/v1",
        "api_key_env": "OLLAMA_API_KEY",
    },
]

SYSTEM_PROMPT_TEMPLATE = """Eres {name}. Tu rol en este panel es: {role}

Se te presentará un diseño de un procesador bio-híbrido. Tu trabajo es hacer una REVISIÓN ADVERSARIAL RIGUROSA. No seas complaciente. Si algo es irreal o fantasioso, dilo claramente.

Responde en español con esta estructura EXACTA:

## VEREDICTO GENERAL
[VIABLE / DUDOSO / IRREAL] - Una palabra

## PUNTOS FUERTES (lo que es real y bien fundamentado)
- ...

## PUNTOS DÉBILES (lo que es dudoso o fantasioso)
- ...

## FATAL FLAWS (si hay algo que hace insalvable el diseño)
- ...

## SUGERENCIAS DE MEJORA
- ...

## CONFIANZA EN EL DISEÑO
[1-10] donde 1="cabeceando mojones, pura fantasía" y 10="diseño publicable en Nature Nanotech hoy"

Se explícito sobre qué partes del diseño tienen respaldo publicado y cuáles son extrapolaciones no verificadas.
"""

USER_PROMPT_TEMPLATE = """Aquí está el artefacto de diseño para tu revisión:

---
{artefact}
---

PREGUNTAS ESPECÍFICAS para tu expertise:
1. ¿Es realista que 3 mutaciones a Cys anclen mecánicamente un Au55 sin desnaturalizar la Ferritina?
2. ¿La diferencia de potencial nativa ARG+/GLU- sobrevive después de que ambos se mutan a Cys? (Al mutar se pierde la carga original)
3. ¿Es el salto de 12.16 Å demasiado optimista para tunelamiento eficiente a 37°C?
4. ¿Hay precedentes publicados reales de clusters Au55 dentro de ferritinas?
5. ¿La posición asimétrica del Au55 dentro del lumen es estable sin dinámica molecular explícita?

Responde con rigor científico. No me ahorres la mala noticia."""


def call_api(expert, system_prompt, user_prompt):
    """Llama a la API del modelo experto."""
    api_key = os.environ.get(expert["api_key_env"], "")
    if not api_key:
        return None, f"API key no encontrada: {expert['api_key_env']}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": expert["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 3000,
    }

    try:
        resp = requests.post(
            f"{expert['base_url']}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )
        if resp.status_code == 200:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            # Track token usage
            usage = data.get("usage", {})
            return content, None, usage
        else:
            return None, f"HTTP {resp.status_code}: {resp.text[:300]}", {}
    except Exception as e:
        return None, f"Error: {str(e)[:300]}", {}


def run_review(artefact_path, rounds=1, output_dir=None):
    """Ejecuta la revisión MoE completa."""

    # Cargar artefacto
    artefact = Path(artefact_path).read_text()

    # Output dir
    if output_dir is None:
        output_dir = Path(__file__).resolve().parent / "generated" / "reviews"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    all_reviews = []
    total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    print(f"{'='*60}")
    print(f"MoE PEER REVIEW - Ronda {rounds}")
    print(f"Artefacto: {artefact_path}")
    print(f"Expertes: {len(EXPERTS)}")
    print(f"{'='*60}\n")

    for expert in EXPERTS:
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            name=expert["name"], role=expert["role"]
        )
        user_prompt = USER_PROMPT_TEMPLATE.format(artefact=artefact)

        print(f"Consultando {expert['name']} ({expert['model']})...")
        content, error, usage = call_api(expert, system_prompt, user_prompt)

        if content:
            print(f"  OK - Respuesta recibida ({len(content)} chars)")
            review = {
                "expert": expert["name"],
                "model": expert["model"],
                "role": expert["role"],
                "content": content,
                "timestamp": timestamp,
                "usage": usage,
            }
            all_reviews.append(review)

            # Track usage
            for key in total_usage:
                total_usage[key] += usage.get(key, 0)

            # Guardar review individual
            safe_name = expert["name"].replace(" ", "_").replace("(", "").replace(")", "")
            review_file = output_dir / f"{timestamp}_{safe_name}.md"
            review_file.write_text(f"# Review: {expert['name']}\n## Rol: {expert['role']}\n## Modelo: {expert['model']}\n\n{content}\n")
        else:
            print(f"  ERROR - {error}")

        # Rate limiting entre expertos
        time.sleep(2)

    # --- CONSOLIDAR ---
    print(f"\n{'='*60}")
    print("CONSOLIDACIÓN DE REVIEWS")
    print(f"{'='*60}\n")

    consolidation = consolidate_reviews(all_reviews)

    # Guardar consolidación
    consol_file = output_dir / f"{timestamp}_CONSOLIDATION.md"
    consol_file.write_text(consolidation)
    print(f"\nConsolidación guardada en: {consol_file}")

    # Guardar JSON completo
    json_file = output_dir / f"{timestamp}_reviews.json"
    with open(json_file, "w") as f:
        json.dump({"timestamp": timestamp, "artefact": str(artefact_path), "reviews": all_reviews, "consolidation": consolidation, "usage": total_usage}, f, indent=2, ensure_ascii=False)

    # Print consolidation
    print(consolidation)

    return all_reviews, consolidation


def consolidate_reviews(reviews):
    """Consolida las reviews de todos los expertos en un veredicto final."""

    lines = ["# CONSOLIDACIÓN MoE - VEREDICTO FINAL\n"]
    lines.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Expertos consultados: {len(reviews)}\n")

    # Extraer veredictos y confianzas
    verdicts = []
    confidences = []

    for r in reviews:
        content = r["content"]
        lines.append(f"---\n## {r['expert']} ({r['model']})\n")
        lines.append(content)
        lines.append("")

        # Intentar extraer veredicto y confianza
        for line in content.split("\n"):
            if "VEREDICTO GENERAL" in line.upper():
                # Next non-empty line
                pass
            if any(v in line.upper() for v in ["VIABLE", "DUDOSO", "IRREAL"]):
                if "VIABLE" in line.upper() and "DUDOSO" not in line.upper():
                    verdicts.append("VIABLE")
                elif "DUDOSO" in line.upper():
                    verdicts.append("DUDOSO")
                elif "IRREAL" in line.upper():
                    verdicts.append("IRREAL")
            # Extraer confianza numérica
            import re
            conf_match = re.search(r'(?:confianza|CONFIANZA).*?(\d+)[/\s]', line)
            if conf_match:
                confidences.append(int(conf_match.group(1)))

    # Resumen ejecutivo
    lines.append("\n---\n## RESUMEN EJECUTIVO\n")
    lines.append(f"Veredictos individuales: {verdicts if verdicts else 'No extraídos automáticamente'}")
    if confidences:
        lines.append(f"Confianza promedio: {sum(confidences)/len(confidences):.1f}/10")
        lines.append(f"Rango de confianza: {min(confidences)}-{max(confidences)}/10")
    else:
        lines.append("Confianza: Ver reviews individuales arriba")

    if verdicts:
        if all(v == "VIABLE" for v in verdicts):
            final = "VIABLE - Consenso unánime"
        elif any(v == "IRREAL" for v in verdicts):
            final = "IRREAL - Al menos un experto considera el diseño insalvable"
        else:
            final = "DUDOSO - Requiere más validación antes de proceder"
        lines.append(f"\nVEREDICTO CONSOLIDADO: {final}")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MoE Peer Review para Protein Lab")
    parser.add_argument("--artefact", required=True, help="Ruta al artefacto de diseño")
    parser.add_argument("--rounds", type=int, default=1, help="Rondas de revisión")
    parser.add_argument("--output-dir", default=None, help="Directorio de salida")
    args = parser.parse_args()

    # Cargar .env
    env_file = Path.home() / ".hermes" / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

    run_review(args.artefact, args.rounds, args.output_dir)