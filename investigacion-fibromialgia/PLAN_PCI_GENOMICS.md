# Plan de envío a PCI Genomics

Fecha: 2026-05-16 | Actualizado: 2026-05-17

---

## 1) Veredicto rápido

El manuscrito calza con PCI Genomics porque el foco real es genomics/bioinformatics: reanálisis de cohortes transcriptómicas públicas, integración con GWAS, y priorización de genes neurales en fibromialgia.

PCI Genomics no es una revista tradicional: es una plataforma de evaluación de preprints. Si el preprint es aceptado, la recomendación pública y la correspondencia editorial se publican; el artículo sigue alojado en el servidor de preprints original (bioRxiv).

---

## 2) Reglas PCI Genomics que hay que respetar

- El preprint no debe estar publicado ni sometido simultáneamente a otra revista.
- Debe ser un preprint **ya publicado** en un servidor (bioRxiv o equivalente) — PCI no evalúa borradores.
- Deben estar accesibles los datos, el código y los scripts de análisis.
- El manuscrito debe ir con **líneas numeradas**.
- PCI espera estándares altos de rigor metodológico, ético y reproducibilidad.
- Si el trabajo recibe recomendación positiva, la evaluación completa pasa a ser pública y citable.
- Si luego se quiere mandar a una revista, conviene primero la recomendación PCI y después una inquiry con link a la evaluación.

---

## 3) Encaje del manuscrito

**Fortalezas para PCI Genomics** (estado actual del preprint):
- ✅ Usa datos públicos (GSE221921 y GSE67311) con GEO accession correctos
- ✅ Pregunta claramente genética/transcriptómica
- ✅ Conecta GWAS (Kerrebijn et al. 2025) con expresión en tejido periférico (PBMCs)
- ✅ Cinco modelos de análisis de sensibilidad para sex confounding (Welch, MWU, OLS sex-adj, female-only)
- ✅ Limitaciones explícitas y frontales (9 puntos en §5)
- ✅ Título ya encuadrado en GWAS + transcriptomics + FM ("GWAS-Prioritized Neural Genes Are Differentially Expressed in Fibromyalgia PBMCs")
- ✅ Abstract cita la convergencia GWAS-transcriptómica como hallazgo principal
- ✅ Lenguaje "exploratory", "hypothesis-generating" y "validation needed" presente en Abstract y §4.5
- ✅ Scripts disponibles y documentados en §Data & Code Availability
- ✅ Tablas de resultados derivadas disponibles en `analisis/`
- ✅ No hay sobreafirmación terapéutica: pramipexole queda como contexto farmacológico

**Riesgo principal de encaje:**
- ⚠️ El preprint no está publicado en bioRxiv todavía — esto es un **blocker duro** para enviar a PCI.
- ⚠️ Falta DOI/permalink permanente del repositorio de código (Zenodo u equivalente).
- ⚠️ El manuscrito no tiene líneas numeradas en su formato actual (`.md`); se necesita PDF con líneas numeradas.

---

## 4) Checklist de preparación — estado actual

### A. Manuscrito (`preprint_dopaminergic_convergence_FM.md`)

- [x] Título PCI-friendly y preciso (GWAS + transcriptomics + FM).
- [x] Abstract sin sobreafirmación causal; hallazgo principal es convergencia GWAS-transcriptómica.
- [x] Discusión usa lenguaje de "exploratory", "hypothesis-generating", "validation needed" (§4.5).
- [x] Citas clave con DOI/PMID/PMCID correctos (todas verificadas).
- [x] Sección de limitaciones frontal (§5, 9 ítems incluyendo sex confounding, FPKM, cell composition, low expression, missing gene, non-replication, GWAS preprint status, no experimental validation, narrative review).
- [x] DRD2/pramipexole encuadrado como contexto farmacológico, no recomendación clínica.
- [ ] **Generar PDF con líneas numeradas** (blocker para envío).

### B. Datos y código

- [x] Scripts documentados en `scripts/`:
  - `sensitivity_analysis_gse221921.py`
  - `cross_context_gwas_neural_genes.py`
  - `phase2_rct_review.py`
