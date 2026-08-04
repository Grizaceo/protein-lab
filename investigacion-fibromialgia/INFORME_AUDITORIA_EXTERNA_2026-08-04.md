# INFORME DE AUDITORÍA EXTERNA — Investigación Fibromialgia

**Fecha:** 2026-08-04
**Versión:** 2.0 (reemplaza la v1.0 del mismo día — ver §0.1)
**Destinatario:** auditor externo (LLM o humano) con acceso read-only al repositorio
**Repositorio:** `https://github.com/Grizaceo/protein-lab`
**Rama auditada:** `fm/e1b-deconvolution-col9a1-ptn`
**SHA auditado:** `ef4c6e47e69c182ce785df815fb964a0c8d6c370`
**Directorio local:** `~/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/`

---

## 0. PROPÓSITO

Este documento permite a un auditor externo reconstruir el estado de la investigación FM y verificarlo por sí mismo, sin depender de la memoria de nadie. Contiene: qué se afirma, dónde vive la evidencia, qué comandos la reproducen, y qué falla.

### 0.1 Por qué esta es la versión 2.0

La v1.0 de este informe (commit `a48c25f`) tenía defectos que la hacían inservible para su propósito. Se documentan porque un auditor los encontrará en el historial de git:

| Defecto v1.0 | Realidad |
|---|---|
| El bloque de reproducción §4.3 usaba `sheet_name=0` y declaraba "genes en columnas, samples en filas", con FM en las filas 0–95 | `sheet_name=0` es `Metadata (Genes)`, una hoja-leyenda de 7×2. La estructura real es la inversa (genes en filas, muestras en columnas) y el grupo viene de la hoja `Metadata (Samples)`, no de la posición. **El bloque lanzaba `KeyError`; quien lo "arreglara" por posición habría obtenido números falsos** |
| "El repositorio contiene todos los scripts, matrices, verificadores" | La matriz primaria está **gitignoreada** (§2.2) |
| Ruta `analisis/default` | `analisis/verificacion_referencias_2026-08-04.txt` |
| Ruta `fuentes_verifues/` | `fuentes_verificadas/` |
| "52/110" en §5 vs "52/100" en §0 | La auditoría base fue **52/100** (`AUDITORIA_EXTERNA_2026-08-03.md:13`) |
| Varios pasajes corruptos e ilegibles | — |
| Declaraba el eje opioide "robusto" con ✅ en el checklist | El eje **no sobrevive** el ajuste por composición celular (§4.2). El caveat estaba mencionado en una línea y contradicho en la tabla de la línea siguiente |

Ninguno de estos defectos afectaba los datos ni los scripts, solo este documento.

---

## 1. QUÉ SE AFIRMA

Tres afirmaciones sustantivas, en orden de solidez.

### 1.1 COL9A1–PTN es el hallazgo principal — sobrevive los tres confusores

Módulo matriz-extracelular / crecimiento neurítico, derivado del cruce entre GSE221921 y los 18 causales de dolor crónico generalizado de Chen 2025.

| gen | FC arit. | FC geom. | d (FPKM) | d (log₂) | modelos 1–5 | ajuste composicional |
|---|---|---|---|---|---|---|
| COL9A1 | 2.32 | 1.72 | +0.88 | +0.86 | **5/5** | **p = 0.012–0.020** |
| PTN | 2.91 | 1.33 | +0.61 | +0.72 | **5/5** | **p = 0.028–0.046** |

Es el **único** módulo del panel que sobrevive simultáneamente: estratificación por sexo, corrección de Bonferroni sobre el modelo ajustado por sexo, y ajuste por composición celular — este último en las cuatro implementaciones de deconvolución probadas. PTN queda marginal bajo fracciones NNLS (p = 0.046) y se reporta como tal.

Ambas proteínas son secretadas y detectables en plasma por Olink. Son los objetivos primarios de validación.

### 1.2 El eje opioide/taquikinina está elevado, pero es composicional

| gen | FC arit. | FC geom. | d (FPKM) | modelos 1–5 | ajuste composicional |
|---|---|---|---|---|---|
| TACR1 | 2.73 | 1.21 | +0.60 | 5/5 | 0.039–0.117 |
| OPRM1 | 2.28 | 1.61 | +0.53 | 5/5 | 0.030–0.080 |
| TAC1 | 2.10 | 1.31 | +0.47 | 5/5 | 0.080–0.393 |
| OPRK1 | 1.78 | 1.13 | +0.38 | 4/5 | 0.796–0.836 |

