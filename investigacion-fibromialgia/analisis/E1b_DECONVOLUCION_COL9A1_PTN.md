# E1b — Ajuste por composición celular: COL9A1/PTN vs eje opioide (GSE221921)

**Fecha:** 2026-08-04
**Script:** `scripts/e1_deconvolution_adjusted_model.py` (ejecutable, ~50 s)
**Salidas:** `E1b_deconvolution_col9a1_ptn.csv`, `E1b_variant_sweep.csv`, `E1b_negative_control_random_genes.csv`
**Motivo:** E1 (commit `03b4609`) probó el ajuste composicional **solo sobre los 7 genes del eje opioide**. El módulo COL9A1–PTN, que la v2.7 del manuscrito declara objetivo primario de validación, nunca fue evaluado bajo ese modelo.

---

## 0. Hallazgo previo de integridad

El commit `03b4609` añadió **únicamente** `analisis/E1_deconvolution_opioid_axis.csv`. No existe en ningún commit del repositorio código que produzca las columnas `p_group_only`, `p_group_sex`, `p_full_adj`, `top_cell_type`. El resultado más adverso de toda la investigación era, hasta ahora, **no reproducible**.

Este script reconstruye la metodología y la valida contra ese CSV antes de extenderla.

---

## 1. Modelos

Sobre `log2(FPKM+1)`, n = 96 FM / 93 HC, 21 375 genes:

| | Modelo |
|---|---|
| M1 | `expr ~ grupo` |
| M2 | `expr ~ grupo + sexo` |
| M3 | `expr ~ grupo + sexo + fracciones celulares` → **`p_full_adj`** |

Fracciones: 12 tipos celulares. Dos estimadores contrastados — NNLS canónico del repositorio (`analisis/deconvolution/gse221921_cell_fractions.csv`) y marker-scores recalculados con los mismos marcadores de `scripts/deconvolution_cell_types.py`. Al ser composicionales (suman 1), se contrasta además descartar el tipo de mayor media como referencia frente a incluir los 12.

---

## 2. Validación contra E1

La variante **NNLS reproduce E1 con 7/7 veredictos idénticos**. La metodología queda confirmada: E1 usó fracciones NNLS + OLS. Las diferencias numéricas menores en M1 provienen de que E1 empleó Welch (varianza desigual) y este script OLS.

**El hallazgo de E1 es correcto: el eje opioide no sobrevive el ajuste composicional.**

---

## 3. Resultado principal — COL9A1 y PTN sobreviven

| gen | M1 (grupo) | M2 (+sexo) | M3 (+células) | β grupo | veredicto |
|---|---|---|---|---|---|
| **COL9A1** | 1.6×10⁻⁸ | 8.9×10⁻⁶ | **0.012** | +0.370 | **sobrevive** |
| **PTN** | 1.6×10⁻⁶ | 9.6×10⁻⁵ | **0.028** | +0.223 | **sobrevive** |
| OPRM1 | 1.7×10⁻⁶ | 6.0×10⁻⁵ | 0.030–0.080 | +0.32 | inestable |
| TACR1 | 2.1×10⁻⁵ | 2.2×10⁻⁴ | 0.039–0.117 | +0.16 | inestable |
| TAC1 | 1.8×10⁻⁴ | 3.5×10⁻³ | 0.080–0.393 | +0.20 | muere |
| PENK | 1.4×10⁻² | 9.5×10⁻³ | 0.250–0.305 | +0.22 | muere |
| OPRK1 | 3.2×10⁻³ | 3.7×10⁻² | 0.796–0.836 | +0.02 | muere |
| OPRD1 | 0.277 | 0.713 | 0.655–0.930 | −0.01 | muere |
| POMC | 0.360 | 0.545 | 0.917–0.928 | +0.02 | muere |

### Barrido de variantes (4 implementaciones)

| gen | NNLS/ref-drop | NNLS/las-12 | scores/ref-drop | scores/las-12 | |
|---|---|---|---|---|---|
| **COL9A1** | 0.020 | 0.020 | 0.012 | 0.012 | **4/4** |
| **PTN** | 0.046 | 0.046 | 0.028 | 0.028 | **4/4** |
| OPRM1 | 0.080 | 0.080 | 0.030 | 0.030 | 2/4 |
| TACR1 | 0.117 | 0.117 | 0.039 | 0.039 | 2/4 |
| resto del eje | — | — | — | — | 0/4 |

COL9A1 y PTN son **los únicos genes que sobreviven bajo las cuatro implementaciones**. PTN queda marginal bajo NNLS (p = 0.046) y debe reportarse como tal.

Colinealidad: VIF máx = 13.1 (NNLS) y 5.6 (marker-scores); mediana 2.7 en ambos. Moderada, no degenerada.

---

## 4. Control negativo — el ajuste no destruye señal indiscriminadamente

600 genes al azar (marcadores celulares excluidos, expresados en ≥50 % de las muestras):

- Con efecto de grupo tras ajustar por sexo (M2 p < 0.05): **273**
- De esos, sobreviven M3: **76/273 = 28 %**
- Mediana de `p_full_adj` en ese subconjunto: 0.182

El ajuste composicional elimina ~72 % de las señales, pero deja pasar una fracción sustancial. **Morir en M3 es informativo y sobrevivir también lo es** — ninguno de los dos resultados es un artefacto del modelo.

---

## 5. Interpretación

1. **El eje opioide/taquikinina es composicional.** Su señal se explica por diferencias en poblaciones celulares entre FM y HC, no por regulación transcripcional por célula. Sigue siendo un hallazgo publicable —y biológicamente interesante— pero es una afirmación distinta a la que hace el manuscrito actual.

2. **COL9A1–PTN es el único módulo que sobrevive los tres confusores** evaluados: sexo, corrección múltiple (Bonferroni sobre el modelo sex-adjusted) y composición celular. Es la señal más robusta de la investigación.

3. **El abstract actual tiene el orden invertido.** Declara el eje opioide "the most robust finding of the investigation"; los datos del propio repositorio dicen lo contrario.

---

## 6. Implicaciones para el manuscrito

- Intercambiar la jerarquía: COL9A1–PTN pasa a hallazgo principal; el eje opioide se reencuadra como **desplazamiento de poblaciones celulares**, no como activación transcripcional.
- Subir el resultado de deconvolución al abstract. Hoy vive en una nota de §4 y contradice la frase titular.
- Reportar PTN como marginal bajo NNLS (p = 0.046).
- El diseño de validación Olink no cambia: COL9A1 y PTN siguen siendo los analitos correctos, ahora con mejor justificación.

---

## 7. Limitaciones

- Las fracciones son **estimadas por marcadores sobre la misma matriz**, no medidas por citometría. Ajustar por covariables derivadas del mismo dato puede sobre-ajustar; el control negativo (§4) acota ese riesgo pero no lo elimina.
- Sin recuentos celulares medidos ni datos de medicación, no se puede separar "composición celular" de "efecto de opioides crónicos sobre la composición". Ambos son consistentes con estos resultados.
- Los marcadores de Mast_cells/Basophils/Dendritic comparten genes (CPA3, MS4A2, FCER1A, HDC), lo que hace inestable la atribución de *qué* tipo celular es el confusor. La conclusión de que **hay** confusión composicional no depende de esa atribución.
- Bulk PBMC no resuelve subpoblaciones. scRNA-seq sería el test definitivo.
