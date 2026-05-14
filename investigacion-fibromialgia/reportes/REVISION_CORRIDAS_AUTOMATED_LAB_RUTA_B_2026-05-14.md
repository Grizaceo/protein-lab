# Revisión y análisis de corridas — Automated Lab / Fibromialgia Ruta B

Fecha de revisión: 2026-05-14 11:40
Run analizado: `automated_lab/results/fibromialgia_ruta_b_20260514_050308`
Reporte automático base: `automated_lab/results/fibromialgia_ruta_b_20260514_050308/REPORTE_MANANA.md`

## 1. Veredicto ejecutivo

La corrida terminó operacionalmente limpia: 1600/1600 experimentos ejecutados con `local_mammal`, 0 errores, 32 ciclos de 50 pares droga-target. El resultado no debe leerse como “tenemos 1600 descubrimientos”, sino como un cribado DTI masivo para priorización. La señal dominante es MOR: el modelo asigna pKd alto a casi cualquier molécula contra MOR, lo que confirma que MOR/LDN es recuperado, pero también prende una alarma de sesgo/promiscuidad del modelo para ese target.

La conclusión útil: la corrida sirve para ordenar controles y rutas de validación; no basta para inferir eficacia clínica ni mecanismo causal en fibromialgia.

## 2. Integridad operacional

| Métrica | Valor |
|---|---:|
| Experimentos planificados | 1600 |
| Exitosos | 1600 |
| Errores | 0 |
| Ciclos | 32 |
| Batch size efectivo | 50 |
| Duración total desde inicio | 6.3451 h |
| Backend | local_mammal / MAMMAL DTI |
| Investigador cloud | ollama-cloud/nemotron-3-super |
| Finalización | scripts/finish_active_run_now.py |

Notas operativas:
- Los primeros 1300 experimentos corrieron con pacing nocturno; los últimos 300 se terminaron con `scripts/finish_active_run_now.py` para no esperar sleeps artificiales.
- `exit code 143` del launcher antiguo fue SIGTERM controlado, no crash del backend.
- Se removió el cron monitor de esta campaña después de completarla para evitar relanzamientos o ruido.

## 3. Distribución global de pKd

| Métrica pKd | Valor | Interpretación aproximada |
|---|---:|---|
| Mínimo | 5.267 | afinidad baja / µM-alta |
| Mediana | 5.839 | centro de masa del cribado |
| Media | 5.892 | afectada por MOR alto |
| Máximo | 7.349 | top: ziconotide→MOR, 44.8 nM |
| Desv. estándar | 0.435 | separación moderada entre targets |

Regla de lectura usada aquí: pKd≈5 equivale a ~10 µM; pKd≈6 a ~1 µM; pKd≈7 a ~100 nM; pKd≈8 a ~10 nM. En modelos DTI, diferencias pequeñas (<0.2 pKd) no deben sobreinterpretarse sin controles.

## 4. Ranking por target

| Target | N | Media pKd | Mediana | Min | Max | SD | ≥7.0 | ≥6.5 | Lectura |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| MOR | 160 | 6.926 | 6.915 | 6.742 | 7.349 | 0.100 | 33 | 160 | Dominante; posible sesgo/promiscuidad. |
| MS4A2 | 160 | 6.235 | 6.210 | 6.139 | 6.896 | 0.089 | 0 | 2 | Segunda señal consistente; revisar mast-cell axis. |
| HDC | 160 | 5.952 | 5.932 | 5.809 | 6.553 | 0.097 | 0 | 1 | Hits aislados, no señal global. |
| NRF2 | 160 | 5.943 | 5.918 | 5.851 | 6.463 | 0.078 | 0 | 0 | Señal baja/moderada. |
| TLR4 | 160 | 5.896 | 5.864 | 5.657 | 6.493 | 0.145 | 0 | 0 | Señal baja/moderada. |
| CPA3 | 160 | 5.781 | 5.754 | 5.667 | 6.587 | 0.121 | 0 | 1 | Hits aislados, no señal global. |
| TRPA1 | 160 | 5.762 | 5.749 | 5.614 | 6.174 | 0.097 | 0 | 0 | Señal baja/moderada. |
| IL-6 | 160 | 5.490 | 5.453 | 5.267 | 6.439 | 0.154 | 0 | 0 | Señal baja/moderada. |
| FCER1A | 160 | 5.487 | 5.457 | 5.326 | 6.448 | 0.142 | 0 | 0 | Señal baja/moderada. |
| IL-1β | 160 | 5.446 | 5.403 | 5.296 | 6.438 | 0.144 | 0 | 0 | Señal baja/moderada. |

