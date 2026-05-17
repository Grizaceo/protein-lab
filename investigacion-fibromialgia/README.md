# GWAS-Prioritized Neural Genes Are Differentially Expressed in Fibromyalgia PBMCs

**A Targeted Reanalysis of Public Transcriptomic Cohorts**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Preprint](https://img.shields.io/badge/Preprint-Draft_v2.0-blue)](preprint_dopaminergic_convergence_FM.md)

---

## Overview

This repository contains the analysis code and derived results for a targeted,
hypothesis-driven reanalysis of two public transcriptomic datasets interrogating
GWAS-prioritized neural genes in fibromyalgia (FM).

**Central question:** Do the 13 neural genes prioritized by the Kerrebijn et al.
(2025) FM GWAS meta-analysis (PMID 41001472) show differential expression in
FM patients?

**Datasets analyzed:**
- **GSE221921** — PBMCs, RNA-seq, 96 FM / 93 HC (Mohapatra et al., 2024)
- **GSE67311** — Whole blood, Affymetrix microarray, 70 FM / 70 HC (Kurian et al., 2017)

**Key findings:**
- *MDGA2* (q = 1.1×10⁻⁷) and *DRD2* (q = 2.9×10⁻⁵) are robustly upregulated
  in FM PBMCs across **all five analytical sensitivity models**, including
  sex-adjusted OLS regression and female-only subgroup analysis.
- *CAMKV* and *CELF4* are supported in 4/5 models but sensitive to sex covariate.
- The GWAS neural gene signal is **PBMC-specific**: absent in whole blood (GSE67311),
  which instead shows the expected mast cell / basophil panel signature.
- The sole positive dopamine agonist RCT in FM (pramipexole; Holman & Myers, 2005)
  remains unreplicated after 21 years.

> **Note:** These are exploratory, hypothesis-generating findings. No wet-lab
> experiments were performed. Validation in sex-balanced cohorts with cell-type
> resolution is required before biological conclusions can be drawn.

---

## Repository Structure

```
investigacion-fibromialgia/
├── preprint_dopaminergic_convergence_FM.md   # Manuscript (draft v2.0)
├── PLAN_PCI_GENOMICS.md                      # Submission strategy for PCI Genomics
├── scripts/
│   ├── sensitivity_analysis_gse221921.py     # Five-model sensitivity analysis (primary)
│   ├── cross_context_gwas_neural_genes.py    # PBMC vs. whole blood cross-context comparison
│   └── phase2_rct_review.py                  # Dopamine agonist RCT evidence table
├── analisis/
│   ├── sensitivity_analysis_GSE221921.csv    # Table 1: five-model robustness results
│   ├── cross_context_gwas_neural_genes.csv   # Table 2: PBMC vs. whole blood contrast
│   └── RCT_dopamine_agonists_FM.csv          # Table 3: dopamine agonist trials
└── datos/
    └── GSE67311_DEGs_*.csv                   # Pre-computed DEGs for whole blood dataset
```

---

## Reproducing the Analysis

### Requirements

```
Python >= 3.10
pandas >= 1.5
scipy >= 1.10
statsmodels >= 0.13
```

Install dependencies:

```bash
pip install pandas scipy statsmodels openpyxl
```

### Data Download

The GSE221921 processed expression matrix must be downloaded manually from GEO:

1. Go to: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE221921
2. Download: `GSE221921_FM_ProcessedData.xlsx` (Supplementary file)
3. Place it at: `datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx`

GSE67311 pre-computed DEG results are included in `datos/`.

### Running the Scripts

```bash
# Primary analysis: five-model sensitivity analysis on GSE221921
python scripts/sensitivity_analysis_gse221921.py

# Cross-context comparison (PBMC vs. whole blood)
python scripts/cross_context_gwas_neural_genes.py

# Dopamine agonist RCT evidence table
python scripts/phase2_rct_review.py
```

Output CSV files will be written to `analisis/` and should match the pre-computed
results included in the repository.

---

## Preprint

The full manuscript is available in [`preprint_dopaminergic_convergence_FM.md`](preprint_dopaminergic_convergence_FM.md).

**Citation (working draft):**

> [Authors TBD] (2026). GWAS-Prioritized Neural Genes Are Differentially Expressed
> in Fibromyalgia PBMCs: A Targeted Reanalysis of Public Transcriptomic Cohorts.
> *Preprint v2.0, May 2026.*

---

## Key References

- Kerrebijn et al. (2025). The genetic architecture of fibromyalgia across 2.5 million individuals. *medRxiv*. PMID: 41001472. doi: 10.1101/2025.09.18.25335914v1
- Mohapatra et al. (2024). Identification of unique genomic signatures in patients with fibromyalgia and chronic pain. *Sci Rep*, 14, 3949. PMID: 38366049
- Kurian et al. (2017). Peripheral Blood Gene Expression in Fibromyalgia. PMID: 27157394 (GSE67311)
- Holman & Myers (2005). A Randomized, Double-Blind, Placebo-Controlled Trial of Pramipexole in Fibromyalgia. *Arthritis Rheum*, 52(8), 2495–2505. PMID: 16052595

---

## License

MIT License. See [LICENSE](LICENSE) for details.

Analysis code: free to use and adapt with attribution.
Derived result tables: CC BY 4.0.
Raw data belongs to the original dataset authors and GEO depositors.

---

## Conflict of Interest

The authors declare no conflicts of interest.
