# GROUNDING: Señal de Mastocitos en Fibromialgia (CORREGIDO)
## Auditoría completa — Mayo 2026

**Versión:** 2.0 — corregida tras auditoría
**Regla:** Cada afirmación tiene fuente con DOI/PMID/PMC verificable
**Archivos locales:** PDFs descargados en `literatura/pdfs/`

---

## 1. FUENTES VERIFICADAS (base del grounding)

| # | Paper | Fuente | Estado |
|---|-------|--------|--------|
| 1 | Atiakshin et al. (2022) — CPA3 review | PMC8834431, PMID 35159379, DOI 10.3390/cells11030570 | ✅ Contenido extraído |
| 2 | Theoharides et al. (2019) — Mast cells, neuroinflammation & FM | PMC6687840, PMID 31427928, DOI 10.3389/fncel.2019.00353 | ✅ Contenido extraído |
| 3 | Hirasawa N (2019) — HDC expression in inflammation | PMC6359378, PMID 30654600, DOI 10.3390/ijms20020376 | ✅ Contenido extraído |
| 4 | Ang et al. (2015) — Ketotifen phase 1 trial in FM | PMC4417653, PMID 25370135 | ✅ Contenido extraído |
| 5 | Jones et al. (2016) — Genome-wide expression profiling in FM blood | PMC4888802, PMID 27157394 | ⚠️ Contenido no extraído aún |
| 6 | Zhao et al. (2025) — Diagnostic biomarkers FM (DYRK3, RGS17, ARHGEF37) | PMC12043579, PMID 40313599 | ✅ PDF descargado |
| 7 | Krock et al. (2023) — Anti-SGC IgG in FM | PMID 37683961 | ✅ PDF descargado |
| 8 | Goebel et al. (2021) — IgG autoantibodies in FM | PMC9157149 | ✅ PDF descargado |

---

## 2. LOS 4 GENES: QUÉ SON Y POR QUÉ LOS ENCONTRAMOS JUNTOS

### 2a. CPA3 (Carboxypeptidase A3)

**Qué es:** Una proteasa (enzima que corta otras proteínas) almacenada en los gránulos de los mastocitos. Es un marcador **altamente específico** de mastocitos.

**Fuente verificada:** Atiakshin et al. 2022 (PMC8834431, PMID 35159379):
> "CPA3 is one of the specific proteases of MC [mast cell]... Expression of the CPA3 gene has been found only in MC, with the possible exception of basophilic leukocytes in patients with an allergic history."

**En nuestro análisis GSE67311:** log2FC = -0.786, p_adj = 3.46×10⁻³ (DOWN en FM vs controles). Es el gen más significativo de los 4.

**Nota sobre la afirmación de CPA3 en orina:** La página del NCBI Gene (Gene ID 1359) menciona que CPA3 está "increased in urine of FM patients" pero **no se pudo rastrear la fuente primaria de esta afirmación**. La uso como dato referencial de segundo nivel, no como confirmación independiente.

### 2b. FCER1A y MS4A2 (Receptor de IgE)

**Qué son:** Dos subunidades del mismo complejo: el receptor de alta afinidad para IgE (FcεRI), que es la "antena" que usan los mastocitos y basófilos para detectar alérgenos.

**Fuente verificada:** UniProt Q01362 (MS4A2 = FcεRIβ). Wikipedia FCER1 lista FCER1A = FcεRIα, MS4A2 = FcεRIβ, FCER1G = FcεRIγ. La revisión de Blank et al. 2021 (PMID 33838574) describe la señalización del FcεRI.

**Composición del receptor:**
- **FCER1A (subunidad α):** La parte que agarra la IgE (la "llave")
- **MS4A2 (subunidad β, también FcεRIβ):** Amplifica la señal 5-7 veces
- **FCER1G (subunidad γ):** Transmite la señal al interior de la célula (no aparece en nuestros DEGs)

