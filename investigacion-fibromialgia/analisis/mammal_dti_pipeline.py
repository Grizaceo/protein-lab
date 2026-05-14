#!/usr/bin/env python3
"""
MAMMAL DTI Pipeline — Fibromialgia
==================================
Usa MAMMAL fine-tuned para DTI (Drug-Target Interaction) para rankear
los fármacos small-molecule contra sus targets en fibromialgia.

Modelo: ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd
Task: Predicción de binding affinity (pKd) entre proteína + SMILES

Autor: DAVI + Cristóbal
Fecha: 2026-05-14
"""

import sys, os, json, time
import torch
import numpy as np
from fuse.data.tokenizers.modular_tokenizer.op import ModularTokenizerOp
from mammal.model import Mammal
from mammal.keys import *

# ─── CONFIG ────────────────────────────────────────────────
BASE_DIR = "/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia"
FASTA_FILE = f"{BASE_DIR}/datos/target_sequences.fasta"
OUTPUT_FILE = f"{BASE_DIR}/analisis/RESULTADOS_MAMMAL_DTI.json"

# ─── SMALL MOLECULE DRUGS (SMILES) ─────────────────────────
# Solo fármacos small-molecule. Biologics (anakinra, tocilizumab) no tienen SMILES.
DRUGS = {
    "naltrexona_LDN": {
        "smiles": "C=CCN1CCC23C4C(=O)CCC2(C1CC5=C3C(=C(C=C5)O)O4)O",
        "target": "MOR",
        "tier": "Tier2",
        "notes": "LDN (Low-Dose Naltrexone), antagonista MOR"
    },
    "dimetil_fumarato": {
        "smiles": "COC(=O)C=CC(=O)OC",
        "target": "NRF2",
        "tier": "Tier1",
        "notes": "Tecfidera, activador NRF2, FDA 2013"
    },
    "suzetrigine": {
        "smiles": "CC1=C(SC(=N1)NC(=O)C2=C(C=CC=C2F)F)C(=O)NCC(F)(F)F",
        "target": "Nav1.8",
        "tier": "Tier1",
        "notes": "VX-548, inhibidor Nav1.8, FDA 2025"
    },
    "TAK242": {
        "smiles": "CC1=CC(=CC(=C1Cl)C(F)(F)F)NC(=O)C2=C(C=CC=C2F)F",
        "target": "TLR4",
        "tier": "Tier2",
        "notes": "Resatorvid, antagonista TLR4, Fase II"
    },
    # GRC17536 SMILES no verificado públicamente. Lo excluimos por rigor.
    # Si se encuentra, agregar aquí.
}

# ─── LOAD FASTA TARGETS ────────────────────────────────────
def load_fasta(path):
    """Carga secuencias FASTA, retorna dict: name -> seq"""
    targets = {}
    with open(path) as f:
        name = None
        seq_parts = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    targets[name] = "".join(seq_parts)
                # Parse header: >Name|Gene|UniProt|Tier
                header = line[1:]
                parts = header.split("|")
                name = parts[0] if len(parts) > 0 else header
                seq_parts = []
            elif line:
                seq_parts.append(line)
        if name:
            targets[name] = "".join(seq_parts)
    return targets


