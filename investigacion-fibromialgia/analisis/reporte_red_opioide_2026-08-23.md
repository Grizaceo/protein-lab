# Informe de estado — Infraestructura de red del eje opioide (protein-lab)

**Fecha:** 2026-08-23 · **Tipo:** informe de estado verificable (sin cierre de líneas, sin preprint)
**Fuentes (leídas tal cual, no modificadas):**
- `experiments/gnn_architecture_v1.json` — grafo 48 nodos / 61 aristas, GraphSAGE_mean 2 capas
- `experiments/ora_gprofiler_v1.json` — ORA g:Profiler, 49 genes, 80 términos significativos
- `experiments/string_network_v1.json` — red STRING v12, 61 interacciones, confidence_threshold 700
- `experiments/string_ids_v1.json` — 48 STRING IDs resueltos (Homo sapiens 9606)

---

## (a) Genes `is_opioid=True` en el grafo — grado y conectividad

El grafo `gnn_architecture_v1` tiene 48 nodos, 61 aristas (densidad 0.054, peso = STRING combined_score). De los 48 genes, **9 están marcados `is_opioid=True`**:

| Gene | idx | Grado (total) | Aristas puente a no-opioides | Score máx. |
|------|-----|---------------|------------------------------|------------|
| DRD2 | 0 | 10 | PPP2R2B (0.913), NCAM1 (0.625), HDC (0.499), HTT (0.455) | 0.913 |
| NPY | 7 | 10 | MLN (0.595), HDC (0.445) | 0.986 |
| TAC1 | 13 | 8 | MLN (0.824) | 0.999 |
| POMC | 16 | 8 | MLN (0.434) | 0.999 |
| OPRM1 | 18 | 8 | — | 0.999 |
| PNOC | 15 | 8 | — | 0.915 |
| PENK | 14 | 7 | — | 0.999 |
| OPRD1 | 19 | 5 | — | 0.988 |
| TACR1 | 17 | 4 | — | 0.999 |

**Subgrafo opioide-opioide:** 30 de las 61 aristas (49%) conectan genes opioides entre sí; 22 de esas
tienen score ≥ 0.7 (alta confianza). El núcleo es un clúster denso: PENK–OPRM1 (0.999), POMC–OPRM1 (0.999),
TAC1–TACR1 (0.999), PENK–POMC (0.988), NPY–POMC (0.986), PENK–OPRD1 (0.984).

**Puentes opioide → resto del grafo (8 aristas):** DRD2–PPP2R2B (0.913) y TAC1–MLN (0.824) son los únicos
puentes de alta confianza. DRD2 es el hub dopaminérgico que conecta el módulo opioide con genes
no-opioides (PPP2R2B, NCAM1, HDC, HTT).

**Discrepancia de etiquetado detectada (honestidad):** el módulo opioide 1 de STRING (`string_network_v1`)
tiene 11 genes: OPRD1, PNOC, TACR1, TAC1, DRD2, PPP2R2B, POMC, NPY, MLN, OPRM1, PENK. Pero en el grafo
solo 9 de esos 11 tienen `is_opioid=True`: **MLN y PPP2R2B no llevan el flag** (aunque están en el módulo
STRING). Además, el grafo (48 nodos) **no contiene OPRK1**, que sí está en el gene set de ORA (49 genes).
Los `string_ids_v1.json` (48 IDs) tampoco incluyen OPRK1; sí incluyen LEG1/C6orf58.

## (b) Hallazgos ORA (g:Profiler, `ora_gprofiler_v1.json`)

Tool: g:GOSt REST API, tool_version `e114_eg62_p19_27110d83`, organismo **hsapiens**, método g_SCS,
threshold 0.05. Input 49 genes, **80 términos significativos**. Top pathways con p-valores:

| # | Fuente | Pathway | p-value | Genes intersección |
|---|--------|---------|---------|--------------------|
| 1 | GO:BP | neuropeptide signaling pathway (GO:0007218) | **1.29e-07** | 8 |
| 2 | REAC | Peptide ligand-binding receptors (R-HSA-375276) | 3.68e-07 | 10 |
| 3 | KEGG | Neuroactive ligand signaling (04082) | 2.51e-06 | 9 |
| 4 | KEGG | Neuroactive ligand-receptor interaction (04080) | 3.97e-06 | 11 |
| 5 | REAC | Class A/1 (Rhodopsin-like) receptors (R-HSA-373076) | 4.13e-06 | 11 |
| 6 | GO:BP | behavior (GO:0007610) | 1.50e-05 | 12 |
| 7 | GO:BP | **GPCR opioid receptor signaling** (GO:0038003) | 1.58e-05 | 4 |
| 8 | GO:BP | synapse (GO:0045202) | 3.26e-05 | 16 |
| 9 | GO:BP | response to nicotine | 7.95e-05 | 5 |
| 10 | GO:BP | synaptic signaling | 1.20e-04 | 12 |

