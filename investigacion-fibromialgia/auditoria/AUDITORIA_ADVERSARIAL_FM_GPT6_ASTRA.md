# AUDITORÍA ADVERSARIAL — FIBROMIALGIA / CONVERGENCIA DOPAMINÉRGICA

**Fecha:** 2026-09-06
**Modelo auditor:** DAVI (gpt-6-astra vía ChatGPT/Codex Subscription)
**Alcance:** Solo lectura, sin nuevos experimentos ni mutaciones de archivos.
**Manuscritos auditados:**
- Paper 1 (Principal): `investigacion-fibromialgia/preprint_dopaminergic_convergence_FM.md` — Draft v2.14, agosto 2026.
- Paper 2 (Docking): `investigacion-fibromialgia/docking_fm_targets/docking_FM_targets_GPCR.md` — Draft v1.2, agosto 2026.
- Evidencia: `analisis/*.json`, `sensitivity_analysis_*.csv`, `E1b_variant_sweep.csv`, `falsification_results.json`, `e01_evalue_results.json`, `e02_evalue_ptn_results.json`, `ichor-fme-exercise-responder-grounding-v2.json`, `rubrics/protein-lab.json`.
- GROUNDING: `GROUNDING.md`.

---

## A. HALLAZGO CRÍTICO #1 — REFERENCIAS BIBLIOGRÁFICAS FALSAS (12 PMIDs)

**Severidad:** FATAL para cualquier sumisión. Bloquea bioRxiv, PCI y revistas.

Verificación de 59 PMIDs contra PubMed E-utilities (batch 2026-09-06).
12 PMIDs están mapeados a artículos completamente ajenos al tema citado:

| PMID citado | Título real en PubMed | Tema citado en manuscrito | Línea Paper 1 |
|-------------|----------------------|---------------------------|---------------|
| 32251800 | "Cutaneous tuberculosis" | Davis 2020 biomarkers review | ~728 |
| 37427244 | "Urinary bladder metastasis..." | Pain biomarkers in FM | ~730 |
| 39674732 | Ajeno a FM/SP/mast cells | Findeisen 2025 (SP/mast) | ~750 |
| 39135076 | Ajeno a FM/enkephalins | García-Domínguez 2024 | ~748 |
| 30797693 | Ajeno a SFPN/FM | Grayston 2019 SFPN review | ~766 |
| 39511971 | Ajeno a FM/neuroinflammation | Littlejohn & Guymer 2018 | ~746 |
| 39525179 | Ajeno a FM/neuroinflammation | Theoharides 2019 | ~750 |
| 37371737 | Ajeno a multi-omics FM | Bonomi 2025 / Favretti 2025 | ~756 |
| 31031621 | Ajeno a FM/pathophysiology | Aitella 2026 | ~750 |
| 19130090 | Ajeno a exercise/FM/analgesia | Sluka 2018 / Bruehl 2020 | ~773 |
| 39840902 | Ajeno a exercise/FM | Nijs 2015 / Belviranlı 2024 | ~769 |
| 40747659 | Ajeno a gut-brain/FM | Erdrich 2020 | ~761 |

(Algunas líneas aproximadas — los PMIDs están concentrados en las referencias finales,
bloques de líneas 669-777.)

**Acción requerida:**
1. Re-verificar CADA referencia contra PubMed uno por uno.
2. Eliminar o reasignar los 12 PMIDs erróneos.
3. Este hallazgo por sí solo justifica rechazar cualquier sumisión hasta que se corrija.

---

## B. HALLAZGO CRÍTICO #2 — DESINCRONIZACIONES Paper 1 / Paper 2 / GROUNDING

1. **Paper 2 versiona a Paper 1 como "v2.8"** (Paper 2 línea 24: "companion transcriptomic manuscript, v2.8").
   Real: v2.14. **Corregir.**

2. **Paper 2 afirma "no hay estructura experimental humana para OPRM1"** (§2.1).
   Falso. PDB 8EFO y 8EF5 (OPRM1 humano crio-EM) existen y el lab los usó.
   **Agregar cita o reformular.**

3. **GROUNDING.md no cubre Fibromialgia.** Solo Nipah, ferritina-Au, RFdiffusion, EET.
   No hay auditoría de las 59 citas del manuscrito FM. G4 (procedencia) no es verificable
   contra GROUNDING actual. **Extender GROUNDING con citas FM verificadas.**

---

## C. HALLAZGO ALTO #3 — FME KILL vs. ENCUADRE

**Empírico:** `ichor-fme-exercise-responder-grounding-v2.json` → rho=-0.078, p=0.74, n=20.
Test pre-registrado, criterio KILL activado (rho<0.2 → rechazar).

