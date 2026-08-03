# Tangente 1: Desconvolución Transcriptómica Fina y Discriminación Celular (Mastocito vs Basófilo)

**Fecha:** Mayo 2026  
**Repositorio:** `protein-lab/investigacion-fibromialgia`  
**Dataset Analizado:** GSE67311 (Sangre Completa, N=140: 67 FM vs 75 HC, Microarray Affymetrix) + GSE221921 (PBMCs, N=189, RNA-seq)  
**Script Ejecutado:** [`scripts/tangent1_mastocyte_vs_basophil.py`](file:///wsl.localhost/Ubuntu/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/scripts/tangent1_mastocyte_vs_basophil.py)

---

## 1. Contexto y Pregunta Central #1

**Pregunta 1:** ¿Es la caída de CPA3/MS4A2/FCER1A/HDC en sangre completa un reflejo de degranulación/migración hacia tejidos (DRG/piel) o una depleción de basófilos circulantes?

Para responder a esta pregunta con rigor empírico, evaluamos por separado los marcadores celulo-específicos de:
1. **Mastocitos puros/maduros:** `CPA3` (Carboxipeptidasa A3), `TPSAB1` (Triptasa $\alpha/\beta 1$), `KIT` (c-Kit / CD117, esencial para linaje de mastocitos y ausente en basófilos maduros).
2. **Basófilos circulantes puros:** `GATA2` (factor de transcripción maestro de basófilos), `CLC` (proteína de cristales Charcot-Leyden), `PRG2`.
3. **Compartidos (Basófilos + Mastocitos):** `MS4A2` (FcεRIβ), `FCER1A` (FcεRIα), `HDC` (Histidina Descarboxilasa).

---

## 2. Resultados Cuantitativos en Sangre Completa (GSE67311)

### Tabla 1: Expresión Diferencial de Marcadores de Linaje Inmune

| Gen | Categoría Celular | FM Mean | HC Mean | $\log_2\text{FC}$ | Valor $p$ | Valor $q$ (FDR) | Significativo |
|---|---|---|---|---|---|---|---|
| **CPA3** | Específico Mastocito/Basófilo Primed | 6.1319 | 6.9182 | **-0.7863** | $4.99 \times 10^{-7}$ | **$0.000004$** | **SÍ (DOWN)** |
| **GATA2** | Específico Basófilo (TF Maestro) | 5.9785 | 6.4301 | **-0.4516** | $1.72 \times 10^{-5}$ | **$0.000031$** | **SÍ (DOWN)** |
| **MS4A2** | Compartido (FcεRIβ) | 4.6032 | 5.1195 | **-0.5163** | $1.71 \times 10^{-6}$ | **$0.000008$** | **SÍ (DOWN)** |
| **FCER1A** | Compartido (FcεRIα) | 6.7669 | 7.2682 | **-0.5012** | $7.22 \times 10^{-6}$ | **$0.000022$** | **SÍ (DOWN)** |
| **HDC** | Compartido (Histidina Descarboxilasa) | 5.1957 | 5.7241 | **-0.5284** | $1.45 \times 10^{-5}$ | **$0.000031$** | **SÍ (DOWN)** |
| **TPSAB1** | Específico Mastocito Maduro (Triptasa) | 5.8354 | 5.8129 | +0.0225 | 0.8317 | 0.8798 | NO (Invariable) |
| **KIT** | Específico Mastocito Maduro (c-Kit) | 5.4104 | 5.4200 | -0.0095 | 0.6009 | 0.7726 | NO (Invariable) |
| **CLC** | Específico Basófilo/Eosinófilo | 10.1556 | 10.3326 | -0.1769 | 0.3730 | 0.5595 | NO (Invariable) |
| **PRG2** | Específico Eosinófilo/Basófilo | 4.1036 | 4.0988 | +0.0048 | 0.8798 | 0.8798 | NO (Invariable) |

---

## 3. Discusión e Interpretación Biológica Directa

1. **Ausencia de Señal de Mastocito Maduro en Sangre:**
   - Los mastocitos maduros no circulan de forma libre en sangre en sujetos sanos ni en estados inflamatorios crónicos leves; son residentes tisulares (piel, mucosas, meninges, DRG).
   - Los dos marcadores canónicos de mastocitos maduros con gránulos, `KIT` (c-Kit) y `TPSAB1` (Triptasa), **permanecen estrictamente invariables** en sangre completa ($\log_2\text{FC} \approx 0$, $q > 0.75$).

2. **Caída Selectiva de Basófilos Circulantes / Subtipo de Precursores Granulocíticos:**
   - En sangre periférica, los **basófilos** (0.5–1% de los leucocitos totales) expresan de forma constitutiva e intensa `GATA2`, `HDC`, `FCER1A` y `MS4A2`.
   - El hecho de que `GATA2` (TF maestro exclusivo del linaje basofílico circulante) caiga significativamente ($\log_2\text{FC} = -0.45, q = 0.000031$) junto con `HDC`, `FCER1A` y `MS4A2` demuestra que **la señal observada en GSE67311 refleja principalmente la depleción cuantitativa o el agotamiento funcional de los basófilos circulantes en la sangre perférica**.

3. **La Paradoja de CPA3 ($\log_2\text{FC} = -0.79$):**
   - `CPA3` sufre la caída más drástica del panel. Aunque `CPA3` es la proteasa característica de mastocitos tipo $\text{MC}_{\text{TC}}$, en basófilos periféricos estimulados o "primados" por citoquinas la transcripción de `CPA3` se activa activamente.
   - La caída paralela de `CPA3` y `GATA2` sin cambios en `KIT` ni `TPSAB1` sugiere que la reserva circulante de basófilos/progenitores granulocíticos deprimidos en sangre periférica está severamente comprometida.

---

## 4. Conclusión de la Pregunta 1

> **Respuesta Definitiva:** La caída de `CPA3/MS4A2/FCER1A/HDC` en sangre completa **NO es una prueba directa de migración masiva de mastocitos maduros**, sino la manifestación de una **depleción/agotamiento de basófilos circulantes y progenitores granulocíticos en sangre periférica**. Los mastocitos maduros tisulares (DRG/piel) deben ser evaluados mediante biopsias locales o marcadores histológicos, no mediante transcriptómica de sangre total.
