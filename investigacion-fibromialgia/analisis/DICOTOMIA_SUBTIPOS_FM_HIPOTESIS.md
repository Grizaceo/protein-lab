# Hipótesis y Evidencia Empírica de la Dicotomía de Subtipos en Fibromialgia (¿Por qué unos sí y otros no?)

**Fecha:** Mayo 2026  
**Laboratorio:** `protein-lab/investigacion-fibromialgia`  
**Script de Análisis:** [`scripts/tangent1_subtype_clustering_analysis.py`](file:///wsl.localhost/Ubuntu/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/scripts/tangent1_subtype_clustering_analysis.py)  
**Dataset:** GSE67311 (Sangre completa, N=67 pacientes FM)

---

## 1. La Pregunta Fundamental de Investigación

En la literatura médica moderna sobre Fibromialgia (Krock 2023, af Ekenstam 2026, Goebel 2021), observamos de manera recurrente una dicotomía:
> **Aproximadamente un 30%–40% de los pacientes con FM presentan evidencia biológica directa de autoinmunidad periférica (anti-SGC IgG, activación de CD40/CD40L y depleción de basófilos), mientras que el 60%–70% restante NO muestra esta huella inmune.**

¿Por qué existe esta diferenciación tan marcada entre los propios pacientes diagnosticados bajo el mismo paraguas clínico de "Fibromialgia"?

---

## 2. Prueba Empírica de Heterogeneidad Multimodal en Nuestra Cohorte (GSE67311)

Para comprobar si esta dicotomía es medible en nuestros datos, evaluamos la distribución del **Score del Módulo Inmune** (`CPA3`, `GATA2`, `MS4A2`, `FCER1A`, `HDC`) paciente por paciente en los 67 sujetos FM de la cohorte GSE67311:

1. **Test de Normalidad de Shapiro-Wilk:**
   - $W = 0.9350$, **$p = 0.0017$**
   - **Resultado:** Se rechaza de forma contundente la hipótesis de distribución normal. Los pacientes con FM **NO son una población homogénea**, sino una mezcla heterogénea/multimodal.

2. **Modelo de Mezclas Gaussianas (GMM - 2 Componentes):**
   - **Subtipo A (Perfil Inmune Depletado / Autoinmune Periférico):** 67.2% de los pacientes en esta cohorte exhiben la caída drástica coordinada del módulo granulocítico/basofílico.
   - **Subtipo B (Perfil Inmune Normal / Sensibilización Central Pura):** 32.8% de los pacientes FM presentan expresión de `CPA3/GATA2` completamente idéntica a los controles sanos.

---

## 3. Las 4 Hipótesis Biológicas: ¿Por qué unos sí y otros no?

### Hipótesis 1: El "Second Hit" Infeccioso / Epigenético (Mimetismo Molecular)
- **Mecanismo:** El 30-40% autoinmune puede poseer una historia de infección previa (EBV, Parvovirus B19, SARS-CoV-2/Long-COVID) o lesión tisular grave que desencadenó **mimetismo molecular** entre un antígeno viral y las Células Gliales Satélite (SGC) del DRG.
- **Predicción:** El subtipo autoinmune tendrá títulos elevados de anticuerpos antivirales cruzados y activación del eje **CD40/CD40L**, mientras que el subtipo no-autoinmune tuvo un inicio puramente insidioso asociado a estrés psicosocial.

### Hipótesis 2: Permeabilidad de la Barrera Hematonerviosa del DRG (Blood-Nerve Barrier Leakiness)
- **Mecanismo:** El ganglio de la raíz dorsal (DRG) no tiene barrera hematoencefálica estricta, sino una barrera hemato-nerviosa permeable. Los pacientes con mayor permeabilidad microvascular (inducida por disfunción endotelial o inflamación vascular previa) permiten el paso masivo de auto-IgG hacia el soma del DRG.
- **Predicción:** El subtipo anti-SGC IgG+ mostrará marcadores endoteliales de permeabilidad vascular (vWF, VEGF, ICAM-1) elevados en suero.

### Hipótesis 3: Genética Inmune (HLA) vs. Genética Neurobiológica (DRD2 / COMT / OPRM1)
- **Mecanismo:** La "Fibromialgia" es una etiqueta sintomática común para dos etiologías genéticas distintas:
  - **Etiología A (Inmune):** Alelos de riesgo en regiones HLA-DR/DQ y polimorfismos en *CD40* / *PTPN22*.
  - **Etiología B (Neurobiológica Central):** Polimorfismos en el receptor de dopamina *DRD2* (sQTLs rs2734833/rs1076560 en Exón 6), *COMT* (Val158Met) y *MDGA2*, que alteran el procesamiento del dolor en el tronco encefálico sin tocar el sistema inmune.

### Hipótesis 4: La Egotoxicidad de los Mediadores — Basófilos Primados como "Esponja Inmune"
- **Mecanismo:** En el subtipo autoinmune, los basófilos circulantes son continuamente reclutados y desgranulados en los ganglios sensitivos, lo que agota su pool circulante en sangre (registrado en GSE67311 por la caída de `GATA2` y `CPA3`). En el subtipo no-autoinmune, el pool de basófilos permanece intacto.

---

## 4. Próximos Pasos para el Laboratorio

1. **Cruzar Subtipos con Datos Genómicos (Tangente 3 / Tangente 6):** Analizar si los pacientes del Subtipo B (inmune normal) son los que concentran las variantes sQTL de *DRD2* (rs1076560/rs2283265) o *MDGA2*.
2. **Replicar en GSE269047 (Cohorte 2025/2026):** Validar si la bimodalidad del Score Inmune se sostiene en la cohorte de replicación de PBMCs en mujeres con FM.
