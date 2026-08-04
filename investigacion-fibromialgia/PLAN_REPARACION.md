# PLAN DE REPARACIÓN Y CONTINUACIÓN — Investigación FM

**Para:** el agente Hermes que asiste a Cristóbal en esta investigación
**Origen:** `AUDITORIA_EXTERNA_2026-08-03.md` (auditoría adversarial independiente, 52/100)
**Verificador:** `scripts/audit_verify_claims.py`
**Estado inicial:** 3/11 checks en PASS

---

## REGLAS DE TRABAJO (leer antes de tocar nada)

1. **No "arregles" los FAIL forzando datos.** Los FAIL del verificador describen la realidad.
   El trabajo es hacer que **el texto** sea consistente con ellos, no al revés.
2. **Todo número publicado debe salir de un script commiteado.** Si un número vino de un
   "análisis de sesión", el número es válido pero **no publicable** hasta que exista el script.
   Este fue el error #7.
3. **Ninguna referencia entra sin verificación por API.** Antes de escribir un PMID:
   ```bash
   curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=<PMID>&retmode=json" \
     | python3 -c "import json,sys;d=json.load(sys.stdin)['result'];k=d['uids'][0];print(d[k].get('sortfirstauthor'),'|',d[k].get('source'),d[k].get('pubdate'),'|',d[k].get('title'))"
   ```
   Comparar autor, año, revista, volumen y páginas contra lo escrito. Si no coincide **todo**, no se usa.
4. **Todo hallazgo en GSE221921 se reporta con los 5 modelos de §2.4**, no solo Mann-Whitney
   sobre la cohorte completa. La cohorte es 91F/5M vs 41F/52M: sin ajuste por sexo, cualquier
   gen sexo-dependiente produce un falso positivo. Ese fue el error #3.
5. **Cuando una fuente no midió un analito, eso no es evidencia de nada.** Distinguir siempre
   "medido y nulo" de "no medido". Ese fue el error #4.
6. **Ejecuta `scripts/audit_verify_claims.py` antes y después de cada fase** y anota el conteo.

---

## FASE 0 — Estado (5 min)

```bash
cd investigacion-fibromialgia
python3 scripts/audit_verify_claims.py 2>&1 | tail -25
```

Anota el resultado en un archivo de bitácora. Esperado ahora: **3/11 PASS**.

---

## FASE 1 — Reparaciones bloqueantes

Bloquean la publicación. Hacerlas en orden. Cada una tiene criterio de aceptación.

### R1 · Referencia fabricada — Zhang 2007 [CRÍTICO · 5 min]

`preprint_dopaminergic_convergence_FM.md:463`. El PMID 17351609 **no existe**.

Reemplazar la línea completa por:

```
Zhang, Y., Bertolino, A., Fazio, L., Blasi, G., Rampino, A., Romano, R., Lee, M.L.T., Xiao, T.,
Papp, A., Wang, D., & Sadée, W. (2007). Polymorphisms in human dopamine D2 receptor gene affect
gene expression, splicing, and neuronal activity during working memory. *Proc Natl Acad Sci USA*,
104(51), 20552–20557. PMID: 18077373.
```

Revisar además §4.10 (`preprint:365-377`): la cita sostiene el mecanismo de splicing de exón 6.
Confirmar que lo afirmado (rs1076560/rs2283265 modulan inclusión de exón 6, D2S vs D2L)
está efectivamente en ese paper, y **no** afirmar `D' = 1.0` con rs2734833 sin una fuente
de LD verificable (LDlink/LDpair contra 1000G EUR). Si no se puede verificar, escribir
"en desequilibrio de ligamiento" sin el valor puntual.

**Aceptación:** el PMID resuelve por API y autor/revista/volumen/páginas coinciden.

### R2 · Referencia mal atribuida — Peng 2022 [CRÍTICO · 5 min]

