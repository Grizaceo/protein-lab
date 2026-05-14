# PLAN DE RECOMENDACIONES — Fibromialgia, Post-Evidencia Ortogonal

**Fecha:** 2026-05-14 17:00
**Basado en:** EVIDENCIA_ORTOGONAL v2 + REVISION_ADVERSARIAL
**Regla:** cada paso tiene un "¿para qué?" y un "¿qué decisión depende de esto?"

---

## Panorama actual

Tres líneas de evidencia convergen parcialmente:

```
EVIDENCIA CLÍNICA        EVIDENCIA GENÉTICA       EVIDENCIA TRANSCRIPTÓMICA
│                        │                        │
LDN reduce dolor         GWAS 2.5M: FM = SNC      GSE67311: mastocitos↓
SMD -0.85 (ACR 2025)     MOR NO en 26 loci        MS4A2↓ CPA3↓ FCER1A↓
│                        DRD2 SÍ en loci           MOR no aparece en sangre
│                        │                        │
└────────────────────────┴────────────────────────┘
                         │
              MOR es target farmacológico válido
              pero la genética no lo señala como causal
              y la sangre no lo detecta.
                         │
              ¿Mecanismo LDN = MOR o TLR4?
              ¿FM = SNC con epifenómeno periférico?
              ¿Mastocitos = causa o consecuencia?
```

---

## PLAN DE ACCIÓN (ordenado por impacto/viabilidad)

---

### PASO 1 [ALTA PRIORIDAD · 30 min] — Fichar los RCTs de LDN en FM

**Qué:** Recuperar y extraer datos de los ensayos clínicos incluidos en el meta-análisis ACR 2025.

**Búsqueda PubMed:**
```
"low dose naltrexone" AND fibromyalgia
naltrexone low dose fibromyalgia randomized
```

