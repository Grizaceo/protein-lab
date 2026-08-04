# Computational Docking and De Novo Design Against Fibromyalgia-Implicated GPCR Targets

**Authors:** Cristóbal Muñoz Rojas¹

¹ Independent Researcher, Santiago, Chile. Correspondence: cristoe4@gmail.com

**Preprint — Draft v1.1 — August 2026**

> ⚠️ **RETENIDO — NO SOMETER (2026-08-04).** Una auditoría de ligandos encontró que **10 de los 11 ligandos de referencia del campaign son moléculas incorrectas** (solo morfina es correcta): dopamina sin un hidroxilo, pramipexol y met-encefalina sin azufre, bromocriptina sin bromo, aprepitant sin flúor. Todos los ΔG de §3.1, §3.2 y §3.3 corresponden a compuestos distintos de los declarados. Con ligandos validados, aprepitant pasa de −3.2 a −10.12 kcal/mol y la "inversión de ranking" de §3.2 desaparece. Evidencia completa y alcance en `analisis/AUDITORIA_LIGANDOS_DOCKING_2026-08-04.md`. El manuscrito requiere re-correr el campaign antes de cualquier difusión. El paper 1 (transcriptómica) no está afectado.

---

## Abstract

Fibromyalgia (FM) is a chronic pain condition with a largely unknown peripheral molecular basis. A targeted reanalysis of public PBMC transcriptomics (GSE221921) identified elevation of the opioid/tachykinin neuropeptide axis — *TACR1* (NK1 receptor, d = +0.60), *OPRM1* (μ-opioid, d = +0.53), *TAC1* (Substance P, d = +0.47), *OPRK1* (κ-opioid, d = +0.38) — as the largest effect-size block in FM PBMCs. That block survives all five sex-adjusted sensitivity models but **not** adjustment for cell composition, and is therefore best read as a shift in circulating leukocyte populations rather than per-cell upregulation (companion transcriptomic manuscript, v2.8). These receptors nonetheless remain the GPCRs that FM transcriptomics and GWAS jointly implicate, and their structural tractability is a question independent of that compositional caveat. To probe the structural druggability of these targets and of the dopaminergic axis (*DRD2*, prioritized by FM GWAS), we performed a computational chemistry campaign: (i) molecular docking of known agonists/antagonists and endogenous ligands against *DRD2* (PDB 6VMS + AlphaFold), *TACR1* (AlphaFold), and *OPRM1* (AlphaFold); (ii) biophysical DRD2/DRD3 pocket mapping and de novo D2-selective candidate design; (iii) in silico docking validation of the de novo library; and (iv) an exploratory Transformer-based conditional generation pipeline. We show that AutoDock Vina + AlphaFold reproduces the qualitative ranking of reference agonists (bromocriptine > pramipexole > dopamine for DRD2; morphine > enkephalins for OPRM1) but fails to resolve fine potency differences between drug-like agonists (morphine vs fentanyl scored equivalently). These results were intended to establish a working docking pipeline for FM-implicated GPCRs and a structurally grounded, D3-excluding de novo candidate set. **A ligand audit conducted after this draft (see the notice above) found that 10 of the 11 reference ligands were incorrectly prepared, so the affinity values and rankings below do not yet support any conclusion about the pipeline's precision.** The campaign is being re-run with formula-validated ligands.

**Keywords:** fibromyalgia, DRD2, TACR1, OPRM1, molecular docking, AutoDock Vina, AlphaFold, de novo design, GPCR, neuropeptide axis

---

## 1. Introduction

The peripheral biology of fibromyalgia (FM) has been reframed by population-scale plasma proteomics (UK Biobank Olink) and targeted transcriptomic reanalysis. Two non-inflammatory axes dominate the FM peripheral signature (companion transcriptomic manuscript, v2.8): an extracellular-matrix / neurite-outgrowth module (COL9A1, PTN), which is the cell-intrinsic core — the only signal surviving sex stratification, Bonferroni correction and cell-composition adjustment simultaneously — and an opioid/tachykinin neuropeptide block (TACR1, OPRM1, TAC1, OPRK1) that is larger in effect size but compositional in origin, with CA14 as a direction-specific reference candidate. The dopaminergic axis (*DRD2*) is prioritized independently by FM GWAS (Kerrebijn et al., 2025) and shows robust PBMC upregulation.

