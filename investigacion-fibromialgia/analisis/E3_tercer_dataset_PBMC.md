# E3 — Replicación del eje opioide en un tercer dataset PBMC

**Fecha:** 2026-08-04

## Objetivo

Buscar un tercer dataset PBMC de fibromyalgia en GEO para replicar los hallazgos del eje opioide (OPRM1, OPRK1, TACR1, TAC1, PENK).

## Búsqueda en GEO (2026-08-04)

Queries: "fibromyalgia PBMC expression", "fibromyalgia blood RNA-seq", "fibromyalgia monocyte expression", "fibromyalgia peripheral blood"

Total de datasets de fibromyalgia en GEO: 18 GSE

### Datasets de transcriptómica FM relevantes

| GSE | n | Plataforma | Tejido | ¿Servible como réplica PBMC? |
|-----|---|------------|--------|------------------------------|
| **GSE221921** | 189 | 24676 | PBMC RNA-seq | No — ya usado como discovery |
| **GSE67311** | 166 | Affymetrix | Whole blood | No — ya usado como réplica fracasada (no confirma) |
| GSE334369 | 206 | 24676 | Neutrófilos | No — neutrófilos purificados, no PBMC |
| GSE229750 | 12 | 24676 | Neutrófilos | No — neutrófilos post-tocilizumab, n=12 |
| GSE269047 | 43 | 22462 | PBMC (HERV) | No — eliminado en R10 (transcripts HERV) |
| GSE274134 | 12 | 24676 | Músculo? | No — manual therapy, no PBMC |
| GSE303093 | 48 | 19057 | small RNA | No — miRNA/tRF, no mRNA |
| GSE156184 | 9 | 11154 | Células senescentes | No — no FM |

## Resultado

**No existe un tercer dataset PBMC de FM públicamente disponible en GEO a la fecha (2026-08-04).**

Los dos únicos datasets de sangre periférica FM con transcriptómica de mRNA genónico son:
1. GSE221921 (PBMC RNA-seq, discovery) — ya usado
2. GSE67311 (whole blood microarray, réplica) — ya usado (no replica)

GSE334369 (neutrófilos FM, n=206) es el dataset más nuevo y grande pero está enncedido neutrófilos purificados, no PBMC. No es una réplica del eje opioide en PBMC.

## Conclusión

La replicación en un tercer dataset PBMC no es posible con los datos públicos disponibles actualmente.

**Estado:** No realizable — el dataset no existe.

## Implicación para el preprint

Se debe añadir a las limitaciones:
> "No existe un tercer dataset PBMC de FM públicamente disponible en GEO (2026-08-04). La replicación del eje opioide en un tercer cohort PBMC requiere acceso a datos no públicos o un nuevo estudio."

Esto se añadirá al preprint en la próxima revisión.

## Datos suplementarios

Búsqueda realizada mediante NCBI E-utilities (esearch + esummary en db=gds con filtros por tipo de muestra: PBMC, blood, monocyte, leukocyte, peripheral blood).
