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
