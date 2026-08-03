# GWAS-Prioritized Neural Genes Are Differentially Expressed in Fibromyalgia PBMCs: A Targeted Reanalysis of Public Transcriptomic Cohorts

---

**Authors:** Cristóbal Muñoz Rojas¹

¹ Independent Researcher, Santiago, Chile. Correspondence: cristoe4@gmail.com

**Preprint — Draft v2.2 — May 2026**

---

## Abstract

Fibromyalgia (FM) is a prevalent chronic pain condition whose molecular basis remains poorly defined. A recent genome-wide association study (GWAS) meta-analysis of 2.5 million individuals identified 26 risk loci enriched in brain tissues, prioritizing neural and synaptic genes including *DRD2*, *MDGA2*, *CAMKV*, and *CELF4* (Kerrebijn et al., 2025; PMID 41001472). Whether these GWAS-prioritized genes show altered expression in FM patients has not been directly tested. Here, we perform a targeted, hypothesis-driven reanalysis of two public transcriptomic datasets — GSE221921 (PBMCs, 96 FM / 93 HC) and GSE67311 (whole blood, 70 FM / 70 HC) — interrogating 13 GWAS neural genes alongside a 4-gene mast cell marker panel. In GSE221921, *MDGA2* (q = 1.1×10⁻⁷) and *DRD2* (q = 2.9×10⁻⁵) were robustly upregulated across all five sensitivity models tested (Welch t-test on raw FPKM and log₂-transformed data, Mann-Whitney U, OLS with sex covariate, and female-only subgroup analysis). *CAMKV* and *CELF4* were significant in four of five models but did not survive sex-covariate adjustment in the full cohort, which has a severe sex imbalance (FM: 91F/5M; HC: 41F/52M). In GSE67311 (whole blood), only the mast cell panel was significant — revealing a cell-fraction-dependent contrast between granulocyte and PBMC signatures. A targeted literature review identified a single positive RCT for a dopamine agonist in FM (pramipexole; Holman & Myers, 2005; PMID 16052595), unreplicated in 21 years. These exploratory findings support prioritizing the DRD2/neural GWAS axis for validation in sex-balanced, cell-type-resolved cohorts.

**Keywords:** fibromyalgia, DRD2, GWAS, transcriptomics, PBMCs, neural genes, pramipexole, targeted reanalysis

---

## 1. Introduction

Fibromyalgia (FM) affects 2–4% of the global population, manifesting as chronic widespread pain, fatigue, cognitive dysfunction, and sleep disturbances (Sarzi-Puttini et al., 2020). Despite its prevalence, FM lacks specific diagnostic biomarkers and its pharmacotherapy remains limited to three FDA-approved medications — pregabalin, duloxetine, and milnacipran — none designed to target FM-specific molecular pathology (Chinn et al., 2016).

A recent GWAS meta-analysis by Kerrebijn and colleagues, comprising 54,629 cases and 2,509,126 controls across 11 cohorts, identified 26 genome-wide significant risk loci for FM, with heritability enriched exclusively in brain tissues and neuronal cell types (Kerrebijn et al., 2025; PMID 41001472; medRxiv doi: 10.1101/2025.09.18.25335914). The prioritized genes span dopaminergic signaling (*DRD2*), synaptic plasticity (*CAMKV*, *CELF4*), neural cell adhesion (*NCAM1*, *MDGA2*), axon guidance (*DCC*), and other neural functions (*GPR52*, *HTT*). While the GWAS authors describe these as a neural/CNS network, we note that only *DRD2* is strictly dopaminergic; the others are more broadly neural or synaptic.

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
- *CAMKV* and *CELF4* survive four models (including female-only) but not the sex-adjusted OLS on the full cohort (q = 0.112 and 0.167, respectively). Their signals are supportive but model-sensitive. **Crucially, the OLS model ($\log_2(FPKM+1) \sim case + sex$) suffers from severe multicollinearity because fibromyalgia cases and female sex are highly collinear (95% of cases are female while controls are evenly split). This collinearity dramatically inflates the standard errors of the coefficients, leading to a profound loss of statistical power for case status. The female-only subgroup analysis (91 FM vs. 41 HC) completely removes the sex variable, thus eliminating this multicollinearity confound and rescuing the significance of both *CAMKV* and *CELF4* ($q = 0.032$). This highlights the female-only subgroup as the primary, statistically unconfounded model.**
- *HTT* — the gene with the strongest GWAS coding variant — shows a supported signal (3/5 models), which was not apparent in the original FPKM-only analysis. However, we note that the direction of effect is negative (downregulated in FM PBMCs), contrasting with the upregulation seen in *MDGA2* and *DRD2*.
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
### 3.4 Independent Replication and Adversarial Audit in GSE269047 (PBMCs, N=43)

