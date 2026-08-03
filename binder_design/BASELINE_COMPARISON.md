# Baseline comparison — RFdiffusion vs BindCraft

**Target:** Nipah G (2VSM chain A)  
**Updated:** 2026-07-04

## Old pipeline (FAILED)

| Property | Value |
|----------|-------|
| Method | RFdiffusion + ProteinMPNN + AF2 multimer (Colab T4) |
| Runs | 11 iterations (`colab_runs/INDEX.md`) |
| Best ipTM | **0.16–0.18** |
| Best pAE (complex) | ~27.8 Å |
| pLDDT binder | ✅ > 0.85 (high confidence misfolds) |
| Threshold needed | ipTM > 0.50 |
| Verdict | **Failed** — confident but non-binding designs |

## New pipeline (VALIDATION PENDING)

| Property | Value |
|----------|-------|
| Method | BindCraft (integrated AF2 hallucination + MPNN + filters) |
| Reference | Nature 2025, avg 46% experimental success |
| Runs | 0 completed (infrastructure ready) |
| Target | Same Nipah G, minimal/full PDB prepared |
| Success criterion | ipTM > 0.50 (any design) |

## Why the old pipeline failed

1. **AF2 vanilla ipTM is a weak filter** — high pLDDT + catastrophic pAE (~28 Å) = confident misfold.
2. **No integrated scoring during generation** — RFdiffusion proposes geometry; AF2 scores after the fact.
3. **Missing Rosetta ΔΔG filter** — without ddg < −30 REU, wet-lab success drops ~9% → ~1% (Sappington 2026).
4. **Manual Colab loop** — many runs never got complex scoring (ipTM null in ITERATION_STATE.json).

## What BindCraft adds

- Joint optimization of structure + sequence during hallucination
- Internal filters before "Accepted" output
- State-of-the-art on competition targets (won EGFR competition designs)

## Comparison table (fill after first BindCraft run)

| Run ID | Trajectories | Accepted | Best ipTM | Passed filter | Date |
|--------|-------------|----------|-----------|---------------|------|
| bindcraft_nipah_smoke_001 | — | — | — | — | pending |
| RFdiffusion baseline | 11 iter | 64+ designs | 0.16 | 0 | 2026-04 |

## Public benchmark (Nipah competition)

- Adaptyv Nipah competition: ~9.3% experimental hit rate
- Best binder: KD 370 pM
- Our goal: reach ipTM > 0.5 in silico first, then submit when competition opens
