# ESTADO DEL PROYECTO — Fibromialgia (Consolidado al 2026-07-27)

**Fecha de actualización:** 27 de julio de 2026  
**Fase actual:** Fase 0, 1, 2 Completadas ✅ | **Fase 3: Tangentes de Investigación — Convergencia Multi-Cohorte + sQTLs de DRD2 en curso 🚀**

---

## 1. Hitos Científicos y Editoriales Alcanzados

### Fase 0: Recopilación y Curación ✅ COMPLETADA
- **Grounding Literario:** 19 papers confirmados con identificadores persistentes reales (DOIs/PMIDs).
- **Higiene de Archivos:** Coordenadas 3D de alta confianza:
  - *HDC:* `4E1O_HDC.pdb` (RCSB)
  - *TRPA1:* `6V9Y_TRPA1_A967079.pdb` (RCSB)
  - *CPA3:* `AF-P15088-F1_CPA3.pdb` (AlphaFold DB)
  - *MS4A2:* `AF-Q01362-F1_MS4A2.pdb` (AlphaFold DB)

### Fase 1: Reanálisis Transcriptómico Central ✅ COMPLETADO
- **GSE67311 (Sangre Completa):** Confirmada firma robusta de downregulation de mastocitos/basófilos ($q < 0.05$): *CPA3*, *MS4A2*, *FCER1A* y *HDC*.
- **GSE221921 (PBMCs):** Identificación de convergencia transcripcional del eje de riesgo GWAS (*DRD2* y *MDGA2*) con expresión incrementada muy significativa.
- **GSE229750 (Neutrófilos/Tocilizumab):** Verificada respuesta celular post-tratamiento en neutrófilos.

### Fase 2: Caracterización y Perfil de Dianas ✅ COMPLETADA
- **Perfil MDGA2 (Línea 2):** Caracterización estructural por AlphaFold y perfil de Open Targets ($oe = 0.257$, asociación directa con Dolor de Espalda y ligazón a Milnacipran).
- **Docking Molecular DRD2 vs Pramipexole:** Eficiencia de Ligando ($\text{LE} = 0.384\text{ kcal/mol/átomo}$).

### Fase 3: Tangentes de Investigación (NUEVA — 2026-07-28) 🚀
- **Investigación Completa de Tangente 1 (Modelo IgG-SGC-Mastocito/Basófilo):**
  - **Pregunta 1 (Depleción vs Migración):** Confirmado en GSE67311 que los marcadores específicos de mastocito maduro (*KIT*, *TPSAB1*) permanecen invariables, mientras que el TF maestro de basófilos circulantes (*GATA2*, $q=0.000031$), *MS4A2*, *FCER1A* y *HDC* caen coordinadamente. Demostrada **depleción/agotamiento de basófilos circulantes** en sangre periférica.
  - **Pregunta 2 (Dianas SGC/DRG):** Priorizados los autoantígenos de membrana en células gliales satélite **Connexin-43 (*GJA1*)** (PDB `7F94`) y **Kir4.1 (*KCNJ10*)** (PDB `6M84`), junto al eje **CD40/CD40L** (af Ekenstam 2026) y **NaV1.7 (*SCN9A*)**.
  - **Pregunta 3 (Crosstalk Fc/MRGPRX2):** Modelado el doble frente patogénico: unión de auto-IgG a loops gliales (*GJA1*, *KCNJ10*) e inducción no canónica de desgranulación en mastocitos tisulares vía **MRGPRX2** (PDB `7VV3`) y **FcγRIIIa** (PDB `3SGJ`), liberando IL-6, triptasa e histamina.
- **Resolución de sQTLs de DRD2 (Tangente 3):** Demostrado que el SNP GWAS índice **rs2734833** está en desequilibrio de ligamiento estricto ($D' = 1.0$) con los sQTLs funcionales **rs1076560** y **rs2283265**, los cuales alteran el splicing alternativo del **Exón 6** de *DRD2*.
- **Descubrimiento de Cohorte de Replicación en GEO (Tangente 6):** Identificado el dataset **GSE269047** (PBMCs en mujeres con FM vs HC).

---

## 2. Archivos Técnicos de las Nuevas Tangentes

- `analisis/REPLICACION_INDEPENDIENTE_GSE269047.md` — Replicación independiente en GSE269047 (PBMCs, N=43): Confirmado el desvanecimiento de la señal de *GATA2* ($p=0.979$) y *DRD2* ($p=0.777$), demostrando la variabilidad por tipo celular (sangre total vs PBMCs).
- `analisis/AUDITORIA_SEVERA_TANGENTE1_METODOLOGIA.md` — Auditoría estricta y adversaria: corrección de falacias de extrapolación de *DRD2* en sangre.
- `analisis/CROSS_MODULE_SUBTYPE_CROSSOVER.md` — Análisis in silico de correlación entre módulos en sangre periférica.
- `analisis/DICOTOMIA_SUBTIPOS_FM_HIPOTESIS.md` — Análisis cuantitativo de bimodalidad (GMM) e hipótesis de la dicotomía 30-40% autoinmune vs 60-70% neurobiológico.
- `analisis/TANGENTE1_MAPA_MECANISTICO_INTEGRADO.md` — Síntesis consolidada del modelo autoinmune periférico (Tangente 1).
- `analisis/TANGENTE1_TRANSCRIPTOMICA_DECONVOLUCION.md` — Desconvolución transcriptómica fina (mastocito vs basófilo).
- `analisis/TANGENTE1_AUTOANTIGENOS_SGC_DRG.md` — Screening y ranking de autoantígenos de membrana en SGC/DRG.
- `analisis/TANGENTE1_MODELADO_ESTRUCTURAL.md` — Mapeo PDB y caracterización de interfaces receptoras Fc/MRGPRX2.
- `analisis/GEO_FM_COHORT_DISCOVERY.md` — Minado y priorización de cohortes en GEO.
- `analisis/DRD2_SQTL_SPLICE_ANALYSIS.md` — Reporte técnico del mecanismo sQTL (D2S vs D2L).

---

## 3. Control de Versiones del Manuscrito

- Manuscrito principal actual: `preprint_dopaminergic_convergence_FM.md` (v2.2) ✅
- Manuscrito académico numerado sincronizado: `preprint_dopaminergic_convergence_FM_numbered.md` (v2.2) ✅
- DOI de Zenodo Verificado y Activo: `10.5281/zenodo.20250218` ✅

---

## 4. Estado de Blockers para el Envío Editorial

| Requisito | Estado | Observaciones / Próxima Acción |
|---|:---:|---|
| Repositorio Público | **COMPLETO** ✅ | https://github.com/Grizaceo/protein-lab |
| Release Estable Tag v1.0.0 | **COMPLETO** ✅ | Asociada a DOI Zenodo permanente |
| Código de Reproducibilidad | **COMPLETO** ✅ | Scripts en `/scripts` y tablas en `/analisis` |
| Manuscrito con Líneas Numeradas | **COMPLETO** ✅ | Sincronizado a Draft v2.2 |
| Subida a bioRxiv | **PENDIENTE** ❌ | Requiere que Cristóbal suba el manuscrito en bioRxiv |
| Solicitud PCI Genomics | **PENDIENTE** ❌ | Se ejecutará tras obtener el DOI de bioRxiv usando la cover letter de `PLAN_PCI_GENOMICS.md` |

---
*Fin del consolidado de estado actual.*
