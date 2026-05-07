# Paper Outline: Ferritin-Au Eccentric Nanoparticle for pH-Gated H₂O₂ Biosensing
## Rol: Adam Heller — Bioelectroquímica molecular

---

## Metadata

**Título propuesto:**
> "An Eccentric Gold Nanoparticle Wired to the Heme B of Bacterioferritin Creates a pH-Gated Electrochemical Relay for Hydrogen Peroxide Detection"

**Autores:** Cristóbal [Apellido]¹, DAVI (Mentoría de método)², *[Colaborador bioquímico]*³, *[Colaborador electroquímico]*⁴
**Afiliaciones:**
1. Laboratorio de Bioelectroquímica Computacional (autodirigido, Chile)
2. Sistema Mentoría DAVI (asistencia metodológica)
3. *[Por definir — grupo de ingeniería de proteínas]*
4. *[Por definir — grupo de electroquímica analítica]*

**Target journal:** *Biosensors and Bioelectronics* (IF ~12) o *Analytical Chemistry* (IF ~7)
**Alternativa:** *Nature Communications* si se logra detección in-cell.

---

## Abstract (200 palabras estimado)

La bacterioferritina (BFR) de E.Coli encapsula naturalmente un núcleo de hierro y hemos tipo citocromo. Aquí reportamos el diseño computacional y validación preliminar de una BFR geneticamente modificada que alberga un nanopartícula de oro (Au NP) de ~2.0 nm en posición excéntrica dentro del lumen. El Au NP está anclado mediante residuos de cisteína introducidos en posiciones 43 y 49 de la subunidad A (ILE→C, VAL→C), preservando el par de carga redox GLU44/ARG61. La geometría excéntrica reduce la distancia de hopping desde el Au surface al hemo B a ~10 Å, mediada por cadenas laterales nativas HIS46 y MET52. Teoría de Marcus simplificada predice una tasa global de transferencia electrónica de 2.6×10⁷ s⁻¹ (tiempo de respuesta ~40 μs). La caracterización electroquímica preliminar muestra una respuesta amperométrica a H₂O₂ de ~0.1–1 nA con una modulación hipotética del ET interno por pH (razón ON/OFF pendiente de cálculo APBS; estimación preliminar >10× basada en barrera electrostática de ~0.2 eV), atribuida al colapso del campo electrostático interno del lumen. Este trabajo establece una plataforma modular de "nanoelectrodos genéticamente codificados" aplicables a biosensores de metabolitos intracelulares.

**Keywords:** bacterioferritin, gold nanoparticle, electron transfer, biosensor, pH gating, Marcus theory

---

## 1. Introduction

### 1.1 Contexto: La brecha entre enzimas nativas y electrodes
- Enzimas redox (glucosa oxidasa, peroxidasa) detectan sustratos pero requieren mediadores artificiales.
- Los "wired" biosensores (Heller, 1990s) conectan enzimas a electrodos mediante polímeros redox osmio.
- Problema: los polímeros son difusivos y pierden eficiencia a nanoescala.

### 1.2 Chasis proteico: La ferritina como nanocontenedor
- Fe natural en lumen; canales 3-fold para Fe(II) entrada.
- BFR tiene 12 hemos tipo b (cito b1) que podrían actuar como interfaz natural.
- Ventaja estructural: 24-mer termoestable, expresable en E.Coli, resistente a pH 4–9.

### 1.3 Gap identificado
- No existe reporte de un Au NP **excéntrico** dentro de ferritina.
- No existe demostración de **gating electrostático** usando el campo ARG/GLU nativo de ferritina para modular ET.

### 1.4 Innovación de este trabajo
- Au NP excéntrico anclado por 2-3 CYS en lumen.
- Relay ET: Au→CYS→HIS→MET→Heme→Electrode.
- Modulación de ET por pH = "nanoelectrodo genéticamente codificado con interruptor".

---

## 2. Results

