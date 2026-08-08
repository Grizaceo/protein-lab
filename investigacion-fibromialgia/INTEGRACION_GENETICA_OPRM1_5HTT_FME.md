# INTEGRACIÓN GENÉTICA — OPRM1 / 5-HTT y el Respondedor al Ejercicio (Módulo D)

**Fecha:** 2026-08-07
**Estado:** Hipótesis de integración (no computable localmente — GSE221921 no tiene genotipos).
**Ancla:** Tour et al. 2017 (PMID 28282362) — verificado por API PubMed 2026-08-07.

---

## 1. El hallazgo externo

Tour J et al., *Pain* 2017 (PMID 28282362): "Gene-to-gene interactions regulate endogenous pain modulation in fibromyalgia patients and healthy controls — antagonistic effects between opioid and serotonin-related genes."

- En controles sanos: **mayor EIH se asoció con OPRM1 G (señal opioide fuerte) combinado con 5-HTT low / 5-HT1A G (tono serotoninérgico débil)**.
- En FM: la misma interacción gen–gen mostró efectos antagónicos entre genes opioide y serotoninérgicos → el *balance*, no un sistema solo, gobierna la modulación endógena del dolor.

Esto es el primer marcador genético de **respondedor al ejercicio** en FM. Conecta directo con nuestro eje opioide composicional: el sistema está ahí (lo medimos elevado en sangre) pero su *funcionalidad* depende del balance genético opioide/serotonina.

---

## 2. SNPs a genotipar (pre-especificados)

| Gen | SNP | Alelo de interés | Función |
|---|---|---|---|
| OPRM1 | rs1799971 (A118G) | G (Arg) — mayor señal opioide | Receptor μ-opioide |
| SLC6A4 (5-HTT) | 5-HTTLPR | S (low-expression) | Transportador de serotonina |
| HTR1A (5-HT1A) | rs6295 | G | Autorreceptor serotoninérgico |

---

## 3. Conexión con NUESTROS hallazgos

| Nuestro hallazgo | Rol del balance OPRM1/5-HTT |
|---|---|
| Eje opioide composicional elevado (TACR1/OPRM1/OPRK1/TAC1) | El eje está "encendido" en sangre; el genotipo decide si eso es funcional (respondedor) o desensibilizado (no-respondedor / uso crónico de opioides). |
| COL9A1/PTN sobrevive todo (matriz + nervio) | Substrato somático que el ejercicio remodela. Hipótesis: su elevación plasmática se da en el genotipo opioide-favorable + SFPN preservada. |
| CA14 ↓ (referencia direccional) | Fuera del alcance genético de este módulo. |

---

## 4. Diseño de análisis (para la cohorte FME)

1. Genotipar rs1799971, 5-HTTLPR, rs6295 en los 75 FM + 75 HC del protocolo.
2. Construir variable de "genotipo opioide-favorable / serotonina-baja" (G + S/Low + G-5HT1A).
3. Test primario (exploratorio): ¿el genotipo predice ΔPPT (respondedor EIH)? Regresión logistica, ajustada por edad/sexo/medicación.
4. Test secundario: ¿el genotipo predice elevación COL9A1/PTN en plasma Olink?
5. **Corrección:** familia-wise (FWER) across el grid genotipo×fenotipo (3 SNPs × 2 fenotipos = 6 tests; α/6).

---

## 5. Honestidad del módulo

- **No computable hoy.** GSE221921 es solo transcriptoma; cero datos genómicos.
- **1 solo estudio fundante** (Tour 2017). Replica limitada; riesgo de sobre-interpretación si se presenta como confirmado.
- **No es diagnóstico.** El balance genético explica parte de la varianza de EIH, no la totalidad.
- **Valor:** convierte "respondedor vs no-respondedor" de observación clínica en variable pre-especificada y testeable en la validación FME (módulo C + D juntos).

---

## 6. Vinculación con el manuscrito

- §4.8 del manuscrito v2.10 cita este módulo.
- El grounding (GROUNDING_FM_VARIANTE_EJERCICIO.md, §5) lista Tour 2017 con PMID 28282362 verificado.
- Pendiente: si se ejecuta la validación FME, este módulo pasa de "hipótesis" a "análisis secundario pre-especificado".
