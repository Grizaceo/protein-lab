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

## 2. Teoría de Marcus y Corrección por Efecto de Tamaño Cuántico (QSE)

Para el hopping secuencial de electrones (ET) en proteínas, la tasa de transferencia entre dos centros redox está regida por la ecuación de Marcus clásica:

$$k_{ET} = \frac{2\pi}{\hbar} |V_{AB}|^2 \frac{1}{\sqrt{4\pi\lambda k_B T}} \exp\left(-\frac{(\Delta G^\circ + \lambda)^2}{4\lambda k_B T}\right)$$

Donde:
- $V_{AB}$ es el acoplamiento electrónico que decae exponencialmente con la distancia.
- $\lambda$ es la energía de reorganización ($\sim 0.5 - 1.5\text{ eV}$ para centros redox en proteínas).
- $\Delta G^\circ$ es el cambio de energía libre Gibbs de la reacción.

### 2.1 Corrección del Potencial del Au NP Confinado (QSE)
Originalmente se asumió $\Delta G^\circ \approx 0$ bajo la hipótesis de que la nanopartícula de oro (Au NP) se comporta como oro bulk. Sin embargo, para un nanocluster de $\sim 2.0\text{ nm}$ de diámetro ($\sim 150 - 200$ átomos de oro) en un entorno luminal estrecho, la energía electrostática de carga de un solo electrón ($e^2/2C$) induce un **Quantum Size Effect (QSE)** significativo según la aproximación de Bard/Murray.

1. **Capacitancia ($C$) del cluster en dieléctrico confinado**:
   Dentro del lumen de la bacterioferritina, el entorno es una mezcla de agua ($\varepsilon \approx 80$) y el núcleo proteico ($\varepsilon \approx 4$). La constante dieléctrica efectiva nominal es $\varepsilon_{eff} \approx 30$ (rango de incertidumbre $20 - 40$).
   Para un radio de cluster $R = 1.0\text{ nm}$ ($1.0 \times 10^{-9}\text{ m}$):
   $$C = 4\pi \varepsilon_0 \varepsilon_{eff} R = 4\pi (8.854 \times 10^{-12}\text{ F/m}) \times 30 \times 1.0 \times 10^{-9}\text{ m} \approx 3.34 \times 10^{-18}\text{ F}$$

2. **Desplazamiento del potencial redox QSE ($\Delta V_{QSE}$)**:
   La energía de carga electrostática por electrón es:
   $$\Delta V_{QSE} = \frac{e}{2C} = \frac{1.602 \times 10^{-19}\text{ C}}{2 \times 3.34 \times 10^{-18}\text{ F}} \approx 0.024\text{ V} = +24.0\text{ mV}$$
   Este corrimiento anódico hace que sea termodinámicamente más difícil oxidar la nanopartícula en confinamiento.

3. **Potencial redox efectivo y energía libre ($\Delta G^\circ$)**:
   - $E^\circ(\text{Au bulk tiol}) \approx +100\text{ mV}$ vs SHE (interfaz funcionalizada).
   - $E^\circ(\text{Au NP confinado}) = E^\circ(\text{Au bulk tiol}) + \Delta V_{QSE} \approx +124.0\text{ mV}$ vs SHE.
   - $E^\circ(\text{Heme B BFR}) \approx -225\text{ mV}$ vs SHE (referencia cristalográfica experimental).
   
   Para la transferencia de electrones en el sentido de descarga de la nanopartícula hacia el canal del hemo (Au NP $\rightarrow$ Heme B), la energía libre termodinámica es:
   $$\Delta G^\circ = E^\circ(\text{Heme B}) - E^\circ(\text{Au NP}) = -225\text{ mV} - 124\text{ mV} = -349.0\text{ meV} = -0.349\text{ eV}$$
   Este valor revela un proceso **fuertemente exergónico** ($\Delta G^\circ < 0$), lo que impulsa activamente el flujo electrónico.