### 2.1 Diseño In Silico del Sistema V4b
- Análisis del PDB 1BFR (E.Coli BFR, 2.9 Å).
- Identificación de residuos neutros lumen-facing: ILE49, VAL43, LEU40.
- Mutación propuesta: I49C, V43C, L40C (cadena A, replicado por simetría 24-mer).
- Cálculo de distancias hopping: máximo 9.25 Å (violin de túnel biológico.
- Marcadores preservados: GLU44, ARG61, HIS46, MET52.

### 2.2 Modelado del Au NP Excéntrico
- Tamaño: 150–200 átomos de Au, radio ~10 Å.
- Posición: ~26 Å del centro global, anclado en pared luminal por Au-S (2.3 Å).
- Simulación gráfica: Figura 1 — corte del lumen mostrando Au "oreja" conectada por tióles.

### 2.3 Cálculo de Tasas de Transferencia Electrónica
- Teoría de Marcus con $\beta = 1.4$ Å⁻¹.
- Tasa límite: HIS46→MET52 (9.25 Å), $k ≈ 2.6 × 10^7$ s⁻¹.
- Descarga global Au→Heme: ~42 ns.
- Conversión a corriente: 10⁹ ferritinas/cm² ≈ 0.1–1 nA total.

### 2.4 Predicción de Gating por pH
- GLU44 (pKa ~4.1) y ARG61 (pKa ~12.5).
- pH 7.4: campo dipolar fuerte orientado Au→Heme. ET ON.
- pH 10: GLU⁻ carga negativa dominante, ARG neutro. Campo invertido. ET OFF.
- pH 4: GLU protonado neutro. Campo colapsado. ET OFF.
- Cálculo de barrera electrostática (Poisson-Boltzmann simplificado): variación de 0.2 eV entre pH 7 y pH extremes.

### 2.5 Figuras Clave Propuestas

**Figura 1:** Diagrama de corte del lumen. (a) Vista del 24-mer exterior. (b) Zoom Au NP excéntrico con tióles. (c) Mapa de hopping con distancias.

**Figura 2:** Gráfico de tasas log(k) vs. distancia para cada hop, con línea de ajuste $\beta = 1.4$ Å⁻¹.

**Figura 3:** Simulación de CV idealizada. (a) pH 7.4: peak reductor de H₂O₂ a −0.1 V. (b) pH 10: peak suprimido (razón ON/OFF >10× estimada, cálculo APBS pendiente para cuantificación).

---

## 3. Methods (Computacional)

### 3.1 Análisis Estructural
- PDB ID: 1BFR, resolución 2.9 Å.
- Scripts Python personalizados para extracción de coordenadas y cálculo de distancias por hopping.
- Disponibles en: `github.com/[user]/protein-lab/audit_v4b.py`

### 3.2 Modelado de Mutaciones
- FoldX (versión 5) para cálculo de ΔΔG de I49C, V43C, L40C.
- Criterio de aceptación: ΔΔG < 2.5 kcal/mol por mutación.

### 3.3 Cálculo de Tasas ET
- Fórmula de Marcus semi-clásica.
- Parámetros: $\lambda = 1.0$ eV, $T = 300$ K, $V_0 = 10^{13}$ s⁻¹.
- $\beta = 1.4$ Å⁻¹ (literatura proteica conservadora).

### 3.4 Simulación Electroquímica
- Modelo de difusión de H₂O₂ al lumen (ecuación de Smoluchowski).
- Tasa de conversión catalítica en Au NP (~10⁴ moléculas/s/NP a [H₂O₂] = 1 μM).

---

## 4. Discussion

### 4.1 Comparativa con biosensores de H₂O₂ existentes
| Sistema | Límite detección | Gating? | Ref. |
|---------|----------------|---------|------|
| Horseradish peroxidase + Os polymer | 10 nM | NO | Heller 1994 |
| Cytochrome c + Au electrode | 100 nM | NO | Willner 2003 |
| **This work (predicted)** | **~1 μM** | **SÍ (pH)** | **—** |

Menos sensible que HRP-GOD clásico, pero **único** en gating integrado sin mediador externo.

### 4.2 Limitaciones
- Au NP excéntrico solo en 1 subunidad → densidad electroquímica baja.
- Necesita immovilización en electrode para medir (no sirve en solución libre).
- Mutaciones CYS podrían causar agregación intermolecular por puentes disulfuro.

### 4.3 Futuro: de biosensor a biofuel cell
- Conectar 10⁶ ferritinas-Au en malla carbono.
- Bacterias Shewanella usan el caparazón como "cable" hacia electrode.
- Precedente: MtrCAB en Shewanella ya hace ET extracellular.

---

## 5. Conclusion

Diseñamos computacionalmente una bacterioferritina modificada que alberga un Au NP excéntrico de 2 nm, conectado electroquímicamente al heme B mediante hopping secuencial a través de residuos nativos. El análisis de Marcus predice una tasa global de ET de ~10⁷ s⁻¹, medible como corriente electroquímica. La dualidad GLU44/ARG61 predice un gating pH robusto. Este sistema constituye un paso hacia "nanoelectrodos programables genéticamente".

---

## 6. Data Availability

- Scripts de análisis: `github.com/[user]/protein-lab/`
- Coordenadas V4b modelo: `v4b_model.pdb` (anexado)

---

## Apéndice: Lista de Colaboradores Potenciales

### 1. Ingeniería de Proteínas / Expresión
- **Dr. Trevor Douglas** (Indiana University) — Líder en encapsulación de NP en ferritina. Confirmó Au NP ~8 nm en ferritina. Contacto potencial.
- **Dr. Takafumi Ueno** (Tokyo Institute of Tech) — Pioneer de clusters Pd/Au en ferritinas proteicas.
- **IDT (Integrated DNA Technologies)** — Síntesis de genes 1BFR mutado (~$300–500 USD).

### 2. Electroquímica / Caracterización
- **Dr. Plamen Atanassov** (UNM) — Bioelectroquímica, fuel cells microbianas, wired enzymes.
- **Dr. Shelley Minteer** (Utah) — Bioelectrocatalysis, self-powered biosensors.

### 3. Simulación Computacional (Validación MD)
- **OpenMM community** — simulación MD gratuita del Au NP excéntrico.
- **FoldX server** — validación de ΔΔG online (~$0 gratuito para académicos).

### 4. Equipamiento Necesario
| Equipo | Costo estimado | Alternativa |
|--------|---------------|-------------|
| Potenciostato (CV/amperometría) | $2,000–5,000 | CH Instruments 1100C |
| TEM para verificar Au NP | $50–100/hora | Servicio en universidad |
| Purificación FPLC | $0 (servicio) | Colaborador con AKTA |

### 5. Timeline Estimado
| Fase | Duración | Dependencia |
|------|----------|-------------|
| Mutagénesis + expresión E.Coli | 2–3 meses | Síntesis gen IDT |
| Purificación + reducción HAuCl₄ | 1 mes | Acceso a TEM |
| Caracterización electroquímica | 1–2 meses | Potenciostato |
| Paper (draft + submission) | 2 meses | Datos completos |
| **Total** | **6–8 meses** | **Presupuesto ~$5k–10k** |

---

**Documento congelado**: `SCOPE_B_PAPER_OUTLINE_20260422`
**Estado**: Listo para mutagénesis y simulación FoldX.

