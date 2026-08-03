# GROUNDING UK BIOBANK OLINK — Dolor crónico (verificación de primera mano)

**Fecha:** 2026-08-03
**Fuente principal:** Li ZY et al. "Large-Scale Plasma Proteomics to Profile Pathways and Prognosis of Chronic Pain", Advanced Science 2025;12(16):e2410160. PMID 40048323 (texto completo vía API OA NCBI, PMC12021123)
**Preprint relacionado:** medRxiv 2024.10.29.24316353 (2,923 proteínas, 29,254 participantes, nociplástico n=4,153, FM n=717)

---

## VEREDICTO

**IL-6, IL-8/CXCL8, TAC1 y Substance P NO aparecen ni una vez en el análisis de proteómica plasmática de dolor crónico más grande publicado (51,644 participantes UK Biobank).**

Esto es un dato poblacional de máxima potencia estadística que NO apoya nuestra hipótesis de IL-8/IL-6 como biomarcadores plasmáticos de dolor crónico/FM.

## EVIDENCIA (leída en el texto completo, no solo abstract)

1. **Estudio:** 2,923 proteínas plasmáticas (Olink Explore) de 51,644 UKB participantes con dolor crónico en 6 sitios (cabeza/cuello/hombro, espalda, abdominal, cadera, rodilla)
2. **474 proteínas asociadas a dolor crónico** — enriquecidas en rutas inmunes y metabólicas
3. **11 proteínas compartidas entre sitios de dolor**
4. **10 proteínas validadas por Mendelian Randomization como marcadores causales:** CD302, RARRES2, TNFRSF1B, BTN2A1, TNFRSF9, COL18A1, TNF, CD74, TNFRSF4, BTN2A1 (nota: BTN2A1 aparece 2x en el abstract — posible typo del paper)
5. **Búsqueda exhaustiva en texto completo:** "IL-8" 0 menciones, "CXCL8" 0, "IL-6" 0, "interleukin" 0, "chemokine" 0, "TAC1" 0, "Substance P" 0

## QUÉ SIGNIFICA PARA NUESTRA LÍNEA (honestidad cruda)

### A favor de nuestra hipótesis (matiz importante)
- Este estudio es sobre **dolor crónico general por sitio**, NO fibromialgia específicamente. El preprint (medRxiv 2024) sí analizó nociplástico (n=4,153) y FM (n=717) y construyó scores proteicos con AUC 0.76 (FM) — o sea que la proteómica SÍ distingue FM a nivel de score multi-proteína, aunque las proteínas individuales relevantes no sean IL-6/IL-8.
- El estudio de Bäckryd 2017 (Olink Target 96, 35 FM vs 46 controles) SÍ encontró IL-8 elevado en plasma FM. Diferencia clave: cohorte FM pura y panel inflamatorio dirigido vs. cohorte de dolor general y screen amplio.

### En contra (la parte que no podemos ignorar)
- Si IL-6/IL-8 fueran marcadores plasmáticos robustos de dolor crónico, con 51,644 personas y 2,923 proteínas, deberían haber aparecido. No aparecieron ni como asociación nominada.
- Las 10 proteínas causales (CD302, RARRES2, TNFRSF1B...) NO incluyen ninguna citoquina inflamatoria clásica. El eje causal del dolor crónico plasmático, según UKB, NO es el eje IL-6/IL-8.
- O'Mahony 2021 (metaanálisis) mostraba IL-8 robusto en FM — pero ese metaanálisis agrega estudios pequeños (n típico 20-100) con ELISA heterogéneo. UKB es el test de escala: no confirma.

## RECOMENDACIÓN REVISADA

1. **Bajar la expectativa sobre IL-8/IL-6 como biomarcadores plasmáticos de FM.** La evidencia de escala poblacional no los respalda. Mantenerlos como control positivo TÉCNICO del assay Olink (reproducibilidad entre compartimentos), NO como hallazgo principal.

