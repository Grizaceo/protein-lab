# Auditoría de etiquetado del eje opioide — discrepancias y corrección (protein-lab)

**Fecha:** 2026-08-23 · **Tipo:** auditoría de etiquetado (sin papers, sin commits, sin preprints)
**Fuentes (leídas tal cual, no modificadas):**
- `experiments/ora_gprofiler_v1.json` — ORA g:Profiler, 49 genes input, 80 términos significativos
- `experiments/string_ids_v1.json` — 48 STRING IDs resueltos (Homo sapiens 9606)
- `experiments/string_network_v1.json` — red STRING v12, módulo opioide STRING-1 (11 genes)
- `experiments/gnn_architecture_v1.json` — grafo GNN 48 nodos / 61 aristas, GraphSAGE_mean

**Método:** lista canónica = (a) los 9 genes con `is_opioid=true` en `gnn_architecture_v1`; (b) OPRK1 y OPRL1
(receptores opioides clásicos); (c) genes del input ORA anotados a GO:0038003 (opioid receptor signaling) o
GO:0007218 (neuropeptide signaling). Conexión al módulo opioide = distancia de camino más corto (BFS) desde
los 9 genes flag=true, umbral ≤2. Todo verificado por script sobre los JSON (grados, BFS, componentes).

---

## (a) Tabla de genes disputados

| Gene | en_ORA (input) | en_grafo GNN | en string_ids | grado | flag_is_opioid | conexión_módulo_opioide |
|------|----------------|--------------|---------------|-------|----------------|--------------------------|
| OPRK1 | **SÍ** (pos. 20 de 49) | **NO** | NO | — | — (ausente) | **N/A — nodo inexistente** |
| OPRL1 | NO | NO | NO | — | — (ausente) | N/A — nunca fue parte del input |
| MLN | SÍ | SÍ | SÍ | 3 | **false** ⚠️ | **SÍ — dist 1** (TAC1 0.824, NPY 0.595, POMC 0.434) |
| PPP2R2B | SÍ | SÍ | SÍ | 2 | false | SÍ — dist 1 (DRD2 0.913) — pero no es eje funcional |
| DRD2 | SÍ | SÍ | SÍ | 10 | true | núcleo (dist 0) |
| NPY | SÍ | SÍ | SÍ | 10 | true | núcleo (dist 0) |
| TAC1 | SÍ | SÍ | SÍ | 8 | true | núcleo (dist 0) |
| PENK | SÍ | SÍ | SÍ | 7 | true | núcleo (dist 0) |
| PNOC | SÍ | SÍ | SÍ | 8 | true | núcleo (dist 0) |
| POMC | SÍ | SÍ | SÍ | 8 | true | núcleo (dist 0) |
| TACR1 | SÍ | SÍ | SÍ | 4 | true | núcleo (dist 0) |
| OPRM1 | SÍ | SÍ | SÍ | 8 | true | núcleo (dist 0) |

Contexto topológico: el módulo STRING-1 (`string_network_v1`) tiene 11 genes; de ellos 10 están en el grafo
(OPRD1, PNOC, TACR1, TAC1, DRD2, PPP2R2B, POMC, NPY, MLN, OPRM1, PENK — todos). El grafo tiene 61 aristas;
la componente conexa del núcleo opioide tiene 29 de 48 nodos; 19 nodos quedan aislados (GPR52, CAMKV, CELF4,
DCC, MDGA2, KYNU, SRD5A2, CA14, BTN2A1, CD302, CRELD1, DPEP1, C6orf58, PRSS53, BPIFB2, DDR1, FAM171B,
LRRC37A2, ST3GAL1).

Los genes de intersección exactos de GO:0038003 (int. 4 genes) y GO:0007218 (int. 8 genes) **no están
enumerados en `ora_gprofiler_v1.json`** (solo guarda `intersection_size`). Inferencia conservadora por anotación
GO estándar sobre el input de 49: GO:0038003 → OPRM1 + OPRD1 + OPRK1 + un 4º no enumerado (dado que OPRL1 no
está en el input); GO:0007218 → NPY, TAC1, POMC, PNOC, PENK, OPRM1, OPRD1, OPRK1, TACR1, MLN (8 de ellos). En
ambos términos **OPRK1 aparece por anotación** y en ninguno aparece OPRL1 (no estaba en el input ORA).

---

## (b) Veredicto honesto

**OMISIONES REALES de etiquetado (corregir en el próximo spec del grafo):**

1. **MLN — omisión real (flag `is_opioid=false` incorrecto).** Motilina, péptido del eje
   neuropéptido/opioide (anotación candidata a GO:0007218), miembro del módulo STRING-1 junto a los 9
   flag=true, y a distancia 1 del núcleo con aristas de confianza media-alta (TAC1–MLN 0.824, NPY–MLN
   0.595). Su `false` contradice el propio módulo; el label del GNN perdió un positivo verdadero. **Debe
   pasar a `is_opioid=true`.**
2. **OPRK1 — omisión del pipeline (peor categoría).** Está en el input de ORA (índice 20 de 49), es
   receptor opioide clásico anotado a GO:0038003, y aun así **no existe en `string_ids_v1.json` ni en el
   grafo**: el paso de resolución de IDs STRING lo perdió (solo 48 de 49 input se resolvieron; el
   informe previo ya notaba que el mapping contiene LEG1/C6orf58, que sí entró). Su ausencia NO es una
   decisión biológica, es una **falla del pipeline**: hay que re-resolver el STRING ID de OPRK1 y
   re-consultar la red antes del entrenamiento.

