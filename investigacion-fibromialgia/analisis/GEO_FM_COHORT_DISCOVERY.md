# DESCUBRIMIENTO DE COHORTES GEO — FIBROMIALGIA (2026)

## 1. Metodología de Búsqueda
Se ejecutó un minado de datos en NCBI GEO (Gene Expression Omnibus) para identificar cohortes independientes de pacientes con Fibromialgia (FM) con perfiles transcriptómicos en sangre periférica (PBMCs o sangre total) para evaluar la replicación de la sobreexpresión de *DRD2* y *MDGA2*.

### Criterios de Exclusión
- **GSE221921:** Cohorte primaria ya analizada (96 FM / 93 HC, PBMCs).
- **GSE67311:** Cohorte secundaria ya analizada (70 FM / 70 HC, Sangre total).
- Datasets no humanos o no transcriptómicos (solo metilación / SNP array).

---

## 2. Matriz de Cohortes Identificadas en GEO

| GEO Accession | Título / Descripción | Tipo de Muestra | Plataforma | Tamaño Muestral | Presencia de Dianas | Publicación | Relevancia |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GSE269047** | HERV activation in ME/CFS and FM | PBMCs | Microarray alta densidad | Mujeres FM vs HC | Cobertura total (*DRD2*, *MDGA2*) | 2025/2026 | ⭐ **MÁXIMA (Prioridad 1)** |
| **GSE229750** | Effect of tocilizumab on FM neutrophils | Neutrófilos | Microarray Illumina | 5 FM vs 5 HC (Baseline) | Cobertura total (*DRD2*, *MDGA2*) | BioRxiv / GEO | 🟡 **MEDIA (Prioridad 2)** |
| **GSE221921** | FM PBMC transcriptomics | PBMCs | RNA-seq / FPKM | 96 FM vs 93 HC | Analizado | Sci Rep 2024 | Excluido (Cohorte Primaria) |
| **GSE67311** | Whole blood expression in FM | Sangre Total | Affymetrix Array | 70 FM vs 70 HC | Analizado | Jones 2016 | Excluido (Cohorte Secundaria) |

---

## 3. Cohorte Seleccionada para Replicación: GSE269047
- **Tejido:** PBMCs (coincidencia 100% estricta con GSE221921).
- **Población:** Mujeres con Fibromialgia vs Controles Sanos (elimina la multicolinealidad por sexo).
- **Acción:** Proceder a descargar la matriz procesada e interrogar las sondas de *DRD2*, *MDGA2*, *CAMKV* y *CELF4*.