- [x] Tablas derivadas en `analisis/` (CSV).
- [x] Instrucciones para replicar el flujo en §Data & Code Availability.
- [x] **Subir repositorio a GitHub** (público) — https://github.com/Grizaceo/protein-lab
- [x] **Crear release/tag estable** — `v1.0.0` publicado.
- [x] **Obtener DOI de Zenodo** — DOI: `10.5281/zenodo.20250218`
- [ ] Verificar que el flujo corre de punta a punta con los datos de GEO.

### C. Preprint en servidor

- [ ] **Subir preprint a bioRxiv** (blocker duro — PCI solo evalúa preprints publicados).
  - Categoría sugerida: Genomics / Bioinformatics.
  - Incluir nota de "not submitted to a journal" en cover letter a bioRxiv.
- [ ] Obtener DOI de bioRxiv.

### D. Materiales de envío a PCI

- [ ] Preparar cover note breve para PCI Genomics (ver §6).
- [ ] Preparar shortlist de posibles recommenders (ver §7).
- [ ] Tener listo resumen de por qué el estudio es relevante para genomics.
- [ ] Dejar explícito en el envío qué parte es reanálisis computacional y qué parte es revisión narrativa de soporte.

---

## 5) Ajustes editoriales — estado actual

| Ajuste | Estado |
|--------|--------|
| Reescribir framing del título (GWAS + transcriptomics + FM) | ✅ Hecho |
| Abstract: hallazgo principal = convergencia GWAS-transcriptómica | ✅ Hecho |
| DRD2 como robusto pero periférico y no confirmatorio | ✅ Hecho |
| Bajar nivel de inferencia terapéutica (pramipexole = contexto) | ✅ Hecho |
| Fortalecer reproducibilidad (data/code availability) | ✅ Parcial — falta DOI permanente |
| Líneas numeradas en el PDF final | ❌ Pendiente |

---

## 6) Cover note para PCI Genomics (borrador)

```
Subject: Submission request — GWAS-Prioritized Neural Genes Are Differentially Expressed
in Fibromyalgia PBMCs: A Targeted Reanalysis of Public Transcriptomic Cohorts

Dear PCI Genomics Editorial Board,

We submit for recommendation consideration a preprint presenting a targeted,
hypothesis-driven reanalysis of two public transcriptomic datasets (GSE221921,
GSE67311) in fibromyalgia. The study interrogates 13 GWAS-prioritized neural genes
(Kerrebijn et al., 2025; PMID 41001472) for differential expression in PBMCs and
whole blood, applying five analytical sensitivity models to address severe sex
imbalance in the primary cohort.

The central result — robust upregulation of MDGA2 and DRD2 across all five models,
including sex-adjusted OLS and female-only subgroup analysis — represents a direct
test of the hypothesis that GWAS genetic architecture is reflected in peripheral
transcriptomic signatures. Crucially, we contextualize these peripheral signals
against their absence in granulocyte-containing whole blood, revealing a
cell-fraction-dependent pattern consistent with the lymphocyte/monocyte biology
of the PBMC compartment.

This work is strictly exploratory and hypothesis-generating. We explicitly
acknowledge nine limitations including sex confounding, use of FPKM rather than
raw counts, absence of cell deconvolution, and the GWAS source being a preprint.
All code and derived data are publicly available at GitHub (https://github.com/Grizaceo/protein-lab) 
and archived on Zenodo (DOI: 10.5281/zenodo.20250218).

This preprint is not submitted to any journal. It has not been peer reviewed
previously.

Sincerely,
[Authors]
```

---

## 7) Shortlist de recommenders — áreas temáticas a priorizar

Buscar recommenders con experiencia en una o más de estas áreas:
1. **GWAS de dolor crónico / fibromialgia** — más cercano al tema; buscar autores que hayan publicado sobre genetic architecture of chronic pain.
2. **Transcriptómica de PBMCs / inmunogenómica** — experiencia en análisis de sensibilidad y confounding.
3. **Integración GWAS-transcriptómica (colocalization, eQTL, TWAS)** — contexto metodológico apropiado.
4. **Farmacogenómica dopaminérgica / receptores DRD2** — para el componente de contexto farmacológico.

