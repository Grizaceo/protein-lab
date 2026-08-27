# ESM3 Guided Generation for FM — Ready for Colab

**Source:** https://colab.research.google.com/github/Biohub/esm/blob/main/cookbook/tutorials/esm3_guided_generation.ipynb
**Input:** `protein-lab/experiments/esm3_input_sequences.json` (5 genes, UniProt verified)
**Requirement:** Colab with T4 GPU (free tier)

## Script

```python
import torch
from esm.models.esm3 import ESM3
from esm.sdk.api import ESM3Prompt

# Load model (T4 GPU compatible)
model = ESM3.from_pretrained("esm3_sm_open_t36_2B_500M")

# Input sequences (from UniProt, verified)
sequences = {
    "OPRM1": "MDSSAAPTNASNCTDALAYSSCSPAPSPGSWVNLSHLDGNLSDPCGPNRT...",
    "OPRD1": "MEPAPSAGAELQPPLFANASDAYPSACPSAGANASGPPGARSASSLALAI...",
    "TRPV1": "MKKWSSTDLGAAADPLQKDTCPDPLDGDPNSRPPPAKPQLSTAKSRTRLF...",
    "CXCL12": "MNAKVVVVLVLVLTALCLSDGKPVSLSYRCPCRFFESHVARANVKHLKIL..."
}

results = {}
for name, seq in sequences.items():
    prompt = ESM3Prompt.from_sequence(seq)
    variants = model.generate(prompt, num_samples=10, temperature=0.7, conditioning="structure")
    results[name] = [{"identity": v.identity, "sequence": v.sequence} for v in variants]

# Save results
import json
with open("esm3_variants.json", "w") as f:
    json.dump(results, f, indent=2)
```

## Expected Output

For OPRM1 (400aa): ~10-15 min on T4 GPU → 10 variants with structure-conditioned generation.

## Status

**PENDING** — Requires Colab execution. Script ready.