**AUSENCIAS JUSTIFICADAS del grafo (sin evidencia STRING / fuera de alcance):**

1. **OPRL1 (receptor de nociceptina) — ausencia justificada.** No está en el input ORA (49 genes UKB
   causales) ni, por tanto, en la consulta STRING. No es una omisión: está fuera del gene set. Documentar
   en el spec que OPRL1 queda fuera del alcance de este grafo (si el próximo dataset lo incluye, debe
   entrar).
2. **PPP2R2B — flag `false` CORRECTO (no corregir).** Subunidad reguladora de la fosfatasa PP2A: no es
   péptido ni receptor opioide ni neuropéptido. Su presencia en el módulo STRING-1 es un **artefacto
   topológico** de su arista de alta confianza con DRD2 (0.913, e interacción con COL9A1 0.402), no una
   membresía funcional del eje opioide. Etiquetarla como positiva contaminaría la clase minoritaria con
   un falso positivo funcional. **Queda como el caso de control ideal**: "en módulo STRING pero NO opioide",
   para verificar que el GNN aprende señal funcional y no meramente topológica.
3. **COL9A1/PTN** (COL9A1, PTN): ya falsificado en `string_network_v1` (0 interacciones de alta confianza
   con el módulo opioide); no son candidatos opioides.

**Resumen:** 1 corrección de flag (MLN), 1 omisión de pipeline (OPRK1), 1 ausencia justificada (OPRL1,
fuera de gene set), 1 no-corrección (PPP2R2B, flag correcto pese al módulo).

---

## (c) Recomendación concreta — lista final canónica para el GNN

Para el **próximo entrenamiento** (grafo 48 nodos actual, CPU):

| Grupo | Genes | n |
|-------|-------|---|
| **Clase positiva (eje opioide) — 10** | OPRM1, OPRD1, OPRK1*, PENK, PNOC, POMC, TAC1, TACR1, NPY, DRD2 | 10 |
| **Con corrección** | MLN: `is_opioid=false` → `true` (se añade a la clase positiva) | — |
| **Negativos hard (módulo STRING pero no opioide)** | PPP2R2B | 1 |
| **Resto del grafo (negativos)** | los otros 37 nodos | 37 |

\* OPRK1 **no puede etiquetarse como nodo** hasta que exista en el grafo: requiere re-consulta STRING
(resolver `9606` OPRK1 y pedir la red con el input de 49). Con aristas recién traídas el grafo pasaría a
49 nodos; el entrenamiento de este ciclo se hace sobre los 48 actuales y OPRK1 se incorpora en la **v2**
del grafo (acción pendiente, no bloqueante del experimento CPU de abajo).

Regla de corrección al construir el dataset del experimento: `label = 1` para los 10 genes positivos
(incluyendo MLN), `label = 0` para el resto. Eliminar la feature `is_opioid` binaria del input de nodos
para no hacer trampa (dejar solo `e_value` y `degree`; el flag corregido pasa a ser el objetivo, no
feature). Nota de honestidad: con 10 positivos de 48, la clase minoritaria es 21% — desbalance fuerte,
tratar con weighted loss (ver sección d).

---

## (d) Experimento concreto CPU-only propuesto para el kanban

**Título:** `gnn_graphsage_v2_cpu_opioid10` — GraphSAGE 48 nodos, clase minoritaria 10/48

- **Modelo:** GraphSAGE_mean 2 capas (SAGEConv 2→16 relu, SAGEConv 16→8 relu, Linear 8→2) — el mismo de
  `gnn_architecture_v1`; PyTorch + PyTorch Geometric, **CPU** (48 nodos, 61 aristas = trivial, <2 GB RAM,
  sin GPU).
- **Labels:** 10 positivos (los 9 actuales + MLN corregido) vs 38 negativos; **remover** la feature
  `is_opioid` del input (solo `e_value` + `degree`), para que el test sea de topología y no de fuga.
- **Validación:** stratified 5-fold (10 positivos → 2 por test en cada fold) o leave-one-out sobre
  positivos; weighted CrossEntropy (weights [1.0, 3.8]) y/o balanced sampler; early stopping por F1
  macro en val; 300-500 épocas.
- **Métricas:** F1 macro, precisión/recall por clase, ROC-AUC, matriz de confusión; baseline:
  clasificador mayoritario (F1≈0.72 en negativos) y `degree` umbral (sanity).
- **Verificable (falsificación):** si F1 macro > baseline y el recall de positivos ≥ 0.6 y los fallos se
  concentran en los nodos puente (PPP2R2B, NCAM1, COL18A1), la topología STRING soporta el eje opioide;
  si el modelo no supera al baseline o clasifica PPP2R2B como positivo, **falsifica** que el grafo
  codifique el eje (señal topológica, no funcional).
- **Salida:** `experiments/gnn_graphsage_v2_train_cpu.json` con métricas y matriz de confusión (spec
  hash, siguiendo la convención del lab). Sin GPU, sin APIs externas.

---

**Archivos modificados:** ninguno de los 4 JSON fuente (solo lectura). Este informe es el único archivo
nuevo. Sin commits, sin preprints tocados.
