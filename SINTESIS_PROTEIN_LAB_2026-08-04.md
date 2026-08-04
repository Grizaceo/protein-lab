# SÍNTESIS TRANSVERSALE — PROTEIN-LAB

**Fecha:** 2026-08-04
**Autor del informe:** DAVI (modo meta-análisis)
**Alcance:** todas las líneas de trabajo del repo `~/.hermes/workspace/ACTIVE/protein-lab/` (126 commits, 12 líneas documentadas)
**Base de síntesis:** `ESTADO_INVESTIGACIONES.md` (2026-07-04), `EXPERIMENT_PRIORITIZATION.md` (2026-07-04), `GROUNDING.md` (2026-04), `HANDOFF_SESION.md`, `HANDOFF_PARALIZACION.md`, + auditorías FM (2026-08-03/04) + git log completo.

---

## 0. ÍNDICE DE LÍNEAS DE TRABAJO

| # | Línea | Carpeta | Estado (evidencia) | TRL |
|---|--------|---------|---------------------|-----|
| 1 | Fibromialgia (transcriptómica + UKB) | `investigacion-fibromialgia/` | Preprint v2.9 local, auditado | 4-5 |
| 2 | FM Docking (paper 2) | `investigacion-fibromialgia/docking_fm_targets/` | **RETENIDO** (10/11 ligandos erróneos) | 1 |
| 3 | Binder Design (Nipah G) | `binder_design/` | Infra lista, smoke test Colab pendiente | 3 |
| 4 | CASP17 | `casp17/` | Scripts listos, sin registro ni corridas | 2 |
| 5 | H. gigas — GH7 barorresistencia | `hirondellea-gigas/investigacion-baroresistencia-gh7/` | MD ~15 ps real, no 100 ns | 2 |
| 6 | H. gigas — Sistema Aluminio | `hirondellea-gigas/` | Docs Fase 1-2, BLAST genoma pendiente | 2 |
| 7 | H. gigas — Proteoma presión | `hirondellea-gigas/colab_alphafold/` | Catálogo + embeddings listos | 3 |
| 8 | H. gigas — Catálogo general | `hirondellea-gigas/proteinas/` | 15+ entradas | 2 |
| 9 | Materiales Avanzados (Re SAC) | `materiales-avanzados-chile/` | Phase4 docking parcial; DFT/WHAM ausente | 1-2 |
| 10 | Ferritina-Au biosensor | root: `parallel_lab.py`, `SCOPE_C_*.py`, `DESIGN_ARTEFACT_*.md` | Diseño conceptual consolidado | 2-3 |
| 11 | Hemoglobina-MTR | `exp01-hemoglobina/`, `investigaciones/hemoglobina-mtr/` | Estructura creada, sin actividad | 1 |
| 12 | Automated Lab (DTI nocturno) | `automated_lab/` | v2 operativo, sin corridas recientes | 3 |

---

## 1. PATRONES DE TRABAJO DEL LAB

### 1.1 Buenos (elevar a estándar)

- **Ciclo generate→review→verify (AI-Assisted Research Methodology).** Declarado en el preprint FM y aplicado: cada claim pasa por verificador ejecutable (`audit_verify_claims.py`). *Evidencia:* commit `788e2bc` (revisión adversarial 3 issues), `16893ef` (FASE 1 R1-R14).
- **Auditoría adversarial obligatoria antes de preprint.** El preprint FM pasó de 52/100 (auditoría base) a ~75 post-reparación. Este patrón es el que salvó el trabajo. *Evidencia:* `AUDITORIA_EXTERNA_2026-08-03.md`, `PLAN_REPARACION.md`, `BITACORA_REPARACION.md`.
- **Grounding de citas (verificación por API/DOI).** `GROUNDING.md` es el guardián: documenta inventos de sub-agentes (Kang 2007, Tominaga 2006, Hainfeld 2011 NO existen en PubMed). *Regla:* lo que no está en GROUNDING.md = NO verificado.
- **Deconvolución + corrección por sexo como estándar post-hoc en transcriptómica.** Nació en FM pero es transferible. *Evidencia:* `sensitivity_analysis_gse221921.py` (5 modelos), `e1_deconvolution_adjusted_model.py` (modelo 6 composicional).
- **Spin-off de papers cuando una línea se vuelve "otro paper injertado".** FM hizo esto con docking (§4.6-4.9 → paper 2). *Evidencia:* commit `8c1c95a`.

