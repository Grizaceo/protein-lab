# ColabDesign / RFdiffusion diffusion test

Source zip: `../test.result.zip`
Notebook reference: `https://colab.research.google.com/github/sokrypton/ColabDesign/blob/v1.1.1/rf/examples/diffusion.ipynb`

## Why this exists
This run was executed in Google Colab because the local RTX 4060 8GB setup is not sufficient for the required ColabDesign/RFdiffusion dependencies and runtime.

## What is inside
- `outputs/test/design.fasta` — 8 sequence candidates with metadata
- `outputs/test/mpnn_results.csv` — ProteinMPNN and structure scores
- `outputs/test/best.pdb` / `best_design0.pdb` — top backbone/model output
- `outputs/test/all_pdb/` — per-candidate PDBs
- `outputs/test_0.trb` — serialized run metadata/config
- `outputs/traj/` — trajectory PDBs

## Run config (from .trb)
- input_pdb: /content/RFdiffusion/inference/../examples/input_pdbs/1qys.pdb
- num_designs: 1
- design_startnum: 0
- radius: 10.0
- write_trajectory: True
- scaffold_guided: False
- align_motif: True
- symmetric_self_cond: True
- final_step: 1
- contigs: ['100-100']
- T: 50
- b_0: 0.01
- b_T: 0.07
- guide_scale: 10

## Result summary
- Number of designs: 8
- Best pLDDT: design 1 — 0.935
- Best ProteinMPNN: design 7 — 1.081
- Best pTM: design 1 — 0.792
- Lowest PAE: design 1 — 3.210
- Lowest RMSD: design 3 — 0.417

## Quick interpretation
- The run completed successfully and produced sane scores.
- The best balance is likely between design 1 (best pLDDT / pTM / PAE) and design 7 (best MPNN).
- This is a good baseline to reproduce or extend in Colab.

## Suggested next Colab step
1. Re-run the same notebook with the same target and seed to check reproducibility.
2. Then move to a target-driven binder/scaffold design setup instead of a generic diffusion test.
3. Keep the local 4060 out of the loop; use Colab as the execution environment.

## Key files
- `raw/outputs/test/design.fasta`
- `raw/outputs/test/mpnn_results.csv`
- `raw/outputs/test/best_design0.pdb`
- `raw/outputs/test_0.trb`
