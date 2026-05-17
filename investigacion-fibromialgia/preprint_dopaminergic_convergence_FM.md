# GWAS-Prioritized Neural Genes Are Differentially Expressed in Fibromyalgia PBMCs: A Targeted Reanalysis of Public Transcriptomic Cohorts

---

**Authors:** [To be determined]

**Preprint — Draft v2.0 — May 2026**

---

## Abstract

Fibromyalgia (FM) is a prevalent chronic pain condition whose molecular basis remains poorly defined. A recent genome-wide association study (GWAS) meta-analysis of 2.5 million individuals identified 26 risk loci enriched in brain tissues, prioritizing neural and synaptic genes including *DRD2*, *MDGA2*, *CAMKV*, and *CELF4* (Kerrebijn et al., 2025; PMID 41001472). Whether these GWAS-prioritized genes show altered expression in FM patients has not been directly tested. Here, we perform a targeted, hypothesis-driven reanalysis of two public transcriptomic datasets — GSE221921 (PBMCs, 96 FM / 93 HC) and GSE67311 (whole blood, 70 FM / 70 HC) — interrogating 13 GWAS neural genes alongside a 4-gene mast cell marker panel. In GSE221921, *MDGA2* (q = 1.1×10⁻⁷) and *DRD2* (q = 2.9×10⁻⁵) were robustly upregulated across all five sensitivity models tested (Welch t-test on raw FPKM and log₂-transformed data, Mann-Whitney U, OLS with sex covariate, and female-only subgroup analysis). *CAMKV* and *CELF4* were significant in four of five models but did not survive sex-covariate adjustment in the full cohort, which has a severe sex imbalance (FM: 91F/5M; HC: 41F/52M). In GSE67311 (whole blood), only the mast cell panel was significant — revealing a cell-fraction-dependent contrast between granulocyte and PBMC signatures. A targeted literature review identified a single positive RCT for a dopamine agonist in FM (pramipexole; Holman & Myers, 2005; PMID 16052595), unreplicated in 21 years. These exploratory findings support prioritizing the DRD2/neural GWAS axis for validation in sex-balanced, cell-type-resolved cohorts.

**Keywords:** fibromyalgia, DRD2, GWAS, transcriptomics, PBMCs, neural genes, pramipexole, targeted reanalysis

---

## 1. Introduction

Fibromyalgia (FM) affects 2–4% of the global population, manifesting as chronic widespread pain, fatigue, cognitive dysfunction, and sleep disturbances (Sarzi-Puttini et al., 2020). Despite its prevalence, FM lacks specific diagnostic biomarkers and its pharmacotherapy remains limited to three FDA-approved medications — pregabalin, duloxetine, and milnacipran — none designed to target FM-specific molecular pathology (Chinn et al., 2016).

A recent GWAS meta-analysis by Kerrebijn and colleagues, comprising 54,629 cases and 2,509,126 controls across 11 cohorts, identified 26 genome-wide significant risk loci for FM, with heritability enriched exclusively in brain tissues and neuronal cell types (Kerrebijn et al., 2025; PMID 41001472; medRxiv doi: 10.1101/2025.09.18.25335914v1). The prioritized genes span dopaminergic signaling (*DRD2*), synaptic plasticity (*CAMKV*, *CELF4*), neural cell adhesion (*NCAM1*, *MDGA2*), axon guidance (*DCC*), and other neural functions (*GPR52*, *HTT*). While the GWAS authors describe these as a neural/CNS network, we note that only *DRD2* is strictly dopaminergic; the others are more broadly neural or synaptic.

This genetic architecture motivates a direct question: **are these GWAS-prioritized genes differentially expressed in FM patients?** Several bioinformatic studies have analyzed the GSE221921 PBMC dataset (Mohapatra et al., 2024; Bi et al., 2024; Zhao et al., 2025; Gowri Gopal et al., 2026), but all employed unbiased genome-wide approaches (DEG → PPI → hub genes). None tested the specific hypothesis that the GWAS-defined gene set is coordinately altered — a targeted, hypothesis-driven analysis that is distinct from and complementary to unbiased discovery.

In this study, we: (1) test the GWAS neural gene set for differential expression in PBMCs (GSE221921) and whole blood (GSE67311), including comprehensive sensitivity analyses for sex confounding; (2) include a negative control panel of mast cell markers; and (3) contextualize our findings with a targeted literature review of dopamine agonist trials in FM.

---

## 2. Methods

### 2.1 Gene Set Definition

