# AUDITORÍA EXTERNA ADVERSARIAL — Preprint FM v2.6

**Fecha:** 2026-08-03
**Auditor:** revisor independiente adversarial (rol: intentar derrumbar el trabajo, no validarlo)
**Alcance:** preprint v2.6 + 8 documentos de soporte + 6 scripts + fuente primaria XML
**Método:** re-ejecución de todos los scripts, re-cálculo de todos los números desde matrices crudas,
verificación de citas contra el XML de PMC12713070 y contra la API de PubMed, y ejecución de
tests estadísticos que el trabajo **no** realizó.
**Verificador ejecutable:** `scripts/audit_verify_claims.py` (corre en ~2 min, 11 checks)

---

## PUNTAJE: 52 / 100 — MALO (umbral publicable ≥ 70)

| Rúbrica | Pts | Resumen |
|---|---|---|
| Integridad de citas (25) | **11** | Verificación del XML primario **excelente**; pero 1 PMID **inexistente**, 1 paper **totalmente mal atribuido**, 2 PMIDs cruzados, 1 título inventado, 1 referencia faltante |
| Corrección estadística (25) | **12** | Números **100% reproducibles** (16/16 exactos); pero el claim central **colapsa** bajo el propio estándar de ajuste por sexo del preprint |
| Honestidad interpretativa (25) | **15** | Cultura de auto-corrección **real y documentada**; pero el abstract es sistemáticamente más confiado que los docs internos, que contienen la refutación |
| Reproducibilidad (15) | **8** | Scripts corren, seed fijada, Zenodo y GitHub reales; pero **ningún script del repo produce los números del abstract** |
| Estructura científica (10) | **6** | Bien organizado y con predicción falsable; §4.6–4.9 es otro paper injertado |

> **El puntaje está dominado por fallas de publicabilidad, no de fabricación de datos.**
> Los datos son reales y fueron recalculados uno por uno. El problema es el aparato de
> citas y una inferencia estadística que nunca se ejecutó.

---

## LO QUE AGUANTA EL ATAQUE (decir esto explícitamente, es mérito real)

1. **Reproducibilidad numérica perfecta.** Los 16 valores de las Tablas 2 y 4, los 5 rho de
   co-expresión PBMC, la Tabla 1 completa contra su CSV y los 5 FC de GSE67311 reproducen
   **exactos hasta el tercer decimal** desde las matrices crudas. **No hay ni un número inventado.**
2. **Las 5 citas textuales de Chen 2025 son literales**, verificadas contra
   `fuentes_verificadas/PMC12713070_Chen2025_AdvSci_CWP_proteogenomic.xml` — incluida la de
   agonistas: *"CA14 agonists—rather than inhibitors—may offer greater therapeutic utility in this context"*.
3. **La corrección de dirección de CA14 está documentada con el error previo escrito y marcado ❌**
   (`GROUNDING_UKB_Olink_DolorCronico.md:159-191`). Eso es integridad real, no cosmética.
4. **La corrección PENK→TAC1 está propagada al 100%.** Búsqueda exhaustiva de residuos en todo
   el repo: **cero**.
5. **El eje opioide/taquikinina (claim C) es un hallazgo genuino** — es lo único que sobrevive
   el ajuste por sexo, OLS y female-only. Hoy está subordinado a CA14; debería ser el titular.
6. **Los negativos están reportados sin cosmética** en los docs internos (GSE67311, GSE269047,
   *"la cross-validación de la madrugada era falsa"*).

---

## VEREDICTOS POR CLAIM

### A) CA14 candidato causal #1 — **PARCIALMENTE CIERTO, con un fallo CRÍTICO no detectado**

**Todo lo que se cita de Chen 2025 es correcto y literal:**

| Claim | Cita verificada en el XML | |
|---|---|---|
| ↓ en plasma | *"the ten most downregulated proteins were **CA14**, APOF, PON3, SELENOP, EGFR, ITGAV, SCT, CELA2A, IGFBP3, and PPY"* | ✓ |
| MR protector | *"while CA14 and LEG1 were negatively associated with pain cross-sectionally, MR suggested protective effects of genetically elevated expression"* | ✓ |
| Agonistas, no sulthiame | *"**CA14 agonists—rather than inhibitors—may offer greater therapeutic utility in this context**"* | ✓ literal |
| top-ranking | *"CA14, identified as the top-ranking protein…"* | ✓ |
| PP.H4 > 0.5 | *"Three proteins—CA14, DDR1, and MLN—demonstrated strong evidence of colocalization (PP.H4 > 0.5)"* | ✓ |
| top SHAP | *"CA14 emerged as the most impactful, reflected by its highest SHAP value"* | ✓ |

