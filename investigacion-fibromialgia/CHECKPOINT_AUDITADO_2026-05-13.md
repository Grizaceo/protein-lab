# CHECKPOINT AUDITADO — Investigación Fibromialgia

**Fecha:** 2026-05-13 20:25 America/Santiago  
**Objetivo:** dejar un punto de partida limpio para no seguir trabajando sobre alucinaciones.  
**Regla desde este checkpoint:** si un claim no está en este archivo como `VALIDADO` o `USABLE CON CAUTELA`, no se usa para decisiones posteriores sin re-verificar.

---

## 0. Resumen ejecutivo honesto

El proyecto tiene una base útil, pero la auditoría encontró problemas importantes de higiene: varios archivos marcados como “PDF” son HTML o páginas descargadas con extensión `.pdf`, y 4 estructuras PDB estaban mal asignadas al target. Eso no invalida los hallazgos de expresión génica ni los embeddings ESM2, pero sí obliga a rebajar la confianza en algunos documentos previos, especialmente `RESULTADOS_PDB.md` y el resumen de “PDFs descargados” en `REFERENCIAS.md`.

Lo que queda sólido: GSE67311 muestra una señal reproducible dentro de nuestro análisis de sangre completa, con CPA3/MS4A2/FCER1A/HDC downregulated a FDR < 0.05; GSE229750, usando los XLSX suplementarios reales de GEO, muestra solo 3 genes significativos FM vs controles en neutrófilos; ESM2 generó 11 embeddings válidos y MOR es un outlier global real en esa matriz; y las citas críticas de ketotifen, mast cells/FM, HDC, CPA3 y anti-SGC IgG existen con identificadores resolubles.

Lo que queda débil: la tabla de 16 targets es útil como mapa exploratorio, pero NO todos los targets tienen el mismo nivel de evidencia directa en fibromialgia. Nav1.8 y TRPA1 son biológicamente plausibles por dolor/DRG/SFN, pero su estatus como “target FM directo” debe tratarse con cautela. NRF2/oxidative stress, IL-1/IL-6/IL-8, auto-IgG, mastocitos/basófilos y MOR/LDN están mejor anclados, pero cada uno con limitaciones.

---

## 1. Estado auditado por fase

| Fase | Estado anterior | Estado auditado | Veredicto |
|---|---:|---:|---|
| Paso 1 — 16 targets en 4 tiers | ✅ | ⚠️ | Útil como mapa, pero requiere granular evidencia por target. No tratar todos como igualmente validados. |
| Paso 2 — GSE67311 → señal mastocitos/basófilos | ✅ | ✅ | Validado con CSV local. 8 genes FDR<5%; 4 relevantes: CPA3, MS4A2, FCER1A, HDC. |
| Grounding mastocitos/ketotifen | ✅ | ✅/⚠️ | La corrección ketotifen negativo está validada. La hipótesis mastocitos-FM sigue siendo hipótesis, no consenso. |
| Exp 1 — GSE229750 tocilizumab/neutrófilos | ✅ | ✅/⚠️ | Datos XLSX reales, pero n pequeño. Bueno para exploración, no para conclusión clínica. |
| Exp 2 — ESM2 embeddings | ✅ | ✅/⚠️ | Embeddings válidos. MOR outlier válido. Mean pooling NO sirve para pockets ni mecanismo local. |
| Exp 3 — PDB/druggability | ✅ | ❌→⚠️ corregido | 4 PDBs estaban mal asignados. Se movieron a `rejected_misassigned/` y se agregaron estructuras corregidas cuando posible. |

---

## 2. Auditoría local de archivos

### 2.1 PDFs / full text

La carpeta `literatura/pdfs/` NO debe interpretarse literalmente como “todo son PDFs”. Auditoría con `file` mostró:

**PDF reales:**
- `Ghasemikhah_2025_FrontiersNeurosci_LipidMetabolism.pdf`
- `Goebel_2021_PainMed_ResearchRecommendations.pdf`
- `Ho_2025_FrontiersPain_RedoxChronicPain.pdf`
- `Zhao_2025_FrontiersGenetics_DYRK3_RGS17_ARHGEF37.pdf`

