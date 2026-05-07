# 2026-04-23_test_2vsm

- Notebook: https://colab.research.google.com/github/sokrypton/ColabDesign/blob/main/rf/examples/diffusion.ipynb
- Goal: binder design against Nipah G target using `2VSM_chainA_only.pdb` and hotspots near the ephrin-B2 interface.
- Why Colab: RFdiffusion/ProteinMPNN/AF validation exceed safe local workflow on RTX 4060 8GB.

## Recovered config
- input_pdb: `outputs/test/input.pdb`
- contigs: `A188-207/A211-603 90-90`
- hotspots: `A239,A241,A489,A491,A505,A558`
- T: 50
- num_designs: 8
- guide_scale: 10

## Key metrics (64 sequence validations)
- Mean pLDDT: 0.757
- Mean i_pTM: 0.160
- Mean i_PAE: 27.799
- Mean RMSD: 49.566
- Mean MPNN: 1.152

## Best observed values
- Best pLDDT: design 1 n=2 -> 0.915, i_pTM 0.155, i_PAE 27.767, RMSD 70.130
- Best interface metrics: design 5 n=1 -> i_pTM 0.192, i_PAE 26.675, RMSD 21.085, pLDDT 0.692
- Best MPNN: design 6 n=6 -> MPNN 1.029, pLDDT 0.856, i_pTM 0.163

## Interpretation
This run completed end-to-end, but interface validation is poor. The binder folds reasonably in some cases (pLDDT up to 0.915), yet AlphaFold does not support a stable target-binder complex:
- i_pTM is very low across the board (~0.16)
- i_PAE is very high (~28)
- RMSD is very large, meaning AF moved the binder far from the designed pose

Conclusion: this is not a validated binder hit. Treat as a negative/diagnostic run, not a candidate for promotion.

## Recommended next action
1. Do not promote any design from this run.
2. Retry with a tighter target patch / better interface conditioning.
3. Consider beta-strand interface conditioning or a more focused epitope instead of hotspot-only guidance.
4. If reusing anything, shortlist designs 3_n0, 1_n2, and 5_n1 only as diagnostic references.