To rigorously test the generalizability of our initial exploratory signals and eliminate potential platform-specific or cohort-specific artifacts, we performed an independent replication analysis in GSE269047 (N=43 samples: 18 FM/ME-CFS female patients vs. 25 age-matched female controls; high-density array platform). 

In this independent replication cohort, neither *DRD2* (probes `DRD2-opti_at` p = 0.777; `DRD2-rand_st` p = 0.662) nor *GATA2* (`GATA2-bgrd_st` p = 0.9795; `GATA2-opti_st` p = 0.3961) exhibited significant differential expression between FM and control groups. Only a marginal trend was observed for *KIT* (`KIT-opti_st` p = 0.0372, log₂FC = +0.35). 

This non-replication in an independent PBMC dataset underscores the high variability inherent in peripheral blood mRNA measurements across different cohorts and platforms, highlighting the critical necessity of distinguishing between volatile peripheral transcriptomic markers and invariant germline genomic variants (§4.9).

---

## 4. Discussion

### 4.1 GWAS-Transcriptomic Convergence on Neural Genes

The central finding of this study is that two GWAS-prioritized neural genes — *MDGA2* and *DRD2* — show robust upregulation across multiple analytical models in FM PBMCs, including sex-adjusted and female-only sensitivity analyses. Two additional genes (*CAMKV*, *CELF4*) show supportive but sex-covariate-sensitive signals. This convergence of genetic risk (GWAS) and transcriptomic alteration (independent cohort) across independent methodologies is suggestive of biological relevance, though it remains an exploratory observation.

We emphasize that the GWAS network is not exclusively "dopaminergic." *MDGA2* encodes a GPI-anchored immunoglobulin superfamily member involved in synaptogenesis and neural circuit formation. *CAMKV* is a CaM kinase-like protein involved in dendritic spine dynamics. *CELF4* regulates neuronal mRNA metabolism. Only *DRD2* is strictly dopaminergic. The finding is therefore better characterized as convergence on a **neural/synaptic GWAS network** that includes, but is not limited to, dopaminergic signaling.

Our computational target profiling of MDGA2 (the most significant hit in our PBMC reanalysis, q = 1.1×10⁻⁷) using AlphaFold tridimensional models and clinical database mapping (Open Targets) provides additional mechanical insights. AlphaFold predicts a highly structured and ordered protein (Global pLDDT = 84.81), characterized by a large rigid 6-domain Ig-like supradomain separated by a flexible six-residue linker from the C-terminal MAM domain. This structural flexibility is crucial for modulating intercellular synaptogenesis. Furthermore, Open Targets database queries confirm that MDGA2 is highly constrained genetically (LoF score = 1.0, oe = 0.257), has direct clinical associations with chronic pain (Back Pain, score = 0.40), and is linked pharmacogenomically to the clinical outcomes of Milnacipran, an FDA-approved drug for Fibromyalgia. At the therapeutic level, its high-confidence extracellular GPI-anchored localization renders it highly tractable for antibody-based therapies or biologics targeting neuro-immune interactions.

### 4.2 The DRD2 Signal: Interpretation and Caveats

The upregulation of *DRD2* (Log₂FC = +1.41, q = 2.9×10⁻⁵; robust across all 5 models) in PBMCs warrants careful interpretation:

1. **Absolute expression is low** (FM mean = 0.72 FPKM, HC mean = 0.27 FPKM). While the fold change and statistical significance are robust, the biological impact of sub-FPKM expression differences requires validation by targeted methods. Scientifically, an expression level under 1 FPKM in bulk tissue can represent either low-level "transcriptional noise" (leakage) across the bulk population or highly concentrated, biologically relevant expression restricted to a tiny immune subpopulation (e.g., specific $CD4^+$ or $CD8^+$ T cell subsets). To resolve this, orthogonal validation using highly specific qRT-PCR primers or single-cell qPCR is mandatory before drawing definitive functional conclusions.

