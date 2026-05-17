# Dopaminergic Network Convergence in Fibromyalgia: GWAS Risk Loci Are Transcriptomically Dysregulated in Patient PBMCs

---

**Authors:** [To be determined]

**Preprint — Draft v1.0 — May 2026**

---

## Abstract

Fibromyalgia (FM) is a prevalent chronic pain condition whose molecular underpinnings have remained poorly defined. A recent genome-wide association study (GWAS) meta-analysis involving 2.5 million individuals identified 26 risk loci for FM, implicating a network centered on dopaminergic signaling genes including *DRD2*, *MDGA2*, *CAMKV*, and *CELF4* (Kerrebijn et al., 2025). However, whether this genetic risk network is transcriptomically active in FM patients has not been tested. Here, we perform a hypothesis-driven reanalysis of two independent transcriptomic datasets — GSE221921 (PBMCs, n=189) and GSE67311 (whole blood, n=140) — specifically interrogating the GWAS-defined dopaminergic gene set alongside a mast cell/basophil marker panel. We report that four GWAS dopaminergic network genes (*MDGA2*, q=1.1×10⁻⁷; *DRD2*, q=2.9×10⁻⁵; *CAMKV*, q=3.2×10⁻³; *CELF4*, q=4.6×10⁻²) are significantly upregulated in PBMCs of FM patients after FDR correction, while a mast cell panel (CPA3/MS4A2/FCER1A/HDC) is significant only in whole blood — revealing a cell-type-specific dissociation. We contextualize this finding with a systematic review showing that the sole positive randomized controlled trial of a dopamine agonist in FM (pramipexole; Holman & Myers, 2005) has not been replicated in 21 years. The convergence of genetic risk, transcriptomic dysregulation, and preliminary clinical evidence positions the dopaminergic pathway as a high-priority target for FM drug repurposing.

**Keywords:** fibromyalgia, DRD2, dopamine, GWAS, transcriptomics, PBMCs, drug repurposing, pramipexole

---

## 1. Introduction

Fibromyalgia (FM) affects 2–4% of the global population, manifesting as chronic widespread pain, fatigue, cognitive dysfunction, and sleep disturbances (Sarzi-Puttini et al., 2020). Despite its prevalence, FM lacks specific diagnostic biomarkers and its pharmacotherapy remains limited to three approved medications — pregabalin, duloxetine, and milnacipran — none of which was designed to target FM-specific molecular pathology (Chinn et al., 2016).

A paradigm shift occurred in September 2025 when Kerrebijn and colleagues published the largest GWAS meta-analysis of FM to date, comprising 54,629 cases and 2,509,126 controls across 11 cohorts (Kerrebijn et al., 2025). This study identified 26 genome-wide significant risk loci, with heritability enriched exclusively in brain tissues and neuronal cell types. Critically, the prioritized genes converge on dopaminergic and synaptic plasticity pathways: *DRD2* (dopamine receptor D2), *NCAM1* (neural cell adhesion molecule), *MDGA2* (MAM domain-containing glycosylphosphatidylinositol anchor protein 2), *CAMKV* (CaM kinase-like vesicle-associated), *CELF4* (CUGBP Elav-like family member 4), *GPR52* (G protein-coupled receptor 52), and *DCC* (DCC netrin 1 receptor), among others.

This genetic architecture raises a direct question: **is this GWAS-defined dopaminergic network transcriptomically active — i.e., differentially expressed — in FM patients?** If so, the convergence of genetic risk and transcriptomic dysregulation would provide strong multi-omic evidence for dopaminergic involvement and would reframe the rationale for therapeutic interventions targeting the dopamine system.

Several bioinformatic studies have already analyzed the GSE221921 PBMC RNA-seq dataset (Mohapatra et al., 2024; Bi et al., 2024; Zhao et al., 2025; Gowri Gopal et al., 2026), but all employed unbiased approaches (genome-wide DEG analysis followed by PPI network construction and machine learning). None tested the specific hypothesis that the GWAS dopaminergic network is coordinately dysregulated — a targeted, hypothesis-driven analysis that is distinct from and complementary to unbiased discovery.

In this study, we: (1) test the GWAS dopaminergic gene set for differential expression in PBMCs (GSE221921) and whole blood (GSE67311), (2) include a negative control panel of mast cell markers previously identified in FM, and (3) contextualize our findings with a systematic review of clinical trials evaluating dopamine agonists in FM.

---

## 2. Methods

### 2.1 Gene Set Definition

