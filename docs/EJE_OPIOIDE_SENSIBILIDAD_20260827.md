# Síntesis: sensibilidad del eje opioide — ESM3-OPRM1 vs ablación GNN

**Fecha:** 2026-08-27 · **Tarea kanban:** protein-2 · **Fuentes:** `experiments/esm3_oprm1_v3.json` y `experiments/ablacion_gnn_v3_20260823.json`

> Regla de esta síntesis: todo valor citado existe literalmente en los JSON fuente, con el nombre de campo exacto. No se ha inferido, promediado ni extrapolado ningún número.

---

## 1. Qué es cada experimento (y qué no es)

### 1.1 `esm3_oprm1_v3.json` — un SPEC, no un resultado

| Campo (nombre exacto) | Valor literal |
|---|---|
| `experiment_id` | `"esm3_oprm1_v2"` |
| `status` | `"SPEC_V3_READY_PENDING_COLAB"` |
| `target_protein.gene` / `uniprot_id` / `length` | `"OPRM1"` / `"P35372"` / `400` |
| `target_protein.declared_vs_actual.matches_uniprot` | `true` |
| `evaluation.primary_metric` / `tool` | `"ddG_folding"` / `"FoldX 5.0"` |
| `evaluation.secondary_metric` / `tool_secondary` | `"docking_affinity"` / `"AutoDock Vina"` |
| `evaluation.control_set` | `"mutated_70pct N=30 (seed=42) AND mutated_70pct_compmatched N=30 (seed=42) — two control arms at identical Hamming distance"` |
| `evaluation.n_controls_preregistered` / `n_esm3_variants_preregistered` | `30` / `20` |
| `evaluation.statistical_test` / `alpha` | `"Mann-Whitney U"` / `0.05` |
| `esm3_generation.status` | `"PENDING_COLAB — dataset v2, human receptor, two control arms"` |
| `esm3_generation.identity_range` | `"70-90%"` |

**El experimento ESM3 no ha corrido.** El propio registro lo declara en `known_limitations`: *"ESM3 has not run. Every number in this spec is a plan, not a measurement."* No existe ningún ddG medido, ningún p-value, ninguna afinidad de docking en este JSON. La corroboración indirecta: `spec_hash` y `result_hash` son idénticos (`sha256:0b4129db219b7fb82c40dba8685b6b7ec33dff2d963babf7cd2c76a2beb99fc3`) — no hay resultados que hash-izar.

Lo que sí aporta el registro, a nivel de diseño (plan, no medición):

- **Criterio de falsación preregistrado** (`falsification_criteria.rejection_criteria`): `"Mann-Whitney p < 0.05 AND rank-biserial r > 0.3 against BOTH control arms"`. La hipótesis H1 es que variantes ESM3 de OPRM1 tienen ddG más favorable que mutantes aleatorios emparejados por Hamming.
- **Anti optional-stopping** (`evaluation.optional_stopping`): `"PROHIBITED. N fijado antes de ejecutar."`
- **Cobertura estructural declarada** (`evaluation.structure_coverage_caveat`): 8EFO modela residuos 2..368 de 400; mutaciones fuera de ese rango quedan **excluidas de la métrica primaria y contadas explícitamente**. `known_limitations` lo cuantifica: *"8EFO models 367 of 400 residues (2..368)"*.
- **Corrección de defectos graves** (`defect_corrected_v3`, `defect_corrected_v4`): el target original era un fragmento shuffled de 53 caracteres, no OPRM1; el receptor 6DDE era murino (Mus musculus P42866) y fue reemplazado por 8EFO humano (2.8 Å, ligando 8QY/PZM21) con replicado 8EF5 (7V7/fentanilo).
- **Brazo de control verificado** (`control_arm_status.verdict`): `"SOUND, reusable"` — consenso de 100 controles `mutated_70pct` == UniProt P35372 con identidad 100.0%; identidad por control exactamente 70.0% (n=100); shuffled 6.0% mean, uniform 4.9% mean.
- **Encuadre fibromialgia retirado** (`fibromyalgia_framing.status`): `"REMOVED"` — `string_indirect_path_opioid_ecm_v1` (pre-registrado, N=1000) falsó la hipótesis de rutas paralelas: el módulo opioide está más lejos de COL9A1/PTN que el azar conservando grado (`p_far=0.001`).

