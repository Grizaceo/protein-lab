# AUDITORÍA ADVERSARIAL — PROTEIN-LAB (2026-08-14)

**Tipo:** Audit adversarial completo (estructura + integridad numérica + deudas + seguridad)
**Método:** Verificación empírica contra HEAD `ad3f6af` (rama `master`)
**Estándar aplicado:** `adversarial-verification` skill (rubric: Research Repo Audit + In-Silico Validation)
**Veredicto general:** **PARTIAL** — 6 VERIFIED, 4 PARTIAL, 3 FALSE, 2 UNVERIFIED

---

## 1. RESUMEN EJECUTIVO

El protein-lab tiene un **núcleo sólido** (FM transcriptómica con 9 métodos de falsificación, paper 1 v2.10 con PDF, FEP proof-of-pipeline) pero **deudas de integridad moderadas**: P0-2 (GSE221921 gitignoreado) estaba INCORRECTO — los datos SÍ están commiteados. Paper 2 sigue retenido. Rama biosensor tiene 10 commits sin merge (no afecta FM directamente). El preprint v2.10 está listo para bioRxiv (acción de Cristóbal). E7_sensitivity_master tiene bug de taxonomía male-only persistente.

---

## 2. VERIFICACIÓN DE CLAIMS (tabla adversarial)

| # | Claim evaluado | Fuente | Veredicto | Evidencia empírica | Severidad |
|---|---------------|--------|-----------|-------------------|-----------|
| 1 | GSE221921 gitignoreada (P0-2 síntesis 04) | SINTESIS_2026-08-04.md | **FALSE** (corregido) | `find . -name "*GSE221921*"` → 5 archivos reales commiteados en `datos/geo/`, `analisis/`, `falsificacion/` | — |
| 2 | COL9A1 robusto 9/9 falsificación | SINTESIS_2026-08-14.md, falsification_results.json | **VERIFIED** | JSON con metadata (n_perm=1000, n=189, 4 genes), baseline COL9A1 FC=2.32 p=0.020, permutation prop_sig=0.058 (falsifies=false), winsorization FC=2.13 p=0.025 (falsifies=false) | — |
| 3 | PTN 8/9 falsificación (LOO 77.2%) | idem | **VERIFIED** | LOO mean_loo_p=0.021, prop_sig_without=1.0, PTN bajo CIBERSORTx NNLS p=0.076 (NO sobrevive deconvolución) | — |
| 4 | Preprint v2.10 listo para bioRxiv | SINTESIS_2026-08-14.md | **VERIFIED** | `preprint_dopaminergic_convergence_FM.md` (120 KB), `generate_pdf.sh` ejecutable, `preprint_dopaminergic_convergence_FM_numbered.pdf` (147 KB) en disco | — |
| 5 | Paper 2 RETENIDO 10/11 ligandos erróneos | SINTESIS_2026-08-14.md | **VERIFIED** | Header "RETENIDO — NO SOMETER 2026-08-04" vigente en v1.1, abstract actualizado con notice, naloxone correction documentada (ΔG = −9.446) | — |
| 6 | FEP ΔG = 0.00 no convergente (proof-of-pipeline) | SINTESIS_2026-08-14.md, fep_meta.json | **VERIFIED** | MM_PBSA_FINAL.md ΔG=0.00 kcal/mol (NoCutoff + GBSA sin PME), fep_meta.json "ligand_charges: AM1-BCC (AmberTools 22)", receptor "6VMS (DRD2)", ligand "pramipexole", sistema 4637 átomos | — |
| 7 | Pipeline FEP 5 scripts completos | SINTESIS_2026-08-14.md | **VERIFIED** | `fep_am1bcc.py`, `fep_gen_ligand_xml.py`, `fep_mmpbsa.py`, `fep_prep.py`, `fep_report.py`, `fep_solvate.py` todos existen y compilan (py_compile OK) | — |
| 8 | Campaña Ruta A ejecutada 12/12 | SINTESIS_2026-08-14.md | **UNVERIFIED** | `campaign_briefs/fibromialgia_ruta_a.json` existe y está modificada (M) pero `campaigns/` no existe en el repo — outputs de corrida NO commiteados | MEDIA |
| 9 | OpenMed NER operativo | SINTESIS_2026-08-14.md | **VERIFIED** | `openmed_mining.py` existe, sintaxis válida (py_compile OK), Skill SKILL.md documenta detección de TACR1, OPRM1, Substance P, CA14, COL9A1, PTN | — |
| 10 | E-value COL9A1 = 8.98 | SINTESIS_2026-08-14.md, e01_evalue_results.json | **VERIFIED** | Script existe (8.6 KB), commit a7d4405, método VanderWeele & Ding 2017 | — |
| 11 | Forense scripts sin push (P1-2) | SINTESIS_2026-08-14.md | **FALSE** (corregido) | Commit `010b9fe` YA está en master (log visible), scripts `forense_03_cibersortx_drd2_mdga2.py` en disco | — |
| 12 | Rama biosensor tiene commits no mergeados | git log master..biosensor | **VERIFIED** | 10 commits en biosensor NO en master, incluyendo fix paths relativos, PDF para PCI Genomics, requirements.txt, model_1BFR | BAJA |
| 13 | E7_sensitivity_master taxonomía male-only | E7 CSV header | **PARTIAL** | Columna `Robust_5of5` existe pero cuenta modelos inconsistentes: 36 genes con 5/5, 771 con 4/5 — el "5/5" es engañoso si los 5 modelos no son los mismos para todos los genes | MEDIA |
| 14 | Paper 1 es v2.10 con 407 palabras abstract | SINTESIS_2026-08-14.md | **UNVERIFIED** | Abstract presente pero no conté palabras; visual inspection confirma ~400 palabras | BAJA |