**Encuadre en Paper 1:** §4.9-4.10.1 (~38 líneas) mantiene FME como eje operacionalizable.
Aunque el texto lo acota como "design module" / "anecdote, not evidence" /
"hypothesis-generating", el volumen narrativo contradice el resultado negativo.

**Riesgo:** Un revisor hostil dirá "el test pre-registrado falló pero el paper mantiene
el subfenotipo como eje central".

**Acción sugerida:**
- Reducir FME a una frase en Limitaciones.
- Mover el protocolo a un apéndice o documento separado.
- Declarar explícitamente: "El test pre-registrado FME fue negativo (rho=-0.078, p=0.74).
  La hipótesis basal de que la firma sanguínea predice respuesta al ejercicio fue falsificada."

---

## D. HALLAZGO MEDIO #4 — E-VALUE §3.4.7

1. **Borenstein d→OR tratado como RR.** Usa ln(OR)≈d·π/√3 pero luego calcula E-value sobre RR
   (no OR). Para d=0.86, OR=4.76 solo si el outcome es raro; aquí es ratio de medias, no risk ratio.
2. **Benchmarks epidemiológicos sin fuente.** "Smoking→lung cancer RR 15-30", "obesity→diabetes RR 3-7",
   "age→mortality RR 2-5" — sin citar Marmot 2005 ni fuente real.

**Acción:** Justificar la aproximación o eliminar los benchmarks. Agregar fuente.

---

## E. HALLAZGO MEDIO #5 — VIF>5 POST-HOC

El umbral VIF>5 para el ajuste ortogonal del eje opioide fue seleccionado post-hoc.
El manuscript lo documenta (§3.2) pero no lo declara como análisis exploratorio.

**Agregar en Limitaciones:** "El umbral VIF>5 fue seleccionado post-hoc; los valores p
del ajuste ortogonal no deben interpretarse como confirmatorios."

---

## F. G6 (CONTROL ARM INVARIANT) — RESULTADO DE SUBAGENTE DELEGADO

**Regla exacta** `rubrics/protein-lab.json:92-98` (propuesta @ichor):
> "A control arm's stated invariant (composition, Hamming distance, length, degree)
> must be measured on the stored sequences and the measurement recorded in the artefact."
> `block_when`: "An arm declares an invariant that the stored data does not satisfy."

**Medición sobre `experiments/esm3_control_sequences_v1.json`** (4 brazos × 100 seqs, WT = P35372, 400 aa):

| Brazo (n=100) | Hamming vs WT | L1 vs WT (mean) | Declarado | G6 |
|---|---|---|---|---|
| `shuffled` | 365–386 | 0 (100/100 cero exacto) | `same_as_OPRM1` | **PASS** |
| `uniform` | 368–389 | 136–216 (mean 176.0) | `uniform_random` | **PASS** |
| `mutated_70pct` | 120 exacto | mean 71.14 | `NOT_same_as_OPRM1` | **PASS** |
| `mutated_70pct_compmatched` | 120 exacto | 0 (100/100 cero) | `same_as_OPRM1_exact_L1_zero` | **PASS** |

**Veredicto G6: PASS en todos los 4 brazos.** Los invariantes declarados en los artefactos
coinciden con las mediciones sobre las secuencias almacenadas. No hay brecha declaración-vs-dato.

**Nota:** Este G6 aplica al módulo de diseño de proteínas ESM3/no manuscrito FM.
El Paper 1 (transcriptómica) no usa brazos de control experimentales de secuencias;
sus "controles" son modelos estadísticos (modelos 1-6 de sexo/composición).

---

## G. SCORECARD — 10 RECLAMOS

