#!/usr/bin/env python3
"""
au_np_redox_correction.py — FIX #3 (Rev 2026-04-24)
======================================================
Corrección del potencial redox del Au NP confinado dentro del lumen de BFR.

PROBLEMA ORIGINAL:
  SCOPE_B_MARCUS_ANALYSIS.md asumía ΔG° ≈ 0 (Au NP ≈ Au bulk) para el cálculo
  de Marcus. Sin embargo, nanopartículas de Au con < 300 átomos en espacios
  confinados exhiben el "quantum size effect" (QSE): el potencial redox se
  desplaza respecto al Au bulk debido a la energía de carga e²/2C.

CORRECCIÓN:
  Se aplica la aproximación electrostática de Bard/Murray para calcular el
  desplazamiento del potencial redox ΔV = e²/2C, donde C es la capacitancia
  del cluster esférico en dieléctrico de proteína.

  Luego se evalúa cómo ΔG° ≠ 0 modifica la tasa de Marcus.

REFERENCIAS:
  - Murray et al. Science 1998, 280:2098 (Au₅₅ y Au₂₅ redox cuantizado)
  - Bard et al. JACS 2004 (capacitancia NP esférica en solvente proteico)
  - Hicks et al. J Phys Chem B 2005 (coulomb staircase Au NP)

Uso: python au_np_redox_correction.py
"""

import numpy as np

# ─── Constantes físicas ────────────────────────────────────────────────────────
E_CHARGE   = 1.602e-19   # C
KB         = 1.381e-23   # J/K
H_BAR      = 1.055e-34   # J·s
EPS0       = 8.854e-12   # F/m
EV_TO_J    = 1.602e-19   # J/eV
T          = 300.0        # K (fisiológico)

# ─── Parámetros del Au NP (V4b excéntrico) ────────────────────────────────────
R_AU_NP_NM   = 1.0      # nm  (radio del cluster ~2nm diámetro, ~150-200 átomos)
N_ATOMS      = 175      # estimación media (150-200 átomos)

# Dieléctrico efectivo dentro del lumen de ferritina
# Valor estimado: mezcla agua (ε~80) + proteína (ε~4) en proporción ~60/40 lumen
# Resultado empírico de simulaciones MD de ferritinas: ε_eff ≈ 20-40
EPS_EFF_LOW  = 20.0     # límite inferior
EPS_EFF_HIGH = 40.0     # límite superior
EPS_EFF_NOM  = 30.0     # nominal

# Potencial redox de referencia: Au bulk en solución acuosa
# Au³⁺/Au⁰ = +1.52 V vs SHE; pero el potencial de oxido de superficie del Au
# NP relevante para electroquímica en proteínas es el E° de la interfaz Au/tiol.
# Para Au NP funcionalizadas con tioles: E° ≈ +0.0 a +0.2 V vs SHE (estimación)
# Potencial redox Heme B en BFR: E° ≈ -225 mV vs SHE (Quail et al. 1996)
E0_AU_BULK_V  =  0.10   # V vs SHE (Au NP tiol, estimación)
E0_HEME_B_V   = -0.225  # V vs SHE (Heme B BFR, referencia verificada)

print("=" * 68)
print("CORRECCIÓN REDOX Au NP CONFINADO — Quantum Size Effect (QSE)")
print("Rev: 2026-04-24 | Ref: Murray 1998, Bard 2004, Hicks 2005")
print("=" * 68)

# ─── 1. Capacitancia del cluster esférico C = 4πε₀ε_eff·R ──────────────────
R_m = R_AU_NP_NM * 1e-9  # m

print(f"\n1. CAPACITANCIA DEL CLUSTER (C = 4πε₀ε_eff·R)")
print(f"   Radio Au NP    : {R_AU_NP_NM:.1f} nm  (~{N_ATOMS} átomos)")
print(f"   ε_eff (rango)  : {EPS_EFF_LOW} – {EPS_EFF_HIGH}  (nominal: {EPS_EFF_NOM})")

caps = {}
for eps, label in [(EPS_EFF_LOW, "ε=20 (mín)"), (EPS_EFF_NOM, "ε=30 (nom)"), (EPS_EFF_HIGH, "ε=40 (máx)")]:
    C = 4 * np.pi * EPS0 * eps * R_m   # F
    caps[label] = C
    DV = E_CHARGE / (2 * C)            # V  (energía de carga de un electrón = e²/2C)
    DV_mV = DV * 1000
    print(f"   {label}: C = {C:.3e} F | ΔV_QSE = e²/2C = {DV_mV:.1f} mV")

# Usar nominal para el análisis
C_nom = caps["ε=30 (nom)"]
DV_nom_V = E_CHARGE / (2 * C_nom)

# ─── 2. Potencial redox efectivo del Au NP confinado ─────────────────────────
print(f"\n2. POTENCIAL REDOX EFECTIVO DEL Au NP CONFINADO")
print(f"   E°(Au bulk tiol)    : {E0_AU_BULK_V*1000:+.0f} mV vs SHE")
print(f"   ΔV_QSE (nominal)    : +{DV_nom_V*1000:.1f} mV  (desplazamiento anódico por QSE)")
E0_AU_NP_V = E0_AU_BULK_V + DV_nom_V  # El QSE hace más difícil oxidar el NP pequeño
print(f"   E°(Au NP confinado) : {E0_AU_NP_V*1000:+.1f} mV vs SHE  (estimación)")