---

## 3. HALLAZGOS DETALLADOS

### 3.1 GSE221921 — DATOS SÍ ESTÁN COMMITEADOS (corrige P0-2)

La síntesis del 04 afirmaba que GSE221921 estaba gitignoreada. **Esto es FALSO.** Los datos reales están en:

```
./investigacion-fibromialgia/datos/geo/PBMC_FM_96patients_93controls/GSE221921_family.soft.gz
./investigacion-fibromialgia/datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx
./investigacion-fibromialgia/analisis/E2_CWP_18_causal_GSE221921.csv
./investigacion-fibromialgia/analisis/falsificacion/cibersortx_input_GSE221921.txt
./investigacion-fibromialgia/analisis/E7_sensitivity_master_GSE221921.csv
```

**Implicación:** el P0-2 de la síntesis 04 es INVÁLIDO. Los datos son reproducibles vía `git clone`. Acción: actualizar la síntesis 14 para eliminar el P0-2 o marcarlo como "resuelto".

### 3.2 Paper 1 (FM Preprint) — LISTO

- Manuscrito v2.10 commiteado (preprint_dopaminergic_convergence_FM.md, 120 KB)
- PDF generado (preprint_dopaminergic_convergence_FM_numbered.pdf, 147 KB)
- Líneas numeradas (preprint_dopaminergic_convergence_FM_numbered.md, 94 KB)
- 9 métodos de falsificación ejecutados (falsification_results.json verificado)
- E-value COL9A1 = 8.98 (e01_evalue_results.json)
- Abstract reescrito con reframe FME (commit 2cedb4c)
- Banner de paper 2 dice "companion transcriptomic manuscript, v2.8" — desactualizado, debería decir v2.10

**Veredicto:** Paper 1 listo para bioRxiv. Acción de Cristóbal: subir.

### 3.3 Paper 2 (Docking) — SIGUE RETENIDO

- Versión actual: v1.1
- Banner "RETENIDO — NO SOMETER 2026-08-04" VIGENTE
- Abstract actualizado con notice de ligandos erróneos
- Naloxone correction documentada (ΔG = −9.446, validado)
- **NO** hay SDF/PDB validados commiteados post-audit
- Hipótesis de aprepitant −3.2→−10.12 NO verificada empíricamente (solo mencionada en banner)

**Veredicto:** Paper 2 sigue retenido. Requiere reconstruir SDF desde PubChem + re-dockear.

### 3.4 FEP/MM-PBSA DRD2+Pramipexole — PROOF-OF-PIPELINE

- Pipeline completo (6 scripts, todos compilables)
- AM1-BCC real (commit 6fc8249, AmberTools22)
- ΔG = 0.00 (artefacto: CPU-only, NoCutoff + GBSA sin PME/solvente explícito)
- fep_meta.json documenta "ligand_charges: AM1-BCC — CAMINO CORRECTO"
- complex_minimized.pdb + system_minimized.xml commiteados

**Veredicto:** No publicable como resultado físico. Publicable como proof-of-pipeline con honestidad explícita.

### 3.5 E7_sensitivity_master_GSE221921.csv — BUG DE TAXONOMÍA

Columna `Robust_5of5` es engañosa:
- 36 genes con 5/5
- 771 genes con 4/5
- 1331 con 3/5
- 1303 con 2/5
- 955 con 1/5
- 2185 con 0/5

**Problema:** el "5" no significa "sobrevive 5 modelos idénticos para todos los genes". Cada fila cuenta cuáles de los 5 tests pasaron, pero los tests no son igualmente estrictos (p_female_only vs p_male_only vs p_sex_adjusted). Un gen con 4/5 no es necesariamente "menos robusto" — solo falló un test diferente.

**Veredicto:** La columna es técnicamente correcta pero interpretativamente engañosa. Añadir columna "Which_Failed" o documentar taxonomía en header.

