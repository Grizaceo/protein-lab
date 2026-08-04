================================================================================
  PROTEIN-LAB — ESTADO DE INVESTIGACIONES
  Generado: 2026-06-22 | Actualizado: 2026-07-04 (auditoria + binder_design)
================================================================================

Este documento resume el estado real de cada linea de investigacion en
protein-lab, basado en los archivos de estado, bitacoras, planillas y
evidencia en disco.


1) FIBROMIALGIA — DOPAMINERGIC CONVERGENCE (FM)
================================================================================

  Carpeta: investigacion-fibromialgia/
  Tienes preprint: preprint_dopaminergic_convergence_FM.md (v2.2, numerado)

  FASE 1 — eQTLs / GTEx / Regulacion Genetica            COMPLETO
  FASE 2 — Replicacion externa (GSE274134, ME/CFS, GTEx) COMPLETO
  FASE 3 — Manuscrito preprint v2.2                       COMPLETO
  FASE 4 — Docking integracion                            COMPLETO
  FASE 5 — AlphaFold + Open Targets (MDGA2)               COMPLETO

  Sub-componentes:
  +-- GSE274134 (replicacion pre/post MT)         COMPLETO -> Indetectable
  +-- ME/CFS scRNA-seq (especificidad)             COMPLETO -> Indetectable
  +-- GTEx v8 (basal PBMCs)                        COMPLETO -> TPM=0 sangre
  +-- eQTL rs36030569 -> MDGA2 (putamen, NAcc)     COMPLETO
  +-- eQTL rs12420205 -> DRD2 (medula C-1)         COMPLETO
  +-- QTL rs2734833 (FM GWAS) -> no eQTL basal      COMPLETO

  PENDIENTE:
  - Estrategia 4: Transcriptomica espacial musculo FM (datos no disponibles
    en GEO, monitorear)
  - Subida de preprint v2.2 a bioRxiv
  - Envio a PCI Genomics

  BLOQUEO PARA CORREO: Ninguno tecnico. Solo subir bioRxiv -> PCI Genomics.


2) FIBROMIALGIA — FEP/MM-PBSA (D2 vs D3 SELECTIVITY)
================================================================================

  Carpeta: investigacion-fibromialgia/fep/  *** NO EXISTE EN DISCO ***
  Experim design: FEP_EXPERIMENT_DESIGN.md (referenciado, no verificado)
  Launch guide:   FEP_LAUNCH_GUIDE.md (referenciado, no verificado)

  Estado: DISENADO EN DOCS, CARPETA Y SCRIPTS AUSENTES (auditoria 2026-07-04)

  Candidatos listos (6 compuestos, Tier 1 y Tier 2):
    C1 (Transformer#1), C2 (Transformer#2), Denovo_Sel_3, Denovo_CNS_3,
    Comb_#1, Comb_#2

  Receptores listos:
    DRD2: 6VMS (activo, 2.9A), DRD3: 3PBL (activo, 2.9A)

  Scripts necesarios (05 scripts descritos, NO implementados aun):
    01_prepare_systems.py  |  02_run_md.py  |  03_setup_fep.py
    04_run_fep.py          |  05_analyze.py

  Plan hibrido: RTX 4060 (prep + MD) + Colab Pro A100 (FEP)
  Estimado: 5-6 semanas para pipeline completo

  BLOQUEO: Requiere creacion de scripts y lanzamiento de corridas.
  Prioridad sugerida: Alta si el objetivo es sintetizar candidatos.


3) FIBROMIALGIA — FERRITINA BIOMATERIAL
================================================================================

  Carpeta: investigaciones/ferritina-biomaterial/

  Estado: EXPLORATORIO / ESTRUCTURA CREADA

  Contenido en disco: datos/, docs/, scripts/ (vacio, sin scripts visibles)
  Sin README, sin PENDING_TRACKER, sin bitacora de ejecucion.

  Observacion: Carpeta creada pero sin evidencia de corridas ejecutadas
  o resultados documentados. Posible linea futura no iniciada.


