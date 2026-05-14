#!/usr/bin/env python3
"""
MAMMAL DTI Pipeline v2 — Fibromialgia
======================================
Usa MAMMAL DTI fine-tuned model con DtiBindingdbKdTask para
predecir binding affinity (pKd) entre fármacos small-molecule y
sus targets proteicos.

Formato correcto: DtiBindingdbKdTask.data_preprocessing() →
model.forward_encoder_only() → DtiBindingdbKdTask.process_model_output()

Autor: DAVI + Cristóbal
Fecha: 2026-05-14
"""

import sys, os, json, time
import torch
import numpy as np
from fuse.data.tokenizers.modular_tokenizer.op import ModularTokenizerOp
from mammal.model import Mammal
from mammal.keys import *
from mammal.examples.dti_bindingdb_kd.task import DtiBindingdbKdTask

# ─── CONFIG ────────────────────────────────────────────────
BASE_DIR = "/home/gris/.hermes/workspace/protein-lab/investigacion-fibromialgia"
FASTA_FILE = f"{BASE_DIR}/datos/target_sequences.fasta"
OUTPUT_JSON = f"{BASE_DIR}/analisis/RESULTADOS_MAMMAL_DTI_v2.json"
OUTPUT_MD = f"{BASE_DIR}/analisis/RESULTADOS_MAMMAL_DTI.md"

# Normalization constants from the model (BindingDB pKd stats)
NORM_Y_MEAN = 5.79384684128215
NORM_Y_STD = 1.33808027428196

# ─── SMALL MOLECULE DRUGS ──────────────────────────────────
DRUGS = {
    "naltrexona_LDN": {
        "smiles": "C=CCN1CCC23C4C(=O)CCC2(C1CC5=C3C(=C(C=C5)O)O4)O",
        "target": "MOR",
        "tier": "Tier2",
        "notes": "LDN (Low-Dose Naltrexone), antagonista MOR, FDA aprobado"
    },
    "dimetil_fumarato": {
        "smiles": "COC(=O)C=CC(=O)OC",
        "target": "NRF2",
        "tier": "Tier1",
        "notes": "Tecfidera, activador NRF2, FDA 2013 para EM"
    },
    "suzetrigine_VX548": {
        "smiles": "CC1=C(SC(=N1)NC(=O)C2=C(C=CC=C2F)F)C(=O)NCC(F)(F)F",
        "target": "Nav1.8",
        "tier": "Tier1",
        "notes": "VX-548, inhibidor Nav1.8, FDA 2025"
    },
    "TAK242_resatorvid": {
        "smiles": "CC1=CC(=CC(=C1Cl)C(F)(F)F)NC(=O)C2=C(C=CC=C2F)F",
        "target": "TLR4",
        "tier": "Tier2",
        "notes": "Resatorvid, antagonista TLR4, Fase II"
    },
}


def load_fasta(path):
    targets = {}
    with open(path) as f:
        name = None
        seq_parts = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    targets[name] = "".join(seq_parts)
                parts = line[1:].split("|")
                name = parts[0]
                seq_parts = []
            elif line:
                seq_parts.append(line)
        if name:
            targets[name] = "".join(seq_parts)
    return targets


def predict_dti(model, tokenizer_op, target_seq, drug_smiles, device):
    """Predict pKd for a target-drug pair using MAMMAL DTI."""
    result = {"status": "ok"}
    
    # 1. Build sample dict
    sample_dict = {"target_seq": target_seq, "drug_seq": drug_smiles}
    
    # 2. Preprocess (converts to MAMMAL tokenized format)
    sample_dict = DtiBindingdbKdTask.data_preprocessing(
        sample_dict=sample_dict,
        tokenizer_op=tokenizer_op,
        target_sequence_key="target_seq",
        drug_sequence_key="drug_seq",
        norm_y_mean=None,  # prediction mode: no normalization
        norm_y_std=None,
        device=device,
    )
    
    # 3. Forward pass (encoder_only for regression)
    with torch.no_grad():
        batch_dict = model.forward_encoder_only([sample_dict])
    
    # 4. Post-process (denormalize)
    batch_dict = DtiBindingdbKdTask.process_model_output(
        batch_dict,
        scalars_preds_processed_key="model.out.pkd",
        norm_y_mean=NORM_Y_MEAN,
        norm_y_std=NORM_Y_STD,
    )
    
    # 5. Extract pKd
    result["pkd"] = float(batch_dict["model.out.pkd"][0])
    
    # Kd = 10^(-pKd) in M (molar)
    result["kd_molar"] = 10 ** (-result["pkd"])
    
    # Interpretation
    if result["pkd"] >= 8:
        result["interpretation"] = "Alta afinidad (nM)"
    elif result["pkd"] >= 6:
        result["interpretation"] = "Afinidad moderada (µM)"
    elif result["pkd"] >= 4:
        result["interpretation"] = "Afinidad baja (mM)"
    else:
        result["interpretation"] = "Afinidad muy baja o inespecífica"
    
    return result


