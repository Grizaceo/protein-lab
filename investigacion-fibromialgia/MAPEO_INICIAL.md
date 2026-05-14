# MAPEO INICIAL — Investigación Fibromialgia
## Protein Lab → Fibromalia: Estado del Arte y Rutas de Ataque

**Fecha:** 2026-05-13
**Versión:** 0.1 (borrador vivo — se actualiza continuamente)

---

## 1. ¿QUÉ SABEMOS DE LA FIBROMIALGIA? (Estado del Arte)

### 1.1 El paradigma está cambiando (2021-2025)

La FM ya NO es solo "dolor central sin causa conocida". Hay 4 líneas de evidencia que la redefinen:

**A) Hipótesis autoinmune (Goebel et al., 2021-2025)**
- IgG autoanticuerpos de pacientes FM se unen a ganglios de raíz dorsal (DRG) en ratones → inducen dolor
- Anti-satellite glia cell IgG correlaciona con severidad (Krock et al., PMC10348624)
- Subconjunto de pacientes FM tiene perfil autoinmune claro
- **Implicación:** Si es autoinmune, se puede atacar con terapias inmunomoduladoras o eliminación de autoanticuerpos

**B) Small Fiber Neuropathy (SFN) — ~50% de pacientes**
- ~50% de mujeres FM tienen reducción de inervación cutánea (PAIN Reports 2025)
- Pérdida de fibras Aδ y C en biopsia de piel
- **Implicación:** No es solo central — hay componente periférico medible y potencialmente tratable

**C) Estrés oxidativo + disfunción mitocondrial**
- Marcadores elevados: MDA, 4-HNE (peroxidación lipídica)
- Defensas antioxidantes reducidas: CoQ10, SOD, catalasa
- Actividad NRF2 comprometida (PMC12106312)
- **Implicación:** Terapias redox (NRF2 activadores, CoQ10, tiamina) tienen base mecanística

**D) Disbiosis intestinal → dolor (Cell/Neuron 2025)**
- Trasplante de microbiota de pacientes FM a ratones → induce dolor
- Trasplante de microbiota sana → alivia dolor (estudio abierto en humanos)
- **Implicación:** Eje intestino-cerebro como modulador del dolor FM

### 1.2 Biomarcadores emergentes

| Tipo | Biomarcador | Fuente | Estado |
|------|-------------|--------|--------|
| Genético | DYRK3, RGS17, ARHGEF37 | Frontiers Genetics 2025 (PMID 40313599) | AUC 0.83 diagnóstico |
| Proteico | Panel multi-proteína (Olink) | PMC12841610 | Exploratorio, sin validación clínica |
| Autoanticuerpos | Anti-satellite glia cell IgG | Brain Behav Immun 2023 (PMID 37683961) | Correlación con severidad |
| Neuroimagen | EEG gamma band connectivity | Frontiers Pain Res 2026 (PMID 41625159) | 99.57% accuracy (463 participantes) |
| Metabólico | Perfil redox (MDA, 4-HNE, CoQ10) | Frontiers Pain Res 2025 (PMC12106312) | Consistente pero no específico |
| Neuropático | Densidad de fibras intraepidérmicas | PAIN Reports 2025 | ~50% pacientes anormal |
| Inflamatorio | IL-1, IL-6, IL-8 | Cells 2024 (PMID 39451237) | Correla con dolor y discapacidad |
| Genómico | HERV fingerprints | PMC12061480 2025 | FM vs ME/CFS diferenciable |

### 1.3 Tratamientos actuales y en desarrollo

**FDA-approved (actual):**
- Duloxetina (SNRI) — beneficio ~30% pacientes
- Milnacipran (SNRI) — similar
- Pregabalin (antiepiléptico) — beneficio ~30% pacientes