Es el bloque de mayor tamaño de efecto y sobrevive los cinco modelos de sensibilidad por sexo. **Ningún gen del eje sobrevive el ajuste por composición celular en las cuatro implementaciones.** La elevación refleja un cambio en qué leucocitos circulan, no regulación transcripcional por célula.

Dos confusores no separables con estos datos: el uso crónico de opioides en FM regula la expresión de sus propios receptores, y puede además alterar la composición celular.

**Control negativo que hace interpretable este resultado:** de 600 genes al azar (marcadores excluidos), 273 tenían efecto de grupo tras ajustar por sexo y **76 (28 %) sobrevivieron el ajuste composicional**. El ajuste elimina ~72 % de los efectos pero deja pasar una minoría sustancial — morir es informativo y sobrevivir también.

### 1.3 CA14 — degradado a referencia direccional

1. Plasma: ↓ en dolor crónico generalizado (Chen 2025, n = 29 254); MR indica que la elevación genética es protectora.
2. PBMC mRNA: FC = 2.29 sin ajustar, pero **colapsa female-only** (p = 0.135). Dentro de controles sanos, la razón mujeres/hombres es 2.41 — del mismo tamaño que el "efecto FM" reportado. Confusor estructural.
3. Farmacología: sulthiame es **inhibidor**; el paper original propone **agonistas**. Dirección inversa.

Predicción testable: CA14 ↓ en plasma FM. Dirección de reposicionamiento: agonismo.

---

## 2. CÓMO REPRODUCIR

### 2.1 Entorno

Python 3.10; `pandas`, `numpy`, `scipy`, `statsmodels`, `openpyxl`.

### 2.2 Los datos primarios NO están en el repositorio

`datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx` (60 MB) está **gitignoreado** (`.gitignore:2`). Es la fuente de prácticamente todos los números de §1. Diez scripts dependen de él, incluido el verificador.

**Un `git clone` no puede reproducir nada hasta descargarlo.** Instrucciones en `README.md`, sección *Data Download*:

```
1. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE221921
2. Descargar GSE221921_FM_ProcessedData.xlsx (archivo suplementario)
3. Colocarlo en datos/geo/PBMC_FM_96patients_93controls/
```

GSE67311 sí está incluido (`datos/geo/GSE67311/`).

### 2.3 Verificador de claims numéricos — 46 s

```bash
python3 scripts/audit_verify_claims.py
```

Salida esperada: **3/11 PASS**. Los 8 FAIL son hallazgos genuinos, no bugs — documentan el confusor de sexo en CA14, el reporte selectivo de co-expresión, las sondas del eje cerca del fondo en whole blood, y tres fallas del modelo QSP. `PLAN_REPARACION.md` es explícito: *"el texto debe ser consistente con estos FAIL, no forzarlos a PASS"*.

Un auditor debe confirmar que el manuscrito **reconoce** cada FAIL. Lo hace: nota de corrección por reporte selectivo (§3.3), caveat de percentil de fondo (§3.3), retracción del QSP a "hipótesis no evaluable" (§4.2).

### 2.4 Ajuste por composición celular — 48 s

```bash
python3 scripts/e1_deconvolution_adjusted_model.py
```

Cuatro bloques: validación contra E1, resultado COL9A1/PTN, control negativo de 600 genes, y barrido de cuatro implementaciones con VIF. Salidas en `analisis/E1b_*.csv`.

### 2.5 Recálculo independiente desde la matriz cruda

Este bloque es autónomo — no usa código del repositorio, para que el auditor no dependa de él:

```python
import pandas as pd, numpy as np
from scipy.stats import mannwhitneyu

X = "datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx"
xls = pd.ExcelFile(X)   # hojas: Metadata (Genes) | Metadata (Samples) | Values (FPKM)
ms  = pd.read_excel(xls, 'Metadata (Samples)')   # columnas: Sample | Etiology | Gender
v   = pd.read_excel(xls, 'Values (FPKM)')        # genes en FILAS, muestras en COLUMNAS

# El grupo viene de Etiology, NO de la posición de la fila
# (las primeras filas del archivo son Control, no FM)
fm = [s for s, e in zip(ms['Sample'], ms['Etiology']) if e == 'Fibromyalgia']  # n=96
hc = [s for s, e in zip(ms['Sample'], ms['Etiology']) if e == 'Control']       # n=93

def cohen_d(a, b):
    sp = np.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1)) / (len(a)+len(b)-2))
    return (a.mean() - b.mean()) / sp

for g in ['TACR1', 'OPRM1', 'TAC1', 'OPRK1', 'CA14', 'COL9A1', 'PTN']:
    r = v[v['Hugo_Gene_Symbol'].astype(str).str.upper() == g].iloc[0]
    A = pd.to_numeric(r[fm], errors='coerce').dropna().values
    B = pd.to_numeric(r[hc], errors='coerce').dropna().values
    print(f"{g}: FC_arit={A.mean()/B.mean():.3f}  "
          f"FC_geom={2**(np.log2(A+1).mean()-np.log2(B+1).mean()):.2f}  "
          f"d={cohen_d(A,B):+.2f}  p={mannwhitneyu(A,B,alternative='two-sided')[1]:.2e}")
```

Debe devolver TACR1 FC_arit = 2.731 / d = +0.60, COL9A1 d = +0.88, CA14 FC_arit = 2.292 — coincidiendo con las Tablas 2 y 4.

### 2.6 Referencias

```bash
cat analisis/verificacion_referencias_2026-08-04.txt
```

27 PMIDs verificados contra la API de PubMed, 0 errores. El preprint cita **exactamente 27 PMIDs distintos**, de modo que la cobertura es del 100 %, no una submuestra. Re-verificación puntual:

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=41025730&retmode=json" \
  | python3 -m json.tool
