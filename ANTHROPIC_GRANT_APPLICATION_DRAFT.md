# Anthropic AI for Science — Rare Disease Research Grant Application Draft

**Deadline:** August 2, 2026, 11:59 PM PST
**Amount:** Up to $50,000 in Claude API credits over 6 months
**Track:** Track 1 (Basic Science)

---

## STRATEGY SUMMARY

**The pivot:** Reframe the existing fibromialgia pipeline as a proof-of-concept for a transferable agentic AI methodology, then propose applying it to specific rare diseases from Monarch's prioritized list using DisMech/Mondo resources.

**What we have (evidence of capability):**
1. Preprint v2.2 (Draft, May 2026) — GWAS-transcriptomic convergence in fibromialgia
2. Public repo: github.com/Grizaceo/protein-lab (DOI: 10.5281/zenodo.20250218)
3. agentic-lab-eac framework: github.com/Grizaceo/agentic-lab-eac (Apache-2.0)
4. Pipeline: transcriptomic reanalysis → molecular docking → de novo drug design (Transformer encoder-decoder)
5. Human-in-the-loop agentic methodology already documented in the preprint

**What we propose (the new work):**
Apply the same pipeline to 5 rare diseases from Monarch's prioritized list where:
- Public transcriptomic data exists (GEO)
- Drug targets are poorly characterized
- Mechanistic understanding is limited
- DisMech has gaps (diseases marked "absent" in curation candidates)

---

## TRACK SELECTION: Track 1 (Basic Science) — primary

**Rationale:** Track 1 fits our profile. We are an independent researcher (not a biotech startup), our pipeline is computational (not wet-lab), and the work produces mechanistic hypotheses and public datasets — exactly what Track 1 funds. The Monarch partnership (DisMech, Mondo) is Track 1's stated partner ecosystem.

**Secondary angle (Track 2):** The de novo drug design component (Transformer + docking + QSAR) could justify a Track 2 application for drug development, but Track 1 is the stronger fit given our current evidence.

---

## TARGET RARE DISEASES (preliminary selection from Monarch's 431 prioritized)

### Selection criteria:
1. Monarch priority list (initial-diseases.md)
2. DisMech status = "absent" (uncurated — maximum value contribution)
3. Public transcriptomic data available (GEO)
4. Known drug target gaps
5. Mechanistic convergence potential (shared pathways across diseases)

### Candidate diseases:

| Disease | MONDO ID | DisMech status | GEO datasets verified | Rationale |
|---------|----------|:---:|:---:|---|
| Hutchinson-Gilford progeria | MONDO:0008310 | secondary_only | GSE113957, GSE137083 (RNA-seq fibroblasts) | Rich transcriptomic data; aging/inflammation; lonafarnib alternatives |
| Neurofibromatosis type 1 | MONDO:0018975 | absent | GSE218493 + RNA-seq (Banerjee 2025) | NF1/RAS pathway; transcriptomic mechanisms poorly mapped |
| Fabry disease | MONDO:0010526 | absent | Kidney transcriptome (Delaleu 2023, Kidney Int) | Lysosomal storage; ETR-resistant targets; drug repurposing |
| Pitt-Hopkins syndrome | MONDO:0012589 | absent | GSE48367 (TCF4 study) | Ultra-rare neurodevelopmental; TCF4 haploinsufficiency |
| Myasthenia gravis | MONDO:0009688 | absent | GSE85452, GSE103974 | Autoimmune neurological; AChR/MuSK antibodies; thymus-mediated |

---

## DRAFT APPLICATION TEXT

### Project Title (100 chars max)

Agentic Transcriptomic Repurposing for Rare Diseases: From Fibromyalgia Proof-of-Concept to Monarch-Integrated Mechanistic Discovery

### Project Description / Abstract (500 words)

Fibromyalgia affects 2-4% of the global population, yet its molecular basis remains poorly defined. We developed an agentic AI pipeline — built with Claude and formalized in the open-source agentic-lab-eac framework — that combines (1) hypothesis-driven reanalysis of public transcriptomic cohorts, (2) molecular docking against structurally characterized targets, and (3) conditional Transformer-based de novo molecular generation for selective drug candidates. Applied to fibromyalgia, this pipeline identified robust convergence between GWAS-prioritized neural genes (DRD2, MDGA2) and transcriptomic alterations in PBMCs, produced structural insights into DRD2/DRD3 selectivity, and generated novel candidate scaffolds with predicted CNS penetration (preprint v2.2, DOI: 10.5281/zenodo.20250218).