Lectura: MOR separa demasiado del resto (media 6.926 vs MS4A2 6.235). Eso puede ser biología parcialmente real para ligandos opioides, pero como ocurre con fármacos químicamente muy diversos, también es firma de target bias del modelo.

## 5. Top 25 absoluto

| # | Droga | Target | pKd | Kd aprox. | Ciclo |
|---:|---|---|---:|---:|---:|
| 1 | ziconotide | MOR | 7.349 | 44.8 nM | 24 |
| 2 | montelukast | MOR | 7.211 | 61.5 nM | 19 |
| 3 | everolimus | MOR | 7.153 | 70.3 nM | 32 |
| 4 | anandamide | MOR | 7.149 | 71.0 nM | 29 |
| 5 | cyclosporine | MOR | 7.148 | 71.1 nM | 32 |
| 6 | fexofenadine | MOR | 7.128 | 74.5 nM | 18 |
| 7 | sirolimus | MOR | 7.121 | 75.7 nM | 32 |
| 8 | rapamycin | MOR | 7.121 | 75.7 nM | 32 |
| 9 | tacrolimus | MOR | 7.119 | 76.0 nM | 32 |
| 10 | buprenorphine | MOR | 7.113 | 77.1 nM | 2 |
| 11 | verapamil | MOR | 7.111 | 77.4 nM | 23 |
| 12 | epigallocatechin_gallate | MOR | 7.086 | 82.0 nM | 21 |
| 13 | zafirlukast | MOR | 7.072 | 84.7 nM | 19 |
| 14 | colchicine | MOR | 7.068 | 85.5 nM | 15 |
| 15 | diltiazem | MOR | 7.057 | 87.7 nM | 23 |
| 16 | cetirizine | MOR | 7.050 | 89.1 nM | 17 |
| 17 | hydroxychloroquine | MOR | 7.049 | 89.3 nM | 16 |
| 18 | cromolyn | MOR | 7.047 | 89.7 nM | 16 |
| 19 | baricitinib | MOR | 7.040 | 91.2 nM | 30 |
| 20 | nimodipine | MOR | 7.039 | 91.4 nM | 24 |
| 21 | suzetrigine | MOR | 7.033 | 92.7 nM | 22 |
| 22 | escitalopram | MOR | 7.026 | 94.2 nM | 9 |
| 23 | levocetirizine | MOR | 7.025 | 94.4 nM | 17 |
| 24 | TAK242_resatorvid | MOR | 7.019 | 95.7 nM | 1 |
| 25 | trazodone | MOR | 7.015 | 96.6 nM | 10 |

Observación crítica: el Top 25 absoluto es 100% MOR. Como ranking global, por tanto, es poco informativo: prioriza target antes que molécula.

## 6. Top 25 excluyendo MOR

| # | Droga | Target | pKd | Kd aprox. | Ciclo |
|---:|---|---|---:|---:|---:|
| 1 | ziconotide | MS4A2 | 6.896 | 127.1 nM | 24 |
| 2 | ziconotide | CPA3 | 6.587 | 258.8 nM | 24 |
| 3 | cyclosporine | MS4A2 | 6.577 | 264.9 nM | 32 |
| 4 | ziconotide | HDC | 6.553 | 279.9 nM | 24 |
| 5 | everolimus | MS4A2 | 6.499 | 317.0 nM | 32 |
| 6 | ziconotide | TLR4 | 6.493 | 321.4 nM | 24 |
| 7 | ziconotide | NRF2 | 6.463 | 344.3 nM | 24 |
| 8 | sirolimus | MS4A2 | 6.458 | 348.3 nM | 32 |
| 9 | rapamycin | MS4A2 | 6.458 | 348.3 nM | 32 |
| 10 | tacrolimus | MS4A2 | 6.452 | 353.2 nM | 32 |
| 11 | ziconotide | FCER1A | 6.448 | 356.5 nM | 24 |
| 12 | ziconotide | IL-6 | 6.439 | 363.9 nM | 24 |
| 13 | ziconotide | IL-1β | 6.438 | 364.8 nM | 24 |
| 14 | montelukast | MS4A2 | 6.420 | 380.2 nM | 19 |
| 15 | epigallocatechin_gallate | MS4A2 | 6.420 | 380.2 nM | 21 |
| 16 | fexofenadine | MS4A2 | 6.396 | 401.8 nM | 18 |
| 17 | buprenorphine | MS4A2 | 6.370 | 426.6 nM | 2 |
| 18 | paroxetine | MS4A2 | 6.369 | 427.6 nM | 9 |
| 19 | cyclosporine | TLR4 | 6.353 | 443.6 nM | 32 |
| 20 | zafirlukast | MS4A2 | 6.349 | 447.7 nM | 19 |
| 21 | verapamil | MS4A2 | 6.337 | 460.3 nM | 23 |
| 22 | baricitinib | MS4A2 | 6.328 | 469.9 nM | 30 |
| 23 | prazosin | MS4A2 | 6.323 | 475.3 nM | 11 |
| 24 | suzetrigine | MS4A2 | 6.322 | 476.4 nM | 22 |
| 25 | dexamethasone | MS4A2 | 6.316 | 483.1 nM | 15 |

