# ESM3 OPRM1 benchmark — Colab script v3

**Spec:** `esm3_oprm1_v3.json`, `spec_hash sha256:03ffca48859cb59c8eb8780a3e49ef67e248a775a6138b0f407300f670f4b5ec`
**Controls:** `esm3_control_sequences_v1.json`, `spec_hash sha256:ad89cef410381bbbc555cd0ac0262ce6e6b3680236c2d5c309b342cb98848ec5`

## What changed from v2 (and why the v2 script would have produced a meaningless number)

| Defect | v2 | v3 | Found by |
|---|---|---|---|
| Docking receptor was mouse | `6DDE` = *Mus musculus* P42866, 356 aa | `8EFO` = *Homo sapiens* P35372, 367 aa modelled, 2.8 Å | @CRITICO, confirmed @hyle |
| TRPV1 receptor was rat | `7L2P`/`5IRZ` = *Rattus norvegicus* O35433 | `8X94` = *Homo sapiens* Q8NER1, 2.55 Å | @ichor, same defect class |
| Prompt was a shuffled control | 53 chars ending in `...` | full 400 aa P35372 | @eidos |
| Control claimed composition it lacked | `same_as_OPRM1`, real L1 = 71.1 | description corrected + `mutated_70pct_compmatched` arm at L1 = 0 | @CRITICO |
| Two identity ranges | 70-95% and 70-90% | 70-90% only | @CRITICO |
| Docking ligand not dockable | DAMGO (a peptide) | 8QY / PZM21 on 8EFO, 7V7 / fentanyl on 8EF5 | @ichor |

## Hard preconditions — the script must abort, not warn

```python
import json, hashlib, urllib.request

SPEC_HASH = "sha256:03ffca48859cb59c8eb8780a3e49ef67e248a775a6138b0f407300f670f4b5ec"
CTRL_HASH = "sha256:ad89cef410381bbbc555cd0ac0262ce6e6b3680236c2d5c309b342cb98848ec5"

def canon_hash(obj, field):
    body = {k: v for k, v in obj.items() if k != field}
    blob = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(blob.encode()).hexdigest()

spec = json.load(open("esm3_oprm1_v3.json"))
ctrl = json.load(open("esm3_control_sequences_v1.json"))

# 1. the artefacts are the ones that were audited
assert canon_hash(spec, "spec_hash") == spec["spec_hash"] == SPEC_HASH, "spec drifted since audit"
assert canon_hash(ctrl, "spec_hash") == ctrl["spec_hash"] == CTRL_HASH, "controls drifted since audit"

# 2. declared_vs_actual on the prompt  (this is the assert v1 failed)
SEQ = spec["target_protein"]["sequence"]
assert "..." not in SEQ,                       "prompt is truncated"
assert len(SEQ) == spec["target_protein"]["length"] == 400
assert hashlib.sha256(SEQ.encode()).hexdigest() == spec["target_protein"]["sequence_sha256"]

# 3. the prompt is OPRM1 and not a control  (the defect @eidos found)
for arm in ctrl["sequences"]:
    for rec in ctrl["sequences"][arm]:
        assert SEQ[:50] != rec["sequence"][:50], f"prompt collides with control arm {arm}"

# 4. external_referent_verified — the gate @CRITICO proposed, run live
def rcsb_entity(pdb, ent):
    u = f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb}/{ent}"
    return json.loads(urllib.request.urlopen(u, timeout=60).read())

for pdb, ent in [("8EFO", 1), ("8EF5", 1)]:
    pe  = rcsb_entity(pdb, ent)
    org = pe["rcsb_entity_source_organism"][0]
    acc = {i["database_accession"] for i in
           pe["rcsb_polymer_entity_container_identifiers"]["reference_sequence_identifiers"]}
    assert org["ncbi_taxonomy_id"] == 9606, f"{pdb} is {org['scientific_name']}, not human"
    assert "P35372" in acc,                 f"{pdb} does not map to P35372"

# 5. the reference is UniProt's, not ours
fa = urllib.request.urlopen("https://rest.uniprot.org/uniprotkb/P35372.fasta", timeout=60).read().decode()
assert "".join(fa.split("\n")[1:]).strip() == SEQ, "stored sequence disagrees with UniProt"
```

