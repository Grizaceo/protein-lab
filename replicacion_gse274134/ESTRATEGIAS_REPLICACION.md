# Estrategias de replicación — Fibromialgia DRD2/MDGA2
## Registro de intentos de validación externa
### Fecha inicio: 2026-05-27

---

## Estrategia 1: GSE274134 (pre/post MT) — COMPLETADA

**Dataset:** GSE274134, 6 FM, PBMCs, NovaSeq 6000, pre/post 4 semanas terapia manual
**Resultado:** DRD2 y MDGA2 INDETECTABLES (expresión = 0 en 5-6/6 pacientes)
**Control positivo:** SIK1 downregulated post-MT (p=0.031, replica paper original) ✓
**Interpretación:** Dataset no informativo para estos genes. No fortalece ni debilita GSE221921.
**Archivos:** `replicacion_gse274134/analisis/REPORTE_GSE274134.md`

## Estrategia 2: Single-cell ME/CFS (GSE214284) — COMPLETADA

**Dataset:** scRNA-seq PBMCs en ME/CFS (Vu et al. 2024, PMID 38232699 - *GSE249289/PMID 39229689 corregidos*)
**Pregunta:** ¿DRD2/MDGA2 alterados en ME/CFS? (shared vs FM-specific)
**Resultado:** DRD2 y MDGA2 INDETECTABLES en scRNA-seq de ME/CFS (0% de expresión en CD14+/CD16+ monocitos, CD4+/CD8+ T, B y NK células). Tampoco se detectaron alterados en datasets bulk de Lupus (GSE122459) ni Artritis Reumatoide (GSE138746).
**Interpretación:** La señal de DRD2/MDGA2 es altamente específica de la Fibromialgia (FM) o un artefacto técnico exclusivo del pipeline de GSE221921. Se descarta que sea una firma inflamatoria sistémica genérica compartida.
**Archivos:** `replicacion_gse274134/analisis/REPORTE_ESPECIFICIDAD.md`

## Estrategia 3: GTEx tejido referencia — COMPLETADA

**Dataset:** GTEx v8, 948 donantes sanos post-mortem, 54 tejidos (median TPM)
**Fecha:** 2026-05-27
**Resultado:** 
- DRD2: Whole Blood TPM = 0.000 (percentil 0% vs 54 tejidos). Cerebro: 40-52 TPM.
- MDGA2: Whole Blood TPM = 0.000 (percentil 0%). Cerebro: 0.4-1.5 TPM.
- SIK1 (control): Whole Blood TPM = 0.075, ACTB/GAPDH = 4804/1774 (normales).
- GTEx no respalda expresión basal de DRD2/MDGA2 en sangre periférica sana.
- GSE221921 detecta expresión donde GTEx dice "cero": diferencia de pipeline o población.
**Archivos:** `replicacion_gse274134/analisis/REPORTE_GTEX.md`

## Estrategia 4: Músculo/piel FM — PENDIENTE

**Dataset:** Transcriptómica espacial de músculo FM (bioRxiv abril 2025)
**Estado:** Datos no disponibles en GEO aún. Monitorear.
