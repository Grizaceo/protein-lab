#!/usr/bin/env python3
"""
automated_lab/backends/_run_dti.py
===================================
Script interno lanzado por local_mammal.py via subprocess con conda python.
PROCESA UN LOTE de experimentos en una sola carga de modelo.

Recibe JSON por stdin.
Retorna SOLO JSON por stdout (sin warnings, sin logs).
"""

import sys, json, os

# SUPRIMIR WARNINGS que contaminan stdout
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import warnings
warnings.filterwarnings("ignore")
import logging
logging.disable(logging.CRITICAL)

# Leer input de stdin
data = json.load(sys.stdin)
experiments = data.get("experiments", [])

if not experiments:
    print(json.dumps({"error": "No experiments"}))
    sys.exit(1)

import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Redirigir todas las salidas de HF/transformers a /dev/null
import contextlib

with contextlib.redirect_stdout(open(os.devnull, 'w')):
    with contextlib.redirect_stderr(open(os.devnull, 'w')):
        from fuse.data.tokenizers.modular_tokenizer.op import ModularTokenizerOp
        from mammal.model import Mammal
        from mammal.examples.dti_bindingdb_kd.task import DtiBindingdbKdTask

        NORM_Y_MEAN = 5.79384684128215
        NORM_Y_STD = 1.33808027428196

        model = Mammal.from_pretrained("ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd")
        model.eval()
        model.to(device=device)

        tokenizer_op = ModularTokenizerOp.from_pretrained(
            "ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd"
        )

        # Procesar todos los experimentos
        results = []
        for exp in experiments:
            try:
                exp_type = exp.get("type", "dti_pkd")
                target_seq = exp.get("target_seq", "")
                drug_smiles = exp.get("drug_smiles", "")

                if exp_type == "dti_pkd":
                    sample_dict = {"target_seq": target_seq, "drug_seq": drug_smiles}
                    sample_dict = DtiBindingdbKdTask.data_preprocessing(
                        sample_dict=sample_dict,
                        tokenizer_op=tokenizer_op,
                        target_sequence_key="target_seq",
                        drug_sequence_key="drug_seq",
                        norm_y_mean=None,
                        norm_y_std=None,
                        device=device,
                    )

                    with torch.no_grad():
                        batch_dict = model.forward_encoder_only([sample_dict])

                    batch_dict = DtiBindingdbKdTask.process_model_output(
                        batch_dict,
                        scalars_preds_processed_key="model.out.pkd",
                        norm_y_mean=NORM_Y_MEAN,
                        norm_y_std=NORM_Y_STD,
                    )

                    pkd = float(batch_dict["model.out.pkd"][0])
                    kd_molar = 10 ** (-pkd)

                    results.append({
                        "status": "ok",
                        "pkd": round(pkd, 3),
                        "kd_molar": kd_molar,
                        "interpretation": (
                            "Alta afinidad (nM)" if pkd >= 8 else
                            "Afinidad moderada (µM)" if pkd >= 6 else
                            "Afinidad baja (mM)" if pkd >= 4 else
                            "Afinidad muy baja"
                        ),
                    })
                else:
                    results.append({"status": "error", "error": f"Unknown type: {exp_type}"})
            except Exception as e:
                results.append({"status": "error", "error": str(e)})

# SOLO imprimir el JSON al stdout
# Marker para separar warnings del JSON real
print("__MAMMAL_RESULT__")
print(json.dumps(results))