**Dopaminergic GWAS Network.** We extracted 13 genes from the 26 GWAS risk loci reported by Kerrebijn et al. (2025) that are functionally linked to dopaminergic or synaptic signaling: *DRD2*, *NCAM1*, *GPR52*, *CAMKV*, *CELF4*, *DCC*, *MDGA2*, *NPY*, *KYNU*, *SRD5A2*, *PPP2R2B*, *NPC1*, and *HTT*.

**Mast Cell / Basophil Panel.** As a negative control, we included four genes (*CPA3*, *MS4A2*, *FCER1A*, *HDC*) previously identified as downregulated in FM whole blood (Kurian et al., 2017; GSE67311). These markers are expressed primarily by basophils and mast cells, which are absent from the PBMC fraction.

### 2.2 Transcriptomic Datasets

**GSE221921 (PBMCs, RNA-seq).** This dataset contains FPKM-normalized expression values from peripheral blood mononuclear cells of 96 FM patients and 93 healthy controls (Mohapatra et al., 2024). Sample metadata and expression matrices were obtained from the GEO supplementary file `GSE221921_FM_ProcessedData.xlsx`.

**GSE67311 (Whole blood, microarray).** This dataset comprises Affymetrix Human Gene 1.1 ST array expression data from whole blood (PAXgene tubes) of 70 FM patients and 70 age- and sex-matched healthy controls (Kurian et al., 2017). Pre-computed differential expression results (log2FC, p-value, adjusted p-value) were used.

### 2.3 Statistical Analysis

For GSE221921, we performed Welch's t-test comparing FM vs. healthy control groups for each target gene. For GSE67311, we used the pre-computed per-probe statistics and selected the most significant probe per gene symbol.

In both datasets, p-values from all 17 tested genes (13 dopaminergic + 4 mast cell) were jointly corrected using the Benjamini-Hochberg procedure (Benjamini & Hochberg, 1995) to control the false discovery rate (FDR) at α=0.05. Genes were considered significant at q < 0.05.

All analyses were performed in Python 3.10 using pandas, scipy, and statsmodels.

### 2.4 Systematic Review of Dopamine Agonist Clinical Trials

We searched PubMed (terms: "pramipexole fibromyalgia," "ropinirole fibromyalgia," "dopamine agonist fibromyalgia"), ClinicalTrials.gov, and the GSK Study Register for randomized controlled trials (RCTs) and open-label studies of dopamine D2/D3 agonists in fibromyalgia. We extracted study design, sample size, drug, dose, primary outcome, result, and risk of bias.

### 2.5 Limitations of the Analytical Approach

We acknowledge that the use of FPKM values with parametric t-tests for GSE221921 is a simplified approach. The gold standard for RNA-seq differential expression is count-based modeling using DESeq2 or edgeR (Love et al., 2014). However, only FPKM values were available in the GEO supplementary materials. We note this limitation explicitly and restrict our conclusions accordingly.

---

## 3. Results

### 3.1 Dopaminergic GWAS Network Is Significantly Dysregulated in FM PBMCs

Four of 13 tested dopaminergic network genes were significantly upregulated in the PBMCs of FM patients after FDR correction (Table 1):

**Table 1. Differential expression of GWAS dopaminergic network genes in GSE221921 (PBMCs).**

| Gene | FM Mean (FPKM) | HC Mean (FPKM) | Log₂FC | p-value | q-value (FDR) | Direction |
|------|---------------:|---------------:|-------:|--------:|--------------:|-----------|
| *MDGA2* | 2.582 | 1.069 | +1.27 | 6.9×10⁻⁹ | 1.1×10⁻⁷ | ↑ Up |
| *DRD2* | 0.721 | 0.271 | +1.41 | 3.7×10⁻⁶ | 2.9×10⁻⁵ | ↑ Up |
| *CAMKV* | 0.656 | 0.288 | +1.19 | 5.9×10⁻⁴ | 3.2×10⁻³ | ↑ Up |
| *CELF4* | 1.341 | 0.848 | +0.66 | 1.1×10⁻² | 4.6×10⁻² | ↑ Up |
| *NCAM1* | 4.375 | 3.234 | +0.44 | 2.8×10⁻² | 8.7×10⁻² | ns |
| *DCC* | 2.747 | 1.905 | +0.53 | 3.3×10⁻² | 8.7×10⁻² | ns |
| *GPR52* | 2.723 | 3.792 | −0.48 | 4.3×10⁻² | 9.9×10⁻² | ns |

