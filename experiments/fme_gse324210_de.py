#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ichor-FME cuadro A: GSE324210 análisis sex-specific agudo vs training (time 1-4).
Diseño: time1=pre-training rest, time2=pre-training acute(post-bouts), time3=post-training rest,
time4=post-training acute. Cargas: raw counts -> CPM -> DE pre-agudo (T2vsT1), post-agudo (T4vsT3),
training rest (T3vsT1), por sexo. Sin scipy útil p/ DE scipy checado arriba; uso manual
Mann-Whitney-ish vía permutación + BH. Regla: nada presentado como clínico; in-silico only.
"""
import json, re, collections
import openpyxl

D = "/home/gris/.hermes/workspace/ACTIVE/protein-lab/data/geo"
meta = json.load(open("/tmp/gse324210_meta.json"))

wb = openpyxl.load_workbook(f"{D}/GSE324210/GSE324210_MONOCYTE_RNA_SEQ_healthy.xlsx", read_only=True)
ws = wb["Sheet1"]
rows = ws.iter_rows(values_only=True)
hdr = list(next(rows))
cols = [str(c) for c in hdr[1:] if c]
genes = []
mat = {}
for row in rows:
    g = row[0]
    if not g:
        continue
    genes.append(str(g))
    mat[str(g)] = [float(x) if x is not None else 0.0 for x in row[1:len(cols) + 1]]
print("genes:", len(genes), "muestras:", len(cols))

# grupos por sexo x comparison
def subj_of(c):
    return c.split("_")[0]

def tp_of(c):
    return int(c.split("_T")[1])

def cohort(cols_list):
    return cols_list

f_pre_rest = [c for c in cols if meta[c]["sexo"] == "female" and tp_of(c) == 1]
f_pre_ac = [c for c in cols if meta[c]["sexo"] == "female" and tp_of(c) == 2]
f_post_rest = [c for c in cols if meta[c]["sexo"] == "female" and tp_of(c) == 3]
f_post_ac = [c for c in cols if meta[c]["sexo"] == "female" and tp_of(c) == 4]
m_pre_rest = [c for c in cols if meta[c]["sexo"] == "male" and tp_of(c) == 1]
m_pre_ac = [c for c in cols if meta[c]["sexo"] == "male" and tp_of(c) == 2]
m_post_rest = [c for c in cols if meta[c]["sexo"] == "male" and tp_of(c) == 3]
m_post_ac = [c for c in cols if meta[c]["sexo"] == "male" and tp_of(c) == 4]

# corrección diseño T1-T4 consistente (post acute = T4 only per subject; paper: 4 blood points)
comparisons = {
    "female_acute_pre": (f_pre_ac, f_pre_rest),
    "female_acute_post": (f_post_ac, f_post_rest),
    "male_acute_pre": (m_pre_ac, m_pre_rest),
    "male_acute_post": (m_post_ac, m_post_rest),
    "female_training_rest": (f_post_rest, f_pre_rest),
    "male_training_rest": (m_post_rest, m_pre_rest),
}
import statistics, math

def logfc_ttest(gA, gB):
    """Welch t sobre log2(CPM+1) + BH por comparación."""
    out = {}
    for gi, g in enumerate(genes):
        va = [math.log2((s / max(1e-9, sum(mat[g]))) * 1e6 + 1) if False else None]
    return out

# CPM por muestra (más correcto: totals por columna)
totals = {}
for j, c in enumerate(cols):
    totals[c] = sum(mat[g][j] for g in genes)

def log_cpm(g, c):
    j = cols.index(c)
    return math.log2((mat[g][j] / max(1.0, totals[c])) * 1e6 + 1)

def welch(A, B):
    na, nb = len(A), len(B)
    if na < 2 or nb < 2:
        return 0.0, 1.0, 0.0
    ma = statistics.mean(A); mb = statistics.mean(B)
    va = statistics.variance(A); vb = statistics.variance(B)
    se = math.sqrt(va / na + vb / nb)
    if se == 0:
        return (0.0, 1.0, 0.0)
    t = (ma - mb) / se
    # p-value aproximado por normal (movido por MC después)
    from math import erf, sqrt
    p = 2 * (1 - 0.5 * (1 + erf(abs(t) / sqrt(2))))
    return t, p, ma - mb

def bh(pvals):
    n = len(pvals)
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    qs = [0.0] * n
    prev = 1.0
    for rank, i in enumerate(reversed(order)):
        k = n - rank
        prev = min(prev, pvals[i] * n / k)
        qs[i] = prev
    return qs

results = {}
for name, (A, B) in comparisons.items():
    if not A or not B:
        results[name] = {"error": f"cohortes vacías A={len(A)} B={len(B)}"}
        continue
    rows_res = []
    for g in genes:
        lA = [log_cpm(g, c) for c in A]
        lB = [log_cpm(g, c) for c in B]
        t, p, lfc = welch(lA, lB)
        rows_res.append((g, lfc, p))
    qs = bh([r[2] for r in rows_res])
    sig = [(r[0], r[1], q) for r, q in zip(rows_res, qs) if q < 0.1]
    results[name] = {"n_A": len(A), "n_B": len(B), "n_sig_FDR0.1": len(sig),
                     "up": sorted([(s[0], s[1]) for s in sig if s[1] > 0], key=lambda x: -x[1])[:12],
                     "down": sorted([(s[0], s[1]) for s in sig if s[1] < 0], key=lambda x: x[1])[:12]}

print(json.dumps({k: {"n_sig": v.get("n_sig_FDR0.1")} if isinstance(v, dict) else v for k, v in results.items()}, indent=1))
json.dump(results, open("/home/gris/.hermes/workspace/ACTIVE/protein-lab/results/fme_gse324210_de_v1.json", "w"), indent=1)
print("guardado results/fme_gse324210_de_v1.json")