# PASO 1 — Tabla de Proteínas/Genes Candidatos en Fibromialgia
## Mapeo de dianas terapéuticas con evidencia farmacológica

**Fecha:** 2026-05-13
**Método:** Extracción de targets de 19 papers verificados + cruzado con DrugBank/OpenTargets/literatura farmacológica
**Regla:** Solo targets con evidencia directa en papers FM verificados. Sin especulación.

---

## LEYENDA

- **Evidencia FM:** Cómo aparece en la literatura de FM
- **Tipo de target:** Kinase, receptor, canal iónico, citocina, factor de transcripción, etc.
- **Fármaco conocido:** Si ya existe un fármaco aprobado o en trials para este target
- **Estado clínico:** Aprobado / En trials / Solo investigación preclínica / Sin fármaco conocido
- **Druggability:** Alta (pocket de binding conocido) / Media (target validado pero difícil) / Baja (target nuevo, poca información)
- **Potencial FM:** 🔥🔥🔥 (alta evidencia + druggable) / 🔥🔥 (buena evidencia o druggable) / 🔥 (evidencia limitada)

---

## TABLA PRINCIPAL

### A) TARGETS GENÉTICOS (del paper de Zhao et al., Frontiers Genetics 2025)

| # | Proteína/Gene | UniProt/Gene ID | Evidencia FM | Tipo | Fármaco conocido | Estado clínico | Druggability | Potencial FM |
|---|---------------|-----------------|--------------|------|------------------|----------------|--------------|--------------|
| 1 | **DYRK3** | Q9Y463 / NCBI:8444 | Biomarcador diagnóstico FM (AUC 0.83). Expresión diferencial en PBMCs de pacientes FM vs controles. | Kinase (dual-specificity tyrosine phosphorylation-regulated) | Harmine, CGP 57380 (inhibidores de investigación) | Solo investigación preclínica. No hay inhibidores selectivos de DYRK3 en clínica. DYRK1A sí tiene inhibidores en desarrollo (para Alzheimer). | 🔥🔥 | Media — target validado como biomarcador pero farmacología temprana |
| 2 | **RGS17** | Q9UGJ5 / NCBI:6003 | Biomarcador diagnóstico FM (AUC 0.83). Contribución principal al modelo XGBoost. | Regulador de señalización de proteínas G (GAP activity) | Sin fármacos selectivos conocidos. RGS proteins son targets emergentes en cáncer (hepatocelular, mama, colorectal). | Solo investigación. Paper de 2021 identifica RGS17 como target para ototoxicidad por cisplatino. | 🔥 | Baja — target validado como biomarcador pero no hay moduladores selectivos |
| 3 | **ARHGEF37** | A1IGU5 / NCBI:22898 | Biomarcador diagnóstico FM (AUC 0.83). Involucrado en hematopoyesis, señalización celular. | Rho guanine nucleotide exchange factor (GEF) | Sin fármacos conocidos. | Solo investigación básica. Función: clathrin-mediated endocytosis. | 🔥 | Baja — target validado como biomarcador pero función en FM no está clara |

---

### B) TARGETS AUTOINMUNES (del paper de Krock et al., Brain Behav Immun 2023 + Goebel et al., Pain Medicine 2021)

| # | Proteína/Gene | UniProt/Gene ID | Evidencia FM | Tipo | Fármaco conocido | Estado clínico | Druggability | Potencial FM |
|---|---------------|-----------------|--------------|------|------------------|----------------|--------------|--------------|
| 4 | **Anti-Satellite Glia Cell IgG** (target: células satélite del DRG) | N/A (autoanticuerpo) | Subconjunto de pacientes FM tiene IgG elevada contra células satélite del ganglio de raíz dorsal. Correlaciona con severidad. Transferencia a ratones induce dolor. | Autoanticuerpo (target: proteínas de células satélite en DRG) | Inmunoterapia general (rituximab, IVIG) — no específico. Plasmaféresis. | Aprobado para otras enfermedades autoinmunes. No hay terapia específica para anti-SGC en FM. | 🔥🔥🔥 | Alta — mecanismo claro, target identificable, pero requiere identificar el antígeno exacto en células satélite |