Herramientas para buscar recommenders en PCI Genomics:
- Usar el buscador de recommenders del portal PCI Genomics por keywords: "GWAS", "transcriptomics", "chronic pain", "fibromyalgia", "bioinformatics".
- Buscar autores de papers clave del propio manuscrito (Kerrebijn, Mohapatra, Kurian) y verificar si están registrados como recommenders en PCI.

---

## 8) Plan de envío — fases con timeline estimado

### Fase 0 — Reproducibilidad (blocker; ~2–3 días)
- Subir repositorio de scripts a GitHub como repositorio público.
- Crear release `v1.0.0` con tag estable.
- Depositar en Zenodo para obtener DOI permanente.
- Verificar que el pipeline corre de punta a punta desde los datos de GEO.

### Fase 1 — Cierre del paquete técnico (~1–2 días)
- Generar PDF del manuscrito con líneas numeradas.
- Actualizar §Data & Code Availability con DOI de Zenodo y URL del repo GitHub.
- Revisar que todos los archivos suplementarios (Tablas 1-3 como CSV) son reproducibles desde los scripts.

### Fase 2 — Publicación en bioRxiv (~1 día + tiempo de moderación)
- Subir preprint a bioRxiv (categoría: Genomics).
- Esperar aprobación de moderación (típicamente 24–48h).
- Obtener DOI de bioRxiv.

### Fase 3 — Envío a PCI Genomics
- Completar cover note (ver §6).
- Identificar 1–3 recommenders potenciales (ver §7).
- Enviar solicitud de recomendación a través del portal PCI Genomics.
- Esperar confirmación de que un recommender toma el artículo.

### Fase 4 — Durante la evaluación
- Contestar revisiones con tono sobrio y sin pelear por matices menores.
- Si piden aclaraciones metodológicas razonables, incorporarlas.
- Si detectan problemas reales, corregirlos de inmediato.

### Fase 5 — Si se recomienda
- Usar la evaluación PCI como respaldo citable.
- Decidir entre Peer Community Journal, un PCI-friendly journal o una revista externa.
- Si es revista externa, mandar inquiry previa con el link a la evaluación PCI.

---

## 9) Riesgos que pueden trabar la aceptación

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|------------|
| Falta de DOI/permalink del código | **Baja** (¡Resuelto!) | OK |
| Preprint no publicado en bioRxiv | **Alta** (aún no subido) | Blocker duro — resolver en Fase 2 |
| Manuscrito sin líneas numeradas | **Alta** (formato .md actual) | Resolver en Fase 1 |
| Framing demasiado terapéutico | **Baja** (ya corregido) | Verificar en revisión final |
| Datos no totalmente reproducibles | **Media** (pipeline no verificado de punta a punta) | Resolver en Fase 0 |
| Cita o referencia dudosa | **Baja** (todas con PMID/DOI) | OK |
| Simultaneidad con otra sumisión | **Nula** | OK |
| Reviewer solicita deconvolución celular | **Alta** | Ya anticipado en §5 del manuscrito |
| GWAS fuente (Kerrebijn) sigue como preprint | **Media** | Ya explicitado como limitación §5 item 7 |

---

## 10) Decisión recomendada

El manuscrito está científicamente listo. El framing, las limitaciones, y la sección de código/datos ya están en el estado correcto para PCI Genomics.

**Los únicos blockers son operativos:**
1. ~~Repositorio GitHub público + release `v1.0.0`~~ ✅ https://github.com/Grizaceo/protein-lab
2. ~~DOI de Zenodo~~ ✅ `10.5281/zenodo.20250218`
3. Preprint publicado en bioRxiv
4. PDF con líneas numeradas

**No enviar a PCI hasta tener los 4 ítems anteriores resueltos.**

El siguiente paso inmediato es la **Fase 0**: publicar el repositorio de scripts en GitHub y obtener el DOI de Zenodo.
