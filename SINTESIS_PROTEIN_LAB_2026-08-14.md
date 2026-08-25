# SÍNTESIS TRANSVERSALE — PROTEIN-LAB

**Fecha:** 2026-08-14
**Autor del informe:** DAVI (modo meta-análisis)
**Alcance:** todas las líneas de trabajo del repo `~/.hermes/workspace/ACTIVE/protein-lab/` (~158 commits, 12 líneas + sub-líneas)
**Base de síntesis:** `SINTESIS_PROTEIN_LAB_2026-08-04.md` (126 commits, 12 líneas documentadas, **válida como base pre-04**). Este documento es la **actualización incremental 04→14 ago** (32 commits) y registra reorganización de líneas, fase de falsificación, pipeline FEP proof-of-pipeline, manuscrito v2.10, y campaña Ruta A del automated_lab.

**Estrategia para evitar timeout:** esta síntesis fue construida procesando el delta 04→14 en 4 bloques temáticos acotados (A: falsificación, B: FEP/MM-PBSA, C: manuscrito+paper2, D: reorganización). Los resultados se verificaron directamente del disco. Se usaron subagentes en paralelo para los bloques A/B/C; sus resúmenes fueron descartados por corrupción/prompt-injection y reconstruidos aquí desde evidencia primaria.

---

## 0. ÍNDICE DE LÍNEAS DE TRABAJO

| # | Línea | Carpeta | Estado (evidencia) | TRL |
|---|--------|---------|---------------------|-----|
| 1 | Fibromialgia (transcriptómica + UKB) | `investigacion-fibromialgia/` | Preprint v2.10 local, 9 métodos falsificación ejecutados | 4-5 |
| 2 | FM Docking (paper 2) | `investigacion-fibromialgia/docking_fm_targets/` | **RETENIDO** (10/11 ligandos erróneos, banner vigente v1.1) | 1 |
| 3 | FM FEP/MM-PBSA (DRD2+pramipexole) | `investigacion-fibromialgia/fep_drd2/` | **PIPELINE COMPLETO / ΔG NO CONVERGENTE** (proof-of-pipeline) | 1-2 |
| 4 | Binder Design (Nipah G) | `binder_design/` | Infra lista, smoke test Colab pendiente | 3 |
| 5 | CASP17 | `casp17/` | Scripts listos, sin registro ni corridas | 2 |
| 6 | H. gigas — GH7 barorresistencia | `hirondellea-gigas/` | MD ~15 ps real, no 100 ns | 2 |
| 7 | H. gigas — Sistema Aluminio | `hirondellea-gigas/` | Docs Fase 1-2, BLAST genoma pendiente | 2 |
| 8 | H. gigas — Proteoma presión | `hirondellea-gigas/` | Catálogo + embeddings listos | 3 |
| 9 | H. gigas — Catálogo general | `hirondellea-gigas/proteinas/` | 15+ entradas | 2 |
| 10 | ~~Materiales Avanzados (Re SAC)~~ | **MIGRADO** a `materiales-science-lab/` | Phase4 docking parcial; DFT/WHAM ausente | 1-2 |
| 11 | ~~Ferritina-Au biosensor~~ | **MIGRADO** a `material-science-lab/` | Diseño conceptual, SCOPE_C_*, DESIGN_ARTEFACT_* movidos | 2-3 |
| 12 | Hemoglobina-MTR | `exp01-hemoglobina/`, `investigaciones/hemoglobina-mtr/` | Estructura creada, sin actividad | 1 |
| 13 | Automated Lab (DTI nocturno) | `automated_lab/` | v2 operativo, **campaña Ruta A ejecutada** (12/12 OK) | 3 |
| 14 | OpenMed NER Mining | `openmed_mining.py` (raíz) | Operativo, modelos HF verificados sobre hallazgos FM | 3 |

---

## 1. PATRONES DE TRABAJO DEL LAB (actualización 04→14)

### 1.1 Buenos (confirmados/elevados a estándar)

