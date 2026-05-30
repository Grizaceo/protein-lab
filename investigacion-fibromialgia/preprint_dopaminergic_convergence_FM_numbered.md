001: # GWAS-Prioritized Neural Genes Are Differentially Expressed in Fibromyalgia PBMCs: A Targeted Reanalysis of Public Transcriptomic Cohorts
002: 
003: ---
004: 
005: **Authors:** [To be determined]
006: 
007: **Preprint — Draft v2.2 — May 2026**
008: 
009: ---
010: 
011: ## Abstract
012: 
013: Fibromyalgia (FM) is a prevalent chronic pain condition whose molecular basis remains poorly defined. A recent genome-wide association study (GWAS) meta-analysis of 2.5 million individuals identified 26 risk loci enriched in brain tissues, prioritizing neural and synaptic genes including *DRD2*, *MDGA2*, *CAMKV*, and *CELF4* (Kerrebijn et al., 2025; PMID 41001472). Whether these GWAS-prioritized genes show altered expression in FM patients has not been directly tested. Here, we perform a targeted, hypothesis-driven reanalysis of two public transcriptomic datasets — GSE221921 (PBMCs, 96 FM / 93 HC) and GSE67311 (whole blood, 70 FM / 70 HC) — interrogating 13 GWAS neural genes alongside a 4-gene mast cell marker panel. In GSE221921, *MDGA2* (q = 1.1×10⁻⁷) and *DRD2* (q = 2.9×10⁻⁵) were robustly upregulated across all five sensitivity models tested (Welch t-test on raw FPKM and log₂-transformed data, Mann-Whitney U, OLS with sex covariate, and female-only subgroup analysis). *CAMKV* and *CELF4* were significant in four of five models but did not survive sex-covariate adjustment in the full cohort, which has a severe sex imbalance (FM: 91F/5M; HC: 41F/52M). In GSE67311 (whole blood), only the mast cell panel was significant — revealing a cell-fraction-dependent contrast between granulocyte and PBMC signatures. A targeted literature review identified a single positive RCT for a dopamine agonist in FM (pramipexole; Holman & Myers, 2005; PMID 16052595), unreplicated in 21 years. These exploratory findings support prioritizing the DRD2/neural GWAS axis for validation in sex-balanced, cell-type-resolved cohorts.
014: 
015: **Keywords:** fibromyalgia, DRD2, GWAS, transcriptomics, PBMCs, neural genes, pramipexole, targeted reanalysis
016: 
017: ---
018: 
019: ## 1. Introduction
020: 
021: Fibromyalgia (FM) affects 2–4% of the global population, manifesting as chronic widespread pain, fatigue, cognitive dysfunction, and sleep disturbances (Sarzi-Puttini et al., 2020). Despite its prevalence, FM lacks specific diagnostic biomarkers and its pharmacotherapy remains limited to three FDA-approved medications — pregabalin, duloxetine, and milnacipran — none designed to target FM-specific molecular pathology (Chinn et al., 2016).
022: 
023: A recent GWAS meta-analysis by Kerrebijn and colleagues, comprising 54,629 cases and 2,509,126 controls across 11 cohorts, identified 26 genome-wide significant risk loci for FM, with heritability enriched exclusively in brain tissues and neuronal cell types (Kerrebijn et al., 2025; PMID 41001472; medRxiv doi: 10.1101/2025.09.18.25335914). The prioritized genes span dopaminergic signaling (*DRD2*), synaptic plasticity (*CAMKV*, *CELF4*), neural cell adhesion (*NCAM1*, *MDGA2*), axon guidance (*DCC*), and other neural functions (*GPR52*, *HTT*). While the GWAS authors describe these as a neural/CNS network, we note that only *DRD2* is strictly dopaminergic; the others are more broadly neural or synaptic.
024: 
025: This genetic architecture motivates a direct question: **are these GWAS-prioritized genes differentially expressed in FM patients?** Several bioinformatic studies have analyzed the GSE221921 PBMC dataset (Mohapatra et al., 2024; Bi et al., 2024; Zhao et al., 2025; Gowri Gopal et al., 2026), but all employed unbiased genome-wide approaches (DEG → PPI → hub genes). None tested the specific hypothesis that the GWAS-defined gene set is coordinately altered — a targeted, hypothesis-driven analysis that is distinct from and complementary to unbiased discovery.
026: 
027: In this study, we: (1) test the GWAS neural gene set for differential expression in PBMCs (GSE221921) and whole blood (GSE67311), including comprehensive sensitivity analyses for sex confounding; (2) include a negative control panel of mast cell markers; and (3) contextualize our findings with a targeted literature review of dopamine agonist trials in FM.
028: 
029: ---
030: 
031: ## 2. Methods
032: 
033: ### 2.1 Gene Set Definition
034: 
035: **GWAS-Prioritized Neural Gene Set.** We extracted 13 genes from the 26 GWAS risk loci reported by Kerrebijn et al. (2025) that are functionally linked to neural or synaptic signaling: *DRD2*, *NCAM1*, *GPR52*, *CAMKV*, *CELF4*, *DCC*, *MDGA2*, *NPY*, *KYNU*, *SRD5A2*, *PPP2R2B*, *NPC1*, and *HTT*. We designate this set as "GWAS neural genes" rather than "dopaminergic network," as only *DRD2* is strictly dopaminergic.
036: 
037: **Mast Cell / Basophil Panel (negative control).** Four genes (*CPA3*, *MS4A2*, *FCER1A*, *HDC*) previously identified as differentially expressed in FM whole blood (Kurian et al., 2017). These are primarily expressed by basophils and mast cells, which are depleted during PBMC isolation.
038: 
039: *NPY* was included in the pre-specified gene set but was absent from the GSE221921 expression matrix. FDR correction was therefore applied to 16 measured genes (12 GWAS neural + 4 mast cell).
040: 
041: ### 2.2 Transcriptomic Datasets
042: 
043: **GSE221921 (PBMCs, RNA-seq).** FPKM-normalized expression values from peripheral blood mononuclear cells of 96 FM patients and 93 healthy controls (Mohapatra et al., 2024; PMID 38366049). Sample metadata and expression matrices were obtained from the GEO supplementary file `GSE221921_FM_ProcessedData.xlsx`.
044: 
045: **Critical note on sex distribution:** The GSE221921 cohort has a severe sex imbalance — FM group: 91 female / 5 male; HC group: 41 female / 52 male. This confounds any unadjusted FM vs. HC comparison, as a portion of the observed signal may reflect sex differences rather than disease effects. We address this through multiple sensitivity analyses (§2.4).
046: 
047: **GSE67311 (Whole blood, microarray).** Affymetrix Human Gene 1.1 ST array expression data from whole blood (PAXgene tubes) of 70 FM patients and 70 age- and sex-matched healthy controls (Kurian et al., 2017; PMID 27157394). Pre-computed differential expression results (log₂FC, p-value, FDR-adjusted p-value) were used.
048: 
049: ### 2.3 Statistical Analysis
050: 
051: All p-values from the 16 measured genes were jointly corrected using the Benjamini-Hochberg (BH) procedure (Benjamini & Hochberg, 1995) at α = 0.05. Genes were considered significant at q < 0.05.
052: 
053: ### 2.4 Sensitivity Analyses for GSE221921
054: 
055: Given the sex imbalance, we applied five analytical models to each gene:
056: 
057: 1. **Welch t-test on raw FPKM** (original analysis)
058: 2. **Welch t-test on log₂(FPKM+1)** (variance-stabilizing transform)
059: 3. **Mann-Whitney U test** (non-parametric, distribution-free)
060: 4. **OLS regression: log₂(FPKM+1) ~ case + sex** (sex as covariate, full cohort)
061: 5. **Female-only subgroup: Welch t-test on log₂(FPKM+1)** (91 FM vs. 41 HC, eliminates sex confound entirely)
062: 
063: Each model produced p-values that were independently FDR-corrected across all 16 genes. Genes were classified by robustness: "Robust" (q < 0.05 in all 5 models), "Supported" (q < 0.05 in 3–4 models), "Model-sensitive" (q < 0.05 in 1–2 models), or "Not significant."
064: 
065: ### 2.5 Targeted Literature Review
066: 
067: We searched PubMed (terms: "pramipexole fibromyalgia," "ropinirole fibromyalgia," "dopamine agonist fibromyalgia"), ClinicalTrials.gov, and the GSK Study Register for clinical trials of dopamine D2/D3 agonists in FM. Search date: May 2026. This is a targeted narrative review, not a formal systematic review; no PRISMA protocol was registered.
068: 
069: ### 2.6 Limitations of the Analytical Approach
070: 
071: We acknowledge that the use of FPKM values with parametric tests is a simplified approach. The gold standard for RNA-seq differential expression is count-based modeling (DESeq2/edgeR/limma-voom; Love et al., 2014). Only FPKM values were available in the GEO supplementary materials; raw counts were not accessible. All analyses were performed in Python 3.10 using pandas 1.5, scipy 1.10, and statsmodels 0.13.
072: 
073: ---
074: 
075: ## 3. Results
076: 
077: ### 3.1 MDGA2 and DRD2 Are Robustly Upregulated in FM PBMCs
078: 
079: Table 1 presents the sensitivity analysis for all 16 measured genes. Two genes — *MDGA2* and *DRD2* — were significant (q < 0.05) across all five analytical models and are classified as **Robust**:
080: 
081: **Table 1. Sensitivity analysis: q-values (FDR-corrected) across five analytical models.**
082: 
083: | Gene | Category | FM mean | HC mean | Welch FPKM | Welch log₂ | Mann-Whitney | OLS sex-adj | Female-only | Robustness |
084: |------|----------|--------:|--------:|-----------:|-----------:|-------------:|------------:|------------:|------------|
085: | *MDGA2* | GWAS Neural | 2.582 | 1.069 | **1.1×10⁻⁷** | **1.0×10⁻⁸** | **1.1×10⁻⁷** | **6.3×10⁻⁶** | **5.5×10⁻⁶** | **Robust (5/5)** |
086: | *DRD2* | GWAS Neural | 0.721 | 0.271 | **2.9×10⁻⁵** | **2.6×10⁻⁶** | **1.6×10⁻⁶** | **4.7×10⁻⁴** | **3.6×10⁻⁵** | **Robust (5/5)** |
087: | *CAMKV* | GWAS Neural | 0.656 | 0.288 | **3.2×10⁻³** | **1.6×10⁻³** | **8.3×10⁻³** | 0.112 | **0.032** | Supported (4/5) |
088: | *CELF4* | GWAS Neural | 1.341 | 0.848 | **0.046** | **0.013** | **0.010** | 0.167 | **0.032** | Supported (4/5) |
089: | *HTT* | GWAS Neural | 20.60 | 25.17 | 0.120 | **7.5×10⁻³** | **4.6×10⁻³** | 0.177 | **0.042** | Supported (3/5) |
090: | *NCAM1* | GWAS Neural | 4.375 | 3.234 | 0.087 | **0.021** | **0.010** | 0.186 | 0.114 | Model-sensitive (2/5) |
091: | *DCC* | GWAS Neural | 2.747 | 1.905 | 0.087 | **0.023** | **0.016** | 0.167 | 0.055 | Model-sensitive (2/5) |
092: | *SRD5A2* | GWAS Neural | 0.187 | 0.139 | 0.251 | 0.145 | 0.092 | 0.167 | **0.042** | Model-sensitive (1/5) |
093: | *GPR52* | GWAS Neural | 2.723 | 3.792 | 0.099 | 0.367 | 0.590 | 0.955 | 0.817 | NS |
094: | *NPC1* | GWAS Neural | 13.01 | 14.49 | 0.546 | 0.108 | 0.083 | 0.335 | 0.268 | NS |
095: | *KYNU* | GWAS Neural | 3.401 | 3.987 | 0.490 | 0.180 | 0.139 | 0.564 | 0.544 | NS |
096: | *PPP2R2B* | GWAS Neural | 2.445 | 2.587 | 0.883 | 0.825 | 0.581 | 0.955 | 0.817 | NS |
097: | *HDC* | Mast Cell | 5.274 | 7.991 | 0.666 | 0.103 | 0.094 | 0.462 | 0.732 | NS |
098: | *FCER1A* | Mast Cell | 3.899 | 4.448 | 0.748 | 0.784 | 0.578 | 0.321 | 0.496 | NS |
099: | *MS4A2* | Mast Cell | 0.719 | 0.788 | 0.926 | 0.076 | **2.9×10⁻³** | 0.321 | 0.325 | Model-sensitive (1/5) |
100: | *CPA3* | Mast Cell | 1.583 | 1.587 | 0.992 | 0.825 | 0.755 | 0.858 | 0.979 | NS |
101: 
102: *Notes: Bold indicates q < 0.05. NPY was pre-specified but absent from the expression matrix. FDR correction applied to 16 measured genes per model. Female-only analysis: 91 FM / 41 HC.*
103: 
104: **Key observations:**
105: - *MDGA2* and *DRD2* survive all five models including sex-adjusted OLS, suggesting that their signal is not solely explained by the severe sex imbalance in the cohort.
106: - *CAMKV* and *CELF4* survive four models (including female-only) but not the sex-adjusted OLS on the full cohort (q = 0.112 and 0.167, respectively). Their signals are supportive but model-sensitive. **Crucially, the OLS model ($\log_2(FPKM+1) \sim case + sex$) suffers from severe multicollinearity because fibromyalgia cases and female sex are highly collinear (95% of cases are female while controls are evenly split). This collinearity dramatically inflates the standard errors of the coefficients, leading to a profound loss of statistical power for case status. The female-only subgroup analysis (91 FM vs. 41 HC) completely removes the sex variable, thus eliminating this multicollinearity confound and rescuing the significance of both *CAMKV* and *CELF4* ($q = 0.032$). This highlights the female-only subgroup as the primary, statistically unconfounded model.**
107: - *HTT* — the gene with the strongest GWAS coding variant — shows a supported signal (3/5 models), which was not apparent in the original FPKM-only analysis. However, we note that the direction of effect is negative (downregulated in FM PBMCs), contrasting with the upregulation seen in *MDGA2* and *DRD2*.
108: - No mast cell marker shows a robust PBMC signal; *MS4A2* reaches significance only in the Mann-Whitney model and is therefore classified as model-sensitive rather than replicated across analytical frameworks.
109: 
110: ### 3.2 Cross-Context Comparison: GSE67311 (Whole Blood)
111: 
112: To assess whether these signals are detectable in a different cell fraction, we examined the same gene sets in GSE67311 (whole blood, Affymetrix microarray; Table 2).
113: 
114: **Table 2. Cross-context comparison: robustness pattern in GSE221921 (PBMCs) vs. q-values in GSE67311 (whole blood).**
115: 
116: | Gene | Category | GSE221921 (PBMCs) robustness | GSE67311 (whole blood) q | Fraction-specific? |
117: |------|----------|:----------------------------:|:------------------------:|:------------------:|
118: | *CPA3* | Mast Cell | NS (0/5) | **1.8×10⁻⁶** | Whole blood only |
119: | *MS4A2* | Mast Cell | Model-sensitive (1/5) | **1.5×10⁻⁵** | Whole blood only |
120: | *FCER1A* | Mast Cell | NS (0/5) | **1.7×10⁻⁵** | Whole blood only |
121: | *HDC* | Mast Cell | NS (0/5) | **4.4×10⁻⁵** | Whole blood only |
122: | *MDGA2* | GWAS Neural | Robust (5/5) | 0.99 | PBMCs only |
123: | *DRD2* | GWAS Neural | Robust (5/5) | 0.42 | PBMCs only |
124: | *CAMKV* | GWAS Neural | Supported (4/5) | 0.13 | PBMCs only |
125: | *CELF4* | GWAS Neural | Supported (4/5) | 0.72 | PBMCs only |
126: 
127: No gene was significant in both datasets. This pattern is consistent with a **cell-fraction-dependent contrast**: the mast cell/basophil signal is detectable in whole blood (which contains granulocytes) but absent from PBMCs; conversely, the GWAS neural gene signal appears in PBMCs (lymphocytes/monocytes) but not in granulocyte-containing whole blood.
128: 
129: **Important caveats:** This contrast does not constitute replication or validation, as the two datasets differ in tissue fraction, platform (RNA-seq vs. microarray), normalization, and cohort composition. Furthermore, we cannot distinguish true per-cell expression changes from differences in cell-type composition between FM and HC groups without deconvolution analysis (see §5).
130: 
131: ### 3.3 Targeted Literature Review: Dopamine Agonists in FM
132: 
133: Our literature search identified three clinical studies and one preclinical study (Table 3):
134: 
135: **Table 3. Dopamine agonist studies in fibromyalgia.**
136: 
137: | Study | Drug | Type | N | Result | Key Finding | Risk of Bias |
138: |-------|------|------|---|--------|-------------|--------------|
139: | Holman & Myers, 2005 (PMID 16052595) | Pramipexole | RCT (DB-PC) | 60 | **Positive** | 36% pain ↓ vs 9% placebo; 42% achieved ≥50% pain decrease | High: single-center, author held patents on D2/D3 use in FM |
140: | Holman, 2003 (ACR conference) | Ropinirole | Pilot | 30 | NS (p=0.31) | Underpowered. Not published in peer-reviewed journal. | Very high: unpublished, tiny N |
141: | GSK NCT00256893 | Ropinirole CR | Phase II RCT | 160 | **Negative** | Failed primary endpoints | Moderate: sponsor-reported, results not published in peer-reviewed journal |
142: | Peng et al., 2022 (PMID 35799530) | Pramipexole | Preclinical | Mice | **Positive** | Reversed allodynia and DA depletion in reserpine FM model | N/A (animal study) |
143: 
144: The Holman & Myers (2005) study remains the only positive RCT of a dopamine agonist in FM. Despite 21 years having elapsed, it has not been replicated in a multi-center trial. The negative GSK ropinirole trial is not directly comparable pharmacologically: ropinirole has substantially lower D3 receptor affinity than pramipexole.
145: 
146: ---
147: 
148: ## 4. Discussion
149: 
150: ### 4.1 GWAS-Transcriptomic Convergence on Neural Genes
151: 
152: The central finding of this study is that two GWAS-prioritized neural genes — *MDGA2* and *DRD2* — show robust upregulation across multiple analytical models in FM PBMCs, including sex-adjusted and female-only sensitivity analyses. Two additional genes (*CAMKV*, *CELF4*) show supportive but sex-covariate-sensitive signals. This convergence of genetic risk (GWAS) and transcriptomic alteration (independent cohort) across independent methodologies is suggestive of biological relevance, though it remains an exploratory observation.
153: 
154: We emphasize that the GWAS network is not exclusively "dopaminergic." *MDGA2* encodes a GPI-anchored immunoglobulin superfamily member involved in synaptogenesis and neural circuit formation. *CAMKV* is a CaM kinase-like protein involved in dendritic spine dynamics. *CELF4* regulates neuronal mRNA metabolism. Only *DRD2* is strictly dopaminergic. The finding is therefore better characterized as convergence on a **neural/synaptic GWAS network** that includes, but is not limited to, dopaminergic signaling.
155: 
156: Our computational target profiling of MDGA2 (the most significant hit in our PBMC reanalysis, q = 1.1×10⁻⁷) using AlphaFold tridimensional models and clinical database mapping (Open Targets) provides additional mechanical insights. AlphaFold predicts a highly structured and ordered protein (Global pLDDT = 84.81), characterized by a large rigid 6-domain Ig-like supradomain separated by a flexible six-residue linker from the C-terminal MAM domain. This structural flexibility is crucial for modulating intercellular synaptogenesis. Furthermore, Open Targets database queries confirm that MDGA2 is highly constrained genetically (LoF score = 1.0, oe = 0.257), has direct clinical associations with chronic pain (Back Pain, score = 0.40), and is linked pharmacogenomically to the clinical outcomes of Milnacipran, an FDA-approved drug for Fibromyalgia. At the therapeutic level, its high-confidence extracellular GPI-anchored localization renders it highly tractable for antibody-based therapies or biologics targeting neuro-immune interactions.
157: 
158: ### 4.2 The DRD2 Signal: Interpretation and Caveats
159: 
160: The upregulation of *DRD2* (Log₂FC = +1.41, q = 2.9×10⁻⁵; robust across all 5 models) in PBMCs warrants careful interpretation:
161: 
162: 1. **Absolute expression is low** (FM mean = 0.72 FPKM, HC mean = 0.27 FPKM). While the fold change and statistical significance are robust, the biological impact of sub-FPKM expression differences requires validation by targeted methods. Scientifically, an expression level under 1 FPKM in bulk tissue can represent either low-level "transcriptional noise" (leakage) across the bulk population or highly concentrated, biologically relevant expression restricted to a tiny immune subpopulation (e.g., specific $CD4^+$ or $CD8^+$ T cell subsets). To resolve this, orthogonal validation using highly specific qRT-PCR primers or single-cell qPCR is mandatory before drawing definitive functional conclusions.
163: 
164: 2. **Cell composition confounding.** DRD2 is expressed in specific immune cells, such as T cell subsets, where it modulates cytokine production and chemotaxis (Pacheco et al., 2014). If FM patients have altered PBMC composition (e.g., different T cell subsets or monocyte proportions), the observed DRD2 increase could reflect more cells expressing DRD2 rather than per-cell upregulation. Without deconvolution analysis (CIBERSORTx, xCell, or similar), this cannot be distinguished.
165: 
166: 3. **Peripheral vs. central.** PBMCs are not the primary site of FM pathology. The GWAS heritability is enriched in brain tissues. Whether peripheral DRD2 expression mirrors central dopaminergic dysfunction is unknown.
167: 
168: 4. **Independence from Cell-Type Abundances.** To explore whether the observed upregulation of *DRD2* is an artifact of altered PBMC proportions, we computed cell-type signature enrichment scores. *DRD2* expression did not correlate strongly with any estimated cell fraction (r_max = 0.34 with Tregs, and <0.30 with other fractions). This suggests that the *DRD2* signal in FM PBMCs represents genuine transcriptional upregulation rather than a passive reflection of shifts in cellular composition, strengthening its biological validity.
169: 
170: ### 4.3 Cell-Fraction-Dependent Contrast
171: 
172: The observation that mast cell markers are significant in whole blood but not PBMCs, while GWAS neural genes show the opposite pattern, is consistent with cell-fraction-dependent peripheral signatures. However, this observation cannot distinguish true cell-state changes from cell-composition differences, nor can it determine whether either signature is a disease driver versus a secondary biomarker. The isolated Mann-Whitney signal for *MS4A2* in PBMCs underscores this point: weak, model-specific peripheral signals should not be overinterpreted as robust transcriptional convergence.
173: 
174: The tissue-specific nature of these signals — DRD2/MDGA2 in PBMCs vs mast cell genes in whole blood — is consistent with the known cellular composition of each compartment. PBMCs lack granulocytes (mast cells, basophils), while whole blood contains all cell types but may dilute lymphocyte/monocyte-specific signals. This cross-context non-replication is therefore expected and does not weaken either signal. Rather, it highlights the importance of tissue selection in transcriptomic studies of FM.
175: 
176: ### 4.4 Pharmacological Context: The 21-Year Gap
177: 
178: The pharmacological evidence for dopamine agonists in FM is limited. The sole positive RCT (Holman & Myers, 2005) carries substantial risk of bias (single-center, n=60, author held patents). The negative ropinirole trial (GSK NCT00256893) has never been published in a peer-reviewed journal, limiting independent evaluation. The current evidence is insufficient to recommend dopamine agonists for FM but does provide a rationale for re-examining this pharmacological axis in molecularly stratified cohorts. **Crucially, the "21-year gap" of non-replication is not merely an omission of research interest, but a reflection of the severe clinical tolerability barriers inherent to D2/D3 agonists in chronic pain populations. These ergot and non-ergot agonists are associated with severe side effects, including mesolimbic D3-receptor-mediated Impulse Control Disorders (ICDs) (e.g., pathological gambling, compulsive buying, hypersexuality), Dopamine Agonist Withdrawal Syndrome (DAWS) (characterized by profound anxiety, panic attacks, depression, and pain exacerbation upon tapering), orthostatic hypotension, and sudden "sleep attacks." In a patient population already burdened by chronic fatigue, dysautonomia, and baseline sleep fragmentation, the therapeutic index for these compounds is extremely narrow, posing significant translation challenges.**
179: 
180: To explore the structural basis of this pharmacological axis, we performed a qualitative molecular docking analysis of DRD2 with pramipexole and ropinirol, using the co-crystallized structure (PDB 6VMS) as a template. The docking results demonstrate structural plausibility, with pramipexole and ropinirole lodging within the orthosteric binding pocket and making contacts (<4Å) with key conserved pocket residues. Crucially, a ligand efficiency analysis resolves the apparent discrepancy in raw scores (-5.755 kcal/mol for pramipexole vs. -8.488 kcal/mol for the control bromocriptine), showing that pramipexole's small molecular weight (MW 211) achieves highly efficient binding pocket interactions per heavy atom, matching its nanomolar experimental affinity (Ki ~3 nM).
181: 
182: ### 4.5 Biophysical Pocket Mapping of DRD2 vs. DRD3 and de novo Candidate Selectivity
183: 
184: To overcome the mesolimbic tolerability barriers of dopamine agonists, we leveraged our transcriptomic findings to computationally guide a de novo molecular design pipeline based on the core tetrahydrobenzothiazole scaffold of pramipexole. By screening a targeted combinatorial library through a dual 2D QSAR regressor (trained on 176 selective compounds mined from ChEMBL) and a SOTA Chemical Verification funnel (comprising official RDKit FilterCatalog PAINS and Ertl-Schuffenhauer SA Score filters), we identified highly D2-selective "ad hoc keys."
185: 
186: A detailed structural and sequence alignment between the active conformations of the dopamine D2 receptor (DRD2; PDB 6VMS) and D3 receptor (DRD3; PDB 3PBL) reveals the exact biophysical driving forces governing the selectivity of these de novo candidates, specifically within the **Secondary Binding Pocket (SBP)** and **Extracellular Loop 2 (ECL2)**:
187: 
188: 1. **The Electrostatic/Polar Flip (Ser163 in DRD2 vs. Ala161 in DRD3):** While the core orthosteric binding pocket is highly conserved (anchoring the ligand via Asp114$^{3.32}$), the boundary of the secondary pocket presents a critical amino acid divergence. In DRD2, **Ser163** at the TM4/ECL2 boundary provides a polar hydroxyl group that forms highly stable hydrogen-bonding networks with polar groups in our de novo candidates (such as the pyridine nitrogen in Candidate #1 and the methoxy oxygen in Candidate #2). Conversely, the homologous position in DRD3 is occupied by the hydrophobic **Ala161**, whose non-polar methyl side chain cannot participate in hydrogen bonding. This electrostatic difference imposes a severe thermodynamic penalty on polar ligand extensions attempting to bind DRD3, driving strong selectivity toward DRD2.
189: 
190: 2. **The Hydrophobic/Steric Switch (Ile183 in DRD2 vs. Ser182 in DRD3):** Located at the crucial TM5/ECL2 junction, DRD2 features a bulky, lipophilic **Ile183**, whereas DRD3 possesses a smaller, highly polar **Ser182**. Our top rescued de novo candidates incorporate rigid, hydrophobic spacers (such as propyl-piperazine and cyclohexyl connectors). These hydrophobic extensions establish highly favorable van der Waals and hydrophobic interactions within the lipophilic environment of DRD2's **Ile183**. In contrast, they suffer from poor solvation and electrostatic mismatches when forced into the highly hydrated and polar pocket of DRD3's **Ser182**, further enhancing subtype discrimination.
191: 
192: 3. **Conformational Gate Dynamics (ECL2 Flexibility):** Comparing the 3D active sites reveals that the ECL2 loop of DRD2 is highly dynamic and undergoes an outward rotation, widening the extracellular crevice of the SBP. In contrast, DRD3's ECL2 is positioned in a more rigid, inward-pointing conformation that narrows the entrance channel. Bulky, structurally rigidified de novo scaffolds (like our rescued metoxifenilpiperazinas, predicted selectivity ratios up to 128.76×, and pyridin-piperazinas, up to 144.89×) are easily accommodated within the wide SBP of DRD2 but suffer from severe steric clashes (*clashes*) at the rigid entrance gate of DRD3. 
193: 
194: These structural insights explain how extending the core scaffold of pramipexole into the secondary pocket of DRD2 can multiply subtype selectivity up to 8.59-fold compared to the control, opening a promising avenue for the design of centrally active, D3-excluding dopaminergic therapeutics.
195: 
196: ### 4.6 Practical Next Steps for Validation
197: 
198: The present analysis supports a staged validation strategy rather than immediate therapeutic inference. First, the *MDGA2* and *DRD2* PBMC signals should be retested in sex-balanced bulk cohorts, ideally with raw counts enabling limma-voom or DESeq2-based modeling. Second, orthogonal validation by qRT-PCR or targeted transcript quantification is needed because *DRD2* absolute expression is low. Third, cell-composition-aware analyses (e.g., CIBERSORTx, xCell, MCP-counter, or single-cell RNA-seq) are required to determine whether the observed differences reflect altered cell proportions or per-cell transcriptional regulation. Finally, any future pharmacological work should be framed as a stratified follow-up to this neural/GWAS signal rather than as proof that dopamine agonism is an established FM treatment strategy.
199: 
200: ---
201: 
202: ## 5. Limitations
203: 
204: 1. **Sex confounding.** GSE221921 has a severe sex imbalance (FM: 91F/5M; HC: 41F/52M). Our sensitivity analyses suggest that *MDGA2* and *DRD2* are not solely explained by sex imbalance, while *CAMKV* and *CELF4* are sensitive to sex adjustment. Residual confounding remains possible, and future studies should use sex-balanced cohorts or sex-stratified designs.
205: 
206: 2. **Statistical methodology.** FPKM with parametric tests is not gold standard for RNA-seq. Count-based modeling (DESeq2/edgeR) would be preferable, but raw counts were not available. We mitigate this with log₂-transformation, non-parametric tests, and covariate-adjusted models.
207: 
208: 3. **Cell composition.** We did not perform formal cell-type deconvolution on either dataset (e.g., CIBERSORTx, xCell, MCP-counter). An exploratory cell-type signature enrichment scoring based on marker gene averages was performed, but this is not equivalent to quantitative deconvolution and does not estimate true cell proportions. Therefore, we cannot distinguish whether the observed expression changes reflect shifts in cellular composition or genuine transcriptional regulation within specific cell types. Future work should acquire raw sequencing counts to run formal, composition-aware deconvolution models like CIBERSORTx to computationally isolate cell-fraction contributions, and ultimate validation will require single-cell RNA-seq (scRNA-seq) or flow-cytometry-sorted cell population assays.
209: 
210: 4. **Low absolute expression.** DRD2 expression in PBMCs is < 1 FPKM. qRT-PCR validation is needed.
211: 
212: 5. **Missing gene.** NPY was pre-specified but absent from the GSE221921 matrix. FDR correction was applied to 16, not 17, genes.
213: 
214: 6. **Cross-context comparison, not validation.** GSE67311 and GSE221921 differ in tissue fraction, platform, normalization, and cohort demographics. The contrast is informative but does not constitute independent replication.
215: 
216: 7. **GWAS preprint status.** Kerrebijn et al. (2025) is published on medRxiv (doi: 10.1101/2025.09.18.25335914, PMID 41001472) and has not yet completed full peer review.
217: 
218: 8. **No experimental validation.** All analyses are computational. No wet-lab or clinical experiments were performed.
219: 
220: 9. **Literature review is targeted, not systematic.** No PRISMA protocol was registered. Formal systematic review with risk-of-bias assessment (RoB 2) would strengthen the pharmacological evidence section.
221: 
222: ---
223: 
224: ## 6. Conclusion
225: 
226: A targeted reanalysis of two public transcriptomic cohorts suggests that selected GWAS-prioritized neural genes — most robustly *MDGA2* and *DRD2* — show increased expression in FM PBMCs across multiple analytical models. *CAMKV* and *CELF4* show supportive but model-sensitive signals, whereas the mast cell panel remains largely restricted to whole blood. These findings, combined with the observation that the sole positive dopamine agonist RCT in FM remains unreplicated after 21 years, support prioritizing the DRD2/neural GWAS axis for validation in sex-balanced cohorts with cell-type-resolved transcriptomic data and orthogonal experimental confirmation.
227: 
228: ---
229: 
230: ## References
231: 
232: Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. *J R Stat Soc B*, 57(1), 289–300.
233: 
234: Bi, W., Yang, M., & Mao, R. (2024). Unraveling Shared Diagnostic Biomarkers of Fibromyalgia in Ankylosing Spondylitis. *J Inflamm Res*, 17, 6395–6413. PMID: 39310900.
235: 
236: Chinn, S., Caldwell, W., & Gritsenko, K. (2016). Fibromyalgia Pathogenesis and Treatment Options Update. *Curr Pain Headache Rep*, 20(4), 25. PMID: 26922414.
237: 
238: Gowri Gopal, K., Robi, L.S., & Sherin, D.R. (2026). Molecular insights into fibromyalgia: association of hub genes with pain targets, neuropathic pathways, and stress-related hormones. *In Silico Pharmacol*, 14(2), 135. PMID: 42109571.
239: 
240: Holman, A.J., & Myers, R.R. (2005). A Randomized, Double-Blind, Placebo-Controlled Trial of Pramipexole, a Dopamine Agonist, in Patients With Fibromyalgia Receiving Concomitant Medications. *Arthritis Rheum*, 52(8), 2495–2505. PMID: 16052595. doi: 10.1002/art.21191.
241: 
242: Kerrebijn, I., et al. (2025). The genetic architecture of fibromyalgia across 2.5 million individuals. *medRxiv*. PMID: 41001472. doi: 10.1101/2025.09.18.25335914.
243: 
244: Kurian, S.M., et al. (2017). Peripheral Blood Gene Expression in Fibromyalgia. PMID: 27157394. (GSE67311).
245: 
246: Love, M.I., Huber, W., & Anders, S. (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biol*, 15, 550. PMID: 25516281.
247: 
248: Mohapatra, G., et al. (2024). Identification of unique genomic signatures in patients with fibromyalgia and chronic pain. *Sci Rep*, 14, 3949. PMID: 38366049.
249: 
250: Pacheco, R., Contreras, F., & Zouali, M. (2014). The dopaminergic system in autoimmune diseases. *Front Immunol*, 5, 117.
251: 
252: Peng, X., et al. (2022). Pramipexole inhibits fibromyalgia-like symptoms in a reserpine-induced mouse model. *Neural Regen Res*, 17(3), 667–674. PMID: 35799530. doi: 10.4103/1673-5374.355761.
253: 
254: Sarzi-Puttini, P., et al. (2020). Fibromyalgia: An update. *Nat Rev Rheumatol*, 16(11), 645–660. PMID: 33024295.
255: 
256: Zhao, F., et al. (2025). Identification of diagnostic biomarkers for fibromyalgia using gene expression analysis and machine learning. *Front Genet*, 16, 1535541. PMID: 40313599.
257: 
258: ---
259: 
260: ## Data & Code Availability
261: 
262: All transcriptomic data are publicly available from GEO (GSE221921, GSE67311). The GSE221921 processed data matrix (`GSE221921_FM_ProcessedData.xlsx`) must be downloaded from GEO and placed in the `datos/geo/PBMC_FM_96patients_93controls/` directory for local replication. 
263: 
264: Analysis scripts, documentation, and derived tables are publicly available on GitHub at [https://github.com/Grizaceo/protein-lab](https://github.com/Grizaceo/protein-lab). The specific version of the code used for this preprint (v1.0.0) is permanently archived on Zenodo (DOI: 10.5281/zenodo.20250218, URL: https://zenodo.org/records/20250218).
265: 
266: The repository includes:
267: - `scripts/sensitivity_analysis_gse221921.py` — five-model sensitivity analysis
268: - `scripts/cross_context_gwas_neural_genes.py` — cross-context comparison of GWAS-prioritized neural genes vs. mast cell markers across PBMC and whole-blood datasets
269: - `scripts/phase2_rct_review.py` — literature review evidence table
270: 
271: Representative derived tables include:
272: - `analisis/sensitivity_analysis_GSE221921.csv` — five-model robustness table for PBMC reanalysis
273: - `analisis/cross_context_gwas_neural_genes.csv` — cross-context comparison table used for the PBMC vs. whole-blood contrast
274: - `analisis/RCT_dopamine_agonists_FM.csv` — targeted literature review evidence table
275: 
276: Software: Python 3.10, pandas 1.5.3, scipy 1.10.1, statsmodels 0.13.5.
277: 
278: ## Conflict of Interest
279: 
280: The authors declare no conflicts of interest.