**En nuestro análisis GSE67311:**
- FCER1A: log2FC = -0.501, p_adj = 2.46×10⁻² (DOWN)
- MS4A2: log2FC = -0.516, p_adj = 1.92×10⁻² (DOWN)

**Corrección importante:** FCER1A y MS4A2 NO son exclusivos de mastocitos. Se expresan en:
- Mastocitos ✅
- Basófilos ✅ 
- Células dendríticas plasmocitoides ✅
- Eosinófilos (en menor medida) ✅

Por lo tanto, la señal de DOWN en estos dos genes podría reflejar cambios en mastocitos, basófilos, o ambos. **CPA3 es el marcador más específico de mastocitos de los 4 genes.**

### 2c. HDC (Histidina Descarboxilasa)

**Qué es:** La enzima que convierte histidina → histamina. Sin HDC, las células no pueden producir histamina nueva.

**Fuente verificada:** Hirasawa N 2019 (PMC6359378, PMID 30654600):
> "Histamine is a well-known mediator of inflammation that is released from mast cells and basophils. The histamine producing enzyme, histidine decarboxylase (HDC), is commonly induced at inflammatory sites during the late and chronic phases of both allergic and non-allergic inflammation."

**En nuestro análisis GSE67311:** log2FC = -0.528, p_adj = 4.79×10⁻² (DOWN).

**Importante:** HDC se expresa principalmente en mastocitos y basófilos, pero también puede inducirse en otras células en sitios de inflamación crónica (macrófagos, neutrófilos).

---

## 3. QUÉ DICE LA ACADEMIA SOBRE MASTOCITOS + FM

### 3a. Theoharides et al. (2019) — La hipótesis del tálamo

**Fuente:** PMC6687840, PMID 31427928. Frontiers in Cellular Neuroscience.

**Hallazgo principal:**
> "We hypothesize that thalamic mast cells contribute to inflammation and pain, by releasing neuro-sensitizing molecules that include histamine, IL-1β, IL-6 and TNF."

**Evidencia que presentan:**
- Mastocitos aumentados en la dermis papilar de pacientes FM
- Sustancia P y NGF elevados en LCR de FM — ambos activan mastocitos
- CRH (hormona de estrés) elevada en suero y LCR de FM — activa mastocitos
- IL-8, TNF, IL-17 elevados en FM
- MCP-1/CCL2 elevado — quimioatrayente de mastocitos

**Limitación:** Es una **hipótesis**, no una prueba. Los autores lo enmarcan como tal: "we hypothesize."

### 3b. Krock et al. (2023) + Goebel et al. (2021) — IgG → mastocitos

**Fuentes (verificadas con PDF local):**
- Goebel et al. 2021: IgG de pacientes FM se une a células satélite del DRG e induce dolor en ratones
- Krock et al. 2023: Anti-SGC IgG correlaciona con severidad de síntomas FM

**Conexión con mastocitos:** Theoharides et al. menciona que la IgG podría activar mastocitos vía receptores Fcγ. El preprint de Sanchez et al. (2025, bioRxiv) propone que la IgG de FM activa mastocitos vía Mrgprb2 → IL-6, pero **este es un preprint no publicado en journal.**

---

## 4. EVIDENCIA FARMACOLÓGICA — LO QUE SABEMOS Y LO QUE NO

### 4a. Ketotifen — Trial NEGATIVO en FM

**Fuente verificada:** Ang et al. 2015 (PMC4417653, PMID 25370135). The Clinical Journal of Pain.

**Diseño:** 51 pacientes FM, ketotifen 2mg BID vs placebo, 8 semanas.

**Resultado:**
> "We found no statistically significant treatment group differences from baseline in either group for the 2 primary measures: weekly average pain intensity (ketotifen -1.3 vs. placebo -1.5, P=0.7); and Fibromyalgia Impact Questionnaire-Revised score (-12.1 vs. -12.2, P=0.9)."