**2025 — Nuevo:**
- **Tonmya (TNX-102 SL)** — ciclobenzaprina sublingual, FDA Fast Track, aprobado agosto 2025. Target: sueño no restaurador
- **Suzetrigine** — inhibidor selectivo Nav1.8, FDA aprobado enero 2025 para dolor agudo (no FM específico pero relevante)

**En investigación activa:**
- Low-dose naltrexone (LDN) — múltiples estudios pequeños
- Cannabinoids — 82% pacientes reportan mejoría (encuesta)
- Psilocybin — estudio protocolizado (Front Psychiatry 2024)
- NRF2 activadores, CoQ10, tiamina, H2 molecular
- Estimulación magnética transcraneal repetitiva (rTMS)
- Vagus nerve stimulation

---

## 2. CRUCES CON MACHINE LEARNING / AI

### 2.1 ML para diagnóstico

| Estudio | Método | Data | Resultado |
|---------|--------|------|-----------|
| Frontiers Pain 2025 | ML + EEG connectivity | 48 participantes | 99.57% accuracy (gamma band) |
| PMC12863579 | ML + rs-fMRI + DTI | OpenNeuro database | Clasificación binaria FM vs control |
| Frontiers Genetics 2025 | ML + gene expression (GEO) | Microarrays | 3 genes, AUC 0.83 |
| PMC11227885 | LLM + análisis de texto | Clinical notes | Detección de patrones sutiles |

### 2.2 Multi-omics + ML (estado del campo)

- **BioMapAI** (bioRxiv 2024): Multi-omics longitudinal en 153 ME/CFS + 96 controles. Framework aplicable a FM.
- **ML + multi-omics en ME/CFS** (Huang et al., 2024, Springer): Review de cómo integrar genómica, transcriptómica, proteómica, metabolómica. Directamente transferible a FM.
- No se encontró un paper específico de "multi-omics + ML para FM" publicado — esto es un GAP y una oportunidad.

### 2.3 Lo que NO se ha hecho (gaps = oportunidades)

1. **Proteómica + ESM2 embeddings para FM** — Nadie ha usado protein language models para analizar las proteínas diferencialmente expresadas en FM
2. **Geometría tropical aplicada a biomarcadores de FM** — Nuestro framework es original aquí
3. **Diseño de proteínas terapéuticas para dianas de FM** — Nadie está diseñando binders para los autoanticuerpos o canales iónicos relevantes en FM
4. **Integración multi-omics + estructura proteica + ML** — No existe pipeline que vaya de datos ómicos → estructura → diseño de fármacos/proteínas

---

## 3. RUTAS DE ATAQUE PARA EL LAB

### Ruta A: "Mapa de dianas terapéuticas basado en estructura"
**Objetivo:** Identificar y priorizar targets proteicos en FM usando datos ómicos + estructura

Pasos:
1. Recopilar datasets de proteómica/transcriptómica FM de GEO
2. Identificar proteínas diferencialmente expresadas (DEPs)
3. Mapear DEPs a estructuras PDB (o predichas por AlphaFold)
4. Calcular embeddings ESM2 para DEPs vs wild-type
5. Usar geometría tropical para caracterizar pockets de binding
6. Priorizar targets "druggables" con mejor score compuesto

**Ventaja:** Usa directamente las herramientas del lab (ESM2, tropical metrics, estructura)
**Poder de cómputo:** Local (RTX 4060) suficiente para ESM2 650M

### Ruta B: "Diseño de proteínas anti-autoanticuerpos"
**Objetivo:** Diseñar proteínas que bloqueen los autoanticuerpos IgG de FM

Pasos:
1. Identificar epítopos de unión de anti-DRG IgG
2. Diseñar proteínas decoy que compitan por unión
3. Usar RFdiffusion + AlphaFold para diseño y validación
4. Caracterizar con geometría tropical

**Ventaja:** Aplicación directa del pipeline de binder design del lab
**Poder de cómputo:** Necesita Colab/Kaggle (RFdiffusion)