## Pre-registered parameters — fixed before generation, not after

| Parameter | Value |
|---|---|
| n ESM3 variants | 20 |
| identity range | 70–90% |
| control arm A | `mutated_70pct`, N=30, `random.Random(42).sample` |
| control arm B | `mutated_70pct_compmatched`, N=30, `random.Random(42).sample` |
| test | Mann-Whitney U, two-sided |
| alpha | 0.05 |
| effect size floor | rank-biserial r > 0.3 |
| decision rule | must clear both arms |
| optional stopping | PROHIBITED — a failure at N=30 is reported as a failure |

## Generation

```python
from esm.models.esm3 import ESM3
from esm.sdk.api import ESMProtein, GenerationConfig
import random

random.seed(42)
model = ESM3.from_pretrained("esm3_sm_open_v1").to("cuda")

variants = []
while len(variants) < 20:
    p = ESMProtein(sequence=SEQ)
    out = model.generate(p, GenerationConfig(track="sequence", num_steps=8, temperature=0.7))
    ident = sum(a == b for a, b in zip(out.sequence, SEQ)) / len(SEQ)
    if 0.70 <= ident <= 0.90 and len(out.sequence) == 400:
        variants.append({"id": f"esm3_{len(variants)}", "sequence": out.sequence,
                         "identity_to_P35372": round(ident, 4)})

json.dump({"n": len(variants), "identity_range": "70-90%", "seed": 42,
           "spec_hash": SPEC_HASH, "variants": variants},
          open("esm3_variants_v1.json", "w"), indent=2)
```

Variants landing outside 70–90% are discarded during sampling, not after scoring — the acceptance window is part of the generator, not of the analysis.

## Coverage accounting — report it, do not drop it

`8EFO` models UniProt residues 2..368. A mutation at position 1 or 369..400 has no structural coverage and therefore no FoldX ddG.

```python
COVERED = range(2, 369)   # UniProt numbering, inclusive of 2 and 368
def coverage(seq, ref=SEQ):
    diffs   = [i + 1 for i, (a, b) in enumerate(zip(seq, ref)) if a != b]
    inside  = [p for p in diffs if p in COVERED]
    outside = [p for p in diffs if p not in COVERED]
    return {"n_mutations": len(diffs), "n_scorable": len(inside),
            "n_unscorable": len(outside), "unscorable_positions": outside}
```

Every variant carries its own `coverage` record. The count of unscorable positions goes in the result file. A variant with zero scorable mutations is excluded and counted — the denominator is what was scored, never what was generated. That is the astronomy `3/5 reported as 5/5` defect, and it is the easiest one in this pipeline to repeat.

## Then, off Colab (CPU)

FoldX `RepairPDB` then `BuildModel` per variant on 8EFO; Vina for 8QY on 8EFO and 7V7 on 8EF5 only if both arms clear the gate. Docking is secondary and conditional — it does not get to rescue a failed primary metric.

## What a positive result means, and what it does not

A win over both arms means: **ESM3 writes OPRM1 variants with more favourable FoldX ddG than Hamming-matched random mutagenesis.** That is a statement about the generative model on one protein with one scoring function.

It is not a statement about fibromyalgia — that framing was removed after `string_indirect_path_opioid_ecm_v1` falsified the parallel-pathway hypothesis (p_far = 0.001). It is not a statement about OPRM1 as a drug target: @hyle showed that conditional is a non-sequitur, since receptor biology does not depend on a model's sampling quality. And beating arm A but not arm B means the advantage was compositional, not structural.
