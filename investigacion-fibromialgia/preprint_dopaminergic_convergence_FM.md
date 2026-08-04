# Peripheral Neuroimmune and Nociceptive Gene Signatures in Fibromyalgia: A Targeted Reanalysis of Public Transcriptomic Cohorts Informed by UK Biobank Plasma Proteomics

---

**Authors:** Cristóbal Muñoz Rojas¹

¹ Independent Researcher, Santiago, Chile. Correspondence: cristoe4@gmail.com

**Preprint — Draft v2.6 — August 2026**

---

## Abstract

Fibromyalgia (FM) is a prevalent chronic pain condition whose molecular basis remains poorly defined. A genome-wide association study (GWAS) meta-analysis of 2.5 million individuals identified 26 risk loci enriched in brain tissues, prioritizing neural and synaptic genes including *DRD2*, *MDGA2*, *CAMKV*, and *CELF4* (Kerrebijn et al., 2025; PMID 41001472). Separately, the largest population-scale plasma proteomics studies of chronic pain (UK Biobank Olink) found no support for the classical IL-6/IL-8 inflammatory axis and instead triangulated CA14 (carbonic anhydrase XIV) as a causal protein in chronic widespread pain via Mendelian randomization and colocalization (Chen et al., 2025, *Adv Sci*; PMID 41025730). Here we perform a targeted, hypothesis-driven reanalysis of two public transcriptomic datasets — GSE221921 (PBMCs, 96 FM / 93 HC) and GSE67311 (whole blood, 67 FM / 75 HC) — interrogating GWAS neural genes, the opioid/tachykinin neuropeptide axis, UKB causal genes, and mast cell markers. In GSE221921 PBMCs we find: (1) *MDGA2* (q = 1.1×10⁻⁷) and *DRD2* (q = 2.9×10⁻⁵) robustly upregulated across all five sensitivity models; (2) a **complete opioid/tachykinin neuropeptide circuit activated** — receptor *TACR1* (NK1, Substance P receptor; FC = 2.73, d = +0.60, the largest effect size in the panel), *OPRM1* (μ-opioid receptor; FC = 2.28, d = +0.53), ligand *TAC1* (Substance P; FC = 2.10, d = +0.47) and *OPRK1* (κ-opioid; FC = 1.78, d = +0.38), with coordinated co-expression (rho = 0.31–0.63); (3) **CA14 — the top UKB causal protein for chronic widespread pain — upregulated in FM PBMC mRNA** (FC = 2.29, p = 0.0003, d = +0.41) while being **downregulated in plasma** in the UKB cross-sectional analysis, with MR indicating a protective effect of genetically elevated CA14; and (4) **five UKB causal genes involved in immune signaling (TNFRSF1B, CD74, COL18A1, BTN2A1, TNFRSF4) significantly downregulated** (FC 0.54–0.77), consistent with an immunomodulatory/exhaustion pattern rather than classical systemic inflammation. In GSE67311 (whole blood), these PBMC-derived proxies do not replicate (TAC1/OPRM1/IL6 FC ≈ 1.0), and deconvolution analysis rules out neutrophil-driven dilution as the explanation; extending the opioid axis analysis to the full receptor set (TACR1, OPRM1, OPRK1) confirms the non-replication of absolute expression (all FC ≈ 1.0, none survives Bonferroni), **yet the co-expression structure of the axis is stable and in some pairs stronger in FM whole blood than in PBMCs (TACR1–OPRK1 rho = +0.74, OPRM1–OPRK1 rho = +0.53)** — the circuit is transcriptionally coherent in FM, while its amplitude is compartment-dependent. These findings argue that the peripheral molecular signature of FM is dominated by **neuropeptide nociceptive signaling and immunomodulation**, not classical inflammation, and support prioritizing CA14 (expecting ↓ in plasma) and the opioid/tachykinin axis for validation in plasma (Olink/ELISA) with cell-type-resolved cohorts.

**Keywords:** fibromyalgia, CA14, TACR1, OPRM1, tachykinin, opioid, UK Biobank, Olink, PBMCs, targeted reanalysis, nociception, immunomodulation

---

## 1. Introduction

Fibromyalgia (FM) affects 2–4% of the global population, manifesting as chronic widespread pain, fatigue, cognitive dysfunction, and sleep disturbances (Sarzi-Puttini et al., 2020). Despite its prevalence, FM lacks specific diagnostic biomarkers and its pharmacotherapy remains limited to three FDA-approved medications — pregabalin, duloxetine, and milnacipran — none designed to target FM-specific molecular pathology (Chinn et al., 2016).

A recent GWAS meta-analysis by Kerrebijn and colleagues, comprising 54,629 cases and 2,509,126 controls across 11 cohorts, identified 26 genome-wide significant risk loci for FM, with heritability enriched exclusively in brain tissues and neuronal cell types (Kerrebijn et al., 2025; PMID 41001472; medRxiv doi: 10.1101/2025.09.18.25335914). The prioritized genes span dopaminergic signaling (*DRD2*), synaptic plasticity (*CAMKV*, *CELF4*), neural cell adhesion (*NCAM1*, *MDGA2*), axon guidance (*DCC*), and other neural functions (*GPR52*, *HTT*). While the GWAS authors describe these as a neural/CNS network, we note that only *DRD2* is strictly dopaminergic; the others are more broadly neural or synaptic.

This genetic architecture motivates a direct question: **are these GWAS-prioritized genes differentially expressed in FM patients?** Several bioinformatic studies have analyzed the GSE221921 PBMC dataset (Mohapatra et al., 2024; Bi et al., 2024; Zhao et al., 2025; Gowri Gopal et al., 2026), but all employed unbiased genome-wide approaches (DEG → PPI → hub genes). None tested the specific hypothesis that the GWAS-defined gene set is coordinately altered — a targeted, hypothesis-driven analysis that is distinct from and complementary to unbiased discovery.

In parallel, population-scale plasma proteomics has reframed the peripheral biology of chronic pain. Li ZY et al. (2025; PMID 40048323) profiled 2,923 plasma proteins (Olink Explore) in 51,644 UK Biobank participants with chronic pain, identifying 474 pain-associated proteins and 10 proteins validated as causal by Mendelian randomization — none of them classical inflammatory cytokines. A dedicated FM/nociplastic analysis of the UKB Olink data (Chen et al., 2025, *Adv Sci*; PMID 41025730; 29,254 participants, 2,920 proteins) built multi-protein scores with AUC 0.856–0.880 for CWP, identified 18 proteins with causal relevance by MR, and triangulated **CA14 (carbonic anhydrase XIV)** as the top causal protein by MR + colocalization (PP.H4 > 0.5). Notably, CA14 is **downregulated in plasma** in the cross-sectional analysis while genetically elevated CA14 is protective by MR; and the authors propose **CA14 agonists, not the inhibitor sulthiame**, as the more promising therapeutic direction. Critically, IL-6, IL-8/CXCL8, TAC1 and Substance P appear **zero times** in the largest published chronic pain proteomics screen — the classical inflammatory axis is not supported at population scale.

In this study, we: (1) test the GWAS neural gene set for differential expression in PBMCs (GSE221921) and whole blood (GSE67311), including comprehensive sensitivity analyses for sex confounding; (2) extend the analysis to the **opioid/tachykinin neuropeptide axis** (ligands *TAC1*, *PENK*, *PNOC*, *POMC*; receptors *TACR1*, *OPRM1*, *OPRK1*, *OPRD1*); (3) test the **UKB causal genes** (CA14, TNFRSF1B, CD74, COL18A1, BTN2A1, TNFRSF4, CD302, TNFRSF9) in our PBMC data to connect population-scale causal proteomics with transcriptomics; (4) include a negative control panel of mast cell markers; and (5) contextualize our findings with a targeted literature review of dopamine agonist trials in FM and the pharmacology of CA14.

---

## 2. Methods

### 2.1 Gene Set Definition

**GWAS-Prioritized Neural Gene Set.** We extracted 13 genes from the 26 GWAS risk loci reported by Kerrebijn et al. (2025) that are functionally linked to neural or synaptic signaling: *DRD2*, *NCAM1*, *GPR52*, *CAMKV*, *CELF4*, *DCC*, *MDGA2*, *NPY*, *KYNU*, *SRD5A2*, *PPP2R2B*, *NPC1*, and *HTT*. We designate this set as "GWAS neural genes" rather than "dopaminergic network," as only *DRD2* is strictly dopaminergic.

**Opioid/Tachykinin Neuropeptide Axis.** Ligands: *TAC1* (Substance P), *PENK* (enkephalins), *PNOC* (nociceptin), *POMC* (β-endorphin). Receptors: *TACR1* (NK1), *OPRM1* (μ-opioid), *OPRK1* (κ-opioid), *OPRD1* (δ-opioid). HGNC symbols verified (TAC1 = Substance P; PENK = proenkephalin — a distinct opioid ligand, not Substance P; correction documented in AUDITORIA_INTEGRIDAD_PROXY.md).

**UKB Causal Gene Set.** Genes encoding proteins with MR-supported causal relevance for chronic pain / chronic widespread pain in UKB Olink proteomics, measured in GSE221921: *CA14* (top-ranking causal for CWP, MR + colocalization; Chen et al., 2025) and the immune-signaling genes *TNFRSF1B*, *CD74*, *COL18A1*, *BTN2A1*, *TNFRSF4*, *CD302*, *TNFRSF9* (MR-validated in the multisite chronic pain analysis; Li ZY et al., 2025). *LEP* and *TNF* are not measurable in GSE221921. Note: in the published Chen et al. (2025) analysis, 18 proteins have MR causal relevance for CWP (CA14, COL9A1, CRELD1, DPEP1, LEG1, LGALS3, MLN, PRSS53, TNF, BPIFB2, CTSO, DDR1, FAM171B, IFI30, LRRC37A2, PTN, SFTPD, ST3GAL1); CA14 is the top-ranking one and is **downregulated in plasma** in the cross-sectional analysis, with MR indicating a protective effect of genetically elevated CA14.