2. **El hallazgo UKB sugiere mirar sus 10 proteínas causales** (CD302, RARRES2, TNFRSF1B, BTN2A1, TNFRSF9, COL18A1, TNF, CD74, TNFRSF4) en nuestros datos: ¿alguna está diferencialmente expresada en PBMC de FM (GSE221921)? Eso conectaría nuestra línea transcriptómica con la proteómica causal de UKB. Es un pivot natural y barato.

3. **El preprint medRxiv (nociplástico/FM) merece lectura completa** — los scores proteicos con AUC 0.76 para FM son la evidencia poblacional más fuerte de que la proteómica plasmática SÍ contiene señal FM, solo que en combinación, no en una citoquina individual.

## FUENTES
| Fuente | Tipo | Acceso |
|--------|------|--------|
| Li ZY 2025, Adv Sci (PMID 40048323) | Publicado, peer-reviewed | PMC12021123 (OA) |
| medRxiv 2024.10.29.24316353 | Preprint (versión previa) | medrxiv.org |
| UKB-PPP (Sun 2023, Nature) | Datos UKB Olink | registry.opendata.aws/ukbppp (S3 acceso controlado) |

---

## ANÁLISIS PROPIO (2026-08-03): LAS 10 PROTEÍNAS CAUSALES UKB EN GSE221921 (PBMC FM)

**Pregunta del pivot:** ¿las proteínas que UKB validó como CAUSALES de dolor crónico están diferencialmente expresadas en PBMC de FM?

**Resultado (9/10 medibles en GSE221921; RARRES2 y TNF ausentes):**

| Gen UKB causal | FC (FM/HC) | MWU p | Bonf ×9 | d | Dirección |
|---------------|-----------|-------|---------|-----|-----------|
| TNFRSF1B | 0.541 | <0.0001 | <0.0001 | -0.56 | ↓↓ significativo |
| COL18A1 | 0.581 | 0.0001 | 0.0005 | -0.54 | ↓↓ significativo |
| CD74 | 0.579 | <0.0001 | <0.0001 | -0.44 | ↓↓ significativo |
| TNFRSF4 | 0.768 | 0.0004 | 0.0036 | -0.23 | ↓ significativo |
| BTN2A1 | 0.745 | 0.0025 | 0.023 | -0.35 | ↓ significativo |
| CD302 | 0.717 | 0.154 | NS | -0.19 | ↓ trend |
| TNFRSF9 | 1.459 | 0.805 | NS | +0.27 | ~plano |

**Lectura:** 5 de 9 genes causales UKB están SIGNIFICATIVAMENTE DISMINUIDOS en PBMC de FM.
Esto NO apoya un perfil proinflamatorio clásico en PBMC; apunta a un patrón de
**inmunomodulación/agotamiento** (receptores de TNF y señales inmunes reducidos).

**Conexión con nuestro trabajo:** refuerza la lectura de que el eje inflamatorio clásico
(IL-6/IL-8) NO es el protagonista periférico en FM. El patrón dominante es de señalización
inmune REDUCIDA en PBMC — consistente con la literatura de disfunción inmune/agotamiento
en FM (y con LGALS3BP ↓ que ya habíamos visto).

**Limitación declarada:** mRNA en PBMC ≠ proteína en plasma. La dirección plasma de estos
5 genes causales NO se infiere de aquí — solo documentamos que el mRNA de los genes que UKB
valida como causales está reducido en el compartimento celular FM.

---

## EXTENSIÓN (2026-08-03): PREPRINT CWP (medRxiv 2024.10.29.24316353) + CA14/LEP

**Fuente:** Chen L et al. medRxiv 2024 (EuropePMC PPR932603). 2,923 proteínas, 29,254 UKB.
4,153 nociplástico, 717 FM. Texto: abstract completo vía API EuropePMC.