Aquí emergen dos patrones: ziconotide aparece como outlier multi-target y MS4A2 concentra muchos de los mejores no-MOR. Ambos requieren cautela: ziconotide es péptido/fármaco no oral y puede estar fuera del dominio small-molecule clásico; MS4A2 puede ser ruta interesante por mast cells, pero necesita controles negativos y evidencia omics/literatura.

## 7. Señales normalizadas por target

Para no dejar que MOR gane por escala absoluta, calculé z-score dentro de cada target. Esto pregunta: “¿qué molécula es anormalmente alta para SU target?”.

| # | Droga | Target | pKd | z dentro del target |
|---:|---|---|---:|---:|
| 1 | ziconotide | MS4A2 | 6.896 | 7.42 |
| 2 | ziconotide | IL-1β | 6.438 | 6.88 |
| 3 | ziconotide | FCER1A | 6.448 | 6.75 |
| 4 | ziconotide | NRF2 | 6.463 | 6.72 |
| 5 | ziconotide | CPA3 | 6.587 | 6.66 |
| 6 | ziconotide | HDC | 6.553 | 6.18 |
| 7 | ziconotide | IL-6 | 6.439 | 6.18 |
| 8 | ziconotide | TRPA1 | 6.174 | 4.27 |
| 9 | cyclosporine | IL-6 | 6.142 | 4.24 |
| 10 | ziconotide | MOR | 7.349 | 4.24 |
| 11 | ziconotide | TLR4 | 6.493 | 4.13 |
| 12 | cyclosporine | CPA3 | 6.270 | 4.04 |
| 13 | cyclosporine | FCER1A | 6.062 | 4.04 |
| 14 | cyclosporine | MS4A2 | 6.577 | 3.84 |
| 15 | everolimus | CPA3 | 6.236 | 3.76 |
| 16 | cyclosporine | IL-1β | 5.975 | 3.67 |
| 17 | rapamycin | CPA3 | 6.186 | 3.35 |
| 18 | sirolimus | CPA3 | 6.186 | 3.35 |
| 19 | everolimus | NRF2 | 6.199 | 3.31 |
| 20 | everolimus | IL-1β | 5.923 | 3.31 |

Esta tabla es más útil para generar hipótesis que el Top absoluto, porque rescata outliers en targets de baja media como IL-6/IL-1β/FCER1A.

## 8. Fármacos semilla / controles conocidos

| Droga | Mejor target | Mejor pKd | MOR pKd | Comentario |
|---|---|---:|---:|---|
| naltrexona_LDN | MOR | 6.913 | 6.913 | Control positivo recuperado: MOR alto/moderado. |
| naltrexone | MOR | 6.844 | 6.844 | Control positivo recuperado: MOR alto/moderado. |
| dimetil_fumarato | MOR | 6.839 | 6.839 | NRF2 no domina; compatible con mecanismo covalente/profármaco mal capturado por pKd. |
| suzetrigine | MOR | 7.033 | 7.033 | Nav1.8 no fue ejecutado localmente; MOR/MS4A2 son off-target hipotéticos, no conclusión. |
| suzetrigine_VX548 | MOR | 6.908 | 6.908 | Nav1.8 no fue ejecutado localmente; MOR/MS4A2 son off-target hipotéticos, no conclusión. |
| TAK242_resatorvid | MOR | 7.019 | 7.019 | TLR4 no sobresale; posible limitación del modelo o mecanismo no canónico. |
| rapamycin | MOR | 7.121 | 7.121 | Perfiles idénticos; duplicado/alias esperado, usar uno solo en próximos runs. |
| sirolimus | MOR | 7.121 | 7.121 | Perfiles idénticos; duplicado/alias esperado, usar uno solo en próximos runs. |