`preprint:451`. PMID 35799530 = Ziaee SM, neuregulin en esclerosis múltiple. Nada que ver.

Reemplazar por:

```
Martins, C.P., et al. (2022). Pramipexole, a dopamine D3/D2 receptor-preferring agonist,
attenuates reserpine-induced fibromyalgia-like model in mice. *Neural Regen Res*, 17(2),
450–458. PMID: 34269222.
```

Verificar dónde se cita en el cuerpo y que la afirmación asociada corresponda a ese paper.

**Aceptación:** PMID resuelve y coincide autor/volumen/páginas.

### R3 · Tres referencias con datos incorrectos [MENOR · 10 min]

| Línea | Corrección |
|---|---|
| `preprint:417` | Bäckryd 2017 → **PMID 28424559** (el actual, 28331362, es Turnbull, anestesia de rodilla). El PMID correcto ya está en `PROTOCOL_Olink_FM_Biomarker_Validation.md:8` |
| `preprint:423` | De la Luz-Cuellar 2023 → título real: *"Spinal dopaminergic D1- and D2-like receptors have a sex-dependent effect in an experimental model of fibromyalgia"* |
| `preprint:437` | "Kurian, S.M., et al. (2017)" → **Jones, K.D., et al. (2016). Genome-wide expression profiling in the peripheral blood of patients with fibromyalgia. *Clin Exp Rheumatol*, 34(2 Suppl 96), S89–98. PMID: 27157394.** El repo ya tiene el full text: `literatura/adicional_grounding/verified/fulltext_xml/PMC4888802_Jones_2016_GSE67311.xml` |

Actualizar también las menciones en cuerpo: `preprint:45` y `preprint:55` dicen "Kurian et al., 2017".

Añadir a la lista de referencias (hoy citado en Tabla 6 pero ausente):

```
Trott, O., & Olson, A.J. (2010). AutoDock Vina: improving the speed and accuracy of docking
with a new scoring function, efficient optimization, and multithreading. *J Comput Chem*,
31(2), 455–461. PMID: 19499576.
```

Para O'Mahony 2021, Rodríguez-Pintó 2014, Tsilioni 2016 y Pacheco 2014: **resolver el PMID por
API o eliminar la referencia**. Rodríguez-Pintó 2014 es la que sostiene el mecanismo
SP→IL-8 de `preprint:153` — si no se verifica, esa frase debe caer.

**Aceptación:** correr una verificación por API sobre **todas** las referencias del preprint
y que 0 fallen. Guardar la salida como `analisis/verificacion_referencias_<fecha>.txt`.

### R4 · CA14 colapsa bajo ajuste por sexo [CRÍTICO · 2-3 h] ← **la más importante**

**Diagnóstico.** El FC=2.29 de CA14 es del mismo tamaño que el efecto sexo puro medido dentro
de los controles sanos (F/M = 2.41, p=0.034). Los grupos son 91F/5M vs 41F/52M.

```
CA14  cohorte completa: p=3.3e-04  d=+0.41  FC=2.29
      female-only:      p=0.1345   d=+0.24  FC=1.60   NO SIGNIFICATIVO
      OLS ~case+sex:    p=0.0960                       NO SIGNIFICATIVO
```

**Trabajo:**

1. Crear `scripts/validate_ukb_causal_gse221921.py` y `scripts/validate_opioid_axis_gse221921.py`
   que apliquen los **5 modelos de §2.4** (Welch FPKM, Welch log2, Mann-Whitney, OLS ~case+sex,
   female-only) a **todos** los genes de las Tablas 2 y 4. Reusar la lógica de
   `scripts/sensitivity_analysis_gse221921.py`, que ya la implementa para los 16 genes GWAS.
   El bloque `[2]` de `scripts/audit_verify_claims.py` tiene el cálculo ya hecho — cópialo.
2. Reescribir las Tablas 2 y 4 con columnas por modelo y una columna **Robustez**
   (5/5, 4/5, …), igual que la Tabla 1.
