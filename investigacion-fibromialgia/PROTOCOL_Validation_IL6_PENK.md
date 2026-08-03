# Protocolo Experimental: Validación de biomarcadores IL-6 + Substance P en plasma FM

## Objetivo
Validar los 2 proxies periféricos identificados en el análisis in-silico (IL6 + PENK) como biomarcadores de dolor en fibromialgia mediante análisis computacional usando datasets públicos + modelo de clasificación.

## Diseño experimental in-silico

### Datasets
- **GSE221921**: 96 FM vs 93 HC (PBMCs, RNA-seq FPKM) — *ya analizado*
- **GSE67311**: 70 FM vs 70 HC (whole blood, Affymetrix) — *cross-validation*
- **PXD008076**: Khoonsari 2019 (CSF proteome, 4 discriminadoras) — *referencia CSF*

### Biomarcadores objetivo
1. **IL6** — validated proxy (HIGH grade, significant en GSE221921 y cross-validated en GSE67311)
2. **TAC1 / Substance P** — validated proxy (HIGH grade tras corrección 2026-08-03: FC=2.10, p=0.0002 en GSE221921; antes anotado PENK)
3. **PENK** — hallazgo opioide endógeno separado (MEDIUM, FC=1.38, p=0.0031) — NO es Substance P

### Plataforma
- **Colab Pro+ T4 GPU**: procesamiento de datos transcriptómicos + análisis de clasificación
- **Alternativa Kaggle**: CPU compute para análisis estadístico
- **Modal**: para correr el modelo de clasificación (Olink-style) a escala

## Pipeline de validación

### Fase 1: Preprocesamiento (Colab)
1. Descargar GSE221921 + GSE67311 processed data
2. Normalizar expresión (log2 transform + quantile normalization)
3. Extraer valores para IL6 y PENK en todos los samples
4. Clasificar FM vs HC usando logistic regression (sklearn)

### Fase 2: Análisis de clasificación (Colab/Modal)
1. Entrenar modelo: [IL6, PENK] → FM/HC classification
2. Cross-validation 5-fold
3. Métricas: sensitivity, specificity, AUC
4. Comparar con paper original (Wray 2009: sens 95%, spec 96%)

### Fase 3: Validación cross-dataset
1. Validar modelo entrenado en GSE221921 sobre GSE67311
2. Ajustar thresholds
3. Reporte de generalización

## Métricas esperadas
- AUC ≥ 0.75 (baseline paper: 0.95 sens/0.96 spec)
- Sensitivity ≥ 0.80
- Specificity ≥ 0.80

## Entregables
1. Notebook Colab con pipeline completo
2. Script Python reproducible (`validate_fm_biomarkers.py`)
3. Reporte de métricas (`validation_report.md`)
4. Tabla final con proxy grades actualizados
