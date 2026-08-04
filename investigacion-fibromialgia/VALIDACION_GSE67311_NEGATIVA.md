# VALIDACIÓN CRUZADA GSE67311 — Resultado NEGATIVO (bloqueo científico)

**Fecha:** 2026-08-03
**Dataset:** GSE67311 — "Peripheral Blood Gene Expression in Fibromyalgia Patients" (whole blood, Affymetrix GPL11532)
**Paper declara:** 70 FM vs 70 HC | **Metadata GEO real:** 67 FM vs 75 HC (142 total — diferencia reportada)
**Script:** `scripts/validate_fm_biomarkers_gse67311.py` (reproducible)

---

## VEREDICTO: LOS PROXIES DE GSE221921 NO SE REPRODUCEN EN GSE67311

| Gen | GSE221921 (PBMC) | GSE67311 (whole blood) | Reproduce? |
|-----|------------------|------------------------|------------|
| TAC1 | FC=2.10, p=0.0002 | FC=1.004, p=0.495, NS | ❌ NO |
| OPRM1 | FC=2.28, p<0.0001 | FC=1.020, p=0.160, NS | ❌ NO |
| IL6 | FC=1.66, p=0.0002 | FC=1.023, p=0.524, NS | ❌ NO |
| PENK | FC=1.38, p=0.0031 | FC=1.038, p=0.031, Bonf=0.248 | ⚠️ trend (no sobrevive Bonf) |
| PCSK1N | FC=0.76 (↓) | FC=1.041 (↑), p=0.045 | ❌ INVIERTE DIRECCIÓN |
| LGALS3BP | FC=0.75 (↓), p=0.0003 | FC=0.956 (↓), p=0.337, NS | ⚠️ dirección consistente, NS |
| MDH1 | FC=0.86, NS | FC=0.985, NS | ✅ NS en ambos |

---

## ITEM C (2026-08-03): DECONVOLUCIÓN CELULAR — LA HIPÓTESIS DE DILUCIÓN NO SE SOSTIENE

**Pregunta:** ¿la no-replicación se explica porque whole blood diluye la señal linfocitaria por neutrófilos?

**Resultado (marcadores de tipo celular en GSE67311):**
- Composición celular FM vs HC: ESENCIALMENTE IDÉNTICA
  - Neutrófilos: FM=10.92 vs HC=10.89 (7 marcadores)
  - Linfocitos T: FM=9.89 vs HC=9.98 | B: 8.88 vs 8.88 | monocitos: 11.11 vs 11.13 | NK: 8.43 vs 8.51
- Correlación score neutrófilo vs proxies: débil y mixta
  - TAC1: r=+0.07, NS | IL6: r=-0.02, NS | OPRM1: r=-0.22, p=0.008 | PENK: r=-0.13, NS | PCSK1N: r=-0.02, NS

**Conclusión del item C:** la discrepancia NO es dilución por neutrófilos — la composición celular
es comparable entre grupos y los proxies no correlacionan sistemáticamente con la fracción
neutrofílica. Las explicaciones restantes (sin datos nuevos) son:
1. Diferencia de plataforma: RNA-seq FPKM (GSE221921) vs microarray RMA log2 (GSE67311)
2. Heterogeneidad de cohorte: pacientes distintos, criterios de inclusión distintos
3. Efectos reales pero pequeños (d≈0.2-0.5) que no sobreviven ruido entre plataformas
4. Los hallazgos de GSE221921 son parcialmente cohorte-específicos

**Implicancia práctica:** los proxies son PBMC/RNA-seq-específicos. El protocolo Olink mide
plasma (proteína), que es el test definitivo — no se puede resolver con más transcriptómica
de sangre. La decisión A (aceptar limitación + Olink como arbitro) queda reforzada.

## ITEM E (2026-08-03): EJE OPIOIDE/TAQUIKININA COMPLETO EN GSE67311 — NO REPLICA, PERO LA CO-EXPRESIÓN SÍ ES ESTABLE