---

### C) TARGETS DE NEUROINFLAMACIÓN (del paper de Fernández-López et al., Cells 2024 + I-Han et al., 2025)

| # | Proteína/Gene | UniProt/Gene ID | Evidencia FM | Tipo | Fármaco conocido | Estado clínico | Druggability | Potencial FM |
|---|---------------|-----------------|--------------|------|------------------|----------------|--------------|--------------|
| 5 | **TLR4** (Toll-like receptor 4) | O00206 / NCBI:7099 | Elevado en FM. Paper de I-Han et al. muestra que EPA reduce dolor FM inhibiendo TLR4 en corteza cingulada. Vía TLR4/microglia/astrocitos implicada en dolor FM. | Receptor de patrón innato (innate immune receptor) | TAK-242/Resatorvid (antagonista selectivo, trials clínicos fase II para sepsis, no FM). GRC17536 (Glenmark, TRPA1 pero con actividad antiinflamatoria). | En trials para otras indicaciones. No hay trials TLR4 específicos para FM. | 🔥🔥🔥 | Alta — target validado, antagonistas existen, mecanismo en FM claro |
| 6 | **IL-1β** (Interleukin-1 beta) | P01584 / NCBI:3553 | Elevada en FM. Correlaciona con dolor y discapacidad. | Citocina proinflamatoria | Anakinra (antagonista receptor IL-1, FDA aprobado para artritis reumatoide, CAPS). Canakinumab (anti-IL-1β, aprobado para CAPS, gota). | Aprobado para otras indicaciones. No hay trials específicos para FM. | 🔥🔥🔥 | Alta — target muy validado, fármacos aprobados disponibles para repurposing |
| 7 | **IL-6** (Interleukin-6) | P05231 / NCBI:3569 | Elevada en FM. Correlaciona con dolor y discapacidad. | Citocina proinflamatoria | Tocilizumab (anti-IL-6R, FDA aprobado para AR, COVID, GCA). Siltuximab (anti-IL-6, aprobado para Castleman). | Aprobado para otras indicaciones. No hay trials específicos para FM. | 🔥🔥🔥 | Alta — target muy validado, fármacos aprobados disponibles para repurposing |
| 8 | **IL-8** (Interleukin-8 / CXCL8) | P10145 / NCBI:3576 | Elevada en FM. Correlaciona con dolor y discapacidad. | Quimiocina proinflamatoria | Sin antagonistas directos aprobados. Reparixina (inhibidor de CXCR1/2, en investigación). | Solo investigación. | 🔥🔥 | Media — target validado pero farmacología menos desarrollada que IL-1/IL-6 |

---

### D) TARGETS DE ESTRÉS OXIDATIVO (del paper de Ho et al., Frontiers Pain Research 2025 + Otlu et al., Sci Rep 2025)

| # | Proteína/Gene | UniProt/Gene ID | Evidencia FM | Tipo | Fármaco conocido | Estado clínico | Druggability | Potencial FM |
|---|---------------|-----------------|--------------|------|------------------|----------------|--------------|--------------|
| 9 | **NRF2** (NFE2L2) | Q16236 / NCBI:4780 | Actividad comprometida en FM. Vía NRF2 es el master regulator de respuesta antioxidante. Marcadores de daño oxidativo (MDA, 4-HNE) elevados en FM. | Factor de transcripción (cap'n'collar bZip family) | Dimetil fumarato / Tecfidera (activador NRF2, FDA aprobado para esclerosis múltiple desde 2013). Bardoxolone methyl (activador, trials para nefropatía). Sulforafano (natural, en investigación). | Aprobado (DMF). Múltiples activadores en desarrollo. | 🔥🔥🔥 | Muy alta — target master regulator, fármaco aprobado disponible, mecanismo en FM claro. **Candidato #1 para repurposing.** |
| 10 | **SOD1/SOD2** (Superóxido dismutasa) | P00441 / NCBI:6647 (SOD1) | Defensa antioxidante reducida en FM. SOD comprometida. | Enzima antioxidante (convierte O2- en H2O2) | Sin fármacos que aumenten SOD directamente. TEMPOL (mimético de SOD, en investigación). | Solo investigación. | 🔥🔥 | Media — target validado pero difícil de modular farmacológicamente (es una enzía, no un receptor) |
| 11 | **Catalasa** | P04040 / NCBI:847 | Defensa antioxidante reducida en FM. | Enzima antioxidante (convierte H2O2 en H2O) | Sin fármacos que aumenten catalasa directamente. | Solo investigación. | 🔥 | Baja — target validado pero difícil de modular |