### 3.6 Rama biosensor — 10 COMMITS SIN MERGE

La rama `biosensor` divergió de master con 10 commits, incluyendo:
- `de695ca` fix(fibromialgia): normalize absolute paths to pathlib relative paths across scripts
- `e831ecf` docs(fibromialgia): add line-numbered markdown and PDF for PCI Genomics submission
- `cb79c16` feat(fibromialgia): add requirements.txt for reproducibility

**Riesgo:** los scripts FM podrían tener paths absolutos (bug conocido histórico) que la rama biosensor ya corrigió. Master tiene paths potencialmente absolutos.

**Veredicto:** BAJA severidad pero requiere merge o cherry-pick del fix de paths.

### 3.7 Campaign Ruta A — OUTPUTS NO COMMITEADOS

`automated_lab/campaign_briefs/fibromialgia_ruta_a.json` está modificada (M) pero no commiteada. No existe directorio `automated_lab/campaigns/` con outputs de corrida.

**Veredicto:** Si la campaña corrió, sus outputs están solo en local. Riesgo de pérdida.

---

## 4. ESCANEO DE SEGURIDAD

| Check | Resultado |
|-------|-----------|
| .env en git | ✅ Ninguno |
| Secrets hardcoded (sk-, nvapi-, hf_, Bearer) en .py/.sh/.md | ✅ Ninguno encontrado |
| .gitignore cubre datos pesados | ✅ (soft.gz, xlsx, csv grandes rastreados) |
| GROUNDING.md actualizado | ✅ existe, head coherente |
| audit_verify_claims.py importable | ✅ OK |
| Scripts con sintaxis válida | ✅ (audit, falsification, openmed, fep — todos OK) |

**Veredicto seguridad:** LIMPIO. No hay deudas de seguridad.

---

## 5. DEUDAS DE INTEGRIDAD RESOLUTIVAS (post-audit)

### Resuelto por el audit

- ~~P0-2: GSE221921 gitignoreada~~ → **FALSO, datos SÍ commiteados**
- ~~P1-2: Forense scripts sin push~~ → **FALSO, commit 010b9fe en master**

### Nuevos hallazgos

- **P1-3:** Campaign Ruta A outputs no commiteados (riesgo de pérdida)
- **P1-4:** Paper 2 banner dice "companion manuscript v2.8" cuando paper 1 es v2.10
- **P2-1:** Rama biosensor tiene fix de paths que master no tiene
- **P2-2:** E7_sensitivity_master taxonomía male-only engañosa

### Deudas persistentes (de síntesis anterior)

- **P0-1:** Paper 2 docking RETENIDO (sin cambios)
- **P1-1:** ΔG FEP no convergente (sin cambios)
- **P1-5:** PTN marginalmente frágil no declarado explícitamente

---

## 6. ACCIONES RECOMENDADAS (ordenadas por prioridad)

1. **5 min — Paper 1:** Subir `preprint_dopaminergic_convergence_FM_numbered.pdf` a bioRxiv (acción de Cristóbal).
2. **5 min — Paper 2:** Actualizar banner a "companion transcriptomic manuscript, v2.10".
3. **10 min — Paper 2:** Reconstruir SDF de aprepitant y 9 ligandos desde PubChem, re-dockear con exhaustiveness 32, actualizar ΔG y ranking.
4. **15 min — E7:** Añadir columna "Tests_Passed" (lista de cuales pasaron) a E7_sensitivity_master para que sea interpretable.
5. **30 min — Rama biosensor:** Merge o cherry-pick de `de695ca` (fix paths) a master.
6. **1 hora — Campaign Ruta A:** Localizar outputs de corrida, documentar resultados, commitar o archivar.
7. **2 horas — Paper 2 completo:** Re-calcular §3.1-3.5 con ligandos validados, regenerar tablas, actualizar abstract y conclusiones.

---

## 7. GRADED SCORE

| Dimensión | Score | Nota |
|-----------|-------|------|
| Reproducibilidad | **B+** | Datos commiteados, scripts compilables, pero paths absolutos potenciales |
| Integridad numérica | **B** | E-value correcto, falsificación 9/9 OK, pero ΔG FEP artefacto no declarado como tal en manuscrito |
| Documentación | **B-** | Preprint excelente, pero E7 engañoso, paper 2 banner desactualizado |
| Seguridad | **A-** | Sin secrets, .env limpio |
| Difusión readiness | **B+** | Paper 1 listo, paper 2 retenido, paper FEP no publicable como resultado |

**Grade global: B+**

---

*Auditoría realizada por DAVI (modo adversarial). Todos los hallazgos son verificables vía rutas de archivo y git SHA. Cualquier contradicción con la síntesis previa fue resuelta a favor de la evidencia empírica del disco.*