### 1.2 Malos (corregir)

- **Sub-agentes inventan referencias y fórmulas.** Histórico en abril 2026 (ferritina) y agosto 2026 (docking FM: 10/11 ligandos erróneos — dopamina sin OH, pramipexol sin S, bromocriptina sin Br, aprepitant sin F). *Mitigación:* validar toda fórmula SDF contra PubChem antes de dockear.
- **Resultados publicados sin código que los reproduzca.** Caso E1 FM: commit solo CSV, irreproducible 15h. *Mitigación:* todo número publicado debe salir de un script commiteado (regla de PLAN_REPARACION).
- **Definiciones de robustez incompatibles entre archivos.** Caso E7 FM: `E7_sensitivity_master_GSE221921.csv` usaba male-only (5 FM) como "5/5"; el preprint usaba otro set. *Mitigación:* definir una sola taxonomía de modelos por línea.
- **Sobre-declaración de TRL.** Re SAC, GH7 MD, FM FEP fueron corregidos de "3-4" a "1-2" por auditoría. *Mitigación:* separar "infraestructura lista" de "evidencia científica".
- **Datos gitignoreados rompen `git clone`.** La matriz GSE221921 (60 MB) está gitignoreada; un clon no reproduce nada. *Mitigación:* README con instrucciones de descarga explícitas + checksum.

### 1.3 Estándares sugeridos para el lab

1. Todo paper lleva su `audit_verify_claims.py` commiteado.
2. Toda estructura molecular (PDB/SDF) validada por fórmula+MW contra fuente antes de uso.
3. Cada línea tiene un `ESTADO_LINEA.md` con TRL real y evidencia de disco.
4. Nunca "Robust N/5" sin citar qué 5 modelos.

---

## 2. FRAMEWORKS REUTILIZABLES (catálogo)

| Framework | Ruta | Resuelve | Reutilizable fuera de FM | Documentado |
|-----------|------|----------|--------------------------|--------------|
| `audit_verify_claims.py` | `investigacion-fibromialgia/scripts/` | Verificador 11 checks de claims numéricos | SÍ (adaptar matrices) | ✅ |
| `sensitivity_analysis_gse221921.py` | idem | 5 modelos × genes (sex-strat) | SÍ (cualquier RNA-seq sesgado) | ✅ |
| `e1_deconvolution_adjusted_model.py` | idem | Modelo 6 composicional + control negativo 600 genes | SÍ | ✅ |
| `generate_numbered_preprint.py` | idem | Regenera preprint con líneas numeradas | SÍ | ✅ |
| `prepare_bindcraft_target.py` | `binder_design/scripts/` | Prep target para BindCraft en Colab | SÍ | ✅ |
| `filter/process/monitor_bindcraft` | `binder_design/scripts/` | Pipeline binder design | SÍ | ✅ |
| `SCOPE_C_REAL_GEOMETRY.py` | root | Distancias reales PDB (ET ferritina) | SÍ | ✅ |
| `parallel_lab.py` | root | Simulador arquitecturas paralelas (biosensor) | PARCIAL | ⚠️ (sin tests) |
| `CASP17_ColabFold_Pipeline.ipynb` | `casp17/` | Pipeline predicción estructura | SÍ | ✅ |
| `fetch_targets.py` / `format_submission.py` | `casp17/scripts/` | Descarga/formateo CASP17 | SÍ | ✅ |
| `automated_lab/llm_researcher.py` | `automated_lab/` | DTI nocturno (MAMMAL) | PARCIAL | ⚠️ |
| `tropical_metrics.py` | root | Geometría tropical en proteínas (ORIGINAL lab) | SÍ (es novedoso) | ⚠️ |

**Nota crítica (GROUNDING.md):** el framework "tropical biomaterial" (geometría tropical + Ihara Zeta + RMT en proteínas) es **ORIGINAL del lab**, no tiene precedente en literatura. Citar solo componentes individuales, nunca sugerir un paper previo que los combina.

---

## 3. CONCLUSIONES CIENTÍFICAS POR LÍNEA (tabla de confianza)

