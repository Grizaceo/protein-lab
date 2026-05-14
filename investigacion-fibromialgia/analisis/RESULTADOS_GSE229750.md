# EXPERIMENTO 1: GSE229750 — Neutrófilos FM pre/post Tocilizumab
## Documentación de resultados

**Fecha:** 2026-05-13
**Dataset:** GSE229750 (RNA-seq, neutrófilos aislados de sangre periférica)
**Fuente:** NCBI GEO, archivos suplementarios: GSE229750_FM_HC.xlsx + GSE229750_FM_TCZ.xlsx
**Tamaño:** 60,623 genes, estadísticas pre-calculadas por los autores

---

## DISEÑO EXPERIMENTAL

### FM vs Healthy Controls (FM_HC)
- 5 pacientes FM (FM_1, FM_2, FM_4, FM_5, FM_7) — neutrófilos aislados
- 5 controles sanos (MHC_67, MHC_70, MHC_71, MHC_72, MHC_73)
- Datos: counts + TPM + log2FC pre-calculado (columna `log2FC_AB_C`)
- N total con padj válido: 27,924 genes

### Tocilizumab pre vs post (FM_TCZ)
- Comparación 1: FM_3 (post, week 12) vs FM_1 (pre, week 0)
- Comparación 2: FM_6 (post, week 12) vs FM_4 (pre, week 0)
- **2 pares pre/post nada más** — n muy pequeño
- Datos: counts + TPM + log2FC pre-calculado por paciente

---

## RESULTADO 1: FM vs Controles — SEÑAL MUY DÉBIL

Solo 3 genes significativos (padj < 0.05, |log2FC| > 0.5):

| Gene | log2FC | padj | Dirección | Función |
|------|--------|------|-----------|---------|
| TSPAN13 | -2.478 | 6.0e-08 | DOWN FM | Tetraspanina 13 |
| C3AR1 | +1.938 | 1.03e-04 | UP FM | Receptor de complemento C3a |
| PI3 | +0.986 | 9.53e-04 | UP FM | Elafina (inhibidor de proteasa) |

**Interpretación:** Los neutrófilos de pacientes FM muestran muy poca alteración transcripcional respecto a controles. Esto contrasta fuertemente con GSE67311 donde encontramos cientos de genes alterados. Posible razón: los neutrófilos no son el tipo celular más afectado en FM (los mastocitos/basófilos probablemente sí, pero son una fracción mínima en sangre).

---

## RESULTADO 2: Tosilizumab — EFECTO MASIVO (¿artefacto?)

2605 genes con padj < 0.05 y |log2FC| > 0.5 en el promedio de ambas comparaciones.

**Top genes que BAJAN con tocilizumab (podrían normalizar genes UP en FM):**
LY6E, RSAD2, EGR3, OAS3, OAS2, CMPK2, HBA2, IFI6, ISG15, IFI44L...

Muchos son **genes de respuesta a interferón (ISGs)** — esto sugiere que tocilizumab está suprimiendo una firma de IFN en neutrófilos FM.

**Top genes que SUBEN con tocilizumab:**
ARG1, etc. (menos numerosos que los que bajan)

**ADVERTENCIA METODOLÓGICA:** Con solo n=2 pares pre/post, la estadística es frágil. Un outlier en un paciente puede generar un p-value "significativo" artificialmente. Los resultados deben interpretarse con cautela.

---

## RESULTADO 3: CRUCE CON GENES DE MASTOCITOS

### CPA3
- FM vs CTRL: log2FC ≈ -0.001, padj ≈ 0.988 — **NO alterado en neutrófilos FM**
- Pre vs Post tocilizumab: NA en ambas comparaciones (expresión muy baja en neutrófilos)
- **Interpretación:** CPA3 es específico de mastocitos, no se expresa en neutrófilos

### MS4A2
- FM vs CTRL: log2FC ≈ -0.002, padj ≈ 0.988 — **NO alterado en neutrófilos FM**
- FM_6_vs_FM_4: log2FC = **+3.19**, padj = **0.021** — SUBE con tocilizumab *** SIG ***
- **Interpretación:** El tocilizumab aumenta MS4A2 en neutrófilos de FM. Pero como MS4A2 no estaba alterado en neutrófilos FM (vs CTRL), no sabemos si esto es "normalizar" o un efecto colateral