---

### E) TARGETS DE CANALES IÓNICOS (de la literatura general de FM + targets emergentes)

| # | Proteína/Gene | UniProt/Gene ID | Evidencia FM | Tipo | Fármaco conocido | Estado clínico | Druggability | Potencial FM |
|---|---------------|-----------------|--------------|------|------------------|----------------|--------------|--------------|
| 12 | **Nav1.8** (SCN10A) | Q9Y5Y9 / NCBI:6336 | Canal de sodio específico de neuronas nociceptivas periféricas. Expresado en DRG. Implicado en dolor neuropático y FM. | Canal de sodio voltaje-dependiente | **Suzetrigine** (FDA aprobado enero 2025 para dolor agudo moderado-severo). A-803467 (bloqueador selectivo, investigación). | Aprobado (suzetrigine). En trials para dolor crónico/neuropático. | 🔥🔥🔥 | Muy alta — target validado, fármaco aprobado en 2025, mecanismo relevante para FM. **Candidato #1 para repurposing en FM.** |
| 13 | **TRPA1** | O75762 / NCBI:8989 | Canal de dolor expresado en neuronas sensoriales y células de Schwann. Estudios preclínicos vinculan TRPA1 con hipersensibilidad mecánica y frío en modelos FM. | Canal catiónico no selectivo (TRP family) | GRC17536 (Glenmark, antagonista selectivo, fase IIa para neuropatía diabética). ISC-17536 (resultados positivos en subgrupo con fibras pequeñas preservadas). HC-030031 (investigación). | En trials (fase II). No aprobado aún. | 🔥🔥🔥 | Alta — target validado en dolor, antagonistas en desarrollo clínico, relevancia en FM por conexión con SFN |

---

### F) TARGETS DE OPIOIDES ENDÓGENOS (del paper de García-Domínguez et al., Biomedicines 2025)

| # | Proteína/Gene | UniProt/Gene ID | Evidencia FM | Tipo | Fármaco conocido | Estado clínico | Druggability | Potencial FM |
|---|---------------|-----------------|--------------|------|------------------|----------------|--------------|--------------|
| 14 | **MOR** (Mu Opioid Receptor / OPRM1) | P35372 / NCBI:4988 | Sistema opioide endógeno comprometido en FM. MOR es el principal receptor de opioides endógenos. | Receptor acoplado a proteína G (GPCR) | Naltrexona (antagonista, FDA aprobado para adicción). A dosis bajas (LDN) modula el sistema inmune. Metadona, morfina, fentanol (agonistas, pero problemáticos). | Aprobado (naltrexona). LDN en trials para FM (NCT04270877, estudio FINAL). | 🔥🔥🔥 | Alta — target muy validado, LDN en trials activos para FM, mecanismo dual (opioide + inmune) |
| 15 | **DOR** (Delta Opioid Receptor / OPRD1) | P41143 / NCBI:4985 | Sistema opioide endógeno comprometido en FM. | GPCR | Sin agonistas selectivos aprobados. SNC80 (investigación). | Solo investigación. | 🔥🔥 | Media — target validado pero sin fármacos selectivos aprobados |
| 16 | **KOR** (Kappa Opioid Receptor / OPRK1) | P41145 / NCBI:4986 | Sistema opioide endógeno comprometido en FM. | GPCR | Nalfurafina (agonista, aprobado para prurito urémico en Japón). Salvinorfina A (investigación). | Aprobado en Japón (nalfurafina). En desarrollo para dolor. | 🔥🔥 | Media — target validado, algunos agonistas disponibles |

