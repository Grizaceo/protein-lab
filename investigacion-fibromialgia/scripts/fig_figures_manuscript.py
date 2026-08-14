#!/usr/bin/env python3
"""
Figuras del manuscrito v2.10 — E1b deconvolución COL9A1/PTN.

Genera las 3 figuras centrales del análisis de ajuste composicional:
  Fig 1 — Forest plot M1/M2/M3 (eje opioide + COL9A1/PTN)
  Fig 2 — Barrido de variantes de deconvolución (4 implementaciones)
  Fig 3 — Control negativo (600 genes al azar)

Output: results/fig1_forest_m1m2m3.png, fig2_variant_sweep.png, fig3_negative_control.png
"""

import pathlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

REPO = pathlib.Path(__file__).resolve().parent.parent
ANALISIS = REPO / 'analisis'
RESULTS = REPO / 'results'
RESULTS.mkdir(exist_ok=True)

# Estilo consistente con el manuscrito (blanco, limpio, sin ornamentación)
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 9,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.08,
})

# Colores: eje opioide = gris, COL9A1/PTN = azul oscuro (hallazgo principal)
OPIOID_COLOR = '#777777'
ECM_COLOR = '#1f4e79'
ECM_EDGE = '#0d2b45'
THRESHOLD = 0.05


def load_results():
    """Carga los CSVs de salida del script E1b."""
    main = pd.read_csv(ANALISIS / 'E1b_deconvolution_col9a1_ptn.csv')
    sweep = pd.read_csv(ANALISIS / 'E1b_variant_sweep.csv')
    null = pd.read_csv(ANALISIS / 'E1b_negative_control_random_genes.csv')
    return main, sweep, null


def fig1_forest_m1m2m3(main_df):
    """Forest plot de p-values para M1, M2, M3."""
    genes = list(main_df['Gene'])
    n = len(genes)
    y_pos = np.arange(n)

    fig, axes = plt.subplots(1, 3, figsize=(10, max(3.5, n * 0.45)), sharey=True)

    models = [
        ('p_group_only', 'M1\ngrupo', '#444444'),
        ('p_group_sex', 'M2\n+ sexo', '#555555'),
        ('p_full_adj', 'M3\n+ composición', '#1f4e79'),
    ]

    for ax, (col, title, color) in zip(axes, models):
        vals = main_df[col].values
        colors = [ECM_COLOR if g in ('COL9A1', 'PTN') else OPIOID_COLOR for g in genes]
        ax.barh(y_pos, vals, color=colors, height=0.6, edgecolor='white', linewidth=0.5)
        ax.axvline(THRESHOLD, color='#cc0000', linestyle='--', linewidth=0.8, alpha=0.7, label=f'p = {THRESHOLD}')
        ax.set_xscale('log')
        ax.set_xlim(1e-9, 2)
        ax.set_title(title, fontsize=10, fontweight='bold', pad=8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(genes, fontsize=8)
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0e'))
        ax.tick_params(axis='x', labelsize=7)
        ax.invert_yaxis()

        # Etiquetas de sobrevivientes
        for i, (v, g) in enumerate(zip(vals, genes)):
            if v < THRESHOLD:
                ax.text(v * 1.5, i, f'p = {v:.2f}', va='center', fontsize=6.5,
                        color=ECM_COLOR if g in ('COL9A1', 'PTN') else '#333333')

    axes[0].set_ylabel('')
    axes[1].set_xlabel('p-value (log scale)', fontsize=9, labelpad=8)
    fig.suptitle('Sensitivity analysis: nested models on log₂(FPKM+1)', fontsize=11, fontweight='bold', y=1.02)
    fig.tight_layout()
    out = RESULTS / 'fig1_forest_m1m2m3.png'
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f'  Guardado: {out.name}')
    return out


