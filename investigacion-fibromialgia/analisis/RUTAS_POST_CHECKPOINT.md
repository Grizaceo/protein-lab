# RUTAS POST-CHECKPOINT — Fibromialgia

**Fecha:** 2026-05-13  
**Base:** `CHECKPOINT_AUDITADO_2026-05-13.md` + auditoría de `literatura/adicional_grounding/`.

Este archivo deja anotadas las dos rutas oficiales que quedan abiertas. No decide por ti; solo deja el terreno limpio para que elijas sin pisar alucinaciones.

---

## Ruta A — Mastocito / basófilo / IgG periférica

### Pregunta central

¿Existe en fibromialgia un subtipo donde auto-IgG, mastocitos/basófilos y mediadores como IL-6/histamina/triptasa contribuyen al dolor periférico?

### Base validada localmente

1. **Señal transcriptómica propia en GSE67311**
   - CPA3 DOWN
   - MS4A2 DOWN
   - FCER1A DOWN
   - HDC DOWN

   Interpretación limpia: señal coordinada de mastocitos/basófilos en sangre completa. No prueba migración, pero justifica investigar eje mastocito/basófilo.

2. **Jones et al. 2016 / GSE67311**
   - PMID 27157394
   - PMC4888802
   - Fulltext XML local: `literatura/adicional_grounding/verified/fulltext_xml/PMC4888802_Jones_2016_GSE67311.xml`

3. **Goebel et al. 2021 — IgG transfer**
   - PMID 34196305
   - PMC8245181
   - DOI 10.1172/JCI144201
   - Fulltext XML local.

   Uso permitido: sostener que existe evidencia experimental de que IgG de pacientes FM puede transferir rasgos de dolor a ratones.

4. **Theoharides et al. 2019 — mast cells/neuroinflammation/FM**
   - PMID 31427928
   - PMC6687840
   - DOI 10.3389/fncel.2019.00353
   - Fulltext XML local.

   Uso permitido: hipótesis publicada de mastocitos en neuroinflamación/dolor FM. No es prueba definitiva.

5. **Ang et al. 2015 — Ketotifen trial**
   - PMID 25370135
   - PMC4417653
   - DOI 10.1097/AJP.0000000000000169
   - Fulltext XML local.

   Uso permitido: estabilizar mastocitos con ketotifen no mostró beneficio significativo en ese ensayo. Esto evita entusiasmo falso.

6. **CPA3 y HDC como grounding celular**
   - CPA3 review: PMID 35159379 / PMC8834431 / DOI 10.3390/cells11030570
   - HDC review: PMID 30654600 / PMC6359378 / DOI 10.3390/ijms20020376
   - Fulltext XML local.

### Base con cautela

- **Blanco et al. 2010**: mastocitos aumentados en piel FM. PMID 20428906 / DOI 10.1007/s10067-010-1474-7. Metadata verificada, pero sin fulltext local.
- **Krock et al. 2023**: anti-SGC IgG relacionado con severidad. PMID 37683961 / DOI 10.1016/j.bbi.2023.09.003. Metadata verificada, pero sin fulltext local.
- **Seefried et al. 2025**: autoantibodies in FMS. PMID 39907533 / DOI 10.1097/j.pain.0000000000003535. Metadata verificada, pero sin fulltext local.
- **af Ekenstam et al. 2026**: blood biomarkers / CD40 / anti-SGC. PMID 41271190 / DOI 10.1016/j.bbi.2025.106185. Metadata verificada, pero sin fulltext local.
- **Sanchez et al. 2025 bioRxiv Mrgprb2/MRGPRX2**: DOI 10.1101/2025.05.15.652596. Existe y fue leído externamente, pero no quedó fulltext local limpio por Cloudflare. Bajo criterio estricto: watchlist, no pilar fuerte.

### Claims prohibidos en esta ruta