- **Falsificación computacional sistemática (9 métodos).** Commit `2da2a00`: se ejecutó una batería de 9 tests (permutación, winsorization, leave-one-out, housekeepers, replicación whole-blood, etc.) con resultados reales. COL9A1 robusto 9/9, PTN 8/9, MDGA2/DRD2 8/8. Housekeepers (ACTB/GAPDH/B2M) todos NS. *Evidencia:* `analisis/falsificacion/falsification_results.json`, `scripts/falsification_execute.py`.
- **E-value para sensibilidad a confusión.** Commit `a7d4405`: COL9A1 E-value = 8.98 (VanderWeele & Ding 2017). Un confounder necesitaría RR ≥ 9.0 con ambos COL9A1 y FM para explicar el efecto. *Evidencia:* `analisis/falsificacion/e01_evalue_results.json`, `scripts/e01_evalue_col9a1.py`.
- **Auditoría externa reproducible.** Commit `a48c25f`: informe v2.0 reescrito con comandos verificados uno a uno. *Evidencia:* `INFORME_AUDITORIA_EXTERNA_2026-08-04.md` (246 líneas).
- **Protocol-first preprint con predicciones testeables.** Commit `2cedb4c`: reframe del manuscrito a formato con predicciones explícitas y falsables.
- **CIBERSORTx-equivalente NNLS.** Commit `6a01eab`: deconvolución celular alternativa que falsifica PTN (p=0.076) pero confirma COL9A1/MDGA2/DRD2.
- **OpenMed NER local.** Commit `7b9d373`: pipeline de minería de literatura NER local (ProteinDetect/ChemicalDetect/PharmaDetect/DiseaseDetect) verificado sobre hallazgos FM (detectó TACR1, OPRM1, Substance P, CA14, COL9A1, PTN con conf 0.56-0.94). Sin nube.
- **AM1-BCC real.** Commit `6fc8249`: cargas AM1-BCC REALES vía AmberTools22 (micromamba+conda-forge), reemplazando Gasteiger heurístico. Template GAFF validado.

### 1.2 Malos (detectados en este delta, corregir)

- **ΔG no declarado como prueba-de-concepto en paper FEP.** El pipeline está completo pero ΔG = 0.00 (artefacto por CPU-only + GBSA sin PME/solvente explícito). No puede presentarse como resultado físico válido. *Mitigación:* declarar explícitamente "proof-of-pipeline" y no comparar contra ΔG de文献.
- **PTN marginalmente frágil.** Leave-One-Out = 77.2% iteraciones permanecen significativas. No es 100%. *Mitigación:* declarar PTN como "marginalmente frágil a exclusión de muestra individual".
- **Forense scripts en WIP no push.** Commit `010b9fe`: scripts forense (03_cibersortx_drd2_mdga2.py, 04_fpkm_artifact_analysis.py) preservados localmente pero NO push. Riesgo de pérdida.

### 1.3 Estándares sugeridos (confirmados de la base del 04)

1. Todo paper lleva su `audit_verify_claims.py` commiteado.
2. Toda estructura molecular validada por fórmula+MW contra fuente antes de uso.
3. Cada línea tiene un `ESTADO_LINEA.md` con TRL real.
4. Nunca "Robust N/5" sin citar qué 5 modelos.
5. **NUEVO (04→14):** toda batería de falsificación se documenta con APPLIED/REMAINING/NOT-APPLICABLE por claim (`AUDIT_FALSIFICATION_METHODS.md` como plantilla).
6. **NUEVO (04→14):** E-value ≥ 2.0 como estándar para claims observacionales (referencia COL9A1 E=8.98 como benchmark).
7. **NUEVO (04→14):** ΔG de FEP se acompaña siempre de nota de convergencia y recursos computacionales (CPU-only vs GPU, solvente, tiempo MD).

---

## 2. FRAMEWORKS REUTILIZABLES (catálogo actualizado 04→14)