### Ruta C: "Clasificador multi-omics con estructura proteica"
**Objetivo:** Integrar datos multi-omics con features de estructura proteica para diagnóstico

Pasos:
1. Recopilar datos multi-omics de FM (GEO, proteomics DBs)
2. Generar features: embeddings ESM2, tropical metrics, pLDDT, etc.
3. Entrenar clasificador (XGBoost, MLP, etc.)
4. Validar en datasets independientes
5. Interpretar features importantes → nuevos biomarcadores

**Ventaja:** ML + biología estructural = enfoque original
**Poder de cómputo:** Local + Kaggle

### Ruta D: "Cribado virtual de compuestos para targets de FM"
**Objetivo:** Usar docking + geometría tropical para buscar moduladores de targets FM

Pasos:
1. Seleccionar targets (Nav1.8, TRPA1, NRF2, etc.)
2. Obtener estructuras (PDB o AlphaFold)
3. Cribado virtual con geometría tropical
4. Validar top hits con MD o ensayos in silico

**Ventaja:** Puede identificar candidatos a fármacos rápidamente
**Poder de cómputo:** Local + Modal/Kaggle

---

## 4. DATASETS Y RECURSOS DISPONIBLES

### Datos ómicos
- **GEO (NCBI):** Múltiples datasets de expresión génica FM (buscar "fibromyalgia" → ~50+ datasets)
- **OpenNeuro:** rs-fMRI + DTI datos de FM
- **Olink:** Paneles proteómicos inflamatorios (referenciados en literatura)
- **ProteomicsDB:** Datos proteómicos humanos

### Estructuras proteicas relevantes
- **Nav1.8 (SCN10A):** PDB 6J8E, 6JJ6 — canal de sodio clave en dolor
- **TRPA1:** PDB 3J9P — receptor de dolor
- **NRF2 (NFE2L2):** Múltiples estructuras — factor de transcripción antioxidante
- **IgG Fc region:** PDB 1H3X — para diseño de decoys

### Herramientas disponibles
- **Local (RTX 4060):** ESM2 (8M-650M), BioPython, análisis estructural, ML
- **Colab:** RFdiffusion, AlphaFold, ColabFold
- **Kaggle:** GPU gratuita para entrenamiento ML
- **Modal:** GPU cloud para computación intensiva

---

## 5. PLAN DE FASES SUGERIDO

### Fase 0: Recopilación (AHORA)
- [ ] Descargar papers clave y guardar en literatura/
- [ ] Descargar datasets GEO relevantes
- [ ] Mapear estructuras PDB de targets prioritarios
- [ ] Crear lista curada de DEPs (proteínas diferencialmente expresadas)

### Fase 1: Análisis in silico local
- [ ] Generar embeddings ESM2 de proteínas FM-relevantes
- [ ] Calcular métricas tropicales de pockets de binding
- [ ] Análisis de redes de interacción proteína-proteína
- [ ] Priorización de targets

### Fase 2: ML + Multi-omics
- [ ] Integrar datos multi-omics
- [ ] Entrenar clasificador FM vs control
- [ ] Interpretar features → nuevos biomarcadores
- [ ] Publicar resultados preliminares

### Fase 3: Diseño de proteínas (Colab/Kaggle)
- [ ] Diseñar binders para targets prioritarios
- [ ] Validar con AlphaFold
- [ ] Caracterizar con geometría tropical

### Fase 4: Validación y publicación
- [ ] Escribir paper
- [ ] Preprint en bioRxiv
- [ ] Submit a journal

---

## 6. NOTAS Y DECISIONES PENDIENTES

- **Decidir:** ¿Cuál ruta atacar primero? (Recomendación: Ruta A → C → B → D)
- **Decidir:** ¿Enfocarse en subtipo autoinmune o FM general?
- **Decidir:** ¿Colaborar con algún grupo clínico para validación?

---

*Este documento es un borrador vivo. Se actualiza a medida que se encuentra nueva literatura y se toman decisiones.*
