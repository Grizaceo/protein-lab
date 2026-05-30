# Reporte Clínico-Computacional: Ventana de Selectividad PK/PD del Pramipexol
**Análisis in silico de la Ocupación de Receptores DRD2 Periféricos vs. DRD3 Centrales**

---

## 1. Resumen Ejecutivo
Este reporte técnico evalúa, mediante modelado matemático farmacocinético/farmacodinámico (PK/PD) de un compartimento en estado estacionario (*steady-state*), la selectividad del agonista dopaminérgico **Pramipexol** por los receptores centralizados **DRD3 (límbicos)** frente a los periféricos **DRD2 (PBMCs)**. 

Nuestra simulación demuestra matemáticamente una paradoja biológica sumamente favorable para el tratamiento de la **Fibromialgia (FM)**:
1. Debido a la alta afinidad termodinámica intrínseca del pramipexol por DRD3 ($K_d = 0.5\text{ nM}$) en comparación con DRD2 ($K_d = 3.0\text{ nM}$), combinada con su penetración activa a través de la barrera hematoencefálica ($K_p = 8.0$), **el Pramipexol se concentra de forma masiva en el sistema nervioso central (SNC)**.
2. A dosis clínicamente eficaces para Fibromialgia ($0.125\text{ mg}$ a $0.250\text{ mg/día}$ en toma única nocturna), se alcanza una saturación central del receptor **DRD3 de entre 86.2% y 92.5%**, mientras que la ocupación periférica de **DRD2 en PBMCs se mantiene en niveles mínimos de 14.1% a 24.1%**.
3. Este diferencial define una **ventana de selectividad terapéutica óptima ($\Delta \approx 68\% - 72\%$)**, minimizando los efectos adversos periféricos mediados por DRD2 (hipotensión ortostática, náuseas, emesis) mientras se maximiza el efecto terapéutico central en vías límbicas implicadas en la modulación del dolor y la fatiga.

---

## 2. Parámetros PK/PD de Referencia (Literatura Humana)

Los siguientes parámetros fueron integrados en el simulador a partir de datos clínicos y preclínicos reportados en la literatura científica:

| Parámetro | Símbolo | Valor Simulado | Justificación Fisiológica / Fuentes |
| :--- | :---: | :---: | :--- |
| **Biodisponibilidad Oral** | $F$ | $90\%$ ($0.90$) | Absorción casi completa, mínimo efecto de primer paso hepático. |
| **Volumen de Distribución** | $V_d$ | $500\text{ L}$ | Amplia distribución tisular (catión hidrofílico acumulado celularmente). |
| **Vida Media de Eliminación** | $t_{1/2}$ | $8.0\text{ h}$ | Constante de eliminación $K_e = 0.0866\text{ h}^{-1}$. Aclaramiento $CL \approx 43.3\text{ L/h}$. |
| **Constante de Absorción** | $K_a$ | $1.5\text{ h}^{-1}$ | Modelado para formulación de liberación inmediata (IR), $T_{max} \approx 1-2\text{ h}$. |
| **Coeficiente de Partición cerebral**| $K_p$ | $8.0$ | Relación tejido cerebral/plasma. Elevada por transporte activo mediado por OCT3. |
| **Afinidad DRD2 (PBMCs)** | $K_d(D2)$ | $3.0\text{ nM}$ | Concentración de saturación media periférica de Pramipexol humano. |
| **Afinidad DRD3 (Límbico)** | $K_d(D3)$ | $0.5\text{ nM}$ | Alta afinidad central (selectividad intrínseca de subfamilia D2-like). |

---

## 3. Formulación Matemática del Modelo

El modelo acopla la cinética transitoria plasmática con el equilibrio termodinámico local en los biofases periférico y central:

### 3.1. Cinética Plasmática Transitoria (Multi-dosis)
Para $N$ dosis administradas a tiempos $t_i$, la concentración plasmática en gramos/litro ($C_{plasma}(t)$) se obtiene por superposición lineal:

$$C_{plasma}(t) = \sum_{i=1}^{N} \frac{F \cdot \text{Dosis}_i \cdot K_a}{V_d \cdot (K_a - K_e)} \left( e^{-K_e(t - t_i)} - e^{-K_a(t - t_i)} \right) \quad \forall t \ge t_i$$

La concentración molar plasmática en nanomolar ($\text{nM}$) se calcula convirtiendo microgramos a moles con el peso molecular base ($211.27\text{ g/mol}$):

$$C_{plasma,\text{nM}}(t) = C_{plasma,\text{ng/mL}}(t) \times \frac{1000}{211.27}$$

### 3.2. Ecuaciones de Ocupación Dinámica de Receptores
*   **Periferia (PBMCs - DRD2):**
    
    $$\text{Occupancy}_{D2}(t) = \frac{C_{plasma,\text{nM}}(t)}{K_d(D2) + C_{plasma,\text{nM}}(t)} \times 100\%$$

*   **Cerebro (Límbico - DRD3):**
    
    $$\text{Occupancy}_{D3}(t) = \frac{C_{plasma,\text{nM}}(t) \times K_p}{K_d(D3) + \left(C_{plasma,\text{nM}}(t) \times K_p\right)} \times 100\%$$

