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
| 1.6 | Batch effect analysis (GSE221921 metadata) | Confound | **REMAINING** | If batch drives signal → artefactual |
| 1.7 | Winsorization / trimming (5%/95%) | Robustness | **REMAINING** | If FC collapses with outlier removal → outlier-driven |
| 1.8 | Permutation testing (labels FM/HC shuffled) | Robustness | **REMAINING** | If signal survives permutation → label-independent (artefactual) |
| 1.9 | Leave-one-out cross-validation | Robustness | **REMAINING** | If single patient drives effect → not robust |
| 1.10 | CIBERSORTx deconvolution (alternative method) | Robustness | **REMAINING** | If signal collapses with different deconv → method-dependent |
| 1.11 | DESeq2/edgeR re-analysis (if counts available) | Robustness | **REMAINING** | If not significant with count model → FPKM artefact |
| 1.12 | Housekeeper comparison (ACTB, GAPDH, B2M) | Baseline | **REMAINING** | If housekeepers are equally "significant" → platform noise |
| 1.13 | Re-definition of case (if severity data exist) | Design | **NOT APPLICABLE** | No severity metadata in GSE221921 |
| 1.14 | MR inverse (COL9A1/PTN as outcomes) | Causal | **REMAINING** | If no causal link → reactive, not driver |

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
| 2.7 | VIF sensitivity (VIF max 13.1 reported) | Robustness | **REMAINING** | If removing high-VIF fractions changes result → collinearity-driven |
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
| **HIGH** | Permutation testing (labels FM/HC) | 1, 2, 4 | HIGH | If signal survives → artefactual |
| **HIGH** | Winsorization / trimming (5%/95%) | 1, 4 | HIGH | If FC collapses → outlier-driven |
| **HIGH** | CIBERSORTx deconvolution | 1, 2 | MEDIUM | If signal collapses → method-dependent |
| **HIGH** | Batch effect analysis (GSE221921) | 1, 2, 4 | HIGH | If batch drives signal → artefactual |
| **HIGH** | Leave-one-out cross-validation | 1 | HIGH | If single patient drives → not robust |
| **MEDIUM** | VIF sensitivity (remove high-VIF fractions) | 2 | HIGH | If result changes → collinearity-driven |
| **MEDIUM** | DESeq2/edgeR re-analysis | 1 | MEDIUM | If not significant → FPKM artefact |
| **MEDIUM** | Housekeeper comparison | 1 | HIGH | If housekeepers equally significant → noise |
| **MEDIUM** | MR inverse (COL9A1/PTN as outcomes) | 1 | MEDIUM | If no causal link → reactive |
| **MEDIUM** | Power analysis for GSE67311 non-replication | 5 | HIGH | If underpowered → false negative |
| **LOW** | Isoform-specific expression | 1 | MEDIUM | If wrong isoform → misleading |
| **LOW** | Negative control with spike-ins | 1 | LOW | No spike-in data |

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

**Yes — at least 5 high-feasibility methods remain unapplied:**

1. Permutation testing
2. Winsorization
3. Batch effect analysis
4. Leave-one-out cross-validation
5. CIBERSORTx deconvolution

These are not «cosmetic» — each could genuinely refute Claim 1 (our central finding) if the outcome is negative. Applying them is not optional for a rigorous preprint; it is the difference between «we tested for confounds» and «we tested for all computable confounds.»

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