**Pero el pilar propio del triángulo es un artefacto de sexo:**

```
CA14   cohorte completa:   p=3.3e-04   d=+0.41   FC=2.29    <- lo publicado
       SOLO MUJERES:       p=0.1345    d=+0.24   FC=1.60    <- NO SIGNIFICATIVO
       OLS ~case+sex:      p=0.0960                          <- NO SIGNIFICATIVO
       CA14 en CONTROLES:  F=0.901 vs M=0.374, p=0.034       <- CA14 ES SEXO-DEPENDIENTE
       ratio F/M en controles = 2.41   ≈   el "FC=2.29" publicado
```

Grupos: FM 91F/5M vs HC 41F/52M. **El efecto sexo puro (2.41×) explica prácticamente todo el
"efecto FM" (2.29×).** Además CA14 está inflado de ceros (29/189) y es extremo
(mediana ~0.5, máx 20.96), lo que hace frágil cualquier FC de medias.

El preprint declara en §2.4 cinco modelos obligatorios por el desbalance de sexo, y en §4.3
que *"the female-only subgroup [is] the primary, statistically unconfounded model"* — pero
ese estándar se aplicó **solo a los 16 genes GWAS/mastocito**, nunca a las Tablas 2 y 4.

**Nota de matiz que también corresponde:** la propia metodología de Chen 2025 define
*"strong evidence of colocalization"* como **PH4 ≥ 0.8**, y *"medium evidence"* como
0.5 < PH4 < 0.8. El paper luego llama "strong" a PP.H4 > 0.5, contradiciéndose. Citar
"PP.H4 > 0.5" es fiel, pero conviene declarar que por el propio umbral del paper eso es
**evidencia media, no fuerte**.

### B) El eje IL-6/IL-8 no sobrevive a escala poblacional — **PARCIALMENTE CIERTO, formulación falaz**

El conteo es honesto y lo verifiqué en el texto completo de Li ZY 2025 (PMC12021123):
`51,644` ✓, `2,923` ✓, y **0 menciones** de IL6 / IL-6 / CXCL8 / IL-8 / interleukin / TAC1 / Substance P ✓.

**Pero la inferencia no lo es.** El preprint (L29, L235, L407) escribe:
*"IL-6, IL-8/CXCL8, TAC1 and Substance P appear **zero times** … the classical inflammatory
axis **is not supported** at population scale."*

**TAC1 / Substance P nunca estuvieron en el panel Olink.** Cero menciones de un analito no
medido no es evidencia de nada. Y el repo ya lo sabe:

- `EJE_OPIOIDE_TAQUIKININA_FM.md:56` — *"UKB **no medía neuropéptidos** en su panel inflamatorio — por eso TAC1/TACR1 no aparecen ahí"*
- `PROTOCOL_Olink_FM_Biomarker_Validation.md:28` — *"Substance P (TAC1, **no está en panel Olink**)"*

Para IL-6/CXCL8 (sí presentes en Olink Explore 3072) el argumento es válido pero **débil**:
0 menciones en el texto narrativo ≠ ausencia en las 474 proteínas asociadas, que viven en
tablas suplementarias que no se consultaron.

**Problema adicional en el mismo bloque:** el preprint (L43, Tabla 4) presenta 8 genes como
*"MR causal chronic pain"* aplicables a FM. El texto de Li ZY dice que son **específicos de
sitio anatómico**: *"CD302 → headache; RARRES2 → neck/shoulder; TNFRSF1B → back; CD74 → hip;
BTN2A1/TNFRSF9/COL18A1/TNF → abdominal; BTN2A1 y TNFRSF4 → knee"*.
**Ninguno de los 5 que el preprint destaca aparece en la lista de 18 causales de CWP de Chen 2025.**
Se está usando un set génico de dolor lumbar/rodilla/cabeza como si fuera un set de FM.