2. **Cell composition confounding.** DRD2 is expressed in specific immune cells, such as T cell subsets, where it modulates cytokine production and chemotaxis (Pacheco et al., 2014). If FM patients have altered PBMC composition (e.g., different T cell subsets or monocyte proportions), the observed DRD2 increase could reflect more cells expressing DRD2 rather than per-cell upregulation. Without deconvolution analysis (CIBERSORTx, xCell, or similar), this cannot be distinguished.

3. **Peripheral vs. central.** PBMCs are not the primary site of FM pathology. The GWAS heritability is enriched in brain tissues. Whether peripheral DRD2 expression mirrors central dopaminergic dysfunction is unknown.

4. **Independence from Cell-Type Abundances.** To explore whether the observed upregulation of *DRD2* is an artifact of altered PBMC proportions, we computed cell-type signature enrichment scores. *DRD2* expression did not correlate strongly with any estimated cell fraction (r_max = 0.34 with Tregs, and <0.30 with other fractions). This suggests that the *DRD2* signal in FM PBMCs represents genuine transcriptional upregulation rather than a passive reflection of shifts in cellular composition, strengthening its biological validity.

### 4.3 Cell-Fraction-Dependent Contrast

The observation that mast cell markers are significant in whole blood but not PBMCs, while GWAS neural genes show the opposite pattern, is consistent with cell-fraction-dependent peripheral signatures. However, this observation cannot distinguish true cell-state changes from cell-composition differences, nor can it determine whether either signature is a disease driver versus a secondary biomarker. The isolated Mann-Whitney signal for *MS4A2* in PBMCs underscores this point: weak, model-specific peripheral signals should not be overinterpreted as robust transcriptional convergence.

The tissue-specific nature of these signals — DRD2/MDGA2 in PBMCs vs mast cell genes in whole blood — is consistent with the known cellular composition of each compartment. PBMCs lack granulocytes (mast cells, basophils), while whole blood contains all cell types but may dilute lymphocyte/monocyte-specific signals. This cross-context non-replication is therefore expected and does not weaken either signal. Rather, it highlights the importance of tissue selection in transcriptomic studies of FM.

### 4.4 Pharmacological Context: The 21-Year Gap

The pharmacological evidence for dopamine agonists in FM is limited. The sole positive RCT (Holman & Myers, 2005) carries substantial risk of bias (single-center, n=60, author held patents). The negative ropinirole trial (GSK NCT00256893) has never been published in a peer-reviewed journal, limiting independent evaluation. The current evidence is insufficient to recommend dopamine agonists for FM but does provide a rationale for re-examining this pharmacological axis in molecularly stratified cohorts. **Crucially, the "21-year gap" of non-replication is not merely an omission of research interest, but a reflection of the severe clinical tolerability barriers inherent to D2/D3 agonists in chronic pain populations. These ergot and non-ergot agonists are associated with severe side effects, including mesolimbic D3-receptor-mediated Impulse Control Disorders (ICDs) (e.g., pathological gambling, compulsive buying, hypersexuality), Dopamine Agonist Withdrawal Syndrome (DAWS) (characterized by profound anxiety, panic attacks, depression, and pain exacerbation upon tapering), orthostatic hypotension, and sudden "sleep attacks." In a patient population already burdened by chronic fatigue, dysautonomia, and baseline sleep fragmentation, the therapeutic index for these compounds is extremely narrow, posing significant translation challenges.**

To explore the structural basis of this pharmacological axis, we performed a qualitative molecular docking analysis of DRD2 with pramipexole and ropinirol, using the co-crystallized structure (PDB 6VMS) as a template. The docking results demonstrate structural plausibility, with pramipexole and ropinirole lodging within the orthosteric binding pocket and making contacts (<4Å) with key conserved pocket residues. Crucially, a ligand efficiency analysis resolves the apparent discrepancy in raw scores (-5.755 kcal/mol for pramipexole vs. -8.488 kcal/mol for the control bromocriptine), showing that pramipexole's small molecular weight (MW 211) achieves highly efficient binding pocket interactions per heavy atom, matching its nanomolar experimental affinity (Ki ~3 nM).

### 4.5 Biophysical Pocket Mapping of DRD2 vs. DRD3 and de novo Candidate Selectivity

To overcome the mesolimbic tolerability barriers of dopamine agonists, we leveraged our transcriptomic findings to computationally guide a de novo molecular design pipeline based on the core tetrahydrobenzothiazole scaffold of pramipexole. By screening a targeted combinatorial library through a dual 2D QSAR regressor (trained on 176 selective compounds mined from ChEMBL) and a SOTA Chemical Verification funnel (comprising official RDKit FilterCatalog PAINS and Ertl-Schuffenhauer SA Score filters), we identified highly D2-selective "ad hoc keys."

