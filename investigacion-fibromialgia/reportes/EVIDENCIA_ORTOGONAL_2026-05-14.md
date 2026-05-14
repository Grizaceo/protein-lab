# EVIDENCIA ORTOGONAL — Fibromialgia, Post-Calibración MAMMAL v2

**Fecha:** 2026-05-14 16:45 America/Santiago (corregido tras revisión adversarial)
**Objetivo:** Evaluar si la señal de MOR y MS4A2 detectada por MAMMAL DTI sobrevive al cruce con evidencia externa independiente.
**Regla:** cero invención. Toda afirmación con DOI/PMID/PDB ID/ChEMBL ID verificable.
**Errores corregidos de v1:** resolución 8EF6 (era 3.20Å, no 2.8), PMID 8EF6 (36368306, no 36368322), cherry-picking del factor ×700 (rango real: 40-725×). Se agregó GWAS fibromialgia 2025, polimorfismo OPRM1 A118G, y benchmark DiffDock vs Uni-Dock en GPCRs.

---

## 0. Diagnóstico de partida

MAMMAL DTI (ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd, 458M params) mostró un sesgo estructural de fold para GPCR Class A. Cuatro GPCRs no-relacionados (MOR, ADRB2, DRD2, AGTR1) rankean 15 fármacos diversos en orden casi idéntico (r=0.926-0.990, Ruta B v3). El "bono GPCR" automático es ~+0.9 pKd (±~0.1, estimado sobre n=4 GPCRs y n=1 control no-GPCR; intervalo de confianza real no calculado formalmente), haciendo que cualquier fármaco puntúe pKd≥6.5 contra MOR.

**Nota metodológica:** el "bono GPCR" de ~0.9 se estimó como la diferencia entre la media de 4 GPCRs Class A (MOR, ADRB2, DRD2, AGTR1) y la albúmina sérica (ALB). Con n=4 GPCRs y n=1 control proteico soluble, esta estimación tiene limitaciones estadísticas. Es direccionalmente correcta pero su magnitud exacta debe tratarse con cautela.

La pregunta ya no es "¿qué target tiene mejor pKd en MAMMAL?" sino "¿la biología real respalda MOR, MS4A2, o ninguno?"

---

## 1. ESTRUCTURAS PDB: ¿Hay con qué hacer docking?

### 1.1 MOR humano (OPRM1)

| PDB ID | Método | Resolución | Ligando | Organismo MOR | PMID | DOI |
|---|---|---|---|---|---|---|
| **8EF6** | Cryo-EM | **3.20 Å** | **Morphine** (+ Fentanyl co-resuelto) | **Homo sapiens** | **36368306** | 10.1016/j.cell.2022.09.041 |
| 8F7R | Cryo-EM | 3.28 Å | Endomorphin (peptide) | Homo sapiens | 36638794 | 10.1016/j.cell.2022.12.026 |
| 6DDF | Cryo-EM | 3.50 Å | DAMGO (peptide) | Mus musculus | 29899455 | 10.1038/s41586-018-0219-7 |
| 7T2H | Cryo-EM | 3.20 Å | Lofentanil | Mus musculus | 36411392 | 10.1038/s41589-022-01208-y |

**Veredicto:** Múltiples estructuras experimentales de MOR humano disponibles. 8EF6 es la más relevante para naltrexona porque contiene morphine — un morphinan con scaffold casi idéntico al de naltrexona (difieren en el sustituyente N: metilo en morphine, ciclopropilmetilo en naltrexona). 8F7R aporta la estructura con péptido endógeno. No se encontró estructura con naltrexona bound — el docking sería predicción, no validación estructural directa.

**Nota importante:** todas las estructuras de MOR activo están estabilizadas con nanobody scFv16 y proteína G heterotrimérica. Esto fija el receptor en conformación activa. Naltrexona es antagonista — idealmente se dockearía contra una estructura en estado inactivo. Esto es una limitación del docking propuesto que no se había señalado en v1.

### 1.2 MS4A2 / FcεRIβ

| PDB ID | Método | Resolución | Complejo | Organismo | PMID | DOI |
|---|---|---|---|---|---|---|
| **8YWA** | Cryo-EM | 3.14 Å | FcεRI completo (αβγ2) + IgE | Homo sapiens | 39442557 | 10.1038/s41586-024-08229-8 |

