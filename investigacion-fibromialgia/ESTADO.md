# ESTADO DEL PROYECTO — Fibromialgia (Consolidado al 2026-05-29)

**Fecha de actualización:** 29 de mayo de 2026  
**Fase actual:** Fase 0, Fase 1 y Fase 2 Completadas ✅ | Preprint v2.2 listo para bioRxiv & PCI Genomics

---

## 1. Hitos Científicos y Editoriales Alcanzados

### Fase 0: Recopilación y Curación ✅ COMPLETADA
- **Grounding Literario:** 19 papers confirmados con identificadores persistentes reales (DOIs/PMIDs).
- **Higiene de Archivos:** Auditoría exhaustiva completada, rechazando 4 PDBs mal asignados e incorporando las coordenadas tridimensionales de alta confianza:
  - *HDC:* `4E1O_HDC.pdb` (RCSB)
  - *TRPA1:* `6V9Y_TRPA1_A967079.pdb` (RCSB)
  - *CPA3:* `AF-P15088-F1_CPA3.pdb` (AlphaFold DB)
  - *MS4A2:* `AF-Q01362-F1_MS4A2.pdb` (AlphaFold DB)

### Fase 1: Reanálisis Transcriptómico Central ✅ COMPLETADO
- **GSE67311 (Sangre Completa):** Confirmada firma robusta de downregulation de mastocitos/basófilos ($q < 0.05$): *CPA3*, *MS4A2*, *FCER1A* y *HDC*.
- **GSE221921 (PBMCs):** Identificación de convergencia transcripcional del eje de riesgo GWAS (*DRD2* y *MDGA2*) con expresión incrementada muy significativa.
- **GSE229750 (Neutrófilos/Tocilizumab):** Verificada respuesta celular post-tratamiento en neutrófilos, mostrando firmas restrictivas.

### Fase 2: Caracterización y Perfil de Dianas ✅ COMPLETADA
- **Perfil MDGA2 (Línea 2):** Caracterización estructural por AlphaFold (supradominio Ig-like rígido de 6 dominios + linker flexible + dominio MAM) y perfil de Open Targets ($oe = 0.257$, asociación directa con Dolor de Espalda y ligazón farmacogenómica a Milnacipran, diana soluble ideal para anticuerpos).
- **Docking Molecular DRD2 vs Pramipexole:** Superada la paradoja del Vina Score mediante análisis de **Eficiencia de Ligando (LE)**. Pramipexole exhibe $LE = 0.384$ kcal/mol/átomo (el doble que la Bromocriptina), justificando su afinidad nanomolar experimental (~3 nM).

---

## 2. Resoluciones de la Auditoría y Peer Review (v2.2)

Se ha promovido el preprint a la versión **Draft v2.2** resolviendo con rigor de revisor par los siguientes puntos metodológicos críticos:
1. **Colinealidad en Ajuste OLS:** Se documentó que el modelo OLS sex-adjusted de GSE221921 sufre de multicolinealidad extrema (FM es 95% femenino; controles 50%). Se establece que el **subgrupo de solo mujeres es el modelo estadísticamente más limpio**, salvando la significancia de *CAMKV* y *CELF4*.
2. **Advertencia de Baja Expresión de DRD2:** Se incorporó la advertencia sobre valores $< 1$ FPKM, discutiendo el ruido transcripcional frente a la expresión restringida en subpoblaciones de células T y ordenando qPCR ortogonal.
3. **Limitación de Deconvolución:** Se explicitó en las limitaciones del preprint la ausencia de deconvolución cuantitativa formal (CIBERSORTx), sugiriendo su implementación con conteos crudos y validación de scRNA-seq.
4. **Tolerabilidad de Pramipexole:** Se detalló el "vacío de 21 años" de no-replicación a través de las barreras clínicas de los D2/D3 agonists (mesolimbic D3-mediated Impulse Control Disorders, DAWS, hipotensión y sleep attacks).

---

## 3. Control de Versiones del Manuscrito

- Manuscrito principal actualizado: `preprint_dopaminergic_convergence_FM.md` (v2.2) ✅
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