3. **Reclasificar CA14** a: *"señal confundida por sexo — no significativa en el modelo primario
   (female-only p=0.135). El fold-change observado en la cohorte completa es atribuible al
   desbalance 91F/5M vs 41F/52M; CA14 es sexo-dependiente en controles sanos (p=0.034)."*
4. **La predicción direccional Olink (CA14 ↓ en plasma FM) SE MANTIENE** — deriva de Chen 2025
   (n=29,254), no de nuestro dato de PBMC. Explicitar que se mantiene **a pesar** del colapso,
   porque es independiente. No hay que abandonar CA14: hay que dejar de presentar el mRNA de
   PBMC como pilar del triángulo.
5. Reescribir: abstract (L15), §3.4 (L181-200), §4.1 (L233), §4.2 (L241-251), Conclusión (L407),
   y `PROTOCOL_Olink...md:46` y `:256`.

**Aceptación:** `audit_verify_claims.py` sigue reportando FAIL en "CA14 sobrevive female-only"
(es la realidad) **pero** ninguna afirmación del preprint lo contradice.

### R5 · Invertir la jerarquía del preprint [CRÍTICO · 2 h] ← consecuencia de R4

El eje opioide/taquikinina es **el hallazgo real** y hoy está subordinado a CA14. Sobrevive
lo que CA14 no sobrevive:

| Gen | p cohorte | p female-only | d female-only | OLS ~case+sex |
|---|---|---|---|---|
| TACR1 | 9.9e-04 | 0.0087 | +0.59 | 0.0002 |
| OPRM1 | 4.6e-06 | **0.0001** | +0.50 | 0.0001 |
| TAC1 | 1.9e-04 | 0.0038 | +0.37 | 0.0035 |
| OPRK1 | 1.7e-03 | 0.0311 | +0.29 | 0.0371 |
| PENK | 3.2e-03 | **0.0003** | **+0.41** | 0.0095 |

**Trabajo:**
- Título y abstract giran sobre el eje opioide/taquikinina; CA14 pasa a "predicción
  direccional heredada de UKB, sin soporte transcriptómico propio tras ajuste por sexo".
- **Corregir el sub-reporte de PENK:** hoy figura como "trend" (d=+0.21). En el modelo primario
  es d=+0.41, p=0.0003 — **más fuerte que TACR1**. Debe subir a hallazgo principal.
- Declarar honestamente: bajo Bonferroni sobre las 14 pruebas del análisis female-only, solo
  **OPRM1 y PENK** sobreviven (TACR1 0.122, TAC1 0.054, OPRK1 0.435). Los *effect sizes* se
  mantienen; la pérdida es de **potencia** (41 controles mujeres), no de efecto. Decirlo así.

### R6 · Claim B: no medido ≠ no asociado [CRÍTICO · 30 min]

`preprint:29`, `:235`, `:407`. Hoy dice que IL-6, IL-8, **TAC1 y Substance P** aparecen 0 veces
y concluye que "the classical inflammatory axis is not supported at population scale".

**TAC1/Substance P nunca estuvieron en el panel Olink.** El propio repo lo dice
(`EJE_OPIOIDE_TAQUIKININA_FM.md:56`, `PROTOCOL_Olink...md:28`).

Reformular en dos afirmaciones separadas:

> (i) IL-6 y CXCL8 **sí** están cubiertos por Olink Explore 3072 y no figuran entre las
> proteínas destacadas del texto principal de Li ZY 2025 — evidencia **débil** de no-prominencia,
> no de ausencia de asociación (las 474 proteínas asociadas están en tablas suplementarias
> que no consultamos).
> (ii) TAC1 y Substance P **no están cubiertos por el panel** y por lo tanto **no son evaluables**
> con estos datos. Su ausencia del texto no aporta información.