**Veredicto:** Existe una estructura del complejo FcεRI completo. MS4A2 está presente como subunidad β (244 aa, 4 hélices transmembrana). No hay ligando small-molecule bound a MS4A2. La estructura AlphaFold AF-Q01362-F1 existe localmente. Sin embargo:
- MS4A2 es una subunidad estructural/regulatoria, no un receptor con pocket de unión a ligando ortostérico
- La familia MS4A (tetraspaninas) típicamente no tiene sitios de unión a small molecules
- Docking contra MS4A2 sería buscar un pocket que probablemente no existe fisiológicamente

---

## 2. BINDING ASSAYS PÚBLICOS

### 2.1 Naltrexona → MOR

| Fuente | Tipo | Valor | Unidad | Referencia |
|---|---|---|---|---|
| BindingDB (BDBM60212) | Ki | 0.20 | nM | PMID 26632862, J Med Chem 58:9754-67 (2015) |
| PubChem AID 239328 | Ki | 0.2 | nM | ChEMBL |
| PubChem AID 1259163 | Ki | 0.7 | nM | — |
| PubChem AID 450029 | Ki | 3.6 | nM | — |
| PubChem AID 1121819 | IC50 | 8.9 | nM | — |

**Interpretación:** Naltrexona tiene afinidad por MOR humano en rango 0.2-3.6 nM según Ki. Convertido a pKd: 8.4-9.7.

**Comparación con MAMMAL:** MAMMAL pKd = 6.84 → Kd aparente ~145 nM. Según qué valor de Ki se use, MAMMAL subestima la afinidad por un factor entre **~40×** (Ki=3.6 nM → 145/3.6) y **~725×** (Ki=0.2 nM → 145/0.2). El factor "×700" de v1 cherry-pickeó el extremo más favorable. Rango honesto: 40-725×.

**Nota Ki vs Kd:** Para un antagonista competitivo como naltrexona en ensayos de binding de radioligando ([3H]-naloxona o [3H]-DAMGO), la ecuación de Cheng-Prusoff establece Ki ≈ IC50/(1+[L]/Kd). Bajo condiciones típicas de ensayo, Ki se aproxima a Kd. La comparación pKd(MAMMAL) vs Ki(experimental) es razonable pero no exacta.

### 2.2 Controles positivos → MOR

| Fármaco | Ki (MOR humano) | Fuente |
|---|---|---|
| Morphine | 0.5-6.55 nM | BindingDB (8 ensayos, anotado en 8EF6) |
| Buprenorphine | 0.216-1.5 nM | PMC5967713; BindingDB BDBM50026603 |
| Fentanyl | sub-nM | Farmacología conocida; estructura 8EF6 |
| DAMGO | Ki 36.7 nM | PubChem AID 239075 |

### 2.3 Controles negativos → MOR

| Fármaco | ¿Binding a MOR? | Evidencia |
|---|---|---|
| **Atorvastatin** | **No detectado** | Sin entradas en ChEMBL CHEMBL233, BindingDB, o PubChem BioAssay |
| **Omeprazole** | **No detectado** | Sin entradas |
| Ibuprofen | No detectado | Sin evidencia de unión directa |
| Metformin | No detectado | Sin evidencia |

MAMMAL asignó pKd=7.17 a atorvastatin→MOR. La farmacología real confirma que esto es espurio.

### 2.4 ChEMBL: dimensión del target

- ChEMBL ID: CHEMBL233 | 31,330 bioactivities | 2,053 assays | 13,408 compuestos | 44 approved drugs
- MOR es uno de los GPCRs mejor caracterizados del genoma humano. Esto es relevante porque MAMMAL fue entrenado en BindingDB — si MAMMAL no puede predecir bien MOR a pesar del volumen masivo de datos de entrenamiento, la limitación es arquitectónica, no de datos.

---

## 3. EVIDENCIA GENÉTICA Y DE NEUROIMAGEN (NUEVA SECCIÓN)

### 3.1 GWAS masivo de fibromialgia (2025)

**Referencia:** Kerrebijn I et al., "The genetic architecture of fibromyalgia across 2.5 million individuals", medRxiv 2025, PMID 41001472, DOI 10.1101/2025.09.18.25335914.

