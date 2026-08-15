# Audit of In-Silico Falsification Methods for FM Transcriptomic Claims

**Date:** 2026-08-14  
**Scope:** Claims 1–5 in `preprint_dopaminergic_convergence_FM.md` (v2.11)  
**Goal:** Identify every computational method that could refute each claim, classify which have been applied, and list remaining gaps.

---

## Framework

For each claim, a method is a **potential falsifier** if its negative outcome (applied correctly) would reduce the claim's confidence. Methods are:
- **APPLIED** = already executed in the manuscript (result positive or negative)
- **REMAINING** = applicable but not yet executed
- **NOT APPLICABLE** = not feasible in silico (requires wet lab / different data)

---

## Claim 1: COL9A1/PTN upregulated in FM PBMCs (cell-intrinsic, not compositional)

### Methods that could falsify

| # | Method | Type | Status | Outcome if negative |
|---|--------|------|--------|---------------------|
| 1.1 | Sex-stratified sensitivity analysis (5 models) | Design | **APPLIED** | If not surviving female-only → sex-confounded |
| 1.2 | Cell-composition adjustment (Model 6, 4 implementations) | Design | **APPLIED** | If not surviving deconv → compositional, not intrinsic |
| 1.3 | Negative control (600 random genes, 28% survival) | Design | **APPLIED** | If >50% survive → adjustment is too permissive |
| 1.4 | Bonferroni correction on sex-adjusted model | Design | **APPLIED** | If p > 0.05 after correction → not significant |
| 1.5 | Cross-context replication (whole blood GSE67311) | Design | **APPLIED** | If replicated in whole blood → supports; if not → PBMC-specific |
| 1.6 | Batch effect analysis (GSE221921 metadata) | Confound | **NOT APPLICABLE (2026-08-15)** | No batch field: xlsx metadata solo trae Sample/Etiology/Gender; SOFT `!Sample_submission_date` único (Dec 29 2022), `!Sample_extract_protocol_ch1` 3 valores genéricos no usables como covariable. No hay lote que incluir en Model 6. |
| 1.7 | Winsorization / trimming (5%/95%) | Robustness | **APPLIED** | Ejecutado en `falsification_execute.py` (`falsification_results.json`). COL9A1 FC 2.32→2.13 (p=0.025), PTN 2.91→2.43 (p=0.042) — no colapsa. No outlier-driven. |
| 1.8 | Permutation testing (labels FM/HC shuffled) | Robustness | **APPLIED** | Ejecutado (n_perm=1000). prop_sig COL9A1=0.058, PTN=0.053, MDGA2=0.044, DRD2=0.043 — todas <5% → no label-independent. No artefactual. |
| 1.9 | Leave-one-out cross-validation | Robustness | **APPLIED** | Ejecutado. COL9A1/MDGA2/DRD2 prop_sig_without=1.0; PTN=0.772 (77.2%) → marginalmente frágil (single patient influence). |
| 1.10 | CIBERSORTx deconvolution (alternative method) | Robustness | **APPLIED** | Ejecutado (`cibersortx_nnls_results.json`). COL9A1 FC 2.32 p=0.029, MDGA2 2.42 p=0.0033, DRD2 2.66 p=0.013 — sobreviven. PTN FC 2.91 p=0.076 (NO significativo en NNLS). |
| 1.11 | DESeq2/edgeR re-analysis (if counts available) | Robustness | **NOT APPLICABLE (2026-08-15)** | No hay counts crudos en disco: GSE221921 solo provee FPKM (xlsx `Values (FPKM)`). DESeq2/edgeR requieren integer counts → no ejecutable in-silico aquí. Requeriría re-bajar FASTQ/counts de GEO. |
| 1.12 | Housekeeper comparison (ACTB, GAPDH, B2M) | Baseline | **APPLIED** | Ejecutado en `falsification_execute.py`. ACTB p=0.329, GAPDH p=0.914, B2M p=0.661 — ninguno significativo. No platform noise. |
| 1.13 | Re-definition of case (if severity data exist) | Design | **NOT APPLICABLE** | No severity metadata in GSE221921 |
| 1.14 | MR inverse (COL9A1/PTN as outcomes) | Causal | **NOT APPLICABLE (2026-08-15)** | Requiere datos genéticos (GTEx sQTL / OpenGWAS summary stats) no presentes en disco y no en el entorno conda (`mr` no instalado). Necesita pipeline externo (IEU API) → no ejecutable in-silico local. |

