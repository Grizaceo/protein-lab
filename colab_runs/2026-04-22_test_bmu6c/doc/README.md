# Colab Run: test_bmu6c

## Source
- **Notebook URL**: Google Colab (RFdiffusion + ProteinMPNN)
- **Date**: 2026-04-22
- **Local archive**: `~/.hermes/workspace/protein-lab/colab_runs/2026-04-22_test_bmu6c/`

## Why Colab
Local RTX 4060 8GB GPU cannot handle RFdiffusion structure generation / ProteinMPNN redesign at reasonable speed. Execution was offloaded to Google Colab GPU runtime.

## Config Recovered from `.trb`
- **Input PDB**: `1qys.pdb`
- **Contig**: `100-100` (scaffold / unconstrained de novo, 100 aa)
- **Num designs**: 1
- **Final step (diffusion)**: `T=1` (early-stop / reduced noise trajectory)
- **Trajectory**: written (two trajectory files extracted, ~2.4 MB total)
- **Model**: Base_ckpt.pt (RFdiffusion base model)

## Outputs
- **Total designs**: 1 design × 8 MPNN sequences = 8 candidates
- **PDB structures**: `best.pdb`, `best_design0.pdb`, plus 7 `_n0`..`_n7` variants in `all_pdb/`
- **MPNN results**: `mpnn_results.csv`

## Metrics Summary

| Metric     | Mean   | Best    | Baseline (mean) | Delta vs Baseline |
|------------|--------|---------|-------------------|-------------------|
| pLDDT      | 0.895  | 0.936   | 0.909             | -0.014            |
| pTM        | 0.677  | 0.764   | 0.741             | -0.064            |
| PAE        | 5.649  | 3.924   | 3.939             | +1.710            |
| RMSD       | 0.844  | 0.681   | 0.609             | +0.235            |
| MPNN       | 1.134  | 1.079   | 0.967             | +0.167            |

### Best Candidate
- **design0_n2**: pLDDT = 0.936, pTM = 0.764, PAE = 3.924, RMSD = 0.817

## Interpretation
- **Structural quality declined vs baseline** on every aggregate metric except individual best pLDDT (0.936 is good, but the mean pLDDT is lower).
- Mean PAE jumped from ~3.9 to ~5.6, indicating increased positional uncertainty across candidates.
- RMSD increased from 0.609 to 0.844, suggesting the redesign ensemble is more structurally dispersed.
- MPNN scores are worse (higher = worse in this metric); baseline was ~0.967, this run is ~1.134.
- This run is **not promoted** to the new baseline. Baseline remains `2026-04-22_diffusion_test`.
- Best individual candidate `design0_n2` is viable but does not justify a shift since baseline had competitive candidates and better aggregates.

## Recommended Next Colab Action
- Lock notebook parameters and seed explicitly to estimate variance.
- If repeated runs yield similarly worse aggregates, investigate if `1qys` as a scaffold / `100-100` contig is the source of quality drift vs the baseline scaffold.