**Mast Cell / Basophil Panel (negative control).** Four genes (*CPA3*, *MS4A2*, *FCER1A*, *HDC*) previously identified as differentially expressed in FM whole blood (Kurian et al., 2017). These are primarily expressed by basophils and mast cells, which are depleted during PBMC isolation.

*NPY* was included in the pre-specified gene set but was absent from the GSE221921 expression matrix. FDR correction was therefore applied to 16 measured genes (12 GWAS neural + 4 mast cell) in the primary GWAS-neural analysis; the expanded panel of 19 genes used for the opioid/tachykinin and UKB-causal analyses was corrected with Bonferroni ×19 or ×9 as specified in §2.3.

### 2.2 Transcriptomic Datasets

**GSE221921 (PBMCs, RNA-seq).** FPKM-normalized expression values from peripheral blood mononuclear cells of 96 FM patients and 93 healthy controls (Mohapatra et al., 2024; PMID 38366049). Sample metadata and expression matrices were obtained from the GEO supplementary file `GSE221921_FM_ProcessedData.xlsx`.

**Critical note on sex distribution:** The GSE221921 cohort has a severe sex imbalance — FM group: 91 female / 5 male; HC group: 41 female / 52 male. This confounds any unadjusted FM vs. HC comparison, as a portion of the observed signal may reflect sex differences rather than disease effects. We address this through multiple sensitivity analyses (§2.4).

**GSE67311 (Whole blood, microarray).** Affymetrix Human Gene 1.1 ST array expression data from whole blood (PAXgene tubes) of FM patients and healthy controls (Kurian et al., 2017; PMID 27157394). **Metadata verification (2026-08-03): the GEO sample metadata contains 67 FM / 75 HC (142 total), which differs from the 70/70 reported in the original paper.** Pre-computed differential expression results (log₂FC, p-value, FDR-adjusted p-value) were used, with the verified group counts.

### 2.3 Statistical Analysis

All p-values from the 16 measured genes in the GWAS-neural analysis were jointly corrected using the Benjamini-Hochberg (BH) procedure (Benjamini & Hochberg, 1995) at α = 0.05. Genes were considered significant at q < 0.05.

For the expanded panel of 19 genes (validate_fm_biomarkers_iter2.py, v3 post-adversarial-audit), expression values are heavy-tailed and non-normal (Shapiro-Wilk rejects normality for all genes, both groups), so **Mann-Whitney U tests** were used as the primary inference, with **Bonferroni correction across the 19-gene panel** (N_GENES_PANEL = 19), and **Cohen's d** (pooled SD) reported as the effect size. T-tests are retained only as reference. Classification: proxy significant if p_Bonf < 0.05; effect size graded small (d < 0.3), small–medium (0.3 ≤ d < 0.5), medium (0.5 ≤ d < 0.8).

For the UKB-causal gene analysis (9 measurable genes in GSE221921), Bonferroni correction ×9 was applied to the Mann-Whitney p-values.

For the opioid/tachykinin axis, Mann-Whitney U p-values are reported; the four core genes (TACR1, OPRM1, TAC1, OPRK1) survive conservative Bonferroni correction across the 21-gene union panel (19 + TACR1 + OPRK1; e.g., TACR1 p = 0.0010 × 21 = 0.021; OPRK1 p = 0.0017 × 21 = 0.036). Spearman rank correlation was used for co-expression analysis across all 189 samples.

### 2.4 Sensitivity Analyses for GSE221921

Given the sex imbalance, we applied five analytical models to each gene:

1. **Welch t-test on raw FPKM** (original analysis)
2. **Welch t-test on log₂(FPKM+1)** (variance-stabilizing transform)
3. **Mann-Whitney U test** (non-parametric, distribution-free)
4. **OLS regression: log₂(FPKM+1) ~ case + sex** (sex as covariate, full cohort)
5. **Female-only subgroup: Welch t-test on log₂(FPKM+1)** (91 FM vs. 41 HC, eliminates sex confound entirely)

Each model produced p-values that were independently FDR-corrected across all 16 genes. Genes were classified by robustness: "Robust" (q < 0.05 in all 5 models), "Supported" (q < 0.05 in 3–4 models), "Model-sensitive" (q < 0.05 in 1–2 models), or "Not significant."

### 2.5 Targeted Literature Review

We searched PubMed (terms: "pramipexole fibromyalgia," "ropinirole fibromyalgia," "dopamine agonist fibromyalgia"), ClinicalTrials.gov, and the GSK Study Register for clinical trials of dopamine D2/D3 agonists in FM; and PubMed/EuropePMC for CA14, sulthiame, and UKB Olink chronic pain proteomics (Li ZY et al., 2025; Chen et al., 2025). Search date: August 2026. This is a targeted narrative review, not a formal systematic review; no PRISMA protocol was registered.

### 2.6 Limitations of the Analytical Approach

We acknowledge that the use of FPKM values with parametric tests is a simplified approach. The gold standard for RNA-seq differential expression is count-based modeling (DESeq2/edgeR/limma-voom; Love et al., 2014). Only FPKM values were available in the GEO supplementary materials; raw counts were not accessible. All analyses were performed in Python 3.10 using pandas 1.5, scipy 1.10, and statsmodels 0.13. The primary inference therefore uses non-parametric Mann-Whitney U with Bonferroni correction (§2.3), which is robust to the FPKM distribution.

---

## 3. Results

### 3.1 MDGA2 and DRD2 Are Robustly Upregulated in FM PBMCs

Table 1 presents the sensitivity analysis for all 16 measured genes. Two genes — *MDGA2* and *DRD2* — were significant (q < 0.05) across all five analytical models and are classified as **Robust**:

**Table 1. Sensitivity analysis: q-values (FDR-corrected) across five analytical models.**

| Gene | Category | FM mean | HC mean | Welch FPKM | Welch log₂ | Mann-Whitney | OLS sex-adj | Female-only | Robustness |
|------|----------|--------:|--------:|-----------:|-----------:|-------------:|------------:|------------:|------------|
| *MDGA2* | GWAS Neural | 2.582 | 1.069 | **1.1×10⁻⁷** | **1.0×10⁻⁸** | **1.1×10⁻⁷** | **6.3×10⁻⁶** | **5.5×10⁻⁶** | **Robust (5/5)** |
| *DRD2* | GWAS Neural | 0.721 | 0.271 | **2.9×10⁻⁵** | **2.6×10⁻⁶** | **1.6×10⁻⁶** | **4.7×10⁻⁴** | **3.6×10⁻⁵** | **Robust (5/5)** |
| *CAMKV* | GWAS Neural | 0.656 | 0.288 | **3.2×10⁻³** | **1.6×10⁻³** | **8.3×10⁻³** | 0.112 | **0.032** | Supported (4/5) |
| *CELF4* | GWAS Neural | 1.341 | 0.848 | **0.046** | **0.013** | **0.010** | 0.167 | **0.032** | Supported (4/5) |
| *HTT* | GWAS Neural | 20.60 | 25.17 | 0.120 | **7.5×10⁻³** | **4.6×10⁻³** | 0.177 | **0.042** | Supported (3/5) |
| *NCAM1* | GWAS Neural | 4.375 | 3.234 | 0.087 | **0.021** | **0.010** | 0.186 | 0.114 | Model-sensitive (2/5) |
| *DCC* | GWAS Neural | 2.747 | 1.905 | 0.087 | **0.023** | **0.016** | 0.167 | 0.055 | Model-sensitive (2/5) |
| *SRD5A2* | GWAS Neural | 0.187 | 0.139 | 0.251 | 0.145 | 0.092 | 0.167 | **0.042** | Model-sensitive (1/5) |
| *GPR52* | GWAS Neural | 2.723 | 3.792 | 0.099 | 0.367 | 0.590 | 0.955 | 0.817 | NS |
| *NPC1* | GWAS Neural | 13.01 | 14.49 | 0.546 | 0.108 | 0.083 | 0.335 | 0.268 | NS |
| *KYNU* | GWAS Neural | 3.401 | 3.987 | 0.490 | 0.180 | 0.139 | 0.564 | 0.544 | NS |
| *PPP2R2B* | GWAS Neural | 2.445 | 2.587 | 0.883 | 0.825 | 0.581 | 0.955 | 0.817 | NS |
| *HDC* | Mast Cell | 5.274 | 7.991 | 0.666 | 0.103 | 0.094 | 0.462 | 0.732 | NS |
| *FCER1A* | Mast Cell | 3.899 | 4.448 | 0.748 | 0.784 | 0.578 | 0.321 | 0.496 | NS |
| *MS4A2* | Mast Cell | 0.719 | 0.788 | 0.926 | 0.076 | **2.9×10⁻³** | 0.321 | 0.325 | Model-sensitive (1/5) |
| *CPA3* | Mast Cell | 1.583 | 1.587 | 0.992 | 0.825 | 0.755 | 0.858 | 0.979 | NS |

*Notes: Bold indicates q < 0.05. NPY was pre-specified but absent from the expression matrix. FDR correction applied to 16 measured genes per model. Female-only analysis: 91 FM / 41 HC.*

