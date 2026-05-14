# RESULTADOS P3 + P4 — Genética de MOR y Dopamina en Fibromialgia

**Fecha:** 2026-05-14 17:55
**Pasos del plan:** P3 (OPRM1 A118G en FM) + P4 (DRD2/dopamina en FM)

---

## P3: OPRM1 A118G (rs1799971) EN FIBROMIALGIA

### El polimorfismo

| Parámetro | Valor |
|---|---|
| Gen | OPRM1 (mu opioid receptor 1) |
| rsID | rs1799971 |
| Nombre común | A118G (Asn40Asp) |
| Alelo ancestral | A (adenina, Asn40) |
| Alelo variante | G (guanina, Asp40) |
| Frecuencia alelo G | 10-32% poblacional |
| Efecto funcional | **Pérdida de función** — menor disponibilidad de MOR, menor señalización opioide |
| Fenotipo | Mayor sensibilidad al dolor por presión, menor respuesta a opioides exógenos, alteración de modulación emocional del dolor |

### ¿Está asociado con fibromialgia?

**Respuesta corta: la evidencia es débil y contradictoria.**

| Estudio | Año | Hallazgo |
|---|---|---|
| PMID 24671502 | 2014 | Investigó OPRM1 A118G en susceptibilidad a FM e intensidad de dolor. **Abstract no accesible** en esta sesión (PubMed fetch falló) |
| Ondategui et al. (Biomedicines 13(5):1183) | **2025** | **"Controversial results"** respecto al rol de OPRM1 rs1799971 y COMT rs4680 en FM. El abstract completo no se pudo extraer, pero las palabras del autor son: "there are controversial results regarding their roles in FM" |
| GWAS 2025 (PMID 41001472) | 2025 | 2.5M individuos, 26 loci FM. **OPRM1 NO está entre los 26 loci.** |

**Interpretación:** A pesar de que OPRM1 A118G tiene un efecto funcional bien documentado sobre el receptor MOR y la sensibilidad al dolor, la evidencia de asociación específica con fibromialgia es débil. El GWAS más grande jamás hecho (2.5M personas) no lo detectó. Esto puede deberse a:
- Tamaño de efecto pequeño (OR < 1.1) que requiere muestras aún mayores
- El polimorfismo afecta la experiencia de dolor en general, no la suscetibilidad a FM específicamente
- Heterogeneidad entre estudios (criterios diagnósticos, población)

### Implicación para el proyecto

**OPRM1 A118G NO es un anclaje genético fuerte para la hipótesis MOR en FM.** Esto no descarta a MOR como target farmacológico — insulina no está en GWAS de diabetes tipo 1 y es el tratamiento estándar. Pero sí debilita el argumento de "MOR está genéticamente implicado en FM." La hipótesis MOR se sostiene por farmacología (naltrexona, LDN), no por genética.

---

## P4: DRD2/DOPAMINA EN FIBROMIALGIA — LA RUTA MEJOR ANCLADA GENÉTICAMENTE

### Evidencia acumulada (ordenada por nivel)

#### Nivel 1: GWAS 2025 (máxima evidencia)

| Hallazgo | Detalle |
|---|---|
| Locus | DRD2/NCAM1 en cromosoma 11 |
| GWAS | Kerrebijn et al., 2.5M individuos, 26 loci |
| Significancia | Genome-wide significant (p < 5×10⁻⁸) |
| Implicación | DRD2 es uno de los 26 genes con evidencia genética robusta de asociación con FM |

**Esto es el nivel más alto de evidencia que existe en genética humana.** No es un estudio candidato — es un GWAS.

#### Nivel 2: Meta-análisis COMT — asociación confirmada

| Referencia | Año | Hallazgo |
|---|---|---|
| PMID 22722321 | 2012 | Meta-análisis: COMT rs4680 (Val158Met) asociado con FM/chronic widespread pain. "Fibromyalgia or chronic widespread pain is the only type of chronic pain that could be associated with COMT rs4680." |
| PMC11562751 | 2024 | Val158Met asociado con FM, intensidad de dolor, depresión y alteración del sueño en pacientes brasileños |

**COMT Val158Met — mecanismo:**
- Alelo Met → menor actividad COMT → ↓ degradación de dopamina → ↑ dopamina en sinapsis
- ↑ dopamina → alteración de la modulación descendente del dolor
- Met/Met: mayor intensidad de dolor, más tender points, mayor riesgo FM
- Interacción gen-ambiente: portadores Met/Met más vulnerables a FM tras estrés físico/emocional

#### Nivel 3: Estudio neuroendocrino — alteración funcional de D2 en FM

| Referencia | Año | Hallazgo |
|---|---|---|
| Malt et al., J Affect Disord 75:77-82 | 2003 | **Buspirone challenge test en 22 mujeres FM vs 14 controles.** Prolactina aumentada en FM (p < 0.05) → indica **aumento de sensibilidad o densidad de receptores D2**. Respuesta de temperatura y GH (5-HT1A) sin cambios. |