**Archivos con extensión `.pdf` pero contenido HTML/texto:**
- `Ang_2015_PMC4417653_Ketotifen_FM_Trial.pdf`
- `Atiakshin_2022_PMC8834431_CPA3_MastCell_Review.pdf`
- `Cai_2025_Neuron_GutMicrobiotaPain.pdf`
- `Gimenez-Orenga_2025_PMC_HERV_FM_MECFS.pdf`
- `Ichikawa_2019_PMC6359378_HDC_Inflammation.pdf`
- `Krock_2023_BrainBehavImmun_AntiSGC_IgG.pdf`
- `Li_2025_FrontiersPharm_FibroPharmaUpdate.pdf`
- `Theoharides_2019_PMC6687840_MastCells_Neuroinflammation_FM.pdf`

**Implicación:** esos papers pueden estar verificados por DOI/PMID/PMC o por extracción web, pero el claim “PDF descargado y verificado” queda revocado salvo los 4 PDF reales anteriores. Desde ahora distinguir entre:
- `PDF real local`
- `HTML/full text local o extracción web`
- `verificado por identificador, sin full text local`

### 2.2 PDBs

La auditoría contra RCSB encontró 4 estructuras mal asignadas:

| Archivo viejo | Problema real | Acción |
|---|---|---|
| `7OBN_NRF2.pdb` | 7OBN es una DNA ligase, no NRF2 | movido a `datos/pdb/rejected_misassigned/` |
| `7ZYX_CPA3.pdb` | 7ZYX es un i-motif DNA, no CPA3 | movido a `rejected_misassigned/` |
| `7Q5X_MS4A2.pdb` | 7Q5X es HIF prolyl hydroxylase 2/EGLN1, no MS4A2 | movido a `rejected_misassigned/` |
| `4E1M_HDC.pdb` | 4E1M es HIV-1 integrase, no HDC | movido a `rejected_misassigned/` |

Estructuras corregidas agregadas:

| Target | Archivo corregido | Fuente | Estado |
|---|---|---|---|
| HDC | `datos/pdb/corrected/4E1O_HDC.pdb` | RCSB 4E1O, human histidine decarboxylase + histidine methyl ester | VALIDADO |
| TRPA1 + A-967079 | `datos/pdb/corrected/6V9Y_TRPA1_A967079.pdb` | RCSB 6V9Y, TRPA1 bound with A-967079 | VALIDADO |
| CPA3 | `datos/pdb/corrected/AF-P15088-F1_CPA3.pdb` | AlphaFold DB v6, UniProt P15088 | PREDICCIÓN, no PDB experimental |
| MS4A2 | `datos/pdb/corrected/AF-Q01362-F1_MS4A2.pdb` | AlphaFold DB v6, UniProt Q01362 | PREDICCIÓN, no PDB experimental |

**Regla:** `RESULTADOS_PDB.md` queda supersedido por este checkpoint en todo lo relativo a CPA3, MS4A2, HDC, 7OBN, 7Q5X, 7ZYX y 4E1M.

---

## 3. Datos ómicos auditados

### 3.1 GSE67311 — sangre completa / expresión diferencial

Archivo auditado: `datos/GSE67311_DEGs_FDR5_named.csv`.

Resultado confirmado localmente:

| Gene | log2FC | FDR/p_adj | Interpretación |
|---|---:|---:|---|
| CPA3 | -0.786268 | 0.003462 | DOWN en FM |
| C1orf150 | -0.430256 | 0.007607 | DOWN en FM |
| MS4A2 | -0.516327 | 0.019154 | DOWN en FM |
| FCER1A | -0.501249 | 0.024550 | DOWN en FM |
| ITGB8 | -0.328260 | 0.026497 | DOWN en FM |
| GATA2 | -0.451550 | 0.047922 | DOWN en FM |
| C11orf83 | -0.148509 | 0.047922 | DOWN en FM |
| HDC | -0.528351 | 0.047922 | DOWN en FM |

**Claim validado:** CPA3/MS4A2/FCER1A/HDC forman una señal coherente de mastocitos/basófilos en sangre completa, no de “mastocitos puros”. CPA3 es el marcador más específico de mastocitos; MS4A2, FCER1A y HDC también pueden reflejar basófilos y otras células FcεRI/HDC+.