We now propose to transfer this validated pipeline to rare genetic diseases, where the methodological gap is greatest and the potential impact is highest. Rare diseases affect 400 million people worldwide, yet mechanistic understanding is fragmented across 7,000+ conditions, each with small patient populations and limited datasets. The Monarch Initiative's DisMech knowledge base — curated with Claude Code — currently covers 1,298 disorders (2,051 subtypes), grounded in 21,000+ cited publications, but hundreds of prioritized rare diseases remain uncurated or have only secondary mechanistic entries.

Our project will:

1. **Select 5 rare diseases** from Monarch's prioritized list where transcriptomic data exists in GEO but mechanistic curation is absent in DisMech (Hutchinson-Gilford progeria, neurofibromatosis type 1, Fabry disease, Pitt-Hopkins syndrome, and myasthenia gravis).

2. **Apply the agentic pipeline** to each: hypothesis-driven transcriptomic reanalysis of public GEO datasets, target identification via Open Targets/AlphaFold profiling, and drug repurposing analysis against existing pharmacopeia.

3. **Generate mechanistic hypotheses** for DisMech contribution: structured YAML entries with ontology bindings (Mondo, HPO, MAXO), evidence snippets validated against PubMed abstracts, and pathograph networks.

4. **Cross-disease pattern detection**: Use Claude's reasoning to identify shared mechanistic pathways across the 5 diseases — the "mechanistic convergence" approach that is intractable with traditional single-disease studies but tractable with agentic AI.

5. **Deliverables**: 5 DisMech YAML entries submitted as PRs to monarch-initiative/dismech; a cross-disease mechanistic analysis preprint; open-source pipeline extensions in agentic-lab-eac for rare disease-specific workflows.

The $50,000 in Claude credits enables: large-scale literature synthesis across 5 disease domains (~$15K in inference), transcriptomic reanalysis with sensitivity models ($5K), molecular docking and de novo generation runs ($10K), cross-disease pattern synthesis and hypothesis generation ($10K), and DisMech curation with evidence validation ($10K). The 6-month timeline allows: Month 1-2 for disease selection and data acquisition, Month 3-4 for pipeline execution, Month 5-6 for synthesis, curation, and submission.

This project demonstrates that agentic AI can reshape our understanding of rare diseases by applying a validated, open-source, human-in-the-loop methodology to the exact gap that Monarch and Anthropic have identified: the mechanistic dark matter of rare disease biology.

### Novelty claim (what becomes possible with frontier AI that wasn't before)

Without frontier AI: rare disease research is stuck in single-disease silos. Each condition has ~1-5 published transcriptomic studies, manual literature review takes months per disease, and cross-disease mechanistic synthesis is intractable because no human team can read 5,000+ papers across 5 diseases and identify shared pathways.

With Claude: we can run the same hypothesis-driven pipeline across 5 rare diseases in 6 months, synthesize literature at scale, identify cross-disease mechanistic convergence, and produce DisMech-ready structured entries with automatically validated evidence. The pipeline is not "AI summarizing papers" — it's AI executing a rigorous, reproducible analytical workflow (transcriptomic statistics → structural biology → drug design) that would take a traditional lab 2-3 years per disease.

### Team / Qualifications

**Cristóbal Muñoz Rojas** — Independent researcher, Santiago, Chile. Affiliation: University of Chile, Faculty of Law (cristobal.munoz@derecho.uchile.cl). 

Demonstrated capability:
- Preprint: "GWAS-Prioritized Neural Genes Are Differentially Expressed in Fibromyalgia PBMCs" (v2.2, DOI: 10.5281/zenodo.20250218)
- Open-source framework: agentic-lab-eac (Apache-2.0, github.com/Grizaceo/agentic-lab-eac)
- Public repo: github.com/Grizaceo/protein-lab
- Full pipeline: transcriptomic reanalysis (Python, pandas, scipy, statsmodels), molecular docking (AutoDock Vina, RDKit), conditional Transformer generation (PyTorch), AlphaFold structural analysis, Open Targets profiling
- Human-in-the-loop agentic methodology: all claims validated against primary sources (GEO, PDB, ChEMBL, PubMed)