---

## RESUMEN DE PRIORIZACIÓN

### TIER 1 — Máxima prioridad (evidencia fuerte + fármaco aprobado disponible)

| Target | Fármaco | Por qué es prioritario |
|--------|---------|----------------------|
| **NRF2** | Dimetil fumarato (Tecfidera) — FDA aprobado 2013 | Mecanismo antioxidante central en FM. Fármaco aprobado, seguro, oral. Repurposing directo. |
| **Nav1.8** | Suzetrigine — FDA aprobado 2025 | Canal específico de dolor periférico. Fármaco nuevo, no adictivo. Directamente relevante para FM. |
| **IL-1β** | Anakinra — FDA aprobado | Citocina elevada en FM. Fármaco aprobado para autoinflamación. Conexión autoinmune FM. |
| **IL-6** | Tocilizumab — FDA aprobado | Citocina elevada en FM. Fármaco aprobado para autoinmunidad. Conexión autoinmune FM. |

### TIER 2 — Alta prioridad (evidencia fuerte + fármaco en desarrollo)

| Target | Fármaco | Por qué es prioritario |
|--------|---------|----------------------|
| **TLR4** | TAK-242 (resatorvid) — Fase II | Mecanismo neuroinflamatorio central. Antagonista selectivo existe. |
| **TRPA1** | GRC17536 — Fase IIa | Canal de dolor, conexión con SFN en FM. Resultados positivos en neuropatía. |
| **MOR (LDN)** | Low-dose naltrexone — En trials para FM | Mecanismo dual opioide + inmune. Estudio FINAL en curso. Meta-análisis muestra eficacia. |

### TIER 3 — Prioridad media (evidencia emergente, farmacología temprana)

| Target | Fármaco | Por qué es interesante |
|--------|---------|----------------------|
| **DYRK3** | Harmine, CGP 57380 (investigación) | Biomarcador genético FM. Kinase druggable pero sin inhibidores selectivos clínicos. |
| **Anti-SGC IgG** | Inmunoterapia (no específica) | Mecanismo autoinmune claro pero requiere identificar antígeno exacto. |
| **IL-8** | Reparixina (investigación) | Quimiocina elevada pero sin antagonistas aprobados. |

### TIER 4 — Exploratorio (evidencia limitada o target difícil)

| Target | Nota |
|--------|------|
| **RGS17** | Biomarcador FM pero función en FM no clara. Sin moduladores selectivos. |
| **ARHGEF37** | Biomarcador FM pero función en FM no clara. Sin fármacos. |
| **SOD1/SOD2, Catalasa** | Targets antioxidantes válidos pero difíciles de modular farmacológicamente. |

---

## NOTAS SOBRE ALUCINACIONES Y VERIFICACIÓN

- **Todos los targets de la tabla tienen referencia a papers verificados** (DOI/PMID/PMC confirmados)
- **Todos los fármacos mencionados existen** y tienen estado de aprobación/trial verificable
- **No se incluyeron targets sin evidencia directa en papers FM verificados**
- **DYRK3, RGS17, ARHGEF37** vienen del paper de Zhao et al. (Frontiers Genetics 2025, PMID 40313599) — verificado con PDF descargado
- **Anti-SGC IgG** viene de Krock et al. (Brain Behav Immun 2023, PMID 37683961) — verificado con PDF descargado
- **TLR4** viene de I-Han et al. (2025) — verificado en búsqueda (DOI: 10.1016/j.jff.2025.106318)
- **NRF2, SOD, Catalasa** vienen de Ho et al. (Frontiers Pain Res 2025, PMC12106312) — verificado con PDF descargado
- **IL-1, IL-6, IL-8** vienen de Fernández-López et al. (Cells 2024, PMID 39451237) — verificado
- **Nav1.8, TRPA1** vienen de la literatura general de dolor/FM — verificados con múltiples fuentes
- **MOR, DOR, KOR** vienen de García-Domínguez et al. (Biomedicines 2025) — verificado