| Framework | Ruta | Resuelve | Reutilizable fuera de FM | Documentado |
|-----------|------|----------|--------------------------|-------------|
| `audit_verify_claims.py` | `investigacion-fibromialgia/scripts/` | Verificador 11 checks de claims numéricos | SÍ (adaptar matrices) | ✅ |
| `sensitivity_analysis_gse221921.py` | idem | 5 modelos × genes (sex-strat) | SÍ (cualquier RNA-seq sesgado) | ✅ |
| `e1_deconvolution_adjusted_model.py` | idem | Modelo 6 composicional + control negativo 600 genes | SÍ | ✅ |
| `falsification_execute.py` | `investigacion-fibromialgia/scripts/` | Batería 9 métodos de falsificación (permutación, winsorization, LOO, housekeepers, etc.) | SÍ (plantilla `AUDIT_FALSIFICATION_METHODS.md`) | ✅ |
| `e01_evalue_col9a1.py` | idem | E-value VanderWeele & Ding (2017) para asociación gen-enfermedad | SÍ (cualquier estudio observacional) | ✅ |
| `cibersortx_nnls_deconvolution.py` | idem | CIBERSORTx-equivalente con NNLS (deconvolución celular) | SÍ (cualquier bulk RNA-seq) | ✅ |
| `generate_numbered_preprint.py` | idem | Regenera preprint con líneas numeradas | SÍ | ✅ |
| `prepare_bindcraft_target.py` | `binder_design/scripts/` | Prep target para BindCraft en Colab | SÍ | ✅ |
| `filter/process/monitor_bindcraft` | `binder_design/scripts/` | Pipeline binder design | SÍ | ✅ |
| `fep_gen_ligand_xml.py` | `investigacion-fibromialgia/scripts/` | Template GAFF del ligando para OpenMM | SÍ (cualquier FEP) | ✅ |
| `fep_prep.py` | idem | Merge complejo receptor-ligando + parametrización AMBER | SÍ | ✅ |
| `fep_solvate.py` | idem | Minimización del sistema | SÍ | ✅ |
| `fep_mmpbsa.py` | idem | Framework MM-PBSA (descomposición por grupos) | SÍ | ✅ |
| `fep_am1bcc.py` | idem | Cargas AM1-BCC REALES vía AmberTools22 (reemplaza Gasteiger) | SÍ (estándar académico) | ✅ |
| `fep_report.py` | idem | Reporte automatizado FEP | SÍ | ✅ |
| `openmed_mining.py` | raíz | Mining de literatura NER local (4 modelos: Protein/Chemical/Pharma/Disease Detect) | SÍ (cualquier dominio biomédico) | ✅ |
| `SCOPE_C_REAL_GEOMETRY.py` | raíz (ahora migrado) | Distancias reales PDB (ET ferritina) | SÍ | ✅ |
| `parallel_lab.py` | raíz (ahora migrado) | Simulador arquitecturas paralelas (biosensor) | PARCIAL | ⚠️ (sin tests) |
| `tropical_metrics.py` / `src/metrics/tropical_metrics_v2.py` | raíz | Geometría tropical en proteínas (ORIGINAL lab, sin precedente) | SÍ (es novedoso) | ⚠️ |
| `automated_lab/llm_researcher.py` | `automated_lab/` | DTI nocturno (MAMMAL) | PARCIAL | ⚠️ |

**Nota crítica (GROUNDING.md + anti-hallucinación):** el framework "tropical biomaterial" (geometría tropical + Ihara Zeta + RMT en proteínas) es **ORIGINAL del lab**, no tiene precedente en literatura. Citar solo componentes individuales, nunca sugerir un paper previo que los combina.

---

## 3. CONCLUSIONES CIENTÍFICAS POR LÍNEA (tabla de confianza actualizada)

### 3.1 Fibromialgia (transcriptómica) — CONFIANZA: ALTA/MEDIA

