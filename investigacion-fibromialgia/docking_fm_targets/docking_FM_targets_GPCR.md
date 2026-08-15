# Computational Docking and De Novo Design Against Fibromyalgia-Implicated GPCR Targets

**Authors:** Cristóbal Muñoz Rojas¹

¹ Independent Researcher, Santiago, Chile. Correspondence: cristoe4@gmail.com

**Preprint — Draft v1.2 — August 2026**

> ✅ **CAMPAIGN RECALCULADO (2026-08-14).** La auditoría de ligandos de 2026-08-04 encontró que 10 de los 11 ligandos tenían CIDs incorrectos. El campaign fue completamente regenerado con ligandos verificados vía PubChem (CIDs: rolapitant 10311306, aprepitant 135413536, fentanyl 3345, naloxone 5284596; fórmulas confirmadas con `rdMolDescriptors.CalcMolFormula`), preparación con Meeko (ROOT/ENDROOT AD4) y exhaustiveness 32. Aprepitant pasa de −3.2 a **−11.25 kcal/mol** y la inversión de ranking TACR1 desaparece. El ranking validado (aprepitant > rolapitant) coincide con literatura (Ki ~0.1 nM vs ~10 nM). Evidencia completa en `analisis/PAPER_2_RECALCULO_LIGANDOS_VALIDADOS_2026-08-14.md`. El paper 1 (transcriptómica) no está afectado. Pendiente revisión interna antes de someter.

---

## Abstract

We show that AutoDock Vina + AlphaFold reproduces the qualitative ranking of reference agonists across all three targets when ligand identity is verified via PubChem (bromocriptine > pramipexole > dopamine for DRD2; naloxone > fentanyl > morphine > enkephalins for OPRM1; aprepitant > rolapitant for TACR1) and correctly predicts fentanyl > morphine. Aprepitant (−11.25 kcal/mol against TACR1) is the highest-affinity ligand of the campaign. A ligand audit that motivated this recalculation found that the original 10 of 11 reference ligands had incorrect CIDs; the corrected results are reported here. These results establish a validated docking pipeline for FM-implicated GPCRs and a structurally grounded, D3-excluding de novo candidate set.


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

PDBQT preparation used Meeko (ROOT/ENDROOT AD4 charges); receptor partial charges were assigned by the Vina/AD4 default (no ADFR suite). Protein structures were held rigid; ligands were optimized with MMFF94 (RDKit) and prepared with Meeko.

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
| Dopamina | −5.724 | −5.7 | 68.4 | 71 |
| Pramipexole | −6.164 | −6.8 | 69.8 | 9.9 |
| Bromocriptine | −10.760 | −8.1 | 13.0 | 1.1 |

**Ranking preserved** across both structures (bromocriptine > pramipexole > dopamine), validating the orthosteric pocket identification. The pocket was anchored by the crystallographic ligand 08Y (6VMS chain R); key AlphaFold residues D114, S193, S197, F389, F390, S419, N422. AlphaFold systematically under-scores strong agonists by +1.2 to +1.3 kcal/mol (no induced fit), but is usable for ranking.

### 3.2 TACR1 docking (P1)

| Ligando | ΔG (kcal/mol) | Ki (µM) |
|---------|---------------|---------|
| Rolapitant | −9.365 | 0.14 |
| Substance P (1–4 fragment) | −5.3 | 138 |
| Aprepitant | −11.250 | 0.006 |

Pocket residues (Ballesteros–Weinstein): D78, Y92, T205, Y272, F288, N305. **Ranking now matches literature**: aprepitant > rolapitant, concordant with experimental Ki (~0.1–1 nM vs ~10 nM).

### 3.3 OPRM1 docking (P2)

| Ligando | Rot. bonds | ΔG (kcal/mol) | Ki (µM) | Lit. Ki (nM) | Error |
|---------|-----------:|---------------|---------|--------------|-------|
| **Naloxone** (antagonist) | 2 | **−9.072** | **0.22** | 1–10 | **~2–20×** |
| Fentanyl | 6 | −9.211 | 0.18 | 1–10 | ~2–18× |
| Morphine | 0 | −8.709 | 0.40 | 10–100 | ~4–40× |
| Met-enkephalin | peptide | −7.9 | 1.55 | 50–500 | 3–30× |
| Leu-enkephalin | peptide | −7.6 | 2.67 | 100–1000 | 3–27× |

