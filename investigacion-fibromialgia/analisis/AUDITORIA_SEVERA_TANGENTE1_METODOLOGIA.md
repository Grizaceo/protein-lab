# Auditoría Severa y Verificación Adversaria de los Resultados (Tangente 1 y Subtipos en Fibromialgia)

**Fecha:** Mayo 2026  
**Laboratorio:** `protein-lab/investigacion-fibromialgia`  
**Autor:** Antigravity AI Agent (Postura de Auditoría Escéptica)  
**Script de Auditoría:** [`scripts/audit_adversarial_tangent1.py`](file:///wsl.localhost/Ubuntu/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/scripts/audit_adversarial_tangent1.py)

---

## 1. Postura de Auditoría: Cero Triunfalismo, Cero Sesgo de Confirmación

Esta auditoría somete a evaluación crítica todos los hallazgos previos del laboratorio sobre la **Tangente 1** (modelo autoinmune mastocito/basófilo) y la **supuesta ortogonalidad in silico** con el eje dopaminérgico. El objetivo es identificar fallos metodológicos, limitaciones de plataforma, artefactos de muestreo y sobreinterpretación biológica.

---

## 2. Hallazgos de la Auditoría Técnica (Prueba por Prueba)

### 🚨 Falencia #1: Falacia de Extrapolación Tisular de *DRD2* en Sangre (Falso "Descubrimiento de Ortogonalidad")

- **Lo que afirmamos previamente:** Que la falta de correlación ($r = +0.069$, $p = 0.57$) entre el módulo inmune (`CPA3/GATA2`) y el módulo neural (`DRD2/MDGA2`) probaba que la autoinmunidad periférica y la disfunción dopaminérgica central eran "mecanismos independientes/ortogonales".
- **La realidad auditada:**
  - En el microarray de sangre completa (GSE67311), la sonda de *DRD2* (`7951703`) muestra una intensidad media de **5.84 log2** (percentil 45.9%), pero con una variabilidad extremadamente baja ($\text{std} = 0.21$).
  - *DRD2* en sangre completa proviene de la baja expresión en subpoblaciones de linfocitos T y monocitos periféricos. **La expresión de *DRD2* en sangre NO refleja la actividad dopaminérgica del estriado, el tálamo o el tronco encefálico.**
  - **Veredicto:** Afirmar la "ortogonalidad del sistema dopaminérgico central" analizando ARN de sangre periférica es un **error de extrapolación tisular sin validez biológica**. La ortogonalidad solo podría probarse cruzando datos de suero con neuroimagen (PET/fMRI) o líquido cefalorraquídeo (LCR).

---

### 🚨 Falencia #2: Riesgo de Artefacto por Farmacoterapia en GSE67311

- **Lo que afirmamos previamente:** Que la caída de `CPA3` ($\log_2\text{FC} = -0.79$), `GATA2` ($\log_2\text{FC} = -0.45$), `MS4A2` ($\log_2\text{FC} = -0.52$) y `FCER1A` ($\log_2\text{FC} = -0.50$) prueba una "depleción autoinmune de basófilos circulantes en un subtipo FM".
- **La realidad auditada:**
  - El dataset GSE67311 comprende sangre completa de 70 pacientes con FM en tratamiento del mundo real.
  - Muchos fármacos comúnmente prescritos en FM (antidepresivos tricíclicos, duloxetina, pregabalina, AINEs u opioides) tienen **efectos inmunomoduladores directos comprobados sobre la transcripción de granulocitos y basófilos**.
  - **Veredicto:** Sin haber controlado por la variable de medicación de los sujetos (datos no disponibles de forma granular en el series matrix original), **NO se puede descartar que la caída de marcadores de basófilos sea un efecto secundario farmacológico en lugar de una etiología autoinmune primaria**.

---

### 🚨 Falencia #3: Sobreinterpretación del Subtipo Inmune 30–40%

- **Lo que afirmamos previamente:** Que existe un subtipo bien consolidado donde el 30–40% de los pacientes tienen enfermedad autoinmune por IgG anti-SGC y el resto no.
- **La realidad auditada:**
  - Los estudios de Goebel 2021 (N=15) y Krock 2023 son estudios exploratorios en cohortes pequeñas.
  - El único ensayo clínico controlado de fase 1 dirigido a estabilización de mastocitos en FM (**Ang et al. 2015, Ketotifeno 2mg BID**) fue **rigurosamente NEGATIVO** ($p = 0.7$ en dolor promedio, $p = 0.9$ en FIQR).
  - Si la degranulación de mastocitos fuera la causa primaria del dolor en ese 30-40%, el ketotifeno habría mostrado al menos una tendencia de respuesta en un subgrupo, lo cual no ocurrió.
  - **Veredicto:** La teoría autoinmune periférica es una **hipótesis biológica atractiva pero clínicamente no validada**. La evidencia terapéutica actual no respalda el bloqueo mastocitario en FM.

---

## 3. Matriz de Corrección de Postura para el Laboratorio

| Afirmación Previa (Triunfalista) | Error Detectado por Auditoría | Postura Correcta Cien por Ciento Rigurosa |
|---|---|---|
| "Probamos que la vía dopaminérgica y la vía inmune son ortogonales ($r=0.069$)" | ❌ Extrapolación de *DRD2* en sangre a la función cerebral central | ⚠️ *DRD2* en sangre no representa al SNC. La independencia de vías en cerebro debe evaluarse con PET/LCR, no con sangre. |
| "Demostramos depleción de basófilos como causa autoinmune de FM" | ⚠️ Posible confusión por tratamiento farmacológico previo | ⚠️ Existe una caída de marcadores granulocíticos en sangre, pero no se descarta sesgo por medicación crónica en FM. |
| "Tangente 1 es el descubrimiento del mecanismo periférico de la FM" | ❌ El ensayo con ketotifeno fue negativo | ⚠️ Tangente 1 es una hipótesis biológica fascinante en ratones, pero clínicamente frágil en humanos. |

---

## 4. Conclusión de la Auditoría

El laboratorio debe mantener un **lenguaje de cautela científica estricta**:
- **NO usar términos como "descubrimiento", "demostración definitiva" o "prueba de ortogonalidad".**
- Enmarcar la Tangente 1 como un **modelo hipotético periférico de investigación**, sujeto a validación experimental directa y condicionado por severas limitaciones de plataforma en los microarrays de sangre periférica.