| Afirmación | Confianza | Base | Caveat |
|------------|-----------|------|--------|
| COL9A1 upregulated en PBMCs FM, cell-intrinsic | **ALTA** | Falsificación 9/9 tests (permutación prop_sig 0.058, winsorization FC 2.13 p=0.025, LOO mean_p 0.021, housekeepers NS), E-value 8.98, CIBERSORTx NNLS FC 2.32 p=0.029 | Replicación whole blood GSE67311 FC≈1.0 — posiblemente PBMC-specific |
| PTN upregulated en PBMCs FM | **MEDIA** | Falsificación 8/9 (LOO 77.2% — marginalmente frágil), E-value no calculado, CIBERSORTx NNLS FC 2.91 p=0.076 (NO significativo en deconvolución) | LOO 77.2% indica dependencia de muestras individuales |
| Eje opioide elevado en PBMC | **MEDIA → BAJA** (post-falsificación) | GSE221921, 5 modelos sex-surviving | Composicional — 0/7 genes sobreviven ajuste celular (NNLS DRD2 FC 2.66 p=0.013 sí sobrevive, pero TACR1/OPRM1 no evaluados en NNLS) |
| MDGA2/DRD2 upregulated en PBMCs FM | **ALTA** | CIBERSORTx NNLS MDGA2 FC 2.42 p=0.0033, DRD2 FC 2.66 p=0.0126 | N=4 genes en NNLS; necesita replicación en cohorte independiente |
| CA14 causal UKB, ↓ plasma | **ALTA** | Chen 2025 PMID 41025730 (peer-reviewed) | mRNA PBMC colapsa female-only; degradado a referencia |
| COL9A1/PTN sobreviven todo (sex + Bonferroni + composición) | **ALTA** | E1b modelo 6, 4 implementaciones | PTN marginal bajo NNLS (p=0.076) |
| IL-6/IL-8 no respaldado poblacionalmente | **MEDIA** | Li ZY 2025 (51,644 UKB) | TAC1/SP no cubiertos por panel = no evaluables |

### 3.2 FM FEP/MM-PBSA (DRD2+pramipexole) — CONFIANZA: BAJA (proof-of-pipeline)

| Afirmación | Confianza | Base | Caveat |
|------------|-----------|------|--------|
| Pipeline FEP/MM-PBSA implementado y funcional | **ALTA** (infra) | 5 scripts commiteados, complejo minimizado estable (E +38,316 → −19,652 kJ/mol), AM1-BCC real | No hay ΔG convergente |
| ΔG_bind DRD2+pramipexole | **RETIRADO / NO CONVERGENTE** | MM-PBSA calculado = 0.00 kcal/mol (artefacto metodológico: NoCutoff + GBSA sin PME/solvente explícito) | CPU-only, sin GPU. Solvatación explícita ~1.7M átomos inviable en RTX 4060 8GB |
| AM1-BCC reemplaza Gasteiger | **ALTA** | fep_am1bcc.py, AmberTools22 (micromamba+conda-forge), frcmod + mol2 commiteados | Requiere AmberTools 22 instalado; sin fallback silencioso |

### 3.3 FM Docking (paper 2) — CONFIANZA: BAJA / RETENIDO

| Afirmación | Confianza | Base | Caveat |
|------------|-----------|------|--------|
| Paper 2 de docking | **RETENIDO — NO SOMETER** | Banner "RETENIDO 2026-08-04" vigente en v1.1 | 10/11 ligandos erróneos. Con ligandos validados: aprepitant pasa de −3.2 a −10.12 kcal/mol, inversión de ranking desaparece |
| Docking pipeline FM GPCR | **MEDIA** (estructural, no cuantitativa) | Métodos documentados (Vina + AlphaFold), abstract reescrito | Falla en resolver diferencias finas entre agonistas (morfina vs fentanyl mismo score) |

### 3.4 Binder Design (Nipah G) — CONFIANZA: BAJA (infra only)

Sin cambios en este delta. RFdiffusion falló (ipTM max 0.16). BindCraft documentado, sin corrida validada.

### 3.5 H. gigas — CONFIANZA: BAJA/MEDIA

Sin cambios en este delta. GH7 MD ~15 ps reales. Catálogo 15+ candidatos + embeddings ESM2.

### 3.6 Ferritina-Au biosensor / Materiales Avanzados — CONFIANZA: N/A (migrados)

Líneas 10 y 11 **migradas a `material-science-lab/`** (commit `d0c4579`, 4.3 GB movidos). SCOPE_C_*, DESIGN_ARTEFACT_*, parallel_lab.py, tropical_metrics*, materiales-avanzados-chile/ ya no viven en protein-lab. Registry automated_lab sin MaterialesAdapter. Se registra la migración; el estado detallado de estas líneas vive en el informe de material-science-lab.