### 3.1 Fibromialgia (transcriptómica) — CONFIANZA: ALTA/MEDIA

| Afirmación | Confianza | Base | Caveat |
|------------|-----------|------|--------|
| Eje opioide elevado en PBMC | MEDIA | GSE221921, 5 modelos sex-surviving | Composicional — 0/7 genes sobreviven ajuste celular; confundido por medicación opioide |
| COL9A1/PTN sobreviven todo (sex + Bonferroni + composición) | ALTA | `e1_deconvolution_adjusted_model.py`, 4/4 implementaciones, p=0.012-0.046 | PTN marginal bajo NNLS (p=0.046) |
| CA14 causal UKB, ↓ plasma | ALTA | Chen 2025 PMID 41025730 (peer-reviewed) | mRNA PBMC colapsa female-only (p=0.135); degradado a referencia |
| IL-6/IL-8 no respaldado a escala poblacional | MEDIA | Li ZY 2025 (51,644 UKB) | TAC1/SP no cubiertos por panel = no evaluables |
| No replica en whole blood | ALTA | GSE67311, FC≈1.0 | Sondas del eje en decil inferior de intensidad |

### 3.2 Binder Design (Nipah G) — CONFIANZA: BAJA (infra only)

- RFdiffusion falló (ipTM max 0.16). BindCraft documentado pero **sin corrida validada**. No hay evidencia de ipTM>0.5 todavía.

### 3.3 Ferritina-Au biosensor — CONFIANZA: MEDIA (diseño) / BAJA (validación)

- Mecanismo: jaula ferritina + núcleo Au. Contactos Fe-S verificados (A-MET52↔B-HEM-FE 2.20 Å).
- **Citas de Au25/Au55/Au144 "dentro de ferritina" son FALSAS** (GROUNDING.md). Estrategia real: nucleación in situ desde Au3+ con CYS.
- Corriente estimada ~1 μA detectable — pero es simulación, no medida.

### 3.4 H. gigas — CONFIANZA: BAJA/MEDIA

- GH7 MD: trayectorias ~15 ps reales (no 100 ns documentado). Análisis RMSD/RMSF NO ejecutado.
- Proteoma presión: catálogo 15 candidatos + embeddings ESM2 listos. AlphaFold Colab pendiente.

### 3.5 Materiales Avanzados (Re SAC) — CONFIANZA: BAJA

- Phase4 Vina: 42 poses PO4-proxy (~-2 kcal/mol). MD OpenMM existe (trajectories .dcd).
- DFT/GPAW, WHAM/PMF, Marcus/LZ, CI-NEB: **NO en disco** (solo narrativa).
- Claim "ARG319 salt bridge": residuo 319 es ALA en estructura usada. TRL real 1-2.

### 3.6 CASP17 / Automated Lab / Hemoglobina — CONFIANZA: N/A (sin ejecución)

- CASP17: scripts listos, sin registro ni predicciones.
- Automated Lab: v2 operativo, sin corridas nocturnas recientes.
- Hemoglobina-MTR: estructura creada, sin hipótesis ni actividad.

---

## 4. DEUDAS DE INTEGRIDAD (P0–P3)

### P0 — BLOQUEANTES (corregir antes de cualquier difusión)

- **[P0-1] Paper 2 FM docking: 10/11 ligandos erróneos.** Solo morfina correcta. `AUDITORIA_LIGANDOS_DOCKING_2026-08-04.md` documenta fórmulas discrepantes. **Paper retenido.** Ruta: reconstruir todos los SDF desde PubChem, re-dockear con exhaustiveness 32, regenerar §3.1-3.5. *Evidencia:* commit `4969830`.
- **[P0-2] Matriz GSE221921 gitignoreada.** `git clone` no reproduce el preprint. Ruta: README con link de descarga + checksum; considerar Git LFS o hosting externo. *Evidencia:* `.gitignore:2`.

### P1 — ALTAS (afectan calidad científica)