The targets of this manuscript are the GPCRs of the second axis plus DRD2. That choice is deliberate and worth stating plainly: COL9A1 and PTN are the stronger transcriptomic signals, but they are a secreted collagen and a secreted growth factor — neither is a small-molecule GPCR target, so neither is addressable by the docking campaign reported here. The compositional caveat weakens the *biological* case for OPRM1/TACR1 as FM drug targets, but does not change whether these receptors are structurally tractable, which is the question this manuscript actually answers.

The translational question is whether these targets are structurally tractable for small-molecule intervention. FM has a 21-year gap of non-replicated positive dopamine-agonist trials, driven in part by severe mesolimbic tolerability barriers of D2/D3 agonists (Impulse Control Disorders, DAWS). A D3-excluding, centrally active dopaminergic agent would be the intellectually interesting design goal. Meanwhile, NK1 (TACR1) antagonists failed FM pain trials, and chronic opioid exposure is discouraged in FM guidelines — so OPRM1 repurposing is contra-indicated.

This manuscript reports a computational chemistry campaign to (1) validate a docking pipeline against FM-implicated GPCRs using known ligands, (2) map the DRD2/DRD3 selectivity determinants, (3) design D2-selective de novo candidates, and (4) explore generative chemistry. We treat all results as structural plausibility, not thermodynamic quantification, and explicitly document where the method fails.

---

## 2. Methods

### 2.1 Receptor structures

- *DRD2*: PDB 6VMS (cryo-EM, 3.8 Å, active-state, chain R) and AlphaFold model P14416 (pLDDT 72.4).
- *TACR1* (NK1): AlphaFold model P25103 (pLDDT 78.4) — no experimental human structure with bound ligand available.
- *OPRM1* (μ-opioid): AlphaFold model P35372 (pLDDT 76.6) — no experimental human structure available.

PDBQT preparation used Open Babel (`obabel`) with AutoDock Tools atom types; receptor partial charges were assigned by the Vina/AD4 default (no ADFR suite). Protein structures were held rigid; ligands were optimized with MMFF94 (RDKit) and prepared with Meeko.

### 2.2 Docking

AutoDock Vina v1.2.5. Search box centered on the orthosteric pocket: DRD2 [109.4, 124.7, 100.4] Å, 22×22×22 Å; TACR1 and OPRM1 boxes centered on literature-derived pocket residues (see §3). Exhaustiveness default (8) unless noted. Affinity (ΔG, kcal/mol) converted to Ki via the standard Vina relation Ki = exp(ΔG·1000/(R·T)) at 298 K.

### 2.3 De novo design

A combinatorial library was screened through a dual 2D QSAR regressor trained on 176 selective DRD2/DRD3 compounds mined from ChEMBL, with RDKit PAINS and Ertl–Schuffenhauer SA-score filters. Selectivity was predicted as Ki(DRD3)/Ki(DRD2). CNS MPO score integrated six physicochemical properties with a basic-amine pKa estimate (~9.5).

### 2.4 Generative chemistry

A conditional Transformer encoder–decoder was trained on the ChEMBL selective dataset (176 compounds) augmented 30× via SMILES enumeration (5,970 samples), conditioned on high D2/D3 selectivity. Generated SMILES were filtered through a 4-level cascade (sanitization/Lipinski/QED → PAINS/SA → QSAR/novelty → CNS MPO consensus).

---

## 3. Results

### 3.1 DRD2 docking (P0)

