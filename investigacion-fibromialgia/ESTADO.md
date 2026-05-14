# ESTADO DEL PROYECTO — Fibromialgia (Actualizado)

**Fecha:** 2026-05-13
**Fase actual:** Fase 0 completada + Fase 1 iniciada

---

## Resumen de lo completado

### Fase 0: Recopilación ✅ COMPLETADA
- 19 papers verificados con DOI/PMID/PMC
- 8 PDFs descargados
- 16 targets farmacéuticos identificados y clasificados en 4 tiers
- 3 datasets GEO descargados:
  - GSE67311: Microarray, sangre completa, 142 muestras (67 FM + 75 Ctrl) ✅ Procesado
  - GSE221921: RNA-seq, PBMC, 189 muestras (96 FM + 93 Ctrl) ⚠️ Datos crudos en SRA
  - GSE229750: Microarray, neutrófilos, 12 muestras (pre/post tocilizumab) ✅ Descargado

### Fase 1: Análisis in silico 🔄 EN PROGRESO
- Análisis de expresión diferencial completado para GSE67311
- 4 genes significativos identificados (todos DOWN en FM)
- Cruce con targets farmacéuticos realizado

---

## Hallazgos clave del análisis de datos

### GSE67311 — Genes diferencialmente expresados en sangre FM

**4 genes significativos (p_adj < 0.05, |log2FC| > 0.5):**

| Gene | log2FC | p_adj | Dirección | Función |
|------|--------|-------|-----------|---------|
| **CPA3** | -0.786 | 3.46e-03 | DOWN | Carboxypeptidase A3 (mastocito) |
| **MS4A2** | -0.516 | 1.92e-02 | DOWN | Receptor IgE (FcεRIβ) |
| **FCER1A** | -0.501 | 2.46e-02 | DOWN | Receptor IgE (FcεRIα) |
| **HDC** | -0.528 | 4.79e-02 | DOWN | Histidina descarboxilasa |

**Conclusión: Señal de mastocitos DOWNregulated en FM.**

Esto es un hallazgo nuevo que no estaba en nuestra tabla de targets. Los mastocitos son células inmunes que liberan histamina y otros mediadores inflamatorios. Que estén downregulated en sangre periférica podría indicar:
- Menos mastocitos en sangre (migración a tejidos)
- Mastocitos menos activos
- Cambio en composición celular de la sangre

### Cruce con targets farmacéuticos

Ningún target Tier 1-2 (NRF2, Nav1.8, IL-1, IL-6, TLR4, TRPA1) apareció como DEG en sangre periférica. Esto sugiere que las alteraciones están en otros tejidos (DRG, cerebro, intestino) o son post-traduccionales.

### RGS17 — Conexión parcial

RGS17 (biomarcador de Zhao et al.) apareció en el top 50 con tendencia UP (log2FC=+0.138, p=1.86e-04) pero sin alcanzar FDR<5%.

---

## Datasets pendientes de procesar

### GSE229750 — Neutrófilos + Tocilizumab
- 12 muestras: 7 FM + 5 controles, con datos pre/post tratamiento con tocilizumab
- **Valor único:** Permite ver si la tocilizumab normaliza los genes alterados en FM
- Pendiente: Análisis de expresión diferencial + efecto del tratamiento

### GSE221921 — PBMC RNA-seq
- Datos crudos en SRA, no en formato procesable directamente
- Opción: Buscar la tabla de conteos en el paper de Zhao et al. o en la web del estudio

---

## Próximos pasos inmediatos

1. **Procesar GSE229750** (neutrófilos + tocilizumab) — dataset pequeño, rápido de analizar
2. **Análisis de vías** — ¿qué pathways están alterados según los DEGs?
3. **Mastocitos como nuevo target** — investigar fármacos estabilizadores de mastocitos (cromoglicato, ketotifen, anti-IgE)
4. **ESM2 embeddings** — para los targets Tier 1 que no aparecieron como DEGs