`#` | `Reclamo` | `Ubicación` | `Evidencia en Disco` | `Veredicto` | `Severidad`
--- | --- | --- | --- | --- | ---
1 | COL9A1 hallazgo más robusto (Bonferroni + 5 sexo + 4 deconv + E-value 8.98) | §3.4.5, §7.2, Abstract | `e01_evalue_results.json`, `E1b_variant_sweep.csv` | **VERIFIED** | BAJA
2 | PTN secundario/hipótesis-generando; falsificado por NNLS (p=0.076), LOO frágil | §7.2, §3.4.5 | `e02_evalue_ptn_results.json` | **VERIFIED** | BAJA
3 | Eje opioide "parcialmente sensible a composición con componente per-célula retenido" | §3.2 | `vif_sensitivity_opioid_axis.py`, `E1b_variant_sweep.csv` | **VERIFIED** | BAJA
4 | FME es subfenotipo respondedor operacionalizable | §4.9-4.10 | `ichor-fme-exercise-responder-grounding-v2.json` (KILL) | **PARTIAL** | ALTA
5 | CA14 "sex-confounded, no sobrevive modelo primario femenino" | §4.2 | `sensitivity_analysis_GSE221921.csv` (p=0.135 F-only) | **VERIFIED** | BAJA
6 | MDGA2 y DRD2 robustos a sexo (5/5 modelos) | §3.1 | `sensitivity_analysis_GSE221921.csv` | **VERIFIED** | BAJA
7 | Ranking docking reproducido con ligandos verificados (bromo>prami>dopa; aprep>rolap) | Paper 2 §3.1-3.3 | `docking_validated_results.json`, `dockings_validados/*.pdbqt` | **VERIFIED** | BAJA
8 | E-values robustez confusión no medida | §3.4.7, Tabla 6 | `e01/e02_evalue_results.json` | **PARTIAL** (OR→RR no justificado) | MEDIA
9 | Batería 9 tests falsificación valida COL9A1/MDGA2/DRD2 | §7.1 | `falsification_results.json` | **VERIFIED** | BAJA
10 | Paper 2: "no hay estructura experimental humana OPRM1" | Paper 2 §2.1 | PDB 8EFO/8EF5 existen | **FALSE** | MEDIA

---

## H. LOS 3 "KILL-SHOTS" DEL REVISOR HOSTIL

1. **"Minería post-hoc con p-hacking de 21 genes y Bonferroni arbitrario."**
   Defensa: PARCIALMENTE BLINDADO. VIF>5 no pre-especificado. Agregar advertencia.

2. **"12 referencias mapeadas a artículos incorrectos."**
   Defensa: NO BLINDADO. Requiere re-verificación 1-a-1.

3. **"Test pre-registrado FME falló pero el paper mantiene el subfenotipo como eje."**
   Defensa: PARCIALMENTE BLINDADO. Reducir a frase + mover a apéndice.

---

## I. DICTAMEN DE PUBLICACIÓN

**bioRxiv:** CONDICIONAR — Aprobatorio solo tras corregir los 12 PMIDs, separar Paper 2,
y declarar explícitamente el KILL FME. bioRxiv no hace peer review pero sí screening
ético; las citas falsas son rechazo inmediato.

**PCI Genomics:** REQUIERE REVISIÓN MAYOR — Scope aceptable pero los PMIDs falsos
serán detectados por recomenders. Tras correcciones, viable.
**PCI Registered Reports:** NO VIABLE — Datos ya analizados; no hay Stage 1 previo.

**Revista Q1/Q2:** SOLO COMO CORRESPONDENCIA O PROTOCOLO — Falta validación independiente
(3er cohorte), wet-lab, y pre-registration genuina. No viable como artículo primario
de descubrimiento de biomarker.

---

## J. CHECKLIST PRE-SUMISIÓN OBLIGATORIO

- [ ] Re-verificar UNO por UNO los 59 PMIDs contra PubMed; reasignar/eliminar los 12 erróneos.
- [ ] Paper 2 línea 24: "v2.8" → "v2.14".
- [ ] Paper 2 §2.1: Corregir "no hay estructura experimental humana para OPRM1" (citar 8EFO/8EF5).
- [ ] Declarar KILL FME explícitamente: "rho=-0.078, p=0.74, hipótesis basal falsificada".
- [ ] Separar Paper 1 de Paper 2 para sumisión.
- [ ] E-value §3.4.7: Justificar OR→RR o eliminar benchmarks. Agregar fuente Marmot.
- [ ] VIF>5 en Limitaciones: declarar post-hoc, no confirmatorio.
- [ ] Reducir FME a frase en Limitaciones; mover protocolo a apéndice.
- [ ] Repositorio github.com/Grizaceo/protein-lab debe estar realmente público.
- [ ] Declarar explícitamente que análisis son exploratorios salvo pre-registrados.

---

## K. RESUMEN EJECUTIVO

El trabajo tiene un núcleo sólido: COL9A1, batería de 9 tests de falsificación,
honestidad estadística sobre VIF/composición, reproducibilidad formal de scripts.
Pero las 12 referencias falsas (PMIDs mapeados a artículos ajenos) son una objeción
letal que bloquea CUALQUIER sumisión. El FME KILL no está resuelto narrativamente.
Corregido esto, Paper 1 es un preprint válido y posible artículo de protocolo;
Paper 2 debe ir por separado como prueba de concepto metodológico.

**No convertir este documento en evidencia por sí mismo: cada acción requiere
re-verificación independiente por el investigador a cargo.**

---
*Artefacto generado por DAVI — 2026-09-06 — modo solo lectura.*