| Ligando | 6VMS ΔG (kcal/mol) | AF ΔG | 6VMS Ki (µM) | AF Ki (µM) |
|---------|--------------------|-------|--------------|------------|
| Dopamina | -5.4 | -5.7 | 111 | 71 |
| Pramipexole | -8.0 | -6.8 | 1.4 | 9.9 |
| Bromocriptine | -9.4 | -8.1 | 0.13 | 1.1 |

**Ranking preserved** across both structures (bromocriptine > pramipexole > dopamine), validating the orthosteric pocket identification. The pocket was anchored by the crystallographic ligand 08Y (6VMS chain R); key AlphaFold residues D114, S193, S197, F389, F390, S419, N422. AlphaFold systematically under-scores strong agonists by +1.2 to +1.3 kcal/mol (no induced fit), but is usable for ranking.

### 3.2 TACR1 docking (P1)

| Ligando | ΔG (kcal/mol) | Ki (µM) |
|---------|---------------|---------|
| Rolapitant | -6.7 | 12.3 |
| Substance P (1–4 fragment) | -5.3 | 138 |
| Aprepitant | -3.2 | 4398 |

Pocket residues (Ballesteros–Weinstein): D78, Y92, T205, Y272, F288, N305. **Ranking partially inverted** vs experiment: rolapitant scored better than aprepitant, whereas experimental aprepitant (Ki ~0.1–1 nM) is the higher-affinity NK1 antagonist. Causes: (1) receptor PDBQT lacks AD4 partial charges; (2) aprepitant is highly flexible (4 stereocenters); (3) AlphaFold apo state misses antagonist-stabilized induced fit. This establishes a precision limit for flexible antagonists under rigid docking.

### 3.3 OPRM1 docking (P2)

| Ligando | Rot. bonds | ΔG (kcal/mol) | Ki (µM) | Lit. Ki (nM) | Error |
|---------|-----------:|---------------|---------|--------------|-------|
| **Naloxone** (antagonist) | 2 | **-9.44** | **0.12** | 1–10 | **~12–120×** |
| Morphine | 0 | -8.7 | 0.40 | 10–100 | 4–40× |
| Fentanyl | 6 | -8.5 | 0.55 | 1–10 | 55–550× |
| Met-enkephalin | peptide | -7.9 | 1.55 | 50–500 | 3–30× |
| Leu-enkephalin | peptide | -7.6 | 2.67 | 100–1000 | 3–27× |

Pocket residues: S147, V293, T296, P297, H299, I300, K305. **Ranking preserved** among agonists: morphine > fentanyl (Vina cannot resolve their ~100× in vivo potency difference — a pharmacokinetic and efficacy effect, not binding) and met-enkephalin > leu-enkephalin (matches literature).

**Naloxone correction (2026-08-04).** An earlier version of this manuscript reported that naloxone "failed to dock (SMILES/parsing issue, low exhaustiveness)". That was a misreading: the message emitted was `WARNING: At low exhaustiveness, it may be impossible to utilize all CPUs` — a CPU-utilization notice, not a docking failure. The original run had completed and written valid poses. Re-docking with a formula-validated ligand (PubChem CID 5284596; C19H21NO4, MW 327.38; MMFF94/RDKit) in the same box gives ΔG = **−9.446 at exhaustiveness 8 and −9.444 at exhaustiveness 32** — fully converged. Naloxone is the **best-scoring ligand of the OPRM1 set** and the only one whose predicted Ki approaches its experimental range.

### 3.4 DRD2/DRD3 pocket mapping and de novo selectivity

Alignment of DRD2 (6VMS) and DRD3 (3PBL) active conformations reveals three selectivity determinants at the secondary binding pocket (SBP) / ECL2:

1. **Electrostatic/Polar flip** — DRD2 Ser163 (H-bond donor) vs DRD3 Ala161 (hydrophobic). Penalizes polar ligand extensions in DRD3.
2. **Hydrophobic/Steric switch** — DRD2 Ile183 (bulky) vs DRD3 Ser182 (polar). Favors rigid hydrophobic spacers in DRD2.
3. **Conformational gate** — DRD2 ECL2 rotates outward (wide SBP); DRD3 ECL2 is rigid/inward (narrow gate). Bulky rigidified scaffolds clash at DRD3.