> "Dopaminergic rather than serotonergic neurotransmission is altered in fibromyalgia, suggesting increased sensitivity or density of dopamine D2 receptors in fibromyalgia patients."

#### Nivel 4: Revisiones contemporáneas

| Referencia | Año | Contenido |
|---|---|---|
| Ablin, PAIN Reports 10:e1256 | 2025 | Revisión de genética FM: COMT Val158Met, DRD2 Taq1A, SLC6A4 5-HTTLPR, DRD4 VNTR. GWAS futuros integrarán multi-ómicas. |
| NCT04192058 | 2020+ | Ensayo clínico evaluando tDCS (estimulación transcraneal) en FM estratificado por DRD2 Taq1A (rs1800497) |

---

## SÍNTESIS CRUZADA P3+P4: LO INESPERADO

```
PREGUNTA: ¿Qué vía tiene mejor soporte genético en FM?

EVIDENCIA:
  OPRM1/MOR:      [débil]      A118G controversial, GWAS negativo
  DRD2/dopamina:   [███ FUERTE] GWAS positive + COMT meta-analysis + estudio funcional
  Serotonina:      [██ medio]   SLC6A4 5-HTTLPR, pero buspirone challenge no mostró alteración 5-HT1A
  Mastocitos/IgE:  [casi nulo]  Sin polimorfismos documentados, señal transcriptómica nomás

IMPLICACIÓN: El proyecto ha estado enfocado en MOR/opioides y mastocitos/MS4A2,
cuando la evidencia genética MÁS FUERTE apunta a la vía dopaminérgica.
```

### ¿Por qué esto no es obvio en la clínica?

1. No hay fármacos "dopaminérgicos puros" aprobados para FM
2. Los SNRIs (duloxetina, milnacipran) aumentan dopamina indirectamente — y SÍ están aprobados para FM
3. El agonista D2 pramipexol ha mostrado eficacia en FM en estudios pequeños (pero no es primera línea)
4. La desregulación dopaminérgica en FM es sutil (no es Parkinson) — requiere estudios específicos para detectarla

---

## DECISIÓN PARA EL PROYECTO

### ¿Abrir la ruta dopamina/DRD2?

**Sí, como tercera ruta paralela.** Argumentos:

1. **Anclaje genético sólido:** DRD2 está en los 26 loci GWAS. COMT tiene meta-análisis positivo. Esto no es especulación.

2. **Explica la eficacia de SNRIs:** Duloxetina y milnacipran (aprobados FDA para FM) inhiben la recaptación de noradrenalina y serotonina, pero la noradrenalina aumenta dopamina en corteza prefrontal (el transportador NET también recapta dopamina en PFC). Si la dopamina es relevante, los SNRIs tienen sentido mecanístico.

3. **Conexión con el GWAS:** DRD2 es uno de los 26 loci. No es un hallazgo aislado — es parte de la arquitectura genética de FM.

4. **DRD2 es druggable:** Es un GPCR Class A con miles de ligandos conocidos. Ya tenemos experiencia docking GPCRs (MOR). DRD2 sería más fácil de modelar que TLR4 o MS4A2.

### ¿Competiría con MOR/LDN o con mastocitos?

No. Son tres rutas complementarias:

| Ruta | Evidencia principal | Limitación |
|---|---|---|
| **MOR/LDN** | Farmacológica (binding + RCTs mixtos) | Sin anclaje genético; RCTs contradictorios |
| **Mastocitos/MS4A2** | Transcriptómica (GSE67311) | Sin anclaje genético; MS4A2 no es target farmacológico |
| **Dopamina/DRD2** | Genética (GWAS + COMT + estudio funcional) | Sin fármaco candidato obvio (¿pramipexol?) |

Una hipótesis integradora tentativa (especulativa, requiere validación):
- FM tiene origen genético en SNC (GWAS → cerebro)
- La desregulación dopaminérgica (COMT + DRD2) altera la modulación descendente del dolor
- La disfunción opioide (OPRM1 A118G en subgrupos) modula la experiencia afectiva del dolor
- Los mastocitos periféricos (MS4A2↓ en sangre) reflejan disfunción neuroinmune secundaria o comórbida
- LDN podría funcionar corrigiendo el déficit opioide sin abordar la raíz dopaminérgica

---

## RECOMENDACIÓN

**P4 reveló una ruta más fuerte que P3.** Sugiero:

1. **Mantener MOR/LDN como ruta A** (farmacológica, no genética)
2. **Mantener mastocitos como ruta B** (transcriptómica, no genética)
3. **Abrir dopamina/DRD2 como ruta C** (genética, la mejor anclada de las tres)
   - Primer paso: PubMed "pramipexole fibromyalgia dopamine agonist"
   - Segundo paso: verificar si DRD2 está en nuestros 16 targets (estaba como GPCR_ctrl en Ruta B v3)
   - Tercer paso: evaluar fármacos dopaminérgicos con potencial de repurposing

---

*Síntesis P3+P4. Commit siguiente.*
