# Method Description Template (≤2 pages)

**Competition:** [NAME]  
**Target:** [TARGET NAME / PDB]  
**Team:** protein-lab  
**Date:** [YYYY-MM-DD]

---

## 1. Overview

We designed de novo protein binders against [TARGET] using the BindCraft pipeline (Pacesa et al., Nature 2025). BindCraft integrates AlphaFold2-based hallucination, ProteinMPNN sequence design, and multi-stage computational filtering in a single automated workflow.

## 2. Target preparation

- Source structure: [PDB ID], chain [X]
- Trimming: [residue range], [N] residues retained
- Hotspot residues (if used): [list]
- Rationale: minimize GPU memory for cloud execution while preserving binding interface

## 3. Design protocol

| Parameter | Value |
|-----------|-------|
| Pipeline | BindCraft v[VERSION] |
| Compute | Google Colab [T4 / A100] |
| Trajectories | [N] |
| Binder length | [65-150] aa |
| Random seed | [42] |

Optional second generator: RFdiffusion (diversity pool), ranked jointly with BindCraft outputs.

## 4. Filtering and ranking

Designs were filtered using:

1. **BindCraft internal filters** (pLDDT, ipTM, clash, confidence)
2. **Post-hoc thresholds:** ipTM ≥ 0.50, pLDDT ≥ 80
3. **Rosetta cartesian_ddg** ≤ −30 REU (PyRosetta, where computed)
4. **Novelty:** Tanimoto / edit distance vs training set

Final ranking: ipTM (desc) → pLDDT (desc) → ΔΔG (asc).

## 5. Submission selection

Top [N ≤ 100] designs submitted in ranked order. Each sequence ≤250 aa, de novo (no motif scaffolding).

## 6. Limitations

- All scoring is computational; no experimental validation prior to submission.
- AutoDock/Vina or RFdiffusion-only pipelines were not used for final selection.
- [Add target-specific caveats]

## References

- Pacesa M. et al. One-shot design of functional protein binders with BindCraft. Nature 2025. doi:10.1038/s41586-025-09429-6
- Sappington et al. Nat Commun 2026 (ΔΔG filter threshold)

---

*Replace bracketed fields before submission. Export to PDF ≤2 pages.*
