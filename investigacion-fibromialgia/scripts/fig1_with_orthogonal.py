#!/usr/bin/env python3
"""
Figura 1 (v2.11) — forest plot M1/M2/M3 + panel M4 ortogonal (drop VIF>5).

Reusa el loader y `run_model` de vif_sensitivity_opioid_axis.py para calcular
los p-values del modelo ortogonal sobre los 9 genes del panel E1b, y emite
results/fig1_forest_m1m2m3.png con 4 paneles.

El panel M4 muestra que el colapso del eje opioide en M3 (full fractions) es
colinealidad: al quitar fracciones de VIF>5, TACR1/OPRM1/TAC1 recuperan
significancia (p<0.05), mientras COL9A1/PTN siguen significativos (robustos).
"""
import pathlib, importlib.util
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

REPO = pathlib.Path(__file__).resolve().parent.parent
RESULTS = REPO / 'results'
RESULTS.mkdir(exist_ok=True)
THRESHOLD = 0.05

# Cargar la lógica VIF ya validada (loader + run_model)
spec = importlib.util.spec_from_file_location(
    "vifmod", REPO / 'scripts' / 'vif_sensitivity_opioid_axis.py')
vifmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vifmod)

# Genes del panel E1b (mismos que el CSV de Fig1 original)
e1b = pd.read_csv(REPO / 'analisis' / 'E1b_deconvolution_col9a1_ptn.csv')
genes = list(e1b['Gene'])

# p-values de los CSV originales (M1, M2, M3 full)
p_m1 = dict(zip(e1b['Gene'], e1b['p_group_only']))
p_m2 = dict(zip(e1b['Gene'], e1b['p_group_sex']))
p_m3 = dict(zip(e1b['Gene'], e1b['p_full_adj']))

# M4 ortogonal: re-calcular con run_model drop_high=True (VIF>5 quitados)
ortho = vifmod.run_model(genes, drop_high=True)
p_m4 = {g: (ortho[g]['p'] if g in ortho and 'p' in ortho[g] else np.nan) for g in genes}

print("=== M4 (ortogonal, drop VIF>5) ===")
for g in genes:
    print(f"  {g:8s} p={p_m4[g]:.4f}  sig={p_m4[g] < THRESHOLD}")

# ---- Figura 4 paneles ----
OPIOID = ['OPRM1', 'OPRK1', 'OPRD1', 'TACR1', 'TAC1', 'PENK', 'POMC']
ECM = ['COL9A1', 'PTN']
OPIOID_COLOR = '#777777'
ECM_COLOR = '#1f4e79'
ECM_EDGE = '#0d2b45'

n = len(genes)
y_pos = np.arange(n)

panels = [
    (p_m1, 'M1\ngrupo', '#444444'),
    (p_m2, 'M2\n+ sexo', '#555555'),
    (p_m3, 'M3\n+ composición\n(full)', '#1f4e79'),
    (p_m4, 'M4\n+ composición\n(ortogonal, VIF>5)', '#7a1f4e'),
]

fig, axes = plt.subplots(1, 4, figsize=(13, max(3.5, n * 0.5)), sharey=True)
for ax, (pdict, title, color) in zip(axes, panels):
    vals = np.array([pdict.get(g, np.nan) for g in genes], dtype=float)
    colors = [ECM_COLOR if g in ECM else OPIOID_COLOR for g in genes]
    ax.barh(y_pos, vals, color=colors, height=0.6, edgecolor='white', linewidth=0.5)
    ax.axvline(THRESHOLD, color='#cc0000', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.set_xscale('log')
    ax.set_xlim(1e-9, 2)
    ax.set_title(title, fontsize=9.5, fontweight='bold', pad=8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(genes, fontsize=8)
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0e'))
    ax.tick_params(axis='x', labelsize=7)
    ax.invert_yaxis()
    for i, (v, g) in enumerate(zip(vals, genes)):
        if not np.isnan(v) and v < THRESHOLD:
            ax.text(v * 1.5, i, f'p = {v:.2f}', va='center', fontsize=6.2,
                    color=ECM_COLOR if g in ECM else '#333333')

axes[0].set_ylabel('Gen', fontsize=9)
axes[1].set_xlabel('p-value (log scale)', fontsize=9, labelpad=8)
fig.suptitle('Sensitivity analysis: nested models on log₂(FPKM+1) — incl. M4 orthogonal (drop VIF>5)',
             fontsize=11, fontweight='bold', y=1.02)
# Leyenda
from matplotlib.patches import Patch
leg = [Patch(facecolor=ECM_COLOR, label='COL9A1/PTN (hallazgo principal)'),
       Patch(facecolor=OPIOID_COLOR, label='eje opioide/taquicinina')]
axes[3].legend(handles=leg, fontsize=6.5, loc='lower right', framealpha=0.9, edgecolor='#cccccc')
fig.tight_layout()
out = RESULTS / 'fig1_forest_m1m2m3.png'
fig.savefig(out, dpi=300)
plt.close(fig)
print(f"  Guardado: {out.name}")
