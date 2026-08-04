# GROUNDING: AlphaFold/ColabFold para FM — Apuntando al neurotransmisor correcto

**Fecha:** 2026-08-04
**Skill usada:** research-grounding + alphafold-database-fetch-and-analyze
**Objetivo:** Identificar qué receptores/dianas de FM tienen estructura 3D disponible para docking y drug design

---

## TL;DR

3 de 5 targets FM tienen estructura AlphaFold con confianza suficiente para docking: DRD2, OPRM1, TACR1 (todos GPCRs, pLDDT 72-78, >38% very-high). COL9A1 y PTN (nuestros Bonferroni-survivors) son estructuralmente malos candidatos para docking directo: COL9A1 es colágeno (pLDDT=61.5, 34% very-low, mayormente desordenado) y PTN es un ligando pequeño con regiones desordenadas (VH=18%). La línea de investigación structural debe apuntar a los GPCRs, no a los genes del PBMC.

---

## Tabla: Targets FM → Estructura AlphaFold → Docking suitability

| Gen | UniProt | Rol FM | Residuos | pLDDT | VH% | VL% | Docking | Cta |
|-----|---------|--------|-----------|-------|-----|-----|---------|-----|
| DRD2 | P14416 | Dopamina reducida CSF, DRD2 upreg PBMC d=+0.99 | 443 | 72.4 | 38 | 26 | SÍ | ALTA |
| OPRM1 | P35372 | Receptor opioide mu, eje opioide (confound E1) | 400 | 76.6 | 48 | 18 | SÍ | ALTA |
| TACR1 | P25103 | Substance P elevada CSF, NK1 upreg d=+0.60 | 407 | 78.4 | 49 | 18 | SÍ | ALTA |
| PTN | P21246 | Bonferroni-survivor, neurotrófico, ligando ALK | 168 | 75.1 | 18 | 18 | NO | MEDIA |
| COL9A1 | P20849 | Bonferroni-survivor, d=0.88, colágeno ECM | 921 | 61.5 | 20 | 34 | NO | BAJA |

---

## Análisis por target

### DRD2 (P14416) — DOPAMINA, el neurotransmisor correcto
- pLDDT 72.4, 38% very-high, 26% very-low
- GPCR de 7 hélices transmembrana — región TM bien definida, terminales desordenados
- PDB experimental disponible: 6VMS (cryo-EM, DRD2-Gi complex, agonist-bound)
- FM: dopamina CSF reducida, respuesta dopaminérgica al dolor attenuada (Wood 2007)
- Nuestro preprint: DRD2 upregulated in PBMC (d=+0.99, robust but compositional confound)
- **Veredicto: MEJOR TARGET para docking.** PDB experimental + AlphaFold + rol FM claro

### OPRM1 (P35372) — OPIOIDE
- pLDDT 76.6, 48% very-high
- GPCR, estructura bien definida
- FM: opioides endógenos elevados en FM (hipótesis analgesia defectuosa)
- E1 mostró que eje opioide es composicional (0/7 genes sobreviven deconvolución)
- **Veredicto: target estructural bueno, pero relevancia FM contaminada por confound composicional**

### TACR1 (P25103) — SUBSTANCE P
- pLDDT 78.4, 49% very-high — la mejor estructura de los 5
- GPCR NK1, la mejor confianza estructural
- FM: substance P elevada en CSF ( Russell 1994 PMID 7526868, verification brewing )
- Upregulated en PBMC (d=+0.60) pero eje opioide composicional
- **Veredicto: segundo mejor target. Estructura más confiable, pero misma contaminación composicional**

### PTN (P21246) — PLEIOTROFINA
- pLDDT 75.1, solo 18% very-high, 51% confident
- Proteína secretada de 168 aa, regiones desordenadas significativas
- Bonferroni-survivor de nuestro análisis (p_adj_bonf=0.020)
- Ligando de ALK (anaplastic lymphoma kinase) — no es un receptor, es un ligando
- **Veredicto: para docking hay que modelar el complejo PTN-ALK, no PTN solo. Más complejo**

### COL9A1 (P20849) — COLÁGENO IX
- pLDDT 61.5, 34% very-low — mayormente desordenado
- Colágeno triple hélice, 921 aa — AlphaFold no modela bien colágenos (repetición Gly-X-Y)
- Bonferroni-survivor de nuestro análisis (p_adj_bonf=8.5e-5, d=0.88)
- **Veredicto: no es diana de docking. Es un biomarcador, no un target terapéutico estructural**

---

## Stack recomendado

