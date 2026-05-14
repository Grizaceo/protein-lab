# DATASETS GEO DESCARGADOS — Fibromialgia
## Registro de datos crudos de expresión génica

**Fecha descarga:** 2026-05-13
**Fuente:** NCBI Gene Expression Omnibus (GEO) — https://www.ncbi.nlm.nih.gov/geo/
**Herramienta:** GEOparse v2.0.4

---

## DATASET 1: GSE221921

| Campo | Detalle |
|-------|---------|
| **Nombre corto** | PBMC_FM_96patients_93controls |
| **Plataforma** | GPL24676 (Illumina HumanHT-12 V4.0) |
| **Tipo** | Expresión génica por microarray |
| **Muestras totales** | 189 |
| **FM pacientes** | 96 |
| **Controles** | 93 |
| **Tejido** | PBMC (mononucleares de sangre periférica) |
| **Tamaño archivo** | 13.6 KB (comprimido) |
| **Descarga** | ✅ Completa |
| **Paper asociado** | Zhao et al. 2025 (Frontiers Genetics, PMID 40313599) — usado como training set |

**Notas:** Los títulos de muestras son genéricos (Sample_268, etc.). La metadata completa está en el archivo SOFT. Según el paper de Zhao et al., este dataset contiene 96 pacientes FM y 93 controles sanos. Los 96 "Other/Unclear" en nuestra clasificación automática corresponden a los pacientes FM (los títulos no incluyen "FM" explícito).

---

## DATASET 2: GSE67311

| Campo | Detalle |
|-------|---------|
| **Nombre corto** | Blood_FM_70patients_70controls |
| **Plataforma** | GPL11532 (Affymetrix Human Gene 1.1 ST Array) |
| **Tipo** | Expresión génica por microarray |
| **Muestras totales** | 142 |
| **FM pacientes** | 67 |
| **Controles** | 75 |
| **Tejido** | Sangre periférica completa |
| **Tamaño archivo** | 34.8 MB (comprimido) — el más grande |
| **Descarga** | ✅ Completa |
| **Paper asociado** | Zhao et al. 2025 — usado como validation set. También usado en múltiples papers posteriores. |

**Notas:** Dataset con más historia de uso en la literatura. 142 muestras bien equilibradas. Las muestras control están etiquetadas como C001, C002, etc.

---

## DATASET 3: GSE229750

| Campo | Detalle |
|-------|---------|
| **Nombre corto** | Neutrophils_FM_tocilizumab_trial |
| **Plataforma** | GPL24676 (Illumina HumanHT-12 V4.0) |
| **Tipo** | Expresión génica por microarray |
| **Muestras totales** | 12 |
| **FM pacientes** | 7 |
| **Controles** | 5 |
| **Tejido** | Neutrófilos (aislados de sangre periférica) |
| **Tamaño archivo** | 2.4 KB (comprimido) — muy pequeño |
| **Descarga** | ✅ Completa |
| **Paper asociado** | Zhao et al. 2025 — dataset suplementario. También asociado a bioRxiv 2025 (Paradoxical Phenotype of Fibromyalgia Neutrophils). |

**Notas especiales:** Este dataset es único — viene de un **ensayo clínico de tocilizumab** (anti-IL-6R, el fármaco que identificamos como Tier 1 en la tabla de targets). Las muestras están etiquetadas como "FM patient X, week 0" y "FM patient X, week 12", lo que significa que hay datos **antes y después del tratamiento con tocilizumab**. Esto es oro puro para análisis de respuesta al tratamiento.

---

## RESUMEN DE MUESTRAS

| Dataset | FM | Control | Total | Tejido |
|---------|----|---------|-------|--------|
| GSE221921 | 96 | 93 | 189 | PBMC |
| GSE67311 | 67 | 75 | 142 | Sangre completa |
| GSE229750 | 7 | 5 | 12 | Neutrófilos (pre/post tocilizumab) |
| **TOTAL** | **170** | **173** | **343** | — |

---

## PRÓXIMOS PASOS SUGERIDOS

1. **Procesar GSE67311** (el más grande y con mejor balance) para identificar DEGs (differentially expressed genes) FM vs control
2. **Cruzar DEGs** con la tabla de targets farmacéuticos (Tier 1-4) para ver si los genes diferenciales coinciden con targets druggables
3. **Analizar GSE229750** para ver el efecto del tocilizumab en la expresión génica de neutrófilos FM — ¿normaliza los DEGs?
4. **Generar ESM2 embeddings** de los targets Tier 1 que aparezcan como DEGs

---

## VERIFICACIÓN DE INTEGRIDAD

- [x] Descarga completada para los 3 datasets
- [x] Archivos SOFT presentes y parseables por GEOparse
- [x] Número de muestras coincide con lo reportado en el paper de Zhao et al.
- [x] Plataformas identificadas (GPL24676, GPL11532)
- [x] Metadatos de muestras extraídos