def main():
    print("=" * 70)
    print("MAMMAL DTI Pipeline v2 — Fibromialgia")
    print("Modelo: biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd")
    print("=" * 70)

    # ── GPU ──
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # ── Targets ──
    print(f"\nCargando targets...")
    targets = load_fasta(FASTA_FILE)
    print(f"  {len(targets)} targets: {', '.join(targets.keys())}")

    # ── Model ──
    print("\nCargando modelo DTI...")
    t0 = time.time()
    model = Mammal.from_pretrained("ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd")
    model.eval()
    model.to(device=device)
    tokenizer_op = ModularTokenizerOp.from_pretrained(
        "ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd"
    )
    print(f"  Cargado en {time.time()-t0:.1f}s")

    # ── Direct predictions (drug → cognate target) ──
    results = []
    print("\n" + "─" * 70)
    print("PREDICCIONES DIRECTAS (fármaco → su target)")
    print("─" * 70)

    for drug_name, drug_info in DRUGS.items():
        target_name = drug_info["target"]
        if target_name not in targets:
            print(f"  ⚠ {drug_name}: target '{target_name}' no encontrado")
            continue

        target_seq = targets[target_name]
        print(f"\n  {drug_name} → {target_name} [{drug_info['tier']}]")
        print(f"    Target: {len(target_seq)} aa")

        try:
            t1 = time.time()
            r = predict_dti(model, tokenizer_op, target_seq, drug_info["smiles"], device)
            elapsed = time.time() - t1

            print(f"    pKd = {r['pkd']:.2f} | Kd = {r['kd_molar']:.2e} M | {r['interpretation']}")
            print(f"    Tiempo: {elapsed:.1f}s")

            results.append({
                "drug": drug_name,
                "target": target_name,
                "tier": drug_info["tier"],
                "notes": drug_info["notes"],
                "pkd": round(r["pkd"], 3),
                "kd_molar": r["kd_molar"],
                "interpretation": r["interpretation"],
                "target_len": len(target_seq),
                "inference_time_s": round(elapsed, 2),
            })

        except Exception as e:
            print(f"    ❌ ERROR: {e}")
            results.append({
                "drug": drug_name,
                "target": target_name,
                "tier": drug_info["tier"],
                "error": str(e),
            })

    # ── Cross-predictions ──
    cross = []
    print("\n" + "─" * 70)
    print("CROSS-PREDICCIONES (todos vs todos, exploratorio)")
    print("─" * 70)
    for drug_name, drug_info in DRUGS.items():
        for target_name, target_seq in targets.items():
            if target_name == drug_info["target"]:
                continue
            try:
                r = predict_dti(model, tokenizer_op, target_seq, drug_info["smiles"], device)
                cross.append({
                    "drug": drug_name,
                    "target": target_name,
                    "pkd": round(r["pkd"], 3),
                    "interpretation": r["interpretation"],
                })
            except Exception as e:
                cross.append({
                    "drug": drug_name,
                    "target": target_name,
                    "error": str(e),
                })

    # ── Save JSON ──
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    output = {
        "pipeline": "MAMMAL DTI v2",
        "model": "ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd",
        "date": "2026-05-14",
        "direct_predictions": results,
        "cross_predictions": cross,
    }
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # ── Markdown table ──
    print("\n" + "=" * 70)
    print("RESULTADOS")
    print("=" * 70)

    md = [
        "# MAMMAL DTI — Predicción de Binding Affinity (pKd)",
        f"**Modelo:** `ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd`",
        f"**Fecha:** 2026-05-14",
        "",
        "## Predicciones directas (fármaco → su target)",
        "",
        "| Fármaco | Target | Tier | pKd | Kd (M) | Interpretación |",
        "|---------|--------|------|-----|--------|---------------|",
    ]
    for r in results:
        if "error" in r:
            md.append(f"| {r['drug']} | {r['target']} | {r['tier']} | ❌ ERROR | — | {r['error']} |")
        else:
            md.append(
                f"| {r['drug']} | {r['target']} | {r['tier']} | "
                f"{r['pkd']:.2f} | {r['kd_molar']:.2e} | {r['interpretation']} |"
            )

    # Highlight best
    valid = [r for r in results if "error" not in r]
    if valid:
        best = max(valid, key=lambda x: x["pkd"])
        md.append("")
        md.append(f"**Mejor afinidad predicha:** {best['drug']} → {best['target']} (pKd={best['pkd']:.2f})")

    md.append("")
    md.append("## Cross-predicciones top-10")
    md.append("")
    md.append("| Fármaco | Target | pKd | Interpretación |")
    md.append("|---------|--------|-----|---------------|")
    cross_valid = sorted(
        [c for c in cross if "error" not in c],
        key=lambda x: x["pkd"],
        reverse=True,
    )
    for c in cross_valid[:10]:
        md.append(f"| {c['drug']} | {c['target']} | {c['pkd']:.2f} | {c['interpretation']} |")

    md.append("")
    md.append("---")
    md.append("*Pipeline: MAMMAL DTI v2 | DAVI + Cristóbal | 2026-05-14*")

    md_text = "\n".join(md)
    with open(OUTPUT_MD, "w") as f:
        f.write(md_text)

    print(md_text)


if __name__ == "__main__":
    main()