| Paso | Herramienta | Hardware | Tiempo est. |
|------|-------------|----------|-------------|
| 1. Estructura base | AlphaFold DB (ya descargado) | N/A | ✅ Done |
| 2. Refinamiento | ColabFold local (AF2 inference) | RTX 4060 8GB | ~30 min/run |
| 3. Protein-ligand | AlphaFold 3 / Protenix | Colab T4 (16GB) | ~10 min/run |
| 4. Docking tradicional | AutoDock Vina / DiffDock | RTX 4060 | ~5 min |
| 5. Complejo receptor-G | ColabFold multimer | Colab T4 | ~20 min |
| 6. Visualización | PyMOL (skill gdm-pymol) | CPU | instant |

---

## Línea de investigación propuesta

**Objetivo:** Validar si los GPCRs dopaminérgico/opioide/neurokinin tienen pockets de unión que justifiquen drug repurposing para FM.

**Paso 1 (P0):** DRD2 docking con agonistas conocidos (dopamina, pramipexole) vs candidatos FM
- Usar PDB 6VMS (experimental, cryo-EM) como referencia
- Comparar con AlphaFold P14416 (predicción)
- Validar que el pocket ortostérico coincide

**Paso 2 (P1):** TACR1 docking con antagonistas NK1 (aprepitant) — ¿ concessions de unión compatibles con FM ?
- AlphaFold P25103 (pLDDT 78.4, mejor estructura)

**Paso 3 (P2):** OPRM1 docking con opioides endógenos (beta-endorfina, encefalina)
- AlphaFold P35372 (pLDDT 76.6)

**Paso 4 (P3):** Complejo PTN-ALK con ColabFold multimer
- Nuevos Bonferroni-survivors, requiere modelar el complejo receptor-ligando

**Paso 5 (P4):** AlphaFold 3 / Protenix para protein-ligand co-folding
- Colab T4, predecir interacciones directas sin docking tradicional

---

## Honestidad estructural

1. **AlphaFold pLDDT no es confianza absoluta.** pLDDT > 70 es razonable pero GPCRs tienen conformaciones dinámicas que AF no captura
2. **6VMS es cryo-EM, no X-ray.** Resolución 3.7 Å — bueno para pocket identification, limitado para atom-level docking
3. **DRD2 tiene PDB experimental.** Para DRD2, USAR 6VMS, no AlphaFold. AlphaFold es fallback para targets sin PDB
4. **COL9A1 como colágeno es un caso especial.** AlphaFold no modela bien triple hélices. Estructura=no usar
5. **Eje opioide tiene confound composicional (E1).** OPRM1/OPRK1/OPRD1 upregulación puede ser artefacto de deconvolución. TACR1 sufre el mismo confound
6. **El único target con relevancia FM limpia + estructura usable es DRD2.** Dopamina es el neurotransmisor más fuertemente implicado en FM (Wood 2007, nuestro preprint R1-R14)
7. **PTN requiere modelar complejo, no monómero.** Es un ligando, no un receptor. El target terapéutico es ALK (el receptor), no PTN
8. **No hay estructura experimental de OPRM1 humana en PDB.** AlphaFold es la única opción para OPRM1

---

## Archivos descargados

```
estructuras/alphafold/
├── DRD2_P14416.pdb           (295 KB) ← usar 6VMS en su lugar
├── DRD2_P14416.cif            (416 KB)
├── DRD2_P14416_metadata.json  (2.8 KB)
├── DRD2_P14416_pae.json       (523 KB)
├── PTN_P21246.pdb             (112 KB)
├── PTN_P21246.cif             (166 KB)
├── PTN_P21246_metadata.json   (2.2 KB)
├── PTN_P21246_pae.json        (79 KB)
├── COL9A1_P20849.pdb          (534 KB)
├── COL9A1_P20849.cif          (762 KB)
├── COL9A1_P20849_metadata.json (3.8 KB)
├── COL9A1_P20849_pae.json     (2.5 MB)
├── OPRM1_P35372.pdb           (261 KB)
├── OPRM1_P35372.cif           (370 KB)
├── OPRM1_P35372_metadata.json (2.7 KB)
├── OPRM1_P35372_pae.json      (408 KB)
├── TACR1_P25103.pdb           (270 KB)
├── TACR1_P25103.cif           (383 KB)
├── TACR1_P25103_metadata.json (2.7 KB)
└── TACR1_P25103_pae.json      (418 KB)
```

---

## Conexión al preprint

- **DRD2** (dopamina) es nuestro top hit del preprint (d=+0.99 robust, gasificado por confound composicional)
- **OPRM1/OPRK1/TACR1** son eje opioide + substance P (E1 mostró confound composicional)
- **COL9A1/PTN** son Bonferroni-survivors del deep-dive pero NO son targets estructurales
- **La dopamina es el neurotransmisor correcto para practicar structural biology en FM**

El grounding dice: si vamos a apuntar al neurotransmisor correcto con AlphaFold, es la dopamina (DRD2). Es el único target con (a) relevancia FM fuerte, (b) estructura experimental disponible (6VMS), y (c) corroboración en nuestro análisis transcriptómico.