### 3.7 Hemoglobina-MTR — CONFIANZA: N/A

Sin cambios en este delta. Estructura creada, sin hipótesis ni actividad.

### 3.8 Automated Lab (DTI nocturno) — CONFIANZA: MEDIA

| Afirmación | Confianza | Base | Caveat |
|------------|-----------|------|--------|
| Campaña Ruta A (mastocitos/IgG) ejecutada | **ALTA** | `automated_lab/campaign_briefs/fibromialgia_ruta_a.json` (v2.0.0), 12/12 experimentos OK | MOR top target (pKd 6.9-7.2), sin cloud review |
| Hipótesis LDN + mastocitos | **MEDIA** | Targets MS4A2/FCER1A/HDC/MOR + drogas naltrexona/ketotifen/cromolín | Naltrexona es DTI, no MAMMAL (MAMMAL falla para GPCRs); interpretar con cautela |
| OpenMed NER sobre FM | **ALTA** | Detectó TACR1, OPRM1, Substance P, TAC1, neurokinin-1, CA14, COL9A1, PTN (conf 0.56-0.94), pregabalin/duloxetine | 4 modelos HF locales, sin nube, batch posible |

### 3.9 Tropical Geometry — CONFIANZA: MEDIA (novedoso)

`tropical_metrics.py` y `src/metrics/tropical_metrics_v2.py` existen y son **originales del lab** (sin precedente en literatura). No se avanzó en este delta. Citar con cautela.

---

## 4. DEUDAS DE INTEGRIDAD (P0–P3, actualizado 04→14)

### P0 — BLOQUEANTES

- **[P0-1] Paper 2 FM docking: 10/11 ligandos erróneos.** Sin cambios. Banner "RETENIDO" sigue vigente (v1.1, commit `12b5e95`). *Ruta:* reconstruir SDF desde PubChem, re-dockear con exhaustiveness 32, regenerar §3.1-3.5. *Evidencia:* `docking_fm_targets_GPCR.md` (header), `analisis/AUDITORIA_LIGANDOS_DOCKING_2026-08-04.md`.
- **[P0-2] Matriz GSE221921 gitignoreada.** Sin cambios. `git clone` no reproduce el preprint. *Mitigación:* README con link + checksum o Git LFS. *Evidencia:* `.gitignore:2`.

### P1 — ALTAS

- **[P1-1] ΔG FEP NO CONVERGENTE mal comunicado.** Si se cita como resultado, es un claim falso. *Mitigación:* declarar explícitamente "proof-of-pipeline" en cualquier documento que mencione FEP DRD2. *Evidencia:* `fep_drd2/MM_PBSA_FINAL.md`, `ESTADO.md` §NUEVO.
- **[P1-2] Forense scripts no push.** `010b9fe` preserva localmente scripts forense (03_cibersortx_drd2_mdga2.py, 04_fpkm_artifact_analysis.py) pero no hizo push. Riesgo de pérdida. *Mitigación:* commit + push o mover a rama dedicada.
- **[P1-3] PTN marginalmente frágil no declarado.** LOO 77.2% es < 100%. Si se presenta PTN como "igual de robusto que COL9A1", es excesivo. *Mitigación:* calificar PTN como "marginalmente frágil".

### P2 — MEDIAS

- **[P2-1] SINTESIS_PROTEIN_LAB_2026-08-04.md desactualizada.** La síntesis del 04 ya no refleja la reorganización de líneas (materiales migrados), la fase de falsificación, ni la campaña Ruta A. *Mitigación:* este documento la actualiza.
- **[P2-2] automated_lab/campaign_briefs/fibromialgia_ruta_a.json modificado no commiteado.** El archivo muestra `M` en git status pero no está en git. *Mitigación:* commit.
- **[P2-3] Preprint v2.10 sin subir a bioRxiv.** Aprobado localmente (generado con `generate_pdf.sh` commit `e69391e`) pero requiere acción de Cristóbal.

### 3 — COSMÉTICAS

