"""MAMMAL binary DTI classification — binder/no-binder para DRD2.
Modo encoder-decoder con prompt BINDING_AFFINITY_CLASS.
Usa modelo base ibm/biomed.omics.bl.sm.ma-ted-458m (pre-entrenado en PPI classification).
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import torch
import numpy as np
from fuse.data.tokenizers.modular_tokenizer.op import ModularTokenizerOp
from mammal.keys import CLS_PRED, SCORES, ENCODER_INPUTS_STR, ENCODER_INPUTS_TOKENS, ENCODER_INPUTS_ATTENTION_MASK
from mammal.model import Mammal

# === DRD2 sequence ===
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

# === Test panel: fármacos con ground truth de binding a DRD2 ===
DRUGS = [
    # POSITIVOS (binders conocidos)
    {"name": "dopamine", "smiles": "C1=CC(=C(C=C1CCN)O)O", "label": 1, "evidence": "endogenous agonist, Ki=1.8-15000 nM"},
    {"name": "pramipexole", "smiles": "CCCN[C@H]1CCC2=C(C1)SC(=N2)N", "label": 1, "evidence": "D3/D2 agonist, Ki D2=3.9 nM"},
    {"name": "ropinirole", "smiles": "CCCN(CCC)CCC1=C2CC(=O)NC2=CC=C1", "label": 1, "evidence": "D2/D3 agonist, Ki D2=2.5 nM"},
    {"name": "bromocriptine", "smiles": "CC(C)CC1C(=O)N2CCCC2C3(N1C(=O)C(O3)(C(C)C)NC(=O)C4CN(C5CC6=C(NC7=CC=CC(=C67)C5=C4)Br)C)O", "label": 1, "evidence": "D2 agonist, co-crystallized 6VMS, Ki=0.62-110 nM"},
    {"name": "cabergoline", "smiles": "CCNC(=O)N(CCCN(C)C)C(=O)C1CC2C(CC3=CNC4=CC=CC2=C34)N(C1)CC=C", "label": 1, "evidence": "D2 agonist, Ki~0.7 nM"},
    # NEGATIVOS (no binders)
    {"name": "atorvastatin", "smiles": "CC(C)c1c(C(=O)Nc2ccccc2)c(c(c1C(=O)Nc2ccccc2)c1ccc(Cl)cc1)CC(C)(C)C", "label": 0, "evidence": "HMG-CoA reductase inhibitor"},
    {"name": "ibuprofen", "smiles": "CC(Cc1ccc(cc1)C(C(=O)O)C)C", "label": 0, "evidence": "COX-1/2 inhibitor, NSAID"},
    {"name": "metformin", "smiles": "CN(C)C(=N)NC(=N)N", "label": 0, "evidence": "AMPK activator, mitochondrial complex I"},
    {"name": "omeprazole", "smiles": "CC1=CN=C(C(=C1OC)C)CS(=O)C2=NC3=C(N2)C=C(C=C3)OC", "label": 0, "evidence": "proton pump inhibitor"},
]

print("Loading MAMMAL base model (encoder-decoder)...")
model_path = "ibm/biomed.omics.bl.sm.ma-ted-458m"
model = Mammal.from_pretrained(model_path, allow_config_mismatch=True)
model.eval()
model.to(device="cuda")
tok = ModularTokenizerOp.from_pretrained(model_path)
print(f"Model loaded. VRAM: {torch.cuda.memory_allocated()/1e9:.1f} GB")

# Classification prompt format from TCR binding example
def predict_binding(target_seq, drug_smiles):
    """Binary classification: does this drug bind this target?"""
    prompt = (
        "<@TOKENIZER-TYPE=AA><BINDING_AFFINITY_CLASS><SENTINEL_ID_0>"
        f"<@TOKENIZER-TYPE=AA><MOLECULAR_ENTITY><MOLECULAR_ENTITY_GENERAL_PROTEIN>"
        f"<SEQUENCE_NATURAL_START>{target_seq}<SEQUENCE_NATURAL_END>"
        f"<@TOKENIZER-TYPE=SMILES><MOLECULAR_ENTITY><MOLECULAR_ENTITY_SMALL_MOLECULE>"
        f"<SEQUENCE_NATURAL_START>{drug_smiles}<SEQUENCE_NATURAL_END>"
        "<EOS>"
    )
    sample = {ENCODER_INPUTS_STR: prompt}
    tok(sample, key_in=ENCODER_INPUTS_STR,
        key_out_tokens_ids=ENCODER_INPUTS_TOKENS,
        key_out_attention_mask=ENCODER_INPUTS_ATTENTION_MASK)
    sample[ENCODER_INPUTS_TOKENS] = torch.tensor(
        sample[ENCODER_INPUTS_TOKENS], device=model.device
    )
    sample[ENCODER_INPUTS_ATTENTION_MASK] = torch.tensor(
        sample[ENCODER_INPUTS_ATTENTION_MASK], device=model.device
    )
    
    with torch.no_grad():
        batch = model.generate(
            [sample], output_scores=True, return_dict_in_generate=True, max_new_tokens=5
        )
    
    # Extract class prediction
    neg_id = tok.get_token_id("<0>")
    pos_id = tok.get_token_id("<1>")
    
    token = batch[CLS_PRED][0][1]  # position 1 = the SENTINEL replacement
    score = float(batch[SCORES][0][1, pos_id].item())
    
    label_map = {neg_id: 0, pos_id: 1}
    pred = label_map.get(int(token), -1)
    
    return pred, score

# === Run inference ===
results = []
print("\n=== DRD2 BINARY CLASSIFICATION ===\n")
for drug in DRUGS:
    pred, score = predict_binding(DRD2_SEQ, drug["smiles"])
    correct = "✓" if pred == drug["label"] else "✗"
    print(f"  {correct} {drug['name']:20s}  true={drug['label']}  pred={pred}  score={score:.4f}  | {drug['evidence']}")
    results.append({**drug, "pred": pred, "score": score, "correct": pred == drug["label"]})

# === Metrics ===
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, f1_score

y_true = [r["label"] for r in results]
y_pred = [r["pred"] for r in results]
y_score = [r["score"] for r in results]

print("\n=== METRICS ===")
print(f"Accuracy : {accuracy_score(y_true, y_pred):.2%}")
print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.2%}")
print(f"Recall   : {recall_score(y_true, y_pred, zero_division=0):.2%}")
print(f"F1       : {f1_score(y_true, y_pred, zero_division=0):.2%}")
try:
    print(f"AUROC    : {roc_auc_score(y_true, y_score):.4f}")
except:
    print("AUROC    : N/A (all same class?)")

# === Save ===
outpath = os.path.join(os.path.dirname(__file__), "mammal_binary_drd2_2026-05-14.json")
with open(outpath, "w") as f:
    json.dump({"target": "DRD2", "model": model_path, "mode": "binary_classification",
               "results": results, "metrics": {
                   "accuracy": accuracy_score(y_true, y_pred),
                   "precision": precision_score(y_true, y_pred, zero_division=0),
                   "recall": recall_score(y_true, y_pred, zero_division=0),
                   "f1": f1_score(y_true, y_pred, zero_division=0)
               }}, f, indent=2)
print(f"\nSaved: {outpath}")
