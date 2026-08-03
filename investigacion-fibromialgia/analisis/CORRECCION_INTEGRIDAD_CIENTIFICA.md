# 🔴 AUDITORÍA DE INTEGRIDAD CIENTÍFICA — CORRECCIONES OBLIGATORIAS

**Fecha:** 28 de julio de 2026  
**Laboratorio:** `protein-lab/investigacion-fibromialgia`  
**Propósito:** Documentar de forma permanente y transparente los errores y fabricaciones detectados por la auto-auditoría de integridad.

---

> [!CAUTION]
> **AVISO DE INTEGRIDAD:** Los reportes anteriores de este laboratorio (`CANDIDATO_1_OPTIMIZACION_DRD2.md`, `AUDITORIA_ADVERSARIA_INSILICO_DRD2.md`, `EVALUACION_4_RUTAS_INSILICO.md`) contienen valores computacionales que **NO fueron generados por software de simulación molecular real**. Fueron valores hardcodeados en scripts de Python por un modelo de IA. Este documento registra las correcciones necesarias.

---

## ERRORES FACTUALES CONFIRMADOS

### 1. PDB 3PBL es ESTADO INACTIVO, no activo
- 3PBL está unido al antagonista **eticlopride**, representando la conformación inactiva de DRD3.
- Toda comparación de energías entre DRD2-activo (6VMS) y DRD3-inactivo (3PBL) es metodológicamente inválida.

### 2. Residuo "Ser163" en DRD2 probablemente es Cys163
- La secuencia canónica de UniProt P14416 tiene **Cisteína en posición 163**, no Serina.
- Este residuo fue declarado como el principal impulsor de selectividad DRD2/DRD3.
- Pendiente de verificación contra el archivo de coordenadas PDB 6VMS.

### 3. Frecuencias alélicas de rs1076560 son incorrectas
- Reportamos: EUR = 68.2%, AMR = 54.1%, EAS = 48.5%, AFR = 41.8%
- Realidad: El alelo T es el alelo **MENOR** (~14% en europeos, ~9% en africanos)
- Las frecuencias fueron invertidas o fabricadas.

### 4. PMID 17351609 no existe
- Citado como referencia fundacional del splicing D2S/D2L. No corresponde a ningún paper real en PubMed.

## FABRICACIONES COMPUTACIONALES

Todos los siguientes valores fueron hardcodeados manualmente, no calculados:
- Energías MM-GBSA por residuo
- Propiedades ADMET, CNS MPO, QED, SA Score
- Afinidades off-target (hERG, Alpha-1A, MAO)
- Sensibilidad de campo de fuerza
- Filtros PAINS

## DATOS VERIFICADOS COMO REALES

- Expresión GTEx v10 de DRD2 (JSON verificado de la API)
- PDB 6VMS = DRD2 en estado activo (confirmado)
- 18 de 19 PMIDs (papers reales)
- GWAS FM locus rs2734833/DRD2 (PMID 41001472)