**Claim prohibido:** “esto prueba migración de mastocitos a tejidos”. Eso es una hipótesis plausible, no demostrado por GSE67311.

### 3.2 GSE229750 — neutrófilos + tocilizumab

Archivos auditados:
- `datos/geo/Neutrophils_FM_tocilizumab_trial/GSE229750_FM_HC.xlsx`
- `datos/geo/Neutrophils_FM_tocilizumab_trial/GSE229750_FM_TCZ.xlsx`
- `datos/GSE229750_DEGs_FM_vs_CTRL_significant.csv`
- `datos/GSE229750_DEGs_PRE_vs_POST_significant.csv`

Resultado confirmado FM vs controles:

| Gene | log2FC_AB_C | padj_AB_C | Dirección |
|---|---:|---:|---|
| TSPAN13 | -2.477766 | 6.00e-08 | DOWN en FM |
| C3AR1 | +1.937700 | 1.03e-04 | UP en FM |
| PI3 | +0.986105 | 9.53e-04 | UP en FM |

**Claim validado:** los neutrófilos en este dataset muestran una señal FM vs control mucho más limitada que GSE67311. Esto apoya la idea de que la señal CPA3/MS4A2/FCER1A/HDC no viene de neutrófilos.

**Claim con cautela:** tocilizumab cambia muchos genes en el archivo pre/post, pero el diseño parece muy pequeño y frágil. No usar los 2605 genes como prueba fuerte de eficacia clínica ni normalización.

---

## 4. Grounding académico auditado

### 4.1 Validado

- Ketotifen en FM: Ang et al. 2015 existe como PMC4417653 / PMID 25370135; el trial fue negativo para dolor y FIQR. Claim válido: ketotifen no mostró beneficio significativo en ese estudio.
- Mast cells + FM: Theoharides et al. 2019 existe como PMC6687840 / PMID 31427928 / DOI 10.3389/fncel.2019.00353. Claim válido: es una hipótesis publicada de mastocitos talámicos/neuroinflamación, no una prueba concluyente.
- CPA3 como marcador de mastocitos: Atiakshin et al. 2022 existe como PMC8834431 / PMID 35159379 / DOI 10.3390/cells11030570. Claim válido: CPA3 es una proteasa específica/altamente característica de mastocitos, con posibles excepciones en basófilos en contexto alérgico.
- HDC/histamina: Hirasawa 2019 existe como PMC6359378 / PMID 30654600 / DOI 10.3390/ijms20020376. Claim válido: HDC produce histamina y puede inducirse en inflamación crónica.
- Anti-SGC IgG: Krock et al. 2023 existe como PMID 37683961 / DOI 10.1016/j.bbi.2023.08.012. Claim válido: anti-satellite glia cell IgG se relaciona con severidad de síntomas.
- IgG/FM: Goebel et al./passive transfer está anclado en PMC8245181 y la revisión/recomendaciones en PMC9157149. Claim válido: existe línea autoinmune IgG→dolor, especialmente en modelos animales.

### 4.2 Usable con cautela

- Sanchez et al. 2025 Mrgprb2/MRGPRX2: existe como bioRxiv 10.1101/2025.05.15.652596v1, pero es preprint. Usar como hipótesis emergente, no como evidencia clínica establecida.
- CPA3 “UP en orina FM”: aparece en NCBI Gene según revisión previa, pero no hay fuente primaria local rastreada. No usar como apoyo fuerte.
- MCAS-FM overlap: hipótesis/debate, no consenso clínico.

### 4.3 Revocado / corregido

- “Ketotifen mejora FM”: revocado; el trial auditado fue negativo.
- “Cromoglicato/omalizumab son opciones terapéuticas FM”: revocado como afirmación fuerte. Son mecanismos plausibles por mastocitos/IgE, pero sin evidencia clínica directa suficiente en FM.

---

## 5. ESM2 auditado

Archivo auditado: `target_embeddings.json`.

Confirmado:
- 11 targets
- embedding dimension: 1280
- modelo declarado: ESM2 650M
- MOR tiene similitud media contra otros targets de 0.677, rango 0.608–0.750
- los demás pares no-MOR tienen media 0.937, rango 0.852–0.966

**Claim validado:** MOR es un outlier global en los embeddings mean-pooled.