Pathways específicamente opioides detectados (sección `opioid_pathways` del JSON):
- GPCR opioid receptor signaling (GO:0038003): p=1.58e-05, 4 genes
- GPCR opioid receptor activity (GO:0004985): p=1.85e-04, 3 genes
- opioid peptide activity: p=1.43e-02, 2 genes

Además `neuropeptide_pathways`: neuropeptide signaling (1.29e-07), neuropeptide hormone activity (1.86e-02),
neuropeptide activity (2.06e-02), neuropeptide binding (2.51e-02), neuropeptide receptor binding (3.59e-02).

Veredicto del experimento: `POSITIVE_ENRICHMENT`; falsificación `NOT_APPLICABLE_ENRICHMENT_FOUND` — el gene
set causal UKB está significativamente enriquecido en pathways neuropeptídicos/opioides. Nota del propio JSON:
"NO prueba funcionalidad en PBMC".

## (c) Veredicto honesto

Esta infraestructura aporta una **base estructural verificable** al claim de convergencia dopaminérgica/opioide:
(i) el módulo STRING-1 de 11 genes nuclea a los 9 genes `is_opioid=True` con 30 aristas internas de alta
confianza (más de la mitad de la red), y DRD2 — el representante dopaminérgico — es hub del grafo (grado 10)
con puentes de alta confianza hacia el módulo opioide (DRD2–PPP2R2B 0.913, DRD2–NPY 0.833) y hacia el resto de
la red; (ii) la ORA independiente enriquece neuropeptide signaling (p=1.29e-07) y GPCR opioid signaling
(p=1.58e-05) con el gene set causal; (iii) el grafo queda listo como entrada de GNN (GraphSAGE, spec hash
registrado). Sin embargo **no alcanza**: no hay un GNN entrenado (el JSON es `ARCHITECTURE_READY`, no hay
métricas de clasificación); STRING es evidencia de interacción anotada, no funcional ni transcriptómica, y el
propio ORA advierte que no prueba funcionalidad en PBMC; la convergencia dopaminérgica–opioide permanece como
**hipótesis topológica** (DRD2 es un nodo conector, no una demostración de mecanismo compartido); y el
análisis STRING (`string_network_v1`) **falsifica parcialmente** la convergencia directa de COL9A1 y PTN con
el módulo opioide (0 interacciones de alta confianza con él), sugiriendo ejes paralelos (neuropéptido +
matriz extracelular + señalización neural) más que un único módulo convergente. Sin validación de expresión
correlacionada en PBMC de FM (p. ej., GSE67311) ni entrenamiento del GNN, **no alcanza** para sostener el
claim de convergencia como mecanismo.

## (d) Siguiente experimento sugerido (CPU-only)

1. **Entrenamiento del GNN en CPU** (prioridad): el grafo es pequeño (48 nodos, 61 aristas) y cabe sin GPU.
   Correr el GraphSAGE de `gnn_architecture_v1` con PyTorch + PyTorch Geometric en CPU, split
   train/val/test sobre los 9 nodos `is_opioid=True` vs el resto (clase minoritaria, usar balanced
   sampling/weighted loss), reportando precisión/recall/F1 y matriz de confusión. Verificable: si el F1
   supera el baseline de clase mayoritaria y la atención se concentra en el subgrafo 13-19, la topología
   apoya el módulo opioide; si no, **falsifica** la utilidad del grafo para este claim.
2. **Segundos vecinos de COL9A1/PTN** (networkx, sin GPU): medir distancia de caminos más corta desde
   COL9A1/PTN al módulo opioide y listar los intermediarios (p. ej., vía NCAM1/COL18A1). Responde la
   pregunta abierta de `string_network_v1` ("¿conexión indirecta a través de segundos vecinos?") y decide
   si hay un camino topológico dopaminérgico–opioide–estructural con el que valga seguir.

Ningún JSON fue modificado; no se tocaron preprints; sin commits.