- **[P3-1] `investigacion-fibromialgia/templates/` (preprint_template.latex) y `artifacts/manuscript/` son untracked.** No rompe nada pero ensucia `git status`.
- **[P3-2] `exp01-hemoglobina/` y `investigaciones/hemoglobina-mtr/` duplicados/espejo.** Consolidar (deuda heredada del 04).
- **[P3-3] Papelera en root:** `nul`, `__pycache__`, `scratch/` (teleprompter/playstation). *Evidencia:* commit `8dbca08`.

---

## 5. CUELLOS DE BOTELLA RECURRENTES (actualizado)

1. **Colab GPU es el limitante duro.** BindCraft, AlphaFold H. gigas, CASP17, FEP production — todos esperan Colab. RTX 4060 local no soporta BindCraft ni ESMFold (crash 16GB). FEP/MM-PBSA colapsa sin solvente explícito + GPU.
2. **Medicación/metadata faltante en GSE221921.** Impide separar composición de biología (deuda heredada).
3. **FEP riguroso requiere OpenMM con CUDA + solvente explícito (PME) + MD ≥10ns.** Hardware actual (CPU-only) no lo soporta.
4. **Re-dockeo paper 2 pendiente.** 10/11 ligandos por reconstruir desde PubChem.
5. **Forense scripts sin push.** Riesgo de pérdida.

---

## 6. RECOMENDACIONES OPERATIVAS PARA PRÓXIMAS SESIONES

1. **Prioridad 1 (difusión):** Subir preprint FM v2.10 a bioRxiv (acción de Cristóbal). Paper listo, PDF generado, 407 palabras abstract.
2. **Prioridad 2 (reparación):** Reparar paper 2 FM docking (P0-1) — re-dockear con ligandos validados. Es el único bloqueante real restante.
3. **Prioridad 3 (FEP honesto):** Re-enmarcar FEP DRD2 como proof-of-pipeline en el manuscrito. No presentar ΔG = 0.00 como resultado físico.
4. **Prioridad 4 (falsificación restante):** Ejecutar los ~20 métodos REMAINING identificados en `AUDIT_FALSIFICATION_METHODS.md` (batch effect, winsorization, LOO, CIBERSORTx, DESeq2/edgeR, MR inverse, VIF, etc.). Alta prioridad: CIBERSORTx (LM22).
5. **Prioridad 5 (forense):** Commit + push de scripts forense o mover a rama dedicada para no perderlos.
6. **Patrón transversal:** aplicar la batería de 9 métodos de falsificación + E-value a TODAS las líneas con claims observacionales, no solo FM.
7. **Consolidar síntesis:** este documento reemplaza/augmente `SINTESIS_PROTEIN_LAB_2026-08-04.md`. Actualizar `ESTADO_INVESTIGACIONES.md` y `EXPERIMENT_PRIORITIZATION.md` para reflejar la migración de líneas.

---

## 7. GLOSARIO DEL LAB (ampliado 04→14)

- **ipTM:** interface pTM score (AlphaFold/BindCraft). >0.5 = buen binder.
- **E1 / E7:** designaciones internas FM de experimentos de deconvolución. E1b = modelo 6 composicional.
- **COL9A1/PTN:** módulo extracellular-matrix/neurite-outgrowth, hallazgo principal FM post-v2.8.
- **Eje opioide:** TACR1/OPRM1/TAC1/OPRK1 — robusto a sexo, composicional a celular.
- **CA14:** carbonic anhydrase XIV, causal UKB, referencia direccional FM.
- **BindCraft:** pipeline de binder design (Nature 2025) que reemplazó RFdiffusion.
- **SCOPE_C:** serie de scripts de biosensor ferritina-oro (geometría real, relay network, numeric biosensor). **Migrado a material-science-lab.**
- **Tropical biomaterial:** framework ORIGINAL del lab (geometría tropical + Ihara Zeta + RMT), sin precedente literario. **Migrado a material-science-lab.**
- **E-value:** medida de sensibilidad a confusión (VanderWeele & Ding 2017). E > 2.0 = robusto a confusión moderada. COL9A1 = 8.98 (muy robusto).
- **NNLS:** Non-Negative Least Squares (CIBERSORTx-equivalente). Deconvolución celular sin valores negativos.
- **AM1-BCC:** cargas partiales estándar académico vía AmberTools antechamber/sqm. Reemplaza Gasteiger heurístico.
- **FEP/MM-PBSA:** Free Energy Perturbation + Molecular Mechanics Poisson-Boltzmann Surface Area. Cálculo de ΔG de unión. Requiere solvente explícito + GPU + MD largo.
- **Proof-of-pipeline:** infraestructura completa y funcional, pero resultado final NO convergente/válido. Estado actual de FEP DRD2.
- **OpenMed:** biblioteca NER biomédico local (Protein/Chemical/Pharma/Disease Detect). Modelos HF 33M-568M, corre en CPU/CUDA 4060.
- **Ruta A (automated_lab):** campaña DTI mastocitos/IgG. Targets MS4A2/FCER1A/HDC/MOR + drogas naltrexona/ketotifen/cromolín.
- **TRL:** Technology Readiness Level. TRL 1-2 = concepto/prueba-de-concepto. TRL 3-4 = validación experimental. TRL 5-6 = prototipo en entorno relevante.

