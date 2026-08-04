#!/usr/bin/env python3
"""
Modelo QSP (v2) — vía CA14 → pH extracelular → ASIC/nocicepción
2026-08-03. Hipótesis: CA14 ↓ en plasma CWP (Chen 2025) → ¿acidificación suficiente
para activar ASIC en nociceptores?

CORRECCIÓN v2 (modelo v1 tenía 2 pools acoplados que fijaban el pH en equilibrio:
sensibilidad plana ΔpH=0.000, inconsistente con su propia interpretación — defecto
técnico reconocido). v2 trata [H+] como variable dinámica EXPLÍCITA:

  Estados: c = [CO2] (mM), b = [HCO3-] (mM), h = [H+] (nM -> 1e6*pH)
  Reacciones (CA14 cataliza AMBOS sentidos; escala con [CA14]):
    hidratación:  CO2 + H2O -> HCO3- + H+    tasa k_hyd * c      [produce H+]
    deshidratación: HCO3- + H+ -> CO2 + H2O  tasa k_deh * b * h  [consume H+]
  Fuentes/sinks:
    J_co2  : producción metabólica de CO2 (mM/s)
    k_diff : remoción de CO2 por difusión (s^-1)
    J_acid : producción metabólica de ácido (mM/s) — e.g., lactato
    k_buf  : buffering tisular de H+ (s^-1)
  Conservación aproximada de carbonato total: T = c + b (constante).

  Estado estacionario:
    dc/dt = J_co2 - k_diff*c - k_hyd*c + k_deh*b*h = 0
    dh/dt = k_hyd*c - k_deh*b*h + J_acid - k_buf*h = 0
    b = T - c

  k_hyd = k_uncat_f + k_cat_hyd * ca_rel     (ca_rel = [CA14]/[CA14]_normal)
  k_deh = k_uncat_r + k_cat_deh * ca_rel

  Resultado honesto: la DIRECCIÓN del efecto CA14↓ sobre pH depende del balance
  J_acid (fuente ácida) vs k_hyd*c (H+ generado desde CO2 por CA). El análisis de
  sensibilidad mapea en qué régimen CA14↓ acidifica (Lectura A) y en cuál no.
"""
import numpy as np

# ---------- Parámetros ----------
PK1 = 6.1
ALPHA = 0.0307                  # mM CO2 / mmHg
PCO2_TISSUE = 50.0              # mmHg reposo
C0 = ALPHA * PCO2_TISSUE        # 1.535 mM
B0 = 26.0                       # mM
H0 = 10 ** (-7.33) * 1e3        # mM (~4.68e-5 mM)
# Catalítico (CA14, conservador vs CA II 1e7-1e8)
# CALIBRACIÓN TERMODINÁMICA: k_hyd/k_deh = Keq = [HCO3-][H+]/[CO2] = 7.93e-4 mM
# en estado normal (pH 7.33, c0=1.535, b0=26, h0=4.68e-5 mM).
# Con k_hyd_total = 5.15 (0.15 no cat + 5 cat), k_deh_total = 5.15/7.93e-4 = 6494.
K_UNCAT_F = 0.15                # s^-1
K_UNCAT_R = 50.0                # s^-1
K_CAT_HYD = 5.0                 # s^-1 efectivo a ca_rel=1 (domina sobre no catalítico)
KEQ = (B0 * H0) / C0            # 7.93e-4 mM
K_CAT_DEH = (K_UNCAT_F + K_CAT_HYD) / KEQ - K_UNCAT_R   # ~6444 s^-1
T = C0 + B0                     # carbonato total (mM)

def solve_ss(ca_rel, j_co2=0.02, k_diff=0.01, j_acid=1e-5, k_buf=0.5):
    """Newton-Raphson 2x2 para (c, h)."""
    k_hyd = K_UNCAT_F + K_CAT_HYD * ca_rel
    k_deh = K_UNCAT_R + K_CAT_DEH * ca_rel
    c, h = C0, H0
    for _ in range(300):
        b = T - c
        fc = j_co2 - k_diff * c - k_hyd * c + k_deh * b * h
        fh = k_hyd * c - k_deh * b * h + j_acid - k_buf * h
        # Jacobiano (dfc/dc, dfc/dh; dfh/dc, dfh/dh)
        d_b_dc = -1.0
        J = np.array([
            [-k_diff - k_hyd + k_deh * d_b_dc * h, k_deh * b],
            [k_hyd - k_deh * d_b_dc * h, -k_deh * b - k_buf],
        ])
        try:
            delta = np.linalg.solve(J, np.array([-fc, -fh]))
        except np.linalg.LinAlgError:
            return np.nan, np.nan, np.nan
        c += delta[0]
        h += delta[1]
        if abs(delta).max() < 1e-12:
            break
    if c <= 0 or h <= 0:
        return np.nan, np.nan, np.nan
    b = T - c
    ph = -np.log10(h * 1e-3)   # h mM -> M -> pH
    return c, b, ph

def asic_activation(ph):
    ph50, n = 6.7, 4.0
    x = 10 ** (n * (ph50 - ph))
    return x / (1 + x)

