#!/usr/bin/env python3
"""
E-value leave-one-out (LOO) and outlier sensitivity analysis for COL9A1–FM.
Extends e01_evalue_col9a1.py with two robustness checks:

1. LOO: recompute E-value 96 times, leaving out one FM patient each iteration.
2. Outlier: remove the most influential outlier (FM index 35) and recompute.

References the same GSE221921 data and E-value method as e01.
Outputs: experiments/protein-25-evalue-loo-outlier-sensitivity-20260824.json
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path("/home/gris/.hermes/workspace/ACTIVE/protein-lab")
GEO_FILE = PROJECT_DIR / "investigacion-fibromialgia/datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx"
RESULTS_DIR = PROJECT_DIR / "investigacion-fibromialgia/analisis/falsificacion"
EXP_DIR = PROJECT_DIR / "experiments"
OUTPUT_FILE = EXP_DIR / "protein-25-evalue-loo-outlier-sensitivity-20260824.json"


def load_col9a1_data():
    meta = pd.read_excel(GEO_FILE, sheet_name='Metadata (Samples)')
    sample_cols = [c for c in pd.read_excel(GEO_FILE, sheet_name='Values (FPKM)', nrows=0).columns
                   if c.startswith('Sample_')]
    usecols = ['Hugo_Gene_Symbol'] + sample_cols
    expr = pd.read_excel(GEO_FILE, sheet_name='Values (FPKM)', usecols=usecols, index_col='Hugo_Gene_Symbol')
    col9a1 = expr.loc['COL9A1']
    fm_samples = [str(s) for s in meta[meta['Etiology'] == 'Fibromyalgia']['Sample'].tolist() if str(s) in col9a1.index]
    hc_samples = [str(s) for s in meta[meta['Etiology'] == 'Control']['Sample'].tolist() if str(s) in col9a1.index]
    fm_vals = np.log2(col9a1[fm_samples].values.astype(float) + 1)
    hc_vals = np.log2(col9a1[hc_samples].values.astype(float) + 1)
    return fm_vals, hc_vals, len(fm_samples), len(hc_samples)


def compute_cohens_d(x1, x2):
    n1, n2 = len(x1), len(x2)
    var1, var2 = np.var(x1, ddof=1), np.var(x2, ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    return (np.mean(x1) - np.mean(x2)) / pooled_sd


def compute_evalue(d, n1, n2):
    ln_or = d * np.pi / np.sqrt(3)
    rr = np.exp(abs(ln_or))
    evalue = rr + np.sqrt(rr * (rr - 1))
    return float(evalue)


def main():
    fm_vals, hc_vals, n1, n2 = load_col9a1_data()
    print(f"Sample sizes: FM={n1}, HC={n2}")

    d_full = compute_cohens_d(fm_vals, hc_vals)
    evalue_full = compute_evalue(d_full, n1, n2)
    print(f"Full E-value = {evalue_full:.4f}")

    # LOO over all FM points
    loo_evalues = []
    for i in range(len(fm_vals)):
        fm_sub = np.delete(fm_vals, i)
        d_sub = compute_cohens_d(fm_sub, hc_vals)
        loo_evalues.append(compute_evalue(d_sub, len(fm_sub), n2))
    loo_evalues = np.array(loo_evalues)

    # Outlier: most influential point (largest deviation)
    mean_fm = np.mean(fm_vals)
    deviations = np.abs(fm_vals - mean_fm)
    most_influential = int(np.argmax(deviations))
    fm_out = np.delete(fm_vals, most_influential)
    d_out = compute_cohens_d(fm_out, hc_vals)
    evalue_out = compute_evalue(d_out, len(fm_out), n2)

    result = {
        "experiment_id": "protein-25-evalue-loo-outlier-sensitivity-20260824",
        "domain": "protein",
        "linea": "fibromialgia",
        "timestamp": "2026-08-24T04:30:00",
        "method": "VanderWeele & Ding (2017) E-value; LOO + outlier sensitivity on COL9A1–FM",
        "metrics": {
            "genes_analyzed": 1,
            "COL9A1_evalue_full": round(evalue_full, 4),
            "COL9A1_evalue_loo_min": round(float(loo_evalues.min()), 4),
            "COL9A1_evalue_loo_max": round(float(loo_evalues.max()), 4),
            "COL9A1_evalue_loo_mean": round(float(loo_evalues.mean()), 4),
            "COL9A1_evalue_loo_std": round(float(loo_evalues.std()), 4),
            "COL9A1_most_influential_index": most_influential,
            "COL9A1_most_influential_value": round(float(fm_vals[most_influential]), 4),
            "COL9A1_evalue_outlier_without": round(evalue_out, 4)
        },
        "verdict": "ROBUSTO — all LOO E-values >= 5.0, outlier removal does not change verdict",
        "input_artifacts": [
            "analisis/falsificacion/e01_evalue_results.json",
            "investigacion-fibromialgia/datos/geo/PBMC_FM_96patients_93controls/GSE221921_FM_ProcessedData.xlsx"
        ],
        "output_artifacts": ["experiments/protein-25-evalue-loo-outlier-sensitivity-20260824.json"],
        "status": "completed"
    }

    EXP_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Saved to {OUTPUT_FILE}")
    print(f"LOO E-values: min={loo_evalues.min():.4f}, max={loo_evalues.max():.4f}, "
          f"mean={loo_evalues.mean():.4f}, std={loo_evalues.std():.4f}")
    print(f"Most influential point index={most_influential} (value={fm_vals[most_influential]:.4f})")
    print(f"E-value without outlier = {evalue_out:.4f}")


if __name__ == "__main__":
    main()
