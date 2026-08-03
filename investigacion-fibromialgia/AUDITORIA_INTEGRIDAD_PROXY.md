# AUDITORÍA DE INTEGRIDAD — Anotación PENK vs TAC1 (Substance P)

**Fecha:** 2026-08-03
**Autor:** DAVI (detectado durante planificación de siguiente paso)
**Severidad:** ALTA (error de anotación genética en hallazgo publicado internamente)
**Estado:** CORREGIDO en este commit

---

## EL ERROR

En el análisis de la madrugada (2026-08-03), se anotó **PENK como proxy de "Substance P"** en
protocolos y reportes. Esto es **genéticamente incorrecto**:

| Gen | Proteína que codifica | Relación con Substance P |
|-----|----------------------|--------------------------|
| **TAC1** (preprotachykinin-1) | Substance P, Neurokinin A | ✅ **GEN REAL de Substance P** |
| **PENK** (proenkephalin) | Encefalinas (opioides endógenos) | ❌ NO — sistema opioide, no taquiquinina |
| PDYN | Dinorfinas | ❌ NO — opioide |
| PNOC | Nociceptina/orfanina FQ | ❌ NO — opioide atípico |

El mapeo probable del error: el paper de proteómica CSF (Khoonsari 2019 / PXD008076) detectó
la PROTEÍNA "Substance P" en CSF. Al hacer matching proteína→gen, se anotó PENK en vez de TAC1.

## LA VERIFICACIÓN (datos reales, GSE221921, 96 FM vs 93 HC)

Recalculado con el gen correcto (Mann-Whitney, mismo estándar adversarial):

| Gen | FM mean | HC mean | FC | MWU p | Cohen d | Interpretación |
|-----|---------|---------|-----|-------|---------|----------------|
| **TAC1** | 1.1752 | 0.5598 | **2.10** | **0.0002** | +0.47 | Substance P REAL — ¡más fuerte que PENK! |
| **PENK** | 2.8598 | 2.0716 | 1.38 | 0.0031 | +0.21 | Encefalinas — hallazgo SEPARADO |
| PNOC | 1.3007 | 1.3489 | 0.96 | 0.47 | -0.02 | Nociceptina: NS |
| OPRM1 | 3.0928 | 1.3553 | **2.28** | **<0.0001** | +0.53 | Receptor mu opioide — NUEVO |

### Consecuencias

1. **El claim "Substance P elevado en FM" SE SOSTIENE** — con TAC1 (FC=2.10, p=0.0002), que es
   MÁS fuerte y más significativo que PENK (FC=1.38, p=0.0031). El proxy no se cae; se corrige el gen.

2. **PENK ya no es "Substance P"** — es un hallazgo INDEPENDIENTE: encefalinas elevadas en PBMCs
   de FM. Combinado con OPRM1 (receptor mu) elevado (FC=2.28, p<0.0001), emerge un **eje opioide
   endógeno completo** (ligando PENK + receptor OPRM1) en PBMCs de FM — hallazgo mecanístico nuevo.

3. **Advertencia de dirección:** en CSF, los opioides endógenos (beta-endorfina) tienden a estar
   BAJOS en FM (Bäckryd 2014). PENK mRNA ↑ en PBMC vs beta-endorfina ↓ en CSF NO es necesariamente
   contradictorio (compartimentos y péptidos distintos), pero debe interpretarse con cuidado:
   encefalina ≠ beta-endorfina, y PBMC ≠ CSF. Documentar, no forzar coherencia.

## ARCHIVOS CORREGIDOS

- `PROTOCOL_Validation_IL6_PENK.md` — renombrado conceptual: proxies = IL-6 + TAC1/Substance P; PENK como hallazgo opioide separado
- `PROTOCOL_Olink_FM_Biomarker_Validation.md` — "Substance P (PENK)" → "Substance P (TAC1)"; nota PENK
- `PROTOCOL_DualPlasmaCSF_Validation.md` — tabla de proxies corregida
- `GROUNDING_Explicacion_Hallazgos_FM.md` — sección 2.4 corregida
- `GROUNDING_FM_Neurobioquimica_Central.md` — tabla y conclusiones corregidas
- `ADVERSARIAL_VERIFICATION_REPORT_2026-08-03.md` — matiz PENK/SP corregido
- `GROUNDING_IL8_Control_Positivo.md` — referencias al eje SP corregidas

## LECCIÓN (para el skill protein-lab)

**NUNCA asumir gen→proteína por nombre común.** "Substance P" → TAC1 (verificar en HGNC antes de
anotar). Los opioides endógenos (PENK/PDYN/PNOC) son un sistema distinto. Regla: para cada claim
proteína→gen, verificar el símbolo HGNC oficial antes de escribir el proxy.
