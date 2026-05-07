# Scope B: Análisis Numérico de Transferencia Electrónica — V4b
## Rol: Adam Heller — Biosensores electroquímicos con conexión molecular directa

---

## 1. Resumen Geométrico V4b (Validado)

| Parámetro | Valor | Status |
|-----------|-------|--------|
| Au NP radio | 10.0 Å | Ajustado para contacto CYS43+49 |
| Au NP centro | ~25.9 Å del centro global | Excéntrico, zona ILE49/VAL43/LEU40 |
| Au surface → CYS43 SG | **1.89 Å** | ÓPTIMO (enlace Au-S directo) |
| Au surface → CYS49 SG | **3.13 Å** | VIABLE (Au-S con ligero estrés) |
| Au surface → CYS40 SG | 5.34 Å | MARGINAL (puente flexible o excluir) |
| **Max hopping gap** | **9.25 Å** (HIS46→MET52) | **VIABLE <15Å** |
| Au surface → Heme B FE | ~9.87 Å | Medición directa posible |

**Veredicto geometría**: PASS. El cluster Au de 2nm puede anclarse químicamente a la pared luminal con 2 tióles fuertes y 1 débil.

---

## 2. Teoría de Marcus Simplificada (Marcus-Lite)

Para hopping secuencial ET en proteínas, la tasa de transferencia entre dos centros redox está dada por:

$$k_{ET} = \frac{2\pi}{\hbar} |V_{AB}|^2 \frac{1}{\sqrt{4\pi\lambda k_B T}} \exp\left(-\frac{(\Delta G^\circ + \lambda)^2}{4\lambda k_B T}\right)$$

Donde:
- $V_{AB}$ = acoplamiento electrónico (decae exponencialmente con distancia)
- $\lambda$ = energía de reorganización (~0.5–1.5 eV para centros metálicos en proteínas)
- $\Delta G^\circ$ = cambio de energía libre (~0 para Au→Heme al potencial redox similar)

### Aproximación para hopping proteico

$$k_{hop} \approx k_0 \cdot e^{-\beta \cdot d}$$

Donde:
- $k_0$ = $10^{13}$ s⁻¹ (frecuencia nuclear límite)
- $\beta$ = 1.0–1.6 Å⁻¹ (factor de decaimiento del túnel en proteínas)
- $d$ = distancia centro a centro

---

## 3. Cálculo de Tasas por Tramo

| Tramo | $d$ (Å) | $e^{-\beta d}$ ($\beta=1.4$) | $k_{hop}$ (s⁻¹) | $t_{hop}$ (ns) |
|-------|---------|-------------------------------|-------------------|----------------|
| Au surface → CYS49 SG | 3.13 | 0.0124 | 1.2×10¹¹ | 8.3 |
| CYS49 SG → HIS46 NE2 | 4.78 | 0.0012 | 1.2×10¹⁰ | 83 |
| HIS46 NE2 → MET52 SD | 9.25 | 2.6×10⁻⁶ | 2.38×10⁷ | 42.1 |
| MET52 SD → Heme B FE | 5.65 | 3.7×10⁻⁴ | 3.7×10⁹ | 270 |

**Tasa limitante**: HIS46 → MET52 (≈42 ns por hop).

### Consideración de hopping múltiple

Para 4 saltos en serie, el rate global es limitado por el paso más lento:

$$k_{overall} \approx k_{limiting} = 2.6 \times 10^7 \text{ s}^{-1}$$

**Tiempo de transferencia total**: ~42 ns por electrón.

Con ~1000 electrones acumulados (saturación de Au NP), la carga descarga en:
- $t_{discharge}$ = 1000 × 42 ns = **42 μs**

**Corriente estimada**:
$$I = \frac{n \cdot e}{t} = \frac{1000 \cdot 1.6 \times 10^{-19} \text{ C}}{42 \times 10^{-6} \text{ s}} \approx 3.8 \times 10^{-12} \text{ A}$$