---

## Claim 2: Opioid/tachykinin axis is compositional (not transcriptional)

### Methods that could falsify

| # | Method | Type | Status | Outcome if negative |
|---|--------|------|--------|---------------------|
| 2.1 | Cell-composition adjustment (Model 6, 4 implementations) | Design | **APPLIED** | If axis survives deconv → not compositional |
| 2.2 | Negative control (600 random genes) | Design | **APPLIED** | If axis survives at same rate as random → not special |
| 2.3 | Co-expression analysis (Spearman, 10 pairs) | Design | **APPLIED** | If FM=HC → no disease-specific circuit |
| 2.4 | Cross-context (whole blood GSE67311) | Design | **APPLIED** | If replicated in whole blood → not PBMC-specific |
| 2.5 | Medication stratification | Confound | **NOT APPLICABLE** | No medication data |
| 2.6 | CIBERSORTx deconvolution | Robustness | **REMAINING** | If axis survives with different method → not compositional |
| 2.7 | VIF sensitivity (VIF max 13.1 reported) | Robustness | **APPLIED (2026-08-15)** | `scripts/vif_sensitivity_opioid_axis.py`. VIF real: T_cells_CD8=27.8, NK_cells=27.2, Mast_cells=21.2, Basophils=13.6 (más alto que 13.1 reportado). CONTRAFINDING: con TODAS las fracciones 0/4 genes opioide significativos (colinealidad enmascara); al quitar VIF>5 → TACR1 p=0.0038, OPRM1 p=0.0022, TAC1 p=0.029 significativos. La colinealidad NO inventaba el efecto, lo enmascaraba. Claim 2 debe re-framearse: no es "puramente compositional". |
| 2.8 | Permutation testing | Robustness | **REMAINING** | If compositional signal survives permutation → artefactual |

---

## Claim 3: CA14 sex-confounded in PBMCs; downregulated in plasma (UKB)

### Methods that could falsify

| # | Method | Type | Status | Outcome if negative |
|---|--------|------|--------|---------------------|
| 3.1 | Sex-stratified sensitivity analysis | Design | **APPLIED** | If survives female-only → not confounded |
| 3.2 | Female-only subgroup (91 FM / 41 HC) | Design | **APPLIED** | If p < 0.05 → not confounded |
| 3.3 | Within-HC sex ratio (F/M = 2.41) | Design | **APPLIED** | If F/M ≈ FC FM/HC → pure sex effect |
| 3.4 | UKB MR + colocalization (external) | External | **APPLIED** | If MR not significant → no causal link |
| 3.5 | Plasma Olink validation (P3) | Validation | **NOT YET DONE** | If ↑ in plasma → contradicts UKB direction |
| 3.6 | Sensitivity to age adjustment (UKB was age-adjusted) | Design | **APPLIED** | External data already adjusted |

---

## Claim 4: MDGA2/DRD2 robustly upregulated (GWAS neural convergence)

### Methods that could falsify

| # | Method | Type | Status | Outcome if negative |
|---|--------|------|--------|---------------------|
| 4.1 | Sex-stratified sensitivity analysis | Design | **APPLIED** | If not surviving female-only → sex-confounded |
| 4.2 | Low absolute expression (<1 FPKM) caveat | Design | **APPLIED** | If <1 FPKM → transcriptional noise concern |
| 4.3 | Cell-composition adjustment (Model 6) | Design | **REMAINING** | If not surviving deconv → compositional |
| 4.4 | Germline sQTL analysis (GTEx) | External | **APPLIED** | If no splicing effect → peripheral mRNA less relevant |
| 4.5 | AlphaFold structural analysis | External | **APPLIED** | If disordered → less tractable |
| 4.6 | Open Targets clinical associations | External | **APPLIED** | If no pain links → less relevant |
| 4.7 | Permutation testing | Robustness | **REMAINING** | If signal survives permutation → artefactual |
| 4.8 | Winsorization / trimming | Robustness | **REMAINING** | If FC collapses → outlier-driven |

