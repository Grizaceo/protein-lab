# CHANGELOG — protein-lab

## [2026-04-24] — Revisión integral V4b (Ruta B, Biosensor BFR-AuNP)

**Contexto:** Revisión end-to-end del lab de diseño de biosensor electroquímico
basado en bacterioferritina de *E. coli* (1BFR) con nanopartícula de Au
excéntrica (~150–175 átomos, r ≈ 1 nm) anclada en el lumen mediante 3 mutaciones
CYS (LEU40→CYS, VAL43→CYS, ILE49→CYS). Ruta de hopping: AuNP surface →
CYS49 SG → HIS46 NE2 → MET52 SD → Heme B FE → electrodo.

Se identificaron 11 problemas; todos fueron corregidos en esta sesión.

---

### Fix #1 — Posición errónea de CYS49 SG
**Archivo creado:** `geometry_cys_rotamer.py`

**Problema:** La aproximación `CA + v * 3.4 Å` (extensión naïve CA→CB) usada en
el cálculo previo tenía un **error posicional de ~2.0 Å** respecto a cualquier
rotámero canónico de CYS (gauche−, trans, gauche+).

**Corrección:** Se implementó cálculo explícito de los 3 rotámeros canónicos χ₁
via rotación de Rodrigues sobre el eje CA→CB, usando ángulos −60°, 180°, +60° y
longitud de enlace CB-SG = 1.810 Å, ángulo CA-CB-SG = 114.4°.

**Resultado confirmado:**
- Rotámero gauche+ (+60°): SG = [14.722, 7.977, 49.444]
- d(SG→NE2 HIS46) = 5.974 Å, d(SG→SD MET52) = 4.965 Å, d(SG→FE HEM B) = 6.444 Å
- Error de aprox. anterior confirmado = 2.0 Å (incompatible con análisis de hopping)

---

### Fix #2 — SCOPE_C_REAL_GEOMETRY.py: geometría real + tabla incertidumbre β
**Archivo modificado:** `SCOPE_C_REAL_GEOMETRY.py`

**Problema:** El script usaba la aproximación naïve CA+v*3.4 para CYS49 SG, y
reportaba solo β=1.4 (valor nominal). La incertidumbre de β (1.0–1.6 Å⁻¹ según
literatura de ET proteico) da **2 órdenes de magnitud** de variación en τ.

**Corrección:**
- Reemplazado cálculo naïve por rotámero gauche+ inline via Rodrigues
- Añadida tabla de propagación de incertidumbre β ∈ {1.0, 1.4, 1.6} para todos
  los saltos del relay

**Corrección crítica:** El paso limitante es **HIS46 NE2 → MET52 SD = 10.921 Å**
(no 9.25 Å como indicaba la versión anterior). Esto da:
- τ(β=1.4) = **437 ns** (anterior: "42 ns" — incorrecto)
- Rango τ: 5.5 ns (β=1.0) → 3.9 μs (β=1.6)

---

### Fix #3 — Corrección ΔG° por efecto cuántico de tamaño (Au NP confinada)
**Archivo creado:** `au_np_redox_correction.py`

**Problema:** El análisis de Marcus asumía ΔG°=0 (sin corrección por confinamiento
del Au NP en ε ≈ 30 del lumen proteico).

**Corrección:** Capacitancia electrostática clásica C = 4πε₀εr para Au NP (r = 10 Å)
en lumen proteico (ε = 30), corrección cuántica ΔV_QSE por nivel de Fermi discreto.

**Resultado:**
- C = 3.338×10⁻¹⁸ F
- ΔV_QSE = +24 mV (corrección por QSE)
- E°(Au NP, ε=30) ≈ +124 mV vs SHE
- ΔG°(Au NP → Heme B BFR) = **−349 meV** (EXERGÓNICO — favorable)
- La reacción favorece espontáneamente el flujo de electrones Au→Heme

---

### Fix #4 — Análisis de conservación evolutiva de ILE49, VAL43, LEU40
**Archivo creado:** `conservation_analysis.py`

**Problema:** No existía análisis de conservación evolutiva para validar que las
mutaciones a CYS en posiciones 40, 43, 49 no destruirían la estabilidad de la
cápside.