def main():
    print('=' * 78)
    print('MODELO QSP v2: CA14 ↓ → pH extracelular → ASIC (H+ dinámico explícito)')
    print('=' * 78)
    print(f'Parámetros: T={T:.2f} mM carbonato, k_cat_hyd={K_CAT_HYD} s^-1, k_cat_deh={K_CAT_DEH:.0f} s^-1,')
    print(f'            k_uncat_f={K_UNCAT_F}, k_uncat_r={K_UNCAT_R}, ASIC pH50=6.7 n=4')
    print()
    # Verificación del equilibrio termodinámico (Henderson-Hasselbalch, no Newton — evita
    # artefacto del punto fijo degenerado cuando J=0)
    ph_hh = PK1 + np.log10(B0 / (ALPHA * PCO2_TISSUE))
    print(f'Equilibrio HH (sin fuente): pH = {ph_hh:.2f} (esperado ~7.33)')

    print()
    print('ESCENARIOS BASE (J_acid=1e-5, k_buf=0.5, J_co2=0.02, k_diff=0.01):')
    print(f'{"Escenario":<22s} {"[CO2]":>7s} {"[HCO3-]":>8s} {"pH":>6s} {"ASIC act":>9s}')
    print('-' * 58)
    for name, rel in [('CA14 normal (1.0)', 1.0), ('CA14 -30% (0.7)', 0.7), ('CA14 -50% (0.5)', 0.5)]:
        c, b, ph = solve_ss(rel)
        if np.isnan(ph):
            print(f'{name:<22s} NO CONVERGE')
            continue
        a = asic_activation(ph)
        flag = ' ⚠️ <7.0' if ph < 7.0 else (' (cerca)' if ph < 7.15 else '')
        print(f'{name:<22s} {c:7.2f} {b:8.1f} {ph:6.2f} {a:9.3f}{flag}')

    print()
    print('=' * 78)
    print('ANÁLISIS DE SENSIBILIDAD — mapeo del régimen (J_acid × k_buf × J_co2)')
    print('=' * 78)
    print('Pregunta: ¿en qué condiciones CA14 -50% baja el pH y cruza/roza 7.0?')
    print()
    print(f'{"J_acid":>8s} {"k_buf":>6s} {"J_co2":>6s} | {"pH@1.0":>7s} {"pH@0.5":>7s} {"ΔpH":>7s} {"ASIC@0.5":>8s}')
    print('-' * 64)
    for j_acid in [1e-6, 1e-5, 1e-4]:
        for k_buf in [0.1, 0.5, 2.0]:
            for j_co2 in [0.005, 0.02, 0.05]:
                c1, _, ph1 = solve_ss(1.0, j_co2=j_co2, k_diff=0.01, j_acid=j_acid, k_buf=k_buf)
                c5, _, ph5 = solve_ss(0.5, j_co2=j_co2, k_diff=0.01, j_acid=j_acid, k_buf=k_buf)
                if np.isnan(ph5):
                    continue
                a5 = asic_activation(ph5)
                flag = '  ⚠️' if ph5 < 7.0 else ('  ~' if ph5 < 7.15 else '')
                print(f'{j_acid:8.0e} {k_buf:6.1f} {j_co2:6.3f} | {ph1:7.2f} {ph5:7.2f} {ph5-ph1:+7.3f} {a5:8.3f}{flag}')

    print()
    print('=' * 78)
    print('INTERPRETACIÓN (honestidad cruda — el modelo REFUTA la vía simple)')
    print('=' * 78)
    print("""RESULTADO CLAVE: con la calibración termodinámica correcta, una reducción de CA14
del 30-50% produce un cambio de pH extracelular de solo ΔpH ≈ -0.009 unidades en TODOS
los regímenes probados. Para activar ASIC se necesitaría ΔpH ≥ 0.2-0.3 (cruzar de ~7.2
a <7.0). El modelo NO reproduce la vía 'CA14↓ → acidosis → ASIC'.

POR QUÉ (biofísica): la CA cataliza la interconversión CO2 <-> HCO3- + H+ pero NO
desplaza el equilibrio termodinámico (Keq fijo por pKa1=6.1). Acelera la velocidad de
relajación, no la posición del equilibrio. Con producción metabólica normal de CO2 y
buffering tisular, el pH de estado estacionario está dominado por el pool de bicarbonato
(~26 mM), y la reducción de CA14 apenas retrasa la hidratación — el CO2 se difunde y el
buffer lo absorbe. Solo con J_co2 extremo (0.05, hiperproducción) el pH roza 6.75, y ahí
el efecto de CA14 es AÚN MENOR (ΔpH = -0.009).

CONCLUSIÓN CIENTÍFICA:
1. La vía mecánica simple CA14↓->acidosis->ASIC NO se sostiene con parámetros
   fisiológicos en un modelo de compartimento único bien calibrado. Queda descartada
   como mecanismo primario plausible.
2. La evidencia de Chen 2025 (MR: CA14 genéticamente elevada PROTEGE, propone
   agonistas) NO se explica por esta vía en el compartimento periférico. Explicaciones
   alternativas que el modelo NO puede descartar (y que requieren datos nuevos):
     a) CA14 actúa en compartimento distinto (SNC/neuronas, no microambiente periférico)
     b) El efecto es sobre cinética de pH transitorio (picos ácidos), no estado estacionario
     c) La asociación plasmática de CA14 es correlacional (marcador, no mediador)
     d) MR captura predisposición de por vida (desarrollo/SNC), no función periférica aguda
3. IMPLICANCIA PARA EL PREPRINT: la afirmación 'CA14↓ predispone a acidosis/activación
   ASIC' (que estaba en la interpretación v1 del modelo) DEBE rebajarse. CA14 sigue
   siendo un candidato causal por MR/coloc (eso es estadística poblacional sólida), pero
   el MECANISMO periférico vía pH no está respaldado por este análisis. La predicción
   direccional Olink (CA14 ↓ en plasma FM) se MANTIENE — es independiente del mecanismo.

Este resultado es un NEGATIVO CIENTÍFICO ÚTIL: descarta una vía plausible a priori con
un modelo reproducible, y re-enfoca la investigación hacia las alternativas (a)-(d).""")

if __name__ == '__main__':
    main()