Y la dirección plasmática de esos 5 **nunca se reporta**; la única pista de la fuente apunta al
revés: *"TNFRSF4, known as OX40 (CD134)… exhibits elevated levels in conditions associated with
immune response to neural damage."* La lectura de "inmunomodulación/agotamiento" es por tanto
especulativa, no "consistente con" la fuente.

### C) Eje opioide/taquikinina en PBMC — **VERDADERO** (el único claim que aguanta todo)

Recalculado desde `GSE221921_FM_ProcessedData.xlsx`. **Coincide hasta el último decimal:**

| Gen | FC calc / publicado | p calc / publicado | d calc / publicado |
|---|---|---|---|
| TACR1 | 2.731 / 2.73 | 0.000995 / 0.0010 | +0.601 / +0.60 |
| OPRM1 | 2.282 / 2.28 | 5.0e-06 / <0.0001 | +0.531 / +0.53 |
| TAC1 | 2.099 / 2.10 | 0.000188 / 0.0002 | +0.469 / +0.47 |
| OPRK1 | 1.775 / 1.78 | 0.001732 / 0.0017 | +0.376 / +0.38 |

Los 5 rho de co-expresión: exactos. **Y sobrevive el ajuste por sexo que CA14 no sobrevive:**
TACR1 p_F=0.0087 (d=+0.59), OPRM1 p_F=0.0001, TAC1 p_F=0.0038, OPRK1 p_F=0.031, PENK p_F=0.0003;
OLS ~case+sex significativo en los cinco.

**Dos matices obligatorios:**
- Bajo Bonferroni sobre las 14 pruebas del análisis female-only, solo **OPRM1 y PENK** sobreviven
  (TACR1 0.122, TAC1 0.054, OPRK1 0.435). Los *effect sizes* sí se mantienen; la pérdida es de
  potencia (41 controles mujeres).
- **PENK está sub-reportado.** El preprint lo llama "trend" (d=+0.21 en cohorte completa), pero
  en mujeres es **d=+0.41, p=0.0003** — más fuerte que TACR1.

### D) GSE67311: "módulo coherente, amplitud compartimento-dependiente" — **FALSO como está escrito**

La no-replicación de amplitud es correcta y bien reportada (los 5 FC≈1.0 reproducen). El
problema es la co-expresión. Corrí el test que nadie corrió (Fisher r-to-z, los **10** pares):

| Par | rho FM | rho HC | p_dif | ¿Reportado en el preprint? |
|---|---|---|---|---|
| TACR1–OPRK1 | +0.736 | +0.405 | **0.003** | SÍ |
| OPRM1–OPRK1 | +0.530 | +0.279 | 0.077 | SÍ |
| TACR1–OPRM1 | +0.420 | +0.280 | 0.353 | SÍ |
| OPRM1–TAC1 | +0.363 | +0.078 | 0.079 | SÍ |
| OPRK1–PENK | +0.375 | +0.150 | 0.157 | SÍ |
| **TACR1–TAC1** | **+0.189 (NS)** | **+0.420 (p<0.001)** | 0.135 | ❌ omitido |
| **OPRK1–TAC1** | +0.259 | +0.370 | 0.473 | ❌ omitido |
| **OPRM1–PENK** | +0.200 | +0.201 | 0.996 | ❌ omitido |
| **TAC1–PENK** | −0.003 | +0.076 | 0.647 | ❌ omitido |

- Se reportan **exactamente** los 5 pares donde FM > HC y se omiten los 4 donde HC ≥ FM.
- *"HC pairs consistently weaker or non-significant"* (L177) es **literalmente falso**: en
  TACR1–TAC1 el HC es más fuerte y significativo, y el FM es NS.
- Solo **1 de 10** pares tiene diferencia FM–HC estadísticamente significativa.
- *"several pairs exceeding the PBMC reference range (0.31–0.63)"* → **solo uno** (0.736).
- **Problema técnico de fondo:** en whole blood esas sondas están en el ruido.
  Percentil de intensidad dentro del array: **TAC1 p8, OPRK1 p13, OPRM1 p19**
  (vs ACTB p99, CD74 p99). Correlacionar sondas del decil inferior mide fondo compartido,
  no un "módulo transcripcional".