- **[P1-1] E1 original sin código.** Commit `03b4609` solo CSV. Reparado en `e9ceded` (script `e1_deconvolution_adjusted_model.py`). Validar que el script esté en el repo principal, no solo en rama `fm/e1b-...`.
- **[P1-2] Re SAC: computo honesto faltante.** Narrativa sin DFT/WHAM/Marcus. Ruta: reconstruir o bajar TRL a 1.
- **[P1-3] GH7 MD: 100 ns no ejecutado + análisis ausente.** Ruta: subir PDB a Kaggle, lanzar Lote 1, correr `scripts/10_analisis_final.py`.

### P2 — MEDIAS

- **[P2-1] Definiciones de "5/5" inconsistentes.** E7 vs §2.4. Resuelto en FM v2.8 pero el patrón persiste en otras líneas potenciales.
- **[P2-2] FC aritméticos inflados en FPKM cola-pesada.** FM v2.9 reporta FC arit + geom. Otras líneas pueden tener el mismo sesgo.
- **[P2-3] Automated Lab sin corridas recientes.** Definir campaña Ruta A (score 17/20 en priorización).

### P3 — COSMÉTICAS / MENORES

- **[P3-1] Hirondellea-gigas, materiales-avanzados-chile, automated_lab sin README.** Añadir `ESTADO_LINEA.md`.
- **[P3-2] `exp01-hemoglobina/` y `investigaciones/hemoglobina-mtr/` duplicados/espejo.** Consolidar.
- **[P3-3] `SINTESIS_PROMPT.md` (este mismo ejercicio) y `nul`, `__pycache__`, `scratch` en root.** Limpiar.

---

## 5. CUELLOS DE BOTELLA RECURRENTES

1. **Colab GPU es el limitante duro.** BindCraft, AlphaFold H. gigas, CASP17, FEP production — todos esperan Colab. RTX 4060 local no soporta BindCraft ni ESMFold (crash 16GB).
2. **Registro externo bloquea.** CASP17 (código XXXX-XXXX-XXXX), competencias Adaptyv (todas cerradas).
3. **Cuota Kaggle (2 sistemas simultáneos)** limita GH7 MD.
4. **GPAW no verificado** bloquea DFT Re SAC.
5. **Medicación/metadata faltante** en GSE221921 impide separar composición de biología (FM).

---

## 6. RECOMENDACIONES OPERATIVAS PARA PRÓXIMAS SESIONES

1. **Prioridad 1:** Reparar paper 2 FM (P0-1) — re-dockear con ligandos validados. Es el único bloqueante real de difusión.
2. **Prioridad 2:** Subir preprint FM v2.9 a bioRxiv (listo, solo falta decisión de Cristóbal).
3. **Prioridad 3:** Smoke test BindCraft Nipah G en Colab (P0-0, score 20/20).
4. **Patrón transversal:** aplicar el ciclo generate→review→verify + grounding de citas a TODAS las líneas, no solo FM.
5. **No sobre-declarar TRL.** Usar la taxonomía de este informe (evidencia de disco vs aspiración).
6. **Consolidar síntesis:** este documento reemplaza/augmenta `ESTADO_INVESTIGACIONES.md` y `EXPERIMENT_PRIORITIZATION.md`; actualizarlos en vez de duplicar.

---

## 7. GLOSARIO DEL LAB

- **ipTM:** interface pTM score (AlphaFold/BindCraft). >0.5 = buen binder.
- **E1 / E7:** designaciones internas FM de experimentos de deconvolución (E1 original, E7 tabla maestra). No confundir con "E1/E2" de la v2.7.
- **COL9A1/PTN:** módulo extracellular-matrix/neurite-outgrowth, hallazgo principal FM post-v2.8.
- **Eje opioide:** TACR1/OPRM1/TAC1/OPRK1 — robusto a sexo, composicional a celular.
- **CA14:** carbonic anhydrase XIV, causal UKB, referencia direccional FM.
- **BindCraft:** pipeline de binder design (Nature 2025) que reemplazó RFdiffusion.
- **SCOPE_C:** serie de scripts de biosensor ferritina-oro (geometría real, relay network, numeric biosensor).
- **Tropical biomaterial:** framework ORIGINAL del lab (geometría tropical + Ihara Zeta + RMT), sin precedente literario.

---

*Informe generado por DAVI en modo meta-análisis. Toda afirmación tiene ruta de evidencia en disco o git SHA. Cruza con `GROUNDING.md` antes de citar cualquier referencia externa.*