def main():
    print("=" * 70)
    print("MAMMAL DTI Pipeline — Fibromialgia")
    print("=" * 70)

    # ── Check GPU ──
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    free_gb = torch.cuda.mem_get_info()[0] / 1e9 if torch.cuda.is_available() else 0
    print(f"Device: {device} | VRAM libre: {free_gb:.2f} GB")

    # ── Load targets ──
    print(f"\nCargando targets desde {FASTA_FILE}...")
    targets = load_fasta(FASTA_FILE)
    print(f"Targets cargados: {list(targets.keys())}")

    # ── Load DTI model ──
    print("\nCargando MAMMAL DTI fine-tuned model...")
    t0 = time.time()
    model = Mammal.from_pretrained("ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd")
    model.eval()
    model.to(device=device)
    tokenizer_op = ModularTokenizerOp.from_pretrained(
        "ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd"
    )
    print(f"Modelo cargado en {time.time()-t0:.1f}s")

    # ── Run predictions ──
    results = []
    print("\n--- Predicciones DTI ---")
    for drug_name, drug_info in DRUGS.items():
        target_name = drug_info["target"]
        if target_name not in targets:
            print(f"  ⚠ {drug_name}: target '{target_name}' no encontrado en FASTA — skip")
            continue

        target_seq = targets[target_name]
        drug_smiles = drug_info["smiles"]

        print(f"\n  {drug_name} → {target_name} (Tier: {drug_info['tier']})")
        print(f"    Target len: {len(target_seq)} aa | SMILES: {drug_smiles[:50]}...")

        # MAMMAL DTI format: {"target_seq": ..., "drug_seq": ...}
        sample_dict = {
            "target_seq": target_seq,
            "drug_seq": drug_smiles,
        }

        try:
            t1 = time.time()
            with torch.no_grad():
                batch_dict = model.predict(
                    [sample_dict],
                    output_scores=True,
                    return_dict_in_generate=True,
                    max_new_tokens=8,
                )

            # Extract prediction
            pred = tokenizer_op._tokenizer.decode(batch_dict[CLS_PRED][0])
            elapsed = time.time() - t1

            print(f"    Predicción: {pred} | Tiempo: {elapsed:.1f}s")

            results.append({
                "drug": drug_name,
                "target": target_name,
                "tier": drug_info["tier"],
                "notes": drug_info["notes"],
                "smiles": drug_smiles,
                "target_len": len(target_seq),
                "prediction_raw": pred,
                "inference_time_s": round(elapsed, 2),
            })

        except Exception as e:
            print(f"    ❌ Error: {e}")
            results.append({
                "drug": drug_name,
                "target": target_name,
                "tier": drug_info["tier"],
                "error": str(e),
            })

    # ── Also run cross-predictions: all drugs vs all targets (exploratory) ──
    print("\n\n--- Cross-predicciones (todos vs todos, exploratorio) ---")
    cross_results = []
    for drug_name, drug_info in DRUGS.items():
        drug_smiles = drug_info["smiles"]
        for target_name, target_seq in targets.items():
            if target_name == drug_info["target"]:
                continue  # ya lo hicimos

            sample_dict = {
                "target_seq": target_seq,
                "drug_seq": drug_smiles,
            }
            try:
                with torch.no_grad():
                    batch_dict = model.predict(
                        [sample_dict],
                        output_scores=True,
                        return_dict_in_generate=True,
                        max_new_tokens=8,
                    )
                pred = tokenizer_op._tokenizer.decode(batch_dict[CLS_PRED][0])
                cross_results.append({
                    "drug": drug_name,
                    "target": target_name,
                    "prediction_raw": pred,
                })
            except Exception as e:
                cross_results.append({
                    "drug": drug_name,
                    "target": target_name,
                    "error": str(e),
                })

    # ── Save ──
    output = {
        "pipeline": "MAMMAL DTI",
        "model": "ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd",
        "task": "Drug-Target Interaction (pKd prediction)",
        "date": "2026-05-14",
        "device": str(device),
        "direct_predictions": results,
        "cross_predictions": cross_results,
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*70}")
    print(f"Resultados guardados en: {OUTPUT_FILE}")
    print(f"Direct: {len(results)} | Cross: {len(cross_results)}")
    print(f"{'='*70}")

    # ── Quick summary ──
    print("\n--- RESUMEN DTI ---")
    for r in results:
        if "error" not in r:
            print(f"  {r['drug']:25s} → {r['target']:8s} [{r['tier']:6s}] = {r['prediction_raw']}")


if __name__ == "__main__":
    main()