Note: While the applicant is formally affiliated with the Faculty of Law (not a traditional life sciences department), the research output demonstrates cross-disciplinary capability — the preprint is a rigorous computational biology study with verified methodology, public data, and reproducible code. This aligns with Anthropic's eligibility for "independent scientists."

### Data & Code Availability

- All transcriptomic data: public GEO datasets (GSE221921, GSE67311 for fibromyalgia proof-of-concept; GSE113957/GSE137083 for progeria, GSE218493 for NF1, GSE178947 for Fabry, GSE48367 for Pitt-Hopkins, GSE85452/GSE103974 for myasthenia gravis)
- Pipeline code: github.com/Grizaceo/protein-lab (MIT licensed), github.com/Grizaceo/agentic-lab-eac (Apache-2.0)
- DisMech contributions: PRs to github.com/monarch-initiative/dismech
- Preprint: DOI 10.5281/zenodo.20250218
- Software: Python 3.10, pandas, scipy, statsmodels, RDKit, AutoDock Vina, PyTorch

### Deliverables (6-month timeline)

| Month | Activity | Output |
|-------|----------|--------|
| 1 | Disease selection, GEO data acquisition, literature corpus building | 5 diseases selected, data downloaded, literature corpora ready |
| 2 | Transcriptomic reanalysis (sensitivity models per disease) | 5 sensitivity analysis tables, differentially expressed gene sets |
| 3 | Target profiling (AlphaFold, Open Targets), molecular docking | Target profiles, docking results, selectivity analyses |
| 4 | De novo drug generation (Transformer), cross-disease pattern synthesis | Candidate scaffolds, cross-disease mechanistic map |
| 5 | DisMech curation (YAML entries, evidence validation, ontology binding) | 5 DisMech PRs submitted |
| 6 | Preprint writing, pipeline extensions, community engagement | Preprint submitted to bioRxiv, agentic-lab-eac v2 release |

### Credit usage breakdown ($50,000)

| Activity | Credits | Justification |
|----------|--------:|--------------|
| Literature synthesis (5 diseases × ~500 papers each) | $15,000 | Large-batch Claude inference for literature corpus analysis, evidence extraction, DisMech YAML generation |
| Transcriptomic reanalysis orchestration | $5,000 | Claude Sonnet/Opus for pipeline orchestration, statistical interpretation, sensitivity model design |
| Molecular docking & de novo generation | $10,000 | Agentic workflows for structural analysis, QSAR model training, candidate filtering |
| Cross-disease mechanistic synthesis | $10,000 | High-volume reasoning across 5 disease datasets, pathway analysis, hypothesis generation |
| DisMech curation & evidence validation | $10,000 | Claude for YAML generation, PubMed evidence validation, ontology binding, PR preparation |

### Why this fits Anthropic's rare disease program

1. **Direct alignment with Monarch partnership**: We contribute to DisMech — Monarch's agent-friendly mechanistic classification library — using the same Claude Code-based curation workflow that Monarch already uses.

2. **Validated methodology, not a proposal**: The fibromialgia preprint proves the pipeline works. We're not proposing to build something; we're proposing to transfer something that works.

3. **Open-source by design**: agentic-lab-eac, protein-lab, and DisMech contributions are all open. Outputs go to public repositories.

4. **Independent researcher**: Aligns with Anthropic's explicit eligibility for "independent scientists" — a chronically underfunded group in rare disease research.

5. **Cross-disease synthesis**: The methodological novelty is using agentic AI to find shared mechanisms across rare diseases — exactly what Anthropic's announcement describes: "detect patterns across them" and "create shared terminology."

---

## NEXT STEPS

1. **Fill out the Google Form** (link below) with the project description above
2. **Polish the novelty claim** — tighten to 2-3 sentences max if the form has a short field
3. **Submit before August 2, 2026, 11:59 PM PST**

## APPLICATION LINK

https://docs.google.com/forms/d/e/1FAIpQLSfwDGfVg2lHJ0cc0oF_ilEnjvr_r4_paYi7VLlr5cLNXASdvA/viewform

## KEY REFERENCES

- Anthropic announcement: https://www.anthropic.com/news/rare-disease-research-grants
- Monarch DisMech: https://github.com/monarch-initiative/dismech
- Monarch prioritized diseases: https://raw.githubusercontent.com/monarch-initiative/dismech/main/initial-diseases.md
- Our preprint: DOI 10.5281/zenodo.20250218
- Our framework: github.com/Grizaceo/agentic-lab-eac