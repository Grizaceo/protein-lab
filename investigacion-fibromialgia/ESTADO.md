# ESTADO DEL PROYECTO — Fibromialgia (Consolidado al 2026-08-08)

**Fecha de actualización:** 8 de agosto de 2026
**Rama actual:** `fm/e1b-deconvolution-col9a1-ptn` (no `master`)
**Manuscrito actual:** `preprint_dopaminergic_convergence_FM.md` → **v2.10** (narrativa reorientada a FME)
**Manuscrito numerado sincronizado:** `preprint_dopaminergic_convergence_FM_numbered.md` → **v2.10** (regenerado 2026-08-08)
**PDFs:** `preprint_..._FM.pdf` (v2.2, 4-ago, DESACTUALIZADO) y `preprint_..._FM_numbered.pdf` (v2.2, 4-ago, DESACTUALIZADO)

---

## 1. Hitos Científicos Alcanzados

### Fase 0: Recopilación y Curación ✅ COMPLETADA
- Grounding de 19 papers con identificadores persistentes reales (DOI/PMID).
- Coordenadas 3D curadas: HDC (`4E1O`), TRPA1 (`6V9Y`), CPA3 (`AF-P15088-F1`), MS4A2 (`AF-Q01362-F1`).

### Fase 1: Reanálisis Transcriptómico ✅ COMPLETADO
- **GSE67311** (sangre total): downregulation robusta de mastocito/basófilo (CPA3, MS4A2, FCER1A, HDC; q<0.05).
- **GSE221921** (PBMCs): convergencia DRD2/MDGA2 (eje GWAS) + **hallazgo titular**: COL9A1 (d=+0.88) y PTN (d=+0.61) sobreviven 5 modelos de sensibilidad sexo + Bonferroni + ajuste por composición leucocitaria (4 deconvoluciones independientes, p=0.012–0.046). Eje opioide/taquikinina (TACR1/OPRM1/OPRK1/TAC1) = mayor tamaño de efecto pero **composicional** (cae tras ajuste celular; opioide exógeno no excluido). CA14 colapsa en estratificación por sexo → referencia direccional.
- **GSE229750** (neutrófilos/Tocilizumab): respuesta post-tratamiento verificada.

### Fase 2: Caracterización y Perfil de Dianas ✅ COMPLETADA
- MDGA2: AlphaFold + Open Targets (oe=0.257).
- Docking DRD2 vs Pramipexole: LE=0.384 kcal/mol/átomo.

### Línea 1: eQTLs GTEx v10 ✅ COMPLETADA
- rs36030569 → MDGA2 (Putamen p=2.13e-11, NES +0.3696; NAcc p=1.98e-9; Frontal p=2.66e-8).
- rs2022568 → MDGA2 (médula espinal C-1, p=6.03e-15, NES +0.4662).
- rs12420205 → DRD2 (médula espinal C-1, p=8.57e-7, NES +0.3936).
- rs2734833 (GWAS FM índice): NO eQTL basal; en LD estricto (D'=1.0) con sQTLs rs1076560/rs2283265 → splicing exón 6 (D2S/D2L).

### Fase 3: Tangentes de Investigación ✅ (modelo mecanístico + replicación)
- **Tangente 1 (IgG-SGC-Mastocito/Basófilo):** depleción de basófilos circulantes (GATA2 q=3.1e-5, MS4A2/FCER1A/HDC ↓ coordinado; KIT/TPSAB1 invariante). Autoantígenos gliales priorizados: GJA1 (`7F94`), KCNJ10 (`6M84`), CD40/CD40L, SCN9A. Crosstalk Fc/MRGPRX2 (`7VV3`)/FcγRIIIa (`3SGJ`).
- **Tangente 6 (Replicación GSE269047):** PBMCs N=43 → señal GATA2 (p=0.979) y DRD2 (p=0.777) **no replica** → evidencia de variabilidad por tipo celular (sangre total vs PBMCs), no falsificación de GSE221921.

### NUEVO (2026-08-07): Subfenotipo FME — Fibromialgia Respondedora al Ejercicio 📝 DISEÑO
- `GROUNDING_FM_VARIANTE_EJERCICIO.md`: 10 PMIDs verificados por API PubMed. EIH (analgesia por ejercicio) mediada por opioides endógenos; ~49% FM = SFPN subyacente (sustrato de COL9A1/PTN); respondedor vs no-respondedor.
- `INTEGRACION_GENETICA_OPRM1_5HTT_FME.md` (Módulo D): balance OPRM1/5-HTT/HTR1A (Tour 2017, PMID 28282362) como predictor genético de respondedor.
- `PROTOCOL_FME_Responder_Phenotyping.md` (Módulo C): diseño 75 FM + 75 HC, EIH (PPT), Olink plasma, biopsia SFPN, genotipado.
- **Estado:** HIPÓTESIS DE DISEÑO. No computable localmente (GSE221921 sin genotipos/bio/ejercicio). Entra al manuscrito como §4.7 (responder phenotyping) y §4.8 (genetic prediction) — narrativa/design-level only, sin recomputar estadísticas primarias.

---

## 2. Control de Versiones del Manuscrito

| Artefacto | Versión | Estado |
|---|---|---|
| `preprint_dopaminergic_convergence_FM.md` | v2.10 | Modificado (sin commitear) |
| `preprint_dopaminergic_convergence_FM_numbered.md` | v2.10 | Regenerado 2026-08-08 (lee del principal) |
| `preprint_dopaminergic_convergence_FM.pdf` | v2.2 | **DESACTUALIZADO** (4-ago) |
| `preprint_dopaminergic_convergence_FM_numbered.pdf` | v2.2 | **DESACTUALIZADO** (4-ago) |
| DOI Zenodo | `10.5281/zenodo.20250218` | Activo ✅ |

---

## 3. Estado de Blockers para Envío Editorial

| Requisito | Estado | Observaciones |
|---|:---:|---|
| Repositorio Público | ✅ COMPLETO | https://github.com/Grizaceo/protein-lab |
| Release Tag v1.0.0 | ✅ COMPLETO | Asociado a DOI Zenodo |
| Código de Reproducibilidad | ✅ COMPLETO | `/scripts` + `/analisis` |
| Manuscrito Numerado (v2.10) | ✅ COMPLETO | Sincronizado 2026-08-08 |
| **Subida a bioRxiv** | ❌ PENDIENTE | Requiere acción de Cristóbal |
| **PDFs de envío** | ❌ DESACTUALIZADOS | Regenerar desde v2.10 antes de enviar |
| Solicitud PCI Genomics | ❌ PENDIENTE | Tras DOI bioRxiv + cover letter `PLN_PCI_GENOMICS.md` |

---

## 4. Deuda de Higiene (resuelta parcialmente 2026-08-08)

- [x] `ESTADO.md` actualizado de v2.2 → v2.10, fecha 2026-08-08.
- [x] Numerado regenerado a v2.10 (antes v2.9).
- [x] 3 archivos FME (GROUNDING/INTEGRACION/PROTOCOL) listos para commitear.
- [ ] PDFs de envío siguen en v2.2 → regenerar (pandoc/latex) antes de bioRxiv.
- [ ] Skill `protein-lab` línea "FM Preprint v2.2 COMPLETO" → actualizar a v2.10.
- [ ] Decisión de rama: el trabajo FME vive en `fm/e1b-...`; ¿merge a `master` antes de bioRxiv?

---

*Fin del consolidado. Próximo paso sugerido: regenerar PDFs v2.10 y decidir merge de rama previo a bioRxiv.*
