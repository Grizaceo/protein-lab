# ESTADO CONSOLIDADO — Fibromialgia, sesión 2026-05-14

**Propósito:** Este archivo reemplaza la lectura de 5 reportes separados. Es el punto de partida para la próxima sesión.
**Reportes fuente (orden cronológico):**
1. EVIDENCIA_ORTOGONAL v1 → v2 (corregida post-revisión adversarial)
2. REVISION_ADVERSARIAL (auto-crítica)
3. PLAN_RECOMENDACIONES (6 pasos)
4. RESULTADOS_P1_P2 (LDN RCTs + TLR4 vs MOR)
5. RESULTADOS_P3_P4 (OPRM1 A118G + DRD2/dopamina)

---

## LO QUE SABEMOS AHORA (post-sesión)

### MAMMAL DTI: descartado como herramienta de ranking

El modelo `ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd` tiene sesgo de fold GPCR Class A. Cuatro GPCRs no-relacionados rankean 15 fármacos en orden casi idéntico (r=0.93-0.99). El "bono GPCR" automático es ~+0.9 pKd. Atorvastatina (estatina, cero actividad opioide) puntúa pKd=7.17 en MOR — más alto que morfina (6.82). No usar MAMMAL para comparar afinidad entre targets de distinto fold.

### MOR (OPRM1): target farmacológico sólido, anclaje genético débil

| Dimensión | Evidencia | Nivel |
|---|---|---|
| Estructural | 8EF6 (cryo-EM, 3.20Å, human MOR + morphine). PMID 36368306 | Sólido |
| Binding | Naltrexona Ki = 0.2-3.6 nM MOR humano. BindingDB, PubChem, ChEMBL (31,330 bioactivities) | Sólido |
| Genético | OPRM1 NO en los 26 loci GWAS 2025 (2.5M individuos). A118G "controversial" en FM (MDPI 2025) | Débil |
| Transcriptómico | MOR no aparece en GSE67311 sangre (esperable: es CNS) | N/A |
| Clínico indirecto | LDN meta-análisis positivo (SMD -0.85), pero RCTs contradictorios (Younger 2013 +, 2024 −) | Mixto |

**Conclusión MOR:** Target farmacológicamente válido, estructuralmente listo para docking, pero sin soporte genético para FM específicamente. La evidencia de LDN en FM es mixta.

### Mecanismo LDN: MOR, no TLR4

La hipótesis TLR4 es bioquímicamente real — (+)-naltrexona se une a MD-2 con Kd=13.7 μM (PMC6700752) y antagoniza TLR4 con IC50~105 μM (PMC4761092). Pero a dosis LDN (4.5 mg/día), la [plasma] de naltrexona es ~10-30 nM — un gap de ~1000×. **TLR4 NO es el mecanismo de LDN a dosis bajas.** MOR (Ki=0.2 nM ≪ [plasma]~10 nM) es farmacocinéticamente plausible. Mecanismo propuesto: bloqueo MOR parcial nocturno → upregulation compensatoria → ventana diurna de analgesia endógena.

### MS4A2/FcεRIβ: biomarcador transcriptómico, no target farmacológico

- DOWN en GSE67311 sangre FM (FDR=0.019), coherente con CPA3↓, FCER1A↓, HDC↓
- Estructura en complejo FcεRI (8YWA, cryo-EM 3.14Å), pero MS4A2 es subunidad estructural sin pocket de small molecule
- Sin datos de binding a naltrexona u otros fármacos
- NO en los 26 loci GWAS 2025
- **Valor:** marcador de depleción/disfunción de mastocitos/basófilos en sangre FM. No es target farmacológico directo.

### DRD2/Dopamina: la ruta MEJOR anclada genéticamente (hallazgo principal de la sesión)

| Dimensión | Evidencia | Nivel |
|---|---|---|
| Genético GWAS | DRD2/NCAM1 entre los 26 loci FM (GWAS 2025, 2.5M) | **Máximo** |
| Genético COMT | Val158Met (rs4680): meta-análisis positivo para FM (PMID 22722321) | Sólido |
| Funcional | Buspirona challenge: aumento de sensibilidad D2 en FM (Malt 2003, n=22) | Moderado |
| Farmacológico | SNRIs (duloxetina, milnacipran) aprobados para FM aumentan dopamina indirectamente | Indirecto |

**Implicación:** La vía dopaminérgica tiene mejor soporte genético que la opioide para FM. DRD2 es GPCR Class A — mismo fold que MOR. Ya tenemos experiencia con GPCRs.

### GWAS 2025: el panorama genético de FM

26 loci de riesgo. Hit principal: HTT (huntingtina). Genes relevantes para nuestro proyecto:
- DRD2/NCAM1 — presente
- OPRM1 (MOR) — ausente
- MS4A2 — ausente
- TLR4 — ausente
- Heritabilidad exclusivamente enriquecida en cerebro y tipos celulares neurales
- FM definida genéticamente como trastorno del SNC

---

## TRES RUTAS ACTIVAS (ordenadas por anclaje genético)

