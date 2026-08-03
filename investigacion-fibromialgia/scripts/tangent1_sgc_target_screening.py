#!/usr/bin/env python3
"""
Tangente 1 - Phase 2: SGC & DRG Nociceptor Membrane Autoantigen Screening.
Profiles candidate surface autoantigens in Satellite Glial Cells (SGCs) and DRG Nociceptors
targeted by autoimmune IgG in Fibromyalgia.
"""

import os
import pathlib
import pandas as pd
import numpy as np

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / 'analisis' / 'tangente1'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Candidate Membrane Autoantigens
TARGET_CANDIDATES = [
    # --- Satellite Glial Cells (SGC) Targets ---
    {
        'gene_symbol': 'GJA1',
        'protein_name': 'Connexin-43 (Cx43)',
        'cell_type': 'Satellite Glial Cell (SGC)',
        'function': 'Gap junction channel coupling SGCs; releases ATP/glutamate during neuroinflammation',
        'subcellular': 'Plasma Membrane (Extracellular loops EL1 & EL2)',
        'autoimmunity_evidence': 'High (Cx43 autoantibodies implicated in neuropathic pain & autoimmune glial disease)',
        'uniprot_id': 'P17302',
        'topology': '4 TM domains, 2 Extracellular Loops (EL1: ~35 aa, EL2: ~45 aa)'
    },
    {
        'gene_symbol': 'KCNJ10',
        'protein_name': 'Kir4.1 Inward Rectifier K+ Channel',
        'cell_type': 'Satellite Glial Cell (SGC)',
        'function': 'Glial K+ buffering and resting membrane potential control in DRG SGCs',
        'subcellular': 'Plasma Membrane (Extracellular loop between TM1-TM2)',
        'autoimmunity_evidence': 'High (Validated autoantigen target in autoimmune CNS/PNS demyelination)',
        'uniprot_id': 'P78508',
        'topology': '2 TM domains, 1 Extracellular Pore Loop (~40 aa)'
    },
    {
        'gene_symbol': 'SLC1A3',
        'protein_name': 'EAAT1 / GLAST (Glutamate Transporter 1)',
        'cell_type': 'Satellite Glial Cell (SGC)',
        'function': 'Glutamate reuptake from DRG neuronal somata to prevent excitotoxicity',
        'subcellular': 'Plasma Membrane (Multiple extracellular loops)',
        'autoimmunity_evidence': 'Moderate (Glial transporter autoantibodies reported in encephalitis)',
        'uniprot_id': 'P43003',
        'topology': '8 TM domains, Extracellular Loops (EL2: ~80 aa)'
    },
    {
        'gene_symbol': 'NFASC',
        'protein_name': 'Neurofascin-155 (NF155)',
        'cell_type': 'Satellite Glial Cell / Paranodal Glia',
        'function': 'Glial-axonal cell adhesion molecule at paranodes and SGC-somatic contacts',
        'subcellular': 'Plasma Membrane (Large extracellular Ig & FnIII domains)',
        'autoimmunity_evidence': 'High (Established target of IgG4/IgG1 autoantibodies in CIDP & nodopathies)',
        'uniprot_id': 'O94856',
        'topology': 'Single-pass Type I, ~1000 aa Extracellular Ectodomain'
    },
    {
        'gene_symbol': 'CD40',
        'protein_name': 'CD40 TNF Receptor Superfamily Member 5',
        'cell_type': 'Glial & Immune Cells (SGC, B cells, Monocytes)',
        'function': 'Co-stimulatory immune-glial receptor; drives B-cell activation & autoantibody production',
        'subcellular': 'Plasma Membrane (Extracellular TNFR domains 1-4)',
        'autoimmunity_evidence': 'Very High (af Ekenstam 2026: CD40/CD40L & anti-SGC IgG elevated in FM)',
        'uniprot_id': 'P25942',
        'topology': 'Single-pass Type I, ~170 aa Extracellular Ectodomain'
    },
    # --- DRG Nociceptor Targets ---
    {
        'gene_symbol': 'SCN9A',
        'protein_name': 'NaV1.7 Voltage-Gated Sodium Channel',
        'cell_type': 'DRG C-fiber Nociceptor',
        'function': 'Primary action potential initiator in small-diameter nociceptive neurons',
        'subcellular': 'Plasma Membrane (Extracellular pore loops S5-S6 in domains I-IV)',
        'autoimmunity_evidence': 'High (Auto-IgG binding to NaV1.7 extracellular loops induces mechanical pain)',
        'uniprot_id': 'Q15858',
        'topology': '24 TM domains, 4 Extracellular Pore Loops'
    },
    {
        'gene_symbol': 'SCN10A',
        'protein_name': 'NaV1.8 Voltage-Gated Sodium Channel',
        'cell_type': 'DRG C-fiber Nociceptor',
        'function': 'Sustained action potential firing in nociceptors',
        'subcellular': 'Plasma Membrane (Extracellular loops)',
        'autoimmunity_evidence': 'Moderate (Involved in auto-IgG induced hyperexcitability)',
        'uniprot_id': 'Q9UI33',
        'topology': '24 TM domains, 4 Extracellular Pore Loops'
    },
    {
        'gene_symbol': 'TRPV1',
        'protein_name': 'TRPV1 Transient Receptor Potential Vanilloid 1',
        'cell_type': 'DRG Nociceptor',
        'function': 'Thermal & chemical nociception',
        'subcellular': 'Plasma Membrane (Extracellular pore loop S5-S6)',
        'autoimmunity_evidence': 'Moderate (Sensitized downstream of SGC/Mast cell IL-6 & tryptase)',
        'uniprot_id': 'Q8NER1',
        'topology': '6 TM domains, 1 Extracellular Pore Loop'
    },
    {
        'gene_symbol': 'MRGPRX2',
        'protein_name': 'Mas-Related G-Protein Coupled Receptor X2',
        'cell_type': 'Mast Cells (and DRG Sensory Neurons)',
        'function': 'Non-IgE receptor for basic secretagogues, substance P, and auto-IgG activation',
        'subcellular': 'Plasma Membrane (Extracellular N-term & ECL1-3)',
        'autoimmunity_evidence': 'High (Sanchez 2025 bioRxiv: IgG-FM engages MRGPRX2 to induce mast cell IL-6)',
        'uniprot_id': 'Q96LB1',
        'topology': '7 TM GPCR, 3 Extracellular Loops + N-terminus'
    }
]