---

## 4. Resultados de la Simulación a Estado Estacionario

El modelo se simuló por un periodo de 7 días ($168\text{ horas}$) para asegurar el estado estacionario completo. Los resultados de ocupación media, máxima y mínima durante las últimas 24 horas se detallan a continuación:

| Regimen de Dosificación | Dosis Diaria | Concentración Plasmática Media (nM) | Ocupación Media DRD3 Límbico (Central) | Ocupación Media DRD2 PBMCs (Periférico) | **Diferencial de Selectividad ($\Delta$)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **FM Inicial** (0.125 mg QD) | $0.125\text{ mg}$ | $0.49\text{ nM}$ | **86.25%** | **14.07%** | **72.19%** (Ventana Óptima) |
| **FM Intermedio** (0.250 mg QD)| $0.250\text{ mg}$ | $0.98\text{ nM}$ | **92.48%** | **24.11%** | **68.37%** |
| **FM Moderado** (0.500 mg QD) | $0.500\text{ mg}$ | $1.96\text{ nM}$ | **96.05%** | **37.86%** | **58.19%** |
| **FM Target Máximo** (1.0 mg QD)| $1.000\text{ mg}$ | $3.91\text{ nM}$ | **97.97%** | **53.70%** | **44.28%** |
| **Parkinson Estándar** (1.0 mg TID)| $3.000\text{ mg}$ | $12.39\text{ nM}$ | **99.48%** | **80.07%** | **19.42%** (Pérdida de ventana) |

---

## 5. Análisis Gráfico in Silico

### 5.1. Perfiles Temporales de Ocupación Dinámica en Estado Estacionario
A continuación se visualizan las fluctuaciones dinámicas del porcentaje de ocupación a lo largo de las últimas 24 horas del régimen en estado estacionario (Día 7):

![Perfil de Ocupación Temporal en Estado Estacionario](file:///\\wsl.localhost\Ubuntu\home\gris\.hermes\workspace\protein-lab\investigacion-fibromialgia\analisis\pk_pd_simulation\plots\steady_state_occupancy_profile.png)

*Figura 1: Curvas dinámicas de ocupación de receptores DRD3 centrales (rosa) frente a DRD2 periféricos (azul) para dosis de Fibromialgia (QD) y dosis de Parkinson (TID).*

### 5.2. Ventana de Selectividad y Umbral de Dosis-Respuesta
El análisis integral de la ventana de seguridad (Diferencial $\Delta = \text{Occupancy}_{D3} - \text{Occupancy}_{D2}$) como una función de la dosis administrada:

![Ventana de Seguridad y Ocupación Acoplada](file:///\\wsl.localhost\Ubuntu\home\gris\.hermes\workspace\protein-lab\investigacion-fibromialgia\analisis\pk_pd_simulation\plots\safety_window_dose_response.png)

*Figura 2: Curvas de dosis-respuesta en estado estacionario con barras de error que indican las fluctuaciones pico ($C_{max}$) y valle ($C_{min}$). Se destaca el valor de $\Delta$ en cada dosis.*

---

## 6. Conclusiones y Discusión Clínico-Farmacológica

### 6.1. ¿Existe una dosis umbral in silico?
**Sí, existe un umbral óptimo de selectividad.**
- Matemáticamente, la máxima ventana de selectividad ($\Delta = 72.19\%$) se localiza en la **dosis mínima de $0.125\text{ mg/día}$**. A esta dosis, el receptor límbico central DRD3 está ampliamente activado (**86.25%**), suficiente para desencadenar efectos pro-dopaminérgicos centrales (mejoría en la fatiga, modulación del dolor límbico y estado de ánimo), mientras que el receptor periférico DRD2 permanece prácticamente inalterado (**14.07%**), minimizando eventos adversos periféricos.
- Conforme la dosis se incrementa hacia **$1.0\text{ mg/día}$**, la ocupación periférica de DRD2 cruza el umbral del 50% (**53.70%**), lo que incrementa significativamente el riesgo de efectos adversos vasomotores y gastrointestinales sin aportar un incremento proporcional relevante en la activación de DRD3, el cual ya se encuentra prácticamente saturado (**97.97%**).

### 6.2. Imposibilidad Termodinámica Inversa
La solicitud de explorar si existe una dosis que *"active el receptor periférico minimizando la activación central"* es **termodinámicamente inviable**. 
Dado que:
1. La barrera hematoencefálica concentra el fármaco de forma activa en el cerebro ($K_p = 8.0$).
2. La afinidad por el receptor central DRD3 es 6 veces superior a la de DRD2 ($K_d = 0.5\text{ nM}$ vs $3.0\text{ nM}$).

Cualquier dosis de Pramipexol que sea suficiente para activar significativamente los receptores DRD2 periféricos en PBMCs (p. ej., $80\%$ de ocupación a dosis de Parkinson de $3.0\text{ mg/día}$) causará inevitablemente una **saturación total y casi absoluta ($>99.4\%$) del receptor central DRD3**, anulando cualquier tipo de selectividad periférica.