**Tarea opcional de alto valor:** descargar la Tabla S4 de Li ZY 2025 (lista de las 2,923
proteínas) y la tabla de las 474 asociadas, y verificar de primera mano si IL6/CXCL8 están y
con qué efecto. Eso convierte un argumento débil en uno fuerte, en cualquier dirección.

### R7 · Claim D: reporte selectivo de co-expresión [MAYOR · 1 h]

`preprint:177` y `VALIDACION_GSE67311_NEGATIVA.md:72-84`.

Se reportan 5 de 10 pares — exactamente los 5 donde FM > HC. Los 4 donde HC ≥ FM se omiten.
La frase *"HC pairs consistently weaker or non-significant"* es **falsa**: en TACR1–TAC1 el HC
es **+0.420 (p<0.001)** y el FM es **+0.189 (NS)**.

**Trabajo:**
1. Publicar los **10** pares con `rho_FM`, `rho_HC` y `p` de Fisher r-to-z. El bloque `[3]`
   de `audit_verify_claims.py` ya lo calcula.
2. Reportar que **solo 1 de 10** pares difiere significativamente (TACR1–OPRK1, p=0.003).
3. Corregir *"several pairs exceeding 0.63"* → **uno**.
4. Añadir el argumento técnico: en whole blood **TAC1 está en el percentil 8, OPRK1 en p13 y
   OPRM1 en p19** de la distribución de intensidades del array (vs ACTB p99). La correlación
   entre sondas del decil inferior puede reflejar fondo compartido, no co-regulación.
5. Rebajar la conclusión a: *"un solo par de co-expresión difiere entre FM y HC; el resto no
   distingue los grupos. La interpretación de 'módulo transcripcional coherente' no está
   sostenida por los datos."*
6. Eliminar la comparación de rho entre RNA-seq FPKM y microarray RMA: son escalas distintas.

### R8 · QSP: el ΔpH es un bug [MAYOR · 1 h]

`scripts/qsp_ca14_ph_nociception.py:47-48`: `K_UNCAT_F=0.15` con `K_UNCAT_R=50.0` implica
Keq = 3.0e-3 mM, **3.8× distinto** del Keq termodinámico (7.92e-4) al que sí se calibró el par
catalítico. Al bajar `ca_rel` el Keq efectivo deriva +2.13% y **eso** produce el ΔpH=−0.009.

Con `k_uncat_r = k_uncat_f / KEQ = 189.3`: **ΔpH = +8e-7 ≈ 0 exacto.**

**Trabajo:**
1. Corregir `K_UNCAT_R = K_UNCAT_F / KEQ`.
2. Reportar el resultado real: **ΔpH = 0 exacto**, y explicar por qué es estructural — al sumar
   las dos ecuaciones de estado estacionario los términos de CA se cancelan idénticamente:
   `k_buf·h = J_co2 + J_acid − k_diff·c`.
3. Declarar que **el pH basal no está calibrado**: lo fija `J_co2/k_buf` (da 7.83/7.21/6.76
   según parámetros no medidos), mientras Henderson-Hasselbalch da 7.33 y ningún escenario
   lo reproduce.
4. **Cambiar la conclusión de "vía descartada" a "hipótesis no evaluable con este modelo".**
   Un modelo que no puede exhibir el efecto no puede refutarlo. La v1 daba ΔpH=0.000 y fue
   descartada como "defecto técnico": **la v1 tenía razón.**
5. Actualizar `SIMULACION_QSP_CA14_PH.md:10,46,55-60` y `preprint:249`.

### R9 · Código faltante para los números publicados [MAYOR · incluido en R4]

`grep -l TNFRSF1B scripts/*.py` → **0 resultados**. Ningún script produce la Tabla 4 ni los
receptores de la Tabla 2. Los números son correctos (verificados independientemente), pero
"Data & Code Availability" (`preprint:471-489`) promete una reproducibilidad que no existe.