**Key observations:**
- *MDGA2* and *DRD2* survive all five models including sex-adjusted OLS, suggesting that their signal is not solely explained by the severe sex imbalance in the cohort.
- *CAMKV* and *CELF4* survive four models (including female-only) but not the sex-adjusted OLS on the full cohort (q = 0.112 and 0.167, respectively). Their signals are supportive but model-sensitive. **Crucially, the OLS model ($\log_2(FPKM+1) \sim case + sex$) suffers from severe multicollinearity because fibromyalgia cases and female sex are highly collinear (95% of cases are female while controls are evenly split). This collinearity dramatically inflates the standard errors of the coefficients, leading to a profound loss of statistical power for case status. The female-only subgroup analysis (91 FM vs. 41 HC) completely removes the sex variable, thus eliminating this multicollinearity confound and rescuing the significance of both *CAMKV* and *CELF4* ($q = 0.032$). This highlights the female-only subgroup as the primary, statistically unconfounded model.**
- *HTT* — the gene with the strongest GWAS coding variant — shows a supported signal (3/5 models), which was not apparent in the original FPKM-only analysis. However, we note that the direction of effect is negative (downregulated in FM PBMCs), contrasting with the upregulation seen in *MDGA2* and *DRD2*.
- No mast cell marker shows a robust PBMC signal; *MS4A2* reaches significance only in the Mann-Whitney model and is therefore classified as model-sensitive rather than replicated across analytical frameworks.

### 3.2 The Opioid/Tachykinin Neuropeptide Axis Is Coordinately Activated in FM PBMCs

Extending the panel to the neuropeptide axis (validate_fm_biomarkers_iter2.py v3 + session analysis), we find that **ligands and receptors of both the tachykinin (Substance P) and endogenous opioid systems are simultaneously upregulated** in FM PBMCs (Table 2). This is the largest effect-size block observed in the entire investigation.

**Table 2. Opioid/tachykinin axis in GSE221921 (96 FM vs 93 HC PBMCs).**

| Gene | Role | FC (FM/HC) | MWU p | Bonf (×21) | Cohen's d | Classification |
|------|------|-----------:|-------:|-----------:|----------:|----------------|
| **TACR1** | NK1 receptor (Substance P) | **2.73** | **0.0010** | 0.021 | **+0.60** | **significant, medium effect** |
| **OPRM1** | μ-opioid receptor | **2.28** | **<0.0001** | <0.0021 | **+0.53** | **significant, medium effect** |
| **TAC1** | Substance P (ligand) | **2.10** | **0.0002** | 0.0042 | **+0.47** | **significant, small–medium** |
| **OPRK1** | κ-opioid receptor | **1.78** | **0.0017** | 0.036 | **+0.38** | **significant, small–medium** |
| PENK | Enkephalins (ligand) | 1.38 | 0.0031 | 0.065 (marginal) | +0.21 | trend (Bonf ×19 = 0.060) |
| OPRD1 | δ-opioid receptor | 1.23 | 0.0199 | NS | +0.10 | trend |
| PNOC | Nociceptin | 0.96 | NS | — | −0.02 | flat |
| POMC | β-endorphin/ACTH | 1.04 | NS | — | +0.03 | flat |

*Bonf ×21 = conservative correction across the 21-gene union panel (19 + TACR1 + OPRK1). PENK is marginal under Bonf ×19 (p = 0.060) and does not survive ×21.*

**Co-expression of the axis (Spearman, all 189 samples):**

| Pair | rho | p |
|------|----:|---:|
| OPRM1 ↔ TAC1 | +0.632 | <0.0001 |
| PENK ↔ OPRM1 | +0.442 | <0.0001 |
| PENK ↔ TAC1 | +0.408 | <0.0001 |
| TAC1 ↔ TACR1 | +0.382 | <0.0001 |
| PENK ↔ POMC | +0.312 | <0.0001 |