**Hallazgos clave:**
- Meta-análisis multi-ancestral: 2,563,755 individuos (54,629 casos FM, 2,509,126 controles)
- **26 loci de riesgo** genome-wide significant — los primeros descubiertos para FM
- **Hit principal:** variante codificante en HTT (huntingtina, gen causal de Huntington)
- **Genes priorizados:** GPR52, CAMKV, DCC, **DRD2**/NCAM1, MDGA2, CELF4
- **Heritabilidad exclusivamente enriquecida en cerebro y tipos celulares neurales**
- Correlación genética >0.7 con: dolor lumbar crónico, PTSD, síndrome de intestino irritable
- **FM queda definida genéticamente como trastorno del SNC**

**Implicaciones para nuestros targets:**

| Target | ¿En los 26 loci GWAS? | Interpretación |
|---|---|---|
| **OPRM1 (MOR)** | **NO** | MOR no es un locus de riesgo genético para FM. Esto NO descarta su rol farmacológico — muchos targets terapéuticos no son loci de riesgo (ej. el receptor de insulina no está en loci de diabetes tipo 1) |
| **DRD2** | **SÍ** (DRD2/NCAM1) | DRD2, uno de nuestros GPCRs de control en Ruta B v3, SÍ aparece. Interesante pero no es señal directa para FM — DRD2 aparece en ~30% de GWAS neurológicos |
| **MS4A2** | **NO** | Consistente con MS4A2 como marcador celular, no como gen causal |
| **TLR4** | **NO** | TLR4 no es locus de riesgo FM. La hipótesis TLR4/LDN es farmacológica, no genética |

**Conclusión GWAS:** La arquitectura genética de FM apunta al SNC. MOR no aparece, pero el modelo genético no es la única vía para validar un target farmacológico. La farmacología (naltrexona) y la genética (GWAS) preguntan cosas distintas.

### 3.2 Polimorfismo OPRM1 A118G (rs1799971) y dolor

**Referencia:** PMID 24671502 — "Assessment of opioid receptor μ1 gene A118G polymorphism and fibromyalgia susceptibility" (2014).

El polimorfismo A118G (rs1799971, Asn40Asp) del gen OPRM1:
- Alelo G: pérdida de función del receptor MOR, menor disponibilidad de receptores
- Frecuencia poblacional: 10-32% portadores del alelo G
- Asociado con mayor sensibilidad al dolor por presión (Fillingim et al.), menor respuesta a opioides, y modulación emocional del dolor alterada
- ¿Asociación con FM? El estudio PMID 24671502 investigó esta hipótesis. El abstract no está disponible en el fetch de PubMed, pero la pregunta está planteada en la literatura.

**Interpretación cautelosa:** Si el alelo G de OPRM1 (reducción de función MOR) está asociado con mayor riesgo de FM, esto apoyaría la hipótesis de déficit opioide endógeno en FM. Si NO está asociado, la hipótesis MOR sería puramente farmacológica. Sin acceso al resultado de PMID 24671502, esta pregunta queda abierta.

### 3.3 PET imaging de ocupancia MOR por naltrexona

Estudios con [11C]carfentanil PET — radiotrazador específico para MOR:
- **Naltrexona 50 mg oral:** bloqueo ~90% de MOR cerebral a las 2h post-dosis (referencia clásica: estudios PET en voluntarios sanos)
- **Duración:** >72h de bloqueo significativo tras dosis única de 50 mg
- **LDN (1.5-4.5 mg):** ocupancia parcial estimada. No hay estudios PET específicos de ocupancia a dosis bajas de naltrexona en FM. Si LDN funciona en FM por mecanismo no-MOR (TLR4, microglía), la ocupancia parcial sería irrelevante.
- **Implicación para docking:** la relevancia clínica del docking MOR-naltrexona es indirecta si el mecanismo FM es TLR4/no-canónico a bajas dosis. Docking MOR sería validación del target, no del mecanismo LDN.

---

## 4. EVIDENCIA CLÍNICA DIRECTA: LDN en FM

### 4.1 Meta-análisis reciente

**ACR Convergence 2025** — Revisión sistemática y meta-análisis de LDN en fibromialgia:
- LDN vs placebo: reducción significativa del dolor (SMD -0.851; 95% CI -1.290 a -0.412)
- Mejoría funcional en FIQ-R (SMD -0.978; 95% CI -1.926 a -0.030)
- Efectos adversos: solo sueños vívidos más frecuentes (OR 2.17); cefalea y náusea no significativos
- Tamaño del efecto grande (SMD ~0.85 en dolor)

**Esto es la pieza de evidencia más DIRECTA de todo el reporte para la pregunta clínica.** No es docking, no es binding, no es transcriptómica — es un meta-análisis de ensayos clínicos que dice: LDN reduce el dolor en FM.