Los scripts de R4 resuelven esto. Actualizar la sección con los archivos nuevos y añadir
`scripts/audit_verify_claims.py` como verificador.

### R10 · Borrar §3.6 (GSE269047) [MAYOR · 20 min]

`preprint:216-222` reporta p-values de `DRD2-opti_at`, `GATA2-bgrd_st`, `KIT-opti_st` y saca
una conclusión científica — y **dos párrafos después** declara que el dataset no es utilizable
porque solo contiene transcritos HERV y "los símbolos Hugo no existen en su anotación"
(`GSE269047_NO_UTILIZABLE.md:20-26`). Los sufijos `opti`/`bgrd`/`rand` son categorías de diseño
de sonda, no genes. Además la cohorte es **FM/ME-CFS mezclada**.

Borrar la sección completa. Dejar en Limitaciones:

> *Se evaluó GSE269047 como cohorte de replicación, pero la plataforma cuantifica transcritos
> HERV y no expresión génica anotada; ninguno de nuestros genes es medible en ella. El dataset
> se descartó sin extraer conclusiones (`GSE269047_NO_UTILIZABLE.md`).*

### R11 · Genes UKB: sitio anatómico ≠ FM [MAYOR · 45 min]

`preprint:43` y Tabla 4 presentan 8 genes como *"MR causal chronic pain"* aplicables a FM. En
Li ZY 2025 son **específicos de sitio**: CD302→cefalea, RARRES2→cuello/hombro, TNFRSF1B→espalda,
CD74→cadera, BTN2A1/TNFRSF9/COL18A1/TNF→abdominal, BTN2A1 y TNFRSF4→rodilla.

**Ninguno de los 5 destacados está entre los 18 causales de CWP de Chen 2025.**

**Trabajo:**
1. Renombrar a "genes causales de dolor crónico **específico de sitio anatómico**" y declarar
   que **ninguno** es causal de CWP/FM en el análisis dedicado.
2. Declarar que la **dirección plasmática de esos 5 es desconocida** — nunca la reportamos, y
   la única pista de la fuente apunta al revés: *"TNFRSF4, known as OX40… exhibits elevated
   levels in conditions associated with immune response to neural damage"*.
3. Rebajar "consistent with an immunomodulatory/exhaustion pattern" a hipótesis explícitamente
   especulativa.

### R12 · Limpieza del protocolo [MENOR · 30 min]

`PROTOCOL_Olink_FM_Biomarker_Validation.md`:
- L66 vs L216: "$2,000-3,000 **por muestra**" vs "run propio ~$5-8K, 100 muestras" — 100× de
  discrepancia. Verificar precios reales de Olink y unificar.
- L58 dice que Explore HT incluye Substance P; L76 dice que no está en Olink. Contradicción.
- L256: "UKB (n=54K)" → Chen 2025 es **n=29,254**. 54,629 es el conteo de casos del GWAS de Kerrebijn.
- L257-259: texto corrupto sin corregir — *"el machismo QSP"*, *"taquinacina"*,
  *"radioinmunocromanografía"*, *"↑ en PBMC miRNA"*, *"Bäckryd/Gröfouri"*, *"CSI opcional"*,
  *"AUX out-of-fold"*. Reescribir la sección 11 completa.
- Renombrar "pre-registro" → **"plan de análisis pre-especificado (no registrado externamente)"**,
  o registrarlo de verdad en OSF/AsPredicted y poner el enlace con timestamp.

### R13 · Nueva limitación obligatoria: medicación y edad [MAYOR · 20 min]

Verifiqué la metadata de GSE221921: **solo tiene `Sample`, `Etiology`, `Gender`.** No hay
edad, ni IMC, ni medicación (el SOFT solo añade `tissue: Blood`).

Esto es especialmente grave **para el hallazgo principal**: pacientes de FM usan opioides,
antidepresivos y pregabalina con alta frecuencia, y la exposición crónica a opioides regula
la expresión de receptores opioides. **La sobre-expresión de OPRM1/OPRK1/TACR1 en PBMC es
exactamente lo que produciría el tratamiento, no necesariamente la enfermedad.**

