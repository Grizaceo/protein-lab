# ADVERSARIAL VERIFICATION REPORT — Biomarcadores FM (GSE221921)

**Fecha:** 2026-08-03
**Revisor:** DAVI (agente adversarial)
**Output auditado:** `validate_fm_biomarkers_iter2.py` + hallazgos de sesión (IL-6/PENK/LGALS3BP)
**Dataset:** GSE221921 — `datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx`
**Rubric:** Investigación/Research (adversarial-verification skill) — claims con fuente verificable, estadística apropiada, limitaciones declaradas.

---

## SUMMARY

- **Issues found: 6** (1 metodológico, 1 de atribución, 1 de magnitud, 1 de fragilidad, 2 de matiz externo)
- **Veredicto central:** El claim IL-6 HIGH / PENK MEDIUM / LGALS3BP UNSUITABLE **sobrevive la verificación adversarial — y se fortalece** al usar la estadística correcta (Mann-Whitney + Bonferroni). Sin embargo, la **magnitud de efecto es pequeña (d<0.32 en todos)** y el claim de "validated proxy" debe matizarse: es "significativo y reproducible", no "efecto clínicamente grande".
- **verified: PARTIAL** (el resultado se confirma; la presentación estadística debe corregirse)

| Claim original | Veredicto adversarial |
|---|---|
| IL-6 FC=1.66, p=0.033, proxy HIGH | ✅ CONFIRMADO, se fortalece (MWU p=0.0002, Bonferroni×12=0.0024) |
| PENK FC=1.38, p=0.157 (NS trend) | ✅ CONFIRMADO, se fortalece (MWU p=0.0031, Bonferroni=0.0378 → SIGNIFICATIVO) |
| LGALS3BP discordancia CSF↑/PBMC↓ | ✅ CONFIRMADO (FC=0.746, MWU p=0.0003) |
| 2-gene model AUC=0.65-0.66 | ⚠️ MATIZADO: AUC honesta out-of-fold = 0.616 (0.648 in-sample) |
| MDH1 LOW | ✅ CONFIRMADO (NS en ambos tests) |
| PCSK1N LOW | ⚠️ RE-CLASIFICAR: significativo con MWU (p=0.0007, Bonferroni=0.0083) |

---

## Q1: DATA INTEGRITY — ✅ PASA

- Mapping `Sample_# → Etiology` correcto: **96 FM + 93 HC = 189 samples**, 0 samples huérfanos (todas las columnas `Sample_` tienen metadata y viceversa).
- Counts reproducen el claim exactamente.
- **Outliers (>3 SD):** 1-3 por grupo por gen. Bajos, no dominan. No hay evidencia de que un outlier único explique los resultados.
- ⚠️ **Fragilidad detectada:** el script apunta a `/tmp/GSE221921_FM_ProcessedData.xlsx` que YA NO EXISTE (se limpió). El archivo real está en `datos/geo/...`. El script es no-reproducible tal como está. **Fix: usar path relativo al repo.**

## Q2: STATISTICAL ROBUSTNESS — ⚠️ METODOLÓGICO (el resultado sobrevive, la prueba era incorrecta)

- **Shapiro-Wilk: TODOS los genes, AMBOS grupos NO normales** (p de 1e-7 a 1e-16). FPKM es heavy-tailed. El `ttest_ind` del script original **asume normalidad que no existe** — metodológicamente incorrecto para FPKM.
- **Con la prueba correcta (Mann-Whitney U) + Bonferroni ×12 genes:**

| Gen | t-test p (script) | MWU p | Bonferroni×12 | Sobrevive? |
|---|---|---|---|---|
| IL6 | 0.033 | **0.0002** | **0.0024** | ✅ SÍ |
| PENK | 0.157 (NS) | **0.0031** | **0.0378** | ✅ SÍ (¡antes NS!) |
| LGALS3BP | 0.034 | **0.0003** | **0.0034** | ✅ SÍ |
| PCSK1N | 0.175 (NS) | **0.0007** | **0.0083** | ✅ SÍ (¡antes LOW!) |
| MDH1 | 0.331 (NS) | 0.986 | 1.0 | ❌ NO |

- **AUC honesta:** el script calcula AUC in-sample (0.648) → **sesgo optimista**. AUC out-of-fold = **0.616**; CV accuracy = 0.582 ± 0.126 (≈ azar). La conclusión del script ("no sirven SOLO para clasificación") es correcta y se refuerza.
- ⚠️ **Issue 1 (metodológico):** el t-test paramétrico sobre FPKM no normal era incorrecto. La documentación debe usar Mann-Whitney.
- ⚠️ **Issue 2 (re-clasificación):** PCSK1N pasó de "LOW/NS" a significativo con el test correcto. No es proxy (dirección ↓, y el CSF decía ↓ también — consistente), pero el veredicto LOW era por test inadecuado.

## Q3: PROXY VALIDITY — ✅/⚠️ EVIDENCIA EXTERNA (el claim se sostiene, con un matiz importante)