**Para cada RCT encontrado, extraer:**
- PMID, año, n, diseño (crossover/paralelo)
- Dosis LDN (mg/día), duración
- Outcome primario: escala de dolor (VAS/NRS)
- Outcome secundario: FIQ-R, fatiga, sueño
- Tamaño del efecto (Cohen's d o SMD)
- Efectos adversos

**¿Para qué sirve esto?**
- Si hay ≥3 RCTs con efecto positivo consistente → LDN queda como la recomendación más sólida del proyecto
- Si los RCTs son pequeños/frágiles (n<30, riesgo de sesgo alto) → la evidencia clínica es más débil de lo que parece
- Nos da números concretos para citar, no solo "ACR 2025 dijo SMD -0.85"

**Herramienta:** web_search PubMed + web_extract abstracts

**Decisión que depende de esto:** ¿Seguir invirtiendo en la hipótesis LDN como recomendación principal del proyecto?

---

### PASO 2 [ALTA PRIORIDAD · 15 min] — Resolver mecanismo TLR4 vs MOR para LDN

**Qué:** Buscar si naltrexona a dosis bajas (1.5-4.5 mg) antagoniza TLR4 a concentraciones plasmáticas alcanzables.

**Búsqueda PubMed:**
```
naltrexone TLR4 antagonist microglia MD2
(+)-naltrexone OR (+)-naloxone TLR4
naltrexone toll-like receptor 4 mechanism low dose
```

**Pregunta clave a responder:**
- ¿A qué concentración (nM/µM) naltrexona antagoniza TLR4 in vitro?
- ¿Las concentraciones plasmáticas de LDN (1.5-4.5 mg/día) alcanzan ese rango?
- Si no: la hipótesis TLR4 es inviable a dosis LDN → el mecanismo sería MOR
- Si sí: la hipótesis TLR4 es plausible → LDN funciona por vía no-opioide

**¿Para qué sirve esto?**
- Define el mecanismo. Si es MOR → el docking tiene sentido. Si es TLR4 → el docking en MOR es irrelevante para FM.
- Informa si buscar fármacos TLR4 puros (TAK-242/resatorvid) sería mejor estrategia que naltrexona

**Herramienta:** PubMed vía web_extract (ncbi.nlm.nih.gov)

**Decisión que depende de esto:** ¿Hacer docking en MOR o pivotar a screening de antagonistas TLR4?

---

### PASO 3 [MEDIA PRIORIDAD · 20 min] — Resolver OPRM1 A118G en fibromialgia

**Qué:** Determinar si el polimorfismo rs1799971 (A118G) de OPRM1 está asociado con fibromialgia.

**Fuente primaria:** PMID 24671502 — intentar acceso vía:
1. PubMed Central (PMC) — verificar si hay versión gratuita
2. Sci-Hub (si es aceptable para el proyecto)
3. Contactar autores (baja probabilidad de respuesta rápida)

**Fuentes alternativas:**
```
OPRM1 A118G fibromyalgia association case-control
rs1799971 fibromyalgia
mu opioid receptor polymorphism chronic widespread pain
```

**¿Para qué sirve esto?**
- Si A118G está asociado con FM → la hipótesis MOR tiene soporte genético además de farmacológico
- Si NO está asociado → MOR es target farmacológico puro, sin anclaje genético. No descarta LDN pero cambia el peso de la evidencia

**Decisión que depende de esto:** Peso relativo de la hipótesis MOR en el write-up final del proyecto

---

### PASO 4 [MEDIA PRIORIDAD · 20 min] — Conectar GWAS con ruta dopamina/DRD2

**Qué:** El GWAS 2025 encontró DRD2/NCAM1 entre los 26 loci de FM. DRD2 fue uno de nuestros GPCRs de control en Ruta B v3.

**Búsqueda:**
```
DRD2 fibromyalgia dopamine chronic pain
DRD2 chronic widespread pain polymorphism
dopamine fibromyalgia pathophysiology
```

**¿Para qué sirve esto?**
- DRD2 está en los 26 loci GWAS → no es ruido
- Si la vía dopaminérgica está implicada en FM, abre una ruta completamente distinta a opioides/mastocitos
- Podría explicar por qué duloxetina (SNRI, aumenta dopamina indirectamente) funciona en FM

**Decisión que depende de esto:** ¿Abrir una tercera ruta de investigación (dopamina/DRD2) o mantener foco en MOR/TLR4/mastocitos?

---

### PASO 5 [BAJA PRIORIDAD · 2-3h setup + ejecución] — Docking Vina-GPU: naltrexona vs MOR

**Qué:** Docking molecular de naltrexona + controles contra MOR humano (8EF6) usando AutoDock Vina-GPU.

**Solo ejecutar si:**
- El Paso 2 indica que el mecanismo es MOR (no TLR4) → el docking sería relevante
- O si queremos validación estructural independientemente del mecanismo clínico

**Setup:**
1. `conda activate protein-lab`
2. Instalar Vina-GPU desde https://github.com/ccsb-scripps/AutoDock-GPU
3. Bajar 8EF6 chain R → limpiar (remover Gi, scFv, morphine) → preparar con Meeko
4. Preparar ligandos con Meeko desde SDF (PubChem):
   - naltrexona (CID 5360515)
   - morphine (CID 5288826) — control positivo
   - buprenorphine (CID 644073) — control positivo
   - atorvastatin (CID 60823) — control negativo
   - omeprazole (CID 4594) — control negativo
5. Caja de docking centrada en coordenadas del MOI co-cristalizado en 8EF6
6. Exhaustiveness=32, 20 poses por ligando

**Criterio de éxito:**
- Morphine debe dockear con RMSD <2Å respecto a la pose co-cristalizada (control de método)
- Naltrexona debe mostrar score comparable o mejor que morphine
- Atorvastatin y omeprazole deben mostrar scores significativamente peores

**¿Para qué sirve esto?**
- Cierra el círculo estructural: MAMMAL no pudo → binding assays sí → ¿docking también?
- Si el docking recapitula el ranking conocido (morphine≈naltrexona ≫ atorvastatin), valida el pipeline
- Si no, indica que ni siquiera docking basado en estructura resuelve el problema GPCR

---

### PASO 6 [BAJA PRIORIDAD · INVESTIGACIÓN] — PET occupancy LDN

**Qué:** Buscar si existen estudios de ocupancia MOR por [11C]carfentanil PET a dosis LDN.

**¿Para qué sirve esto?**
- Si LDN ocupa <20% de MOR → mecanismo TLR4 es más plausible
- Si LDN ocupa >50% de MOR → mecanismo MOR directo es plausible incluso a dosis bajas
- Pero si no existen estos estudios, es un vacío de conocimiento, no una refutación

**No es bloqueante para el proyecto** — es más bien un "nice to have" para el write-up.

---

## DIAGRAMA DE DECISIÓN

```
PASO 1: Fichar RCTs LDN en FM
│
├── RCTs sólidos (n>50, efecto consistente)
│   │
│   └── PASO 2: ¿Mecanismo TLR4 o MOR?
│       │
│       ├── TLR4 plausible a dosis LDN
│       │   └── Recomendación: pivotar a antagonistas TLR4 puros
│       │       (TAK-242/resatorvid como lead compound)
│       │
│       └── Solo MOR a dosis relevantes
│           └── PASO 5: Docking Vina-GPU naltrexona vs MOR
│               └── Si docking valida → LDN/MOR como ruta principal
│
└── RCTs frágiles (n<30, heterogéneos)
    └── Recomendación: LDN es promisorio pero no conclusivo
        Necesitamos más evidencia antes de cerrar el capítulo
        → Esperar más RCTs o buscar datos de mundo real (registros)
```

---

## QUÉ NO HACER

- **No correr más MAMMAL.** Ya sabemos lo que mide. Es un detector de fold GPCR, no de afinidad.
- **No hacer docking contra MS4A2.** Es subunidad estructural sin pocket. Sería forzar la herramienta.
- **No abrir la ruta Nav1.8 sin evidencia FM específica.** Es gran target de dolor pero sin conexión FM documentada.
- **No hacer docking en DiffDock/Colab.** El benchmark GPCR muestra que Vina-GPU es superior.
- **No mezclar las tres líneas de evidencia como si dijeran lo mismo.** Clínica ≠ Genética ≠ Transcriptómica. Preguntan cosas distintas.

---

## RESUMEN PARA PRÓXIMA SESIÓN

Si tenemos 60-90 minutos:

| Minuto | Acción | Herramienta |
|---|---|---|
| 0-5 | Cargar este plan | — |
| 5-35 | PASO 1: PubMed "low dose naltrexone fibromyalgia RCT" | web_search + web_extract |
| 35-50 | PASO 2: PubMed "naltrexone TLR4 antagonist microglia" | web_search + web_extract |
| 50-70 | PASO 3: PMID 24671502 (OPRM1 A118G FM) + alternativas | web_extract + web_search |
| 70-75 | Decisión: ¿docking o pivotar? | — |
| 75-90 | Si docking: setup Vina-GPU. Si pivotar: PubMed TLR4/FM | terminal + web_search |

---

*Plan generado por DAVI. Aprobación de Cristóbal requerida antes de ejecutar.*