Añadir a Limitaciones (§5) y a la discusión del eje opioide:

> *GSE221921 no aporta datos de medicación, edad ni IMC. Dado que el uso de opioides y
> antidepresivos es frecuente en FM y que la exposición crónica a opioides modula la expresión
> de sus receptores, la elevación de OPRM1/OPRK1/TACR1 en PBMC no puede distinguirse de un
> efecto farmacológico con los datos disponibles. Cualquier cohorte de validación debe
> registrar medicación y estratificar por ella.*

Reflejar también en `PROTOCOL:119` (que ya lo contempla para el diseño futuro — bien) y
subirlo a riesgo explícito.

### R14 · Regenerar derivados [5 min]

```bash
python3 scripts/generate_numbered_preprint.py   # regenera *_numbered.md
# y regenerar los 2 PDFs
```

---

## FASE 2 — Criterio de "listo para preprint"

- [ ] Verificación por API de **todas** las referencias, 0 fallos, salida guardada
- [ ] Tablas 2 y 4 con los 5 modelos y columna Robustez
- [ ] Abstract y Conclusión no afirman nada que `audit_verify_claims.py` contradiga
- [ ] Los 10 pares de co-expresión publicados con Fisher z
- [ ] QSP con `K_UNCAT_R` corregido y conclusión "no evaluable"
- [ ] §3.6 eliminada
- [ ] Todo número publicado sale de un script commiteado
- [ ] Limitación de medicación/edad presente
- [ ] `audit_verify_claims.py` corre y su salida es coherente con el texto

Con esto el trabajo pasa de **52 → ~75 (BUENO)** sin un solo dato nuevo.

---

## FASE 3 — Experimentos siguientes (ordenados por valor / costo)

### E1 · Deconvolución real de GSE221921 [ALTA prioridad · 1 día]

`preprint:387` admite que **no** se hizo deconvolución formal en GSE221921, solo promedios de
marcadores. Es la explicación alternativa principal del hallazgo del eje opioide: si FM tiene
más monocitos o subpoblaciones T distintas, TACR1/OPRM1 suben por composición, no por regulación.

- Correr CIBERSORTx (LM22) o xCell sobre la matriz FPKM completa.
- Regresar cada gen del eje contra las fracciones celulares estimadas.
- **Criterio de éxito:** el efecto FM sobrevive el ajuste por fracciones celulares **y** por sexo.
- Si no sobrevive → el hallazgo principal es composicional. **Publicarlo igual.** Es un negativo
  informativo y hoy es un agujero declarado en las limitaciones.

### E2 · Los 18 causales de CWP (los correctos) en GSE221921 [ALTA · 3 h]

Repara el error #11 y genera datos nuevos a costo cero. El set correcto para FM/CWP no es el
de Li ZY (dolor por sitio) sino el de Chen 2025:

```
CA14, COL9A1, CRELD1, DPEP1, LEG1, LGALS3, MLN, PRSS53, TNF, BPIFB2, CTSO, DDR1,
FAM171B, IFI30, LRRC37A2, PTN, SFTPD, ST3GAL1
```

Correr los 5 modelos sobre los que sean medibles. Bonferroni sobre el set completo.
**Pregunta:** ¿alguno sobrevive el modelo female-only? Sería el reemplazo natural de CA14
como candidato transversal, y esta vez con el set génico correcto para el fenotipo correcto.

### E3 · Replicación del eje opioide en un tercer dataset PBMC [ALTA · 1-2 días]

El eje es el hallazgo real y tiene **n=1 dataset**. Buscar en GEO/ArrayExpress/SRA:
`fibromyalgia AND (PBMC OR "peripheral blood mononuclear")`. Considerar también cohortes de
dolor crónico no-FM como control de especificidad.

