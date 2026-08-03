# Reporte de Replicación Independiente: Cohorte GEO GSE269047 (PBMCs en Mujeres con FM vs Controles Sanos)

**Fecha:** Mayo 2026  
**Laboratorio:** `protein-lab/investigacion-fibromialgia`  
**Script de Replicación:** [`scripts/analyze_gse269047_matrix.py`](file:///wsl.localhost/Ubuntu/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/scripts/analyze_gse269047_matrix.py)  
**Dataset Analizado:** GSE269047 (PBMCs, N=43 muestras: 18 FM/ME-CFS vs 25 Controles Sanos, Microarray de alta densidad)

---

## 1. Objetivo de Replicación

Poner a prueba las hipótesis previas derivadas de GSE67311 (sangre completa, 2016) evaluando si la firma de los marcadores del **Módulo Inmune** (`GATA2`, `CPA3`, `MS4A2`, `FCER1A`, `HDC`) o del **Módulo Neural** (`DRD2`, `MDGA2`, `COMT`) se sostienen o **se desvanecen** en una cohorte independiente moderna de PBMCs en mujeres (GSE269047).

---

## 2. Resultados Principales de la Replicación en Silico

### Tabla 1: Desempeño de Sondación y Replicación Estadísitica en GSE269047

| Gen Diana | Probe ID | FM Mean | HC Mean | $\log_2\text{FC}$ | Valor $p$ (Mann-Whitney) | ¿Replicado vs GSE67311? |
|---|---|---|---|---|---|---|
| **GATA2** | `GATA2-bgrd_st` | 8.4690 | 8.4627 | +0.0063 | **0.9795** | ❌ **NO REPLICADO** (Invariable) |
| **GATA2** | `GATA2-opti_st` | 4.4515 | 4.1939 | +0.2576 | **0.3961** | ❌ **NO REPLICADO** (Invariable) |
| **DRD2** | `DRD2-opti_at` | 1.8983 | 1.9162 | -0.0179 | **0.7773** | ❌ **NO REPLICADO** (Invariable) |
| **DRD2** | `DRD2-rand_st` | 2.1573 | 2.3360 | -0.1787 | **0.6620** | ❌ **NO REPLICADO** (Invariable) |
| **KIT** | `KIT-opti_st` | 1.4036 | 1.0552 | **+0.3485** | **0.0372** | ⚠️ Leve elevación marginal |
| **KITLG** | `KITLG-opti_st` | 0.4539 | 0.7628 | -0.3089 | **0.1052** | ❌ No significativo |

---

## 3. Conclusiones Científicas Sobrias

1. **Desvanecimiento de la Caída de *GATA2* en PBMCs:**
   - La drástica caída de *GATA2* ($\log_2\text{FC} = -0.45, q = 0.000031$) que observamos en sangre completa (GSE67311) **NO se sostiene en PBMCs de la cohorte independiente GSE269047** ($p = 0.979$).
   - Esto confirma empíricamente lo que identificó la auditoría: la señal granulocítica/basofílica dependía de la fracción granulocítica de la sangre completa (que se remueve en la preparación de PBMCs) o estaba artefactada por efectos de lote/tratamiento farmacológico en la cohorte antigua de 2016.

2. **Invariancia Total de *DRD2* a Nivel Transcripcional:**
   - *DRD2* no muestra diferencia estadística alguna entre mujeres con FM y controles sanos en PBMCs ($p > 0.65$). Esto respalda la decisión de **abandonar la medición de ARN de *DRD2* en sangre** como biomarcador y mantener el enfoque estrictamente en el análisis de sQTLs de ADN germinal en cerebro (Tangente 3).

---

## 4. Dictamen Final para el Manuscrito

> **Lección de Rigor:** Las firmas transcriptómicas en sangre periférica varían drásticamente según la fracción celular (sangre total vs PBMCs) y la plataforma tecnológica. **No se deben formular teorías de etiología autoinmune sistémica basándose únicamente en microarrays de sangre.**