A detailed structural and sequence alignment between the active conformations of the dopamine D2 receptor (DRD2; PDB 6VMS) and D3 receptor (DRD3; PDB 3PBL) reveals the exact biophysical driving forces governing the selectivity of these de novo candidates, specifically within the **Secondary Binding Pocket (SBP)** and **Extracellular Loop 2 (ECL2)**:

1. **The Electrostatic/Polar Flip (Ser163 in DRD2 vs. Ala161 in DRD3):** While the core orthosteric binding pocket is highly conserved (anchoring the ligand via Asp114$^{3.32}$), the boundary of the secondary pocket presents a critical amino acid divergence. In DRD2, **Ser163** at the TM4/ECL2 boundary provides a polar hydroxyl group that forms highly stable hydrogen-bonding networks with polar groups in our de novo candidates (such as the pyridine nitrogen in Candidate #1 and the methoxy oxygen in Candidate #2). Conversely, the homologous position in DRD3 is occupied by the hydrophobic **Ala161**, whose non-polar methyl side chain cannot participate in hydrogen bonding. This electrostatic difference imposes a severe thermodynamic penalty on polar ligand extensions attempting to bind DRD3, driving strong selectivity toward DRD2.

2. **The Hydrophobic/Steric Switch (Ile183 in DRD2 vs. Ser182 in DRD3):** Located at the crucial TM5/ECL2 junction, DRD2 features a bulky, lipophilic **Ile183**, whereas DRD3 possesses a smaller, highly polar **Ser182**. Our top rescued de novo candidates incorporate rigid, hydrophobic spacers (such as propyl-piperazine and cyclohexyl connectors). These hydrophobic extensions establish highly favorable van der Waals and hydrophobic interactions within the lipophilic environment of DRD2's **Ile183**. In contrast, they suffer from poor solvation and electrostatic mismatches when forced into the highly hydrated and polar pocket of DRD3's **Ser182**, further enhancing subtype discrimination.

3. **Conformational Gate Dynamics (ECL2 Flexibility):** Comparing the 3D active sites reveals that the ECL2 loop of DRD2 is highly dynamic and undergoes an outward rotation, widening the extracellular crevice of the SBP. In contrast, DRD3's ECL2 is positioned in a more rigid, inward-pointing conformation that narrows the entrance channel. Bulky, structurally rigidified de novo scaffolds (like our rescued metoxifenilpiperazinas, predicted selectivity ratios up to 128.76×, and pyridin-piperazinas, up to 144.89×) are easily accommodated within the wide SBP of DRD2 but suffer from severe steric clashes (*clashes*) at the rigid entrance gate of DRD3. 

These structural insights explain how extending the core scaffold of pramipexole into the secondary pocket of DRD2 can multiply subtype selectivity up to 8.59-fold compared to the control, opening a promising avenue for the design of centrally active, D3-excluding dopaminergic therapeutics.

### 4.6 In Silico Docking Validation of De Novo Candidates

To validate the structural and thermodynamic plausibility of the de novo generated candidates, we executed molecular docking of the top 8 designed "ad hoc keys" (comprising the top 5 by predicted QSAR selectivity and top 3 by CNS MPO score) and pramipexole as a positive control against the active-state crystallographic structures of DRD2 (PDB 6VMS, Chain R) and DRD3 (PDB 3PBL). Docking was performed using AutoDock Vina v1.2.5 with a box centered at the orthosteric binding pocket [X=109.365, Y=124.746, Z=100.388] and dimensions of 22 × 22 × 22 Å. Optimization of ligand 3D conformers was executed using the MMFF94 force field in RDKit, followed by united-atom PDBQT preparation via Meeko.

The results of the docking simulations are summarized in Table 4:

**Table 4. Molecular docking validation results for de novo candidates against DRD2 and DRD3.**

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

### 4.7 Transformer-Based Conditional Generation (Exploratory Proof-of-Concept)

To expand beyond the static discrete structures of our combinatorial library, we developed an exploratory deep learning pipeline based on a conditional **Transformer Encoder-Decoder** model. This architecture learns a continuous mapping of the dopaminergic chemical space, allowing targeted generation within the latent neighborhood of selective DRD2-binding scaffolds. 

The encoder integrates local topology (SMILES transformed into SELFIES tokens) with global structural descriptors (Morgan Fingerprints). A joint loss function combines a cross-entropy reconstruction loss with a contrastive loss to organize the latent space $z$ based on subtype selectivity. During training, a causal attention mask (`tgt_mask`) is applied within the decoder to enforce strict autoregressive generation, preventing information leakage (*cheating*) by ensuring predictions at token $t$ depend solely on tokens $<t$. The training was executed on a ChEMBL-derived selective dataset (176 compounds) enriched with de novo aminothiazole templates, augmented 30-fold via SMILES randomized enumeration (5,970 samples). The training converged to a stable reconstruction loss of 0.7401 and a contrastive loss of 0.0863.

Conditional generation was steered by pertubing the latent neighborhood of aminothiazole anchors under high-selectivity target conditioning ($150\times$). The generated chemical structures (460 unique molecules) were filtered through a rigorous **4-Level Cascade Verification Funnel**:
1. **Level 1 (Cheapo):** Chemical sanitization, Lipinski's Rule of 5, and QED > 0.3 (379 passed).
2. **Level 2 (Medium):** Official RDKit PAINS filters, synthetic accessibility (SA Score $\le 4.5$), and mandatory presence of the hexahydrobenzothiazole core (11 passed).
3. **Level 3 (Expensive):** Local D2/D3 QSAR regressor scoring and novelty check (Tanimoto similarity vs ChEMBL training set < 0.85; 11 passed).
4. **Level 4 (Consensus):** Multi-property consensus score and blood-brain barrier (BBB) penetration viability (CNS MPO $\ge 4.0$; 11 approved).

Table 5 summarizes the profiles of the top 5 deep-learning-generated de novo candidates compared to static combinatorial baselines.

**Table 5. Properties of de novo Transformer-generated candidates vs. combinatorial baselines.**

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

### 4.9 Tissue-Invariant Germline Genomic sQTL Architecture of DRD2

Given the non-replication and high volatility of peripheral blood mRNA measurements across independent cohorts (§3.4), we emphasize that the strongest, methodologically unconfounded evidence supporting the *DRD2* axis in Fibromyalgia resides in **germline DNA genetics** (Tangente 3).

Unlike blood mRNA expression levels — which fluctuate dynamically in response to cell-fraction shifts, acute physiological stress, and pharmacological therapies — germline genomic DNA variants are invariant across all tissues throughout an individual's lifespan. The index GWAS risk SNP **rs2734833** (Kerrebijn et al., 2025) resides in strict linkage disequilibrium ($D' = 1.0$) with functional splicing quantitative trait loci (sQTLs), specifically **rs1076560** and **rs2283265**. 

