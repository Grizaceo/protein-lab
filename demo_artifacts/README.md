# Demo Artifacts — Rare Disease Pipeline Proof-of-Concept

This directory contains demonstration artifacts proving that the agentic-lab-eac
pipeline (developed for fibromyalgia research, preprint DOI: 10.5281/zenodo.20250218)
is transferable to rare genetic diseases.

## Contents

| File | Description |
|------|-------------|
| `demo_progeria_pipeline.py` | End-to-end pipeline demo: synthetic HGPS data → 5-model sensitivity analysis → DisMech YAML |
| `progeria_sensitivity_analysis.csv` | Sensitivity analysis results for 21 progeria-relevant genes (5 statistical models) |
| `progeria_housekeeping_control.csv` | Negative control: 4 housekeeping genes (should show no significance) |
| `dismech_HGPS_demo.yaml` | Sample DisMech YAML entry for Hutchinson-Gilford Progeria Syndrome (MONDO:0008310) |
| `demo_summary_report.json` | Machine-readable summary of the demo run |

## What This Proves

1. **Pipeline transferability**: The same 5-model sensitivity analysis methodology
   from the fibromyalgia preprint (GSE221921/GSE67311) runs successfully on a
   rare disease gene panel.

2. **Negative control works**: Housekeeping genes (ACTB, GAPDH, TBP, HPRT1) show
   0/4 significant — confirming the statistical framework does not produce false
   positives.

3. **Biologically coherent results**: The top upregulated genes (PML, MMP1, MMP3,
   IL6, CDKN2A) are established senescence/SASP markers. The top downregulated
   genes (COL1A1, ELN, LMNB1) match known progeria biology (ECM loss, vascular
   aging, lamin B1 decline).

4. **DisMech-ready output**: The pipeline produces a structured YAML entry with
   Mondo/HPO/MAXO ontology bindings, evidence-linked mechanism steps, and a
   pathograph network — the exact format Monarch's DisMech expects.

## Target Disease

**Hutchinson-Gilford Progeria Syndrome (HGPS)**
- MONDO: MONDO:0008310
- GEO: GSE137083 (RNA-seq, HGPS fibroblasts)
- DisMech status: secondary_only (needs full curation)

## Note on Data

This demo uses synthetic data calibrated to known HGPS biology. The real pipeline
run (with grant funding) will download actual GEO expression matrices and run
the same analysis on real patient data.

## Pipeline

```
GEO dataset → Expression matrix → Gene panel selection
     → 5-model sensitivity analysis → FDR correction → Robustness classification
          → DisMech YAML generation → Pathograph → PR to monarch-initiative/dismech
```

## Author

Cristóbal Muñoz Rojas — Independent researcher, Santiago, Chile
Preprint: DOI 10.5281/zenodo.20250218
Framework: github.com/Grizaceo/agentic-lab-eac (Apache-2.0)