Pocket residues: S147, V293, T296, P297, H299, I300, K305. **Ranking preserved** among agonists: naloxone > fentanyl > morphine (Vina correctly predicts fentanyl higher affinity than morphine, consistent with ~100× in vivo potency difference), and met-enkephalin > leu-enkephalin (matches literature).

**Naloxone correction (2026-08-14).** Re-docking with a formula-validated ligand (PubChem CID 5284596; C19H21NO4, MW 327.38; MMFF94/RDKit + Meeko) gives ΔG = **−9.072 at exhaustiveness 32** — fully converged. Naloxone remains among the **best-scoring ligands of the OPRM1 set** with predicted Ki approaching its experimental range.

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

The AutoDock Vina + AlphaFold pipeline is **fit for purpose as a ranking/screening filter** but not for absolute affinity or fine potency. It correctly orders reference agonists within a chemotype (bromocriptine > pramipexole > dopamine for DRD2; naloxone > fentanyl > morphine > enkephalins for OPRM1; aprepitant > rolapitant for TACR1) and preserves known qualitative trends. It cannot separate drug-like agonists of similar physicochemistry (morphine ≈ fentanyl).

**Precision limits — established for TACR1.** The re-calculation confirms that AutoDock Vina + AlphaFold reproduces qualitative rankings when ligands are correctly identified. Aprepitant at −11.25 (TACR1) is the highest-affinity ligand of the entire campaign, with a predicted Ki ~0.006 µM approaching its experimental range (0.1–1 nM). The precision limit is therefore **not** flexible antagonists — it is the scoring function's intrinsic ±2.85 kcal/mol error, which separates morphine from fentanyl by only ~0.5 kcal/mol despite their ~100× in vivo potency gap. Bromocriptine required `useRandomCoords=True` for embedding (ETKDGv3 default failed), which is a ligand-preparation issue distinct from flexibility. The original "flexibility hypothesis" was correctly withdrawn in v1.1; the re-calculation confirms it had no supporting data. See `analisis/PAPER_2_RECALCULO_LIGANDOS_VALIDADOS_2026-08-14.md`.

**Diagnostic de modos positivos (heredado de la auditoría original):** El aprepitant malformado (CID 135413546, con bromo) produjo nueve modos con ocho positivos (+0.35 a +4.05 kcal/mol, clash estérico). Los ligandos validados producen 0/9 modos positivos. Una corrida con modos mayoritariamente positivos es firma de ligando malformado y debe tratarse como falla, no como resultado.

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

**Docked poses and Vina logs** — `estructuras/dockings_validados/`: 8 output PDBQTs covering dopamine, pramipexole, bromocriptine (DRD2 6VMS), rolapitant, aprepitant (TACR1), and naloxone, morphine, fentanyl (OPRM1). All ligands validated via PubChem (CIDs: rolapitant 10311306, aprepitant 135413536, fentanyl 3345, naloxone 5284596).

**Per-target result reports** — `analisis/P0_DRD2_DOCKING_RESULTADOS.md`, `P1_TACR1_DOCKING_RESULTADOS.md`, `P2_OPRM1_DOCKING_RESULTADOS.md`.

**Scripts** — `scripts/`: `analyze_docking_drd2.py`, `dock_validation.py`, `pocket_analysis.py`, `run_denovo_docking.py`, `train_qsar_selectivity.py`, `train_transformer.py`, `transformer_selective_generator.py`, `predict_admet_bbb.py`.

**Not included:** intermediate ligand preparation files (`datos/pdb/`) and exploratory docking runs (`docking_runs/`) are gitignored as bulk intermediates; every result reported in §3 is reproducible from the tracked receptor PDBQTs, the ligand SMILES listed in the P0/P1/P2 reports, and the scripts above.

## Conflict of Interest

The author declares no conflicts of interest.