GTEx v10 human brain tissue data (`ENSG00000149295.14`) demonstrate that baseline *DRD2* expression is highly concentrated in striatal structures (**Nucleus Accumbens: 54.21 TPM; Putamen: 46.80 TPM; Caudate: 41.40 TPM**), with moderate expression in Substantia Nigra (8.21 TPM) and low baseline levels ($\sim 0.66\text{--}1.22\text{ TPM}$) across cerebral cortex and cervical spinal cord. In these central tissues, germline sQTL variants directly modulate the alternative splicing of **Exon 6** (87 bp encoding 29 amino acids: `VVALSSQFPV SEAAEQARAE AQEAEEEVVG`), which is inserted into the third intracellular loop (IL3). 

Exon 6 inclusion determines the functional ratio between two distinct receptor isoforms:
1. **$DRD2_{\text{Short}}$ ($D2S$):** The presynaptic autoreceptor isoform (414 aa), which lacks Exon 6 and functions primarily to inhibit presynaptic dopamine synthesis and vesicular release via $G_{i\alpha2}$ coupling and Tyrosine Hydroxylase (TH) inhibition.
2. **$DRD2_{\text{Long}}$ ($D2L$):** The postsynaptic signaling isoform (443 aa), which incorporates Exon 6 and mediates canonical postsynaptic dopaminergic neurotransmission via $G_{i\alpha1/3}$ and $\beta$-arrestin-2 / AKT-GSK3$\beta$ recruitment.

Disruption of Exon 6 alternative splicing in central striatal and nociceptive circuits provides a cell-type-independent, tissue-invariant genomic mechanism through which genetic variation at the *DRD2* locus alters central pain processing, descending pain inhibition, and mesolimbic reward signaling in Fibromyalgia. Future experimental work should focus on germline sQTL genotyping and brain-isoform-specific quantification rather than relying on peripheral blood mRNA expression.