```

### 2.7 Citas textuales de Chen 2025

`fuentes_verificadas/PMC12713070_Chen2025_AdvSci_CWP_proteogenomic.xml` (texto completo, 140 KB). Palabras clave para verificar la dirección de CA14: `CA14`, `sulthiame`, `agonists`.

### 2.8 Historial

```bash
git log --oneline -25 -- investigacion-fibromialgia/
git log --follow -- investigacion-fibromialgia/preprint_dopaminergic_convergence_FM.md
```

Lineal desde `16893ef`. Sin rebase ni force-push.

---

## 3. ESTRUCTURA REAL DEL REPOSITORIO

```
investigacion-fibromialgia/                       365 archivos trackeados
├── preprint_dopaminergic_convergence_FM.md       MANUSCRITO FUENTE (v2.8)
├── preprint_dopaminergic_convergence_FM_numbered.md   versión con líneas numeradas
├── scripts/                                      43 scripts
│   ├── audit_verify_claims.py                    verificador ejecutable (11 checks)
│   ├── e1_deconvolution_adjusted_model.py        ajuste composicional + control negativo
│   ├── sensitivity_analysis_gse221921.py         5 modelos × 16 genes
│   ├── deconvolution_cell_types.py               fracciones celulares por marcadores
│   ├── validate_opioid_axis_gse67311.py          eje opioide en whole blood
│   └── generate_numbered_preprint.py
├── analisis/                                     79 archivos
│   ├── verificacion_referencias_2026-08-04.txt   27 PMIDs verificados por API
│   ├── E1_deconvolution_opioid_axis.csv          E1 original (sin código — ver §5.1)
│   ├── E1b_DECONVOLUCION_COL9A1_PTN.md           resultado + interpretación
│   ├── E1b_variant_sweep.csv                     4 implementaciones
│   ├── E1b_negative_control_random_genes.csv     600 genes al azar
│   ├── E7_sensitivity_master_GSE221921.csv       conjunto alternativo — NO usado (§5.2)
│   ├── COL9A1_DEEP_DIVE_VEREDICTO.md             módulo COL9A1-PTN (C1-C5)
│   └── REVISION_ADVERSARIAL_2026-08-04.md        3 issues corregidos
├── datos/geo/
│   ├── PBMC_FM_96patients_93controls/            GSE221921 — matriz GITIGNOREADA
│   ├── GSE67311/                                 whole blood, incluido
│   └── Neutrophils_FM_tocilizumab_trial/         GSE229750
├── fuentes_verificadas/                          texto completo Chen 2025
├── estructuras/alphafold/                        PDBs + PDBQTs
├── docking_fm_targets/docking_FM_targets_GPCR.md PAPER 2 (spin-off, v1.0)
├── AUDITORIA_EXTERNA_2026-08-03.md               auditoría base — 52/100
├── PLAN_REPARACION.md / BITACORA_REPARACION.md   plan y ejecución R1-R14
├── VALIDACION_GSE67311_NEGATIVA.md               reporte negativo
└── README.md                                     incluye instrucciones de descarga
```

---

## 4. LO QUE UN AUDITOR DEBE ENCONTRAR

### 4.1 Verificable y correcto

| Dimensión | Comando | Resultado |
|---|---|---|
| Números de Tablas 2 y 4 | `audit_verify_claims.py` bloque [1] | 16/16 exactos al milésimo |
| Co-expresión PBMC | bloque [1] | 5/5 exacta |
| Eje opioide sobrevive ajuste por sexo | bloque [2] | female-only + OLS, 2/2 |
| CA14 colapsa female-only | bloque [2] | p = 0.135; ratio F/M = 2.41 en controles |
| COL9A1/PTN sobreviven composición | `e1_deconvolution_adjusted_model.py` | 4/4 implementaciones |
| Control negativo | mismo script, bloque [3] | 28 % de 273 genes |
| Referencias | `analisis/verificacion_referencias_2026-08-04.txt` | 27/27, cobertura 100 % |
| Negativos reportados sin cosmética | `VALIDACION_GSE67311_NEGATIVA.md`, limitación 3 | sí |
| Paper 2 autocontenido | `docking_fm_targets/docking_FM_targets_GPCR.md` | v1.0, con límites de Vina/AlphaFold declarados |

### 4.2 Lo que el auditor debe confirmar que el manuscrito NO afirma

El manuscrito **no** debe decir que el eje opioide es el hallazgo más robusto, ni que el circuito SP→NK1 está sensibilizado, ni que la elevación de OPRM1/OPRK1 es activación compensatoria del sistema opioide endógeno. Esas afirmaciones estuvieron en versiones ≤ 2.7 y fueron retiradas en la v2.8 porque el ajuste composicional no las soporta.

---

## 5. HALLAZGOS DE INTEGRIDAD (auditoría interna, 2026-08-04)

Se registran porque un auditor externo debe poder verificarlos y porque afectan cómo leer el historial.

### 5.1 E1 se publicó sin código

El commit `03b4609` ("exp: E1 — deconvolucion eje opioide GSE221921") añadió **únicamente** `analisis/E1_deconvolution_opioid_axis.csv`. Ningún commit del repositorio contenía código que produjera sus columnas. El resultado más adverso de la investigación era irreproducible durante ~15 horas.

Reparado en `e9ceded`: `scripts/e1_deconvolution_adjusted_model.py` reconstruye la metodología y **la valida — la variante NNLS reproduce E1 con 7/7 veredictos idénticos**. El hallazgo de E1 era correcto; solo faltaba el código.

Consecuencia adicional: la limitación 3 del manuscrito atribuía confusores específicos por gen (NK para OPRM1, neutrófilos para TACR1, Tregs para TAC1). Esas atribuciones **no replican entre implementaciones** y fueron retiradas en la v2.8. La conclusión de que hay confusión composicional sí es robusta; la de qué tipo celular la causa, no.

### 5.2 Dos definiciones incompatibles de "los cinco modelos"

El repositorio contenía dos conjuntos distintos, ambos etiquetados "5/5":

- **§2.4 del manuscrito:** Welch FPKM, Welch log₂, Mann-Whitney, OLS `case+sex`, female-only.
- **`E7_sensitivity_master_GSE221921.csv`:** sustituye Welch log₂ por un estrato **male-only**.

El estrato male-only contiene **5 pacientes FM**. Ningún gen del panel lo pasa, incluidos genes inequívocamente significativos bajo todos los demás modelos. No puede funcionar como criterio de robustez.

La limitación 12 (commit `5d85382`) había rescorado COL9A1/PTN a "Robust 4/5" usando silenciosamente el conjunto E7, mientras el abstract seguía usando el conjunto §2.4. Resuelto en la v2.8: §2.4 distingue explícitamente ambos conjuntos, E7 se declara no usado para puntuar, y se añade la limitación 12b. Bajo la definición del manuscrito, verificado gen por gen:

| | modelos 1–5 |
|---|---|
| MDGA2, DRD2, TACR1, OPRM1, TAC1, COL9A1, PTN | 5/5 |
| OPRK1 | 4/5 (female-only p = 0.056) |
| CAMKV, CELF4 | 4/5 (falla OLS sex-adj) |
| CA14 | 3/5 |

### 5.3 Los fold-changes eran razón de medias aritméticas

Sobre FPKM de cola pesada — el propio §2.3 declara que Shapiro-Wilk rechaza normalidad en todos los genes y ambos grupos — la razón de medias aritméticas sobreestima el cambio típico hasta ~2×:

| gen | FC aritmético (publicado ≤ v2.7) | FC geométrico |
|---|---|---|
| TACR1 | 2.73 | 1.21 |
| PTN | 2.91 | 1.33 |
| CA14 | 2.29 | 1.32 |
| COL9A1 | 2.32 | 1.72 |
| TNFRSF9 | 1.46 | 1.07 (p rank = 0.805) |

Las **d de Cohen son estables o mayores bajo log₂**, de modo que los efectos no son artefactos de outliers — pero los titulares de fold-change sí estaban inflados. La v2.8 reporta ambas columnas en las Tablas 2 y 4.

---

## 6. LIMITACIONES DECLARADAS

Las 13 limitaciones viven en §5 del manuscrito. Las que más pesan:

1. **Composición celular** (lim. 3). Las fracciones son estimadas por marcadores sobre la misma matriz, no medidas por citometría; ajustar por covariables derivadas del mismo dato arriesga sobreajuste. El control negativo acota ese riesgo, no lo elimina.
2. **Medicación** (lim. 10). Los metadatos de GSE221921 contienen solo `Sample`, `Etiology`, `Gender`. Sin edad, IMC ni fármacos. El eje opioide no puede distinguirse de un efecto farmacológico.
3. **FPKM, no conteos** (lim. 2). DESeq2/edgeR sería preferible; los conteos crudos no están en GEO.
4. **Sin réplica independiente** (lim. 9b). Una búsqueda sistemática en GEO (18 series FM) encontró solo dos datasets de sangre periférica: GSE221921 y GSE67311. No existe un tercer dataset PBMC público.
5. **No replica en whole blood** (lim. 6). Los proxies derivados de PBMC no replican en GSE67311, y las sondas del eje están en el decil inferior de intensidad del array.
6. **mRNA ≠ proteína** (lim. 7). Todo el trabajo es computacional; no hubo experimentos húmedos.

---

## 7. ESTADO

**Manuscrito principal:** v2.8, local, no subido a preprint server.
**Paper 2 (docking):** v1.0, autocontenido, no subido.
**Validación experimental:** ninguna. `PROTOCOL_Olink_FM_Biomarker_Validation.md` especifica el diseño (75 FM + 75 HC, 88 % de potencia en el escenario moderado de atenuación mRNA→proteína).

### Pendientes reales

1. Someter a bioRxiv/medRxiv.
2. Ejecutar la validación Olink en plasma — COL9A1 y PTN como analitos primarios, CA14 como referencia direccional.
3. Para el eje opioide, el seguimiento correcto es citometría de flujo o scRNA-seq, no transcriptómica bulk ni plasma: si el fenómeno es composicional, hay que medir composición.
4. Deconvolucionar DRD2 en el mismo marco (no se hizo).

---

## 8. QUÉ NO AFIRMA ESTE INFORME

No asigna un puntaje. La auditoría base del 2026-08-03 dio **52/100** (umbral publicable ≥ 70) y este documento describe qué cambió desde entonces, pero la calificación le corresponde al auditor externo, no a los autores.

Tampoco afirma que el trabajo esté libre de errores. Los tres hallazgos de §5 se encontraron **después** de que la v1.0 de este mismo informe declarara el trabajo "LISTO". Esa declaración era prematura y se retira.

---

*Repositorio auditable en `ef4c6e4`. Todo lo afirmado aquí tiene archivo o comando asociado.*
