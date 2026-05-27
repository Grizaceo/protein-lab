# Blueprint de Flujo de Campaña: protein-lab (EaC Bridge + World Model)

Blueprint formal de ejecución nocturna diseñado bajo la metodología `modelar-flujo-skills`.

---

## Fases del Pipeline Científico

```
 FASE 1: Literature Grounding
   └── combined_literature: CombinedLiteratureProvider
   └── check: Grounding contra GROUNDING.md (Filtro de citas falsas)

 FASE 2: Brute Hypothesis Generation (KISS style)
   └── generator: BruteHypothesisGenerator (Async parallel generations)
   └── filter: FalsifierAdversary (Static + Heuristic LLM check)

 FASE 3: Surrogate World Model Pruning
   └── model: LocalWorldModel (k-NN prediction + Novelty Scorer)
   └── select: UCB + epsilon-greedy select_top_k (Filtra a Top-K)

 FASE 4: Co-Scientist Peer-Review
   └── reviewer: LLMReasoningBridge (Strengths, weaknesses, risks & scoring)
   └── ranker: TournamentRanker/Heuristic ranking descending

 FASE 5: Experiment Compilation
   └── compiler: ProteinLabCompiler (Translates specs to lowers commands)
   └── check: safety_hooks (RTX 4060 VRAM limits + cron overlap prevention)

 FASE 6: Physical Execution & Feedback Loop
   └── executor: ProteinLabExecutor (MAMMAL local, Colab folding, BioMaterialCAD)
   └── ledger: SQLite WAL research_ledger (Updates real scores & surprise errors)
```

---

## Detalle de Fases y Transición de Estados

### Fase 1: Grounding Bibliográfico
* **Skills involucrados:** native `pubmed-database`, native `literature-search-arxiv`, local `grounding_parser`.
* **Criterio de salida (Gate):** 100% de citas citadas cuentan con PMID/DOI real y verificado. Cualquier cita catalogada como "FALSA" en `GROUNDING.md` causa un rechazo automático del candidato.

### Fase 2: Generación Bruta de Hipótesis
* **Skills involucrados:** custom `ollama-cloud-llm-backend` (Reasoning Bridge), custom `falsifier` (NIM Adversary).
* **Criterio de salida (Gate):** Generación paralela asíncrona de 10 candidatos. Descarte inmediato de alucinaciones obvias (ej. "Au25 dentro de ferritina cage") mediante checks estáticos.

### Fase 3: Poda de Candidatos por World Model
* **Skills involucrados:** local `world_model` (Surrogate layer), local `ledger` (WAL k-NN observations).
* **Criterio de salida (Gate):** Selección de las mejores $K$ hipótesis usando UCB (`fitness_hat + 0.5 * uncertainty`). Registro de la predicción en el ledger para control de sorpresas métricas.

### Fase 4: Peer-Review de Co-Scientist
* **Skills involucrados:** custom `reasoning` (Swarm Peer-Reviewer).
* **Criterio de salida (Gate):** Cada hipótesis seleccionada cuenta con un `ReviewBatch` válido detallando fortalezas, debilidades, riesgos de cómputo y puntuación global.

### Fase 5: Compilación y Seguridad
* **Skills involucrados:** EaC `ExperimentCompiler`, custom `safety` (Harness & WSL monitor).
* **Criterio de salida (Gate):** `plan.ok == True`. Ausencia de errores de VRAM (plegado con ESMFold bloqueado en RTX 4060) y adquisición exitosa del lock de concurrencia `flock` para evitar solapamientos en cron.

### Fase 6: Corrida y Bucle de Aprendizaje
* **Skills involucrados:** native `ExperimentRunner` (MAMMAL DTI), custom `colab_bridge`, local `BioMaterialCAD`.
* **Criterio de salida (Gate):** Registro del pKd real (MAMMAL) o Ihara Zeta/GUE Beta (cadena CAD) en el ledger. Ticking de calibración de shadow mode en el World Model. Generación del morning report `REPORTE_MANANA.md`.