def fig2_variant_sweep(sweep_df):
    """Barrido de variantes de deconvolución (4 implementaciones)."""
    genes = list(sweep_df['Gene'])
    variants = [c for c in sweep_df.columns if c.startswith('NNLS') or c.startswith('scores')]
    n_genes = len(genes)
    n_var = len(variants)

    x = np.arange(n_genes)
    width = 0.18

    fig, ax = plt.subplots(figsize=(10, max(3.5, n_genes * 0.4)))

    colors = ['#1f4e79', '#2e75b6', '#5b9bd5', '#9dc3e6']
    for i, var in enumerate(variants):
        vals = sweep_df[var].values
        offset = (i - n_var / 2 + 0.5) * width
        bars = ax.barh(x + offset, vals, width, label=var, color=colors[i % len(colors)],
                       edgecolor='white', linewidth=0.4)

    ax.axvline(THRESHOLD, color='#cc0000', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.set_xscale('log')
    ax.set_xlim(1e-9, 2)
    ax.set_yticks(x)
    ax.set_yticklabels(genes, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel('p-value (log scale)', fontsize=9, labelpad=8)
    ax.set_title('Deconvolution variant sweep — 4 implementations', fontsize=11, fontweight='bold', pad=10)
    ax.legend(fontsize=7, loc='lower right', framealpha=0.9, edgecolor='#cccccc')
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0e'))
    ax.tick_params(axis='x', labelsize=7)

    # Etiquetas de veredicto
    for i, g in enumerate(genes):
        verdict = sweep_df.loc[sweep_df['Gene'] == g, 'veredicto'].values[0]
        ax.text(1.5, i, verdict, va='center', fontsize=6.5,
                color=ECM_COLOR if g in ('COL9A1', 'PTN') else '#555555',
                fontstyle='italic')

    fig.tight_layout()
    out = RESULTS / 'fig2_variant_sweep.png'
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f'  Guardado: {out.name}')
    return out


def fig3_negative_control(null_df):
    """Control negativo: distribución de p-values en 600 genes al azar."""
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))

    # Panel A: histograma de p-values en M2 (sex-adjusted)
    ax = axes[0]
    m2_sig = null_df[null_df['p_group_sex'] < 0.05]
    ax.hist(null_df['p_group_sex'], bins=40, color='#aaaaaa', edgecolor='white',
            linewidth=0.5, alpha=0.7, label=f'All genes (n={len(null_df)})')
    ax.hist(m2_sig['p_group_sex'], bins=20, color='#5b9bd5', edgecolor='white',
            linewidth=0.5, alpha=0.8, label=f'M2 p < 0.05 (n={len(m2_sig)})')
    ax.axvline(THRESHOLD, color='#cc0000', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.set_xlabel('M2 p-value (+ sexo)', fontsize=9, labelpad=6)
    ax.set_ylabel('Count', fontsize=9)
    ax.set_title('(A) Sex-adjusted p-value distribution', fontsize=9, fontweight='bold')
    ax.legend(fontsize=7, framealpha=0.9)
    ax.tick_params(labelsize=7)

    # Panel B: supervivencia M3 vs M2
    ax = axes[1]
    m2_sig_genes = null_df[null_df['p_group_sex'] < 0.05]
    m3_sig = m2_sig_genes[m2_sig_genes['p_full_adj'] < 0.05]
    not_m3_sig = m2_sig_genes[m2_sig_genes['p_full_adj'] >= 0.05]

    ax.hist(not_m3_sig['p_full_adj'], bins=30, color='#cccccc', edgecolor='white',
            linewidth=0.5, alpha=0.7, label=f'Not survive M3 (n={len(not_m3_sig)})')
    ax.hist(m3_sig['p_full_adj'], bins=15, color='#1f4e79', edgecolor='white',
            linewidth=0.5, alpha=0.8, label=f'Survive M3 (n={len(m3_sig)})')
    ax.axvline(THRESHOLD, color='#cc0000', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.set_xlabel('M3 p-value (+ composición)', fontsize=9, labelpad=6)
    ax.set_ylabel('Count', fontsize=9)
    ax.set_title('(B) Composition-adjusted (M2 survivors only)', fontsize=9, fontweight='bold')
    ax.legend(fontsize=7, framealpha=0.9)
    ax.tick_params(labelsize=7)

    # Anotación de porcentaje
    pct = 100 * len(m3_sig) / len(m2_sig_genes) if len(m2_sig_genes) > 0 else 0
    ax.text(0.95, 0.95, f'{pct:.0f}% survive M3', transform=ax.transAxes,
            fontsize=9, fontweight='bold', color=ECM_COLOR,
            ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=ECM_COLOR, alpha=0.9))

    fig.suptitle('Negative control: 600 random expressed genes (markers excluded)',
                 fontsize=11, fontweight='bold', y=1.02)
    fig.tight_layout()
    out = RESULTS / 'fig3_negative_control.png'
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f'  Guardado: {out.name}')
    return out


def main():
    print("Generando figuras del manuscrito v2.10 — E1b deconvolución...")
    main_df, sweep_df, null_df = load_results()
    print(f"  Cargados: main={len(main_df)} genes, sweep={len(sweep_df)} genes, null={len(null_df)} genes")

    f1 = fig1_forest_m1m2m3(main_df)
    f2 = fig2_variant_sweep(sweep_df)
    f3 = fig3_negative_control(null_df)

    print(f"\n  3 figuras generadas en {RESULTS}/")
    return f1, f2, f3


if __name__ == '__main__':
    main()