**GWAS-Prioritized Neural Gene Set.** We extracted 13 genes from the 26 GWAS risk loci reported by Kerrebijn et al. (2025) that are functionally linked to neural or synaptic signaling: *DRD2*, *NCAM1*, *GPR52*, *CAMKV*, *CELF4*, *DCC*, *MDGA2*, *NPY*, *KYNU*, *SRD5A2*, *PPP2R2B*, *NPC1*, and *HTT*. We designate this set as "GWAS neural genes" rather than "dopaminergic network," as only *DRD2* is strictly dopaminergic.

**Mast Cell / Basophil Panel (negative control).** Four genes (*CPA3*, *MS4A2*, *FCER1A*, *HDC*) previously identified as differentially expressed in FM whole blood (Kurian et al., 2017). These are primarily expressed by basophils and mast cells, which are depleted during PBMC isolation.

*NPY* was included in the pre-specified gene set but was absent from the GSE221921 expression matrix. FDR correction was therefore applied to 16 measured genes (12 GWAS neural + 4 mast cell).

### 2.2 Transcriptomic Datasets

**GSE221921 (PBMCs, RNA-seq).** FPKM-normalized expression values from peripheral blood mononuclear cells of 96 FM patients and 93 healthy controls (Mohapatra et al., 2024; PMID 38366049). Sample metadata and expression matrices were obtained from the GEO supplementary file `GSE221921_FM_ProcessedData.xlsx`.

**Critical note on sex distribution:** The GSE221921 cohort has a severe sex imbalance — FM group: 91 female / 5 male; HC group: 41 female / 52 male. This confounds any unadjusted FM vs. HC comparison, as a portion of the observed signal may reflect sex differences rather than disease effects. We address this through multiple sensitivity analyses (§2.4).

**GSE67311 (Whole blood, microarray).** Affymetrix Human Gene 1.1 ST array expression data from whole blood (PAXgene tubes) of 70 FM patients and 70 age- and sex-matched healthy controls (Kurian et al., 2017; PMID 27157394). Pre-computed differential expression results (log₂FC, p-value, FDR-adjusted p-value) were used.

### 2.3 Statistical Analysis

All p-values from the 16 measured genes were jointly corrected using the Benjamini-Hochberg (BH) procedure (Benjamini & Hochberg, 1995) at α = 0.05. Genes were considered significant at q < 0.05.

### 2.4 Sensitivity Analyses for GSE221921

Given the sex imbalance, we applied five analytical models to each gene:

1. **Welch t-test on raw FPKM** (original analysis)
2. **Welch t-test on log₂(FPKM+1)** (variance-stabilizing transform)
3. **Mann-Whitney U test** (non-parametric, distribution-free)
4. **OLS regression: log₂(FPKM+1) ~ case + sex** (sex as covariate, full cohort)
5. **Female-only subgroup: Welch t-test on log₂(FPKM+1)** (91 FM vs. 41 HC, eliminates sex confound entirely)

Each model produced p-values that were independently FDR-corrected across all 16 genes. Genes were classified by robustness: "Robust" (q < 0.05 in all 5 models), "Supported" (q < 0.05 in 3–4 models), "Model-sensitive" (q < 0.05 in 1–2 models), or "Not significant."

### 2.5 Targeted Literature Review

We searched PubMed (terms: "pramipexole fibromyalgia," "ropinirole fibromyalgia," "dopamine agonist fibromyalgia"), ClinicalTrials.gov, and the GSK Study Register for clinical trials of dopamine D2/D3 agonists in FM. Search date: May 2026. This is a targeted narrative review, not a formal systematic review; no PRISMA protocol was registered.

### 2.6 Limitations of the Analytical Approach

We acknowledge that the use of FPKM values with parametric tests is a simplified approach. The gold standard for RNA-seq differential expression is count-based modeling (DESeq2/edgeR/limma-voom; Love et al., 2014). Only FPKM values were available in the GEO supplementary materials; raw counts were not accessible. All analyses were performed in Python 3.10 using pandas 1.5, scipy 1.10, and statsmodels 0.13.

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
- *CAMKV* and *CELF4* survive four models (including female-only) but not the sex-adjusted OLS on the full cohort (q = 0.112 and 0.167, respectively). Their signals are supportive but model-sensitive.
- *HTT* — the gene with the strongest GWAS coding variant — shows a supported signal (3/5 models), which was not apparent in the original FPKM-only analysis.
- No mast cell marker shows a robust PBMC signal; *MS4A2* reaches significance only in the Mann-Whitney model and is therefore classified as model-sensitive rather than replicated across analytical frameworks.