### 1.2 `ablacion_gnn_v3_20260823.json` — ablación medida y completa

| Campo (nombre exacto) | Valor literal |
|---|---|
| `experiment` | `"ablacion_gnn_v3"` |
| `linea` | `"eje_opioide_fibromialgia"` |
| `archivo_origen_datos` | `"gnn_architecture_v1.json (48 nodos, 61 aristas) + /tmp/ora_genes.json (g:Profiler)"` |
| `protocolo_reproducido` | GraphSAGE mean 2 capas, CrossEntropy weighted [1.0, 3.8], 300 epochs fijas SIN early stopping, LOO sobre los 10 positivos, seed 42 GNN / seed 3 MLP |
| `seeds_usadas` | GNN `[42, 7, 2026]`, MLP `[3, 7, 2026]` |
| `estabilidad` | `"las 3 seeds dan el mismo recall en todas las configs (media == valor reportado)."` |

Resultados por configuración (campos `id`, `recall_pos_LOO`, `f1_macro` del array `configuraciones`):

| Config | `features` | `recall_pos_LOO` | `f1_macro` | Nota clave (del campo `nota`) |
|---|---|---|---|---|
| `gnn_full` | degree + e_value + ora_score | 1.0 | 1.0 | predice exactamente 10 nodos; PPP2R2B prob 0.0085 |
| `gnn_no_ora` | degree + e_value | 1.0 | 0.9695 | 11 predichos; PPP2R2B 0.26; reproduce f1 v2 (0.9695) |
| `gnn_degree` | degree | 1.0 | 0.9142 | predice 13 nodos; PPP2R2B POSITIVO (0.63) — espurio |
| `gnn_ora` | ora_score | 1.0 | 0.8196 | 17 predichos; PPP2R2B negativo (0.41, margen bajo) |
| `gnn_evalue` | e_value | 1.0 | 0.553 | feature CONSTANTE (e_value=0.0 en los 48 nodos); predice 31/48 positivos; PPP2R2B 0.64 — LOO 10/10 APARENTE |
| `mlp_full` | 3 features sin aristas | 0.9 | 0.8333 | falla MLN (0.30) y OPRD1 al borde (0.50) |
| `mlp_ora` | ora_score sin topología | 0.7 | 0.5781 | falla OPRM1 (0.29), OPRD1 (0.29), DRD2 (0.41) |

Campos de resumen del propio JSON:

- `mejor`: `gnn_full`, criterio `"unica config con prediccion exacta (10 predichos, PPP2R2B 0.0085) y f1 perfecto."`
- `peor`: `mlp_ora`, criterio `"menor recall LOO y menor f1; control sin topologia con la unica feature que aporta."`
- `veredicto` (extracto literal): *"La feature que mas aporta es claramente ora_score_funcional … La topologia SÍ aporta sobre las features (GNN full 10/10 con f1 1.0 vs MLP full 9/10, rescatando OPRD1 0.50->0.97 y MLN 0.30->0.99), pero LA TOPOLOGIA SOLA (config e_value, con feature constante) NO codifica el eje: su LOO 10/10 es un artefacto de saturacion del peso de clase (predice 31/48 nodos positivos y PPP2R2B como positivo)."*
- `falsacion_protein7`: `"COMPLETA"` — doble vía: v2 con early-stopping daba LOO 0/10; v3 sin señal funcional satura la clase positiva (31/48 predichos, PPP2R2B positivo).

---

## 2. Comparación de robustez del eje opioide entre ambos enfoques

**No son comparables como resultados, porque uno no tiene resultados.** El registro ESM3 está en `status` `SPEC_V3_READY_PENDING_COLAB`: define métricas (`ddG_folding`, `docking_affinity`), brazos de control y criterio de rechazo, pero **no aporta ni un solo valor medido** sobre el eje. La ablación GNN sí está completa, con 7 configuraciones, 3 seeds por configuración y estabilidad declarada.

Lo que cada línea dice sobre la sensibilidad del eje opioide:

1. **GNN (medido): el eje NO es robusto a la representación.** Es sensible al contenido de las features de forma decisiva. Sin la feature funcional externa `ora_score` (de g:Profiler, ajena al grafo), el LOO 10/10 es un artefacto de saturación (`gnn_evalue`: f1_macro 0.553, 31/48 positivos predichos, PPP2R2B —nodo del módulo STRING pero NO opioide— clasificado positivo con prob 0.64). La topología sola codifica "la masa del módulo STRING", no el eje. Con ORA presente, la topología rescata nodos de feature débil (OPRD1 0.50→0.97, MLN 0.30→0.99), pero la señal discriminante es externa al grafo. El propio protocolo reconoce que el recall LOO satura y necesita el control duro PPP2R2B para discriminar.
2. **ESM3 (plan): robustez estructural del protocolo, no del eje.** El spec es metodológicamente cuidadoso (dos brazos de control a igual distancia de Hamming, N preregistrado, optional stopping prohibido, corrección de receptor murino→humano, cobertura estructural 2..368 declarada), pero hasta que corra en Colab no aporta evidencia ninguna sobre si el eje opioide es robusto en el espacio de secuencias.
3. **Contexto compartido que debilita la robustez del eje para FM:** en el registro ESM3, `fibromyalgia_framing.status` = `REMOVED` porque el análisis de red pre-registrado (N=1000) colocó el módulo opioide más lejos de COL9A1/PTN que el azar (`p_far=0.001`). La ablación GNN, por su parte, muestra que lo que "codifica el eje" es una anotación funcional externa, no la estructura de red. Ambas líneas apuntan en la misma dirección: la señal del eje opioide es frágil y depende de insumos externos (ORA, g:Profiler), no emerge de la topología ni está validada a nivel de secuencias.

---

## 3. Veredicto honesto

**La evidencia disponible NO alcanza para afirmar que el eje opioide sea robusto, y se dice explícitamente.** De los dos experimentos cruzados, uno (ESM3-OPRM1) es un spec preregistrado sin ejecutar —su propio `known_limitations` dice "ESM3 has not run"—, por lo que aporta cero medición sobre sensibilidad del eje a nivel de secuencias; solo demuestra que el protocolo pasó auditorías de diseño (gates, `control_arm_status` SOUND, defectos v3/v4 corregidos). El otro (ablación GNN) está completo y su resultado es más bien negativo para la robustez: el recall LOO 10/10 con topología sola es un artefacto de saturación del peso de clase (31/48 predichos, PPP2R2B positivo a 0.64), y el eje solo se codifica de forma discriminante cuando se inyecta la feature funcional externa `ora_score` (gnn_full 10/10, f1 1.0, PPP2R2B 0.0085), con estabilidad verificada solo sobre 3 seeds, un grafo de 48 nodos y 10 positivos — una base pequeña. Además, el encuadre fibromialgia del propio eje fue retirado (`p_far=0.001`). En resumen: existe evidencia sólida de que la codificación puramente topológica del eje opioide está **falsada** (doble vía, `falsacion_protein7` = "COMPLETA") y evidencia condicional de que depende críticamente de un insumo externo (ORA); no existe evidencia, medida o de secuencias, que permita afirmar robustez del eje. Cualquier afirmación de robustez a partir de estos registros sería un exceso.

---

## Apéndice: trazabilidad de campos

- **De `esm3_oprm1_v3.json`:** `experiment_id`, `status`, `status_notes`, `target_protein` (`gene`, `uniprot_id`, `length`, `declared_vs_actual.matches_uniprot`), `evaluation` (`primary_metric`, `tool`, `secondary_metric`, `tool_secondary`, `control_set`, `n_controls_preregistered`, `n_esm3_variants_preregistered`, `statistical_test`, `alpha`, `optional_stopping`, `structure_coverage_caveat`), `esm3_generation` (`status`, `identity_range`, `n_variants`), `falsification_criteria.rejection_criteria`, `known_limitations` (ítem 4: "ESM3 has not run…"), `control_arm_status` (`verdict`, `evidence`), `defect_corrected_v3`, `defect_corrected_v4`, `fibromyalgia_framing` (`status`, `reason`, `evidence`), `spec_hash`, `result_hash`.
- **De `ablacion_gnn_v3_20260823.json`:** `experiment`, `linea`, `timestamp`, `archivo_origen_datos`, `protocolo_reproducido`, `reconstruccion_features`, `configuraciones` (7 entradas con `id`, `features`, `recall_pos_LOO`, `f1_macro`, `nota`), `mejor`, `peor`, `veredicto`, `falsacion_protein7`, `seeds_usadas`, `estabilidad`.