================================================================================
  PROTEIN-LAB — ESTADO DE INVESTIGACIONES
  Generado: 2026-06-22 (sesion actual)
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

  Carpeta: investigacion-fibromialgia/fep/
  Experim design: FEP_EXPERIMENT_DESIGN.md
  Launch guide:   FEP_LAUNCH_GUIDE.md

  Estado: DISENADO, NO EJECUTADO

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

  Sub-lineas:
  A) Docking molecular                                        COMPLETO
  B) DFT de slab periodico (GPAW)                             COMPLETO
  C) Dinamica Molecular 10ns (OpenMM/MtrF/UndA)              COMPLETO
  D) Umbrella Sampling + WHAM (PMF)                           COMPLETO
  E) Transferencia electronica QM/MM (Marcus/Landau-Zener)    COMPLETO
  F) Estabilidad termica CI-NEB + Langevin                    COMPLETO
  G) Red hopping redox + Ecuaciones Maestras                  COMPLETO
  H) Integracion para CRO                                     COMPLETO

  Referencia: bitacora_fase2_real.md = FINALIZADO Y CONVALIDADO
               bitacora_fase2_ejecucion.md = CRO DOSSIER COMPLETO

  TRL estimado: 3-4
  Firmado por: Antigravity (sistema de validacion adversaria)

  Resultados clave:
  - DFT: Re-N4C2 promovida por W, dG_H* = -0.5122 eV (ideal ~0 eV)
  - MD: MtrF retiene perrhenato por puente salino ARG319 (96.2%)
  - Umbrella: DeltaG_bind = -10.57 kcal/mol (convergencia OK)
  - Marcus/LZ: k_ET = 6.43e9 s-1 (regime adiabativo)
  - CI-NEB: barrera 2.25 eV (sitio estable hasta 600K)
  - Master equations: I_steady = 9.85e3 e-/s

  PENDIENTE: Ninguno tecnico. Linea completa ejecutada. Listo para
  redaccion de paper o escalamiento experimental.


6) HIRONDELLEA GIGAS — BARORRESISTENCIA GH7
================================================================================

  Fase 1 — MSA / Conservacion                              COMPLETO
  Fase 2 — Estructura (AlphaFold DB)                       COMPLETO
  Fase 3 — Analisis estructural comparativo                 COMPLETO
  Fase 4 — Diseno y preparacion de sistemas MD              COMPLETO

  Estado MD 100ns (Kaggle, entrega segun EXPERIMENT_HANDOFF.md):
    WT 0.1 MPa (control)   : RUNNING  (v2, precision: falta subir PDB)
    WT 100 MPa (hadal)     : RUNNING  (v2, precision: falta subir PDB)
    MUT 0.1 MPa (control)  : PENDIENTE (no lanzado)
    MUT 100 MPa (hadal)    : PENDIENTE (no lanzado)

  Pendiente inmediato en Kaggle:
  [ ] Subir wt_solvated.pdb a kernels WT (accion manual en navegador)
  [ ] Cuando WT termine: lanzar kernels MUT
  [ ] Analisis post-MD (scripts/10_analisis_final.py)

  PENDING_TRACKER: Ultima actualizacion 2026-06-08 (desactualizado)

  BLOQUEO: Cuota Kaggle 30h/week (2 WT actuales ~60h). Lote 2 MUT
  planificado para la semana siguiente.

  Paper borrador: outline_paper.md existe (Fase 4 del plan)


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


================================================================================
  RESUMEN EJECUTIVO
================================================================================

  INVESTIGACION                          ESTADO              SIGUIENTE PASO
  ─────────────────────────────────────  ──────────────────  ———————————————
  1. FM Preprint v2.2 (eQTLs)            COMPLETO            Subir bioRxiv
  2. FM FEP/MM-PBSA D2/D3               DISENADO, NO EJEC   Crear scripts
  3. FM Ferritin biomaterial            EXPLORATORIO        Definir hipotesis
  4. FM Hemoglobina MTR                 EXPLORATORIO        Definir hipotesis
  5. Re SAC (CRO dossier)               COMPLETO            Redactar paper
  6. H. gigas GH7 baroresistencia MD    EN EJEC (Kaggle)    Subir PDB, lanzar MUT
  7. H. gigas Sistema Aluminio          Fase 1-2 done, 3 p  BLAST genoma 2025
  8. H. gigas Proteoma presion          Fase 3 done         AlphaFold Colab
  9. H. gigas Catalogo                  PROGRESO (15+)      Fase 4 estructural
  10. CASP17                            SCRIPTS, NO CORRID  Registrar + plegar
  11. Automated Lab v2                  OPERATIVO           Definir campana

  LINEAS ACTIVAS CON TRABAJO PENDIENTE: 4 (FEP, GH7-MD, Al-blast, AF-Colab)
  LINEAS COMPLETAS (paper/redaccion):   2 (FM preprint, Re SAC CRO)
  LINEAS EXPLORATORIAS (sin trabajo):   2 (ferritina, hemoglobina)
================================================================================