- “FM es una enfermedad autoinmune mastocitaria” como afirmación general.
- “Los mastocitos migran a tejidos” como hecho probado por GSE67311. Es hipótesis.
- “Ketotifen/cromoglicato/omalizumab son tratamientos probados para FM”. No lo son.
- “MRGPRX2 es Tier 1” mientras Sanchez no esté localmente descargado/peer-reviewed.

### Qué podría hacer esta ruta si la elegimos

- Rehacer grounding específico de mastocitos/basófilos con solo papers locales o metadata verificada.
- Buscar fulltext/PDF de Blanco 2010, Krock 2023, Seefried 2025, af Ekenstam 2026.
- Separar señal mastocito vs basófilo: CPA3/GATA2/HDC/MS4A2/FCER1A no equivalen a “mastocitos puros”.
- Diseñar una matriz de evidencia por tipo celular: mastocito, basófilo, SGC, DRG neuron, nociceptor.

### Calidad actual

Biológicamente interesante y conectada con nuestros DEGs. Pero todavía mecanísticamente frágil. Buena para investigar causa/subtipo; mala para saltar directo a tratamiento.

---

## Ruta B — MOR / Low-Dose Naltrexone (LDN)

### Pregunta central

¿LDN/MOR es la ruta de repurposing más sobria porque tiene fármaco existente, target estructuralmente claro y literatura clínica directa en FM?

### Base validada localmente

1. **ESM2 local**
   - MOR es outlier global en embeddings mean-pooled.
   - Uso permitido: MOR ocupa un espacio representacional distinto de los targets inmune/inflamatorios estudiados.
   - Uso prohibido: inferir eficacia clínica o pocket binding desde mean pooling.

2. **PDB MOR local corregido**
   - `datos/pdb/4DKL_MOR.pdb`: MOR con antagonista morphinan.
   - `datos/pdb/5C1M_MOR.pdb`: MOR activo con agonista BU72.

   Uso permitido: MOR tiene estructura experimental sólida y pocket GPCR clásico.

3. **Younger et al. 2009 LDN pilot**
   - PMID 19453963
   - PMC2891387
   - DOI 10.1111/j.1526-4637.2009.00613.x
   - Fulltext XML local.

   Uso permitido: evidencia piloto inicial positiva. Limitación: estudio pequeño.

### Base con cautela

- **Lancet Rheumatology 2024 naltrexone 6 mg trial**
  - PMID 38258677
  - DOI 10.1016/S2665-9913(23)00278-3
  - Metadata verificada, pero sin fulltext local.
  - Importante porque puede ser neutral/negativo o matizar el optimismo LDN.

- **LDN meta-analysis 2025**
  - PMID 40540205
  - DOI 10.1007/s11916-025-01411-1
  - Metadata verificada, pero sin fulltext local.
  - No usar como conclusión hasta obtener fulltext.

### Claims prohibidos en esta ruta

- “LDN está probado como tratamiento eficaz para FM” sin matices.
- “MOR outlier ESM2 explica la eficacia clínica”. No lo explica.
- “LDN cura FM”. No.

### Qué podría hacer esta ruta si la elegimos

- Conseguir fulltext del Lancet Rheumatology 2024 y meta-analysis 2025.
- Construir tabla RCT por RCT: dosis, n, diseño, outcome primario, resultado, sesgo.
- Mapear farmacología LDN: MOR antagonism, TLR4/microglia claims, endorphin rebound; separar lo demostrado de lo especulativo.
- Revisar si LDN conecta con la ruta mastocito/IgG por neuroinmunomodulación o si es ruta ortogonal.

### Calidad actual

Más sobria para repurposing porque hay fármaco y target estructural. Pero la evidencia clínica puede estar mezclada; antes de emocionarse hay que auditar RCTs modernos.

---

## Recomendación DAVI

Si quieres entender el mecanismo de fondo: elige **Ruta A**.

Si quieres una ruta de intervención/repurposing más aterrizada: elige **Ruta B**.

Mi inclinación honesta: primero **Ruta B por sobriedad clínica**, pero mantener **Ruta A** como hipótesis biológica principal. La Ruta A explica mejor nuestros DEGs; la Ruta B es más accionable hoy.
