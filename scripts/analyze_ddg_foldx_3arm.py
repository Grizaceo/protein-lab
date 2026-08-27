#!/usr/bin/env python3
"""Analyze ddg_foldx_3arm_v1 battery results (pre-registered stats in SPEC JSON).
Reads Dif_{esm3,blosum62,matched}.fxout, collapses to n=133 unique (pos,wt),
runs two-sided paired Wilcoxon with Holm correction + |ddG|<=10 trimming."""
import re, json, sys
from itertools import combinations

BASE = "/mnt/c/temp/foldx5/battery_foldx"
ARMS = ["esm3", "blosum62", "matched"]
N_PRE = 133
ALPHA = 0.05

def parse_dif(path):
    """Return list of (pos, wt1, mut1, ddG). ddG = col2 of Dif fxout (kcal/mol)."""
    rows = []
    for line in open(path):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2 or not parts[0].endswith(".pdb") or "_" not in parts[0]:
            continue
        try:
            ddg = float(parts[1])
        except ValueError:
            continue
        rows.append((parts[0], ddg))
    return rows

def mut_key_from_pdbrow(pdbname, arm_lists):
    """Dif rows are named <base>_<i>.pdb in submission order -> map to mutation strings."""
    idx = int(re.search(r"_(\d+)\.pdb$", pdbname).group(1))
    return arm_lists[idx - 1]

arm_lists = {}
for arm in ARMS:
    arm_lists[arm] = [l.strip().rstrip(";") for l in open(f"{BASE}/individual_list_{arm}.txt") if l.strip()]

def key_of(mutstr):
    m = re.match(r"^([A-Z])([A-Z])(\d+)([A-Z])$", mutstr)
    return (int(m.group(3)), m.group(1))  # (pos, wt)

data = {}
for arm in ARMS:
    rows = parse_dif(f"{BASE}/Dif_{arm}.fxout")
    assert len(rows) == len(arm_lists[arm]), f"{arm}: {len(rows)} rows vs {len(arm_lists[arm])} list lines"
    d = {}
    for pdbrow, ddg in rows:
        k = key_of(mut_key_from_pdbrow(pdbrow, arm_lists[arm]))
        d[k] = ddg
    data[arm] = d
    print(f"{arm}: {len(d)} unique (pos,wt) keys")

common = set(data["esm3"]) & set(data["blosum62"]) & set(data["matched"])
print(f"common keys across arms: {len(common)} (pre-registered n={N_PRE})")
if len(common) != N_PRE:
    print(f"WARNING: coverage mismatch {len(common)} != {N_PRE} — kill criterion check needed")

keys = sorted(common)
import subprocess, tempfile, math
from statistics import median, mean

def wilcoxon(x, y):
    """Two-sided paired Wilcoxon signed-rank with normal approximation (scipy if present)."""
    try:
        from scipy.stats import wilcoxon as w
        st, p = w(x, y, zero_method="wilcox", alternative="two-sided")
        return st, p
    except Exception:
        d = [a - b for a, b in zip(x, y)]
        d = [v for v in d if v != 0]
        n = len(d)
        ranks = sorted(range(len(d)), key=lambda i: abs(d[i]))
        rp = [0] * len(d)
        i = 0
        while i < len(ranks):
            j = i
            while j + 1 < len(ranks) and abs(d[ranks[j + 1]]) == abs(d[ranks[i]]):
                j += 1
            avg = (i + j) / 2 + 1
            for k2 in range(i, j + 1):
                rp[ranks[k2]] = avg
            i = j + 1
        Wp = sum(rp[i2] for i2 in range(len(d)) if d[i2] > 0)
        mu = n * (n + 1) / 4
        sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
        z = (Wp - mu) / sigma
        p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
        return Wp, p

def rank_biserial(x, y):
    d = [a - b for a, b in zip(x, y)]
    d = [v for v in d if v != 0]
    n = len(d)
    ranks = sorted(range(len(d)), key=lambda i: abs(d[i]))
    rp = [0] * len(d)
    i = 0
    while i < len(ranks):
        j = i
        while j + 1 < len(ranks) and abs(d[ranks[j + 1]]) == abs(d[ranks[i]]):
            j += 1
        avg = (i + j) / 2 + 1
        for k2 in range(i, j + 1):
            rp[ranks[k2]] = avg
        i = j + 1
    Wp = sum(rp[i2] for i2 in range(len(d)) if d[i2] > 0)
    Wm = sum(rp[i2] for i2 in range(len(d)) if d[i2] < 0)
    return (Wp - Wm) / (Wp + Wm)

ks = sorted(common)
raw = {arm: [data[arm][k] for k in ks] for arm in ARMS}
trim = {arm: [v if abs(v) <= 10 else None for v in raw[arm]] for arm in ARMS}
keep = [i for i in range(len(ks)) if trim["esm3"][i] is not None and trim["blosum62"][i] is not None and trim["matched"][i] is not None]

print("\n=== DESCRIPTIVE (n=133) ===")
for arm in ARMS:
    v = raw[arm]
    print(f"{arm:10s} mean={mean(v):+.3f} median={median(v):+.3f} max={max(v):+.2f} min={min(v):+.2f}")
print(f"\n=== TRIMMED |ddG|<=10 (n={len(keep)}) ===")
for arm in ARMS:
    v = [trim[arm][i] for i in keep]
    print(f"{arm:10s} mean={mean(v):+.3f} median={median(v):+.3f}")

def holm(pvals):
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    m = len(pvals)
    adj = [0] * len(pvals)
    running = 0
    for rank, i in enumerate(order):
        val = pvals[i] * (m - rank)
        running = max(running, val)
        adj[i] = min(1.0, running)
    return adj

print("\n=== PAIRED TESTS (n=133, two-sided Wilcoxon) ===")
comps = [("esm3", "blosum62"), ("esm3", "matched"), ("blosum62", "matched")]
pvals, details = [], []
for a, b in comps:
    x, y = raw[a], raw[b]
    st, p = wilcoxon(x, y)
    rbc = rank_biserial(x, y)
    xt = [trim[a][i] for i in keep]; yt = [trim[b][i] for i in keep]
    stt, pt = wilcoxon(xt, yt)
    rbct = rank_biserial(xt, yt)
    details.append((a, b, st, p, rbc, stt, pt, rbct))
    pvals.append(p)
adj = holm(pvals)
for (a, b, st, p, rbc, stt, pt, rbct), pa in zip(details, adj):
    print(f"{a} vs {b}: W={st:.1f} p={p:.3e} r_rb={rbc:+.3f} | trimmed: p={pt:.3e} r_rb={rbct:+.3f} | Holm-adj p={pa:.3e}")

print("\n=== VERDICT LOGIC (pre-registered) ===")
p_eb = dict(zip([(a, b) for a, b, *_ in details], adj))[("esm3", "blosum62")]
rbc_eb = details[0][4]
if p_eb < ALPHA and rbc_eb < -0.3:
    print("H2 REVERSAL: ESM3 beats BLOSUM62 under FoldX (p<0.05 Holm-adj, r<-0.3) -> line re-opens")
elif p_eb >= ALPHA:
    print("H1 CONFIRMS EvoEF2: no significant ESM3 advantage over BLOSUM62 under FoldX")
else:
    print("H3 INCONCLUSIVE zone: significant but small effect — read details")