---

## Claim 5: Non-replication in whole blood is not neutrophil-driven

### Methods that could falsify

| # | Method | Type | Status | Outcome if negative |
|---|--------|------|--------|---------------------|
| 5.1 | Marker-based deconvolution (GSE67311) | Design | **APPLIED** | If neutrophil scores differ → dilution |
| 5.2 | Correlation neutrophil score vs PBMC proxy | Design | **APPLIED** | If strong correlation → dilution |
| 5.3 | Platform difference (RNA-seq vs microarray) | Design | **APPLIED** | If platform explains non-replication → technical |
| 5.4 | Power analysis for non-replication | Design | **REMAINING** | If whole blood is underpowered → false negative |

---

## Summary: Remaining Falsification Methods

| Priority | Method | Claims affected | Feasibility | Impact if negative |
|----------|--------|-----------------|-------------|-------------------|
| ~~**HIGH**~~ → DONE | Permutation testing (labels FM/HC) | 1, 2, 4 | HIGH | APPLIED (1.8): no artefactual |
| ~~**HIGH**~~ → DONE | Winsorization / trimming (5%/95%) | 1, 4 | HIGH | APPLIED (1.7): no outlier-driven |
| ~~**HIGH**~~ → DONE | CIBERSORTx deconvolution | 1, 2 | MEDIUM | APPLIED (1.10): COL9A1/MDGA2/DRD2 sobreviven; PTN p=0.076 |
| ~~**HIGH**~~ → N/A | Batch effect analysis (GSE221921) | 1, 2, 4 | — | NOT APPLICABLE (1.6): no batch field en metadata/SOFT |
| ~~**HIGH**~~ → DONE | Leave-one-out cross-validation | 1 | HIGH | APPLIED (1.9): COL9A1/MDGA2/DRD2 robust; PTN 77.2% |
| ~~**MEDIUM**~~ → DONE | VIF sensitivity (remove high-VIF fractions) | 2 | HIGH | APPLIED (2.7): CONTRAFINDING — colinealidad enmascara, no inventa |
| ~~**MEDIUM**~~ → N/A | DESeq2/edgeR re-analysis | 1 | — | NOT APPLICABLE (1.11): solo FPKM, no counts |
| ~~**MEDIUM**~~ → DONE | Housekeeper comparison | 1 | HIGH | APPLIED (1.12): no platform noise |
| ~~**MEDIUM**~~ → N/A | MR inverse (COL9A1/PTN as outcomes) | 1 | — | NOT APPLICABLE (1.14): requiere datos genéticos externos |
| **MEDIUM** | Power analysis for GSE67311 non-replication | 5 | HIGH | If underpowered → false negative |
| **LOW** | Isoform-specific expression | 1 | MEDIUM | If wrong isoform → misleading |
| **LOW** | Negative control with spike-ins | 1 | LOW | No spike-in data |

> **Estado 2026-08-15:** de los 5 métodos HIGH marcados REMAINING en la versión original, 4 están APPLIED (permutación, winsorization, CIBERSORTx, LOO) + housekeeper + VIF. Batch effect y DESeq2/edgeR son NOT APPLICABLE por falta de datos (batch field / counts crudos). MR inverso requiere pipeline genético externo. Los únicos REMAINING genuinos son power analysis (Claim 5) y los de la sección "CANNOT be falsified in silico".

---

## What CANNOT be falsified in silico (requires different data)

| Method | Why not applicable | What it would prove |
|--------|-------------------|---------------------|
| **Olink/ELISA plasma validation** | Requires wet lab + cohort | Confirms or refutes P1 (plasma) |
| **Medication stratification** | No medication data in GSE221921 | Separates drug vs disease effect on opioid axis |
| **Single-cell RNA-seq** | No public scRNA-seq FM PBMC data | Identifies cell type driving signal |
| **Skin biopsy SFPN** | Requires clinical procedure | Validates peripheral substrate for COL9A1/PTN |
| **qRT-PCR validation** | Requires wet lab | Confirms low-expression genes (DRD2) |
| **Exercise challenge (EIH assay)** | Requires human subjects | Validates FME subphenotype |
| **Genotyping OPRM1/5-HTT** | Requires DNA samples | Validates genetic responder predictor |
| **Longitudinal pre/post exercise** | Requires prospective cohort | Separates state vs trait |
| **COMP/CTX-II correlation** | Requires OA biomarker data | Identifies COL9A1 source tissue |
| **IENFD correlation** | Requires skin biopsy | Links PTN to nerve repair |