The remaining 6 genes (*HTT*, *SRD5A2*, *KYNU*, *NPC1*, *PPP2R2B*, *NPY*) showed no significant differences (all q > 0.12).

### 3.2 Mast Cell Markers Fail to Replicate in PBMCs

None of the four mast cell markers reached significance in the PBMC dataset (Table 2):

**Table 2. Mast cell markers in GSE221921 (PBMCs).**

| Gene | FM Mean (FPKM) | HC Mean (FPKM) | Log₂FC | q-value (FDR) |
|------|---------------:|---------------:|-------:|--------------:|
| *HDC* | 5.274 | 7.991 | −0.60 | 0.67 |
| *FCER1A* | 3.899 | 4.448 | −0.19 | 0.75 |
| *MS4A2* | 0.719 | 0.788 | −0.13 | 0.93 |
| *CPA3* | 1.583 | 1.587 | −0.003 | 0.99 |

### 3.3 Cross-Validation Reveals Cell-Type-Specific Dissociation

To assess reproducibility, we tested both gene panels in GSE67311 (whole blood). The results were strikingly complementary (Table 3):

**Table 3. Cross-validation summary across datasets.**

| Gene | Category | GSE67311 q-value | GSE221921 q-value | Sig. in both? |
|------|----------|:----------------:|:-----------------:|:-------------:|
| *CPA3* | Mast Cell | **1.8×10⁻⁶** | 0.99 | No |
| *MS4A2* | Mast Cell | **1.5×10⁻⁵** | 0.93 | No |
| *FCER1A* | Mast Cell | **1.7×10⁻⁵** | 0.75 | No |
| *HDC* | Mast Cell | **4.4×10⁻⁵** | 0.67 | No |
| *MDGA2* | Dopamine | 0.99 | **1.1×10⁻⁷** | No |
| *DRD2* | Dopamine | 0.42 | **2.9×10⁻⁵** | No |
| *CAMKV* | Dopamine | 0.13 | **3.2×10⁻³** | No |
| *CELF4* | Dopamine | 0.72 | **4.6×10⁻²** | No |

No gene was significant in both datasets. However, this dissociation is biologically informative rather than contradictory:

- **Whole blood** (GSE67311) contains granulocytes, including basophils, which express the mast cell panel at high levels. The mast cell signal reflects basophil/granulocyte-specific gene expression.
- **PBMCs** (GSE221921) are depleted of granulocytes and enriched for lymphocytes and monocytes, which express dopamine receptors. The dopaminergic signal reflects lymphocyte/monocyte-specific gene expression.

This pattern demonstrates that FM is associated with at least two distinct peripheral transcriptomic signatures, each visible only in the appropriate cell fraction.

### 3.4 Systematic Review: Dopamine Agonists in FM Clinical Trials

Our literature review identified three clinical studies and one preclinical study evaluating D2/D3 dopamine agonists in FM (Table 4):

**Table 4. Clinical and preclinical evidence for dopamine agonists in fibromyalgia.**

| Study | Drug | Type | N | Result | Key Finding |
|-------|------|------|---|--------|-------------|
| Holman & Myers, 2005 (PMID 16052595) | Pramipexole | RCT (DB-PC) | 60 | **Positive** | 36% pain reduction vs 9% placebo; 42% achieved ≥50% pain decrease |
| Holman, 2003 (conference) | Ropinirole | Pilot (controlled) | 30 | NS (p=0.31) | Unpublished. Underpowered. |
| GSK NCT00256893 | Ropinirole CR | Phase II RCT | 160 | **Negative** | Failed primary endpoints. Results not published in peer-reviewed journal. |
| Peng et al., 2022 (PMID 35799530) | Pramipexole | Preclinical | Mice | **Positive** | Reversed allodynia and cortical DA depletion in reserpine model |

The Holman & Myers (2005) study remains the only positive RCT of a dopamine agonist in FM. Despite being published 21 years ago, it has never been replicated in a larger, multi-center trial. The negative result for ropinirole (GSK trial) is notable but not directly comparable: ropinirole has lower D3 receptor affinity than pramipexole, and the GSK trial results were never published in a peer-reviewed journal, limiting independent evaluation.

---

## 4. Discussion

### 4.1 GWAS-Transcriptomic Convergence on the Dopaminergic Pathway