- Comparar rho entre RNA-seq FPKM y microarray RMA (plataformas y dinámicas distintas) no es
  una comparación válida en primer lugar.

### E) QSP: ΔpH ≈ −0.009 descarta la vía — **FALSO: el número es un bug de calibración**

El razonamiento **cualitativo** del doc es correcto (`SIMULACION_QSP_CA14_PH.md:26-28`: la
anhidrasa acelera la velocidad, no desplaza el equilibrio). Pero el número no mide eso.

`scripts/qsp_ca14_ph_nociception.py:47-48` fija a mano `K_UNCAT_F=0.15` y `K_UNCAT_R=50.0`,
lo que implica Keq_no-catalizado = 3.0e-3 mM — **3.8× distinto** del Keq termodinámico
(7.92e-4 mM) al que **sí** se calibró el par catalítico. Al bajar `ca_rel`, el par inconsistente
pesa más y el Keq efectivo deriva:

```
(A) parámetros actuales:      ca_rel 1.0→0.5, Keq_efectivo deriva +2.13%  =>  ΔpH = −0.0091
(B) k_uncat_r = k_uncat_f/Keq = 189.3 (consistente):                      =>  ΔpH = +0.0000008
```

**Todo el ΔpH publicado es la deriva del Keq.** Con termodinámica consistente el efecto es
exactamente cero — porque al sumar las dos ecuaciones de estado estacionario los términos de
CA **se cancelan idénticamente**: `k_buf·h = J_co2 + J_acid − k_diff·c`. El modelo es incapaz
*por construcción* de exhibir el efecto.

Y **no está calibrado en el basal**: el pH lo fija `J_co2/k_buf`, no la química del carbonato.
Da 7.83 / 7.21 / 6.76 según `J_co2`, mientras su propio check Henderson-Hasselbalch imprime
7.33 y **ningún escenario lo reproduce**.

Ironía: la v1 daba *"ΔpH = 0.000 plano"* y fue descartada como *"defecto técnico"* (L57-60).
**La v1 tenía razón.** Un modelo que no puede mostrar el efecto no puede refutarlo:
`SIMULACION_QSP_CA14_PH.md:46` (*"queda descartado"*) es un non sequitur.

### F) Power analysis — **PARCIALMENTE CIERTO: supuestos razonables, premisa no**

Corre, reproduce, `seed=42` ✓. `sd_tech = 0.165/ln2 = 0.238` ✓ correcto.
Mann-Whitney ✓ apropiado. n=70 para d=0.5 ✓ reproduce.

Fallos:
1. **La premisa d=0.3–0.6 no está anclada.** CA14 viene de un estudio con n=29,254; estar entre
   las 10 más bajas ahí es perfectamente compatible con **d ≈ 0.1–0.2**, que exigiría
   n ≈ 400–1500/grupo. El protocolo lo admite como riesgo "HIGH" (§9), pero la recomendación
   operativa (n=50–70) se construye sobre el escenario optimista.
2. `sd_bio = 1.0` NPX se declara *"típico"* sin fuente (`power_analysis_ca14_olink.py:36`);
   el rango real es 0.3–1.5 y la potencia es muy sensible a eso.
3. `mu_fm = d*1.0` con `sd_total = 1.028` ⇒ el d simulado real es 0.973·d. Conservador, pero mal etiquetado.
4. **Sin multiplicidad:** el pre-registro corrige ×3 (`PROTOCOL:117`), la simulación usa α=0.05 pelado.

---

## LOS 10 ERRORES CONCRETOS