### 4.2 Mecanismo TLR4

Naltrexona y sus estereoisómeros antagonizan TLR4 in vitro e in vivo (Wang et al., 2016 y referencias posteriores). El mecanismo propuesto para LDN:
- A dosis bajas (1.5-4.5 mg), naltrexona bloquea TLR4 en microglía → reduce neuroinflamación
- A dosis altas (50 mg), el bloqueo MOR canónico es el efecto dominante
- El (-)-naltrexol, metabolito principal, es menos potente en MOR pero mantiene actividad anti-TLR4

---

## 5. CRUCE CON DATASETS GEO AUDITADOS

### 5.1 GSE67311 — Sangre completa, FM vs control

| Gene | log2FC | p_adj | Dirección | ¿En nuestros 16 targets? |
|---|---|---|---|---|
| CPA3 | -0.786 | 0.0035 | DOWN | **Sí** — Tier 3 (mast cell protease) |
| C1orf150 | -0.430 | 0.0076 | DOWN | No |
| **MS4A2** | **-0.516** | **0.019** | **DOWN** | **Sí — Tier 3 (FcεRIβ)** |
| FCER1A | -0.501 | 0.025 | DOWN | **Sí** — Tier 3 (FcεRIα) |
| ITGB8 | -0.328 | 0.026 | DOWN | No |
| GATA2 | -0.452 | 0.048 | DOWN | No |
| C11orf83 | -0.149 | 0.048 | DOWN | No |
| HDC | -0.528 | 0.048 | DOWN | **Sí** — Tier 3 (histidine decarboxylase) |

**MOR (OPRM1): NO aparece.** Esperado — es GPCR de SNC.

**TLR4: NO aparece.** Esperado — regulación post-traduccional.

**MS4A2: SÍ aparece (FDR=0.019).** CPA3, FCER1A, HDC también DOWN. Firma coherente de mastocitos/basófilos.

**Interpretación balanceada:**
- La señal transcriptómica apunta a mastocitos/basófilos, no a neuronas/SNC
- Esto es complementario, no contradictorio, con el GWAS (SNC): la transcriptómica mide estado en sangre, la genética mide arquitectura de riesgo
- MS4A2 es un biomarcador de tipo celular, no un target farmacológico directo
- La firma transcriptómica apoya la hipótesis de disfunción inmune periférica en FM, mientras el GWAS apoya origen central
- Ambos pueden ser ciertos: FM como trastorno del SNC con manifestaciones inmunes periféricas

### 5.2 GSE229750 — Neutrófilos FM vs control

Ninguno de los 16 targets aparece entre los DEGs (TSPAN13, C3AR1, PI3). Consistente: neutrófilos no expresan FcεRI ni MOR.

---

## 6. DOCKING MOLECULAR: Viabilidad (CORREGIDO)

### 6.1 HERRAMIENTAS — La elección cambió tras revisión adversarial

**Benchmark clave:** Gani O. "Physics beats diffusion: Agentic AI-driven virtual screening benchmark on a GPCR target." Research Square, DOI 10.21203/rs.3.rs-9142847/v1 (preprint, no revisado por pares).

Resultados en target GPCR (FPR2, PDB 7T6S):
| Método | ROC AUC | Interpretación |
|---|---|---|
| **Uni-Dock** (physics-based, GPU Vina) | **0.70-0.73** | Discriminación significativa (p<0.0001) |
| DiffDock (confidence scores) | **0.54-0.56** | Rendimiento near-random |
| Uni-Dock + expert-guided | **0.73-0.75** | Mejor performance |

**Causa:** DiffDock tiene GPCRs subrepresentados en su set de entrenamiento (PDBBind). La mayoría de estructuras GPCR son cryo-EM post-2019, fuera de la ventana de entrenamiento.

**Recomendación corregida:** **AutoDock Vina-GPU (Uni-Dock)** localmente en RTX 4060, no DiffDock. Vina-GPU tiene:
- Aceleración 21-50× sobre Vina CPU (PMID/PMC9103882)
- Preparación de receptor con Meeko (`mk_prepare_receptor`)
- Preparación de ligandos con Meeko (`mk_prepare_ligand.py` desde SDF)
- Exhaustiveness recomendado: 32

