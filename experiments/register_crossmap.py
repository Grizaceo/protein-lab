#!/usr/bin/env python3
"""Register the FME cross-map result as a protein-lab experiment spec."""
import json, hashlib, os
from datetime import datetime

def canon_spec(obj):
    filtered = {k: v for k, v in obj.items() if k not in ('spec_hash', 'hash_method')}
    return "sha256:" + hashlib.sha256(json.dumps(filtered, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()

spec = {
    "experiment_id": "ichor-fme-crossmap-gse67311-v1",
    "description": (
        "Cross-map FME module: key genes from GSE324210 (exercise acute response, healthy monocytes) "
        "and GSE334369 (LPS blunted response, FM neutrophils) projected onto GSE67311 (FM vs HC peripheral blood, GPL11532, n=70). "
        "Tests whether the exercise-response / blunter-response genes are also dysregulated in FM blood at baseline."
    ),
    "datasets": {
        "target": "GSE67311 (FM vs HC peripheral blood, AFFY GPL11532 Illumina HumanHT-12 v4)",
        "source_genes": [
            "GSE324210 (exercise response: IL1B/TAC1/MRGPRX2/CA14/TLR4/OPRM1)",
            "GSE334369 (LPS blunted response: IL1B/IL6/CXCL8/TNFAIP3/CA14/TACR1)"
        ],
        "probe_mapping": "GPL11532.annot.gz (22,170 probes mapped to gene symbols)"
    },
    "target_samples": {
        "n_total": 70,
        "fm": 35, "hc": 35
    },
    "key_result": {
        "summary": "None of the 23 key genes are significantly different (all adj.pval > 0.58). The exercise-response / LPS-blunting signature does NOT carry over to FM peripheral blood at baseline.",
        "nominal_trend_IFN_axis_DOWN": {
            "IFI44L": {"log2FC": -0.078, "pval": 0.0254, "adj_pval": 0.5840},
            "IFITM1": {"log2FC": -0.015, "pval": 0.0457, "adj_pval": 0.6169},
            "OAS1": {"log2FC": -0.032, "pval": 0.0376, "adj_pval": 0.6118},
            "IFIT1": {"log2FC": -0.055, "pval": 0.0563, "adj_pval": 0.6173},
            "MX1": {"log2FC": -0.027, "pval": 0.2190, "adj_pval": 0.7264}
        },
        "opioide_axis": {
            "OPRM1": {"log2FC": +0.010, "pval": 0.196, "adj_pval": 0.720},
            "OPRD1": {"log2FC": +0.012, "pval": 0.138, "adj_pval": 0.687},
            "OPRK1": {"log2FC": +0.011, "pval": 0.268, "adj_pval": 0.750},
            "note": "All flat. No peripheral opioid receptor dysregulation in FM blood."
        },
        "sensory_axis": {
            "TAC1": {"log2FC": +0.002, "adj_pval": 0.954},
            "TACR1": {"log2FC": +0.003, "adj_pval": 0.938},
            "note": "Flat. No peripheral taquinin axis dysregulation."
        }
    },
    "interpretation": {
        "for_fme": (
            "FM blood baseline does NOT show constitutive dysregulation of the exercise-response module "
            "or of the LPS-blunted-response genes. The blunted LPS response in PMN (GSE334369) and the acute-exercise "
            "response in monocytes (GSE324210) are STIMULUS-DEPENDENT states, not baseline transcriptional dysregulation. "
            "This supports a state-dependent model: FM alters the RESPONSE to stress, not the RESTING state."
        ),
        "mision_connection": (
            "La forma que se descubre: el fenotipo FME no es visible en sangre basale como expresión diferencial cruda — "
            "pero SI emerge cuando se somete a estrés (ejercicio / LPS). La 'forma' existe en la interacción "
            "estímulo-respuesta, no en el estado basal. Replicar requiere la cohorte húmeda (0 datasets públicos con ΔPPT/EIH)."
        )
    },
    "caveats": [
        "GSE67311 is AFFY array with older platform; sensitivity lower than RNA-seq",
        "IFN nominal p-values do not survive FDR within our 24-gene subset",
        "Peripheral blood confounds (cell-type composition) not fully adjusted",
        "NOMINAL p-values on IFN axis are consistent with fragmentarily-reported IFN decreases in FM but not Bonferroni-corrected"
    ],
    "kill_criterion": {
        "type": "signal_carries_to_target",
        "metric": "at least 1 of 24 key genes with adj.pval < 0.05 and |log2FC| > 0.1 in FM vs HC",
        "threshold": ">= 1 gene",
        "result": "FAIL - Best candidate IFI44L adj.pval=0.584; no gene survives multiple-testing correction",
        "follow_up": "The blunted-response hypothesis survives only at stimulus level, not at baseline"
    },
    "hash_method": "eidos-canonicalization-v1 (excludes spec_hash and hash_method, sort_keys=True, separators=(',',':'), ensure_ascii=False)"
}

spec["spec_hash"] = canon_spec(spec)
print(f"spec_hash: {spec['spec_hash']}")
print(f"Reproduces: {canon_spec(spec) == spec['spec_hash']}")

out_path = f"/home/gris/.hermes/workspace/ACTIVE/protein-lab/experiments/{spec['experiment_id']}.json"
with open(out_path, 'w') as f:
    json.dump(spec, f, indent=2, sort_keys=True, ensure_ascii=False)
print(f"Saved: {out_path}")