| # | Sev | Qué dice | Por qué está mal | Fix |
|---|---|---|---|---|
| **1** | **CRÍTICO** | `preprint:463` — *Zhang, Y. et al. (2007) … J Biol Chem, 282(11), 7790–7798. **PMID: 17351609*** | **El PMID no existe.** `efetch` devuelve `<PubmedArticleSet></PubmedArticleSet>` vacío. JBC 282(11):7790 es PMID 17227761, otro paper. El trabajo real de splicing exón 6 / rs1076560 es **PNAS 2007;104(51):20552-7, PMID 18077373** | Reemplazar por PMID 18077373 y corregir revista/volumen/páginas |
| **2** | **CRÍTICO** | `preprint:451` — *Peng, X. et al. (2022). Pramipexole inhibits fibromyalgia-like symptoms in a reserpine-induced mouse model. Neural Regen Res, 17(3), 667–674. PMID: 35799530* | PMID 35799530 = **Ziaee SM, "neuregulin-1beta1 in multiple sclerosis"**. Autor, título, volumen, páginas y PMID: todo incorrecto. El paper real es **Martins CP et al., Neural Regen Res 2022;17(2):450-458, PMID 34269222** | Reemplazar la entrada completa |
| **3** | **CRÍTICO** | `preprint:15,189,198,233,407` — CA14 ↑ en PBMC FM, FC=2.29, "el candidato transversal más fuerte" | Colapsa en female-only (p=0.135, d=0.24, FC=1.60) y en OLS sex-adj (p=0.096). CA14 es sexo-dependiente en controles (p=0.034; ratio F/M=2.41 ≈ el FC reportado). Tablas 2 y 4 nunca recibieron el ajuste que §2.4 declara obligatorio | Correr los 5 modelos sobre Tablas 2 y 4. Reclasificar CA14 como **"confundido por sexo, no significativo en el modelo primario"**. Reescribir abstract y conclusión |
| **4** | **CRÍTICO** | `preprint:29,235,407` — *"TAC1 and Substance P appear zero times… the classical inflammatory axis is not supported at population scale"* | TAC1/SP **nunca se midieron** en el panel Olink. Ausencia de medición ≠ evidencia de ausencia. El propio repo lo dice (`EJE_OPIOIDE:56`, `PROTOCOL:28`) | Separar: "IL-6/CXCL8 medidos y no destacados" vs "TAC1/SP **no cubiertos** por el panel — no evaluables". Eliminar la conclusión de no-respaldo para neuropéptidos |
| **5** | **MAYOR** | `preprint:177` — *"HC pairs consistently weaker or non-significant"*, *"several pairs exceeding 0.63"* | Falso: en TACR1–TAC1 el HC es más fuerte y significativo (+0.420, p<0.001) y el FM es NS. 4/10 pares tienen HC≥FM y están omitidos. Solo 1 par excede 0.63. Solo 1/10 diferencias es significativa (Fisher z). Las sondas están en percentil 8–19 de intensidad | Publicar los 10 pares con rho_FM, rho_HC y p_dif. Añadir el nivel de intensidad. Rebajar a *"un solo par difiere; el resto no distingue FM de HC"* |
| **6** | **MAYOR** | `SIMULACION_QSP:46` / `preprint:249` — *"la vía queda descartada"*, "thermodynamically calibrated" | El ΔpH=−0.009 es deriva del Keq por `K_UNCAT_R=50` inconsistente; con `k_uncat_r=k_uncat_f/Keq` el efecto es +8e-7. Los términos de CA se cancelan en la suma de ecuaciones ⇒ insensibilidad estructural. El pH basal lo fija `J_co2/k_buf`, no el carbonato (7.83/7.21/6.76 vs HH 7.33) | Corregir `K_UNCAT_R`. Reportar **ΔpH = 0 exacto** y reformular: *"un modelo de estado estacionario no puede evaluar esta hipótesis; requiere modelo cinético transitorio"*. Eliminar "descartada" |
| **7** | **MAYOR** | `preprint:471-489` "Data & Code Availability" + `preprint:126` *"session analysis"* | **Ningún script del repo calcula** TACR1/OPRK1/OPRD1/POMC en GSE221921 ni **nada de la Tabla 4** (CA14 + 8 genes UKB). `grep TNFRSF1B` sobre todos los `.py` → 0 resultados. Los números son correctos (verificados), pero un tercero no tiene ruta de reproducción | Commitear `validate_ukb_causal_gse221921.py` y `validate_opioid_axis_gse221921.py` con los 24 genes y los 5 modelos |
| **8** | **MAYOR** | `preprint:216-222` §3.6 — "replicación independiente" en GSE269047 con p-values de `DRD2-opti_at`, `GATA2-bgrd_st`, `KIT-opti_st`, y conclusión científica derivada | El mismo preprint (L220) y `GSE269047_NO_UTILIZABLE.md` declaran que la plataforma solo tiene transcritos HERV y *"los símbolos Hugo no existen en su anotación"*. Los sufijos `opti`/`bgrd`/`rand` son categorías de diseño de sonda, no genes. Se extrae conclusión de una medición declarada ininterpretable. Además la cohorte es **FM/ME-CFS mezclada** | Borrar §3.6 completa. Dejar una línea en Limitaciones |
| **9** | **MAYOR** | `preprint:43` + Tabla 4 — 8 genes como *"MR causal chronic pain"* aplicables a FM; L200 *"consistent with an immunomodulatory/exhaustion pattern"* | En Li ZY son asociaciones **por sitio anatómico** (cabeza, espalda, cadera, abdomen, rodilla). **Ninguno de los 5 destacados está entre los 18 causales de CWP de Chen 2025.** Y nunca se reporta la dirección plasmática; la única pista de la fuente apunta al revés (*"TNFRSF4/OX40 exhibits elevated levels"*) | Renombrar a "genes causales de dolor crónico **específico de sitio**". Declarar dirección plasmática desconocida y la lectura de "agotamiento" como especulativa |
| **10** | **MENOR** | `preprint:417,423,437` — Bäckryd PMID 28331362; De la Luz-Cuellar título; "Kurian et al. 2017" = GSE67311 | Bäckryd real = **28424559** (28331362 = Turnbull, anestesia de rodilla) — y el PMID correcto **ya está** en `PROTOCOL:8`. De la Luz-Cuellar: el título real es *"…D1- and D2-like receptors have a sex-dependent effect in an experimental model of fibromyalgia"*. GSE67311 = **Jones KD et al., Clin Exp Rheumatol 2016** (el repo ya tiene `PMC4888802_Jones_2016_GSE67311.xml`) | Corregir las tres. Añadir Trott & Olson 2010 (citado en Tabla 6, ausente de la lista) |

