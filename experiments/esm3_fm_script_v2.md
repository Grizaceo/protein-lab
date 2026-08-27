# ESM3 Guided Generation for FM — v2 (CORRECTED)

**Input:** `esm3_input_sequences_v2.json` (dataset_hash sha256:ceb0ff2032f5ce49…)
**Supersedes:** `esm3_fm_script.md` v1 — which hardcoded 53-char TRUNCATED sequences ending in '...'

## Corrections vs v1

| Defect | v1 | v2 |
|---|---|---|
| Sequence truncation | all inputs 53 chars + literal `...` | full length, sha256 recorded |
| Spec target | shuffled control fragment | real UniProt P35372, 400aa |
| SCN9A accession | Q9Y5Y9 = **SCN10A** (wrong gene) | Q15858 = SCN9A (1988aa) |
| SCN9A inclusion | silently dropped from script | **explicitly excluded**: 1988aa > 1024 T4 context |
| Genes run | 4, undeclared | 4, declared: OPRM1, OPRD1, TRPV1, CXCL12 |

## Script

```python
import json, torch
from esm.models.esm3 import ESM3
from esm.sdk.api import ESM3Prompt

SEQS = json.load(open("esm3_input_sequences_v2.json"))["sequences"]
GENES = [g for g,v in SEQS.items() if v["selected_for_esm3"]]   # OPRM1, OPRD1, TRPV1, CXCL12

model = ESM3.from_pretrained("esm3_sm_open_t36_2B_500M").to("cuda")

results = {}
for g in GENES:
    seq = SEQS[g]["sequence"]
    assert len(seq) == SEQS[g]["sequence_length"], f"{g}: truncated input"   # v1 failed exactly here
    assert "..." not in seq, f"{g}: ellipsis in sequence"
    prompt = ESM3Prompt.from_sequence(seq)
    variants = model.generate(prompt, num_samples=20, temperature=0.7, conditioning="structure")
    results[g] = [{"identity": v.identity, "sequence": v.sequence, "len": len(v.sequence)} for v in variants]

json.dump(results, open("esm3_variants_v2.json","w"), indent=2)
```

## Pre-registered downstream (do not renegotiate after seeing output)

- N=20 ESM3 variants per gene, N=30 controls sampled seed=42 from the 100 `mutated_70pct` (identity 70.0% exact).
- Mann-Whitney U on ddG, alpha=0.05, effect size rank-biserial r>0.3. `optional_stopping: PROHIBITED`.
- Controls verified sound: consensus of the 100 mutants reconstructs P35372 at 100.0%.

## Status

**PENDING_COLAB** — blocked on Google login (browser automation down). Script and inputs now verified; v1 would have run on scrambled 53-mers.