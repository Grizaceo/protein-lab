# PROGRAM — Automated Lab: Fibromialgia Drug Repurposing

This is the master brief for the automated lab campaign. Inspired by autoresearch (Karpathy) and the SAIR Summit 2026 (Tunstall: automated lab loop, Tao: lanes for AI).

## Setup

The lab lives at `~/.hermes/workspace/protein-lab/automated_lab/`. 
The experiment data is under `../investigacion-fibromialgia/`.

## What we know

After the audit checkpoint (2026-05-13):
- 16 verified targets in 4 tiers, 4 PDB misassignments corrected
- GSE67311: CPA3/MS4A2/FCER1A/HDC DOWN → mastocito/basófilo signal
- ESM2: MOR is structural outlier (cos ~0.6 vs group ~0.9)
- MAMMAL DTI v2: naltrexona→MOR = 6.91 pKd (122 nM)

Two routes identified:
- **Ruta A** (mechanism): mast cell/IgG/peripheral
- **Ruta B** (repurposing): MOR/LDN

## What this campaign does

Each cycle:
1. Generate N experiments (drug×target combinations + variations)
2. Run MAMMAL DTI on each (local RTX 4060, ~0.2-5s)
3. Log results to `automated_lab/results/`
4. Report top findings

## What you CAN do

- Run `python -m automated_lab.engine.scheduler --campaign X --overnight Y`
- Modify campaign briefs in `automated_lab/campaign_briefs/`
- Add new drugs/SMILES to the idea generator
- Add new backends for Colab/Kaggle/Modal

## What you CANNOT do

- Run experiments on Nav1.8 (1956 aa, needs Colab)
- Modify `investigacion-fibromialgia/CHECKPOINT_AUDITADO_*.md` (ground truth)
- Run wet-lab experiments (obviously)

## The loop

```
LOOP:
  1. Load campaign brief
  2. Generate N experiments from targets × drugs
  3. For each: MAMMAL DTI → pKd
  4. Rank by pKd
  5. Log top-10 to report
  6. If overnight: continue until time budget exhausted
```

## NEUTER STOP

Once the campaign starts, do NOT ask the human if they want to continue.
The human might be asleep. Keep running until interrupted.

## Output format

Each run produces:
- `results/<campaign>_<timestamp>/cycle_XXX/<exp_id>.json` — individual results
- `results/<campaign>_<timestamp>/REPORTE_MANANA.md` — morning report
- `results/<campaign>_<timestamp>/SESSION.json` — session metadata