### 3.2 Cross-Context Comparison: GSE67311 (Whole Blood)

To assess whether these signals are detectable in a different cell fraction, we examined the same gene sets in GSE67311 (whole blood, Affymetrix microarray; Table 2).

**Table 2. Cross-context comparison: robustness pattern in GSE221921 (PBMCs) vs. q-values in GSE67311 (whole blood).**

| Gene | Category | GSE221921 (PBMCs) robustness | GSE67311 (whole blood) q | Fraction-specific? |
|------|----------|:----------------------------:|:------------------------:|:------------------:|
| *CPA3* | Mast Cell | NS (0/5) | **1.8×10⁻⁶** | Whole blood only |
| *MS4A2* | Mast Cell | Model-sensitive (1/5) | **1.5×10⁻⁵** | Whole blood only |
| *FCER1A* | Mast Cell | NS (0/5) | **1.7×10⁻⁵** | Whole blood only |
| *HDC* | Mast Cell | NS (0/5) | **4.4×10⁻⁵** | Whole blood only |
| *MDGA2* | GWAS Neural | Robust (5/5) | 0.99 | PBMCs only |
| *DRD2* | GWAS Neural | Robust (5/5) | 0.42 | PBMCs only |
| *CAMKV* | GWAS Neural | Supported (4/5) | 0.13 | PBMCs only |
| *CELF4* | GWAS Neural | Supported (4/5) | 0.72 | PBMCs only |

No gene was significant in both datasets. This pattern is consistent with a **cell-fraction-dependent contrast**: the mast cell/basophil signal is detectable in whole blood (which contains granulocytes) but absent from PBMCs; conversely, the GWAS neural gene signal appears in PBMCs (lymphocytes/monocytes) but not in granulocyte-containing whole blood.

**Important caveats:** This contrast does not constitute replication or validation, as the two datasets differ in tissue fraction, platform (RNA-seq vs. microarray), normalization, and cohort composition. Furthermore, we cannot distinguish true per-cell expression changes from differences in cell-type composition between FM and HC groups without deconvolution analysis (see §5).

### 3.3 Targeted Literature Review: Dopamine Agonists in FM

Our literature search identified three clinical studies and one preclinical study (Table 3):

**Table 3. Dopamine agonist studies in fibromyalgia.**

| Study | Drug | Type | N | Result | Key Finding | Risk of Bias |
|-------|------|------|---|--------|-------------|--------------|
| Holman & Myers, 2005 (PMID 16052595) | Pramipexole | RCT (DB-PC) | 60 | **Positive** | 36% pain ↓ vs 9% placebo; 42% achieved ≥50% pain decrease | High: single-center, author held patents on D2/D3 use in FM |
| Holman, 2003 (ACR conference) | Ropinirole | Pilot | 30 | NS (p=0.31) | Underpowered. Not published in peer-reviewed journal. | Very high: unpublished, tiny N |
| GSK NCT00256893 | Ropinirole CR | Phase II RCT | 160 | **Negative** | Failed primary endpoints | Moderate: sponsor-reported, results not published in peer-reviewed journal |
| Peng et al., 2022 (PMID 35799530) | Pramipexole | Preclinical | Mice | **Positive** | Reversed allodynia and DA depletion in reserpine FM model | N/A (animal study) |

The Holman & Myers (2005) study remains the only positive RCT of a dopamine agonist in FM. Despite 21 years having elapsed, it has not been replicated in a multi-center trial. The negative GSK ropinirole trial is not directly comparable pharmacologically: ropinirole has substantially lower D3 receptor affinity than pramipexole.

---

## 4. Discussion

### 4.1 GWAS-Transcriptomic Convergence on Neural Genes

The central finding of this study is that two GWAS-prioritized neural genes — *MDGA2* and *DRD2* — show robust upregulation across multiple analytical models in FM PBMCs, including sex-adjusted and female-only sensitivity analyses. Two additional genes (*CAMKV*, *CELF4*) show supportive but sex-covariate-sensitive signals. This convergence of genetic risk (GWAS) and transcriptomic alteration (independent cohort) across independent methodologies is suggestive of biological relevance, though it remains an exploratory observation.

We emphasize that the GWAS network is not exclusively "dopaminergic." *MDGA2* encodes a GPI-anchored immunoglobulin superfamily member involved in synaptogenesis and neural circuit formation. *CAMKV* is a CaM kinase-like protein involved in dendritic spine dynamics. *CELF4* regulates neuronal mRNA metabolism. Only *DRD2* is strictly dopaminergic. The finding is therefore better characterized as convergence on a **neural/synaptic GWAS network** that includes, but is not limited to, dopaminergic signaling.