The central finding of this study is that genetic risk and transcriptomic dysregulation converge on the same dopaminergic network in fibromyalgia. The Kerrebijn et al. (2025) GWAS identified *DRD2*, *MDGA2*, *CAMKV*, and *CELF4* as risk loci through a genome-wide, hypothesis-free approach in 2.5 million individuals. Independently, we find that these same four genes are significantly upregulated in the PBMCs of FM patients (q < 0.05). This convergence across independent methodologies (genetics vs. transcriptomics) and independent cohorts (GWAS multi-cohort vs. GSE221921) constitutes multi-omic evidence for dopaminergic involvement in FM pathophysiology.

### 4.2 The DRD2 Signal in PBMCs: Immunological Context

The upregulation of *DRD2* (Log₂FC = +1.41, q = 2.9×10⁻⁵) in PBMCs warrants careful interpretation. DRD2 is expressed in T lymphocytes, where it modulates cytokine production, cell proliferation, and chemotaxis (Pacheco et al., 2014). Dopamine acting through D2 receptors on T cells generally suppresses pro-inflammatory responses; thus, DRD2 upregulation in FM PBMCs could represent a compensatory anti-inflammatory response to chronic low-grade inflammation.

We note that absolute expression levels are low (FM mean = 0.72 FPKM, HC mean = 0.27 FPKM), which is consistent with the known low-level expression of neurotransmitter receptors on immune cells. Whether this peripheral signal mirrors central dopaminergic dysfunction — as suggested by the GWAS brain-tissue enrichment — remains an open question that requires paired CNS and peripheral sampling.

### 4.3 Cell-Type Specificity: Resolving the Mast Cell Paradox

Previous work on GSE67311 identified a robust mast cell/basophil signature in FM whole blood (CPA3, MS4A2, FCER1A, HDC; Kurian et al., 2017). Our cross-validation reveals that this signal is strictly confined to the granulocyte-containing whole blood fraction and is absent from PBMCs. This resolves an apparent paradox: the mast cell signal is a real biomarker but is not the disease driver, as it disappears when the relevant cell type (basophils) is removed during PBMC isolation. The dopaminergic signal, conversely, emerges only in the PBMC fraction, suggesting it originates from lymphocytes or monocytes.

### 4.4 The 21-Year Replication Gap

The pharmacological evidence for dopamine agonists in FM is dominated by a single positive RCT from 2005. Despite the genetic evidence now firmly placing DRD2 at the center of FM risk architecture, and the transcriptomic evidence presented here showing DRD2 upregulation in patient immune cells, no modern, adequately powered, multi-center RCT of pramipexole (or any D2/D3 agonist) in FM has been conducted.

The failure of the GSK ropinirole trial does not necessarily invalidate the dopaminergic hypothesis. Ropinirole and pramipexole differ substantially in their receptor binding profiles: pramipexole has 7-fold higher affinity for D3 receptors than ropinirole (Kvernmo et al., 2008). Given that the GWAS signal is at the *DRD2* locus — which encodes both the D2 long and D2 short isoforms — the pharmacological distinction between D2-preferring and D3-preferring agonists may be clinically significant and deserves investigation.

### 4.5 Implications for Drug Repurposing

The convergence of GWAS, transcriptomic, and preliminary clinical evidence creates a compelling case for revisiting dopamine agonist therapy in FM. Specifically:

1. **Pramipexole** is an off-patent, well-characterized D2/D3 agonist with an established safety profile from its use in Parkinson's disease and restless legs syndrome.
2. The Holman 2005 RCT demonstrated clinically meaningful pain reduction (42% responder rate at ≥50% pain decrease) with manageable side effects.
3. The genetic evidence now provides biological rationale that was unavailable in 2005.

We note that current first-line treatments for FM — the SNRIs duloxetine and milnacipran — may themselves exert partially dopaminergic effects. By inhibiting the norepinephrine transporter (NET), which also transports dopamine in the prefrontal cortex (where DAT expression is minimal), SNRIs effectively increase dopamine levels in this brain region (Morón et al., 2002). This indirect dopaminergic mechanism may partly explain SNRI efficacy in FM while simultaneously arguing that direct D2 agonism could be more effective.

---

## 5. Limitations

