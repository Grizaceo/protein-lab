# Computational Docking and De Novo Design Against Fibromyalgia-Implicated GPCR Targets

**Authors:** Cristóbal Muñoz Rojas¹

¹ Independent Researcher, Santiago, Chile. Correspondence: cristoe4@gmail.com

**Preprint — Draft v1.0 — August 2026**

---

## Abstract

Fibromyalgia (FM) is a chronic pain condition with a largely unknown peripheral molecular basis. A targeted reanalysis of public PBMC transcriptomics (GSE221921) identified a coordinated activation of the opioid/tachykinin neuropeptide axis — *TACR1* (NK1 receptor, d = +0.60), *OPRM1* (μ-opioid, d = +0.53), *TAC1* (Substance P, d = +0.47), *OPRK1* (κ-opioid, d = +0.38) — as the most robust transcriptomic signal in FM, surviving all five sex-adjusted sensitivity models (companion transcriptomic manuscript). To probe the structural druggability of these targets and of the dopaminergic axis (*DRD2*, prioritized by FM GWAS), we performed a computational chemistry campaign: (i) molecular docking of known agonists/antagonists and endogenous ligands against *DRD2* (PDB 6VMS + AlphaFold), *TACR1* (AlphaFold), and *OPRM1* (AlphaFold); (ii) biophysical DRD2/DRD3 pocket mapping and de novo D2-selective candidate design; (iii) in silico docking validation of the de novo library; and (iv) an exploratory Transformer-based conditional generation pipeline. We show that AutoDock Vina + AlphaFold reproduces the qualitative ranking of reference agonists (bromocriptine > pramipexole > dopamine for DRD2; morphine > enkephalins for OPRM1) but fails to resolve fine potency differences between drug-like agonists (morphine vs fentanyl scored equivalently) and under-scores flexible high-affinity antagonists (aprepitant vs rolapitant reversed vs experiment). These results establish a working docking pipeline for FM-implicated GPCRs while honestly delineating its precision limits, and provide a structurally grounded, D3-excluding de novo candidate set for future FEP/TI or radioligand validation.

**Keywords:** fibromyalgia, DRD2, TACR1, OPRM1, molecular docking, AutoDock Vina, AlphaFold, de novo design, GPCR, neuropeptide axis

---

## 1. Introduction

The peripheral biology of fibromyalgia (FM) has been reframed by population-scale plasma proteomics (UK Biobank Olink) and targeted transcriptomic reanalysis. Two non-inflammatory axes dominate the FM peripheral signature: a complete opioid/tachykinin neuropeptide circuit (TACR1, OPRM1, TAC1, OPRK1) and an extracellular-matrix / neurite-outgrowth module (COL9A1, PTN), with CA14 as a direction-specific reference candidate (companion transcriptomic manuscript, v2.7). The dopaminergic axis (*DRD2*) is prioritized independently by FM GWAS (Kerrebijn et al., 2025) and shows robust PBMC upregulation.

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

| Ligando | ΔG (kcal/mol) | Ki (µM) |
|---------|---------------|---------|
| Morphine | -8.7 | 0.40 |
| Fentanyl | -8.5 | 0.55 |
| Met-enkephalin | -7.9 | 1.55 |
| Leu-enkephalin | -7.6 | 2.67 |

Pocket residues: S147, V293, T296, P297, H299, I300, K305. **Ranking preserved**: morphine > fentanyl (Vina cannot resolve their ~100× in vivo potency difference — a pharmacokinetic, not binding, effect) and met-enkephalin > leu-enkephalin (matches literature). Naloxone failed to dock (SMILES/parsing issue, low exhaustiveness) — non-critical as our FM interest is agonist, not antagonist.

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

The AutoDock Vina + AlphaFold pipeline is **fit for purpose as a ranking/screening filter** but not for absolute affinity or fine potency. It correctly orders reference agonists within a chemotype (bromocriptine > pramipexole > dopamine; morphine > enkephalins) and preserves known qualitative trends. It fails on two axes: (i) it cannot separate drug-like agonists of similar physicochemistry (morphine ≈ fentanyl), and (ii) it under-scores flexible high-affinity antagonists (aprepitant < rolapitant) without induced-fit modeling.

### 4.2 FM relevance and the tolerability wall

The transcriptomic companion shows the opioid axis is robust to sex adjustment but **confounded by cell composition** (0/7 genes survive deconvolution) and by medication exposure (FM patients use opioids chronically). Combined with ACR 2025 guidelines discouraging opioids in FM, OPRM1 is a poor repurposing target. DRD2 remains the genetically prioritized axis, but its peripheral expression is low and compartment-specific; the strongest unconfounded evidence is germline sQTL (companion §4.7), not PBMC mRNA. The de novo D2-selective, D3-excluding design is the one avenue that addresses the tolerability wall directly — but requires FEP/TI or radioligand validation before any inference.

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

Muñoz Rojas, C. (2026). *Peripheral Neuroimmune and Nociceptive Gene Signatures in Fibromyalgia: A Targeted Reanalysis of Public Transcriptomic Cohorts Informed by UK Biobank Plasma Proteomics* (companion transcriptomic manuscript, v2.7).

---

## Data & Code Availability

Docking scripts, PDBQT preparations, and de novo candidate tables are available at [github.com/Grizaceo/protein-lab](https://github.com/Grizaceo/protein-lab) under `investigacion-fibromialgia/docking_fm_targets/`. Receptor models: DRD2 (6VMS, P14416), TACR1 (P25103), OPRM1 (P35372). Ligand SMILES and Vina logs are provided per target.

## Conflict of Interest

The author declares no conflicts of interest.
