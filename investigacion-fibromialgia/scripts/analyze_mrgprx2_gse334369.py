#!/usr/bin/env python3
"""MRGPRX2/TAC1/TACR1 blunting analysis in GSE334369 — completes the axis test
that the 19-gene panel missed (MRGPRX2) and re-runs TAC1/TACR1 with CMA1 control.

Kill criterion (same convention as the parent spec):
at least 1 gene with blunting p<0.05 after Bonferroni (n=6 tests -> 0.0083).
"""
import json
import os
import math

BASE = "/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/datos/geo/GSE334369"
GENES = ["MRGPRX2", "TAC1", "TACR1", "CMA1", "IL1B", "CXCL8"]

groups = json.load(open(os.path.join(BASE, "groups_gse334369.json")))
tpm = json.load(open(os.path.join(BASE, "mrgprx2_tpm.json")))

def log2_ratio(v_lps, v_unstim):
    return math.log2((v_lps + 0.1) / (v_unstim + 0.1))

# Pair by donor: strip the NAR/NNAR suffix from the E-code. Build E-code -> (gsm)
# First map GSM -> E-code via inspect/ filenames
insp = os.path.join(BASE, "inspect")
gsm_to_ecode = {}
for fn in os.listdir(insp):
    # GSM9786802_processed_NEBNext_dual_i5_288.E02NARAligned.tsv.gz
    if fn.startswith("GSM") and "." in fn:
        gsm = fn.split("_")[0]
        ecode = fn.split(".")[1]  # E02NAR
        gsm_to_ecode[gsm] = ecode

# For all other GSMs (not in inspect), parse the tar member name
if len(gsm_to_ecode) < 206:
    import tarfile
    tar = tarfile.open(os.path.join(BASE, "GSE334369_RAW.tar"), "r")
    for m in tar.getmembers():
        name = m.name
        gsm = name.split("_")[0]
        if gsm in gsm_to_ecode:
            continue
        # ...E02NARAligned.tsv.gz
        stem = name.rsplit(".", 2)[0]  # strip .tsv.gz
        ecode = stem.split(".")[-1]    # E02NARAligned
        gsm_to_ecode[gsm] = ecode.removesuffix("Aligned")
    tar.close()

print(f"gsm_to_ecode: {len(gsm_to_ecode)}")

# Precompute donor -> partner GSM maps once (fast)
ecode_to_gsm = {}
for gsm, e in gsm_to_ecode.items():
    ecode_to_gsm[e] = gsm

results = {}
for gene in GENES:
    series = tpm[gene]
    case_pairs, ctrl_pairs = [], []
    unmatched = []
    for grp, tag in [("Case_NAR", "Case"), ("Control_NAR", "Control")]:
        for gsm in groups[grp]:
            e = gsm_to_ecode.get(gsm, "")
            donor = e[:-3]  # strip NAR -> E02
            partner_gsm = ecode_to_gsm.get(donor + "NNAR")
            if partner_gsm is None or gsm not in series or partner_gsm not in series:
                unmatched.append((e, gsm))
                continue
            lr = log2_ratio(series[gsm], series[partner_gsm])
            if tag == "Case":
                case_pairs.append(lr)
            else:
                ctrl_pairs.append(lr)
    results[gene] = {
        "case_pairs": case_pairs,
        "ctrl_pairs": ctrl_pairs,
        "unmatched": unmatched[:5],
    }

# Welch + Wilcoxon-free stats (pure python)
def mean(x):
    return sum(x) / len(x) if x else float("nan")

def var(x):
    m = mean(x)
    return sum((v - m) ** 2 for v in x) / (len(x) - 1) if len(x) > 1 else float("nan")

def welch(a, b):
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return None
    m1, m2 = mean(a), mean(b)
    v1, v2 = var(a), var(b)
    se2 = v1 / n1 + v2 / n2
    t = (m1 - m2) / math.sqrt(se2)
    df = se2**2 / ((v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1))
    return m1 - m2, t, df

def t_sf(t, df):
    # two-sided p via incomplete beta — use math.erfc approx for large df; exact via scipy if available
    try:
        from scipy import stats
        return 2 * stats.t.sf(abs(t), df)
    except Exception:
        # normal approximation
        z = abs(t)
        return math.erfc(z / math.sqrt(2))

out = {}
for gene, d in results.items():
    a, b = d["case_pairs"], d["ctrl_pairs"]
    r = welch(a, b)
    if r is None:
        continue
    delta, t, df = r
    p = t_sf(t, df)
    out[gene] = {
        "n_case": len(a),
        "n_ctrl": len(b),
        "case_LPS_response": mean(a),
        "ctrl_LPS_response": mean(b),
        "blunting_delta_case_minus_ctrl": delta,
        "welch_t": t,
        "df": df,
        "p_val": p,
        "unmatched_example": d["unmatched"],
    }

json.dump(out, open(os.path.join(BASE, "mrgprx2_blunting_results.json"), "w"), indent=1)
for gene, r in out.items():
    flag = " <0.05" if r["p_val"] < 0.05 else ""
    print(f"{gene:10s} nC={r['n_case']:2d} nK={r['n_ctrl']:2d} case={r['case_LPS_response']:+.3f} ctrl={r['ctrl_LPS_response']:+.3f} delta={r['blunting_delta_case_minus_ctrl']:+.3f} p={r['p_val']:.4f}{flag}")