4) FIBROMIALGIA — HEMOGLOBINA MTR
================================================================================

  Carpeta: investigaciones/hemoglobina-mtr/

  Estado: EXPLORATORIO / ESTRUCTURA CREADA

  Contenido en disco: data/, docs/, scripts/
  Sin README ni bitacora. Carpeta espejo de ferritina-biomaterial.

  Observacion: Misma situacion que ferritina-biomaterial. Linea no iniciada
  o en etapa muy temprana de setup.


5) MATERIALES AVANZADOS CHILE — CATALIZADORES RENIO (Re SAC)
================================================================================

  *** CORREGIDO POST-AUDITORIA 2026-07-04 ***

  Estado real en disco: EXPLORATORIO (phase4 parcial solamente)

  Evidencia verificable:
  +-- phase4 Vina docking: 42 poses PO4-proxy (scores ~-2 kcal/mol)
  +-- MD OpenMM: MtrF_HEC676, UndA_HEC904 (trajectories .dcd)
  +-- Umbrella raw traj: MtrF/UndA .dcd (sin WHAM/PMF output)

  NO verificado en disco (solo narrativa en docs/templates):
  - DFT/GPAW, Marcus/LZ, CI-NEB, master equations, CRO dossier
  - bitacora_fase2_real.md / bitacora_fase2_ejecucion.md (ausentes)
  - Ligandos ReO4/TcO4: archivos usan proxy PO4 (REMARK Name = PO4)
  - Claim ARG319 salt bridge: residuo 319 es ALA en estructura usada

  TRL real estimado: 1-2 (no 3-4)
  PENDIENTE: reconstruir computo honesto antes de paper/patente


