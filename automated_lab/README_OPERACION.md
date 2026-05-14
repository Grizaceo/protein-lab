# Automated Lab — Operación nocturna

Estado: v2 operativo (2026-05-14).

## Qué hace

1. Carga una campaña desde `campaign_briefs/*.json`.
2. Genera una cola de experimentos DTI usando:
   - grilla local reproducible de `drugs_smiles × targets`, y
   - KISS Discovery Engine como ranker opcional de hipótesis si hay provider cloud.
3. Ejecuta MAMMAL DTI local en batch mediante el Python del conda env `protein-lab`.
4. Guarda resultados por ciclo con IDs estables por `(campaign, type, drug, target)`.
5. Escribe `REPORTE_MANANA.md` con tabla pKd y revisión del investigador cloud.

## Provider investigador

Default nocturno:

```bash
AUTOMATED_LAB_PROVIDER=ollama-cloud
AUTOMATED_LAB_MODEL=nemotron-3-super
OLLAMA_BASE_URL=https://ollama.com/v1
```

Fallbacks soportados en código:

- OpenRouter: `OPENROUTER_API_KEY`, modelo default `nvidia/nemotron-3-super-120b-a12b:free`.
- Ollama Cloud: `OLLAMA_API_KEY`, modelo default `nemotron-3-super`.
- NVIDIA NIM: `NVIDIA_API_KEY` o `NIM_API_KEY`, modelo default `nvidia/nemotron-3-super-120b-a12b`.

El investigador cloud no ejecuta biología ni inventa SMILES. Solo prioriza hipótesis y resume resultados. El backend científico sigue siendo MAMMAL local.

## Comandos

Smoke reproducible sin KISS:

```bash
cd ~/.hermes/workspace/protein-lab/automated_lab
AUTOMATED_LAB_USE_KISS=0 python -m engine.scheduler --campaign fibromialgia_ruta_b --max-experiments 4
```

Smoke con KISS + Ollama Cloud/Nemotron:

```bash
cd ~/.hermes/workspace/protein-lab/automated_lab
python - <<'PY'
from idea_generation.generator import IdeaGenerator
ideas = IdeaGenerator().generate('fibromialgia_ruta_b', count=4, campaign={
  'campaign': 'fibromialgia_ruta_b',
  'primary_targets': ['MOR'],
  'secondary_targets': ['MS4A2', 'FCER1A', 'HDC'],
  'drugs_smiles': {'naltrexona_LDN': 'C=CCN1CCC23C4C(=O)CCC2(C1CC5=C3C(=C(C=C5)O)O4)O'}
})
print([(i['drug_name'], i['target'], i['source']) for i in ideas])
PY
```

Corrida nocturna manual:

```bash
cd ~/.hermes/workspace/protein-lab/automated_lab
bash scripts/run_overnight.sh fibromialgia_ruta_b 8
```

Con límite explícito:

```bash
bash scripts/run_overnight.sh fibromialgia_ruta_b 8 44
```

## Cautelas científicas

- pKd de MAMMAL = predicción computacional, no evidencia clínica.
- Biologics sin SMILES no son válidos para este backend DTI.
- Nav1.8 queda excluido del DTI local por longitud; requiere Colab/sliding-window.
- No promover targets sin checkpoint DOI/PMID/PMC.

## Auditoría hecha

Problemas corregidos:

1. IDs de experimento eran `exp_00000000` porque `title` venía vacío; los JSON se pisaban entre sí.
2. `--overnight`/`--hours` podía inducir corridas largas por default; ahora one-shot es seguro y la noche debe ser explícita.
3. El scheduler ignoraba `max_experiments` y no guardaba cola completa.
4. Resultados batch no incluían metadata completa (`backend`, `experiment_id`, `timestamp`).
5. KISS necesitaba `max_tokens` configurable y corrección del logging `await resp.text()[:200]`.
6. `automated_lab/results/` estaba listo para contaminar git; ahora está ignorado.