### 4.2 The DRD2 Signal: Interpretation and Caveats

The upregulation of *DRD2* (Log₂FC = +1.41, q = 2.9×10⁻⁵; robust across all 5 models) in PBMCs warrants careful interpretation:

1. **Absolute expression is low** (FM mean = 0.72 FPKM, HC mean = 0.27 FPKM). While the fold change and statistical significance are robust, the biological impact of sub-FPKM expression differences requires validation by qRT-PCR or targeted methods.

2. **Cell composition confounding.** DRD2 is expressed in T cell subsets, where it modulates cytokine production and chemotaxis (Pacheco et al., 2014). If FM patients have altered PBMC composition (e.g., different T cell subsets or monocyte proportions), the observed DRD2 increase could reflect more cells expressing DRD2 rather than per-cell upregulation. Without deconvolution analysis (CIBERSORTx, xCell, or similar), this cannot be distinguished.

3. **Peripheral vs. central.** PBMCs are not the primary site of FM pathology. The GWAS heritability is enriched in brain tissues. Whether peripheral DRD2 expression mirrors central dopaminergic dysfunction is unknown.

### 4.3 Cell-Fraction-Dependent Contrast

The observation that mast cell markers are significant in whole blood but not PBMCs, while GWAS neural genes show the opposite pattern, is consistent with cell-fraction-dependent peripheral signatures. However, this observation cannot distinguish true cell-state changes from cell-composition differences, nor can it determine whether either signature is a disease driver versus a secondary biomarker. The isolated Mann-Whitney signal for *MS4A2* in PBMCs underscores this point: weak, model-specific peripheral signals should not be overinterpreted as robust transcriptional convergence.

### 4.4 Pharmacological Context: The 21-Year Gap

The pharmacological evidence for dopamine agonists in FM is limited. The sole positive RCT (Holman & Myers, 2005) carries substantial risk of bias (single-center, n=60, author held patents). The negative ropinirole trial (GSK NCT00256893) has never been published in a peer-reviewed journal, limiting independent evaluation. The current evidence is insufficient to recommend dopamine agonists for FM but does provide a rationale for re-examining this pharmacological axis in molecularly stratified cohorts.

### 4.5 Practical Next Steps for Validation

The present analysis supports a staged validation strategy rather than immediate therapeutic inference. First, the *MDGA2* and *DRD2* PBMC signals should be retested in sex-balanced bulk cohorts, ideally with raw counts enabling limma-voom or DESeq2-based modeling. Second, orthogonal validation by qRT-PCR or targeted transcript quantification is needed because *DRD2* absolute expression is low. Third, cell-composition-aware analyses (e.g., CIBERSORTx, xCell, MCP-counter, or single-cell RNA-seq) are required to determine whether the observed differences reflect altered cell proportions or per-cell transcriptional regulation. Finally, any future pharmacological work should be framed as a stratified follow-up to this neural/GWAS signal rather than as proof that dopamine agonism is an established FM treatment strategy.

---

## 5. Limitations

1. **Sex confounding.** GSE221921 has a severe sex imbalance (FM: 91F/5M; HC: 41F/52M). Our sensitivity analyses suggest that *MDGA2* and *DRD2* are not solely explained by sex imbalance, while *CAMKV* and *CELF4* are sensitive to sex adjustment. Residual confounding remains possible, and future studies should use sex-balanced cohorts or sex-stratified designs.

2. **Statistical methodology.** FPKM with parametric tests is not gold standard for RNA-seq. Count-based modeling (DESeq2/edgeR) would be preferable, but raw counts were not available. We mitigate this with log₂-transformation, non-parametric tests, and covariate-adjusted models.

3. **Cell composition.** PBMC subpopulation proportions were not available. The observed gene expression differences may reflect altered cell-type composition rather than per-cell transcriptional changes. Computational deconvolution (CIBERSORTx, MCP-counter) or single-cell RNA-seq would be needed to resolve this.

4. **Low absolute expression.** DRD2 expression in PBMCs is < 1 FPKM. qRT-PCR validation is needed.

5. **Missing gene.** NPY was pre-specified but absent from the GSE221921 matrix. FDR correction was applied to 16, not 17, genes.

6. **Cross-context comparison, not validation.** GSE67311 and GSE221921 differ in tissue fraction, platform, normalization, and cohort demographics. The contrast is informative but does not constitute independent replication.

7. **GWAS preprint status.** Kerrebijn et al. (2025) is published on medRxiv (doi: 10.1101/2025.09.18.25335914v1, PMID 41001472) and has not yet completed full peer review.