### Menores adicionales

- PENK con `Bonf=0.248` (L170) y `Bonf=0.155` (L177) en el mismo documento — denominadores inconsistentes.
- `PROTOCOL:66` "Target 96 ~$2,000-3,000 **por muestra**" vs `PROTOCOL:216` "run propio ~$5-8K, 100 muestras" — inconsistencia de ~100×.
- `PROTOCOL:58` dice que Explore HT incluye Substance P; `PROTOCOL:76` dice que no está disponible en Olink. Contradicción en la misma sección.
- `PROTOCOL:256` dice "UKB (n=54K)"; Chen 2025 es n=29,254 (54,629 es el conteo de casos del GWAS de Kerrebijn).
- Texto corrupto sin corregir en `PROTOCOL:257-259`: *"el machismo QSP"*, *"taquinacina"*, *"radioinmunocromanografía"*, *"↑ en PBMC miRNA"*, *"Bäckryd/Gröfouri"*, *"CSI opcional"*, *"AUX out-of-fold"*.
- "Pre-registro" es un markdown en un repo git, no un registro con timestamp de tercero (OSF/AsPredicted). Etiquetarlo como "plan de análisis pre-especificado, no registrado externamente".
- `preprint:259` presenta MDGA2 "Back Pain score = 0.40" (✓ verificado exacto en `analisis/mdga2_associated_diseases.json`) como *"direct clinical associations with chronic pain"*, pero es un score `gwas_credible_sets`, no clínico, y se omiten las asociaciones **más altas**: skeletal abnormality 0.568, smoking initiation 0.539, obesity 0.536, ADHD 0.503 — que retratan a MDGA2 como locus pleiotrópico, no específico de dolor.

---

## VERIFICACIÓN COMPLETA DE REFERENCIAS

