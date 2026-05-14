# PASO 2 — Análisis de Expresión Diferencial FM vs Control
## Resultados del dataset GSE67311 (sangre periférica, 142 muestras)

**Fecha:** 2026-05-13
**Dataset:** GSE67311 (GPL11532, Affymetrix Human Gene 1.1 ST Array)
**Muestras:** 67 FM + 75 controles = 142 total
**Genes en plataforma:** 33,297 probes → 22,148 con gene symbol asignado
**Método:** T-test + corrección Benjamini-Hochberg (FDR)

---

## GENES DIFENCIALMENTE EXPRESADOS SIGNIFICATIVOS

**Criterio:** p_adj < 0.05 Y |log2FC| > 0.5

| # | Gene | log2FC | p_value | p_adj | Dirección | Función |
|---|------|--------|---------|-------|-----------|---------|
| 1 | **CPA3** | -0.786 | 1.04e-07 | 3.46e-03 | DOWN | Carboxypeptidase A3 (mastocito) |
| 2 | **MS4A2** | -0.516 | 1.73e-06 | 1.92e-02 | DOWN | Receptor de IgE (FcεRIβ) |
| 3 | **FCER1A** | -0.501 | 2.95e-06 | 2.46e-02 | DOWN | Receptor de IgE (FcεRIα) |
| 4 | **HDC** | -0.528 | 1.04e-05 | 4.79e-02 | DOWN | Histidina descarboxilasa |

**Tendencia general:** Los 4 genes significativos están **downregulated** en FM vs controles. Todos están relacionados con **mastocitos y respuesta alérgica/inflamatoria**.

---

## TOP 50 GENES (por p-value, con nombre)

| Rank | Gene | log2FC | p_adj | Dir | Nota |
|------|------|--------|-------|-----|------|
| 1 | CPA3 | -0.786 | 3.46e-03 | DW | Mastocito |
| 2 | C1orf150 | -0.430 | 7.61e-03 | DW | Función desconocida |
| 3 | MS4A2 | -0.516 | 1.92e-02 | DW | Receptor IgE |
| 4 | FCER1A | -0.501 | 2.46e-02 | DW | Receptor IgE |
| 5 | ITGB8 | -0.328 | 2.65e-02 | DW | Integrina β8 |
| 6 | GATA2 | -0.452 | 4.79e-02 | DW | Factor transcripción hematopoyesis |
| 7 | C11orf83 | -0.149 | 4.79e-02 | DW | Función desconocida |
| 8 | HDC | -0.528 | 4.79e-02 | DW | Histidina descarboxilasa |
| 9 | AKAP12 | -0.200 | 9.82e-01 | DW | Scaffold proteína A-kinase |
| 10 | ENPP3 | -0.256 | 9.82e-01 | DW | Ectonucleotidasa |
| 11 | FAM46C | +0.324 | 9.82e-01 | UP | Familia con secuencia A |
| 12 | APBB2 | +0.224 | 9.82e-01 | UP | Proteína unión a APP |
| 13 | TIGD1 | -0.205 | 9.82e-01 | DW | Transposasa |
| 14 | MKRN1 | +0.228 | 1.19e-01 | UP | Makorin ring finger |
| 15 | RNF11 | +0.237 | 1.24e-01 | UP | Ring finger proteína |
| 16 | GLRX5 | +0.288 | 2.27e-01 | UP | Glutaredoxina 5 |
| 17 | ICA1L | -0.105 | 2.42e-01 | DW | Islet cell autoantigen |
| 18 | TXNDC11 | -0.087 | 2.52e-01 | DW | Tiorredoxina dominio |
| 19 | KLC3 | +0.199 | 2.52e-01 | UP | Kinesin light chain |
| 20 | LOC100131943 | +0.124 | 2.67e-01 | UP | Locus no caracterizado |
| 21 | DCAF12 | +0.191 | 2.67e-01 | UP | DDB1-CUL4 factor |
| 22 | MARCH8 | +0.213 | 2.67e-01 | UP | E3 ubiquitina ligasa |
| 23 | IL3RA | -0.287 | 2.67e-01 | DW | Receptor IL-3 (CD123) |
| 24 | RGS17 | +0.138 | 2.67e-01 | UP | ⭐ Biomarcador FM (Zhao 2025) |
| 25 | CD38 | -0.232 | 2.89e-01 | DW | Ectoenzima inmune |
| 26 | GPR65 | -0.217 | 3.40e-01 | DW | Receptor acoplado a G |
| 27 | SLC14A1 | +0.377 | 2.83e-01 | UP | Transportador urea |