# ─── 3. ΔG° para el hop Au NP → Heme B ───────────────────────────────────────
print(f"\n3. ΔG° PARA HOP Au NP SURFACE → Heme B")
print(f"   E°(Heme B BFR)      : {E0_HEME_B_V*1000:+.0f} mV vs SHE  (Quail 1996)")
DG0_V = E0_HEME_B_V - E0_AU_NP_V  # ΔG° = -nFΔE = F*(E_heme - E_au) para n=1
DG0_eV = DG0_V  # ya en eV para n=1 (F*ΔV/e = ΔV)
DG0_J  = DG0_eV * EV_TO_J
print(f"   ΔG° = F(E_heme - E_Au NP) = {DG0_V*1000:+.1f} meV  = {DG0_eV:+.4f} eV")
print(f"   Interpretación: {'EXERGÓNICO (ET favorable Au→Heme)' if DG0_V < 0 else 'ENDERGÓNICO (ET desfavorable) — requiere sobretenso'}")

# ─── 4. Efecto de ΔG° ≠ 0 sobre la tasa de Marcus ───────────────────────────
print(f"\n4. IMPACTO DE ΔG° ≠ 0 EN LA TASA DE MARCUS")

# Marcus: k ∝ exp[-(ΔG° + λ)² / (4λkBT)]
# Con ΔG° = 0:  k ∝ exp[-λ / (4kBT)]  (condición de activación basal)
# Con ΔG° ≠ 0:  penalización adicional

LAMBDA_VALUES = {
    "λ=0.5 eV (mín proteína)": 0.5,
    "λ=1.0 eV (típico hemo)":  1.0,
    "λ=1.5 eV (máx proteína)": 1.5,
}
kBT_eV = KB * T / EV_TO_J  # ~0.0259 eV

print(f"\n   Comparación k(ΔG°=0) vs k(ΔG°={DG0_eV*1000:.0f} meV) para distintas λ:")
print(f"   {'λ':30s}  {'k(ΔG°=0) ratio':>15}  {'k(ΔG°≠0) ratio':>16}  {'Factor reducción':>16}")
print(f"   {'─'*30}  {'─'*15}  {'─'*16}  {'─'*16}")

for lbl, lam in LAMBDA_VALUES.items():
    exp_DG0   = np.exp(-(0          + lam)**2 / (4 * lam * kBT_eV))
    exp_DGact = np.exp(-(DG0_eV     + lam)**2 / (4 * lam * kBT_eV))
    ratio = exp_DGact / exp_DG0 if exp_DG0 > 0 else 0
    sign = "↑ mejora" if ratio > 1 else f"↓ x{1/ratio:.1f} reducción"
    print(f"   {lbl:30s}  {exp_DG0:>15.3e}  {exp_DGact:>16.3e}  {sign:>16}")

# ─── 5. Resumen para el Diseño V4b ───────────────────────────────────────────
print(f"""
5. RESUMEN PARA DISEÑO V4b
   ─────────────────────────────────────────────────────────────
   E°(Au NP, ~150 at, ε=30): {E0_AU_NP_V*1000:+.0f} mV vs SHE (vs Au bulk: {E0_AU_BULK_V*1000:+.0f} mV)
   ΔG°(Au→Heme B)          : {DG0_eV*1000:+.0f} meV
   
   DIAGNÓSTICO:
""")
if DG0_eV < 0 and abs(DG0_eV) > 0.1:
    # Exergónico significativo: tasa aumenta respecto a ΔG°=0 en región normal Marcus
    # La región invertida sólo ocurre cuando |ΔG°| > λ; aquí λ_typ=1.0 eV > 0.349 eV
    print("   ✓ ΔG° < 0 (exergónico): la ET Au→Heme B es TERMODINÁMICAMENTE FAVORABLE.")
    print(f"     La tasa de Marcus mejora vs ΔG°=0 (ver tabla arriba).")
    print(f"     |ΔG°| = {abs(DG0_eV)*1000:.0f} meV < λ_típico: NO estamos en región invertida.")
    print(f"     Conclusión: el ΔG° ≠ 0 FAVORECE el diseño V4b.")
    print(f"     ⚠ Incertidumbre: la estimación E°(Au NP tiol) ≈ +100 mV tiene error ±200 mV.")
elif abs(DG0_eV) < 0.1:
    print("   ✓ |ΔG°| < 100 meV: la corrección modifica la tasa < 20× en λ=1 eV.")
    print("     La suposición ΔG°≈0 del SCOPE_B_MARCUS_ANALYSIS es razonable.")
else:
    # Endergónico grande o invertido
    print("   ✗ |ΔG°| > 300 meV endergónico: el diseño necesita ajuste de potencial.")
    print("     Opción: modificar ligandos del Au NP o mutaciones de carga cercanas.")

print(f"""
   ACCIÓN REQUERIDA:
   - Incluir corrección QSE en SCOPE_B_MARCUS_ANALYSIS.md con rango ε_eff 20-40
   - Reportar ΔG° como ≈ {DG0_eV*1000:.0f} meV (estimación, ±100 meV de incertidumbre)
   - Medir E° experimental del Au NP/BFR con voltametría diferencial de pulsos (DPV)
   - Sin dato experimental, reportar k_ET como orden de magnitud, no valor preciso
""")