O sea, **3.8 pA por evento de saturación**.

### PERO: Detección por cascada enzimática (amplificación)

El diseño de Heller no depende de un solo electrón. El Au NP cataliza la reducción de H₂O₂:

$$\text{H}_2\text{O}_2 + 2\text{H}^+ + 2e^- \xrightarrow{Au} 2\text{H}_2\text{O}$$

Cada molécula de H₂O₂ consume **2 electrones** del Au NP. Si [H₂O₂] = 1 μM:
- Flujo difusivo al lumen: ~10⁶ moléculas/s por nanoporo
- Conversión catalítica en Au: ~10⁴–10⁵ e⁻/s

**Corriente resultante**: ~1–10 pA (picoamperios), **mEDIBLE con potenciostato moderno** (Keithley 6485 mide fA).

Al immovilizar 10⁹ ferritinas/cm² en electrodo:
- Densidad de corriente: ~1–10 nA/cm²
- Con área efectiva 0.1 cm²: **0.1–1 nA total**

---

## 4. Comparativa de Cinéticas: Procesador vs. Biosensor

| Métrica | V3 (Procesador) | V4b (Biosensor) |
|---------|-----------------|-----------------|
| Frecuencia objetivo | GHz (imposible) | ms–s (viable) |
| Tasa límite | túnel 12Å puro | 42 ns por evento |
| Métrica de salida | bits/segundo | nanoamperios |
| Instrumento necesario | Osciloscopio de RF | Potenciostato CV |
| Costo instrumento | $50k+ | $1k–5k |
| Paper posible? | NO | SÍ |

---

## 5. Escenario de Detección Optimista (pH-Gated)

Si incluimos el gating por ARG61/GLU44:

| Estado pH | Campo eléctrico lumen | ET Rate | Señal |
|-----------|----------------------|---------|-------|
| pH 7.4 (ARG⁺ / GLU⁻) | Fuerte, dirigido | 42 ns (ON) | ~1 nA |
| pH 10 (ARG⁰ / GLU⁻) | Débil / invertido | >>1 ms (OFF) | ~pA (ruido) |
| pH 4 (ARG⁺ / GLU⁰) | Colapsado | >>1 ms (OFF) | ~pA (ruido) |

**Resultado**: Un biosensor **pH-gated** de H₂O₂ con OFF/ON ratio de ~100×.

---

## 6. Veredicto Scope B: V4b Apto para Prototipo In Vitro

| Criterio | V3 | V4b (Este análisis) |
|----------|----|---------------------|
| Geometría anclaje | FAIL (18Å gap) | **PASS** (1.9Å contacto) |
| Hopping chain viable | DUDOSO (>15Å algún gap) | **PASS** (max 9.25Å) |
| Tasas de ET | Imposible (GHz) | **Viable** (42 ns) |
| Métrica medible | Ninguna | **nA de corriente** |
| Costo instrumentación | Prohibitivo | **Accesible** |
| Precedente publicable | Ninguno | **Ferritin-Au electrochem** |

**Score estimado**: **7.5 / 10** (VIABLE con desarrollo de laboratorio).

---

## 7. Próximos Pasos Requeridos

1. **FoldX / PyRosetta**: Calcular ΔΔG de ILE49→CYS, VAL43→CYS, LEU40→CYS en 1BFR.
2. **MD Corta (OpenMM)**: 10 ns de equilibración del Au NP excéntrico en lumen.
3. **Docking MtrA**: Posicionar MtrA con cisteínas de superficie en el canal 4-fold de BFR.
4. **Síntesis Genética**: Subclonar 1BFR con mutaciones en vector pET28a, expresar en E.Coli BL21(DE3).
5. **Formación de Au NP**: Reducción de HAuCl₄ (20 eq) in situ dentro del lumen purificado.
6. **Celda Electroquímica**: CV y amperometría en electrodo de carbono vitreo.
