# PROTOCOL — Fenotipado del Subfenotipo FM Respondedor al Ejercicio (FME)

**Fecha:** 2026-08-07
**Estado:** Diseño (no ejecutado). Deriva de GROUNDING_FM_VARIANTE_EJERCICIO.md y del manuscrito v2.10 (§4.7).
**Propósito:** Convertir los hallazgos transcriptómicos (COL9A1/PTN + eje opioide composicional) en una estratificación mecánica de FM: respondedor-ejercicio (periférico/somático modulable) vs no-respondedor (sensibilización central / desensibilización opioide).

---

## 1. Justificación (anclada en literatura verificada)

- EIH (analgesia inducida por ejercicio) es mediada por opioides endógenos — naloxona la bloquea (Sluka 2018, PMID 30113953).
- En FM la modulación endógena está disfuncional en muchos pacientes → define respondedor vs no-respondedor (Lannersten 2010, PMID 20621420).
- ~49% de los diagnósticos FM tienen small-fiber polyneuropathy (SFPN) periférico detectable por biopsia de piel (Oaklander 2013, PMID 23748113; Üçeyler 2013, PMID 23474848) → sustrato somático de COL9A1/PTN.
- El ejercicio revierte sensibilización central en respondedores (Ellingson 2016, PMID 26927193).
- Nivel de evidencia del ejercicio en FM: efecto pequeño-moderado, variable (Bidonde 2017, PMID 28636204; Busch 2013, PMID 24362925).

---

## 2. Diseño del Estudio

**Tipo:** Transversal anidado en cohorte de validación (paralelo a PROTOCOL_Olink_FM_Biomarker_Validation.md).
**Sujetos:** 75 FM (criterios ACR 2016) + 75 HC, emparejados por edad/sexo.
**Estratificación obligatoria:** estrato libre-de-opioides (excluye uso crónico >3 meses) — porque el eje opioide en sangre puede reflejar efecto farmacológico, no biológico de enfermedad (Limitación 10 del manuscrito).

### 2.1 Fenotipado de Respondedor (EIH)
- **Basal:** umbral de dolor a presión (PPT, algómetro manual) en punto tender y sitio control, pre-ejercicio.
- **Challenge:** cicloergómetro 15 min a 60% FCmáx (o caminata en cinta, validado en Ellingson 2016).
- **Post:** PPT a 0, 10 y 30 min post-ejercicio.
- **Definición de respondedor:** ΔPPT ≥ +20% a los 10 min vs basal (criterio de la literatura de EIH; umbral ajustable en análisis de sensibilidad).

### 2.2 Eje Periférico / Somático
- **Plasma Olink:** COL9A1, PTN (analitos primarios); CA14 (referencia direccional); + cualquier analito del eje opioide cubierto por el panel Olink (verificar cobertura antes deejecutar — no asumir).
- **Biopsia de piel (SFPN):** punch 3 mm en pierna distal (tobillo), tinción PGP9.5 / anti-CGRP; densidad de fibras epidérmicas (IENFD, fibers/mm) cuantificada por patólogo ciego. Umbral diagnóstico SFPN: <7 fibers/mm (corte estándar).
- **Conectar con COL9A1/PTN:** hipótesis de que la elevación plasmática de COL9A1/PTN se da en el subgrupo con IENFD preservada/modificable (periférico-somático), no en el subgrupo de sensibilización central pura.

### 2.3 Genotipado (módulo D, ver CONSTRAINTES)
- OPRM1 rs1799971 (A118G), 5-HTTLPR, 5-HT1A rs6295.
- Test: ¿la combinación opioide-favorable / serotonina-baja predice respondedor (ΔPPT) y elevación COL9A1/PTN?

---

## 3. Hipótesis de Convergencia (lo que se predice)

| Grupo FME | EIH (ΔPPT) | COL9A1/PTN plasma | IENFD (SFPN) | Interpretación |
|---|---|---|---|---|
| Respondedor | ↑ ≥20% | elevado | preservada/modificable | Periférico-somático modulable (FME) |
| No-respondedor | plano/↓ | eje opioide composicional domina | variable | Sensibilización central / desensibilización opioide |

Si se confirma: nuestros hallazgos transcriptómicos dejan de ser "asociaciones no estratificadas" y pasan a ser marcadores de un subfenotipo operacional.

---

## 4. Poder Estadístico

El brazo Olink hereda el cálculo del protocolo principal: 75+75 da 88% de poder para detectar COL9A1/PTN (d=0.6–0.9, α=0.05). Para la sub-estratificación EIH (≈50% respondedores esperados) el n efectivo cae a ~37/brazo — poder ~55% para efectos pequeños; por eso el diseño es **exploratorio** para la sub-estratificación, confirmatory solo para COL9A1/PTN en plasma.

---

## 5. Limitaciones del Diseño (honestidad)

1. **No local.** Requiere recrutamiento clínico, kits Olink, biopsia de piel, genotipado — ninguno ejecutable en este entorno.
2. **EIH es ruidosa.** El umbral ΔPPT 20% es arbitrario; el ejercicio puede flarear en algunos FM (fenómeno documentado). Control con HC emparejados.
3. **SFPN no es específica de FM** — es comorbilidad, no causa. Su medición sirve para estratificar, no para diagnosticar.
4. **Genotipado es hipótesis-generadora** (Tour 2017 es 1 estudio, n moderado). Sin datos locales; pendiente de cohorte.
5. **Dirección causal abierta:** ¿el ejercicio "arregla" el eje opioide o los respondedores lo tienen sano? Literatura sugiere ambas (Bruehl 2020); en FM falta RCT directo.

---

## 6. Estado de Ejecución

- [ ] Recrutamiento (pendiente — requiere institución clínica)
- [ ] Aprobación ética (pendiente)
- [ ] Ejecución Olink (pendiente — requiere kit)
- [ ] Biopsia SFPN (pendiente — requiere dermatopatólogo)
- [ ] Genotipado OPRM1/5-HTT (pendiente)
- [ ] Análisis de convergencia (pendiente)

**Este protocolo es el entregable del módulo C. No se ejecuta en el protein-lab local; es la hoja de ruta para validación externa.**
