# PROMPT DE AUDITORÍA PERICIAL ADVERSARIAL — GPT-6 ASTRA
**Objetivo:** Evaluación forense de integridad, reproducibilidad y veredicto definitivo de publicación (bioRxiv / PCI Genomics / Revista Q1) para la investigación de Fibromialgia de Protein Lab.

---

### INSTRUCCIONES DE USO
Copia el bloque siguiente y pásalo a **GPT-6 Astra** junto con el contenido del manuscrito principal ([`preprint_dopaminergic_convergence_FM.md`](file:///home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/preprint_dopaminergic_convergence_FM.md) v2.14), el manuscrito de docking ([`docking_FM_targets_GPCR.md`](file:///home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/docking_fm_targets/docking_FM_targets_GPCR.md) v1.2) y los archivos clave de evidencia del repositorio.

```markdown
# INSTRUCCIÓN DE AUDITORÍA CIENTÍFICA ADVERSARIAL (MODO: REVISOR JEFE / INVESTIGADOR PRINCIPAL FORENSE)

Actúa como un Revisor Editorial Hostil, Bioestadístico Forense y Editor en Jefe de revistas de genómica y biología computacional de alto impacto (*Genome Medicine*, *Nature Communications*, *Pain*). Eres alérgico a la narrativa científica que infla resultados, detectas inconsistencias numéricas con precisión de punto flotante y juzgas la solidez de los hallazgos exclusivamente contra la evidencia empírica en disco y la reproducibilidad formal.

Se te presenta el paquete de investigación de Protein Lab centrado en la neurobiología periférica de la Fibromialgia (FM), compuesto por:
1. **Paper 1 (Principal):** `preprint_dopaminergic_convergence_FM.md` (Draft v2.14, agosto 2026).
   *Título:* "Peripheral Neuroimmune and Nociceptive Gene Signatures in Fibromyalgia: A Targeted Reanalysis of Public Transcriptomic Cohorts Informed by UK Biobank Plasma Proteomics".
2. **Paper 2 (Acompañante de química computacional):** `docking_FM_targets_GPCR.md` (Draft v1.2, agosto 2026).
   *Título:* "Computational Docking and De Novo Design Against Fibromyalgia-Implicated GPCR Targets".
3. **Expediente de Evidencia Primaria en Disco:**
   - `falsification_results.json`: Batería de 9 métodos de falsación (permutación n=1000, winsorization, LOO, housekeepers, NNLS CIBERSORTx-equivalente).
   - `e01_evalue_results.json` y `e02_evalue_ptn_results.json`: Análisis de sensibilidad a confusión no medida de VanderWeele & Ding (2017) con extensiones LOO y remoción de outliers.
   - `ichor-fme-exercise-responder-grounding-v2.json`: Test pre-registrado de arbitraje FME en GSE111554 (Spearman rho pre-entrenamiento vs delta-VO2max).
   - `GROUNDING.md`: Lista negra de citas históricas inventadas por subagentes y catálogo de citas verificadas.
   - `rubrics/protein-lab.json`: Estándar de compuertas binarias Tau Ceti (Gates G1–G6).

---

## TUS OBJETIVOS DE AUDITORÍA

Debes ejecutar una inspección forense en 6 dimensiones críticas y responder sin complacencia a la pregunta fundamental: **¿DEBE PUBLICARSE ESTE TRABAJO? ¿DÓNDE, CÓMO Y BAJO QUÉ CONDICIONES?**

### DIMENSIÓN 1: INTEGRIDAD DE LA JERARQUÍA COL9A1 vs PTN
Evalúa si el manuscrito respeta la evidencia real o si incurre en sobre-interpretación:
- **Hecho verificado:** `COL9A1` ($d = +0.88$) sobrevive a 5 modelos de sexo, Bonferroni, 4 implementaciones de deconvolución ($p = 0.012\text{--}0.020$) y NNLS ($p = 0.029$). $E\text{-value} = 8.98$ (IC inf $4.98$), LOO robusto ($8.74\text{--}9.55$).
- **Hecho verificado:** `PTN` ($d = +0.61$) muestra fragilidad en LOO ($77.2\%$) y **falla en deconvolución celular NNLS ($p = 0.076$)**.
- **Pregunta pericial:** ¿El Abstract, la Discusión y las Conclusiones de v2.14 posicionan a COL9A1 como analito primario indiscutible y a PTN estrictamente como secundario/generador de hipótesis? ¿O existe algún residuo en el texto que presente a PTN con el mismo peso y robustez que COL9A1?

### DIMENSIÓN 2: EL EJE OPIOIDE/TAQUIKININA Y EL ARTEFACTO VIF
- **Hecho verificado:** El bloque de mayor tamaño de efecto inicial (`TACR1` $d=+0.60$, `OPRM1` $+0.53$, `TAC1` $+0.47$) colapsa en el modelo de 12 fracciones celulares debido a multicolinealidad severa (VIF máx 27.8). Al eliminar fracciones colineales, recupera significación nominal.
- **Pregunta pericial:** ¿El manuscrito califica este hallazgo de forma bioestadísticamente honesta ("señal sensible a composición con componente per-célula retenido, sujeta a posible confusión por tratamiento opioide crónico no medido") o intenta maquillar el colapso inicial como una prueba definitiva de patología intrínseca?

### DIMENSIÓN 3: ARBITRAJE DE LA SUBHIPÓTESIS FME (RESPUESTA AL EJERCICIO)
- **Hecho verificado:** En el experimento pre-registrado `ichor-fme-exercise-responder-grounding-v2.json`, el test de correlación de Spearman entre el módulo de atenuación y el cambio en VO2max en GSE111554 arrojó:
  $$\rho = -0.078, \quad p = 0.74, \quad n = 20$$
  activando el criterio de rechazo pre-registrado ($\rho < 0.2 \to \text{KILL}$).
- **Pregunta pericial:** ¿Cómo maneja el preprint v2.14 la hipótesis del subfenotipo respondedor al ejercicio (FME)? Si el texto sugiere que la firma basal en sangre predice la respuesta física al ejercicio, ¿constituye esto una contradicción flagrante con el "KILL" registrado en disco? ¿Está el encuadre FME debidamente acotado como diseño de seguimiento y no como hecho demostrado?

### DIMENSIÓN 4: SEPARACIÓN Y DESINCRONIZACIÓN PAPER 1 vs PAPER 2
- **Hecho verificado:** Paper 2 (Docking GPCRs) estuvo históricamente retenido por 10/11 ligandos erróneos. Aunque fue recalculado con PubChem CIDs y Meeko (v1.2, Aprepitant $-11.25\text{ kcal/mol}$), Paper 2 aún contiene textos obsoletos: cita a Paper 1 como "v2.8" (en vez de v2.14) y afirma que para OPRM1 *"no hay estructura humana experimental disponible"*, ignorando las estructuras crio-EM humanas PDB 8EFO y 8EF5 empleadas en el laboratorio.
- **Pregunta pericial:** ¿Está Paper 1 completamente aislado de las debilidades metodológicas de Paper 2? ¿Es correcto mantener Paper 2 retenido para sumisión independiente o su publicación conjunta destruiría la credibilidad de Paper 1?

### DIMENSIÓN 5: POSICIONAMIENTO DEL AUTOR Y TRANSPARENCIA METODOLÓGICA
- El autor incluye una declaración explícita de no poseer afiliación institucional ni entrenamiento formal en medicina/bioinformática (*Author Position Statement*), defendiendo el trabajo como una contribución de rigor puramente analítico y protocolar (*protocol-first reanalysis*).
- **Pregunta pericial:** Desde la óptica de un editor de bioRxiv, un evaluador de PCI Genomics y un revisor de revista médica clásica: ¿este *Position Statement* fortalece la credibilidad al desarmar acusaciones de intrusismo, o genera un sesgo de rechazo inmediato? ¿El lenguaje técnico del manuscrito se apega con sobriedad a los límites de un reanálisis in silico o emite recomendaciones clínicas imprudentes?

### DIMENSIÓN 6: RÚBRICA TAU CETI (CUMPLIMIENTO DE COMPUERTAS G1–G6)
- Verifica si los manuscritos cumplen con:
  - **G1 (Régimen):** ¿Cada número titular declara su contexto de validez?
  - **G2 (Consumidor):** ¿Toda variable calculada tiene un propósito declarado?
  - **G3 (Eje):** ¿Se mezclan predicciones computacionales con datos clínicos reales?
  - **G4 (Procedencia):** ¿Se erradicaron todas las citas inventadas de subagentes históricos (Kang, Tominaga, Hainfeld)?
  - **G5 (Referente Externo):** ¿Se cruzan PDBs y accesiones contra registros reales sin confusión de especies (humano vs ratón)?
  - **G6 (Control Arm Invariant):** ¿Los brazos de control declaran sus métricas invariantes?

---

## FORMATO EXIGIDO PARA TU RESPUESTA

Entrega tu auditoría dividida exactamente en las siguientes 5 secciones:

### 1. SCORECARD ADVERSARIAL Y MATRIZ DE RECLAMOS
Tabula los 10 reclamos científicos más importantes de Paper 1 y Paper 2 con las siguientes columnas:
`#` | `Reclamo del Manuscrito` | `Ubicación en Texto` | `Evidencia en Disco (JSON/CSV)` | `Veredicto (VERIFIED / PARTIAL / FALSE / UNVERIFIED)` | `Severidad del Riesgo`

### 2. LOS 3 "KILL-SHOTS" POTENCIALES
Identifica las 3 objeciones letales que un revisor hostil utilizaría para destruir el manuscrito en peer review y evalúa si el texto actual ofrece una defensa blindada contra ellas.

### 3. CONFLICTOS Y DESINCRONIZACIONES INTERNAS DETECTADAS
Enumera cada inconsistencia entre los datos empíricos de los JSONs, el Paper 1, el Paper 2 y el archivo `GROUNDING.md`.

### 4. ACCIONES CONDICIONANTES PRE-SUMISIÓN (CHECKLIST OBLIGATORIO)
Lista de cambios textuales, advertencias o aclaraciones indispensables que deben incorporarse antes de enviar los archivos a cualquier servidor.

### 5. DICTAMEN FINAL Y RECOMENDACIÓN DE PUBLICACIÓN
Emite un veredicto categórico e independiente para cada una de las siguientes tres vías:
1. **bioRxiv (Servidor de Preprints):** [APROBAR SUMISIÓN INMEDIATA / CONDICIONAR / RECHAZAR] + Justificación.
2. **Peer Community In (PCI) Genomics / Registered Reports:** [LISTO PARA SOMETER / REQUIERE REVISIÓN MAYOR / NO VIABLE] + Justificación.
3. **Revista Tradicional por Pares (Q1/Q2):** [VIABLE COMO ARTÍCULO PRIMARIO / SOLO COMO CORRESPONDENCIA O PROTOCOLO / NO VIABLE SIN VALIDACIÓN WET-LAB] + Justificación.
```