**Claim con cautela:** esto no demuestra que LDN sea eficaz ni que MOR sea “mejor target”; solo dice que MOR tiene una huella global distinta. Es una señal estructural/representacional, no clínica.

**Claim prohibido:** usar mean pooling ESM2 para hablar de pockets, docking o afinidad. Para eso se necesitan per-residue embeddings, estructura válida y docking/ensayos.

---

## 6. Targets y priorización: checkpoint limpio

### 6.1 Targets con mejor base para seguir

**LDN/MOR:** buena justificación para seguir explorando porque MOR está estructuralmente bien caracterizado, naltrexona existe, y la literatura de LDN en FM es una línea real. No venderlo como cura; tratarlo como candidato de repurposing/modulación neuroinmune.

**IL-6/tocilizumab:** biológicamente plausible por inflamación/mastocitos y porque tenemos dataset GSE229750, pero el dataset no prueba eficacia clínica. Útil como vía a estudiar, no como conclusión.

**NRF2/DMF:** plausible por estrés oxidativo y fármaco aprobado, pero requiere separar “NRF2 como vía alterada” de “DMF funcionaría en FM”. La segunda es hipótesis de repurposing.

**Mastocitos/basófilos (CPA3/MS4A2/FCER1A/HDC):** señal transcriptómica real en GSE67311. Buena ruta mecanística. No convertir en “MCAS confirmado”.

### 6.2 Targets que quedan más débiles

**Nav1.8/suzetrigine:** gran target de dolor periférico y druggability alta, pero conexión FM directa todavía debe documentarse mejor. Es fuerte como dolor/nociceptor, no necesariamente como target específico FM.

**TRPA1:** similar a Nav1.8; buena biología de dolor/SFN, pero evidencia FM específica necesita más grounding.

**DYRK3/RGS17/ARHGEF37:** biomarcadores del paper de Zhao, pero aún no dianas terapéuticas sólidas. No priorizar diseño farmacológico sin más evidencia.

---

## 7. Documentos supersedidos o a corregir

Los siguientes documentos siguen siendo útiles como historial, pero no deben usarse como fuente canónica sin mirar este checkpoint:

- `analisis/RESULTADOS_PDB.md`: contiene asignaciones PDB incorrectas; supersedido por sección 2.2 de este checkpoint.
- `literatura/REFERENCIAS.md`: el estado “PDF descargado” está inflado; supersedido por sección 2.1.
- `analisis/GROUNDING_MASTOCITOS_FM.md`: versión vieja; usar `analisis/GROUNDING_MASTOCITOS_CORREGIDO.md` + este checkpoint.
- Cualquier resumen que diga “22 estructuras PDB validadas por target”: corregir a “18 PDB experimentales útiles + 2 PDB corregidos añadidos + 2 AlphaFold predichos; 4 PDBs viejos rechazados”.

---

## 8. Próximo paso recomendado desde base limpia

Antes de hacer más análisis sofisticado, recomiendo dos acciones de higiene:

1. Reescribir `RESULTADOS_PDB.md` como `RESULTADOS_PDB_CORREGIDO.md`, usando solo estructuras verificadas y separando claramente PDB experimental vs AlphaFold.
2. Reescribir `REFERENCIAS.md` o crear `REFERENCIAS_AUDITADAS.md`, con tres estados: `PDF real local`, `HTML/full text local`, `identificador verificado sin full text local`.

Después de eso, la ruta científica más sólida es profundizar en la señal mastocito/basófilo con literatura y datasets específicos, o estudiar MOR/LDN como ruta de repurposing mejor anclada.

---

## 9. Analogía corta del checkpoint

Hasta ahora teníamos un mapa de ciudad útil, pero algunos edificios estaban con etiquetas equivocadas. La señal de mastocitos/basófilos en sangre es un barrio real; MOR como edificio raro también es real; GSE229750 como estación de neutrófilos también es real. Lo que estaba mal eran algunas placas en las puertas: cuatro PDBs decían “CPA3/HDC/MS4A2/NRF2” pero al abrir la puerta eran DNA, integrasa HIV o proteínas no relacionadas. Ya esas placas falsas quedaron en cuarentena.

Este checkpoint es la foto limpia del tablero: desde aquí se puede avanzar, pero sin usar las placas falsas.