## 9. Problemas científicos detectados

### A. Sesgo MOR

MOR tiene media 6.926 y desviación 0.100: casi todas las moléculas caen en una banda estrecha y alta. Esto es sospechoso. Puede indicar que el embedding/proteína MOR induce afinidad basal alta para muchas drogas. Acción: correr panel de decoys contra MOR y targets GPCR/no-GPCR.

### B. Dominio de aplicabilidad

La biblioteca incluye moléculas grandes, péptidos o compuestos complejos (ej. ziconotide, ciclosporina, tacrolimus/sirolimus). MAMMAL puede devolver pKd, pero eso no equivale a drug-likeness ni viabilidad BBB/oral. Acción: separar small molecules realistas, péptidos/biológicos, macrociclos e inmunosupresores.

### C. Targets incompatibles con backend

Nav1.8 fue evitado por longitud; IL-1β/IL-6 son cytokines, no necesariamente targets small-molecule clásicos en el mismo sentido que MOR/TLR4/TRPA1. Biológicos como anakinra/tocilizumab no se evalúan bien como SMILES small-molecule.

### D. Duplicados químicos / alias

Perfiles duplicados detectados: [['dronabinol', 'tetrahydrocannabinol'], ['sirolimus', 'rapamycin']]. Rapamycin/sirolimus son el caso claro. Acción: canonicalizar por PubChem CID/InChIKey antes del próximo batch.

### E. No hay validación externa todavía

pKd predicho no es docking, no es ensayo, no es clínica. Sirve para priorizar qué mirar después.

## 10. Priorización propuesta

### Prioridad 1 — Validar / falsar MOR

- Mantener naltrexona_LDN y naltrexone como controles positivos.
- Añadir decoys negativos estructuralmente diversos.
- Añadir otros GPCRs como controles para ver si el sesgo es MOR específico o GPCR general.
- Comparar con BindingDB/ChEMBL para ligandos MOR conocidos si hay datos.

### Prioridad 2 — MS4A2 / mast-cell axis

- MS4A2 es el segundo target por media y concentra varios hits no-MOR.
- Cruzar contra evidencia de mast cells en fibromialgia y datasets GEO ya auditados.
- Evitar saltar directo a conclusión terapéutica: MS4A2/FcεRIβ no es un target clásico de small molecules simple.

### Prioridad 3 — Filtrar biblioteca por viabilidad farmacológica

- Separar: small molecules, macrociclos, péptidos, biológicos/no aptos.
- Calcular propiedades RDKit básicas: MW, cLogP aproximado, TPSA, HBD/HBA, rotatable bonds.
- Re-rankear no por pKd puro sino por pKd + plausibilidad + evidencia clínica/literatura.

### Prioridad 4 — Re-run focalizado

- Nuevo run pequeño: 20–40 moléculas limpias × 4–6 targets.
- Incluir controles positivos y negativos por target.
- Desactivar moléculas enormes/peptídicas salvo que se analicen en una categoría propia.

## 11. Qué NO concluir

- No concluir que ziconotide, montelukast o everolimus “tratan fibromialgia” por aparecer arriba.
- No concluir que MOR es el único mecanismo: puede ser sesgo del modelo.
- No concluir afinidad real nanomolar sin validación externa.
- No usar IL-1β/IL-6 como si fueran targets small-molecule ordinarios sin revisar mecanismo.

## 12. Archivos y reproducibilidad

- Cola completa: `automated_lab/results/fibromialgia_ruta_b_20260514_050308/EXPERIMENT_QUEUE.json`
- Resultados por ciclo: `automated_lab/results/fibromialgia_ruta_b_20260514_050308/cycle_*`
- Estado final: `automated_lab/results/fibromialgia_ruta_b_20260514_050308/SESSION.json` y `automated_lab/results/fibromialgia_ruta_b_20260514_050308/STATUS.json`
- Reporte automático: `automated_lab/results/fibromialgia_ruta_b_20260514_050308/REPORTE_MANANA.md`

## 13. Siguiente acción recomendada

Construir una tabla “Ruta B v2 focalizada” con 30 moléculas máximo, etiquetadas por clase química/dominio de aplicabilidad, y correr un panel con controles. La meta no es más volumen; es mejor falsación. Ya hicimos la red de pesca. Ahora toca separar pescado de bolsa plástica.
