# SIMULACIÓN QSP — VÍA CA14 → pH EXTRACELULAR → ASIC (resultado NEGATIVO)

**Fecha:** 2026-08-03
**Script:** `scripts/qsp_ca14_ph_nociception.py` (reproducible, numpy + Newton-Raphson 2x2)
**Pregunta:** ¿la reducción de CA14 en CWP/FM (top-10 downregulated en UKB, Chen 2025) puede
producir acidosis extracelular suficiente para activar canales ASIC en nociceptores?

---

## VEREDICTO: LA VÍA PERIFÉRICA SIMPLE NO SE SOSTIENE

| Escenario | pH | ΔpH vs CA14 normal | Activación ASIC |
|-----------|-----|--------------------|-----------------|
| CA14 normal (1.0) | 7.21 | — | 0.009 |
| CA14 −30% (0.7) | 7.20 | −0.009 | 0.010 |
| CA14 −50% (0.5) | 7.20 | **−0.009** | 0.010 |

Para activar ASIC (umbral < 7.0, pH50 ≈ 6.7) se necesitaría un cambio de ≥ 0.2-0.3
unidades de pH. El modelo produce **ΔpH ≈ −0.009** en todos los regímenes probados
(barrido de J_co2 × k_buf × J_acid: 27 combinaciones). **No cruza ni roza el umbral.**

---

## POR QUÉ (biofísica del resultado)

La anhidrasa carbónica cataliza la interconversión CO2 ⇌ HCO3⁻ + H⁺ pero **NO desplaza el
equilibrio termodinámico** (Keq fijado por pKa1 = 6.1). Acelera la *velocidad* de relajación,
no la *posición* del equilibrio. Con el pool de bicarbonato extracelular (~26 mM) como buffer
dominante y producción metabólica de CO2 normal, el pH de estado estacionario queda fijado por
la Henderson-Hasselbalch; una reducción de CA14 solo retrasa la hidratación, y el CO2 se
difunde / el buffer lo absorbe. Incluso con hiperproducción de CO2 (J_co2 = 0.05, pH 6.75),
el efecto de CA14 es aún menor.

## DETALLES DE CALIBRACIÓN (para reproducibilidad)

- Estado normal: pCO2 50 mmHg, [HCO3⁻] 26 mM → pH HH 7.33
- k_cat_hyd = 5 s⁻¹ (CA14 efectiva, conservador vs CA II 10⁷-10⁸ M⁻¹s⁻¹)
- k_cat_deh calibrado por termodinámica: k_hyd/k_deh = Keq = 7.93×10⁻⁴ mM → k_deh ≈ 6450 s⁻¹
- ASIC: pH50 = 6.7, n = 4 (Physiol Rev 2025; Cell Death Discov 2023)
- Método: estado estacionario de [CO2], [HCO3⁻], [H⁺] con fuentes/sinks (J_co2, k_diff, J_acid, k_buf)

## IMPLICANCIA PARA LA INVESTIGACIÓN (honestidad cruda)

1. **CA14 sigue siendo candidato causal** por MR + colocalización (PP.H4 > 0.5) — eso es
   estadística poblacional sólida y NO se toca.
2. **El mecanismo periférico vía pH queda descartado** como vía simple en compartimento único.
   La predicción direccional Olink (CA14 ↓ en plasma FM) se MANTIENE — es independiente del
   mecanismo y sigue siendo el test definitivo.
3. **Explicaciones alternativas** que el modelo no puede descartar (requieren datos nuevos):
   - (a) CA14 actúa en SNC/neuronas, no microambiente periférico
   - (b) Efecto sobre cinética transitoria de pH (picos ácidos), no estado estacionario
   - (c) CA14 plasmática es marcador correlacional, no mediador
   - (d) MR captura predisposición de por vida (desarrollo/SNC), no función periférica aguda

## Nota sobre la v1 del modelo

La primera versión (2 pools acoplados con pH leído por HH) daba sensibilidad plana
(ΔpH = 0.000 en todas las filas) — defecto técnico reconocido y corregido en v2 con
[H⁺] dinámico explícito. La v2 está calibrada termodinámicamente y el resultado es el
negativo reportado aquí. Ninguna versión apoyó la vía acidosis→ASIC.