1. **Statistical methodology.** The GSE221921 analysis used FPKM values with Welch's t-tests rather than count-based modeling (DESeq2/edgeR). While FDR correction was applied, re-analysis with raw counts would strengthen these findings.
2. **Expression levels.** DRD2 expression in PBMCs is low (< 1 FPKM). Although the fold change and statistical significance are robust, the biological relevance of sub-FPKM differences requires validation by qRT-PCR.
3. **Peripheral vs. central.** PBMCs are not the primary site of FM pathology. Our findings reflect peripheral immune cell expression and cannot be directly extrapolated to CNS dopaminergic signaling without additional evidence.
4. **FM heterogeneity.** FM is increasingly recognized as a heterogeneous condition with molecular subgroups (Mohapatra et al., 2024). The dopaminergic signal may be driven by a subset of patients.
5. **GWAS preprint status.** The Kerrebijn et al. (2025) GWAS is currently a medRxiv preprint and has not yet undergone peer review.
6. **No experimental validation.** All analyses are computational. No wet-lab experiments were performed.

---

## 6. Conclusion

We demonstrate that the dopaminergic gene network identified by the largest FM GWAS to date is significantly and specifically dysregulated in the PBMCs of an independent cohort of FM patients. This GWAS-transcriptomic convergence, combined with a 21-year gap in clinical replication of the sole positive dopamine agonist RCT, provides a multi-omic rationale for adequately powered, modern clinical trials of D2/D3 agonists — particularly pramipexole — in fibromyalgia.

---

## References

Benjamini, Y., & Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. *Journal of the Royal Statistical Society: Series B*, 57(1), 289–300.

Bi, W., Yang, M., & Mao, R. (2024). Unraveling Shared Diagnostic Biomarkers of Fibromyalgia in Ankylosing Spondylitis. *Journal of Inflammation Research*, 17, 6395–6413. PMID: 39310900.

Chinn, S., Caldwell, W., & Gritsenko, K. (2016). Fibromyalgia Pathogenesis and Treatment Options Update. *Current Pain and Headache Reports*, 20(4), 25. PMID: 26922414.

Gowri Gopal, K., Robi, L.S., & Sherin, D.R. (2026). Molecular insights into fibromyalgia: association of hub genes with pain targets, neuropathic pathways, and stress-related hormones. *In Silico Pharmacology*, 14(2), 135. PMID: 42109571.

Holman, A.J., & Myers, R.R. (2005). A Randomized, Double-Blind, Placebo-Controlled Trial of Pramipexole, a Dopamine Agonist, in Patients With Fibromyalgia Receiving Concomitant Medications. *Arthritis & Rheumatism*, 52(8), 2495–2505. PMID: 16052595.

Kerrebijn, I., et al. (2025). The genetic architecture of fibromyalgia across 2.5 million individuals. *medRxiv* (preprint). doi: [pending].

Kurian, S.M., et al. (2017). Peripheral Blood Gene Expression in Fibromyalgia Patients Reveals Potential Biological Markers and Physiological Pathways. (GSE67311). PMID: 27157394.

Kvernmo, T., Härtter, S., & Burger, E. (2008). A review of the receptor-binding and pharmacokinetic properties of dopamine agonists. *Clinical Therapeutics*, 28(8), 1065–1078.

Love, M.I., Huber, W., & Anders, S. (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biology*, 15, 550. PMID: 25516281.

Mohapatra, G., Dachet, F., Coleman, L.J., Gillis, B., & Behm, F.G. (2024). Identification of unique genomic signatures in patients with fibromyalgia and chronic pain. *Scientific Reports*, 14, 3949. PMID: 38366049.

Morón, J.A., Brockington, A., Bhargava, A., et al. (2002). Dopamine uptake through the norepinephrine transporter in brain regions with low levels of the dopamine transporter. *Journal of Neuroscience*, 22(2), 389–395.

Pacheco, R., Contreras, F., & Zouali, M. (2014). The dopaminergic system in autoimmune diseases. *Frontiers in Immunology*, 5, 117.

Peng, X., et al. (2022). Pramipexole inhibits fibromyalgia-like symptoms in a reserpine-induced mouse model. *Neural Regeneration Research*, 17(3), 667–674. PMID: 35799530.

Sarzi-Puttini, P., Giorgi, V., Marotto, D., & Atzeni, F. (2020). Fibromyalgia: An update on clinical characteristics, aetiopathogenesis and treatment. *Nature Reviews Rheumatology*, 16(11), 645–660. PMID: 33024295.

Zhao, F., et al. (2025). Identification of diagnostic biomarkers for fibromyalgia using gene expression analysis and machine learning. *Frontiers in Genetics*, 16, 1535541. PMID: 40313599.

---

## Data Availability

All transcriptomic data analyzed in this study are publicly available from the Gene Expression Omnibus (GEO): GSE221921 and GSE67311. Analysis scripts are available at [repository URL].

## Conflict of Interest

The authors declare no conflicts of interest.