Extending the pramipexole tetrahydrobenzothiazole core into the DRD2 SBP multiplies predicted subtype selectivity up to ~8.6× vs control.

### 3.5 De novo docking validation

Top 8 de novo candidates (Table 6) were docked against DRD2/DRD3. All poses anchored at the conserved aspartate (Asp114/Asp110, <3.6 Å). ΔΔG (DRD2−DRD3) ranged −0.05 to +0.47 kcal/mol — within Vina's ±2.85 kcal/mol intrinsic error (Trott & Olson, 2010), so differences are qualitative trends, not quantified selectivity. The directional shift (pramipexole ΔΔG = +0.45 → candidates ≤0.00) is consistent with the design hypothesis of DRD2 preference.

### 3.6 Transformer generative chemistry

460 unique molecules generated; 11 passed the 4-level cascade. Top candidates achieved CNS MPO 4.12–4.75 (BBB-viable), predicted D2/D3 selectivity 21–38×, and Tanimoto novelty ≤0.18 vs training set. Strictly an exploratory proof-of-concept: no synthesis or experimental profiling performed.

---

## 4. Discussion

### 4.1 What the pipeline can and cannot do

The AutoDock Vina + AlphaFold pipeline is **fit for purpose as a ranking/screening filter** but not for absolute affinity or fine potency. It correctly orders reference agonists within a chemotype (bromocriptine > pramipexole > dopamine; morphine > enkephalins) and preserves known qualitative trends. It cannot separate drug-like agonists of similar physicochemistry (morphine ≈ fentanyl).

**Precision limits — not yet established.** An earlier version of this section argued that the pipeline's failure mode is ligand flexibility rather than pharmacological class, using aprepitant (scored −3.2) as the anchor. The ligand audit of 2026-08-04 invalidated that argument: the aprepitant used was not aprepitant (C26H33NO6, no fluorine, versus C23H21F7N4O3), and a formula-validated aprepitant scores −10.12 in the same box — a ~2–3 kcal/mol deviation from experiment rather than ~9, which is within Vina's ordinary error. The flexibility hypothesis may still hold, but it has no supporting data at present and is withdrawn pending the re-run. See `analisis/AUDITORIA_LIGANDOS_DOCKING_2026-08-04.md`.

One diagnostic from that audit is worth carrying into the re-run: the mis-prepared aprepitant produced nine binding modes of which **eight had positive affinity** (+0.35 to +4.05 kcal/mol, i.e. steric clash), whereas the validated ligand produces nine modes all negative (−10.12 to −6.47). A run whose modes are mostly positive is a signature of a malformed ligand and should be treated as a failure, not a result.

### 4.2 FM relevance and the tolerability wall

The transcriptomic companion shows the opioid axis is robust to sex adjustment but **confounded by cell composition**: no axis gene survives adjustment for estimated leukocyte fractions across the four deconvolution implementations tested (OPRM1 and TACR1 are borderline, significant under 2 of 4; TAC1, PENK, OPRK1, OPRD1 and POMC fail under all four). The adjustment is a genuine filter rather than a procedure that removes all signal — a 600-gene negative control shows 28% of sex-adjusted case effects survive it — and COL9A1/PTN do survive, so the axis result is a real negative, not an artifact. Medication exposure compounds this: FM patients use opioids chronically, which regulates opioid receptor expression and may itself alter leukocyte composition. Combined with ACR 2025 guidelines discouraging opioids in FM, OPRM1 is a poor repurposing target. DRD2 remains the genetically prioritized axis, but its peripheral expression is low and compartment-specific; the strongest unconfounded evidence is germline sQTL (companion §4.4, footnote), not PBMC mRNA. The de novo D2-selective, D3-excluding design is the one avenue that addresses the tolerability wall directly — but requires FEP/TI or radioligand validation before any inference.

### 4.3 Limitations