- **IL-6 periférico en FM: SÓLIDO.** Bäckryd 2017 (PMC5344444, el mismo paper Olink usado como template) — IL-6 elevado en plasma FM (p<0.001 univariado), y confirma que "plasma y CSF reflejan compartimentos distintos pero están interconectados". Tsilioni 2016 — IL-6 + SP + TNF elevados en suero FM (vía mast cells). El proxy periférico de IL-6 está anclado.
  - ⚠️ Matiz: en el análisis **multivariado** de Bäckryd, IL-6 NO es de los discriminadores principales (solo univariado). El claim debe decir "elevado periférico reproducible", no "discriminador robusto".
- **Substance P/PENK: PARCIAL.** Russell 1994 (PMID 7526868, 1028 citas) — SP elevado 3-fold en CSF de FM, pero **"no correlaciona con severidad del dolor"**. Tsilioni 2016 lo ve elevado en suero. 
  - ⚠️ **Precedente adverso crítico:** BDNF y NGF están elevados en CSF de FM pero **NO en plasma** (revisión PMC10341963). Los neuropéptidos NO siempre se trasladan al compartimento periférico. La correlación plasma↔CSF de SP **no está establecida** — hay evidencia de que neuropéptidos hermanos fallan en ese traslado. El grade MEDIUM de PENK debe mantener la advertencia de que es el proxy más frágil.
- **LGALS3BP:** la discordancia (CSF↑ / PBMC↓) es biológicamente plausible (secreción microglial local vs. clearance periférico), consistente con el grounding.

## Q4: LGALS3BP DISCORDANCIA — ✅ REPRODUCIBLE (corregir atribución)

- **Números reproducidos exactamente:** FC=0.746 (claim: 0.75), p=0.034 t-test (claim: 0.034), MWU p=0.0003.
- ⚠️ **Issue 3 (atribución):** el prompt adversarial citaba `validate_fm_biomarkers_iter2.py` como fuente del hallazgo LGALS3BP, pero **ese script NO incluye LGALS3BP en su lista de genes** (wray_genes = 10 de Wray + IL6 + PENK). El número es correcto y vino de otro análisis de la sesión, pero la atribución de archivo en la documentación es inexacta. **Fix: documentar de qué script/notebook salió LGALS3BP.**

## Q5: BIOLOGICAL PLAUSIBILITY / EFFECT SIZE — ⚠️ TODOS PEQUEÑOS

| Gen | Cohen's d | Clasificación |
|---|---|---|
| IL6 | +0.313 | small |
| PENK | +0.207 | small |
| LGALS3BP | -0.311 | small |
| PCSK1N | -0.198 | small |
| MDH1 | -0.142 | negligible |

- **Todos los efectos son PEQUEÑOS (d < 0.32).** La significancia estadística es real (y robusta al test no-paramétrico + corrección), pero la **magnitud del efecto es modesta**. "Validated proxy" = significativo y reproducible, NO "efecto clínicamente grande". El protocolo Olink de validación en plasma debe reportar tamaños de efecto, no solo p.
- IL-6 FC=1.66 en PBMCs → "inflamación sistémica en FM": consistente con la literatura (Bäckryd, Tsilioni), pero como efecto small, la frase correcta es "estado proinflamatorio moderado".

---

## RECOMENDACIONES (ordenadas por esfuerzo)

1. **[5 min] Fix path del script:** `/tmp/GSE221921...` → `datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx` (path relativo). Sin esto el script no corre.
2. **[10 min] Reemplazar t-test por Mann-Whitney + Bonferroni** en `validate_fm_biomarkers_iter2.py` y en el validation_report.md. El t-test sobre FPKM no normal es incorrecto aunque el resultado sobreviva.
3. **[10 min] Reportar AUC out-of-fold (0.616), no solo in-sample (0.648).** Añadir StratifiedKFold con OOF predictions.
4. **[15 min] Re-clasificar PCSK1N** de LOW → candidato a proxy (significativo MWU+Bonferroni, dirección consistente CSF↓/PBMC↓). Añadir Cohen's d a la tabla de expresión.
5. **[15 min] Matizar el lenguaje** en protocolo + preprint: "significant small-effect proxy" en vez de "validated proxy" sin calificación; añadir la advertencia BDNF/NGF (los neuropéptidos no siempre trasladan CSF→plasma) junto a PENK.
6. **[15 min] Corregir atribución de LGALS3BP** — documentar la fuente exacta del FC=0.75 (qué script/notebook).

## GRADE: B+

- Confirmado y reproducible (pasa Q1, Q4; Q2 sobrevive con prueba correcta)
- Penalizado por: t-test inapropiado (metodología), AUC in-sample reportada como si fuera honesta, efecto small no declarado, path frágil, atribución LGALS3BP inexacta.
- **No hay falsificación del hallazgo central.** Al contrario: el test correcto fortalece IL-6, PENK y LGALS3BP.

## VEREDICTO FINAL

**verified: PARTIAL** → el claim "IL-6 y PENK son proxies periféricos diferencialmente expresados en FM (LGALS3BP unsuitable)" **se mantiene y se fortalece** con la estadística no-paramétrica. Correcciones obligatorias antes de publicar: Mann-Whitney + Bonferroni, AUC out-of-fold, Cohen's d, path relativo, y matiz de efecto pequeño. El siguiente paso lógico (protocolo Olink IL-6/PENK en plasma) es válido, priorizando IL-6 sobre PENK por su menor fragilidad.