6) HIRONDELLEA GIGAS — BARORRESISTENCIA GH7
================================================================================

  *** CORREGIDO POST-AUDITORIA 2026-07-04 ***

  Infraestructura: notebooks Kaggle + clean_8CEL.pdb (template fungico, no H. gigas)

  Trayectorias en disco (resultados/trayectorias/*.csv):
    WT control, WT hadal, MUT control, MUT hadal — TODAS EXISTEN
    Duracion real: ~7500 steps (~15 ps), NO 100 ns como documentado
    Analisis RMSD/RMSF: NO EJECUTADO (scripts/10_analisis_final.py ausente)
    outline_paper.md: NO EXISTE en disco

  PENDIENTE: completar MD real (100 ns), usar modelo H. gigas, analisis post-MD


7) HIRONDELLEA GIGAS — SISTEMA ALUMINIO / GLUCONATO
================================================================================

  Estado: Fase 1-2 COMPLETAS, Fase 3 pendiente

  Completado:
  - Genes pathway gluconato (GDH A0A6A7FTD1, GNK fragmento A0A6A7GCI1)
  - Homologos + ESM2 embeddings
  - aplicaciones/02_sistema_aluminio.md con FODA
  - vias/VIA_GLUCONATO_ALUMINIO.md

  Pendiente:
  - BLAST genoma 2025 para ORF completa gluconokinasa (Fase 3/4)


8) HIRONDELLEA GIGAS — PROTEOMA PRESION EXTREMA
================================================================================

  Estado: FASE 3 COMPUTACIONAL COMPLETA (catalogo + embeddings)

  Completado:
  - Catalogo 15 candidatos (analisis/proteoma/CANDIDATOS_FASE3.tsv)
  - Embeddings batch 14 secuencias (ESM2 650M)
  - Analisis por familia Hg vs ref (familia_hg_vs_ref.json)
  - aplicaciones/03_proteoma_presion_extrema.md

  Pendiente:
  - Fase 4: Estructura por AlphaFold (Colab) -> paquete listo en
    colab_alphafold/ (notebook + FASTA), esperando ejecucion en Colab
  - Metricas tropicales (baja prioridad, despues de tener confiable PDB)


9) HIRONDELLEA GIGAS — CATALOGO GENERAL
================================================================================

  Estado: EN PROGRESO (15+ entradas)

  Estructura: proteinas/CATALOGO.md
  Plan: PLAN_INVESTIGACION.md (actualizado 2026-06-01)

  Criterio de exito: >=10 entradas anotadas. Cumplido con margen.


10) CASP17 — PARTICIPACION
================================================================================

  Estado: SCRIPTS LISTOS, SIN CORRIDAS

  Completado:
  - fetch_targets.py (descarga y monitoreo de targets)
  - format_submission.py (PDB -> formato CASP TS)
  - README.md con flujo completo

  Pendiente:
  - Registro oficial CASP17 (codigo de registro XXXX-XXXX-XXXX)
  - Ejecucion de predicciones (ColabFold / AlphaFold local)
  - Envio de predicciones


11) AUTOMATED LAB — DTI NOCTURNO
================================================================================

  Estado: v2 OPERATIVO (ultima auditoria 2026-05-14)

  v2 arregla: IDs de experimento, max_experiments, resultados batch,
  KISS integration, resultados en .gitignore.

  Pendiente:
  - No hay evidencia de corridas nocturnas recientes.
  - Requiere definir proxima campaña.
  - Provider default: Ollama Cloud / Nemotron-3-super


12) BINDER DESIGN — COMPETENCIAS ADAPTYV (BindCraft)  *** LINEA ACTIVA ***
================================================================================

  Carpeta: binder_design/
  Estado: INFRAESTRUCTURA LISTA, VALIDACION COLAB PENDIENTE

  Completado (2026-07-04):
  +-- Pipeline BindCraft documentado (reemplaza RFdiffusion fallido)
  +-- Scripts: prepare_bindcraft_target, filter, process, monitor
  +-- Config Nipah G (2VSM), COLAB_INSTRUCTIONS, COMPETE_CHECKLIST
  +-- Baseline comparison vs ipTM 0.16 (11 corridas RFdiffusion)

  Competencia Proteinbase: TODAS CERRADAS (modo practicar-y-esperar)

  PENDIENTE:
  - Smoke test BindCraft en Colab (50 trayectorias)
  - Validar ipTM > 0.5 (criterio migracion pipeline)
  - Monitorear proxima competencia Adaptyv/GEM


================================================================================
  RESUMEN EJECUTIVO
================================================================================

  INVESTIGACION                          ESTADO              SIGUIENTE PASO
  ─────────────────────────────────────  ──────────────────  ———————————————
  12. Binder Design BindCraft (Nipah)    INFRA LISTA         Smoke test Colab
  1. FM Preprint v2.2 (eQTLs)            COMPLETO            Subir bioRxiv (opc.)
  2. FM FEP/MM-PBSA D2/D3               DOCS ONLY           Carpeta fep/ ausente
  3. FM Ferritin biomaterial            EXPLORATORIO        Definir hipotesis
  4. FM Hemoglobina MTR                 EXPLORATORIO        Definir hipotesis
  5. Re SAC (CRO dossier)               EXPLORATORIO        Reconstruir computo
  6. H. gigas GH7 baroresistencia MD    FRAGMENTOS ~15ps    MD 100ns + analisis
  7. H. gigas Sistema Aluminio          DOCS ONLY           BLAST genoma 2025
  8. H. gigas Proteoma presion          SKELETON            AlphaFold Colab
  9. H. gigas Catalogo                  DOCS ONLY           Fase 4 estructural
  10. CASP17                            SCRIPTS, NO CORRID  Registrar + plegar
  11. Automated Lab v2                  OPERATIVO           Definir campana

  LINEA ACTIVA PRINCIPAL: Binder Design (binder_design/)
  LINEAS CON EVIDENCIA REAL: FM preprint core tables, phase4 Re docking parcial
  LINEAS SOBRE-DECLARADAS CORREGIDAS: Re SAC, GH7 MD, FM FEP
================================================================================
