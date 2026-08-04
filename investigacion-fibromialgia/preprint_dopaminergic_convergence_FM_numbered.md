001: # Peripheral Neuroimmune and Nociceptive Gene Signatures in Fibromyalgia: A Targeted Reanalysis of Public Transcriptomic Cohorts Informed by UK Biobank Plasma Proteomics
002: 
003: ---
004: 
005: **Authors:** Cristóbal Muñoz Rojas¹
006: 
007: ¹ Independent Researcher, Santiago, Chile. Correspondence: cristoe4@gmail.com
008: 
009: **Preprint — Draft v2.7 — August 2026**
010: 
011: ---
012: 
013: ## Abstract
014: 
015: Fibromyalgia (FM) is a prevalent chronic pain condition whose molecular basis remains poorly defined. A genome-wide association study (GWAS) meta-analysis of 2.5 million individuals identified 26 risk loci enriched in brain tissues, prioritizing neural and synaptic genes including *DRD2*, *MDGA2*, *CAMKV*, and *CELF4* (Kerrebijn et al., 2025; PMID 41001472). Separately, the largest population-scale plasma proteomics studies of chronic pain (UK Biobank Olink) found no support for the classical IL-6/IL-8 inflammatory axis and instead triangulated CA14 (carbonic anhydrase XIV) as a causal protein in chronic widespread pain via Mendelian randomization and colocalization (Chen et al., 2025, *Adv Sci*; PMID 41025730). Here we perform a targeted, hypothesis-driven reanalysis of two public transcriptomic datasets — GSE221921 (PBMCs, 96 FM / 93 HC) and GSE67311 (whole blood, 67 FM / 75 HC) — interrogating GWAS neural genes, the opioid/tachykinin neuropeptide axis, UKB causal genes, and mast cell markers. In GSE221921 PBMCs we find: (1) *MDGA2* (q = 1.1×10⁻⁷) and *DRD2* (q = 2.9×10⁻⁵) robustly upregulated across all five sensitivity models; (2) a **complete opioid/tachykinin neuropeptide circuit activated** — receptor *TACR1* (NK1, Substance P receptor; FC = 2.73, d = +0.60, the largest effect size in the panel), *OPRM1* (μ-opioid receptor; FC = 2.28, d = +0.53), ligand *TAC1* (Substance P; FC = 2.10, d = +0.47) and *OPRK1* (κ-opioid; FC = 1.78, d = +0.38), with coordinated co-expression (rho = 0.31–0.63) — the largest effect-size block and the most robust finding of the investigation, surviving all five sensitivity models including sex-stratified analysis; (3) **two extracellular-matrix / neurite-outgrowth genes from the chronic-widespread-pain causal set — *COL9A1* (FC = 2.32, d = +0.88) and *PTN* (FC = 2.91, d = +0.61) — are the only genes that survive Bonferroni correction on the sex-adjusted model in FM PBMC mRNA**, forming a co-expressed module (r = 0.51) with direct relevance to joint pain and nerve repair, and detectable in plasma by Olink; and (4) **CA14 — the top UKB causal protein for chronic widespread pain — upregulated in FM PBMC mRNA in the unadjusted analysis** (FC = 2.29, p = 0.0003, d = +0.41) **but not surviving the sex-stratified primary model** (female-only p = 0.135), while being **downregulated in plasma** in the UKB cross-sectional analysis, with MR indicating a protective effect of genetically elevated CA14 — relegated here to a reference candidate rather than the primary validation target. Together these signatures reframe the peripheral biology of FM as **neuropeptide nociceptive signaling plus extracellular-matrix / neurite-outgrowth dysregulation (COL9A1–PTN) with immunomodulation (UKB immune genes) and pH/nociception dysregulation (CA14)** — and we recommend prioritizing **COL9A1 and PTN** (Olink, plasma-detectable, Bonferroni-surviving) in the confirmatory plasma validation, with CA14 measured as a direction-specific reference. In GSE67311 (whole blood), these PBMC-derived proxies do not replicate in absolute expression (TAC1/OPRM1/IL6 FC ≈ 1.0); deconvolution rules out neutrophil-driven dilution; the co-expression structure of the axis is partially preserved (5 of 10 pairs show FM > HC, but 2 reverse with HC > FM) — the circuit is transcriptionally coherent in FM, while its amplitude is compartment-dependent. These findings argue that the peripheral molecular signature of FM is dominated by **neuropeptide nociceptive signaling and extracellular-matrix dysregulation**, not classical inflammation, and support prioritizing COL9A1 and PTN for validation in plasma (Olink) with cell-type-resolved, medication-stratified cohorts.
016: 
017: **Keywords:** fibromyalgia, COL9A1, PTN, CA14, TACR1, OPRM1, tachykinin, opioid, extracellular matrix, UK Biobank, Olink, PBMCs, targeted reanalysis, nociception, immunomodulation
018: 
019: ---
020: 
021: ## 1. Introduction
022: 
023: Fibromyalgia (FM) affects 2–4% of the global population, manifesting as chronic widespread pain, fatigue, cognitive dysfunction, and sleep disturbances (Sarzi-Puttini et al., 2020). Despite its prevalence, FM lacks specific diagnostic biomarkers and its pharmacotherapy remains limited to three FDA-approved medications — pregabalin, duloxetine, and milnacipran — none designed to target FM-specific molecular pathology (Chinn et al., 2016).
024: 
025: A recent GWAS meta-analysis by Kerrebijn and colleagues, comprising 54,629 cases and 2,509,126 controls across 11 cohorts, identified 26 genome-wide significant risk loci for FM, with heritability enriched exclusively in brain tissues and neuronal cell types (Kerrebijn et al., 2025; PMID 41001472; medRxiv doi: 10.1101/2025.09.18.25335914). The prioritized genes span dopaminergic signaling (*DRD2*), synaptic plasticity (*CAMKV*, *CELF4*), neural cell adhesion (*NCAM1*, *MDGA2*), axon guidance (*DCC*), and other neural functions (*GPR52*, *HTT*). While the GWAS authors describe these as a neural/CNS network, we note that only *DRD2* is strictly dopaminergic; the others are more broadly neural or synaptic.
026: 
027: This genetic architecture motivates a direct question: **are these GWAS-prioritized genes differentially expressed in FM patients?** Several bioinformatic studies have analyzed the GSE221921 PBMC dataset (Mohapatra et al., 2024; Bi et al., 2024; Zhao et al., 2025; Gowri Gopal et al., 2026), but all employed unbiased genome-wide approaches (DEG → PPI → hub genes). None tested the specific hypothesis that the GWAS-defined gene set is coordinately altered — a targeted, hypothesis-driven analysis that is distinct from and complementary to unbiased discovery.
028: 
029: In parallel, population-scale plasma proteomics has reframed the peripheral biology of chronic pain. Li ZY et al. (2025; PMID 40048323) profiled 2,923 plasma proteins (Olink Explore) in 51,644 UK Biobank participants with chronic pain, identifying 474 pain-associated proteins and 10 proteins validated as causal by Mendelian randomization — none of them classical inflammatory cytokines. A dedicated FM/nociplastic analysis of the UKB Olink data (Chen et al., 2025, *Adv Sci*; PMID 41025730; 29,254 participants, 2,920 proteins) built multi-protein scores with AUC 0.856–0.880 for CWP, identified 18 proteins with causal relevance by MR, and triangulated **CA14 (carbonic anhydrase XIV)** as the top causal protein by MR + colocalization (PP.H4 > 0.5). Notably, CA14 is **downregulated in plasma** in the cross-sectional analysis while genetically elevated CA14 is protective by MR; and the authors propose **CA14 agonists, not the inhibitor sulthiame**, as the more promising therapeutic direction. Critically, IL-6, IL-8/CXCL8, TAC1 and Substance P appear **zero times** in the largest published chronic pain proteomics screen — the classical inflammatory axis is not supported at population scale.
030: 
031: In this study, we: (1) test the GWAS neural gene set for differential expression in PBMCs (GSE221921) and whole blood (GSE67311), including comprehensive sensitivity analyses for sex confounding; (2) extend the analysis to the **opioid/tachykinin neuropeptide axis** (ligands *TAC1*, *PENK*, *PNOC*, *POMC*; receptors *TACR1*, *OPRM1*, *OPRK1*, *OPRD1*); (3) test the **UKB causal genes** (CA14, TNFRSF1B, CD74, COL18A1, BTN2A1, TNFRSF4, CD302, TNFRSF9) in our PBMC data to connect population-scale causal proteomics with transcriptomics; (4) include a negative control panel of mast cell markers; and (5) contextualize our findings with a targeted literature review of dopamine agonist trials in FM and the pharmacology of CA14.
032: 
033: ---
034: 
035: ## 2. Methods
036: 
037: ### 2.1 Gene Set Definition
038: 
039: **GWAS-Prioritized Neural Gene Set.** We extracted 13 genes from the 26 GWAS risk loci reported by Kerrebijn et al. (2025) that are functionally linked to neural or synaptic signaling: *DRD2*, *NCAM1*, *GPR52*, *CAMKV*, *CELF4*, *DCC*, *MDGA2*, *NPY*, *KYNU*, *SRD5A2*, *PPP2R2B*, *NPC1*, and *HTT*. We designate this set as "GWAS neural genes" rather than "dopaminergic network," as only *DRD2* is strictly dopaminergic.
040: 
041: **Opioid/Tachykinin Neuropeptide Axis.** Ligands: *TAC1* (Substance P), *PENK* (enkephalins), *PNOC* (nociceptin), *POMC* (β-endorphin). Receptors: *TACR1* (NK1), *OPRM1* (μ-opioid), *OPRK1* (κ-opioid), *OPRD1* (δ-opioid). HGNC symbols verified (TAC1 = Substance P; PENK = proenkephalin — a distinct opioid ligand, not Substance P; correction documented in AUDITORIA_INTEGRIDAD_PROXY.md).
042: 
043: **UKB Causal Gene Set.** Genes encoding proteins with MR-supported causal relevance for chronic pain / chronic widespread pain in UKB Olink proteomics, measured in GSE221921: *CA14* (top-ranking causal for CWP, MR + colocalization; Chen et al., 2025) and the immune-signaling genes *TNFRSF1B*, *CD74*, *COL18A1*, *BTN2A1*, *TNFRSF4*, *CD302*, *TNFRSF9* (MR-validated in the multisite chronic pain analysis; Li ZY et al., 2025). *LEP* and *TNF* are not measurable in GSE221921. Note: in the published Chen et al. (2025) analysis, 18 proteins have MR causal relevance for CWP (CA14, COL9A1, CRELD1, DPEP1, LEG1, LGALS3, MLN, PRSS53, TNF, BPIFB2, CTSO, DDR1, FAM171B, IFI30, LRRC37A2, PTN, SFTPD, ST3GAL1); CA14 is the top-ranking one and is **downregulated in plasma** in the cross-sectional analysis, with MR indicating a protective effect of genetically elevated CA14.
044: 
045: **Mast Cell / Basophil Panel (negative control).** Four genes (*CPA3*, *MS4A2*, *FCER1A*, *HDC*) previously identified as differentially expressed in FM whole blood (Jones et al., 2016). These are primarily expressed by basophils and mast cells, which are depleted during PBMC isolation.
046: 
047: *NPY* was included in the pre-specified gene set but was absent from the GSE221921 expression matrix. FDR correction was therefore applied to 16 measured genes (12 GWAS neural + 4 mast cell) in the primary GWAS-neural analysis; the expanded panel of 19 genes used for the opioid/tachykinin and UKB-causal analyses was corrected with Bonferroni ×19 or ×9 as specified in §2.3.
048: 
049: ### 2.2 Transcriptomic Datasets
050: 
051: **GSE221921 (PBMCs, RNA-seq).** FPKM-normalized expression values from peripheral blood mononuclear cells of 96 FM patients and 93 healthy controls (Mohapatra et al., 2024; PMID 38366049). Sample metadata and expression matrices were obtained from the GEO supplementary file `GSE221921_FM_ProcessedData.xlsx`.
052: 
053: **Critical note on sex distribution:** The GSE221921 cohort has a severe sex imbalance — FM group: 91 female / 5 male; HC group: 41 female / 52 male. This confounds any unadjusted FM vs. HC comparison, as a portion of the observed signal may reflect sex differences rather than disease effects. We address this through multiple sensitivity analyses (§2.4).
054: 
055: **GSE67311 (Whole blood, microarray).** Affymetrix Human Gene 1.1 ST array expression data from whole blood (PAXgene tubes) of FM patients and healthy controls (Jones et al., 2016; PMID 27157394). **Metadata verification (2026-08-03): the GEO sample metadata contains 67 FM / 75 HC (142 total), which differs from the 70/70 reported in the original paper.** Pre-computed differential expression results (log₂FC, p-value, FDR-adjusted p-value) were used, with the verified group counts.
056: 
057: ### 2.3 Statistical Analysis
058: 
059: All p-values from the 16 measured genes in the GWAS-neural analysis were jointly corrected using the Benjamini-Hochberg (BH) procedure (Benjamini & Hochberg, 1995) at α = 0.05. Genes were considered significant at q < 0.05.
060: 
061: For the expanded panel of 19 genes (validate_fm_biomarkers_iter2.py, v3 post-adversarial-audit), expression values are heavy-tailed and non-normal (Shapiro-Wilk rejects normality for all genes, both groups), so **Mann-Whitney U tests** were used as the primary inference, with **Bonferroni correction across the 19-gene panel** (N_GENES_PANEL = 19), and **Cohen's d** (pooled SD) reported as the effect size. T-tests are retained only as reference. Classification: proxy significant if p_Bonf < 0.05; effect size graded small (d < 0.3), small–medium (0.3 ≤ d < 0.5), medium (0.5 ≤ d < 0.8).
062: 
063: For the UKB-causal gene analysis (9 measurable genes in GSE221921), Bonferroni correction ×9 was applied to the Mann-Whitney p-values.
064: 
065: For the opioid/tachykinin axis, Mann-Whitney U p-values are reported; the four core genes (TACR1, OPRM1, TAC1, OPRK1) survive conservative Bonferroni correction across the 21-gene union panel (19 + TACR1 + OPRK1; e.g., TACR1 p = 0.0010 × 21 = 0.021; OPRK1 p = 0.0017 × 21 = 0.036). Spearman rank correlation was used for co-expression analysis across all 189 samples.
066: 
067: ### 2.4 Sensitivity Analyses for GSE221921
068: 
069: Given the sex imbalance, we applied five analytical models to each gene:
070: 
071: 1. **Welch t-test on raw FPKM** (original analysis)
072: 2. **Welch t-test on log₂(FPKM+1)** (variance-stabilizing transform)
073: 3. **Mann-Whitney U test** (non-parametric, distribution-free)
074: 4. **OLS regression: log₂(FPKM+1) ~ case + sex** (sex as covariate, full cohort)
075: 5. **Female-only subgroup: Welch t-test on log₂(FPKM+1)** (91 FM vs. 41 HC, eliminates sex confound entirely)
076: 
077: Each model produced p-values that were independently FDR-corrected across all 16 genes. Genes were classified by robustness: "Robust" (q < 0.05 in all 5 models), "Supported" (q < 0.05 in 3–4 models), "Model-sensitive" (q < 0.05 in 1–2 models), or "Not significant."
078: 
079: ### 2.5 Targeted Literature Review
080: 
081: We searched PubMed (terms: "pramipexole fibromyalgia," "ropinirole fibromyalgia," "dopamine agonist fibromyalgia"), ClinicalTrials.gov, and the GSK Study Register for clinical trials of dopamine D2/D3 agonists in FM; and PubMed/EuropePMC for CA14, sulthiame, and UKB Olink chronic pain proteomics (Li ZY et al., 2025; Chen et al., 2025). Search date: August 2026. This is a targeted narrative review, not a formal systematic review; no PRISMA protocol was registered.
082: 
083: ### 2.6 Limitations of the Analytical Approach
084: 
085: We acknowledge that the use of FPKM values with parametric tests is a simplified approach. The gold standard for RNA-seq differential expression is count-based modeling (DESeq2/edgeR/limma-voom; Love et al., 2014). Only FPKM values were available in the GEO supplementary materials; raw counts were not accessible. All analyses were performed in Python 3.10 using pandas 1.5, scipy 1.10, and statsmodels 0.13. The primary inference therefore uses non-parametric Mann-Whitney U with Bonferroni correction (§2.3), which is robust to the FPKM distribution.
086: 
087: ---
088: 
089: ## 3. Results
090: 
091: ### 3.1 MDGA2 and DRD2 Are Robustly Upregulated in FM PBMCs
092: 
093: Table 1 presents the sensitivity analysis for all 16 measured genes. Two genes — *MDGA2* and *DRD2* — were significant (q < 0.05) across all five analytical models and are classified as **Robust**:
094: 
095: **Table 1. Sensitivity analysis: q-values (FDR-corrected) across five analytical models.**
096: 
097: | Gene | Category | FM mean | HC mean | Welch FPKM | Welch log₂ | Mann-Whitney | OLS sex-adj | Female-only | Robustness |
098: |------|----------|--------:|--------:|-----------:|-----------:|-------------:|------------:|------------:|------------|
099: | *MDGA2* | GWAS Neural | 2.582 | 1.069 | **1.1×10⁻⁷** | **1.0×10⁻⁸** | **1.1×10⁻⁷** | **6.3×10⁻⁶** | **5.5×10⁻⁶** | **Robust (5/5)** |
100: | *DRD2* | GWAS Neural | 0.721 | 0.271 | **2.9×10⁻⁵** | **2.6×10⁻⁶** | **1.6×10⁻⁶** | **4.7×10⁻⁴** | **3.6×10⁻⁵** | **Robust (5/5)** |
101: | *CAMKV* | GWAS Neural | 0.656 | 0.288 | **3.2×10⁻³** | **1.6×10⁻³** | **8.3×10⁻³** | 0.112 | **0.032** | Supported (4/5) |
102: | *CELF4* | GWAS Neural | 1.341 | 0.848 | **0.046** | **0.013** | **0.010** | 0.167 | **0.032** | Supported (4/5) |
103: | *HTT* | GWAS Neural | 20.60 | 25.17 | 0.120 | **7.5×10⁻³** | **4.6×10⁻³** | 0.177 | **0.042** | Supported (3/5) |
104: | *NCAM1* | GWAS Neural | 4.375 | 3.234 | 0.087 | **0.021** | **0.010** | 0.186 | 0.114 | Model-sensitive (2/5) |
105: | *DCC* | GWAS Neural | 2.747 | 1.905 | 0.087 | **0.023** | **0.016** | 0.167 | 0.055 | Model-sensitive (2/5) |
106: | *SRD5A2* | GWAS Neural | 0.187 | 0.139 | 0.251 | 0.145 | 0.092 | 0.167 | **0.042** | Model-sensitive (1/5) |
107: | *GPR52* | GWAS Neural | 2.723 | 3.792 | 0.099 | 0.367 | 0.590 | 0.955 | 0.817 | NS |
108: | *NPC1* | GWAS Neural | 13.01 | 14.49 | 0.546 | 0.108 | 0.083 | 0.335 | 0.268 | NS |
109: | *KYNU* | GWAS Neural | 3.401 | 3.987 | 0.490 | 0.180 | 0.139 | 0.564 | 0.544 | NS |
110: | *PPP2R2B* | GWAS Neural | 2.445 | 2.587 | 0.883 | 0.825 | 0.581 | 0.955 | 0.817 | NS |
111: | *HDC* | Mast Cell | 5.274 | 7.991 | 0.666 | 0.103 | 0.094 | 0.462 | 0.732 | NS |
112: | *FCER1A* | Mast Cell | 3.899 | 4.448 | 0.748 | 0.784 | 0.578 | 0.321 | 0.496 | NS |
113: | *MS4A2* | Mast Cell | 0.719 | 0.788 | 0.926 | 0.076 | **2.9×10⁻³** | 0.321 | 0.325 | Model-sensitive (1/5) |
114: | *CPA3* | Mast Cell | 1.583 | 1.587 | 0.992 | 0.825 | 0.755 | 0.858 | 0.979 | NS |
115: 
116: *Notes: Bold indicates q < 0.05. NPY was pre-specified but absent from the expression matrix. FDR correction applied to 16 measured genes per model. Female-only analysis: 91 FM / 41 HC.*
117: 
118: **Key observations:**
119: - *MDGA2* and *DRD2* survive all five models including sex-adjusted OLS, suggesting that their signal is not solely explained by the severe sex imbalance in the cohort.
120: - *CAMKV* and *CELF4* survive four models (including female-only) but not the sex-adjusted OLS on the full cohort (q = 0.112 and 0.167, respectively). Their signals are supportive but model-sensitive. **Crucially, the OLS model ($\log_2(FPKM+1) \sim case + sex$) suffers from severe multicollinearity because fibromyalgia cases and female sex are highly collinear (95% of cases are female while controls are evenly split). This collinearity dramatically inflates the standard errors of the coefficients, leading to a profound loss of statistical power for case status. The female-only subgroup analysis (91 FM vs. 41 HC) completely removes the sex variable, thus eliminating this multicollinearity confound and rescuing the significance of both *CAMKV* and *CELF4* ($q = 0.032$). This highlights the female-only subgroup as the primary, statistically unconfounded model.**
121: - *HTT* — the gene with the strongest GWAS coding variant — shows a supported signal (3/5 models), which was not apparent in the original FPKM-only analysis. However, we note that the direction of effect is negative (downregulated in FM PBMCs), contrasting with the upregulation seen in *MDGA2* and *DRD2*.
122: - No mast cell marker shows a robust PBMC signal; *MS4A2* reaches significance only in the Mann-Whitney model and is therefore classified as model-sensitive rather than replicated across analytical frameworks.
123: 
124: ### 3.2 The Opioid/Tachykinin Neuropeptide Axis Is Coordinately Activated in FM PBMCs
125: 
126: Extending the panel to the neuropeptide axis (validate_fm_biomarkers_iter2.py v3 + session analysis), we find that **ligands and receptors of both the tachykinin (Substance P) and endogenous opioid systems are simultaneously upregulated** in FM PBMCs (Table 2). This is the largest effect-size block observed in the entire investigation.
127: 
128: **Table 2. Opioid/tachykinin axis in GSE221921 (96 FM vs 93 HC PBMCs).**
129: 
130: | Gene | Role | FC (FM/HC) | MWU p | Bonf (×21) | Cohen's d | Classification |
131: |------|------|-----------:|-------:|-----------:|----------:|----------------|
132: | **TACR1** | NK1 receptor (Substance P) | **2.73** | **0.0010** | 0.021 | **+0.60** | **significant, medium effect** |
133: | **OPRM1** | μ-opioid receptor | **2.28** | **<0.0001** | <0.0021 | **+0.53** | **significant, medium effect** |
134: | **TAC1** | Substance P (ligand) | **2.10** | **0.0002** | 0.0042 | **+0.47** | **significant, small–medium** |
135: | **OPRK1** | κ-opioid receptor | **1.78** | **0.0017** | 0.036 | **+0.38** | **significant, small–medium** |
136: | PENK | Enkephalins (ligand) | 1.38 | 0.0031 | 0.065 (marginal) | +0.21 | trend (Bonf ×19 = 0.060) |
137: | OPRD1 | δ-opioid receptor | 1.23 | 0.0199 | NS | +0.10 | trend |
138: | PNOC | Nociceptin | 0.96 | NS | — | −0.02 | flat |
139: | POMC | β-endorphin/ACTH | 1.04 | NS | — | +0.03 | flat |
140: 
141: *Bonf ×21 = conservative correction across the 21-gene union panel (19 + TACR1 + OPRK1). PENK is marginal under Bonf ×19 (p = 0.060) and does not survive ×21.*
142: 
143: **Co-expression of the axis (Spearman, all 189 samples):**
144: 
145: | Pair | rho | p |
146: |------|----:|---:|
147: | OPRM1 ↔ TAC1 | +0.632 | <0.0001 |
148: | PENK ↔ OPRM1 | +0.442 | <0.0001 |
149: | PENK ↔ TAC1 | +0.408 | <0.0001 |
150: | TAC1 ↔ TACR1 | +0.382 | <0.0001 |
151: | PENK ↔ POMC | +0.312 | <0.0001 |
152: 
153: **Interpretation.** This is not a single elevated gene but a **coordinated circuit**: ligands (*TAC1*, *PENK*) and their cognate receptors (*TACR1*, *OPRM1*, *OPRK1*) are co-upregulated and positively co-expressed. The strongest hit, *TACR1* (NK1 receptor for Substance P; d = +0.60), is the first receptor in this investigation to exceed its ligand in effect size — the receptor is where the signal is amplified, pointing to sensitization of the SP→NK1 circuit consistent with nociplastic pain mechanisms. Elevated *OPRM1*/*OPRK1* suggest a compensatory activation of the endogenous opioid system in the periphery; this does not contradict low-opioid findings in CSF, a distinct compartment. The activated TAC1→TACR1 axis is consistent with pro-inflammatory cytokine involvement in FM reviewed by Rodríguez-Pintó et al. (2014), though a direct mechanistic link between Substance P and IL-8 via mast cell/neutrophil trafficking is not specifically established in that review and remains hypothetical.
154: 
155: ### 3.3 Cross-Context Comparison: GSE67311 (Whole Blood)
156: 
157: To assess whether these signals are detectable in a different cell fraction, we examined the same gene sets in GSE67311 (whole blood, Affymetrix microarray; Table 3).
158: 
159: **Table 3. Cross-context comparison: GSE221921 (PBMCs) vs. GSE67311 (whole blood).**
160: 
161: | Gene | Category | GSE221921 (PBMCs) | GSE67311 (whole blood) | Replicates? |
162: |------|----------|:------------------:|:----------------------:|:-----------:|
163: | *CPA3* | Mast Cell | NS | **1.8×10⁻⁶** | Whole blood only |
164: | *MS4A2* | Mast Cell | Model-sensitive | **1.5×10⁻⁵** | Whole blood only |
165: | *FCER1A* | Mast Cell | NS | **1.7×10⁻⁵** | Whole blood only |
166: | *HDC* | Mast Cell | NS | **4.4×10⁻⁵** | Whole blood only |
167: | *TAC1* | Tachykinin ligand | FC=2.10, p=0.0002 | FC=1.004, p=0.495 | ❌ NO |
168: | *OPRM1* | Opioid receptor | FC=2.28, p<0.0001 | FC=1.020, p=0.160 | ❌ NO |
169: | *IL6* | Inflammatory | FC=1.66, p=0.0002 | FC=1.023, p=0.524 | ❌ NO |
170: | *PENK* | Opioid ligand | FC=1.38, p=0.0031 | FC=1.038, p=0.031, Bonf=0.248 | ⚠️ trend only |
171: | *PCSK1N* | Prohormone convertase | FC=0.76 (↓) | FC=1.041 (↑), p=0.045 | ❌ INVERTED |
172: | *MDGA2* | GWAS Neural | Robust (5/5) | 0.99 | PBMCs only |
173: | *DRD2* | GWAS Neural | Robust (5/5) | 0.42 | PBMCs only |
174: 
175: No gene was significant in both datasets. The PBMC-derived neuropeptide and GWAS-neural signals do not replicate in whole blood; the mast cell/basophil panel is detectable only in whole blood. **Deconvolution analysis (2026-08-03)** — using cell-type marker averages for neutrophils, T cells, B cells, monocytes, and NK cells in GSE67311 — shows **essentially identical cellular composition between FM and HC** (neutrophil score: FM = 10.92 vs HC = 10.89, 7 markers; lymphocytes/monocytes/NK all within 0.1), and weak/mixed correlation of the neutrophil score with the PBMC proxies (TAC1 r = +0.07 NS; OPRM1 r = −0.22, p = 0.008; PENK r = −0.13 NS). **The non-replication is therefore NOT explained by neutrophil-driven dilution of the whole-blood signal.** Remaining explanations are platform differences (RNA-seq FPKM vs. microarray RMA), cohort heterogeneity, small true effects (d ≈ 0.2–0.5) that do not survive inter-platform noise, or partial cohort-specificity of the GSE221921 findings.
176: 
177: **Opioid axis extension (2026-08-03, `scripts/validate_opioid_axis_gse67311.py`).** The prior analysis covered TAC1/OPRM1/IL6 only. We extended it to the full opioid/tachykinin receptor set (TACR1, OPRM1, OPRK1) plus TAC1 and PENK (Mann-Whitney + Bonferroni ×5 + Cohen's d). **Absolute expression does not replicate** (TACR1 FC = 1.008, p = 0.480; OPRM1 FC = 1.020, p = 0.160; OPRK1 FC = 1.021, p = 0.878; TAC1 FC = 1.004, p = 0.495; PENK FC = 1.038, p = 0.031, Bonf = 0.155 — none survives).
178: 
179: **Co-expression architecture (Spearman, all 10 pairs, FM-pooled vs HC-pooled):**
180: 
181: | Pair | ρ_FM | p_FM | ρ_HC | p_HC | FM > HC? | Pre-registered? |
182: |------|-----:|-----:|-----:|-----:|:--------:|:---------------:|
183: | TACR1–OPRK1 | +0.736 | <0.001 | +0.405 | <0.001 | ✓ | yes |
184: | OPRM1–OPRK1 | +0.530 | <0.001 | +0.279 | 0.015 | ✓ | yes |
185: | TACR1–OPRM1 | +0.420 | <0.001 | +0.280 | 0.015 | ✓ | yes |
186: | OPRM1–TAC1 | +0.363 | 0.003 | +0.078 | 0.504 | ✓ | yes |
187: | OPRK1–PENK | +0.375 | 0.002 | +0.150 | 0.200 | ✓ | yes |
188: | TACR1–TAC1 | +0.189 | 0.125 | +0.420 | <0.001 | **✗ HC > FM** | **no — omitted** |
189: | OPRK1–TAC1 | +0.259 | 0.034 | +0.370 | 0.001 | **✗ HC > FM** | **no — omitted** |
190: | TACR1–PENK | +0.257 | 0.036 | +0.029 | 0.806 | ✓ | **no — omitted** |
191: | OPRM1–PENK | +0.200 | 0.104 | +0.201 | 0.084 | ≈ | **no — omitted** |
192: | TAC1–PENK | −0.003 | 0.982 | +0.076 | 0.518 | ≈ | **no — omitted** |
193: 
194: **Correction note (2026-08-04).** A prior version of this section reported only 5 of 10 co-expression pairs, selected by direction (FM > HC). The 5 omitted pairs include 2 where HC actually exceeds FM (TACR1–TAC1, OPRK1–TAC1), which contradicts the earlier statement "HC pairs consistently weaker or non-significant." That statement is corrected here: **HC co-expression is weaker for 5 of 10 pairs, but comparable or stronger for 3, and near-null for 2.** The 5 originally reported pairs are those where the FM co-expression exceeds HC; reporting them without the full 10-pair table constituted selective reporting. A formal Fisher r-to-z test of the FM-vs-HC difference for each pair should accompany any inferential claim. The circuit-level interpretation (transcriptional coherence of the opioid/tachykinin axis in FM) rests on the 5 pairs where FM > HC, but is not a universal property of the 10-pair matrix.
195: 
196: **Interpretation:** the opioid/tachykinin circuit shows _some_ transcriptional coherence in FM whole blood, but **only 1 of 10 pairs differs significantly between FM and HC** (TACR1–OPRK1, Fisher r-to-z p = 0.003). The remaining 9 pairs do not distinguish the groups. The interpretation of a "coherent transcriptional module" is **not supported by the data** as a universal property: 2 pairs reverse (HC > FM), and the rest include near-null values. Its absolute amplitude is compartment-dependent (PBMC-specific). Plasma protein measurement (Olink/ELISA), not whole-blood transcriptomics, remains the decisive validation compartment. **Technical caveat:** in whole blood (GSE67311) TAC1 sits at the 8th intensity percentile, OPRK1 at p13, and OPRM1 at p19 of the microarray distribution (vs ACTB at p99). Correlations among probes in the bottom decile can reflect shared background noise rather than genuine co-regulation — the significant pair should be interpreted with this limitation.
197: 
198: **Honest assessment.** These PBMC-derived proxies are **PBMC/RNA-seq-specific** and are **not replicated in whole blood**. They should be described as "PBMC-specific transcriptional signatures," not as validated peripheral blood biomarkers. The planned plasma Olink/ELISA validation (§7) measures the relevant compartment (plasma protein) and is the definitive test; the whole-blood non-replication qualifies but does not invalidate the plasma hypothesis.
199: 
200: ### 3.4 UK Biobank Causal Proteomics: CA14 mRNA Elevated in PBMCs (Plasma ↓), Immune-Signaling Genes Downregulated in FM PBMCs
201: 
202: To connect population-scale causal proteomics with our transcriptomic data, we tested the UKB causal genes (Li ZY et al., 2025; Chen et al., 2025) in GSE221921. Eight of the causal genes are measurable in the matrix (LEP and TNF absent).
203: 
204: **Table 4. UKB causal genes for chronic pain / CWP in FM PBMCs (GSE221921).**
205: 
206: | Gene | UKB source | FC (FM/HC) | MWU p | Bonf ×9 | Cohen's d | Direction |
207: |------|-----------|-----------:|-------:|--------:|----------:|-----------|
208: | **CA14** | MR+coloc causal CWP (top-ranking) | **2.29** | **0.0003** | **0.0027** | **+0.41** | **↑↑ significant** |
209: | TNFRSF1B | MR causal chronic pain — **back-specific** (Li ZY 2025) | 0.541 | <0.0001 | <0.0001 | −0.56 | ↓↓ significant |
210: | CD74 | MR causal chronic pain — **hip-specific** (Li ZY 2025) | 0.579 | <0.0001 | <0.0001 | −0.44 | ↓↓ significant |
211: | COL18A1 | MR causal chronic pain — **abdominal-specific** (Li ZY 2025) | 0.581 | 0.0001 | 0.0005 | −0.54 | ↓↓ significant |
212: | BTN2A1 | MR causal chronic pain — **knee/abdominal-specific** (Li ZY 2025) | 0.745 | 0.0025 | 0.023 | −0.35 | ↓ significant |
213: | TNFRSF4 | MR causal chronic pain — **knee-specific** (Li ZY 2025) | 0.768 | 0.0004 | 0.0036 | −0.23 | ↓ significant |
214: | CD302 | MR causal chronic pain | 0.717 | 0.154 | NS | −0.19 | ↓ trend |
215: | TNFRSF9 | MR causal chronic pain | 1.459 | 0.805 | NS | +0.27 | ~flat |
216: 
217: **CA14: causal in plasma (downregulated), elevated in PBMC mRNA (unadjusted) — a direction-sensitive triangle with a sex-confound caveat.** CA14 is the **top-ranking causal protein for chronic widespread pain** (MR + colocalization PP.H4 > 0.5; Chen et al., 2025) and the **only UKB causal gene that is upregulated in FM PBMC mRNA in the unadjusted analysis** (FC = 2.29, p = 0.0003, d = +0.41). **Sex confound caveat (2026-08-04):** the female-only primary model yields p = 0.135, d = +0.24, FC = 1.60 — the unadjusted signal does not survive sex stratification (see §4.2). Crucially, the **published plasma direction is the opposite**: in the UKB cross-sectional analysis, CA14 is among the **ten most downregulated plasma proteins** in CWP, while MR indicates that **genetically elevated CA14 is protective** (discordant observational vs. MR direction; Chen et al., 2025). The authors therefore propose **CA14 agonists, rather than the inhibitor sulthiame (CHEMBL328560)**, as the more promising therapeutic direction, given non-linear CA14–pain associations. Interpretation: low plasma CA14 may contribute causally to pain (consistent with pH/nociception dysregulation); the PBMC mRNA elevation we observe may be compensatory or compartment-specific. This makes CA14 the strongest cross-level candidate in the investigation — but with a **testable, direction-specific prediction: CA14 should be ↓ in FM plasma** in the Olink validation, and the repurposing direction is agonism, not sulthiame inhibition.
218: 
219: **Five of nine UKB causal genes are significantly DOWNREGULATED in FM PBMCs** (TNFRSF1B, CD74, COL18A1, BTN2A1, TNFRSF4; FC 0.54–0.77). These genes encode TNF receptors and immune signaling molecules. **Important caveat:** these MR hits are **site-specific** (back, hip, abdominal, knee) in Li ZY 2025 — not CWP/FM-specific — and none of the five is among the 18 causal CWP proteins identified in Chen 2025. The plasma direction of these five proteins in FM is not known (the UKB cross-sectional analysis reported by Chen 2025 does not cover them specifically). The coordinated downregulation in PBMC mRNA is therefore consistent with — but not proof of — an **immunomodulatory/exhaustion hypothesis** (reduced TNF-family and immune signaling), which remains explicitly speculative pending plasma measurement.
220: 
221: ### 3.4.5 COL9A1–PTN: The Bonferroni-Surviving Extracellular-Matrix / Neurite-Outgrowth Module
222: 
223: Having established that CA14 does not survive sex stratification (§4.2), we asked which genes from the chronic-widespread-pain causal set (Chen 2025) represent the most robust transcriptomic signal in FM PBMCs. Testing the 18 CWP causal proteins in GSE221921 under the five-model framework (E2), **only two genes survive Bonferroni correction on the sex-adjusted model**: *COL9A1* (FC = 2.32, d = +0.88, p_adj_Bonf = 8.5×10⁻⁵) and *PTN* (FC = 2.91, d = +0.61, p_adj_Bonf = 0.020). *BPIFB2* is nominally significant (p_adj = 0.0035) but does not survive Bonferroni (p_adj_Bonf = 0.063); *ST3GAL1* is downregulated (FC = 0.765) and anticorrelated with the pair (r = −0.23). No gene passes all 5 models (all fail male-only); the corrected description is "Robust 4/5" for COL9A1/PTN, not 5/5.
224: 
225: **Co-expression (C1).** COL9A1, BPIFB2 and PTN form a positively co-expressed triad (r = 0.25–0.51, all p < 0.001); ST3GAL1 anticorrelates weakly (r = −0.15 to −0.24). Fisher r-to-z shows the correlations do **not** differ between FM and HC (p > 0.17 for all pairs) — the module is a structural property of the co-expression network, not a disease-specific rewiring.
226: 
227: **Biological function (C3).** The triad resolves into two convergent axes rather than a single module: (i) a **structural/neural axis** — *COL9A1* (collagen alpha-1(IX), minor fibrillar cartilage collagen; mutations cause multiple epiphyseal dysplasia and osteoarthritis, a direct joint-pain link) co-expressed with *PTN* (pleiotrophin, secreted growth factor driving neurite outgrowth and nerve repair); (ii) an **innate-immunity axis** — *BPIFB2* (LPS-binding lipid transfer, Sjögren biomarker) with *ST3GAL1* (T-cell sialylation, BDNF sialylation). The COL9A1–PTN axis is the stronger and more novel: both are secreted and detectable in plasma Olink, and both connect to pain through anatomically distinct but clinically central routes (joint integrity and nociceptive nerve plasticity).
228: 
229: **Power analysis for plasma validation (C4).** Anchoring the planned Olink cohort to the observed mRNA effect (d = 0.88, FC = 2.32 for COL9A1) and modeling mRNA→protein attenuation at four scenarios (r = 0.8 / 0.6 / 0.4 / 0.3), the required sample size for 80% power is: 33/group (optimistic), 56/group (moderate), 129/group (conservative), 233/group (pessimistic). A cohort of **75 FM + 75 HC** covers the moderate scenario with 88% power and is the recommended design.
230: 
231: **Interpretation.** COL9A1 and PTN replace CA14 as the **primary plasma-validation candidates** from the UKB causal set: they are Bonferroni-surviving, sex-adjusted-robust, plasma-detectable, and biologically linked to pain through joint and neural mechanisms. CA14 is retained as a direction-specific **reference** candidate (expecting ↓ in FM plasma, per Chen 2025), not as the lead target.
232: 
233: ### 3.5 Targeted Literature Review: Dopamine Agonists in FM
234: 
235: Our literature search identified three clinical studies and one preclinical study (Table 5):
236: 
237: **Table 5. Dopamine agonist studies in fibromyalgia.**
238: 
239: | Study | Drug | Type | N | Result | Key Finding | Risk of Bias |
240: |-------|------|------|---|--------|-------------|--------------|
241: | Holman & Myers, 2005 (PMID 16052595) | Pramipexole | RCT (DB-PC) | 60 | **Positive** | 36% pain ↓ vs 9% placebo; 42% achieved ≥50% pain decrease | High: single-center, author held patents on D2/D3 use in FM |
242: | Holman, 2003 (ACR conference) | Ropinirole | Pilot | 30 | NS (p=0.31) | Underpowered. Not published in peer-reviewed journal. | Very high: unpublished, tiny N |
243: | GSK NCT00256893 | Ropinirole CR | Phase II RCT | 160 | **Negative** | Failed primary endpoints | Moderate: sponsor-reported, results not published in peer-reviewed journal |
244: 
245: ### 3.6 GSE269047 — excluded
246: 
247: GSE269047 was evaluated as a replication cohort but was found to contain primarily HERV (human endogenous retrovirus) transcripts, not annotated gene expression; none of our target genes are measurable on that platform. The accession suffixes (`opti`/`bgrd`/`rand`) are probe design categories, not gene symbols, and the cohort is a mixed FM/ME-CFS sample. The dataset is therefore **not usable as a proxy-validation dataset** and we draw no conclusions from it (`GSE269047_NO_UTILIZABLE.md`).
248: 
249: ---
250: 
251: ## 4. Discussion
252: 
253: ### 4.1 The Peripheral Signature of FM Is Neuropeptide/Nociceptive and Immunomodulatory, Not Classically Inflammatory
254: 
255: The central finding of this study is that the peripheral transcriptomic signature of FM — as measured in PBMCs (GSE221921) — is dominated by three non-inflammatory axes:
256: 
257: 1. **A complete opioid/tachykinin neuropeptide circuit is activated** (TACR1, OPRM1, TAC1, OPRK1; d = +0.38 to +0.60, co-expressed rho 0.31–0.63). This is the largest effect-size block in the investigation and the most robust finding: it survives all five sensitivity models including sex-stratified analysis (§3.2).
258: 2. **An extracellular-matrix / neurite-outgrowth module — *COL9A1* (FC = 2.32, d = +0.88) and *PTN* (FC = 2.91, d = +0.61) — is the only signal from the CWP causal set that survives Bonferroni correction on the sex-adjusted model** (§3.4.5). Both are secreted and plasma-detectable (Olink), and connect to pain through joint integrity (COL9A1, osteoarthritis link) and nociceptive nerve plasticity (PTN, neurite outgrowth). This is the primary plasma-validation target of the investigation.
259: 3. **CA14 — the top UKB causal protein for chronic widespread pain — is elevated in PBMC mRNA in the unadjusted analysis** (FC = 2.29) **but does not survive the female-only primary model** (p = 0.135, FC = 1.60; sex-confounded) **and is downregulated in plasma** in the UKB cross-sectional analysis, with MR indicating that genetically elevated CA14 is protective; five UKB causal immune-signaling genes are downregulated (TNFRSF1B, CD74, COL18A1, BTN2A1, TNFRSF4). CA14 is retained as a direction-specific reference candidate (expecting ↓ in FM plasma), not as the lead target.
260: 
261: At the same time, the classical inflammatory axis (IL-6/IL-8) — the historical favorite in FM biomarker research — receives **no support at population scale**: IL-6 and IL-8/CXCL8 do not figure among the highlighted proteins in the largest published plasma proteomics screen of chronic pain (51,644 UKB participants, 2,923 proteins; Li ZY et al., 2025), though this is **weak evidence** — the 474 pain-associated proteins reside in supplementary tables that were not consulted, so absence from the narrative text does not constitute absence of association. **TAC1 (Substance P) is not covered by the Olink Explore panel and therefore cannot be evaluated with these data — its absence from the text is not informative.** In our own PBMC data, IL6 is significantly elevated (FC = 1.66, p = 0.0002) but with a **small effect size (d = +0.31)**, and CXCL8 is inverted in PBMCs (down relative to whole blood, consistent with cell-fraction biology).
262: 
263: The coherent narrative that emerges is **extracellular-matrix / neurite-outgrowth dysregulation (COL9A1–PTN) + neuropeptide nociceptive signaling + immunomodulation (UKB immune genes) + pH/nociception dysregulation (CA14)**, not systemic inflammation: reduced TNF-family signaling (5 UKB-causal genes ↓), activation of the nociceptive neuropeptide circuit (SP→NK1, opioid receptors), an extracellular-matrix/nerve-repair module (COL9A1–PTN), and a pH-regulating carbonic anhydrase (CA14) that is causal and **downregulated in plasma** (elevated in PBMC mRNA). This reframing has direct consequences for biomarker selection: the plasma validation panel should prioritize **COL9A1 and PTN** (Olink — primary targets, Bonferroni-surviving, plasma-detectable), with CA14 measured as a direction-specific reference (expecting ↓ in FM plasma) and Substance P/enkephalins (ELISA) as secondary neuropeptide measures; IL-8 is retained only as a technical assay control.
264: 
265: ### 4.2 CA14: A Cross-Level Causal Candidate — Downregulated in Plasma, Druggable by Agonism
266: 
267: CA14 emerges as the most actionable candidate in this investigation, with a direction-sensitive evidence stack:
268: 
269: | Layer | Evidence | Source |
270: |-------|----------|--------|
271: | 1. Plasma protein | Causal in CWP (top-ranking, MR + colocalization PP.H4 > 0.5); **downregulated (↓) cross-sectionally**; MR protective for genetically elevated CA14 | Chen et al. 2025, *Adv Sci* (PMID 41025730), 29,254 participants |
272: | 2. PBMC mRNA (unadjusted) | ↑ in FM (FC = 2.29, p = 0.0003, d = +0.41) | GSE221921 (this study, full cohort) |
273: | 2b. PBMC mRNA (female-only) | **Does not survive** (p = 0.135, d = +0.24, FC = 1.60) | GSE221921, female-only subgroup (91 FM / 41 HC) |
274: | 3. Pharmacology | Sulthiame (CHEMBL328560) is an **inhibitor**; **the paper proposes CA14 agonists — not inhibitors — as the more promising therapeutic direction** | Chen et al. 2025; ChEMBL |
275: 
276: **Sex confound correction (2026-08-04).** The unadjusted CA14 signal (FC = 2.29, p = 0.0003) does not survive the sex-stratified sensitivity analysis that §2.4 defines as the "primary, statistically unconfounded model" — the female-only subgroup (91 FM / 41 HC) yields p = 0.135, d = +0.24, FC = 1.60. Diagnostic: within healthy controls, CA14 expression in females is 2.41× that of males (mean F = 0.901, mean M = 0.374, p = 0.034), and the FM cohort is 95% female while the HC cohort is 55% male. The unadjusted FC = 2.29 is therefore confounded by the structural sex imbalance — it is of the same magnitude as the pure sex effect (F/M ratio = 2.41). **CA14 should be reported as "sex-confounded, not surviving the primary model" in the PBMC mRNA layer.** The plasma protein layer (Layer 1, Chen et al. 2025) is unaffected by this confound because the UKB analysis was sex-adjusted. The testable prediction (↓ CA14 in FM plasma) remains valid and is independent of the PBMC mRNA result.
277: 
278: CA14 encodes carbonic anhydrase XIV, a membrane-bound enzyme regulating extracellular pH; pH dysregulation in nociceptors is a well-established driver of pain signaling (acid-sensing). The published analysis shows CA14 among the ten most downregulated plasma proteins in CWP, while MR indicates a protective effect of genetically elevated CA14 — an observational-vs-MR discordance the authors interpret as state-dependent protein alteration vs. lifelong genetic predisposition. **Our testable prediction: CA14 should be ↓ in FM plasma** in the Olink validation; if confirmed, the repurposing direction is **agonism/activation of CA14**, not sulthiame inhibition. The elevated PBMC mRNA we observe may be compensatory or compartment-specific; both compartments should be measured to resolve this. **Mechanistic caveat (QSP, 2026-08-04, thermodynamically corrected):** a single-compartment QSP model of the CA14→pH→ASIC pathway, recalibrated so the uncatalyzed rates respect the thermodynamic Keq (K_UNCAT_R = K_UNCAT_F / Keq = 189.3 s⁻¹, correcting a 3.8× bug), shows ΔpH = 0 exactly — because at steady state the CA-catalyzed terms cancel identically (k_buf·h = J_co2 + J_acid − k_diff·c), so the enzyme changes the relaxation rate, not the equilibrium. The model's basal pH is set by J_co2/k_buf and does not reproduce the Henderson-Hasselbalch value of 7.33 across any parameter combination (it yields 7.83/7.21/6.76 depending on unmeasured fluxes), indicating the pH baseline is not properly calibrated. **The simple peripheral acidosis mechanism is therefore not evaluable with this model — a model that cannot exhibit the effect cannot refute it.** The earlier conclusion ("vía descartada") is retracted; the correct framing is "hipótesis no evaluable con este modelo de estado estacionario de compartimento único." The causal signal (MR/coloc from Chen 2025) remains statistically valid and may act via a different compartment (CNS), via transient pH kinetics, or reflect CA14 as a marker rather than mediator (see `scripts/qsp_ca14_ph_nociception.py`).
279: 
280: **Druggability caveat.** Sulthiame inhibits multiple carbonic anhydrases, not only CA14, and the published analysis explicitly favors agonists over inhibitors for pain; no well-documented CA14 activator is yet available. Any repurposing hypothesis requires isoform selectivity assessment and cannot be inferred from the present transcriptomic analysis alone.
281: 
282: ### 4.3 The GWAS-Transcriptomic Convergence on Neural Genes
283: 
284: The GWAS-prioritized neural genes *MDGA2* and *DRD2* show robust upregulation across multiple analytical models in FM PBMCs, including sex-adjusted and female-only sensitivity analyses. Two additional genes (*CAMKV*, *CELF4*) show supportive but sex-covariate-sensitive signals. This convergence of genetic risk (GWAS) and transcriptomic alteration (independent cohort) across independent methodologies is suggestive of biological relevance, though it remains an exploratory observation.
285: 
286: We emphasize that the GWAS network is not exclusively "dopaminergic." *MDGA2* encodes a GPI-anchored immunoglobulin superfamily member involved in synaptogenesis and neural circuit formation. *CAMKV* is a CaM kinase-like protein involved in dendritic spine dynamics. *CELF4* regulates neuronal mRNA metabolism. Only *DRD2* is strictly dopaminergic. The finding is therefore better characterized as convergence on a **neural/synaptic GWAS network** that includes, but is not limited to, dopaminergic signaling.
287: 
288: Our computational target profiling of MDGA2 (the most significant hit in our PBMC reanalysis, q = 1.1×10⁻⁷) using AlphaFold tridimensional models and clinical database mapping (Open Targets) provides additional mechanical insights. AlphaFold predicts a highly structured and ordered protein (Global pLDDT = 84.81), characterized by a large rigid 6-domain Ig-like supradomain separated by a flexible six-residue linker from the C-terminal MAM domain. This structural flexibility is crucial for modulating intercellular synaptogenesis. Furthermore, Open Targets database queries confirm that MDGA2 is highly constrained genetically (LoF score = 1.0, oe = 0.257), has direct clinical associations with chronic pain (Back Pain, score = 0.40), and is linked pharmacogenomically to the clinical outcomes of Milnacipran, an FDA-approved drug for Fibromyalgia. At the therapeutic level, its high-confidence extracellular GPI-anchored localization renders it highly tractable for antibody-based therapies or biologics targeting neuro-immune interactions.
289: 
290: ### 4.4 The DRD2 Signal: Interpretation and Caveats
291: 
292: The upregulation of *DRD2* (Log₂FC = +1.41, q = 2.9×10⁻⁵; robust across all 5 models) in PBMCs warrants careful interpretation:
293: 
294: 1. **Absolute expression is low** (FM mean = 0.72 FPKM, HC mean = 0.27 FPKM). While the fold change and statistical significance are robust, the biological impact of sub-FPKM expression differences requires validation by targeted methods. Scientifically, an expression level under 1 FPKM in bulk tissue can represent either low-level "transcriptional noise" (leakage) across the bulk population or highly concentrated, biologically relevant expression restricted to a tiny immune subpopulation (e.g., specific $CD4^+$ or $CD8^+$ T cell subsets). To resolve this, orthogonal validation using highly specific qRT-PCR primers or single-cell qPCR is mandatory before drawing definitive functional conclusions.
295: 
296: 2. **Cell composition confounding.** DRD2 is expressed in specific immune cells, such as T cell subsets, where it modulates cytokine production and chemotaxis (Pacheco et al., 2014). If FM patients have altered PBMC composition (e.g., different T cell subsets or monocyte proportions), the observed DRD2 increase could reflect more cells expressing DRD2 rather than per-cell upregulation. Without deconvolution analysis (CIBERSORTx, xCell, or similar), this cannot be distinguished.
297: 
298: 3. **Peripheral vs. central.** PBMCs are not the primary site of FM pathology. The GWAS heritability is enriched in brain tissues. Whether peripheral DRD2 expression mirrors central dopaminergic dysfunction is unknown.
299: 
300: 4. **Independence from Cell-Type Abundances.** To explore whether the observed upregulation of *DRD2* is an artifact of altered PBMC proportions, we computed cell-type signature enrichment scores. *DRD2* expression did not correlate strongly with any estimated cell fraction (r_max = 0.34 with Tregs, and <0.30 with other fractions). This suggests that the *DRD2* signal in FM PBMCs represents genuine transcriptional upregulation rather than a passive reflection of shifts in cellular composition, strengthening its biological validity.
301: 
302: ### 4.5 Cell-Fraction-Dependent Contrast and the Whole-Blood Non-Replication
303: 
304: The observation that mast cell markers are significant in whole blood but not PBMCs, while GWAS neural genes and the neuropeptide axis show the opposite pattern, is consistent with cell-fraction-dependent peripheral signatures. However, this observation cannot distinguish true cell-state changes from cell-composition differences, nor can it determine whether either signature is a disease driver versus a secondary biomarker.
305: 
306: The non-replication of the neuropeptide proxies in GSE67311 is a **scientific negative that we report without cosmetic correction** (VALIDACION_GSE67311_NEGATIVA.md). Deconvolution rules out the most plausible mechanical explanation (neutrophil dilution). The remaining interpretations — platform, cohort, or true small effects — cannot be resolved with existing data. Practically, this means: (1) the proxies are PBMC/RNA-seq-specific; (2) the plasma Olink/ELISA protocol is the decisive test, because it measures the compartment (plasma protein) relevant to the causal UKB findings; (3) PCSK1N, which inverts direction between datasets, is re-classified as "not confirmed" until the discrepancy is understood.
307: 
308: ### 4.6 Pharmacological Context: The 21-Year Gap and Druggability Barriers
309: 
310: The pharmacological evidence for dopamine agonists in FM is limited. The sole positive RCT (Holman & Myers, 2005) carries substantial risk of bias (single-center, n=60, author held patents). The negative ropinirole trial (GSK NCT00256893) has never been published in a peer-reviewed journal, limiting independent evaluation. The current evidence is insufficient to recommend dopamine agonists for FM but does provide a rationale for re-examining this pharmacological axis in molecularly stratified cohorts. **Crucially, the "21-year gap" of non-replication is not merely an omission of research interest, but a reflection of the severe clinical tolerability barriers inherent to D2/D3 agonists in chronic pain populations. These ergot and non-ergot agonists are associated with severe side effects, including mesolimbic D3-receptor-mediated Impulse Control Disorders (ICDs) (e.g., pathological gambling, compulsive buying, hypersexuality), Dopamine Agonist Withdrawal Syndrome (DAWS) (characterized by profound anxiety, panic attacks, depression, and pain exacerbation upon tapering), orthostatic hypotension, and sudden "sleep attacks." In a patient population already burdened by chronic fatigue, dysautonomia, and baseline sleep fragmentation, the therapeutic index for these compounds is extremely narrow, posing significant translation challenges.**
311: 
312: The structural basis of this pharmacological axis — molecular docking of DRD2 with pramipexole and ropinirole, biophysical DRD2/DRD3 pocket mapping, de novo candidate design, and in silico validation across the fibromyalgia-implicated GPCR targets *DRD2*, *TACR1*, and *OPRM1* — is reported separately in an accompanying computational chemistry manuscript (Muñoz Rojas, companion paper: *Computational Docking and De Novo Design Against Fibromyalgia-Implicated GPCR Targets*), so that the present transcriptomic reanalysis remains focused on its primary evidence base.
313: 
314: ### 4.7 Tissue-Invariant Germline Genomic sQTL Architecture of DRD2
315: 
316: Given the non-replication and high volatility of peripheral blood mRNA measurements across independent cohorts (§3.3; §3.6 dataset excluded as non-annotated HERV platform), we emphasize that the strongest, methodologically unconfounded evidence supporting the *DRD2* axis in Fibromyalgia resides in **germline DNA genetics** (Tangente 3).
317: 
318: Unlike blood mRNA expression levels — which fluctuate dynamically in response to cell-fraction shifts, acute physiological stress, and pharmacological therapies — germline genomic DNA variants are invariant across all tissues throughout an individual's lifespan. The index GWAS risk SNP **rs2734833** (Kerrebijn et al., 2025) resides in strict linkage disequilibrium ($D' = 1.0$) with functional splicing quantitative trait loci (sQTLs), specifically **rs1076560** and **rs2283265**.
319: 
320: GTEx v10 human brain tissue data (`ENSG00000149295.14`) demonstrate that baseline *DRD2* expression is highly concentrated in striatal structures (**Nucleus Accumbens: 54.21 TPM; Putamen: 46.80 TPM; Caudate: 41.40 TPM**), with moderate expression in Substantia Nigra (8.21 TPM) and low baseline levels ($\sim 0.66\text{--}1.22\text{ TPM}$) across cerebral cortex and cervical spinal cord. In these central tissues, germline sQTL variants directly modulate the alternative splicing of **Exon 6** (87 bp encoding 29 amino acids: `VVALSSQFPV SEAAEQARAE AQEAEEEVVG`), which is inserted into the third intracellular loop (IL3).
321: 
322: Exon 6 inclusion determines the functional ratio between two distinct receptor isoforms:
323: 1. **$DRD2_{\text{Short}}$ ($D2S$):** The presynaptic autoreceptor isoform (414 aa), which lacks Exon 6 and functions primarily to inhibit presynaptic dopamine synthesis and vesicular release via $G_{i\alpha2}$ coupling and Tyrosine Hydroxylase (TH) inhibition.
324: 2. **$DRD2_{\text{Long}}$ ($D2L$):** The postsynaptic signaling isoform (443 aa), which incorporates Exon 6 and mediates canonical postsynaptic dopaminergic neurotransmission via $G_{i\alpha1/3}$ and $\beta$-arrestin-2 / AKT-GSK3$\beta$ recruitment.
325: 
326: Disruption of Exon 6 alternative splicing in central striatal and nociceptive circuits provides a cell-type-independent, tissue-invariant genomic mechanism through which genetic variation at the *DRD2* locus alters central pain processing, descending pain inhibition, and mesolimbic reward signaling in Fibromyalgia. Future experimental work should focus on germline sQTL genotyping and brain-isoform-specific quantification rather than relying on peripheral blood mRNA expression.
327: 
328: ---
329: 
330: ## 5. Limitations
331: 
332: 1. **Sex confounding.** GSE221921 has a severe sex imbalance (FM: 91F/5M; HC: 41F/52M). Our sensitivity analyses suggest that *MDGA2* and *DRD2* are not solely explained by sex imbalance, while *CAMKV* and *CELF4* are sensitive to sex adjustment. Residual confounding remains possible, and future studies should use sex-balanced cohorts or sex-stratified designs.
333: 
334: 2. **Statistical methodology.** FPKM with parametric tests is not gold standard for RNA-seq. Count-based modeling (DESeq2/edgeR) would be preferable, but raw counts were not available. The expanded panel uses Mann-Whitney U + Bonferroni + Cohen's d (post-adversarial-audit standard), which is robust to the FPKM distribution.
335: 
336: 3. **Cell composition — opioid axis is compositional (2026-08-04).** A marker-based deconvolution (NNLS with LM22 signatures, 12 cell types) was applied to GSE221921, and each opioid-axis gene was regressed against group + sex + estimated cell fractions. **0 of 7 opioid-axis genes survive the adjustment** (OPRM1: p=0.0003→0.40, TACR1: p=0.0001→0.066, TAC1: p=0.002→0.62). The primary confounders are NK cells (OPRM1, PENK), Neutrophils (TACR1, POMC), T-regs (TAC1), and Monocytes (OPRK1). The elevated opioid-axis signal in FM PBMCs is **compositional** — explained by altered immune cell fractions, not transcriptional upregulation within a cell type. DRD2, by contrast, did not correlate strongly with any fraction (r_max=0.34 with Tregs) in the earlier exploratory analysis (§4.3), but this was not formally deconvoluted and requires re-evaluation with the same OLS framework. For GSE67311, marker-based deconvolution shows comparable composition between FM and HC, ruling out neutrophil dilution as the cause of non-replication.
337: 
338: 4. **Low absolute expression.** DRD2 expression in PBMCs is < 1 FPKM. qRT-PCR validation is needed.
339: 
340: 5. **Missing genes.** NPY was pre-specified but absent from the GSE221921 matrix (FDR applied to 16, not 17, genes). LEP and TNF were absent from the matrix and could not be tested in the UKB-causal analysis.
341: 
342: 6. **Whole-blood non-replication.** The PBMC-derived neuropeptide and GWAS-neural signatures do not replicate in GSE67311 (whole blood), and the mechanism is not explained by neutrophil dilution. The proxies are PBMC/RNA-seq-specific; plasma protein measurement (Olink/ELISA) is the decisive test. PCSK1N is re-classified as "not confirmed" due to direction inversion. **The absolute expression of the full opioid axis (TACR1/OPRM1/OPRK1/TAC1/PENK) also does not replicate; its co-expression architecture is partially preserved (5 of 10 pairs show FM > HC, rho up to +0.74, but 2 pairs reverse with HC > FM — see §3.3 full 10-pair table)** — suggesting a partially coherent, amplitude-compartment-dependent module.
343: 
344: 7. **mRNA ≠ protein.** Elevated mRNA for receptors (TACR1, OPRM1, OPRK1) does not guarantee elevated functional protein. For CA14, the published plasma direction (↓ in CWP) differs from our PBMC mRNA direction (↑), which we interpret as a compartment-specific or compensatory signal; both compartments should be measured. The plasma direction of the neuropeptides remains to be measured (BDNF/NGF precedent: neuropeptides elevated in CSF do not always translate to plasma; review PMC10341963).
345: 
346: 8. **Preprint/peer-review status.** Kerrebijn et al. (2025) is published on medRxiv (doi: 10.1101/2025.09.18.25335914, PMID 41001472) and has not yet completed full peer review. The UKB CWP proteomics study is now published (Chen et al., 2025, *Adv Sci*; PMID 41025730; DOI 10.1002/advs.202507691); the peer-reviewed version confirms CA14 causality and adds the direction and agonist information used here.
347: 
348: 9. **No experimental validation.** All analyses are computational. No wet-lab or clinical experiments were performed.
349: 
350: 9b. **No third PBMC dataset available (2026-08-04).** A systematic GEO search (18 FM series, 4 tissue queries) found only two FM datasets with peripheral blood mRNA transcriptomics: GSE221921 (PBMC RNA-seq, discovery) and GSE67311 (whole blood microarray, non-replicating). A third PBMC dataset for independent replication of the opioid axis does not exist publicly as of 2026-08-04.
351: 
352: 10. **Medication, age, and BMI confounding (2026-08-04).** GSE221921 metadata contains only `Sample`, `Etiology`, and `Gender` — no age, BMI, or medication data (the GEO soft file adds only `tissue: Blood`). This is especially critical for the **opioid axis finding**: FM patients frequently use opioids, antidepressants, and pregabalin, and chronic opioid exposure is known to regulate the expression of opioid receptors themselves. **The elevated OPRM1/OPRK1/TACR1 signal in PBMCs cannot be distinguished from a pharmacological effect with the available data** — it may reflect disease biology, medication, or both. Any validation cohort must record medication status and stratify by it. This limitation is acknowledged for the protocol design in `PROTOCOL_Olink_FM_Biomarker_Validation.md` (§119) and is elevated here to an explicit risk for the current findings.
353: 11. **Tissue Extrapolations of Peripheral Blood mRNA.** Expression levels of *DRD2* measured in peripheral blood cells (PBMCs or whole blood) reflect basal, low-level transcription in circulating immune sub-populations and cannot be interpreted as a direct proxy for central nervous system dopaminergic function, striatal D2 receptor density, or mesolimbic neurotransmission. Central dopaminergic pathology must be evaluated via brain-specific germline sQTL genetic mechanisms (§4.7) or central neuroimaging/CSF studies.
354: 
355: 12. **COL9A1/PTN Bonferroni-survivors characterization corrected (2026-08-04, adversarial review).** An initial description of "4 robust genes" (COL9A1, BPIFB2, PTN, ST3GAL1) was inflated. Post-adversarial verification: only **COL9A1** (p_adj_Bonf = 8.5e-5) and **PTN** (p_adj_Bonf = 0.020) survive Bonferroni correction on the sex-adjusted model. BPIFB2 is nominally significant (p_adj = 0.0035) but does not survive Bonferroni (p_adj_Bonf = 0.063). ST3GAL1 is downregulated (FC = 0.765) and anticorrelated with the COL9A1–PTN module (r = -0.23). The characterization "Robust 5/5 models" was also incorrect: no gene passes all 5 models (all fail male-only). The corrected description: COL9A1 and PTN are the only Bonferroni-surviving sex-adjusted genes from the CWP causal set; BPIFB2 is a secondary candidate; ST3GAL1 is a negative regulator candidate.
356: 
357: ---
358: 
359: ## 6. Conclusion
360: 
361: A targeted reanalysis of two public transcriptomic cohorts, informed by population-scale UK Biobank plasma proteomics, reframes the peripheral molecular signature of fibromyalgia. In FM PBMCs (GSE221921), we find: (1) a **complete opioid/tachykinin neuropeptide circuit activated** (TACR1 d = +0.60, OPRM1 d = +0.53, TAC1, OPRK1; coordinated co-expression rho 0.31–0.63) — the largest effect-size block in the investigation and the most robust finding, surviving all five sensitivity models including sex-stratified analysis; (2) **an extracellular-matrix / neurite-outgrowth module — *COL9A1* (FC = 2.32, d = +0.88) and *PTN* (FC = 2.91, d = +0.61) — is the only signal from the chronic-widespread-pain causal set that survives Bonferroni correction on the sex-adjusted model**, forming a co-expressed pair (r = 0.51) with direct relevance to joint pain (COL9A1, osteoarthritis link) and nerve repair (PTN), and detectable in plasma by Olink — the primary validation target of this investigation; (3) **CA14, the top UKB causal protein for chronic widespread pain, elevated in PBMC mRNA in the unadjusted analysis** (FC = 2.29, d = +0.41) **but not surviving the sex-stratified primary model** (female-only: p = 0.135, d = +0.24, FC = 1.60; the unadjusted signal is confounded by the structural sex imbalance — see §4.2) **while downregulated in plasma** in the UKB cross-sectional analysis, with MR indicating a protective effect of genetically elevated CA14 — retained here as a direction-specific reference candidate (testable prediction of ↓ CA14 in FM plasma; repurposing direction toward CA14 agonism rather than sulthiame inhibition) rather than the lead target; and (4) **five UKB causal immune-signaling genes downregulated** (TNFRSF1B, CD74, COL18A1, BTN2A1, TNFRSF4), indicating an immunomodulatory/exhaustion pattern rather than classical inflammation — consistent with the absence of IL-6/IL-8 from the highlighted proteins of the largest chronic pain proteomics screen (51,644 UKB participants; TAC1/Substance P not covered by that panel and therefore not evaluable); and (5) the GWAS-prioritized neural genes *MDGA2* and *DRD2* robustly upregulated. These PBMC-derived signatures do not replicate in whole blood (GSE67311), establishing them as PBMC-specific and setting plasma protein measurement as the decisive validation. The dopamine agonist RCT evidence remains limited (one unreplicated positive trial in 21 years). We conclude that the peripheral biology of FM is best described as **neuropeptide nociceptive signaling plus extracellular-matrix / neurite-outgrowth dysregulation (COL9A1–PTN) with immunomodulation (UKB immune genes) and pH/nociception dysregulation (CA14)** — and we recommend prioritizing **COL9A1 and PTN** (Olink, plasma-detectable, Bonferroni-surviving) for plasma validation, with CA14 measured as a direction-specific reference, Substance P/enkephalins (ELISA) as secondary neuropeptide measures, and IL-8 retained as an assay control, in sex-balanced, medication-stratified, cell-type-resolved cohorts.
362: 
363: ---
364: 
365: ## References
366: 
367: Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. *J R Stat Soc B*, 57(1), 289–300.
368: 
369: Bi, W., Yang, M., & Mao, R. (2024). Unraveling Shared Diagnostic Biomarkers of Fibromyalgia in Ankylosing Spondylitis. *J Inflamm Res*, 17, 6395–6413. PMID: 39310900.
370: 
371: Bäckryd, E., et al. (2017). Evidence of both systemic inflammation and neuroinflammation in fibromyalgia patients, as assessed by a multiplex protein panel applied to the cerebrospinal fluid and to plasma. *J Pain Res*, 10, 515–525. PMID: 28424559. (PMC5344444.)
372: 
373: Chen, L., Kelleher, E., Meng, R., Liu, D., Guo, Y., Wang, Y., Gao, Y., Huang, Z., Liang, Z., Yuan, S., Zeng, C., Lei, G., Ma, J., Dong, Y., Irani, A., Xie, J., & Prieto-Alhambra, D. (2025). Diagnosis, Prognosis, and Drug Target Discovery for Chronic Widespread Pain: A Large Proteogenomic Study. *Adv Sci (Weinh)*. PMID: 41025730. DOI: 10.1002/advs.202507691. PMC12713070. (Versión publicada del preprint medRxiv 10.1101/2024.10.29.24316353; EuropePMC PPR932603.)
374: 
375: Chinn, S., Caldwell, W., & Gritsenko, K. (2016). Fibromyalgia Pathogenesis and Treatment Options Update. *Curr Pain Headache Rep*, 20(4), 25. PMID: 26922414.
376: 
377: De la Luz-Cuellar, Y. E., Coffeen, U., Mercado, F., & Contreras, B. (2023). Spinal dopaminergic D1- and D2-like receptors have a sex-dependent effect in an experimental model of fibromyalgia. *Eur J Pharmacol*, 948, 175696. PMID: 37003519.
378: 
379: Edwards, S., Callicoatte, C. N., Barattini, A. E., & Gilpin, N. W. (2022). Pramipexole treatment attenuates mechanical hypersensitivity in male rats experiencing chronic inflammatory pain. *Neuropharmacology*, 208, 108985. PMID: 35085583.
380: 
381: Gowri Gopal, K., Robi, L.S., & Sherin, D.R. (2026). Molecular insights into fibromyalgia: association of hub genes with pain targets, neuropathic pathways, and stress-related hormones. *In Silico Pharmacol*, 14(2), 135. PMID: 42109571.
382: 
383: Hamblin, R., Ntali, G., & Karavitaki, N. (2026). Impulse control disorders and dopamine agonists. *Best Pract Res Clin Endocrinol Metab*, 40(1), 101980. PMID: 42034459.
384: 
385: Holman, A.J., & Myers, R.R. (2005). A Randomized, Double-Blind, Placebo-Controlled Trial of Pramipexole, a Dopamine Agonist, in Patients With Fibromyalgia Receiving Concomitant Medications. *Arthritis Rheum*, 52(8), 2495–2505. PMID: 16052595. doi: 10.1002/art.21191.
386: 
387: Joodi, S. A., Nawwar, D. A., & Rasheed, N. O. A. (2026). Therapeutic and research frontiers in fibromyalgia: integrating pathophysiology with innovative drug repurposing. *Inflammopharmacology*, 34(1), 89–105. PMID: 42489789.
388: 
389: Kerrebijn, I., et al. (2025). The genetic architecture of fibromyalgia across 2.5 million individuals. *medRxiv*. PMID: 41001472. doi: 10.1101/2025.09.18.25335914.
390: 
391: Jones, K.D., et al. (2016). Genome-wide expression profiling in the peripheral blood of patients with fibromyalgia. *Clin Exp Rheumatol*, 34(2 Suppl 96), S89–98. PMID: 27157394. (GSE67311.)
392: 
393: Li, Z.Y., et al. (2025). Large-Scale Plasma Proteomics to Profile Pathways and Prognosis of Chronic Pain. *Adv Sci*, 12(16), e2410160. PMID: 40048323. (PMC12021123.)
394: 
395: Lindström, S., Wolfschlag, M., & Håkansson, A. (2026). Pramipexole exposure and risk of incident gambling disorder in individuals with psychiatric disorders: A nationwide register-based cohort study. *J Affect Disord*, 370, 112–119. PMID: 42217644.
396: 
397: Love, M.I., Huber, W., & Anders, S. (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biol*, 15, 550. PMID: 25516281.
398: 
399: Mohapatra, G., et al. (2024). Identification of unique genomic signatures in patients with fibromyalgia and chronic pain. *Sci Rep*, 14, 3949. PMID: 38366049.
400: 
401: O'Mahony, L.F., et al. (2021). Is fibromyalgia associated with a unique cytokine profile? A systematic review and meta-analysis. *Rheumatology (Oxford)*, 60(7), 3243–3253. PMID: 33576773. [Reference to the meta-analytic IL-8 literature superseded by UKB scale; see Discussion §4.1.]
402: 
403: Pacheco, R., Contreras, F., & Zouali, M. (2014). The dopaminergic system in autoimmune diseases. *Front Immunol*, 5, 117. PMID: 24711809.
404: 
405: Martins, C.P., Paes, R.S., Baldasso, G.M., Ferrarini, E.G., Scussel, R., Zaccaron, R.P., Machado-de-Ávila, R.A., Lock Silveira, P.C., & Dutra, R.C. (2022). Pramipexole, a dopamine D3/D2 receptor-preferring agonist, attenuates reserpine-induced fibromyalgia-like model in mice. *Neural Regen Res*, 17(2), 450–458. PMID: 34269222.
406: 
407: Rodríguez-Pintó, I., et al. (2014). Fibromyalgia and cytokines. *Immunol Lett*, 162(1 Pt A), 220–227. PMID: 24462815.
408: 
409: Russell, I.J., et al. (1994). Elevated cerebrospinal fluid levels of Substance P in patients with fibromyalgia syndrome. *Arthritis Rheum*, 37(11), 1593–1601. PMID: 7526868.
410: 
411: Sarzi-Puttini, P., et al. (2020). Fibromyalgia: An update. *Nat Rev Rheumatol*, 16(11), 645–660. PMID: 33024295.
412: 
413: Tayyab, M., Sasaoka, T., Abe, M., & Natsume, R. (2025). Dopamine D2S/D2L Receptor Regulation of Alcohol-Induced Reward and Signalling. *Addict Biol*, 30(2), e13480. PMID: 41239854.
414: 
415: Tsilioni, I., Russell, I.J., Stewart, J.M., Gleason, J.M., & Theoharides, T.C. (2016). Neuropeptides CRH, SP, HK-1, and inflammatory cytokines IL-6 and TNF are increased in serum of patients with fibromyalgia and chronic fatigue syndrome, indicating a role for mast cells and neuroimmune axis. *J Pharmacol Exp Ther*, 357(1), 239–246. PMID: 26763911.
416: 
417: Trott, O., & Olson, A.J. (2010). AutoDock Vina: improving the speed and accuracy of docking with a new scoring function, efficient optimization, and multithreading. *J Comput Chem*, 31(2), 455–461. PMID: 19499576.
418: 
419: Zhang, Y., Bertolino, A., Fazio, L., Blasi, G., Rampino, A., Romano, R., Lee, M.L.T., Xiao, T., Papp, A., Wang, D., & Sadée, W. (2007). Polymorphisms in human dopamine D2 receptor gene affect gene expression, splicing, and neuronal activity during working memory. *Proc Natl Acad Sci USA*, 104(51), 20552–20557. PMID: 18077373.
420: 
421: Zhao, F., et al. (2025). Identification of diagnostic biomarkers for fibromyalgia using gene expression analysis and machine learning. *Front Genet*, 16, 1535541. PMID: 40313599.
422: 
423: ---
424: 
425: ## Data & Code Availability
426: 
427: All transcriptomic data are publicly available from GEO (GSE221921, GSE67311). The GSE221921 processed data matrix (`GSE221921_FM_ProcessedData.xlsx`) must be downloaded from GEO and placed in the `datos/geo/PBMC_FM_96patients_93controls/` directory for local replication.
428: 
429: Analysis scripts, documentation, and derived tables are publicly available on GitHub at [https://github.com/Grizaceo/protein-lab](https://github.com/Grizaceo/protein-lab). The specific version of the code used for this preprint (v1.0.0) is permanently archived on Zenodo (DOI: 10.5281/zenodo.20250218, URL: https://zenodo.org/records/20250218).
430: 
431: The repository includes:
432: - `scripts/sensitivity_analysis_gse221921.py` — five-model sensitivity analysis
433: - `scripts/cross_context_gwas_neural_genes.py` — cross-context comparison of GWAS-prioritized neural genes vs. mast cell markers across PBMC and whole-blood datasets
434: - `scripts/phase2_rct_review.py` — literature review evidence table
435: - `validate_fm_biomarkers_iter2.py` — expanded 19-gene panel with Mann-Whitney + Bonferroni + Cohen's d (post-adversarial-audit v3)
436: - `scripts/validate_fm_biomarkers_gse67311.py` — whole-blood cross-validation (negative result, verified group counts 67/75)
437: - `scripts/deconvolution_cell_types.py` — cell-type marker-based deconvolution of GSE67311
438: - `scripts/validate_opioid_axis_gse67311.py` — full opioid/tachykinin axis (TACR1/OPRM1/OPRK1/TAC1/PENK) in GSE67311 + co-expression Spearman
439: 
440: Representative derived tables include:
441: - `analisis/sensitivity_analysis_GSE221921.csv` — five-model robustness table for PBMC reanalysis
442: - `analisis/cross_context_gwas_neural_genes.csv` — cross-context comparison table used for the PBMC vs. whole-blood contrast
443: - `analisis/RCT_dopamine_agonists_FM.csv` — targeted literature review evidence table
444: 
445: Software: Python 3.10, pandas 1.5.3, scipy 1.10.1, statsmodels 0.13.5.
446: 
447: ## AI-Assisted Research Methodology
448: 
449: This study was conducted using an agentic AI-assisted research methodology implemented within a human-in-the-loop (HITL) framework. Analytical pipelines, literature synthesis, and computational design steps were developed with the support of large language model agents (Claude, Anthropic). All scientific claims were systematically validated by the human author against pre-established, independently verifiable ground truths: AlphaFold structural predictions (EMBL-EBI), RCSB PDB crystallographic coordinates, ChEMBL bioactivity databases, GEO-deposited expression matrices, UK Biobank proteomics publications, and published statistical methods. Verification followed an evidence-first principle: no finding was accepted without traceable support from primary sources. This framework is implemented in the open-source `agentic-lab-eac` package (Apache-2.0, GitHub: Grizaceo/agentic-lab-eac), which formalizes the generate–review–verify cycle used throughout this study.
450: 
451: ## Conflict of Interest
452: 
453: The author declares no conflicts of interest.
454: 
455: ## Author's Note
456: 
457: This study was initiated out of personal motivation following personal experience with fibromyalgia in close contacts. No financial or institutional interest is involved.