**Corrección:** Alineamiento global (Needleman-Wunsch vía BioPython PairwiseAligner)
de 1BFR contra 9 homólogos conocidos de BFR/ferritina.

**Resultado (modo offline):**
- Posición 40 (LEU): 0% identidad en homólogos, residuos alternativos = Q, M, F
- Posición 43 (VAL): 0% identidad en homólogos
- Posición 49 (ILE): 0% identidad en homólogos
- **Todas las posiciones: BAJA conservación → BAJO RIESGO para mutación a CYS**
- Nota: Para publicación se requiere ConSurf con UniRef90 (>500 homólogos)

---

### Fix #5 — Verificación de clash estérico LEU40→CYS en todos los rotámeros
**Archivo creado:** `clash_check_leu40.py`

**Problema:** No se había verificado si el rotámero de CYS40 tendría clash con
átomos de subunidades vecinas en el contexto del 24-mer.

**Corrección:** Cálculo de distancias entre SG (rotámeros gauche−, trans, gauche+)
y todos los átomos del 24-mer dentro de 5 Å; umbral de clash = distancia van der
Waals < 2.5 Å.

**Resultado — CRÍTICO:**
- gauche−(−60°): **CLASH DURO** con A37-LEU-O (d = 2.22 Å, overlap = 1.10 Å) ❌
- trans(180°): **CLASH DURO** con A32-PHE-CD2 (2.34 Å) y CE2 (2.49 Å) ❌
- **gauche+(+60°): LIBRE — sin clashes** ✓ → ÚNICO rotámero viable
- Distancias inter-SG (40↔43 = 6.98 Å, 40↔49 = 16.32 Å, 43↔49 = 12.23 Å):
  sin riesgo de puentes disulfuro espontáneos

---

### Fix #6 — Automatización de procesado de runs de Colab
**Archivo creado:** `process_colab_run.py`

**Problema:** Los resultados ZIP de Google Colab se descargaban manualmente sin
índice estructurado. Sin automatización el tracking de runs es propenso a error.

**Corrección:** Script que procesa ZIPs en `colab_runs/`, extrae metadata,
genera `INDEX.md` por run y actualiza `colab_runs/INDEX.md` consolidado.

**Resultado:** Procesados 2 ZIPs (test.result.zip → 8 entradas;
test_bmu6c.result.zip → 1 entrada); actualizados archivos INDEX.md.

---

### Fix #7 — Reemplazo de parsers PDB manuales con BioPython en audit_synapse.py
**Archivo modificado:** `audit_synapse.py`

**Problema:** Las funciones `get_coords()` y `get_center_of_mass()` usaban parsing
manual de columnas PDB con bloques `except: continue` (silencia errores de parseo,
incluyendo archivos faltantes, residuos mal formateados, etc.).

**Corrección:** Reemplazadas ambas funciones con implementaciones basadas en
`Bio.PDB.PDBParser(QUIET=True)`. La nueva implementación:
- Lanza `FileNotFoundError` si el PDB no existe (en lugar de devolver None silenciosamente)
- Itera correctamente por chain/residue/atom usando la API jerárquica de BioPython
- Suprime solo advertencias de construcción (QUIET=True), no errores reales
- Acepta residuos tanto ATOM como HETATM (HEM, etc.)

---

### Fix #8 — Optimización de SCOPE_C_HOPPING_GRAPH.py (pre-filtro de zona)
**Archivo modificado:** `SCOPE_C_HOPPING_GRAPH.py`

**Problema:** El script iteraba todos los átomos del 24-mer de BFR (~6000 átomos),
resultando en ~36M pares a evaluar (O(n²)). La ejecución era muy lenta.

**Corrección:**
- Reemplazado parser manual por `Bio.PDB.PDBParser`
- Añadido pre-filtro: **solo cadena A residuos 35–60 + cadena B completa**
  (~280 átomos vs ~6000 → reducción ~20×, mejora teórica ~400× en pares)
- Reemplazada la aproximación naïve de SG (CA+v*1.81) por rotámero gauche+ (+60°)
  via Rodrigues, consistente con Fix #1 y #2

---

