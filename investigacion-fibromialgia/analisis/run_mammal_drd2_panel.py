"""MAMMAL DTI panel — DRD2 vs dopaminérgicos + controles negativos.
Ejecutar desde protein-lab env: /home/gris/.miniconda/envs/protein-lab/bin/python
"""
import os, sys, json, warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

import torch
from mammal.model import Mammal
from fuse.data.tokenizers.modular_tokenizer.op import ModularTokenizerOp
from mammal.examples.dti_bindingdb_kd.task import DtiBindingdbKdTask

NORM_Y_MEAN = 5.79384684128215
NORM_Y_STD = 1.33808027428196

# DRD2 sequence (UniProt P14416)
DRD2_SEQ = (
    "MDPLNLSWYDDDLERQNWSRPFNGSDGKADRPHYNYYATLLTLLIAVIVFGNVLVCMAVS"
    "REKALQTTTNYLIVSLAVADLLVATLVMPWVVYLEVVGEWKFSRIHCDIFVTLDVMMCTA"
    "SILNLCAISIDRYTAVAMPMLYNTRYSSKRRVTVMISIVWVLSFTISCPLLFGLNNADQN"
    "ECIIANPAFVVYSSIVSFYVPFIVTLLVYIKIYIVLRRRRKRVNTKRSSRAFRAHLRAPL"
    "KGNCTHPEDMKLCTVIMKSNGSFPVNRRRVEAARRAQELEMEMLSSTSPPERTRYSPIPP"
    "SHHQLTLPDPSHHGLHSTPDSPAKPEKNGHAKDHPKIAKIFEIQTMPNGKTRTSLKTMSR"
    "RKLSQQKEKKATQMLAIVLGVFIICWLPFFITHILNIHCDCNIPPVLYSAFTWLGYVNSA"
    "VNPIIYTTFNIEFRKAFLKILHC"
)

# Drug panel: SMILES from PubChem
DRUGS = {
    # Agonists / test drugs
    "pramipexole": "CCCN[C@H]1CCC2=C(C1)SC(=N2)N",
    "ropinirole": "CCCN(CCC)CCC1=C2CC(=O)NC2=CC=C1",
    "rotigotine": "CCCN(CCC1=CC=CS1)[C@H]2CCC3=C(C2)C=CC=C3O",
    "bromocriptine": "CC(C)CC1C(=O)N2CCCC2C3(N1C(=O)C(O3)(C(C)C)NC(=O)C4CN(C5CC6=C(NC7=CC=CC(=C67)C5=C4)Br)C)O",
    "cabergoline": "CCNC(=O)N(CCCN(C)C)C(=O)C1CC2C(CC3=CNC4=CC=CC2=C34)N(C1)CC=C",
    "dopamine": "C1=CC(=C(C=C1CCN)O)O",
    # Negative controls (should NOT bind DRD2)
    "atorvastatin": "CC(C)c1c(C(=O)Nc2ccccc2)c(c(c1C(=O)Nc2ccccc2)c1ccc(Cl)cc1)CC(C)(C)C",
    "ibuprofen": "CC(Cc1ccc(cc1)C(C(=O)O)C)C",
    "metformin": "CN(C)C(=N)NC(=N)N",
    "omeprazole": "CC1=CN=C(C(=C1OC)C)CS(=O)C2=NC3=C(N2)C=C(C=C3)OC",
}

print("Loading MAMMAL DTI model...")
model = Mammal.from_pretrained("ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd")
model.eval().to(device="cuda")
tok = ModularTokenizerOp.from_pretrained("ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd")
print(f"Model loaded. VRAM used: ~{torch.cuda.memory_allocated()/1e9:.2f} GB")

results = []
for name, smiles in DRUGS.items():
    try:
        sample = {
            "target_seq": DRD2_SEQ,
            "drug_seq": smiles,
        }
        sample = DtiBindingdbKdTask.data_preprocessing(
            sample_dict=sample, tokenizer_op=tok,
            target_sequence_key="target_seq", drug_sequence_key="drug_seq",
            norm_y_mean=None, norm_y_std=None, device=model.device,
        )
        with torch.no_grad():
            batch = model.forward_encoder_only([sample])
        batch = DtiBindingdbKdTask.process_model_output(
            batch, scalars_preds_processed_key="model.out.pkd",
            norm_y_mean=NORM_Y_MEAN, norm_y_std=NORM_Y_STD,
        )
        pkd = float(batch["model.out.pkd"][0])
        results.append({"drug": name, "pKd": round(pkd, 3)})
        print(f"  {name:20s} → pKd = {pkd:.3f}")
    except Exception as e:
        print(f"  {name:20s} → ERROR: {e}")
        results.append({"drug": name, "pKd": None, "error": str(e)})

print("\n=== SORTED BY pKd ===")
valid = [r for r in results if r["pKd"] is not None]
valid.sort(key=lambda x: x["pKd"], reverse=True)
for r in valid:
    print(f"  {r['drug']:20s} pKd = {r['pKd']:.3f}")

# Save JSON
outpath = os.path.join(os.path.dirname(__file__), "mammal_drd2_panel_2026-05-14.json")
with open(outpath, "w") as f:
    json.dump({"target": "DRD2", "uniprot": "P14416", "results": results, "sorted": valid}, f, indent=2)
print(f"\nSaved to {outpath}")
