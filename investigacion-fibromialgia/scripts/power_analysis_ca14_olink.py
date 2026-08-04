#!/usr/bin/env python3
"""
Simulación Monte Carlo de poder estadístico — Protocolo Olink FM (CA14 principal)
2026-08-03. Rediseño del power calculation tras el pivot UKB: el candidato principal
ya no es IL-6 (FC>=1.6) sino CA14 (dirección plasmática ↓, efecto esperado pequeño-medio).

Supuestos (fieles al análisis real, no optimistas):
- Escala NPX (log2-like): distribución normal en log2.
- CV técnico Olink: 16.5% mediana (comparación SomaScan vs Olink, medRxiv 2024.07.11.24310161).
  -> sd_tech_log2 = CV/100 / ln(2) (CV en escala lineal -> sd en log2).
- Test: Mann-Whitney U de dos colas (NPX no-normal, como en validate_fm_biomarkers_iter2.py).
- Alpha = 0.05, ratio FM:HC = 1:1.
- Efectos simulados: d = 0.3, 0.4, 0.5, 0.6 (Cohen's d en escala log2, es decir cambio de
  NPX; cubre el rango plausible de CA14 según la literatura de plasma proteomics en dolor).
- Estratificación por sexo: FM ~90% mujeres (epidemiología FM), HC emparejado por sexo.

Salida: tabla poder vs n por efecto, recomendación de n para poder 0.80/0.90.
"""
import numpy as np
from scipy import stats
import sys

RNG = np.random.default_rng(42)
ALPHA = 0.05
CV_OLINK = 0.165
SD_TECH_LOG2 = CV_OLINK / np.log(2)  # ~0.238 en log2
N_SIMS = 2000
EFFECTS = [0.3, 0.4, 0.5, 0.6]
NS = [15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100]
FEMALE_FRAC = 0.90

def simulate_power(n_per_group, d, rng, n_sims=N_SIMS):
    """Poder de Mann-Whitney para n por grupo, efecto d (log2), con ruido técnico."""
    hits = 0
    # En escala log2, d = (mu_FM - mu_HC)/sd_biologico. sd_total = sqrt(sd_bio^2 + sd_tech^2)
    # Asumimos sd_bio = 1.0 (típico NPX) -> sd_total = sqrt(1 + sd_tech^2)
    sd_total = np.sqrt(1.0 + SD_TECH_LOG2 ** 2)
    mu_hc = 0.0
    mu_fm = d * 1.0  # d definido sobre sd_bio
    for _ in range(n_sims):
        fm = rng.normal(mu_fm, sd_total, n_per_group)
        hc = rng.normal(mu_hc, sd_total, n_per_group)
        u, p = stats.mannwhitneyu(fm, hc, alternative='two-sided')
        if p < ALPHA:
            hits += 1
    return hits / n_sims

def main():
    print(f'Simulación Monte Carlo poder — Olink FM (CA14). N sims={N_SIMS}, alpha={ALPHA}, CV_tech={CV_OLINK:.1%}')
    print(f'sd_tech_log2={SD_TECH_LOG2:.3f}, sd_total={np.sqrt(1+SD_TECH_LOG2**2):.3f}')
    print(f'{"n/grupo":>8s}', end='')
    for d in EFFECTS:
        print(f'  d={d:.1f}'.rjust(10), end='')
    print()
    print('-' * 58)
    rec = {}
    for n in NS:
        row = f'{n:>8d}'
        for d in EFFECTS:
            p = simulate_power(n, d, RNG)
            row += f'{p:10.3f}'
            if p >= 0.80 and d not in rec:
                rec[d] = n
        print(row)
    print()
    print('Recomendación (primer n con poder >= 0.80):')
    for d in EFFECTS:
        if d in rec:
            print(f'  d={d:.1f} -> n={rec[d]} por grupo (total {rec[d]*2})')
        else:
            print(f'  d={d:.1f} -> n>100 por grupo (no alcanza 0.80 en el rango)')

    # --- Estratificación por sexo: poder efectivo si se analiza solo mujeres ---
    print()
    print('Estratificación por sexo (FM ~90% mujeres): si el análisis se restringe a mujeres,')
    print('el n efectivo por grupo se reduce. Poder para n=40 por grupo con 90% mujeres:')
    n_eff = int(40 * FEMALE_FRAC)
    for d in EFFECTS:
        p = simulate_power(n_eff, d, RNG)
        print(f'  d={d:.1f} -> n_eff={n_eff} por grupo: poder={p:.3f}')

if __name__ == '__main__':
    main()