### Fix #9 — Downgrade de afirmación de gating pH en SCOPE_B_PAPER_OUTLINE.md
**Archivo modificado:** `SCOPE_B_PAPER_OUTLINE.md`

**Problema:** El abstract afirmaba "relación ON/OFF modulada por pH de **100×**"
sin respaldo computacional (no se ha ejecutado APBS/Poisson-Boltzmann).

**Corrección:** Cambiada la afirmación a formulación cautelosa:
> "modulación hipotética del ET interno por pH (razón ON/OFF pendiente de
> cálculo APBS; estimación preliminar >10× basada en barrera electrostática de
> ~0.2 eV)"

También corregida **Figura 3** (eliminado "suprimido 100×" → "suprimido
(razón ON/OFF >10× estimada, cálculo APBS pendiente)").

---

### Fix #10 — Adición de filtro Rosetta DDG en PIPELINE_CLOUD_BINDER_DESIGN.md
**Archivo modificado:** `PIPELINE_CLOUD_BINDER_DESIGN.md`

**Problema:** El pipeline de diseño de binders (Nipah G / 2VSM) carecía del
filtro de estabilidad de interfaz por Rosetta DDG, requerido por literatura
reciente para alcanzar tasas de éxito experimentales razonables.

**Corrección:** Añadido **PASO 4.5** (entre AF2 y Boltz-1):
- Criterio: ΔΔG < −30 REU (~−30 kcal/mol)
- Referencia: Sappington et al., *Nat Commun* 2026, 17:1101
  (DOI: 10.1038/s41467-025-67866-3)
- Justificación: sin este filtro el éxito baja de 9.2% → ~1%
- Incluye snippet de PyRosetta para Colab académico

---

### Fix #11 — Creación de environment.yml
**Archivo creado:** `environment.yml`

**Problema:** No existía archivo de reproducibilidad del entorno conda `protein-lab`.

**Corrección:** Exportado con `conda env export --no-builds` (263 líneas).
Incluye Python 3.10.20, BioPython 1.85, fair-esm 2.0.0, colabfold 1.6.1,
openfold 2.2.0, torch 2.6.0+cu124, jax 0.6.2, entre otros.

---

## Resumen de archivos por estado

| Archivo | Tipo | Estado |
|---|---|---|
| `geometry_cys_rotamer.py` | Nuevo | ✅ Creado |
| `au_np_redox_correction.py` | Nuevo | ✅ Creado |
| `conservation_analysis.py` | Nuevo | ✅ Creado |
| `clash_check_leu40.py` | Nuevo | ✅ Creado |
| `process_colab_run.py` | Nuevo | ✅ Creado |
| `environment.yml` | Nuevo | ✅ Creado |
| `SCOPE_C_REAL_GEOMETRY.py` | Modificado | ✅ Body reemplazado |
| `SCOPE_C_HOPPING_GRAPH.py` | Modificado | ✅ Pre-filtro + BioPython + rotámero gauche+ |
| `audit_synapse.py` | Modificado | ✅ BioPython parser |
| `SCOPE_B_PAPER_OUTLINE.md` | Modificado | ✅ Afirmación pH degradada |
| `PIPELINE_CLOUD_BINDER_DESIGN.md` | Modificado | ✅ Paso 4.5 DDG añadido |
| `CHANGELOG.md` | Nuevo | ✅ Este archivo |

---

## Correcciones numéricas importantes

| Parámetro | Valor anterior (incorrecto) | Valor corregido |
|---|---|---|
| CYS49 SG position | CA + v*3.4 naïve (error ~2.0 Å) | gauche+(+60°) Rodrigues: [14.722, 7.977, 49.444] |
| d(HIS46 NE2 → MET52 SD) | ~9.25 Å | **10.921 Å** (rate-limiting) |
| τ rate-limiting (β=1.4) | "42 ns" | **437 ns** |
| τ rango (β=1.0–1.6) | no reportado | **5.5 ns → 3.9 μs** |
| ΔG°(Au NP → Heme B) | 0 (no calculado) | **−349 meV** (exergónico, favorable) |
| ON/OFF pH ratio | "100×" (sin soporte) | ">10× estimada (APBS pendiente)" |
| Rosetta DDG filtro | ausente | ΔΔG < −30 REU (Sappington 2026) |