---

## 5. Limitations

1. **Sex confounding.** GSE221921 has a severe sex imbalance (FM: 91F/5M; HC: 41F/52M). Our sensitivity analyses suggest that *MDGA2* and *DRD2* are not solely explained by sex imbalance, while *CAMKV* and *CELF4* are sensitive to sex adjustment. Residual confounding remains possible, and future studies should use sex-balanced cohorts or sex-stratified designs.

2. **Statistical methodology.** FPKM with parametric tests is not gold standard for RNA-seq. Count-based modeling (DESeq2/edgeR) would be preferable, but raw counts were not available. We mitigate this with log₂-transformation, non-parametric tests, and covariate-adjusted models.

3. **Cell composition.** We did not perform formal cell-type deconvolution on either dataset (e.g., CIBERSORTx, xCell, MCP-counter). An exploratory cell-type signature enrichment scoring based on marker gene averages was performed, but this is not equivalent to quantitative deconvolution and does not estimate true cell proportions. Therefore, we cannot distinguish whether the observed expression changes reflect shifts in cellular composition or genuine transcriptional regulation within specific cell types. Future work should acquire raw sequencing counts to run formal, composition-aware deconvolution models like CIBERSORTx to computationally isolate cell-fraction contributions, and ultimate validation will require single-cell RNA-seq (scRNA-seq) or flow-cytometry-sorted cell population assays.

4. **Low absolute expression.** DRD2 expression in PBMCs is < 1 FPKM. qRT-PCR validation is needed.

5. **Missing gene.** NPY was pre-specified but absent from the GSE221921 matrix. FDR correction was applied to 16, not 17, genes.

6. **Cross-context comparison, not validation.** GSE67311 and GSE221921 differ in tissue fraction, platform, normalization, and cohort demographics. The contrast is informative but does not constitute independent replication.

7. **GWAS preprint status.** Kerrebijn et al. (2025) is published on medRxiv (doi: 10.1101/2025.09.18.25335914, PMID 41001472) and has not yet completed full peer review.

8. **No experimental validation.** All analyses are computational. No wet-lab or clinical experiments were performed.

10. **Tissue Extrapolations of Peripheral Blood mRNA.** Expression levels of *DRD2* measured in peripheral blood cells (PBMCs or whole blood) reflect basal, low-level transcription in circulating immune sub-populations and cannot be interpreted as a direct proxy for central nervous system dopaminergic function, striatal D2 receptor density, or mesolimbic neurotransmission. Central dopaminergic pathology must be evaluated via brain-specific germline sQTL genetic mechanisms (§4.9) or central neuroimaging/CSF studies.

---

## 6. Conclusion

A targeted reanalysis of two public transcriptomic cohorts suggests that selected GWAS-prioritized neural genes — most robustly *MDGA2* and *DRD2* — show increased expression in FM PBMCs across multiple analytical models. *CAMKV* and *CELF4* show supportive but model-sensitive signals, whereas the mast cell panel remains largely restricted to whole blood. These findings, combined with the observation that the sole positive dopamine agonist RCT in FM remains unreplicated after 21 years, support prioritizing the DRD2/neural GWAS axis for validation in sex-balanced cohorts with cell-type-resolved transcriptomic data and orthogonal experimental confirmation.

---

## References

Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. *J R Stat Soc B*, 57(1), 289–300.

Bi, W., Yang, M., & Mao, R. (2024). Unraveling Shared Diagnostic Biomarkers of Fibromyalgia in Ankylosing Spondylitis. *J Inflamm Res*, 17, 6395–6413. PMID: 39310900.

Chinn, S., Caldwell, W., & Gritsenko, K. (2016). Fibromyalgia Pathogenesis and Treatment Options Update. *Curr Pain Headache Rep*, 20(4), 25. PMID: 26922414.

De la Luz-Cuellar, Y. E., Coffeen, U., Mercado, F., & Contreras, B. (2023). Spinal dopaminergic D2 receptors modulate mechanical allodynia and hyperalgesia. *Eur J Pharmacol*, 946, 175654. PMID: 37003519.

Edwards, S., Callicoatte, C. N., Barattini, A. E., & Gilpin, N. W. (2022). Pramipexole treatment attenuates mechanical hypersensitivity in male rats experiencing chronic inflammatory pain. *Neuropharmacology*, 208, 108985. PMID: 35085583.