8. **No experimental validation.** All analyses are computational. No wet-lab or clinical experiments were performed.

9. **Literature review is targeted, not systematic.** No PRISMA protocol was registered. Formal systematic review with risk-of-bias assessment (RoB 2) would strengthen the pharmacological evidence section.

---

## 6. Conclusion

A targeted reanalysis of two public transcriptomic cohorts suggests that selected GWAS-prioritized neural genes — most robustly *MDGA2* and *DRD2* — show increased expression in FM PBMCs across multiple analytical models. *CAMKV* and *CELF4* show supportive but model-sensitive signals, whereas the mast cell panel remains largely restricted to whole blood. These findings, combined with the observation that the sole positive dopamine agonist RCT in FM remains unreplicated after 21 years, support prioritizing the DRD2/neural GWAS axis for validation in sex-balanced cohorts with cell-type-resolved transcriptomic data and orthogonal experimental confirmation.

---

## References

Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. *J R Stat Soc B*, 57(1), 289–300.

Bi, W., Yang, M., & Mao, R. (2024). Unraveling Shared Diagnostic Biomarkers of Fibromyalgia in Ankylosing Spondylitis. *J Inflamm Res*, 17, 6395–6413. PMID: 39310900.

Chinn, S., Caldwell, W., & Gritsenko, K. (2016). Fibromyalgia Pathogenesis and Treatment Options Update. *Curr Pain Headache Rep*, 20(4), 25. PMID: 26922414.

Gowri Gopal, K., Robi, L.S., & Sherin, D.R. (2026). Molecular insights into fibromyalgia: association of hub genes with pain targets, neuropathic pathways, and stress-related hormones. *In Silico Pharmacol*, 14(2), 135. PMID: 42109571.

Holman, A.J., & Myers, R.R. (2005). A Randomized, Double-Blind, Placebo-Controlled Trial of Pramipexole, a Dopamine Agonist, in Patients With Fibromyalgia Receiving Concomitant Medications. *Arthritis Rheum*, 52(8), 2495–2505. PMID: 16052595. doi: 10.1002/art.21191.

Kerrebijn, I., et al. (2025). The genetic architecture of fibromyalgia across 2.5 million individuals. *medRxiv*. PMID: 41001472. doi: 10.1101/2025.09.18.25335914v1.

Kurian, S.M., et al. (2017). Peripheral Blood Gene Expression in Fibromyalgia. PMID: 27157394. (GSE67311).

Love, M.I., Huber, W., & Anders, S. (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biol*, 15, 550. PMID: 25516281.

Mohapatra, G., et al. (2024). Identification of unique genomic signatures in patients with fibromyalgia and chronic pain. *Sci Rep*, 14, 3949. PMID: 38366049.

Pacheco, R., Contreras, F., & Zouali, M. (2014). The dopaminergic system in autoimmune diseases. *Front Immunol*, 5, 117.

Peng, X., et al. (2022). Pramipexole inhibits fibromyalgia-like symptoms in a reserpine-induced mouse model. *Neural Regen Res*, 17(3), 667–674. PMID: 35799530. doi: 10.4103/1673-5374.355761.

Sarzi-Puttini, P., et al. (2020). Fibromyalgia: An update. *Nat Rev Rheumatol*, 16(11), 645–660. PMID: 33024295.

Zhao, F., et al. (2025). Identification of diagnostic biomarkers for fibromyalgia using gene expression analysis and machine learning. *Front Genet*, 16, 1535541. PMID: 40313599.

---

## Data & Code Availability

All transcriptomic data are publicly available from GEO (GSE221921, GSE67311). Analysis scripts are available in the project repository:
- `scripts/sensitivity_analysis_gse221921.py` — five-model sensitivity analysis
- `scripts/cross_context_gwas_neural_genes.py` — cross-context comparison of GWAS-prioritized neural genes vs. mast cell markers across PBMC and whole-blood datasets
- `scripts/phase2_rct_review.py` — literature review evidence table

Representative derived tables include:
- `analisis/sensitivity_analysis_GSE221921.csv` — five-model robustness table for PBMC reanalysis
- `analisis/cross_context_gwas_neural_genes.csv` — cross-context comparison table used for the PBMC vs. whole-blood contrast
- `analisis/RCT_dopamine_agonists_FM.csv` — targeted literature review evidence table

Software: Python 3.10, pandas 1.5.3, scipy 1.10.1, statsmodels 0.13.5.

## Conflict of Interest

The authors declare no conflicts of interest.