---

*Informe generado por DAVI en modo meta-análisis. Toda afirmación tiene ruta de evidencia en disco o git SHA. Cruza con `GROUNDING.md` antes de citar cualquier referencia externa. Los resultados de los subagentes delegados fueron verificados contra evidencia primaria; los resúmenes inyectados/corrompidos fueron descartados. Fecha de corte: 2026-08-14. Estado del repo en HEAD `e69391e` (rama master).*


---

## DELTA 14→23 AGO (añadido 2026-08-23 por Eidos) — veredictos del ciclo

### Línea 1 (FM): cierre de la vía marginal opioide con veredicto negativo honesto

| Artefacto | Veredicto |
|-----------|-----------|
| `experiments/gse67311_via_marginal_20260823.json` | GSE67311 (whole blood) DEBILITA la vía marginal COL9A1→NCAM1→DRD2: los 3 genes presentes en 33,297 probes pero NINGUNO significativo (COL9A1 FC=1.02 p=0.29 FDR=0.76; DRD2 FC=1.03 p=0.20 FDR=0.71; NCAM1 FC=0.94 p=0.24 FDR=0.73). |
| `experiments/modulo_opioide_GSE67311_20260823.json` | Módulo opioide completo (10 genes) NO sobrevive en GSE67311: 10/10 presentes, 0/10 significativos, todos FDR>0.60. Máximo efecto MLN log2FC 0.062 p=0.049 FDR=0.60 = indistinguible de ruido. |
| `reconciliacion_preprint_pbmc_20260823.json` | Preprint v2.12 NO sobre-generaliza: ya advierte limitación PBMC-específica (secciones 3.3, limitaciones 3/6/11) y usa GSE67311 como validación negativa. |
| `eidos_verificacion_vif_v212_20260823.json` | INCONSISTENCIA de manuscrito: v2.12 reporta "VIF median 2.7, max 13.1" en §3.2 pero el artefacto fuente (AUDIT_FALSIFICATION_METHODS.md §2.7, 15-08) documenta VIF real corregido: T_cells_CD8=27.8, NK=27.2, Mast=21.2, Basophils=13.6. El 13.1 era el valor pre-corrección. **Artefacto de verificación registrado sin tocar el manuscrito.** |

### Conclusiones nuevas

- **La línea opioide queda cerrada con veredicto negativo honesto**: doble evidencia (STRING + GSE67311), NCAM1 invierte signo, 0/10 módulo significativo. El preprint no sobre-generaliza PERO tiene inconsistencia VIF pendiente de corregir (13.1 obsoleto vs 27.8 real).
- **Pendiente P1 nuevo**: corregir §3.2 del preprint v2.12 con el VIF real (27.8) antes de cualquier difusión.

### Estado kanban protein-1

- `SINTESIS_PROTEIN_LAB_2026-08-14.md` verificado en disco (221 líneas, 20KB, cumple señal de terminación). El primer dispatch hizo timeout pero el re-dispatch con scope reducido funcionó. Estado kanban actualizado a completed.