### FCER1A
- FM vs CTRL: log2FC ≈ -0.001, padj ≈ 0.988 — **NO alterado en neutrófilos FM**
- FM_6_vs_FM_4: log2FC = **+3.48**, padj = **9.78e-13** — SUBE con tocilizumab *** SIG ***
- **Interpretación:** Igual que MS4A2 — tocilizumab aumenta drásticamente FCER1A en neutrófilos FM. Pero no sabemos si es normalización o efecto indirecto

### HDC
- FM vs CTRL: log2FC ≈ -0.0005, padj ≈ 0.988 — **NO alterado en neutrófilos FM**
- FM_6_vs_FM_4: log2FC = **+3.14**, padj = **1.51e-09** — SUBE con tocilizumab *** SIG ***
- **Interpretación:** Mismo patrón que FCER1A y MS4A2

**OBSERVACIÓN CRÍTICA:** Los 3 genes (MS4A2, FCER1A, HDC) que estaban DOWN en sangre completa (GSE67311) NO están alterados en neutrófilos aislados (GSE229750). Esto es consistente: estos genes se expresan en mastocitos/basófilos, no en neutrófilos. Su señal DOWN en GSE67311 viene de mastocitos/basófilos (que son una fracción pequeña de las PBMCs/sangre), no de neutrófilos.

El hecho de que tocilizumab aumente estos genes en neutrófilos es interesante pero **no prueba que esté normalizando la señal de mastocitos** — los neutrófilos normalmente no expresan estos genes en niveles altos.

---

## RESULTADO 4: CRUCE CON TARGETS TIER 1

| Target | Gen | FM vs CTRL (neutrófilos) | Interpretación |
|--------|-----|--------------------------|----------------|
| NRF2 | NFE2L2 | log2FC=+0.002, padj=0.993 | NO alterado |
| Nav1.8 | SCN10A | NA (sin datos) | No expresado en neutrófilos |
| IL-1β | IL1B | log2FC=+0.015, padj=0.988 | NO alterado |
| IL-6 | IL6 | log2FC≈0, padj=0.988 | NO alterado |

**Los targets Tier 1 no están alterados a nivel de mRNA en neutrófilos FM.** Esto no sorprende: NRF2 es un factor de transcripción regulado post-traduccionalmente, Nav1.8 es específico de neuronas, y IL-1β/IL-6 se regulan principalmente a nivel de secreción, no de transcripción.

---

## VEREDICTO DEL EXPERIMENTO

### Lo que aprendimos:
1. Los neutrófilos FM muestran muy poca alteración transcripcional (solo 3 genes significativos)
2. La señal de mastocitos (CPA3/MS4A2/FCER1A/HDC) que vimos en GSE67311 NO se replica en neutrófilos — porque son tipos celulares diferentes
3. El tocilizumab tiene un efecto masivo en el transcriptoma de neutrófilos FM (2605 genes), principalmente suprimiendo genes de respuesta a interferón
4. FCER1A, MS4A2 y HDC suben con tocilizumab en neutrófilos, pero como no estaban alterados en neutrófilos FM, no podemos interpretarlo como "normalización"

### Lo que NO aprendimos:
- No podemos validar la hipótesis de mastocitos con este dataset (no es el tipo celular correcto)
- Los efectos del tocilizumab en neutrófilos son interesantes pero el n=2 es muy pequeño

### Próximo paso lógico:
Buscar datasets de **single-cell RNA-seq** o **sorted mast cells/basophils** en FM, que permitan ver la señal de mastocitos directamente, sin la dilución de otros tipos celulares.

---

## ARCHIVOS GENERADOS
- `GSE229750_FM_HC.xlsx` — datos crudos FM vs controles (10.7 MB)
- `GSE229750_FM_TCZ.xlsx` — datos crudos pre/post tocilizumab (5.2 MB)
- `GSE229750_DEGs_FM_vs_CTRL_significant.csv` — 3 genes significativos
- `GSE229750_DEGs_PRE_vs_POST_significant.csv` — 2605 genes alterados por tocilizumab
- `GSE229750_samples_metadata.csv` — metadata de muestras