Si no existe otro PBMC de FM, **decirlo explícitamente en el preprint** — "no existe cohorte
independiente de PBMC de FM disponible públicamente al 2026-08" es en sí un dato útil.

`datos/geo/Neutrophils_FM_tocilizumab_trial/GSE229750_FM_HC.xlsx` ya está en el repo: mirar
si el eje es medible ahí (neutrófilos, compartimento distinto — sirve como contraste de
fracción celular, no como replicación).

### E4 · Power analysis anclado en el efecto real [MEDIA · 4 h]

El actual asume d=0.3–0.6 sin fundamento. Extraer el efecto real de CA14 de las tablas
suplementarias de Chen 2025 (beta/OR por SD de NPX) y convertirlo a d. Si el efecto real es
d≈0.15, la recomendación operativa cambia de "n=70/grupo" a "solo alcanzable por meta-análisis
o pooling multicéntrico" — que es probablemente la conclusión honesta.

Añadir corrección por multiplicidad a la simulación (hoy usa α=0.05 pelado mientras el
pre-registro corrige ×3).

### E5 · QSP v3: modelo cinético transitorio [MEDIA · 2-3 días]

Si se quiere seguir la pregunta mecanística, el modelo de estado estacionario **nunca** podrá
responderla. Lo que sí es evaluable:

- Modelo de dos compartimentos con difusión, no un pool bien mezclado.
- Simulación **transitoria**: un pulso de producción metabólica de CO2/lactato, midiendo la
  amplitud y duración del pico ácido con CA14 al 100% vs 50%.
- Hipótesis testeable: CA14↓ no cambia el pH de equilibrio pero **prolonga** las excursiones
  ácidas transitorias; ASIC responde a la **tasa** de acidificación, no solo al pH absoluto.
- **Criterio:** si el pico transitorio tampoco cruza pH 7.0, la vía periférica queda descartada
  **de verdad** — y esa sí sería una conclusión sostenible.

### E6 · Cruce pendiente D2 [BAJA · 1 h]

`PROTOCOL:137` y `:247` lo dejan abierto: cruzar las 145 proteínas diferenciales de la revisión
sistemática de FM (Gkouvi A et al., PMID 38652420) contra los 18 causales de CWP de Chen 2025.
Barato y cierra un pendiente declarado.

### E7 · Estratificación por sexo como estándar retroactivo [MEDIA · 1 día]

Aplicar los 5 modelos a **todos** los genes que la investigación haya reportado alguna vez
(cualquier documento, cualquier tabla), y publicar una tabla maestra única
`analisis/sensitivity_master_GSE221921.csv` con todos ellos.

Esto convierte el error #3 en infraestructura permanente: cualquier hallazgo futuro entra
por ahí. Después, **añadir un check a `audit_verify_claims.py`** que falle si un documento
cita un gen que no está en la tabla maestra.

---

## LO QUE NO HAY QUE HACER

- **No borres los negativos.** GSE67311, GSE269047 y el QSP son valor real. Corrige la
  interpretación, no elimines el resultado.
- **No abandones CA14.** La predicción "↓ en plasma FM" viene de n=29,254 y es independiente
  de nuestro dato de PBMC. Lo que cae es el pilar transcriptómico, no el candidato.
- **No infles el eje opioide para compensar.** Sobrevive el ajuste por sexo, pero bajo
  Bonferroni completo solo OPRM1 y PENK aguantan, y el confusor de medicación es real y no
  descartable con estos datos. Reportarlo así es lo que lo hace creíble.
- **No añadas secciones nuevas al preprint hasta reparar las viejas.** §4.6–4.9 (docking,
  QSAR, Transformer de novo) ya es material de otro paper injertado en éste; un revisor pedirá
  sacarlo. Considera separarlo en un manuscrito propio.
- **No escribas ningún PMID sin pasarlo por la API primero.** Fue el fallo que más caro salió.