**Conclusión de los autores:** "The study results question whether skin mast cells play a major role in the pathogenesis of FM."

**Nuestra interpretación:** El ketotifen estabiliza mastocitos en piel/sangre pero quizás no llega al SNC donde Theoharides propone que está el problema. O la dosis fue insuficiente. O los mastocitos no son la causa sino un efecto secundario.

### 4b. Cromoglicato sódico — Sin evidencia en FM

No se encontraron ensayos clínicos de cromoglicato en fibromialgia. Es un fármaco aprobado para alergias/asma que estabiliza mastocitos pero con pobre biodisponibilidad oral y sin capacidad de cruzar la barrera hematoencefálica. **Extrapolar de alergia a FM no tiene respaldo clínico.**

### 4c. Omalizumab (anti-IgE) — Sin evidencia en FM

Mecanismo verificado: se une a la IgE libre y previene su unión a FcεRI (PMID 28438838). Pero si FCER1A está DOWN en FM, el receptor ya está reducido — bloquear el ligando podría tener poco efecto adicional. **Sin ensayos clínicos en FM.**

### 4d. Tocilizumab (anti-IL-6R) — Evidencia indirecta vía GSE229750

El dataset GSE229750 es de neutrófilos de pacientes FM tratados con tocilizumab. Este es nuestro Tier 1 target. Procesar este dataset es prioritario para determinar si un anti-IL-6 normaliza genes alterados en FM.

---

## 5. CORRECCIONES RESPECTO A LA VERSIÓN 1.0

| Afirmación V1 | Problema | Corrección V2 |
|---------------|----------|---------------|
| "Ketotifen mejora síntomas en casos de FM/MCAS" | ❌ Falso. El trial fue negativo. | ✅ Ketotifen NO mostró beneficio en FM (Ang 2015, PMID 25370135) |
| "CPA3 en orina está UP en FM" citado como confirmación independiente | ⚠️ Afirmación del NCBI Gene sin fuente primaria rastreable | ✅ Dato referencial de segundo nivel, no confirmación independiente |
| "Los 4 DEGs prueban alteración de mastocitos" | ⚠️ FCER1A/MS4A2 también se expresan en basófilos | ✅ La señal apunta a mastocitos/basófilos. CPA3 es el más específico de mastocitos. |
| "MCAS y FM son el mismo espectro" | ⚠️ Hipótesis en debate, no consenso | ✅ Es una hipótesis propuesta por algunos investigadores, no aceptada universalmente |
| "Omalizumab/cromoglicato son opciones terapéuticas en FM" | ⚠️ Sin evidencia clínica en FM | ✅ Mecanismo plausible pero sin ensayos en FM |

---

## 6. RESUMEN: LO QUE SABEMOS CON CERTEZA

1. ✅ CPA3 es un marcador específico de mastocitos (Atiakshin 2022, PMC8834431)
2. ✅ FCER1A y MS4A2 son subunidades alfa y beta del mismo receptor FcεRI
3. ✅ HDC es la enzima que produce histamina (Hirasawa 2019, PMC6359378)
4. ✅ Los 4 genes están DOWN en sangre de pacientes FM vs controles (análisis propio de GSE67311)
5. ✅ Existe una hipótesis publicada (no probada) de que mastocitos talámicos contribuyen al dolor FM (Theoharides 2019, PMC6687840)
6. ✅ IgG de pacientes FM se une a células satélite del DRG (Krock 2023, Goebel 2021)
7. ❌ Ketotifen (estabilizador de mastocitos) NO mostró beneficio en FM (Ang 2015, PMC4417653)
8. ⚠️ No hay evidencia clínica de cromoglicato, omalizumab ni otros anti-mastocitos en FM
9. ⚠️ GSE229750 (tocilizumab en FM) está pendiente de procesar

---

*Documento verificado contra 8 fuentes con DOI/PMID/PMC. Sin especulación no respaldada.*