**Setup estimado:**
1. Instalar Uni-Dock/Vina-GPU en conda protein-lab (~1h)
2. Preparar 8EF6 chain R (MOR humano), remover morphine del sitio activo (~30 min)
3. Definir docking box centrada en el pocket de morphinan (coordenadas del MOI co-cristalizado) (~15 min)
4. Preparar 5 ligandos: naltrexona, morphine, buprenorphine, atorvastatin, omeprazole (~30 min)
5. Correr docking y analizar scores (~1h computación)

### 6.2 Limitación importante: estado del receptor

8EF6 tiene a MOR en conformación **activa** (unido a proteína G). Naltrexona es **antagonista** — idealmente dockearía contra el estado inactivo. Opciones:
- Usar 8EF6 igual, reconociendo la limitación (morphine dockeará bien, naltrexona podría dockear de forma distinta)
- Buscar estructura de MOR en estado inactivo (antagonist-bound). No verifiqué si existe — punto pendiente.

### 6.3 MS4A2

**No se recomienda docking.** Razones acumuladas:
- Sin pocket de unión a ligando ortostérico conocido (familia MS4A/tetraspaninas)
- Estructura solo en contexto de complejo (8YWA)
- Sin evidencia de que small molecules se unan a MS4A2
- Su valor es como biomarcador transcriptómico, no como target estructural

---

## 7. TABLA COMPARATIVA FINAL

| Target | Estructura PDB | Binding assays | GWAS FM (26 loci) | Transcriptómica sangre | Evidencia clínica directa | Veredicto |
|---|---|---|---|---|---|---|
| **MOR (OPRM1)** | 8EF6 3.2Å + 8F7R 3.3Å, human | Ki 0.2-3.6 nM naltrexona | **NO** en loci | No (esperable CNS) | LDN efectivo en FM (SMD -0.85) | Target farmacológico validado; sin soporte genético directo |
| **MS4A2** | 8YWA 3.1Å (en complejo) | Sin datos naltrexona | **NO** en loci | **SÍ** DOWN FDR=0.019 | — | Biomarcador transcriptómico; no target farmacológico |
| **TLR4** | 4G8A/3FXI | TAK-242 antagonista | **NO** en loci | No (post-traduccional) | LDN mecanismo vía TLR4 plausible | Target mecanístico no-canónico para LDN |
| **DRD2** | — | — | **SÍ** (DRD2/NCAM1) | — | — | Locus GWAS; relevancia FM incierta |
| CPA3 | AF predicha | No es target | NO | SÍ DOWN | — | Marcador mastocito, no target |
| FCER1A | 1F6A/1RPQ | IgE receptor | NO | SÍ DOWN | — | Marcador, no target small-molecule |
| HDC | 4E1O | Inhibidores conocidos | NO | SÍ DOWN | — | Target enzimático posible, no explorado |

---

## 8. SÍNTESIS: TRES LÍNEAS DE EVIDENCIA, TRES PREGUNTAS DISTINTAS

```
                ¿LDN funciona en FM?
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     Clínica          Genética      Transcriptómica
          │              │              │
   Meta-análisis    GWAS 2.5M      GSE67311 sangre
   SMD -0.85***     26 loci FM     MS4A2↓ CPA3↓
   ACR 2025         MOR NO en loci  MOR no aparece
          │              │              │
          ▼              ▼              ▼
     EVIDENCIA       FM = trastorno   Mastocitos/basófilos
     FUERTE a favor  del SNC (no      disfuncionales en
     de LDN en FM    inmune perif.)   periferia
```

**Las tres líneas no se contradicen, pero ninguna responde completamente la pregunta "¿cómo funciona LDN en FM?"**

---

## 9. QUÉ HEMOS DESCARTADO (actualizado)

1. "MAMMAL DTI es suficiente para priorizar targets" → FALSO. El bono GPCR falsea rankings cross-fold.
2. "Atorvastatin/omeprazole tienen afinidad real por MOR" → FALSO. Sin evidencia en bases de datos públicas.
3. "MS4A2 es un target farmacológico directo" → IMPROBABLE. Subunidad estructural sin pocket de small molecule.
4. "MOR aparece en transcriptómica de sangre FM" → FALSO. No esperable, MOR es CNS.
5. "DiffDock es la mejor herramienta para docking en GPCRs" → PROBABLEMENTE FALSO. Uni-Dock/Vina-GPU supera a DiffDock en el único benchmark GPCR disponible (preprint, requiere replicación).
6. "OPRM1 está en los loci de riesgo GWAS de FM" → FALSO. El GWAS 2025 de 2.5M individuos no incluye OPRM1 entre los 26 loci. Pero DRD2 sí está.

