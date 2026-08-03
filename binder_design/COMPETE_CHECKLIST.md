# Competition submission checklist

Use when a Proteinbase/Adaptyv competition opens.

## Before generating designs

- [ ] Confirm competition is **Open** (`python binder_design/scripts/monitor_competitions.py`)
- [ ] Read competition rules on proteinbase.com (target, de novo requirements, length limits)
- [ ] Download official target PDB/sequence from competition page
- [ ] Prepare trimmed target (`prepare_bindcraft_target.py` or equivalent for new target)

## Generation (BindCraft)

- [ ] Run ≥500 trajectories on Colab Pro A100 (or ≥200 on T4 with minimal target)
- [ ] Process output: `process_bindcraft_run.py`
- [ ] Filter: `filter_bindcraft_designs.py` (ipTM ≥0.5, pLDDT ≥80, ddg ≤−30 if available)
- [ ] Verify edit distance ≥25% vs UniRef50 (BindCraft novelty check or manual BLAST)
- [ ] Rank top ≤100 sequences by ipTM → pLDDT → DDG

## Submission package

- [ ] Method description ≤2 pages (`METHOD_DESCRIPTION_TEMPLATE.md`)
- [ ] Ranked FASTA or CSV per competition portal format
- [ ] Team name / author ID from registration
- [ ] Double-check: no motif scaffolding, no lead optimization (unless sdAb rules apply)

## Post-submission

- [ ] Archive run in `colab_runs/bindcraft_{target}_{date}/`
- [ ] Update `BASELINE_COMPARISON.md` with results
- [ ] Update `COMPETITION_STATUS.md`

## Monitor for next competition

- https://proteinbase.com/competitions
- Adaptyv blog / Twitter
- GEM Workshop announcements

Run weekly:

```bash
python binder_design/scripts/monitor_competitions.py
```