```
RUTA C (DOPAMINA/DRD2)         RUTA A (MOR/LDN)           RUTA B (MASTOCITOS)
│                              │                          │
│ GWAS: DRD2 en 26 loci        │ GWAS: OPRM1 NO           │ GWAS: MS4A2 NO
│ COMT: meta-análisis +        │ Binding: Ki 0.2-3.6 nM   │ Transcr: CPA3/MS4A2↓
│ Funcional: D2↑ en FM         │ Clínico: LDN mixto       │ Farmacol: sin target
│ Fármaco: ¿pramipexol?        │ Estructura: 8EF6 lista   │ Estructura: 8YWA complejo
│                              │                          │
│ Anclaje: ████████████ FUERTE │ Anclaje: ██████ MODERADO │ Anclaje: ████ DÉBIL
│ Novedad: ██████████ ALTA     │ Novedad: ██ BAJA         │ Novedad: ████████ ALTA
│ Druggable: ██████ SÍ (GPCR)  │ Druggable: ██████ SÍ     │ Druggable: ██ NO (biomarcador)
```

---

## QUÉ HEMOS DESCARTADO

1. MAMMAL DTI como herramienta de ranking cross-fold
2. TLR4 como mecanismo de LDN a dosis bajas (gap farmacocinético ~1000×)
3. MS4A2 como target farmacológico directo (subunidad estructural, sin pocket)
4. OPRM1 como locus de riesgo genético para FM (GWAS negativo)
5. DiffDock como herramienta de docking para GPCRs (benchmark: Uni-Dock gana AUC 0.73 vs 0.54)
6. Atorvastatina/omeprazol como ligandos reales de MOR (sin evidencia en bases de datos públicas)

---

## ERRORES COMETIDOS Y CORREGIDOS (higiene)

| Error | Corregido en |
|---|---|
| Resolución 8EF6: "2.8 Å" → real: 3.20 Å | EVIDENCIA_ORTOGONAL v2 |
| PMID 8EF6: 36368322 → real: 36368306 | EVIDENCIA_ORTOGONAL v2 |
| Factor ×700 → rango honesto: 40-725× | EVIDENCIA_ORTOGONAL v2 |
| DiffDock como recomendación → Vina-GPU | EVIDENCIA_ORTOGONAL v2 |
| Omisión GWAS 2025, OPRM1 A118G, PET | EVIDENCIA_ORTOGONAL v2 |
| Sesgo pro-MOR en tono | Balanceado en v2 |

---

## PRÓXIMOS PASOS (P5 y P6 del plan quedan pendientes)

**P5 [BAJA] — Docking Vina-GPU naltrexona vs MOR**
- Justificación: validar pipeline de docking. MOR es GPCR bien caracterizado, 8EF6 tiene ligando co-cristalizado.
- NO es para "descubrir" que naltrexona se une a MOR (ya se sabe).
- Setup: Vina-GPU local en RTX 4060, 5 ligandos, exhaustiveness=32.
- Criterio éxito: morphine RMSD<2Å vs pose co-cristalizada.

**P6 [BAJA] — PET occupancy LDN**
- ¿Existen estudios [11C]carfentanil PET a dosis LDN (1.5-4.5 mg)?
- Nice to have, no bloqueante.

**RUTA C — dopamina/DRD2 (NUEVA, alta prioridad)**
- PubMed: "pramipexole fibromyalgia dopamine agonist"
- Verificar DRD2 en nuestros 16 targets (era GPCR_ctrl en Ruta B v3)
- Evaluar fármacos dopaminérgicos con potencial de repurposing

---

## ARCHIVOS DE REFERENCIA (todos en investigacion-fibromialgia/reportes/)

| Archivo | Contenido |
|---|---|
| `EVIDENCIA_ORTOGONAL_2026-05-14.md` | Reporte completo corregido (v2). Tablas, estructuras PDB, binding, GEO, GWAS |
| `REVISION_ADVERSARIAL_2026-05-14.md` | Auto-crítica del reporte v1. Errores, sesgos, omisiones |
| `PLAN_RECOMENDACIONES_2026-05-14.md` | 6 pasos con prioridades, diagrama de decisión |
| `RESULTADOS_P1_P2_2026-05-14.md` | LDN RCTs (Younger+, 2024−) + gap TLR4 1000× |
| `RESULTADOS_P3_P4_2026-05-14.md` | OPRM1 A118G débil + DRD2/dopamina fuerte |
| `ANALISIS_RUTA_B_V3_2026-05-14.md` | Calibración GPCR MAMMAL (sesión anterior) |

---

## UNA FRASE PARA LA PRÓXIMA SESIÓN

*"MAMMAL no mide afinidad. TLR4 no explica LDN. MOR es target real pero sin anclaje genético. Los mastocitos están alterados en sangre pero no son druggables. Y la dopamina —que ni siquiera estaba en el radar al empezar— resultó tener la mejor evidencia genética de todas. La próxima sesión: docking MOR o pivotar a DRD2."*

---

*Consolidado generado por DAVI, 2026-05-14. Commit siguiente.*