def score_candidate(cand):
    """
    Compute Autoantigenic Potential Score (0 to 100):
    - Extracellular domain accessibility (30 pts)
    - Multimer / Cell surface expression (20 pts)
    - Glial / Nociceptor specificity (20 pts)
    - Literature autoantibody precedent in neuropathic/autoimmune disease (30 pts)
    """
    score = 0
    
    # Topology / Ectodomain
    if 'Single-pass' in cand['topology'] or 'Large extracellular' in cand['topology']:
        score += 30
    elif '24 TM' in cand['topology'] or '8 TM' in cand['topology']:
        score += 25
    else:
        score += 20
        
    # Cell surface
    if 'Plasma Membrane' in cand['subcellular']:
        score += 20
        
    # Specificity
    if 'Satellite Glial Cell' in cand['cell_type']:
        score += 20
    else:
        score += 15
        
    # Autoimmunity precedent
    if 'Very High' in cand['autoimmunity_evidence']:
        score += 30
    elif 'High' in cand['autoimmunity_evidence']:
        score += 25
    else:
        score += 15
        
    return score


def main():
    print("=" * 70)
    print("TANGENTE 1 - SGC & NOCICEPTOR MEMBRANE AUTOANTIGEN SCREENING")
    print("=" * 70)
    
    df = pd.DataFrame(TARGET_CANDIDATES)
    df['autoantigen_score'] = df.apply(score_candidate, axis=1)
    df = df.sort_values('autoantigen_score', ascending=False)
    
    print("\n--- Ranked Candidate Autoantigens ---")
    for idx, row in df.iterrows():
        print(f"[{row['autoantigen_score']}/100] {row['gene_symbol']} ({row['protein_name']})")
        print(f"  Cell Type: {row['cell_type']}")
        print(f"  Subcellular / Topology: {row['subcellular']} | {row['topology']}")
        print(f"  Evidence: {row['autoimmunity_evidence']}")
        print("-" * 70)
        
    df.to_csv(OUTPUT_DIR / 'sgc_nociceptor_autoantigen_screening.csv', index=False)
    print(f"\nSaved screening table to {OUTPUT_DIR / 'sgc_nociceptor_autoantigen_screening.csv'}")


if __name__ == '__main__':
    main()
