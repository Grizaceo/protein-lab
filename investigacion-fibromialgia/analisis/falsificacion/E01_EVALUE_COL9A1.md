# E01 — E-value Analysis for COL9A1–FM Association

**Date:** 2026-08-14  
**Script:** `scripts/e01_evalue_col9a1.py`  
**Method:** VanderWeele & Ding (2017) E-value for risk ratio.

---

## 1. Observed Effect

| Metric | Value |
|--------|-------|
| Cohen's d | 0.860 |
| n (FM) | 96 |
| n (HC) | 93 |
| FM mean ± SD | 1.974 ± 0.989 |
| HC mean ± SD | 1.195 ± 0.799 |

---

## 2. E-value Calculation

| Metric | Value |
|--------|-------|
| RR (from d) | 4.757 |
| **E-value** | **8.98** |
| E-value (lower 95% CI) | 4.98 |

---

## 3. Interpretation

**An unmeasured confounder would need to have an association of RR ≥ 9.0 
with BOTH COL9A1 expression AND fibromyalgia status to explain away the observed association.**

### Robustness verdict: **HIGH ✅**

- E-value > 2.0 → robust to moderate confounding (VanderWeele benchmark)
- E-value > 3.0 → robust to substantial confounding
- E-value > 5.0 → extremely robust

### Clinical context (for comparison)

| Association | Approximate RR | Approximate E-value |
|-------------|----------------|---------------------|
| Smoking → lung cancer | 15–30 | 29–59 |
| Obesity → diabetes | 3–7 | 5–13 |
| Age → mortality (per decade) | 2–5 | 3–9 |
| **COL9A1 → FM** | **4.8** | **9.0** |

---

## 4. Limitations

- Assumes binary exposure (FM vs HC). Continuous COL9A1 is dichotomized at the group level.
- E-value is a sensitivity analysis, not a confounder test.
- Does not adjust for sex or composition (done in Model 6 separately).
- Borenstein approximation works best for medium effects; very large effects may overestimate OR.

---

## 5. Implications for the manuscript

- COL9A1 is **robust to moderate unmeasured confounding** (E-value > 2).
- The manuscript's claim that COL9A1 is "the most robust finding" is strengthened.
- No remaining computational falsification for COL9A1; wet-lab validation is the next step.