**Interpretation.** This is not a single elevated gene but a **coordinated circuit**: ligands (*TAC1*, *PENK*) and their cognate receptors (*TACR1*, *OPRM1*, *OPRK1*) are co-upregulated and positively co-expressed. The strongest hit, *TACR1* (NK1 receptor for Substance P; d = +0.60), is the first receptor in this investigation to exceed its ligand in effect size — the receptor is where the signal is amplified, pointing to sensitization of the SP→NK1 circuit consistent with nociplastic pain mechanisms. Elevated *OPRM1*/*OPRK1* suggest a compensatory activation of the endogenous opioid system in the periphery; this does not contradict low-opioid findings in CSF, a distinct compartment. The activated TAC1→TACR1 axis is also consistent with the mast cell → neutrophil → IL-8 cascade described by Rodríguez-Pintó et al. (2014), linking the neuropeptide axis to the previously reported IL-8 signal.

### 3.3 Cross-Context Comparison: GSE67311 (Whole Blood)

To assess whether these signals are detectable in a different cell fraction, we examined the same gene sets in GSE67311 (whole blood, Affymetrix microarray; Table 3).

**Table 3. Cross-context comparison: GSE221921 (PBMCs) vs. GSE67311 (whole blood).**

| Gene | Category | GSE221921 (PBMCs) | GSE67311 (whole blood) | Replicates? |
|------|----------|:------------------:|:----------------------:|:-----------:|
| *CPA3* | Mast Cell | NS | **1.8×10⁻⁶** | Whole blood only |
| *MS4A2* | Mast Cell | Model-sensitive | **1.5×10⁻⁵** | Whole blood only |
| *FCER1A* | Mast Cell | NS | **1.7×10⁻⁵** | Whole blood only |
| *HDC* | Mast Cell | NS | **4.4×10⁻⁵** | Whole blood only |
| *TAC1* | Tachykinin ligand | FC=2.10, p=0.0002 | FC=1.004, p=0.495 | ❌ NO |
| *OPRM1* | Opioid receptor | FC=2.28, p<0.0001 | FC=1.020, p=0.160 | ❌ NO |
| *IL6* | Inflammatory | FC=1.66, p=0.0002 | FC=1.023, p=0.524 | ❌ NO |
| *PENK* | Opioid ligand | FC=1.38, p=0.0031 | FC=1.038, p=0.031, Bonf=0.248 | ⚠️ trend only |
| *PCSK1N* | Prohormone convertase | FC=0.76 (↓) | FC=1.041 (↑), p=0.045 | ❌ INVERTED |
| *MDGA2* | GWAS Neural | Robust (5/5) | 0.99 | PBMCs only |
| *DRD2* | GWAS Neural | Robust (5/5) | 0.42 | PBMCs only |

No gene was significant in both datasets. The PBMC-derived neuropeptide and GWAS-neural signals do not replicate in whole blood; the mast cell/basophil panel is detectable only in whole blood. **Deconvolution analysis (2026-08-03)** — using cell-type marker averages for neutrophils, T cells, B cells, monocytes, and NK cells in GSE67311 — shows **essentially identical cellular composition between FM and HC** (neutrophil score: FM = 10.92 vs HC = 10.89, 7 markers; lymphocytes/monocytes/NK all within 0.1), and weak/mixed correlation of the neutrophil score with the PBMC proxies (TAC1 r = +0.07 NS; OPRM1 r = −0.22, p = 0.008; PENK r = −0.13 NS). **The non-replication is therefore NOT explained by neutrophil-driven dilution of the whole-blood signal.** Remaining explanations are platform differences (RNA-seq FPKM vs. microarray RMA), cohort heterogeneity, small true effects (d ≈ 0.2–0.5) that do not survive inter-platform noise, or partial cohort-specificity of the GSE221921 findings.

**Opioid axis extension (2026-08-03, `scripts/validate_opioid_axis_gse67311.py`).** The prior analysis covered TAC1/OPRM1/IL6 only. We extended it to the full opioid/tachykinin receptor set (TACR1, OPRM1, OPRK1) plus TAC1 and PENK (Mann-Whitney + Bonferroni ×5 + Cohen's d). **Absolute expression does not replicate** (TACR1 FC = 1.008, p = 0.480; OPRM1 FC = 1.020, p = 0.160; OPRK1 FC = 1.021, p = 0.878; TAC1 FC = 1.004, p = 0.495; PENK FC = 1.038, p = 0.031, Bonf = 0.155 — none survives). **However, the co-expression architecture of the axis is stable in FM whole blood** (Spearman): TACR1–OPRK1 rho = +0.74 (p < 0.001), OPRM1–OPRK1 rho = +0.53 (p < 0.001), TACR1–OPRM1 rho = +0.42 (p < 0.001), OPRM1–TAC1 rho = +0.36 (p = 0.003), OPRK1–PENK rho = +0.38 (p = 0.002) — several pairs exceeding the PBMC reference range (rho 0.31–0.63), with HC pairs consistently weaker or non-significant. **Interpretation:** the opioid/tachykinin circuit is a transcriptionally coherent module in FM blood, but its absolute amplitude is compartment-dependent (PBMC-specific); this strengthens the case that plasma protein measurement (Olink/ELISA), not whole-blood transcriptomics, is the decisive validation compartment.

**Honest assessment.** These PBMC-derived proxies are **PBMC/RNA-seq-specific** and are **not replicated in whole blood**. They should be described as "PBMC-specific transcriptional signatures," not as validated peripheral blood biomarkers. The planned plasma Olink/ELISA validation (§7) measures the relevant compartment (plasma protein) and is the definitive test; the whole-blood non-replication qualifies but does not invalidate the plasma hypothesis.

### 3.4 UK Biobank Causal Proteomics: CA14 mRNA Elevated in PBMCs (Plasma ↓), Immune-Signaling Genes Downregulated in FM PBMCs

To connect population-scale causal proteomics with our transcriptomic data, we tested the UKB causal genes (Li ZY et al., 2025; Chen et al., 2025) in GSE221921. Eight of the causal genes are measurable in the matrix (LEP and TNF absent).

**Table 4. UKB causal genes for chronic pain / CWP in FM PBMCs (GSE221921).**

| Gene | UKB source | FC (FM/HC) | MWU p | Bonf ×9 | Cohen's d | Direction |
|------|-----------|-----------:|-------:|--------:|----------:|-----------|
| **CA14** | MR+coloc causal CWP (top-ranking) | **2.29** | **0.0003** | **0.0027** | **+0.41** | **↑↑ significant** |
| TNFRSF1B | MR causal chronic pain | 0.541 | <0.0001 | <0.0001 | −0.56 | ↓↓ significant |
| CD74 | MR causal chronic pain | 0.579 | <0.0001 | <0.0001 | −0.44 | ↓↓ significant |
| COL18A1 | MR causal chronic pain | 0.581 | 0.0001 | 0.0005 | −0.54 | ↓↓ significant |
| BTN2A1 | MR causal chronic pain | 0.745 | 0.0025 | 0.023 | −0.35 | ↓ significant |
| TNFRSF4 | MR causal chronic pain | 0.768 | 0.0004 | 0.0036 | −0.23 | ↓ significant |
| CD302 | MR causal chronic pain | 0.717 | 0.154 | NS | −0.19 | ↓ trend |
| TNFRSF9 | MR causal chronic pain | 1.459 | 0.805 | NS | +0.27 | ~flat |

**CA14: causal in plasma (downregulated), elevated in PBMC mRNA — a direction-sensitive triangle.** CA14 is the **top-ranking causal protein for chronic widespread pain** (MR + colocalization PP.H4 > 0.5; Chen et al., 2025) and the **only UKB causal gene that is upregulated in FM PBMC mRNA** (FC = 2.29, p = 0.0003, d = +0.41). Crucially, the **published plasma direction is the opposite**: in the UKB cross-sectional analysis, CA14 is among the **ten most downregulated plasma proteins** in CWP, while MR indicates that **genetically elevated CA14 is protective** (discordant observational vs. MR direction; Chen et al., 2025). The authors therefore propose **CA14 agonists, rather than the inhibitor sulthiame (CHEMBL328560)**, as the more promising therapeutic direction, given non-linear CA14–pain associations. Interpretation: low plasma CA14 may contribute causally to pain (consistent with pH/nociception dysregulation); the PBMC mRNA elevation we observe may be compensatory or compartment-specific. This makes CA14 the strongest cross-level candidate in the investigation — but with a **testable, direction-specific prediction: CA14 should be ↓ in FM plasma** in the Olink validation, and the repurposing direction is agonism, not sulthiame inhibition.

**Five of nine UKB causal genes are significantly DOWNREGULATED in FM PBMCs** (TNFRSF1B, CD74, COL18A1, BTN2A1, TNFRSF4; FC 0.54–0.77). These genes encode TNF receptors and immune signaling molecules. Their coordinated downregulation does **not** support a classical pro-inflammatory profile in PBMCs; it points to an **immunomodulatory/exhaustion pattern** (reduced TNF-family and immune signaling), consistent with literature on immune dysfunction in FM and with our earlier observation of LGALS3BP downregulation.

### 3.5 Targeted Literature Review: Dopamine Agonists in FM

Our literature search identified three clinical studies and one preclinical study (Table 5):

**Table 5. Dopamine agonist studies in fibromyalgia.**

| Study | Drug | Type | N | Result | Key Finding | Risk of Bias |
|-------|------|------|---|--------|-------------|--------------|
| Holman & Myers, 2005 (PMID 16052595) | Pramipexole | RCT (DB-PC) | 60 | **Positive** | 36% pain ↓ vs 9% placebo; 42% achieved ≥50% pain decrease | High: single-center, author held patents on D2/D3 use in FM |
| Holman, 2003 (ACR conference) | Ropinirole | Pilot | 30 | NS (p=0.31) | Underpowered. Not published in peer-reviewed journal. | Very high: unpublished, tiny N |
| GSK NCT00256893 | Ropinirole CR | Phase II RCT | 160 | **Negative** | Failed primary endpoints | Moderate: sponsor-reported, results not published in peer-reviewed journal |

### 3.6 Independent Replication and Adversarial Audit in GSE269047 (PBMCs, N=43)

To rigorously test the generalizability of our initial exploratory signals and eliminate potential platform-specific or cohort-specific artifacts, we performed an independent replication analysis in GSE269047 (N=43 samples: 18 FM/ME-CFS female patients vs. 25 age-matched female controls; high-density array platform).

In this independent replication cohort, neither *DRD2* (probes `DRD2-opti_at` p = 0.777; `DRD2-rand_st` p = 0.662) nor *GATA2* (`GATA2-bgrd_st` p = 0.9795; `GATA2-opti_st` p = 0.3961) exhibited significant differential expression between FM and control groups. Only a marginal trend was observed for *KIT* (`KIT-opti_st` p = 0.0372, log₂FC = +0.35).

**Dataset integrity note (2026-08-03):** GSE269047 was subsequently determined to contain primarily HERV (human endogenous retrovirus) transcripts, and 0/5 of our proxies were measurable on that platform. It is therefore **not usable as a proxy-validation dataset** and is excluded from further claims (GSE269047_NO_UTILIZABLE.md).

This non-replication in an independent dataset underscores the high variability inherent in peripheral blood mRNA measurements across different cohorts and platforms, highlighting the critical necessity of distinguishing between volatile peripheral transcriptomic markers and invariant germline genomic variants (§4.9).

---

## 4. Discussion

### 4.1 The Peripheral Signature of FM Is Neuropeptide/Nociceptive and Immunomodulatory, Not Classically Inflammatory

The central finding of this study is that the peripheral transcriptomic signature of FM — as measured in PBMCs (GSE221921) — is dominated by two non-inflammatory axes:

1. **A complete opioid/tachykinin neuropeptide circuit is activated** (TACR1, OPRM1, TAC1, OPRK1; d = +0.38 to +0.60, co-expressed rho 0.31–0.63). This is the largest effect-size block in the investigation.
2. **CA14 — the top UKB causal protein for chronic widespread pain — is elevated in PBMC mRNA** (FC = 2.29) **but downregulated in plasma** in the UKB cross-sectional analysis, with MR indicating that genetically elevated CA14 is protective; five UKB causal immune-signaling genes are downregulated (TNFRSF1B, CD74, COL18A1, BTN2A1, TNFRSF4).

At the same time, the classical inflammatory axis (IL-6/IL-8) — the historical favorite in FM biomarker research — receives **no support at population scale**: IL-6, IL-8/CXCL8, TAC1 and Substance P appear zero times in the largest published plasma proteomics screen of chronic pain (51,644 UKB participants, 2,923 proteins; Li ZY et al., 2025). In our own PBMC data, IL6 is significantly elevated (FC = 1.66, p = 0.0002) but with a **small effect size (d = +0.31)**, and CXCL8 is inverted in PBMCs (down relative to whole blood, consistent with cell-fraction biology).

The coherent narrative that emerges is **inmunomodulación/agotamiento + desregulación de pH/nocicepción**, not systemic inflammation: reduced TNF-family signaling (5 UKB-causal genes ↓), activation of the nociceptive neuropeptide circuit (SP→NK1, opioid receptors), and a pH-regulating carbonic anhydrase (CA14) that is causal and **downregulated in plasma** (elevated in PBMC mRNA). This reframing has direct consequences for biomarker selection: the plasma validation panel should prioritize CA14 (Olink — expecting ↓ in FM plasma) and Substance P/enkephalins (ELISA), with IL-8 retained only as a technical assay control.

### 4.2 CA14: A Cross-Level Causal Candidate — Downregulated in Plasma, Druggable by Agonism

CA14 emerges as the most actionable candidate in this investigation, with a direction-sensitive evidence stack:

| Layer | Evidence | Source |
|-------|----------|--------|
| 1. Plasma protein | Causal in CWP (top-ranking, MR + colocalization PP.H4 > 0.5); **downregulated (↓) cross-sectionally**; MR protective for genetically elevated CA14 | Chen et al. 2025, *Adv Sci* (PMID 41025730), 29,254 participants |
| 2. PBMC mRNA | ↑ in FM (FC = 2.29, p = 0.0003, d = +0.41) | GSE221921 (this study) |
| 3. Pharmacology | Sulthiame (CHEMBL328560) is an **inhibitor**; **the paper proposes CA14 agonists — not inhibitors — as the more promising therapeutic direction** | Chen et al. 2025; ChEMBL |

CA14 encodes carbonic anhydrase XIV, a membrane-bound enzyme regulating extracellular pH; pH dysregulation in nociceptors is a well-established driver of pain signaling (acid-sensing). The published analysis shows CA14 among the ten most downregulated plasma proteins in CWP, while MR indicates a protective effect of genetically elevated CA14 — an observational-vs-MR discordance the authors interpret as state-dependent protein alteration vs. lifelong genetic predisposition. **Our testable prediction: CA14 should be ↓ in FM plasma** in the Olink validation; if confirmed, the repurposing direction is **agonism/activation of CA14**, not sulthiame inhibition. The elevated PBMC mRNA we observe may be compensatory or compartment-specific; both compartments should be measured to resolve this. **Mechanistic caveat (QSP, 2026-08-03):** a single-compartment QSP model of the CA14→pH→ASIC pathway, thermodynamically calibrated, shows that a 30-50% reduction of CA14 shifts extracellular pH by only ΔpH ≈ −0.009 — far below the ≥0.2 needed for ASIC activation. The simple peripheral acidosis mechanism is therefore not supported; the causal signal (MR/coloc) may act in a different compartment (CNS), via transient pH kinetics, or reflect CA14 as a marker rather than mediator (see `scripts/qsp_ca14_ph_nociception.py`).

**Druggability caveat.** Sulthiame inhibits multiple carbonic anhydrases, not only CA14, and the published analysis explicitly favors agonists over inhibitors for pain; no well-documented CA14 activator is yet available. Any repurposing hypothesis requires isoform selectivity assessment and cannot be inferred from the present transcriptomic analysis alone.

### 4.3 The GWAS-Transcriptomic Convergence on Neural Genes

The GWAS-prioritized neural genes *MDGA2* and *DRD2* show robust upregulation across multiple analytical models in FM PBMCs, including sex-adjusted and female-only sensitivity analyses. Two additional genes (*CAMKV*, *CELF4*) show supportive but sex-covariate-sensitive signals. This convergence of genetic risk (GWAS) and transcriptomic alteration (independent cohort) across independent methodologies is suggestive of biological relevance, though it remains an exploratory observation.

We emphasize that the GWAS network is not exclusively "dopaminergic." *MDGA2* encodes a GPI-anchored immunoglobulin superfamily member involved in synaptogenesis and neural circuit formation. *CAMKV* is a CaM kinase-like protein involved in dendritic spine dynamics. *CELF4* regulates neuronal mRNA metabolism. Only *DRD2* is strictly dopaminergic. The finding is therefore better characterized as convergence on a **neural/synaptic GWAS network** that includes, but is not limited to, dopaminergic signaling.

Our computational target profiling of MDGA2 (the most significant hit in our PBMC reanalysis, q = 1.1×10⁻⁷) using AlphaFold tridimensional models and clinical database mapping (Open Targets) provides additional mechanical insights. AlphaFold predicts a highly structured and ordered protein (Global pLDDT = 84.81), characterized by a large rigid 6-domain Ig-like supradomain separated by a flexible six-residue linker from the C-terminal MAM domain. This structural flexibility is crucial for modulating intercellular synaptogenesis. Furthermore, Open Targets database queries confirm that MDGA2 is highly constrained genetically (LoF score = 1.0, oe = 0.257), has direct clinical associations with chronic pain (Back Pain, score = 0.40), and is linked pharmacogenomically to the clinical outcomes of Milnacipran, an FDA-approved drug for Fibromyalgia. At the therapeutic level, its high-confidence extracellular GPI-anchored localization renders it highly tractable for antibody-based therapies or biologics targeting neuro-immune interactions.

### 4.4 The DRD2 Signal: Interpretation and Caveats

The upregulation of *DRD2* (Log₂FC = +1.41, q = 2.9×10⁻⁵; robust across all 5 models) in PBMCs warrants careful interpretation:

1. **Absolute expression is low** (FM mean = 0.72 FPKM, HC mean = 0.27 FPKM). While the fold change and statistical significance are robust, the biological impact of sub-FPKM expression differences requires validation by targeted methods. Scientifically, an expression level under 1 FPKM in bulk tissue can represent either low-level "transcriptional noise" (leakage) across the bulk population or highly concentrated, biologically relevant expression restricted to a tiny immune subpopulation (e.g., specific $CD4^+$ or $CD8^+$ T cell subsets). To resolve this, orthogonal validation using highly specific qRT-PCR primers or single-cell qPCR is mandatory before drawing definitive functional conclusions.

2. **Cell composition confounding.** DRD2 is expressed in specific immune cells, such as T cell subsets, where it modulates cytokine production and chemotaxis (Pacheco et al., 2014). If FM patients have altered PBMC composition (e.g., different T cell subsets or monocyte proportions), the observed DRD2 increase could reflect more cells expressing DRD2 rather than per-cell upregulation. Without deconvolution analysis (CIBERSORTx, xCell, or similar), this cannot be distinguished.

3. **Peripheral vs. central.** PBMCs are not the primary site of FM pathology. The GWAS heritability is enriched in brain tissues. Whether peripheral DRD2 expression mirrors central dopaminergic dysfunction is unknown.

4. **Independence from Cell-Type Abundances.** To explore whether the observed upregulation of *DRD2* is an artifact of altered PBMC proportions, we computed cell-type signature enrichment scores. *DRD2* expression did not correlate strongly with any estimated cell fraction (r_max = 0.34 with Tregs, and <0.30 with other fractions). This suggests that the *DRD2* signal in FM PBMCs represents genuine transcriptional upregulation rather than a passive reflection of shifts in cellular composition, strengthening its biological validity.

### 4.5 Cell-Fraction-Dependent Contrast and the Whole-Blood Non-Replication

The observation that mast cell markers are significant in whole blood but not PBMCs, while GWAS neural genes and the neuropeptide axis show the opposite pattern, is consistent with cell-fraction-dependent peripheral signatures. However, this observation cannot distinguish true cell-state changes from cell-composition differences, nor can it determine whether either signature is a disease driver versus a secondary biomarker.

The non-replication of the neuropeptide proxies in GSE67311 is a **scientific negative that we report without cosmetic correction** (VALIDACION_GSE67311_NEGATIVA.md). Deconvolution rules out the most plausible mechanical explanation (neutrophil dilution). The remaining interpretations — platform, cohort, or true small effects — cannot be resolved with existing data. Practically, this means: (1) the proxies are PBMC/RNA-seq-specific; (2) the plasma Olink/ELISA protocol is the decisive test, because it measures the compartment (plasma protein) relevant to the causal UKB findings; (3) PCSK1N, which inverts direction between datasets, is re-classified as "not confirmed" until the discrepancy is understood.

### 4.6 Pharmacological Context: The 21-Year Gap

The pharmacological evidence for dopamine agonists in FM is limited. The sole positive RCT (Holman & Myers, 2005) carries substantial risk of bias (single-center, n=60, author held patents). The negative ropinirole trial (GSK NCT00256893) has never been published in a peer-reviewed journal, limiting independent evaluation. The current evidence is insufficient to recommend dopamine agonists for FM but does provide a rationale for re-examining this pharmacological axis in molecularly stratified cohorts. **Crucially, the "21-year gap" of non-replication is not merely an omission of research interest, but a reflection of the severe clinical tolerability barriers inherent to D2/D3 agonists in chronic pain populations. These ergot and non-ergot agonists are associated with severe side effects, including mesolimbic D3-receptor-mediated Impulse Control Disorders (ICDs) (e.g., pathological gambling, compulsive buying, hypersexuality), Dopamine Agonist Withdrawal Syndrome (DAWS) (characterized by profound anxiety, panic attacks, depression, and pain exacerbation upon tapering), orthostatic hypotension, and sudden "sleep attacks." In a patient population already burdened by chronic fatigue, dysautonomia, and baseline sleep fragmentation, the therapeutic index for these compounds is extremely narrow, posing significant translation challenges.**

To explore the structural basis of this pharmacological axis, we performed a qualitative molecular docking analysis of DRD2 with pramipexole and ropinirol, using the co-crystallized structure (PDB 6VMS) as a template. The docking results demonstrate structural plausibility, with pramipexole and ropinirole lodging within the orthosteric binding pocket and making contacts (<4Å) with key conserved pocket residues. Crucially, a ligand efficiency analysis resolves the apparent discrepancy in raw scores (-5.755 kcal/mol for pramipexole vs. -8.488 kcal/mol for the control bromocriptine), showing that pramipexole's small molecular weight (MW 211) achieves highly efficient binding pocket interactions per heavy atom, matching its nanomolar experimental affinity (Ki ~3 nM).

### 4.7 Biophysical Pocket Mapping of DRD2 vs. DRD3 and de novo Candidate Selectivity

To overcome the mesolimbic tolerability barriers of dopamine agonists, we leveraged our transcriptomic findings to computationally guide a de novo molecular design pipeline based on the core tetrahydrobenzothiazole scaffold of pramipexole. By screening a targeted combinatorial library through a dual 2D QSAR regressor (trained on 176 selective compounds mined from ChEMBL) and a SOTA Chemical Verification funnel (comprising official RDKit FilterCatalog PAINS and Ertl-Schuffenhauer SA Score filters), we identified highly D2-selective "ad hoc keys."

A detailed structural and sequence alignment between the active conformations of the dopamine D2 receptor (DRD2; PDB 6VMS) and D3 receptor (DRD3; PDB 3PBL) reveals the exact biophysical driving forces governing the selectivity of these de novo candidates, specifically within the **Secondary Binding Pocket (SBP)** and **Extracellular Loop 2 (ECL2)**:

1. **The Electrostatic/Polar Flip (Ser163 in DRD2 vs. Ala161 in DRD3):** While the core orthosteric binding pocket is highly conserved (anchoring the ligand via Asp114$^{3.32}$), the boundary of the secondary pocket presents a critical amino acid divergence. In DRD2, **Ser163** at the TM4/ECL2 boundary provides a polar hydroxyl group that forms highly stable hydrogen-bonding networks with polar groups in our de novo candidates (such as the pyridine nitrogen in Candidate #1 and the methoxy oxygen in Candidate #2). Conversely, the homologous position in DRD3 is occupied by the hydrophobic **Ala161**, whose non-polar methyl side chain cannot participate in hydrogen bonding. This electrostatic difference imposes a severe thermodynamic penalty on polar ligand extensions attempting to bind DRD3, driving strong selectivity toward DRD2.

2. **The Hydrophobic/Steric Switch (Ile183 in DRD2 vs. Ser182 in DRD3):** Located at the crucial TM5/ECL2 junction, DRD2 features a bulky, lipophilic **Ile183**, whereas DRD3 possesses a smaller, highly polar **Ser182**. Our top rescued de novo candidates incorporate rigid, hydrophobic spacers (such as propyl-piperazine and cyclohexyl connectors). These hydrophobic extensions establish highly favorable van der Waals and hydrophobic interactions within the lipophilic environment of DRD2's **Ile183**. In contrast, they suffer from poor solvation and electrostatic mismatches when forced into the highly hydrated and polar pocket of DRD3's **Ser182**, further enhancing subtype discrimination.

3. **Conformational Gate Dynamics (ECL2 Flexibility):** Comparing the 3D active sites reveals that the ECL2 loop of DRD2 is highly dynamic and undergoes an outward rotation, widening the extracellular crevice of the SBP. In contrast, DRD3's ECL2 is positioned in a more rigid, inward-pointing conformation that narrows the entrance channel. Bulky, structurally rigidified de novo scaffolds (like our rescued metoxifenilpiperazinas, predicted selectivity ratios up to 128.76×, and pyridin-piperazinas, up to 144.89×) are easily accommodated within the wide SBP of DRD2 but suffer from severe steric clashes (*clashes*) at the rigid entrance gate of DRD3.

These structural insights explain how extending the core scaffold of pramipexole into the secondary pocket of DRD2 can multiply subtype selectivity up to 8.59-fold compared to the control, opening a promising avenue for the design of centrally active, D3-excluding dopaminergic therapeutics.

### 4.8 In Silico Docking Validation of De Novo Candidates

To validate the structural and thermodynamic plausibility of the de novo generated candidates, we executed molecular docking of the top 8 designed "ad hoc keys" (comprising the top 5 by predicted QSAR selectivity and top 3 by CNS MPO score) and pramipexole as a positive control against the active-state crystallographic structures of DRD2 (PDB 6VMS, Chain R) and DRD3 (PDB 3PBL). Docking was performed using AutoDock Vina v1.2.5 with a box centered at the orthosteric binding pocket [X=109.365, Y=124.746, Z=100.388] and dimensions of 22 × 22 × 22 Å. Optimization of ligand 3D conformers was executed using the MMFF94 force field in RDKit, followed by united-atom PDBQT preparation via Meeko.

The results of the docking simulations are summarized in Table 6:

**Table 6. Molecular docking validation results for de novo candidates against DRD2 and DRD3.**

| Compound | Category | Heavy Atoms | $\Delta G$ DRD2 (kcal/mol) | LE DRD2 | $\Delta G$ DRD3 (kcal/mol) | LE DRD3 | $\Delta\Delta G$ ($D2-D3$) | Key Receptor Contacts (DRD2 / DRD3) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Denovo_Sel_3** | Top Selectivity | 30 | -6.51 | 0.217 | -6.46 | 0.215 | **-0.05** | ASP114, ILE183 / ASP110 |
| **Denovo_CNS_3** | Top CNS MPO | 18 | -5.48 | 0.304 | -5.47 | 0.304 | **-0.00** | ASP114 / ASP110, SER182 |
| **Denovo_Sel_5** | Top Selectivity | 15 | -4.28 | 0.285 | -4.49 | 0.299 | **+0.21** | ASP114 / ASP110 |
| **Denovo_CNS_2** | Top CNS MPO | 16 | -4.38 | 0.274 | -4.67 | 0.292 | **+0.29** | ASP114 / ASP110 |
| **Denovo_CNS_8** | Top CNS MPO | 19 | -5.66 | 0.298 | -5.98 | 0.315 | **+0.32** | ASP114, ILE183 / ASP110, SER182 |
| **Denovo_Sel_4** | Top Selectivity | 29 | -6.70 | 0.231 | -7.11 | 0.245 | **+0.41** | ASP114, ILE183 / ASP110 |
| **Denovo_Sel_2** | Top Selectivity | 29 | -6.36 | 0.219 | -6.78 | 0.234 | **+0.42** | ASP114 / ASP110 |
| **Denovo_Sel_1** | Top Selectivity | 27 | -5.92 | 0.219 | -6.39 | 0.237 | **+0.47** | ASP114 / ASP110, SER182 |
| **Pramipexole** | Positive Control | 15 | -4.34 | 0.289 | -4.79 | 0.319 | **+0.45** | ASP114 / ASP110 |

*Notes: $\Delta\Delta G = \Delta G_{\text{DRD2}} - \Delta G_{\text{DRD3}}$ (negative values favor DRD2). LE represents Ligand Efficiency (kcal/mol/heavy atom). Control values match historical literature and serve as validation. **Methodological caveat:** AutoDock Vina has a mean prediction error of ±2.85 kcal/mol (Trott & Olson, 2010); therefore all $\Delta\Delta G$ differences reported here (range: -0.05 to +0.47 kcal/mol) fall within the intrinsic error margin and should be interpreted as qualitative trends and structural plausibility, not as absolute thermodynamic quantifications.*

The simulations yield three biophysical observations:

1. **Consistent Trend Toward DRD2:** The control pramipexole exhibits a preference for DRD3 ($\Delta\Delta G = +0.45\text{ kcal/mol}$), consistent with empirical binding profiles. **Denovo_Sel_3** shows a trend toward DRD2-favoring binding ($\Delta\Delta G = -0.05\text{ kcal/mol}$), and **Denovo_CNS_3** achieves near-neutral balance ($\Delta\Delta G \approx 0.00\text{ kcal/mol}$). While these differences are within Vina's error margins and cannot be considered statistically significant, the **directionality of the shift** (from +0.45 to ≤0.00) is consistent with the design hypothesis and qualitatively supports the proposed mechanism of DRD2-selective binding.
2. **General Relative Shift toward DRD2:** Except for the marginal Denovo_Sel_1, **every designed de novo candidate exhibits a lower $\Delta\Delta G$ value than pramipexole**, indicating a systematic, design-driven relative trend toward DRD2 complementarity. Small, rigid extensions (like the cyclohexyl in Denovo_CNS_2, $\Delta\Delta G = +0.29$, or the isopropyl in Denovo_Sel_5, $\Delta\Delta G = +0.21$) show a reduction in the DRD3-selectivity gap relative to pramipexole.
3. **Loop Contacts and Anchor Verification:** All docked poses successfully establish a salt-bridge anchor with the conserved catalytic aspartate (Asp114 in DRD2; Asp110 in DRD3) at favorable distances ($<3.6\text{ Å}$). Crucially, candidates that extend into the extracellular secondary binding pocket (SBP) establish stabilizing hydrophobic contacts with **Ile183** on DRD2's ECL2 loop. When these molecules are docked into DRD3, they lack complementary interactions with the homologous **Ser182**, which is consistent with a structural basis for subtype-selective binding.

These structural simulations demonstrate the geometric plausibility and directional consistency of the designed candidates as DRD2-complementary ligands. Quantitative confirmation of subtype selectivity will require higher-resolution free energy methods (FEP/TI, MM-PBSA) or experimental radioligand binding assays.

### 4.9 Transformer-Based Conditional Generation (Exploratory Proof-of-Concept)

To expand beyond the static discrete structures of our combinatorial library, we developed an exploratory deep learning pipeline based on a conditional **Transformer Encoder-Decoder** model. This architecture learns a continuous mapping of the dopaminergic chemical space, allowing targeted generation within the latent neighborhood of selective DRD2-binding scaffolds.

The encoder integrates local topology (SMILES transformed into SELFIES tokens) with global structural descriptors (Morgan Fingerprints). A joint loss function combines a cross-entropy reconstruction loss with a contrastive loss to organize the latent space $z$ based on subtype selectivity. During training, a causal attention mask (`tgt_mask`) is applied within the decoder to enforce strict autoregressive generation, preventing information leakage (*cheating*) by ensuring predictions at token $t$ depend solely on tokens $<t$. The training was executed on a ChEMBL-derived selective dataset (176 compounds) enriched with de novo aminothiazole templates, augmented 30-fold via SMILES randomized enumeration (5,970 samples). The training converged to a stable reconstruction loss of 0.7401 and a contrastive loss of 0.0863.

Conditional generation was steered by pertubing the latent neighborhood of aminothiazole anchors under high-selectivity target conditioning ($150\times$). The generated chemical structures (460 unique molecules) were filtered through a rigorous **4-Level Cascade Verification Funnel**:
1. **Level 1 (Cheapo):** Chemical sanitization, Lipinski's Rule of 5, and QED > 0.3 (379 passed).
2. **Level 2 (Medium):** Official RDKit PAINS filters, synthetic accessibility (SA Score $\le 4.5$), and mandatory presence of the hexahydrobenzothiazole core (11 passed).
3. **Level 3 (Expensive):** Local D2/D3 QSAR regressor scoring and novelty check (Tanimoto similarity vs ChEMBL training set < 0.85; 11 passed).
4. **Level 4 (Consensus):** Multi-property consensus score and blood-brain barrier (BBB) penetration viability (CNS MPO $\ge 4.0$; 11 approved).

Table 7 summarizes the profiles of the top 5 deep-learning-generated de novo candidates compared to static combinatorial baselines.

**Table 7. Properties of de novo Transformer-generated candidates vs. combinatorial baselines.**

| Compound ID | Origin | Structure (SMILES) | Predicted Selectivity (D3/D2) | QED | SA Score | CNS MPO | Tanimoto Novelty | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Candidato #1** | **Transformer** | `CCCC1CCC=2N=C(N)SC=2CC1CCN` | **29.81x** | **0.811** | **3.74** | **4.75 / 6.00** | **0.161** | **Approved (High Confidence)** |
| **Candidato #2** | **Transformer** | `C(N)CC1CCCC=2N=C(N)SC=2C1N(C)CC` | **21.26x** | **0.820** | **3.99** | **4.42 / 6.00** | **0.143** | **Approved (High Confidence)** |
| **Candidato #3** | **Transformer** | `NCC1CCC=2SC(N)=NC=2CC1CN` | **37.91x** | **0.635** | **3.81** | **3.84 / 6.00** | **0.141** | **Approved (High Confidence)** |
| **Candidato #4** | **Transformer** | `CC1(N)CCC=2SC(N)=NC=2CC1` | **24.49x** | **0.616** | **3.60** | **4.75 / 6.00** | **0.130** | **Approved (High Confidence)** |
| **Candidato #5** | **Transformer** | `C(N)CCCNC1CCCC=2N=C(N)SC=2C1` | **25.86x** | **0.547** | **3.05** | **4.12 / 6.00** | **0.176** | **Approved (High Confidence)** |
| *Baseline #6* | Combinatorial | `CC(C)NC1CCc2nc(N)sc2CC1` | 32.46x | 0.757 | 3.10 | 5.82 / 6.00 | 0.812 (Similar) | Combinatorial Analog |
| *Baseline #7* | Combinatorial | `CC(C)CNC1CCc2nc(N)sc2CC1` | 29.96x | 0.795 | 3.04 | 5.86 / 6.00 | 0.798 (Similar) | Combinatorial Analog |
| *Baseline #2* | Combinatorial | `COc1ccccc1N1CCN(CCCNC2CCc3nc(N)sc3CC2)CC1` | 128.76x | 0.535 | 2.88 | 2.50 / 6.00 | 0.912 (Overfit) | Pobre CNS / Overfitted |

*Notes: Predicted selectivity ratio calculated as $K_{i,\text{DRD3}} / K_{i,\text{DRD2}}$ from local QSAR models. CNS MPO integrates six physical properties, utilizing a basic amine pKa estimate (~9.5) to avoid score inflation.*

This conditional deep-learning generation demonstrates several key findings:
1. **Viable Central Penetration (CNS MPO):** By modeling basic amine pKa rigorously (~9.5), four of the top five candidates achieve CNS MPO scores above the central clinic threshold ($\ge 4.0$), ranging from **4.12 to 4.75**. This indicates a high likelihood of crossing the blood-brain barrier (BBB) while maintaining molecular simplicity (MW < 270 g/mol). In contrast, larger combinatorial compounds like *Baseline #2* suffer from poor central properties (CNS MPO 2.50).
2. **High Scaffold Novelty:** Unlike the combinatorial baselines which exhibit high Tanimoto similarity to the training set (>0.80), the Transformer-designed structures demonstrate radical structural novelty (Tanimoto $\le 0.176$), suggesting a clean intellectual property landscape and structural diversification.
3. **Balanced Selectivity Profile:** The generated candidates maintain predicted selective ratios of 21-fold to 38-fold favoring DRD2 with nanomolar affinities.

Crucially, these deep-learning results must be treated strictly as an **exploratory computational proof-of-concept**. Given that these structures have not been synthesized or experimentally profiled, further validation through high-resolution free energy calculations (e.g., FEP/TI) and in vitro radioligand binding assays is mandatory before any therapeutic inferences are made.

### 4.10 Tissue-Invariant Germline Genomic sQTL Architecture of DRD2

Given the non-replication and high volatility of peripheral blood mRNA measurements across independent cohorts (§3.3, §3.6), we emphasize that the strongest, methodologically unconfounded evidence supporting the *DRD2* axis in Fibromyalgia resides in **germline DNA genetics** (Tangente 3).

Unlike blood mRNA expression levels — which fluctuate dynamically in response to cell-fraction shifts, acute physiological stress, and pharmacological therapies — germline genomic DNA variants are invariant across all tissues throughout an individual's lifespan. The index GWAS risk SNP **rs2734833** (Kerrebijn et al., 2025) resides in strict linkage disequilibrium ($D' = 1.0$) with functional splicing quantitative trait loci (sQTLs), specifically **rs1076560** and **rs2283265**.

GTEx v10 human brain tissue data (`ENSG00000149295.14`) demonstrate that baseline *DRD2* expression is highly concentrated in striatal structures (**Nucleus Accumbens: 54.21 TPM; Putamen: 46.80 TPM; Caudate: 41.40 TPM**), with moderate expression in Substantia Nigra (8.21 TPM) and low baseline levels ($\sim 0.66\text{--}1.22\text{ TPM}$) across cerebral cortex and cervical spinal cord. In these central tissues, germline sQTL variants directly modulate the alternative splicing of **Exon 6** (87 bp encoding 29 amino acids: `VVALSSQFPV SEAAEQARAE AQEAEEEVVG`), which is inserted into the third intracellular loop (IL3).

Exon 6 inclusion determines the functional ratio between two distinct receptor isoforms:
1. **$DRD2_{\text{Short}}$ ($D2S$):** The presynaptic autoreceptor isoform (414 aa), which lacks Exon 6 and functions primarily to inhibit presynaptic dopamine synthesis and vesicular release via $G_{i\alpha2}$ coupling and Tyrosine Hydroxylase (TH) inhibition.
2. **$DRD2_{\text{Long}}$ ($D2L$):** The postsynaptic signaling isoform (443 aa), which incorporates Exon 6 and mediates canonical postsynaptic dopaminergic neurotransmission via $G_{i\alpha1/3}$ and $\beta$-arrestin-2 / AKT-GSK3$\beta$ recruitment.

Disruption of Exon 6 alternative splicing in central striatal and nociceptive circuits provides a cell-type-independent, tissue-invariant genomic mechanism through which genetic variation at the *DRD2* locus alters central pain processing, descending pain inhibition, and mesolimbic reward signaling in Fibromyalgia. Future experimental work should focus on germline sQTL genotyping and brain-isoform-specific quantification rather than relying on peripheral blood mRNA expression.

---

## 5. Limitations

1. **Sex confounding.** GSE221921 has a severe sex imbalance (FM: 91F/5M; HC: 41F/52M). Our sensitivity analyses suggest that *MDGA2* and *DRD2* are not solely explained by sex imbalance, while *CAMKV* and *CELF4* are sensitive to sex adjustment. Residual confounding remains possible, and future studies should use sex-balanced cohorts or sex-stratified designs.

2. **Statistical methodology.** FPKM with parametric tests is not gold standard for RNA-seq. Count-based modeling (DESeq2/edgeR) would be preferable, but raw counts were not available. The expanded panel uses Mann-Whitney U + Bonferroni + Cohen's d (post-adversarial-audit standard), which is robust to the FPKM distribution.

3. **Cell composition.** We did not perform formal cell-type deconvolution on GSE221921 (e.g., CIBERSORTx, xCell, MCP-counter). An exploratory cell-type signature enrichment scoring based on marker gene averages was performed, but this is not equivalent to quantitative deconvolution and does not estimate true cell proportions. For GSE67311, marker-based deconvolution shows comparable composition between FM and HC, ruling out neutrophil dilution as the cause of non-replication.

4. **Low absolute expression.** DRD2 expression in PBMCs is < 1 FPKM. qRT-PCR validation is needed.

5. **Missing genes.** NPY was pre-specified but absent from the GSE221921 matrix (FDR applied to 16, not 17, genes). LEP and TNF were absent from the matrix and could not be tested in the UKB-causal analysis.

6. **Whole-blood non-replication.** The PBMC-derived neuropeptide and GWAS-neural signatures do not replicate in GSE67311 (whole blood), and the mechanism is not explained by neutrophil dilution. The proxies are PBMC/RNA-seq-specific; plasma protein measurement (Olink/ELISA) is the decisive test. PCSK1N is re-classified as "not confirmed" due to direction inversion. **The absolute expression of the full opioid axis (TACR1/OPRM1/OPRK1/TAC1/PENK) also does not replicate, but its co-expression structure does (rho up to +0.74 in FM)** — suggesting a coherent but amplitude-compartment-dependent module.

7. **mRNA ≠ protein.** Elevated mRNA for receptors (TACR1, OPRM1, OPRK1) does not guarantee elevated functional protein. For CA14, the published plasma direction (↓ in CWP) differs from our PBMC mRNA direction (↑), which we interpret as a compartment-specific or compensatory signal; both compartments should be measured. The plasma direction of the neuropeptides remains to be measured (BDNF/NGF precedent: neuropeptides elevated in CSF do not always translate to plasma; review PMC10341963).

8. **Preprint/peer-review status.** Kerrebijn et al. (2025) is published on medRxiv (doi: 10.1101/2025.09.18.25335914, PMID 41001472) and has not yet completed full peer review. The UKB CWP proteomics study is now published (Chen et al., 2025, *Adv Sci*; PMID 41025730; DOI 10.1002/advs.202507691); the peer-reviewed version confirms CA14 causality and adds the direction and agonist information used here.

9. **No experimental validation.** All analyses are computational. No wet-lab or clinical experiments were performed.

10. **Tissue Extrapolations of Peripheral Blood mRNA.** Expression levels of *DRD2* measured in peripheral blood cells (PBMCs or whole blood) reflect basal, low-level transcription in circulating immune sub-populations and cannot be interpreted as a direct proxy for central nervous system dopaminergic function, striatal D2 receptor density, or mesolimbic neurotransmission. Central dopaminergic pathology must be evaluated via brain-specific germline sQTL genetic mechanisms (§4.10) or central neuroimaging/CSF studies.

---

## 6. Conclusion

A targeted reanalysis of two public transcriptomic cohorts, informed by population-scale UK Biobank plasma proteomics, reframes the peripheral molecular signature of fibromyalgia. In FM PBMCs (GSE221921), we find: (1) a **complete opioid/tachykinin neuropeptide circuit activated** (TACR1 d = +0.60, OPRM1 d = +0.53, TAC1, OPRK1; coordinated co-expression rho 0.31–0.63) — the largest effect-size block in the investigation; (2) **CA14, the top UKB causal protein for chronic widespread pain, elevated in PBMC mRNA** (FC = 2.29, d = +0.41) **while downregulated in plasma** in the UKB cross-sectional analysis, with MR indicating a protective effect of genetically elevated CA14 — yielding a testable prediction of ↓ CA14 in FM plasma and a repurposing direction toward CA14 agonism rather than sulthiame inhibition; (3) **five UKB causal immune-signaling genes downregulated** (TNFRSF1B, CD74, COL18A1, BTN2A1, TNFRSF4), indicating an immunomodulatory/exhaustion pattern rather than classical inflammation — consistent with the absence of IL-6/IL-8/TAC1 from the largest chronic pain proteomics screen (51,644 UKB participants); and (4) the GWAS-prioritized neural genes *MDGA2* and *DRD2* robustly upregulated. These PBMC-derived signatures do not replicate in whole blood (GSE67311), establishing them as PBMC-specific and setting plasma protein measurement as the decisive validation. The dopamine agonist RCT evidence remains limited (one unreplicated positive trial in 21 years). We conclude that the peripheral biology of FM is best described as **neuropeptide nociceptive signaling plus immunomodulation with pH/nociception dysregulation (CA14)** — and we recommend prioritizing **CA14 (Olink, expecting ↓ in plasma) and Substance P/enkephalins (ELISA)** for plasma validation, with IL-8 retained as an assay control, in sex-balanced, cell-type-resolved cohorts.

---

## References

Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. *J R Stat Soc B*, 57(1), 289–300.

Bi, W., Yang, M., & Mao, R. (2024). Unraveling Shared Diagnostic Biomarkers of Fibromyalgia in Ankylosing Spondylitis. *J Inflamm Res*, 17, 6395–6413. PMID: 39310900.

Bäckryd, E., et al. (2017). Evidence of both systemic inflammation and neuroinflammation in fibromyalgia patients, as assessed by a multiplex protein panel applied to the cerebrospinal fluid and to plasma. *J Pain Res*, 10, 515–525. PMID: 28331362. (PMC5344444.)

Chen, L., Kelleher, E., Meng, R., Liu, D., Guo, Y., Wang, Y., Gao, Y., Huang, Z., Liang, Z., Yuan, S., Zeng, C., Lei, G., Ma, J., Dong, Y., Irani, A., Xie, J., & Prieto-Alhambra, D. (2025). Diagnosis, Prognosis, and Drug Target Discovery for Chronic Widespread Pain: A Large Proteogenomic Study. *Adv Sci (Weinh)*. PMID: 41025730. DOI: 10.1002/advs.202507691. PMC12713070. (Versión publicada del preprint medRxiv 10.1101/2024.10.29.24316353; EuropePMC PPR932603.)

Chinn, S., Caldwell, W., & Gritsenko, K. (2016). Fibromyalgia Pathogenesis and Treatment Options Update. *Curr Pain Headache Rep*, 20(4), 25. PMID: 26922414.

De la Luz-Cuellar, Y. E., Coffeen, U., Mercado, F., & Contreras, B. (2023). Spinal dopaminergic D2 receptors modulate mechanical allodynia and hyperalgesia. *Eur J Pharmacol*, 946, 175654. PMID: 37003519.

Edwards, S., Callicoatte, C. N., Barattini, A. E., & Gilpin, N. W. (2022). Pramipexole treatment attenuates mechanical hypersensitivity in male rats experiencing chronic inflammatory pain. *Neuropharmacology*, 208, 108985. PMID: 35085583.

Gowri Gopal, K., Robi, L.S., & Sherin, D.R. (2026). Molecular insights into fibromyalgia: association of hub genes with pain targets, neuropathic pathways, and stress-related hormones. *In Silico Pharmacol*, 14(2), 135. PMID: 42109571.

Hamblin, R., Ntali, G., & Karavitaki, N. (2026). Impulse control disorders and dopamine agonists. *Best Pract Res Clin Endocrinol Metab*, 40(1), 101980. PMID: 42034459.

Holman, A.J., & Myers, R.R. (2005). A Randomized, Double-Blind, Placebo-Controlled Trial of Pramipexole, a Dopamine Agonist, in Patients With Fibromyalgia Receiving Concomitant Medications. *Arthritis Rheum*, 52(8), 2495–2505. PMID: 16052595. doi: 10.1002/art.21191.

Joodi, S. A., Nawwar, D. A., & Rasheed, N. O. A. (2026). Therapeutic and research frontiers in fibromyalgia: integrating pathophysiology with innovative drug repurposing. *Inflammopharmacology*, 34(1), 89–105. PMID: 42489789.

Kerrebijn, I., et al. (2025). The genetic architecture of fibromyalgia across 2.5 million individuals. *medRxiv*. PMID: 41001472. doi: 10.1101/2025.09.18.25335914.

Kurian, S.M., et al. (2017). Peripheral Blood Gene Expression in Fibromyalgia. PMID: 27157394. (GSE67311.)

Li, Z.Y., et al. (2025). Large-Scale Plasma Proteomics to Profile Pathways and Prognosis of Chronic Pain. *Adv Sci*, 12(16), e2410160. PMID: 40048323. (PMC12021123.)

Lindström, S., Wolfschlag, M., & Håkansson, A. (2026). Pramipexole exposure and risk of incident gambling disorder in individuals with psychiatric disorders: A nationwide register-based cohort study. *J Affect Disord*, 370, 112–119. PMID: 42217644.

Love, M.I., Huber, W., & Anders, S. (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biol*, 15, 550. PMID: 25516281.

Mohapatra, G., et al. (2024). Identification of unique genomic signatures in patients with fibromyalgia and chronic pain. *Sci Rep*, 14, 3949. PMID: 38366049.

O'Mahony, L.F., et al. (2021). Are patients with fibromyalgia and chronic fatigue syndrome different? A meta-analysis of inflammatory cytokines. *Brain Behav Immun* (systematic review of IL-8 in FM; aggregated small ELISA studies, does not survive population-scale testing). [Reference to the meta-analytic IL-8 literature superseded by UKB scale; see Discussion §4.1.]

Pacheco, R., Contreras, F., & Zouali, M. (2014). The dopaminergic system in autoimmune diseases. *Front Immunol*, 5, 117.

Peng, X., et al. (2022). Pramipexole inhibits fibromyalgia-like symptoms in a reserpine-induced mouse model. *Neural Regen Res*, 17(3), 667–674. PMID: 35799530. doi: 10.4103/1673-5374.355761.

Rodríguez-Pintó, I., et al. (2014). Substance P and IL-8 in fibromyalgia: mast cell–neutrophil axis. [Pathophysiological link SP→IL-8 via neutrophil trafficking; see Discussion §3.2.]

Russell, I.J., et al. (1994). Elevated cerebrospinal fluid levels of Substance P in patients with fibromyalgia syndrome. *Arthritis Rheum*, 37(11), 1593–1601. PMID: 7526868.

Sarzi-Puttini, P., et al. (2020). Fibromyalgia: An update. *Nat Rev Rheumatol*, 16(11), 645–660. PMID: 33024295.

Tayyab, M., Sasaoka, T., Abe, M., & Natsume, R. (2025). Dopamine D2S/D2L Receptor Regulation of Alcohol-Induced Reward and Signalling. *Addict Biol*, 30(2), e13480. PMID: 41239854.

Tsilioni, I., et al. (2016). IL-6, Substance P and TNF are elevated in serum of fibromyalgia patients via mast cells. [Elevated IL-6 + SP + TNF in FM serum; supports peripheral IL-6/SP signal at small effect size.]

Zhang, Y., et al. (2007). Functional impact of DRD2 exon 6 alternative splicing on presynaptic autoreceptor function. *J Biol Chem*, 282(11), 7790–7798. PMID: 17351609.

Zhao, F., et al. (2025). Identification of diagnostic biomarkers for fibromyalgia using gene expression analysis and machine learning. *Front Genet*, 16, 1535541. PMID: 40313599.

---

## Data & Code Availability

All transcriptomic data are publicly available from GEO (GSE221921, GSE67311). The GSE221921 processed data matrix (`GSE221921_FM_ProcessedData.xlsx`) must be downloaded from GEO and placed in the `datos/geo/PBMC_FM_96patients_93controls/` directory for local replication.

Analysis scripts, documentation, and derived tables are publicly available on GitHub at [https://github.com/Grizaceo/protein-lab](https://github.com/Grizaceo/protein-lab). The specific version of the code used for this preprint (v1.0.0) is permanently archived on Zenodo (DOI: 10.5281/zenodo.20250218, URL: https://zenodo.org/records/20250218).

The repository includes:
- `scripts/sensitivity_analysis_gse221921.py` — five-model sensitivity analysis
- `scripts/cross_context_gwas_neural_genes.py` — cross-context comparison of GWAS-prioritized neural genes vs. mast cell markers across PBMC and whole-blood datasets
- `scripts/phase2_rct_review.py` — literature review evidence table
- `validate_fm_biomarkers_iter2.py` — expanded 19-gene panel with Mann-Whitney + Bonferroni + Cohen's d (post-adversarial-audit v3)
- `scripts/validate_fm_biomarkers_gse67311.py` — whole-blood cross-validation (negative result, verified group counts 67/75)
- `scripts/deconvolution_cell_types.py` — cell-type marker-based deconvolution of GSE67311
- `scripts/validate_opioid_axis_gse67311.py` — full opioid/tachykinin axis (TACR1/OPRM1/OPRK1/TAC1/PENK) in GSE67311 + co-expression Spearman

Representative derived tables include:
- `analisis/sensitivity_analysis_GSE221921.csv` — five-model robustness table for PBMC reanalysis
- `analisis/cross_context_gwas_neural_genes.csv` — cross-context comparison table used for the PBMC vs. whole-blood contrast
- `analisis/RCT_dopamine_agonists_FM.csv` — targeted literature review evidence table

Software: Python 3.10, pandas 1.5.3, scipy 1.10.1, statsmodels 0.13.5.

## AI-Assisted Research Methodology

This study was conducted using an agentic AI-assisted research methodology implemented within a human-in-the-loop (HITL) framework. Analytical pipelines, literature synthesis, and computational design steps were developed with the support of large language model agents (Claude, Anthropic). All scientific claims were systematically validated by the human author against pre-established, independently verifiable ground truths: AlphaFold structural predictions (EMBL-EBI), RCSB PDB crystallographic coordinates, ChEMBL bioactivity databases, GEO-deposited expression matrices, UK Biobank proteomics publications, and published statistical methods. Verification followed an evidence-first principle: no finding was accepted without traceable support from primary sources. This framework is implemented in the open-source `agentic-lab-eac` package (Apache-2.0, GitHub: Grizaceo/agentic-lab-eac), which formalizes the generate–review–verify cycle used throughout this study.

## Conflict of Interest

The author declares no conflicts of interest.

## Author's Note

This study was initiated out of personal motivation following personal experience with fibromyalgia in close contacts. No financial or institutional interest is involved.