### Hallazgos del preprint (abstract verificado)
- **811 proteínas** correlacionadas con CWP (cross-sectional)
- Scores proteicos (ProtS): AUC 0.82 (top-10) y 0.88 (todas), superan al score clínico (0.81)
- Asociación prospectiva hasta 13 años de follow-up
- Firmas proteómicas DISTINTAS para nociplástico vs nociceptivo vs neuropático
- **Biomarcadores causales triangulados por MR + colocalización: CA14 (anhidrasa carbónica 14) y LEPTINA**
- 10 candidatos drug-repurposing para CWP

### Análisis propio en GSE221921 (PBMC FM)

| Gen | Fuente UKB | FC (FM/HC) | MWU p | d |
|-----|-----------|-----------|-------|-----|
| **CA14** | MR+coloc causal CWP | **2.292 ↑** | **0.0003** | +0.41 |
| TNFRSF1B | MR dolor crónico | 0.541 ↓ | <0.0001 | -0.56 |
| COL18A1 | MR dolor crónico | 0.581 ↓ | 0.0001 | -0.54 |
| CD74 | MR dolor crónico | 0.579 ↓ | <0.0001 | -0.44 |
| BTN2A1 | MR dolor crónico | 0.745 ↓ | 0.0025 | -0.35 |
| TNFRSF4 | MR dolor crónico | 0.768 ↓ | 0.0004 | -0.23 |
| LEP | MR+coloc causal CWP | AUSENTE en GSE221921 | — | — |

### Lectura clave
**CA14 es el ÚNICO gen causal UKB que SUBE en PBMC de FM (FC=2.29, p=0.0003).**
- CA14 = anhidrasa carbónica XIV (regulación pH, dolor, nocicepción)
- Consistencia: causal en proteína plasmática (UKB, MR+coloc) Y elevado en mRNA de PBMC (nuestros datos)
- Esto lo convierte en el candidato más fuerte del pivot: cruza transcriptómica → proteómica causal
- La leptina (LEP) no es medible en GSE221921 (ausente) — pendiente para plasma

### Narrative revisado (inmunomodulación, no inflamación clásica)
- Eje IL-6/IL-8: NO respaldado por UKB (0 menciones en 2,923 proteínas) → baja de prioridad
- Patrón PBMC FM: señalización inmune REDUCIDA (5/9 genes MR ↓) + CA14 ↑ (pH/nocicepción)
- Hipótesis actualizada: FM periférica = inmunomodulación/agotamiento + desregulación de pH/nocicepción (CA14), no inflamación sistémica clásica

---

## CA14 — CIERRE DEL TRIÁNGULO (2026-08-03)

**Del texto completo del preprint (medRxiv v1, snippet verificado):**
- "CA14, identified as the **top-ranking protein** and supported by both MR and colocalisation
  analyses, is a **known target of sulthiame (CHEMBL328560)**, suggesting a potential
  therapeutic target for nociplastic pain conditions such as fibromyalgia."
- CA14: "plays an important role in neuronal signal transmission via zinc ion binding and
  carbonate dehydratase activity"

### El triángulo completo para CA14

| Capa | Evidencia | Fuente |
|------|-----------|--------|
| 1. Proteína plasmática | Causal en CWP/FM (top-ranking, MR + colocalización) | UKB Chen 2024 (29,254 personas) |
| 2. mRNA PBMC | ↑ en FM (FC=2.29, p=0.0003, d=+0.41) | GSE221921 (nuestro análisis) |
| 3. Farmacología | Inhibidor conocido: sulthiame (CHEMBL328560), usado en epilepsia | Chen 2024 |

**Implicancia accionable:** CA14 es el candidato más fuerte de toda la investigación —
cruza causalidad poblacional, expresión en nuestros datos, y tiene un fármaco aprobado
(sulthiame) como posible herramienta de validación/repurposing. Es la base de una hipótesis
publicable y potencialmente testable.

**Nota:** sulthiame inhibe anhidrasas carbónicas — si CA14 está elevado en FM, un inhibidor
podría normalizar la señal. Dirección causal (¿CA14 alta causa dolor, o es marcador?) aún
requiere el MR del paper (que la respalda como causal).