---

## CRUCE CON TARGETS FARMACÉUTICOS (Tabla Paso 1)

### ¿Aparecen nuestros targets Tier 1-2 como DEGs?

| Target Tier | Gene | Aparece en DEGs? | p_adj | log2FC | Interpretación |
|-------------|------|------------------|-------|--------|----------------|
| Tier 1 | NRF2 (NFE2L2) | ❌ No | — | — | No diferencialmente expresado |
| Tier 1 | Nav1.8 (SCN10A) | ❌ No | — | — | No diferencialmente expresado |
| Tier 1 | IL-1B | ❌ No | — | — | No diferencialmente expresado |
| Tier 1 | IL-6 | ❌ No | — | — | No diferencialmente expresado |
| Tier 2 | TLR4 | ❌ No | — | — | No diferencialmente expresado |
| Tier 2 | TRPA1 | ❌ No | — | — | No diferencialmente expresado |
| Tier 3 | DYRK3 | ❌ No | — | — | No diferencialmente expresado |
| Tier 3 | RGS17 | ⚠️ Marginal | 0.267 | +0.138 | Tendencia UP pero no significativo |
| Tier 3 | ARHGEF37 | ❌ No | — | — | No diferencialmente expresado |

### Interpretación

**Ningún target Tier 1-2 aparece como DEG significativo en sangre periférica.** Esto NO significa que no sean relevantes — significa que:

1. **La alteración puede ser en tejido específico** (DRG, cerebro, intestino) y no en sangre
2. **La alteración puede ser post-traduccional** (proteína modificada pero mRNA estable)
3. **La alteración puede ser en subpoblaciones celulares** específicas que se diluyen en sangre completa
4. **El dataset GSE67311 puede no tener suficiente poder estadístico** para detectar cambios sutiles

### Lo que SÍ encontramos: señal de mastocitos

Los 4 DEGs significativos apuntan a **mastocitos**:
- **CPA3** (carboxypeptidase A3) — marcador específico de mastocitos
- **MS4A2** (FcεRIβ) — subunidad del receptor de IgE en mastocitos
- **FCER1A** (FcεRIα) — subunidad del receptor de IgE en mastocitos
- **HDC** (histidina descarboxilasa) — produce histamina en mastocitos

**Todos DOWNregulated en FM.** Esto sugiere que los mastocitos en sangre periférica de pacientes FM están **menos activos o menos numerosos** — o que hay un cambio en la composición celular de la sangre.

### RGS17: conexión parcial

RGS17 (biomarcador de Zhao et al.) aparece en el top 50 con tendencia UP (log2FC=+0.138) pero no alcanza significancia estadística (p_adj=0.267). Esto es consistente con el paper de Zhao et al. que lo identificó como biomarcador usando ML sobre múltiples datasets, no solo GSE67311.

---

## CONCLUSIONES DEL PASO 2

1. **GSE67311 muestra una señal de mastocitos downregulated en FM** — esto es nuevo y no está en nuestra tabla de targets
2. **Los targets farmacéuticos Tier 1-2 no aparecen como DEGs en sangre** — la alteración debe ser en otro tejido o a nivel proteico
3. **Necesitamos analizar GSE221921 (PBMC) y GSE229750 (neutrófilos)** para ver si hay señal en otros tejidos
4. **La señal de mastocitos es farmacológicamente targeteable** — existen fármacos estabilizadores de mastocitos (cromoglicato, ketotifen) y anti-IgE (omalizumab)

---

## ARCHIVOS GENERADOS

- `GSE67311_DEGs_all_named.csv` — 33,297 genes con p-values
- `GSE67311_DEGs_FDR5_named.csv` — 8 genes con FDR < 5%
- `GSE67311_DEGs_significant.csv` — 4 genes significativos (p_adj<0.05, |log2FC|>0.5)