**Pregunta (pendiente C):** ¿replican TACR1/OPRM1/OPRK1 (receptores del eje) en whole blood?
El análisis previo solo cubría TAC1/OPRM1/IL6. **Script:** `scripts/validate_opioid_axis_gse67311.py`
(Bonf x5 propio, Mann-Whitney + Cohen's d, co-expresión Spearman FM/HC).

**Tabla 2. Eje opioide/taquininina — GSE67311 whole blood (FM=67, HC=75)**

| Gen | GSE221921 (PBMC) | GSE67311 (whole blood) | Reproduce? |
|-----|------------------|------------------------|------------|
| TACR1 | FC=2.73, d=+0.60 | FC=1.008, p=0.480, Bonf=1.0, d=+0.050 | ❌ NO |
| OPRM1 | FC=2.28, d=+0.53 | FC=1.020, p=0.160, Bonf=0.80, d=+0.222 | ❌ NO |
| OPRK1 | FC=1.78 | FC=1.021, p=0.878, Bonf=1.0, d=+0.191 | ❌ NO |
| TAC1 | FC=2.10, d=+0.47 | FC=1.004, p=0.495, Bonf=1.0, d=+0.038 | ❌ NO |
| PENK | FC=1.38, p=0.0031 | FC=1.038, p=0.031, Bonf=0.155, d=+0.317 | ⚠️ trend (no sobrevive Bonf) |

**Veredicto:** el upregulation absoluto del eje NO replica en whole blood — todos FC≈1.0,
ninguno sobrevive Bonferroni. Esto extiende la no-replicación de los 3 genes originales
(TAC1/OPRM1/IL6) a los 5 genes del eje completo, incluyendo los dos receptores que faltaban
(TACR1, OPRK1). La señal es PBMC-específica, no una propiedad de sangre periférica total.

**Hallazgo matizado — la co-expresión SÍ es estable:** aunque la expresión absoluta no cambia,
la estructura de co-regulación del eje en FM whole blood es ROBUSTA y en algunos pares MÁS
fuerte que en PBMC:

| Par | FM rho (GSE67311) | p | Referencia PBMC rho |
|-----|-------------------|-----|---------------------|
| TACR1–OPRK1 | **+0.736** | <0.001 | 0.31–0.63 |
| OPRM1–OPRK1 | **+0.530** | <0.001 | 0.31–0.63 |
| TACR1–OPRM1 | **+0.420** | <0.001 | 0.31–0.63 |
| OPRM1–TAC1 | +0.363 | 0.003 | 0.31–0.63 |
| OPRK1–PENK | +0.375 | 0.002 | 0.31–0.63 |
| TACR1–TAC1 | +0.189 | 0.125 | NS |

Interpretación: la co-regulación coordinada del circuito (receptores NK1/mu/kappa co-expresados)
es un rasgo estable de sangre periférica en FM, presente incluso en whole blood donde el
upregulation absoluto desaparece. El eje es un módulo transcripcional coherente — lo que
falla en whole blood es la AMPLITUD (fold-change), no la organización del circuito.

**Implicancia:** (1) confirma que la discrepancia PBMC vs whole blood es de compartimento/
sensibilidad, no de biología ausente — el circuito existe y está coordinado en sangre total;
(2) el test definitivo sigue siendo plasma proteico (Olink/ELISA): si la co-expresión es
estable pero la amplitud es dependiente de compartimento, la medición plasmática debe
priorizar sensibilidad (panel Olink Explore HT sobre Target 96); (3) la dirección de CA14
(↓ plasmática) no se ve afectada por este resultado.

## QUÉ SIGNIFICA (honestidad cruda)

1. **La "cross-validación completada" de la madrugada era falsa.** Se documentó "GSE67311
   cross-validation ✅" basándose en la documentación del paper (FTP bloqueado entonces), NO en
   datos reales. Ahora que descargamos los datos, NO reproducen. Eso se corrige aquí.

2. **Diferencia de compartimento real:** GSE221921 = PBMCs (linfocitos/monocitos purificados);
   GSE67311 = whole blood (incluye neutrófilos, que expresan IL-8 masivamente). Es plausible que
   los efectos de linfocitos se diluyan en sangre total. Esto NO excusa la no-replicación, pero
   contextualiza: los proxies son de PBMC, no de sangre total.

3. **PCSK1N invierte dirección** — esto es lo más preocupante. Un proxy que invierte entre
   cohortes no es un proxy confiable. Su re-clasificación a "candidato" (item adversarial) debe
   revertirse a "no confirmado" hasta que se entienda la discrepancia.

4. **TAC1/OPRM1/IL6 no se reproducen** — los tres "HIGH" de GSE221921 colapsan en whole blood.
   El claim "proxies periféricos validados" debe rebajarse a "proxies PBMC-específicos,
   no-replicados en sangre total" hasta nueva evidencia.

## POR QUÉ ES UN BLOQUEO (no solo un matiz)

El item 4 (especificidad vs ME/CFS) y el item 5 (correlación eje opioide) asumían proxies sólidos.
Con GSE67311 negativo, la prioridad cambia: primero hay que entender la discrepancia
PBMC vs whole blood, o los siguientes pasos construyen sobre arena.

## OPCIONES (para decisión de Cristóbal)

- **A)** Aceptar la limitación: proxies PBMC-específicos, y el protocolo Olink valida en plasma
  (que es el compartimento relevante — la no-replicación en whole blood no invalida la hipótesis
  plasmática, la matiza).
- **B)** Buscar un tercer dataset PBMC para validar (si existe GSE con PBMC de FM).
- **C)** Investigar el porqué de la discrepancia (deconvolución de tipos celulares en GSE67311:
  ¿el efecto se diluye por neutrófilos?).
- **D)** Parar la línea de proxies periféricos y re-enfocar.

**Recomendación honesta:** A + C. La no-replicación en whole blood era parcialmente esperable
(compartimento distinto), y el protocolo Olink mide plasma, no sangre total. Pero PCSK1N invirtiendo
dirección es una bandera roja que exige documentarse, no ignorarse.