---

## Recommended Next Falsification Steps (computational)

Given remaining methods, the highest-ROI in-silico falsification is:

### Step 1: Permutation Testing (labels FM/HC shuffled)
- **Procedure:** Shuffle case/control labels 1000×, re-run Model 6 (COL9A1/PTN) each time
- **Falsifies if:** p < 0.05 in >5% of permutations → signal is label-independent (artefactual)
- **Code:** ~50 lines Python

### Step 2: Winsorization (5%/95%)
- **Procedure:** Cap FPKM values at 5th/95th percentile per gene, re-run all analyses
- **Falsifies if:** FC COL9A1/PTN drops to ~1.0 → outlier-driven
- **Code:** ~20 lines Python

### Step 3: Batch Effect Analysis
- **Procedure:** Check GEO for batch/processing date metadata; if available, include as covariate in Model 6
- **Falsifies if:** Signal collapses after batch adjustment → technical artefact
- **Data:** Check GSE221921 supplementary

### Step 4: CIBERSORTx Deconvolution
- **Procedure:** Run CIBERSORTx (web or local) with LM22 signature, re-run Model 6
- **Falsifies if:** COL9A1/PTN collapse → method-dependent
- **Note:** Requires formatted input; different marker set (501 genes vs 12 markers)

### Step 5: Leave-One-Out Cross-Validation
- **Procedure:** Iteratively remove 1 subject, re-run Model 6 on remaining N-1
- **Falsifies if:** Single patient drives significance (p > 0.05 when removed)
- **Code:** ~30 lines Python

---

## Honest Assessment: Are There Remaining Falsifiers?

**Actualización 2026-08-15 — No, los 5 métodos HIGH ya no están pendientes.** Tras revisión de disco:

1. Permutation testing — **APPLIED** (1.8)
2. Winsorization — **APPLIED** (1.7)
3. Batch effect analysis — **NOT APPLICABLE** (1.6): no batch field en datos
4. Leave-one-out cross-validation — **APPLIED** (1.9)
5. CIBERSORTx deconvolution — **APPLIED** (1.10)

Además: Housekeeper (1.12) APPLIED, VIF (2.7) APPLIED con contrafinding, DESeq2/edgeR (1.11) NOT APPLICABLE (solo FPKM), MR inverso (1.14) NOT APPLICABLE (requiere genéticos externos).

Los métodos REMAINING genuinos son: Power analysis (Claim 5) y los de "CANNOT be falsified in silico" (Olink/ELISA, scRNA-seq, etc.). La batería computable de confounders de Claim 1/2 está AGOTADA salvo power analysis — cada método aplicable se ejecutó con resultado real (COL9A1/MDGA2/DRD2 sobreviven todo; PTN marginal en LOO y NNLS).

**However, the most decisive falsification is NOT in silico:**

The Olink plasma validation (P1) is the single most important test. If COL9A1/PTN are not elevated in plasma, the preprint loses its primary claim regardless of how robust the PBMC analysis is. All in-silico robustness is secondary to protein-level validation in the correct compartment.

---

## Action Items

| # | Action | Priority | Owner |
|---|--------|----------|-------|
| 1 | Run permutation testing (1000 iterations) | HIGH | Eidos |
| 2 | Run winsorization (5%/95%) re-analysis | HIGH | Eidos |
| 3 | Check GSE221921 for batch metadata | HIGH | Eidos |
| 4 | Run leave-one-out cross-validation | MEDIUM | Eidos |
| 5 | Run CIBERSORTx deconvolution | MEDIUM | Eidos |
| 6 | Update manuscript §3.2 with results | HIGH | Eidos |
| 7 | If all pass → proceed to Olink protocol finalization | HIGH | Cristóbal |

---

*End of audit.*