1. Receptor PDBQT without ADFR partial charges; absolute scores approximate, ranking reliable.
2. 6VMS is cryo-EM 3.8 Å; TACR1/OPRM1 are AlphaFold apo models (no experimental ligand-bound structure).
3. Rigid docking; no induced fit (AlphaFold 3 / Protenix would address this).
4. No solvation; Vina simplified scoring.
5. De novo and Transformer outputs unscaffolded experimentally.

---

## 5. Conclusion

A reproducible computational docking pipeline for FM-implicated GPCRs (DRD2, TACR1, OPRM1) is established and its precision limits honestly characterized. The pipeline supports qualitative screening and structurally grounded de novo design (D2-selective, D3-excluding candidates), but absolute affinity and antagonist potency require FEP/TI or experimental validation. The FM-relevant translational signal is weak for OPRM1 (confound + guidelines) and indirect for DRD2 (germline, not peripheral); the docking campaign is therefore a methodological foundation, not a drug lead.

---

## References

Chen, L., et al. (2025). Diagnosis, Prognosis, and Drug Target Discovery for Chronic Widespread Pain. *Adv Sci*. PMID: 41025730.

Kerrebijn, I., et al. (2025). The genetic architecture of fibromyalgia across 2.5 million individuals. *medRxiv*. PMID: 41001472.

Trott, O., & Olson, A.J. (2010). AutoDock Vina: improving the speed and accuracy of docking. *J Comput Chem*, 31(2), 455–461. PMID: 19499576.

Muñoz Rojas, C. (2026). *Peripheral Neuroimmune and Nociceptive Gene Signatures in Fibromyalgia: A Targeted Reanalysis of Public Transcriptomic Cohorts Informed by UK Biobank Plasma Proteomics* (companion transcriptomic manuscript, v2.8).

---

## Data & Code Availability

All artifacts are at [github.com/Grizaceo/protein-lab](https://github.com/Grizaceo/protein-lab) under `investigacion-fibromialgia/`. This directory (`docking_fm_targets/`) holds the manuscript only; the code, structures and results live in the paths below.

**Receptor models** — `estructuras/alphafold/`: `DRD2_P14416.pdbqt`, `TACR1_P25103.pdbqt`, `OPRM1_P35372.pdbqt`, each with `_metadata.json` (pLDDT) and `_pae.json`. Experimental DRD2: `estructuras/drd2_receptor_6VMS.pdbqt`.

**Docked poses and Vina logs** — `estructuras/dockings/`: 14 output PDBQTs plus 4 Vina logs, covering dopamine, pramipexole and bromocriptine (DRD2, both 6VMS and AlphaFold), rolapitant, aprepitant and the Substance P 1–4 fragment (TACR1), and morphine, fentanyl, met-/leu-enkephalin and naloxone (OPRM1). The naloxone re-docking of §3.3 adds `naloxone_OPRM1_rerun_exh32_docked.pdbqt`, its full Vina log, and the validated ligand (`naloxone_ligand_rdkit_mmff94.sdf`); the original run is retained as `naloxone_OPRM1_docked.pdbqt` for comparison.

**Per-target result reports** — `analisis/P0_DRD2_DOCKING_RESULTADOS.md`, `P1_TACR1_DOCKING_RESULTADOS.md`, `P2_OPRM1_DOCKING_RESULTADOS.md`.

**Scripts** — `scripts/`: `analyze_docking_drd2.py`, `dock_validation.py`, `pocket_analysis.py`, `run_denovo_docking.py`, `train_qsar_selectivity.py`, `train_transformer.py`, `transformer_selective_generator.py`, `predict_admet_bbb.py`.

**Not included:** intermediate ligand preparation files (`datos/pdb/`) and exploratory docking runs (`docking_runs/`) are gitignored as bulk intermediates; every result reported in §3 is reproducible from the tracked receptor PDBQTs, the ligand SMILES listed in the P0/P1/P2 reports, and the scripts above.

## Conflict of Interest

The author declares no conflicts of interest.