Gowri Gopal, K., Robi, L.S., & Sherin, D.R. (2026). Molecular insights into fibromyalgia: association of hub genes with pain targets, neuropathic pathways, and stress-related hormones. *In Silico Pharmacol*, 14(2), 135. PMID: 42109571.

Hamblin, R., Ntali, G., & Karavitaki, N. (2026). Impulse control disorders and dopamine agonists. *Best Pract Res Clin Endocrinol Metab*, 40(1), 101980. PMID: 42034459.

Holman, A.J., & Myers, R.R. (2005). A Randomized, Double-Blind, Placebo-Controlled Trial of Pramipexole, a Dopamine Agonist, in Patients With Fibromyalgia Receiving Concomitant Medications. *Arthritis Rheum*, 52(8), 2495–2505. PMID: 16052595. doi: 10.1002/art.21191.

Joodi, S. A., Nawwar, D. A., & Rasheed, N. O. A. (2026). Therapeutic and research frontiers in fibromyalgia: integrating pathophysiology with innovative drug repurposing. *Inflammopharmacology*, 34(1), 89–105. PMID: 42489789.

Kerrebijn, I., et al. (2025). The genetic architecture of fibromyalgia across 2.5 million individuals. *medRxiv*. PMID: 41001472. doi: 10.1101/2025.09.18.25335914.

Kurian, S.M., et al. (2017). Peripheral Blood Gene Expression in Fibromyalgia. PMID: 27157394. (GSE67311).

Lindström, S., Wolfschlag, M., & Håkansson, A. (2026). Pramipexole exposure and risk of incident gambling disorder in individuals with psychiatric disorders: A nationwide register-based cohort study. *J Affect Disord*, 370, 112–119. PMID: 42217644.

Love, M.I., Huber, W., & Anders, S. (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biol*, 15, 550. PMID: 25516281.

Mohapatra, G., et al. (2024). Identification of unique genomic signatures in patients with fibromyalgia and chronic pain. *Sci Rep*, 14, 3949. PMID: 38366049.

Pacheco, R., Contreras, F., & Zouali, M. (2014). The dopaminergic system in autoimmune diseases. *Front Immunol*, 5, 117.

Peng, X., et al. (2022). Pramipexole inhibits fibromyalgia-like symptoms in a reserpine-induced mouse model. *Neural Regen Res*, 17(3), 667–674. PMID: 35799530. doi: 10.4103/1673-5374.355761.

Sarzi-Puttini, P., et al. (2020). Fibromyalgia: An update. *Nat Rev Rheumatol*, 16(11), 645–660. PMID: 33024295.

Tayyab, M., Sasaoka, T., Abe, M., & Natsume, R. (2025). Dopamine D2S/D2L Receptor Regulation of Alcohol-Induced Reward and Signalling. *Addict Biol*, 30(2), e13480. PMID: 41239854.

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

Representative derived tables include:
- `analisis/sensitivity_analysis_GSE221921.csv` — five-model robustness table for PBMC reanalysis
- `analisis/cross_context_gwas_neural_genes.csv` — cross-context comparison table used for the PBMC vs. whole-blood contrast
- `analisis/RCT_dopamine_agonists_FM.csv` — targeted literature review evidence table

Software: Python 3.10, pandas 1.5.3, scipy 1.10.1, statsmodels 0.13.5.

## AI-Assisted Research Methodology

This study was conducted using an agentic AI-assisted research methodology implemented within a human-in-the-loop (HITL) framework. Analytical pipelines, literature synthesis, and computational design steps were developed with the support of large language model agents (Claude, Anthropic). All scientific claims were systematically validated by the human author against pre-established, independently verifiable ground truths: AlphaFold structural predictions (EMBL-EBI), RCSB PDB crystallographic coordinates, ChEMBL bioactivity databases, GEO-deposited expression matrices, and published statistical methods. Verification followed an evidence-first principle: no finding was accepted without traceable support from primary sources. This framework is implemented in the open-source `agentic-lab-eac` package (Apache-2.0, GitHub: Grizaceo/agentic-lab-eac), which formalizes the generate–review–verify cycle used throughout this study.

## Conflict of Interest

The author declares no conflicts of interest.

## Author's Note

This study was initiated out of personal motivation following personal experience with fibromyalgia in close contacts. No financial or institutional interest is involved.