| Referencia | PMID declarado | ¿Existe? | Veredicto |
|---|---|---|---|
| Bi 2024 | 39310900 | ✓ Bi W, J Inflamm Res | **OK** |
| **Bäckryd 2017** | **28331362** | ✓ pero es **Turnbull ZA, anestesia rodilla** | ❌ **PMID CRUZADO** → 28424559 |
| Chen 2025 | 41025730 | ✓ Chen L, Adv Sci | **OK** — citas literales verificadas |
| Chinn 2016 | 26922414 | ✓ Chinn S | **OK** |
| **De la Luz-Cuellar 2023** | **37003519** | ✓ autor/revista OK, **título distinto** | ⚠️ **TÍTULO INVENTADO** |
| Edwards 2022 | 35085583 | ✓ Edwards S | **OK** |
| Gowri Gopal 2026 | 42109571 | ✓ | **OK** |
| Hamblin 2026 | 42034459 | ✓ | **OK** |
| Holman & Myers 2005 | 16052595 | ✓ Holman AJ | **OK** |
| Joodi 2026 | 42489789 | ✓ | **OK** |
| Kerrebijn 2025 | 41001472 | ✓ medRxiv | **OK** |
| **Kurian 2017 (GSE67311)** | **27157394** | ✓ pero es **Jones KD 2016, Clin Exp Rheumatol** | ❌ **AUTOR Y AÑO INCORRECTOS** |
| Li ZY 2025 | 40048323 | ✓ Adv Sci | **OK** — 51,644 / 2,923 verificados |
| Lindström 2026 | 42217644 | ✓ | **OK** |
| Love 2014 | 25516281 | ✓ | **OK** |
| Mohapatra 2024 | 38366049 | ✓ | **OK** |
| **Peng 2022** | **35799530** | ✓ pero es **Ziaee SM, neuregulin/EM** | ❌ **PAPER TOTALMENTE DISTINTO** → 34269222 |
| Russell 1994 | 7526868 | ✓ Russell IJ | **OK** |
| Sarzi-Puttini 2020 | 33024295 | ✓ | **OK** |
| Tayyab 2025 | 41239854 | ✓ | **OK** |
| **Zhang 2007** | **17351609** | ❌ **NO EXISTE** | ❌ **PMID FABRICADO** → 18077373 |
| Zhao 2025 | 40313599 | ✓ | **OK** |
| Benjamini & Hochberg 1995 | — | clásico real | OK (sin PMID, aceptable) |
| Pacheco 2014 | — | real (Front Immunol 5:117) | ⚠️ sin PMID |
| O'Mahony 2021 | — | sin PMID ni volumen | ⚠️ **no verificable** |
| Rodríguez-Pintó 2014 | — | sin PMID ni revista | ⚠️ **no verificable**, y sostiene el mecanismo de L153 |
| Tsilioni 2016 | — | sin PMID ni revista | ⚠️ **no verificable** |
| **Trott & Olson 2010** | — | citado en Tabla 6, **ausente de la lista** | ❌ **REFERENCIA FALTANTE** |
| Zenodo 10.5281/zenodo.20250218 | — | ✓ HTTP 200, handle resuelve | **OK** |
| github.com/Grizaceo/protein-lab | — | ✓ HTTP 200 | **OK** |

**4 defectuosas + 1 título inventado + 1 faltante + 3 no verificables, sobre 22 con PMID = 23% de error.**

---

## VEREDICTO FINAL

**No está listo para preprint público.** Bloquean cuatro cosas, en este orden:

1. **Un PMID fabricado y un paper completamente mal atribuido.** Esto solo descalifica el
   manuscrito: es exactamente el modo de falla que el historial del repo registra como
   corregido. La verificación se aplicó con rigor a las fuentes **nuevas** (Chen 2025) y
   nunca a la lista de referencias heredada.
2. **CA14 — el titular del abstract — no sobrevive el ajuste por sexo que el propio preprint
   declara obligatorio.** No es fraude: nadie corrió el test. Pero al correrlo, el efecto se
   explica por la composición 91F/5M vs 41F/52M. El abstract, la conclusión, la Tabla 4, el
   protocolo Olink y la hipótesis pre-registrada dependen de ese número.
3. **La estructura de co-expresión (claim D) está reportada selectivamente** y descansa sobre
   sondas en el ruido de fondo.
4. **El "negativo QSP" es un bug de calibración**, no un resultado.

**Camino más corto a publicable:** ver `PLAN_REPARACION.md`. Con las correcciones ahí descritas
—y **sin un solo dato nuevo**— el trabajo pasa a **BUENO (~75)**, porque el eje opioide es un
hallazgo real y bien medido y la verificación de la fuente primaria es de primer nivel.

---

## Cómo re-verificar todo esto

```bash
cd investigacion-fibromialgia
python3 scripts/audit_verify_claims.py
```

Estado esperado **antes** de reparar: **3/11 PASS**.
Los FAIL no deben "arreglarse forzando datos" — deben hacerse **consistentes con el texto**.