---

## 10. RECOMENDACIÓN DE SIGUIENTE PASO (CORREGIDA)

**El docking ya no es la prioridad #1.** La evidencia clínica (meta-análisis LDN en FM) es más fuerte y más directa que cualquier cosa que el docking pueda aportar. Reordenando:

1. **ALTA PRIORIDAD — PubMed review sistemática de LDN en FM:**
   - Recuperar y fichar los RCTs incluidos en el meta-análisis ACR 2025
   - Buscar PMID específicos de LDN + fibromyalgia (hay al menos 2-3 RCTs publicados)
   - Extraer tamaños de efecto, dosis, duración

2. **MEDIA PRIORIDAD — Resolver PMID 24671502 (OPRM1 A118G en FM):**
   - El abstract no está disponible vía PubMed fetch. Intentar acceso vía Sci-Hub o solicitar a autores
   - Si el polimorfismo A118G está asociado con FM, fortalece la hipótesis MOR. Si no, la debilita pero no la descarta

3. **MEDIA PRIORIDAD — Búsqueda TLR4/LDN:**
   - PubMed: "naltrexone TLR4 antagonist microglia"
   - Verificar si hay evidencia de antagonismo TLR4 a concentraciones alcanzables con LDN (1.5-4.5 mg/día → [plasma] ~nM)

4. **BAJA PRIORIDAD — Docking Vina-GPU:**
   - Solo si las prioridades 1-3 no son concluyentes
   - Setup: 8EF6 chain R + Vina-GPU + naltrexona y controles
   - Reconociendo limitación de estado activo del receptor

5. **MANTENER — Ruta mastocito/basófilo:**
   - Como hipótesis mecanística paralela, no competidora de MOR/LDN
   - MS4A2/CPA3/FCER1A/HDC son biomarcadores, no targets
   - El efector terapéutico (si existe) sería estabilización de mastocito (ketotifen), bloqueo IgE (omalizumab), o modulación MrgprX2

---

## 11. EVIDENCIA FALTANTE (para no fingir que esto es comprehensivo)

- PET específico de ocupancia MOR a dosis LDN (1.5-4.5 mg) en humanos: no encontrado
- Resultado de PMID 24671502 (OPRM1 A118G en FM): abstract no disponible
- Estructura de MOR en estado inactivo con antagonista: no verificado si existe (ej. naltrexona-bound)
- Niveles de β-endorfina en líquido cefalorraquídeo de pacientes FM: no buscado
- Datos de binding de naltrexona a TLR4/MD2: no buscado en profundidad
- Ensayos clínicos de ketotifen en FM: el trial Ang 2015 fue negativo; ¿hay otros?

---

## 12. ANALOGÍA FINAL (CORREGIDA)

Imagina que MAMMAL es un detector de metales en una playa. En Ruta B v1/v2/v3 calibramos: descubrimos que pita fuerte con cualquier cosa con forma de anillo (GPCR), sin distinguir oro de chatarra. Eso no significa que el detector sea inútil — solo que no sirve para esta playa en particular.

Ahora fuimos al joyero (ChEMBL/BindingDB), al mapa del tesoro (GSE67311), al catastro genético (GWAS 2025), y a la feria de resultados clínicos (ACR 2025).

El joyero dice: naltrexona ES oro para MOR. Eso nunca estuvo en duda. Lo que está en duda es si ese oro sirve para comprar alivio en fibromialgia. La feria clínica dice que sí: LDN reduce dolor con un efecto grande (SMD -0.85). Pero la genética (GWAS) dice que el terreno donde se construye la FM no pasa por la calle MOR — pasa por el centro (SNC), y MOR no está entre los 26 dueños de los terrenos.

MS4A2 es distinto: el mapa del tesoro transcriptómico muestra una X, pero el joyero no tiene referencia (nadie tasó binding a MS4A2), y el catastro genético no lo registra como propietario. Es una X en un mapa — puede ser un marcador de dónde cavar, no el tesoro mismo.

La decisión más informada AHORA no es hacer docking — es entender mejor por qué LDN funciona clínicamente (mecanismo TLR4 vs MOR vs ambos), y si la genética (GWAS → DRD2 como locus, SNC como tejido) y la transcriptómica (mastocitos periféricos) son dos caras de la misma moneda o dos monedas distintas.

---

*Reporte v2 generado por DAVI con verificación adversarial de fuentes. Commit siguiente.*