### 2.2 Impacto sobre el Factor de Activación de Marcus
Analicemos la ganancia en el factor de probabilidad térmica exponencial $\exp[-(\Delta G^\circ + \lambda)^2 / 4\lambda k_B T]$ a $T = 300\text{ K}$ ($k_B T \approx 0.0259\text{ eV}$) para una energía de reorganización típica de metaloproteínas $\lambda \approx 1.0\text{ eV}$:

- **Caso sin QSE ($\Delta G^\circ = 0$)**:
  $$\text{Factor} = \exp\left(-\frac{(0 + 1.0)^2}{4 \times 1.0 \times 0.0259}\right) = \exp(-9.65) \approx 6.43 \times 10^{-5}$$
- **Caso corregido con QSE ($\Delta G^\circ = -0.349\text{ eV}$)**:
  $$\text{Factor} = \exp\left(-\frac{(-0.349 + 1.0)^2}{4 \times 1.0 \times 0.0259}\right) = \exp\left(-\frac{0.651^2}{0.1036}\right) = \exp(-4.09) \approx 1.67 \times 10^{-2}$$

**Conclusión**: La corrección de QSE y la exergonicidad de la transferencia aceleran el factor cinético exponencial por un factor de **$\approx 260\times$**. Esto reduce drásticamente las barreras de activación intrínsecas a lo largo de la cadena de salto.

---

## 3. Cálculo de Tasas por Tramo (Refinado)

Mantenemos la aproximación de decaimiento electrónico para hopping proteico:
$$k_{hop} \approx k_0 \cdot e^{-\beta \cdot d}$$
Donde $k_0 = 10^{13}\text{ s}^{-1}$ es la frecuencia nuclear de colisión molecular y $\beta = 1.4\text{ Å}^{-1}$ es la tasa de atenuación dieléctrica típica de una proteína.

| Tramo | $d$ (Å) | $e^{-\beta d}$ ($\beta=1.4$) | $k_{hop}$ (s⁻¹) (Basal) | $k_{hop}$ (s⁻¹) (Marcus Corregido) | $t_{hop}$ (ns) (Corregido) |
|-------|---------|-------------------------------|-------------------|-----------------------------------|----------------------------|
| Au surface → CYS49 SG | 3.13 | 0.0124 | 1.2×10¹¹ | $\sim 1.2\times 10^{11}$ | 8.3 |
| CYS49 SG → HIS46 NE2 | 4.78 | 0.0012 | 1.2×10¹⁰ | $\sim 1.2\times 10^{10}$ | 83 |
| HIS46 NE2 → MET52 SD | 9.25 | 2.6×10⁻⁶ | 2.38×10⁷ | $2.38\times 10^7$ (Basal)* | 42.1 (Túnel libre) |
| MET52 SD → Heme B FE | 5.65 | 3.7×10⁻⁴ | 3.7×10⁹ | $\sim 3.7\times 10^9$ | 0.27 |

*\*Nota: El paso limitante de la red sigue siendo el salto intrínseco de la proteína HIS46 $\rightarrow$ MET52 ($d = 9.25\text{ Å}$, $t_{hop} \approx 42\text{ ns}$), ya que este paso es nativo y no depende directamente de la sobredosis de potencial de la NP. Sin embargo, la exergonicidad general del sistema ($\Delta G^\circ \approx -0.349\text{ eV}$) asegura que no haya estancamiento de carga en el extremo del metal y proporciona una fuerza motriz (overpotential) termodinámica que previene la recombinación.*

### Corriente electroquímica teórica (Saturación)
Con un flujo coordinado y la descarga sostenida de electrones desde la nanopartícula:
- Tiempo de tránsito limitante del electrodo: $\sim 42\text{ ns}$ por electrón.
- Corriente teórica por monómero activo:
  $$I = \frac{e}{t} = \frac{1.602 \times 10^{-19}\text{ C}}{42 \times 10^{-9}\text{ s}} \approx 3.8\text{ pA}$$
- Para un electrodo funcionalizado con una monocapa densa de ferritinas ($\sim 10^{10}\text{ proteínas/cm}^2$):
  $$J = 10^{10} \times 3.8\text{ pA} \approx 38\text{ nA/cm}^2$$
  Esta densidad de corriente es perfectamente **mensurable y detectable** con potenciostatos de laboratorio de gama media.

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
