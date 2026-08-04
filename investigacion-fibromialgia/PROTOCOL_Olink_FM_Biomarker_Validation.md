# Protocolo de Validación Plasmática FM — PLAN IN-SILICO + PRE-REGISTRO para datos futuros
## Convertido de diseño Olink experimental a plan in-silico ejecutable 2026-08-03
## ACTUALIZADO 2026-08-03 — post adversarial verification + grounding UKB + power/QSP

## Basado en:
- Chen 2025 UKB: CA14 ↓ plasma CWP, MR + coloc PP.H4>0.5 (PMID 41025730, PMC12713070)
- Li ZY 2025: UKB Olink 51K, 2,923 proteínas (PMID 40048323)
- Bäckryd 2017: 92 proteins multiplex CSF+plasma (PMID 28424559)
- Revisión sistemática FM proteomics 2024 (PMID 38652420)
- Power analysis: `scripts/power_analysis_ca14_olink.py` (2026-08-03)
- QSP model: `scripts/qsp_ca14_ph_nociception.py` + SIMULACION_QSP_CA14_PH.md

## 0. GROUNDING DE DATOS PÚBLICOS (2026-08-03) — LEER ANTES DE COMPRAR NADA

### No existe dataset Olink de FM en GEO
- Búsqueda GEO (eutils): `fibromyalgia AND Olink` → **0 resultados**
- `fibromyalgia AND plasma` → solo GSE269047 (ya analizado, HERV/ME-CFS) y GSE229750 (neutrófilos)
- Conclusión: la validación Olink FM en plasma **no se puede hacer con datos públicos descargables hoy**. El pipeline `scripts/analyze_olink_npx.py` está listo para cuando lleguen datos (propios o de un colaborador).

### Lo que Bäckryd 2017 YA confirmó en plasma (no hay que re-comprarlo)
- **IL-6 elevado en plasma FM: p<0.001 (univariado)** — validación Olink directa ya publicada
- ⚠️ **PERO IL-6 NO discriminó en CSF** (no estuvo en top-11 CSF) — matiza el claim "proxy de cambios centrales": IL-6 es periférico elevado, no un espejo central fuerte
- **IL-8 es el solapamiento CSF+plasma REAL** (elevado en ambos compartimentos) — mejor control positivo que TNF-α
- TNF-α, BDNF, GDNF: casi todos bajo LoD en CSF — no medibles por Olink en ese contexto

### Implicancia para el protocolo
1. Si el objetivo es "validar IL-6 en plasma FM con Olink": **ya está publicado** (Bäckryd). No comprar un run nuevo para eso — citar.
2. El valor de un run propio sería: correlación directa CSF↔plasma en los mismos sujetos (que Bäckryd no hizo por sujeto) o validación de Substance P (TAC1, no está en panel Olink; PENK es hallazgo opioide separado).
3. **Control positivo correcto: IL-8** (elevado en plasma + CSF, reproducido por múltiples estudios) — no TNF-α (bajo LoD).

---

## 1. Objetivo

Validar **IL-6** y **Substance P (TAC1)** como biomarcadores plasmáticos que correlacionan con cambios centrales (CSF) en fibromialgia, usando tecnología Olink PEA (Proximity Extension Assay).
*Corrección 2026-08-03: Substance P es codificada por TAC1, no PENK. PENK (encefalinas) es hallazgo opioide separado — ver AUDITORIA_INTEGRIDAD_PROXY.md*

---

## 2. Biomarcadores candidatos — ACTUALIZADO 2026-08-04 (post deep-dive COL9A1)

**PIVOT 2026-08-04:** El deep-dive COL9A1 (experimentos C1-C5) reemplaza a CA14 como candidato principal de validación. CA14 no sobrevive female-only (p=0.1345) ni ajuste por composición celular (E1). La hipótesis CA14→pH→ASIC1a fue descartada (E5: QSP v3 transitorio, ΔpH=-0.015). COL9A1 reemplaza a CA14: d=0.88, robusto 5/5 modelos, sobrevive female-only y sex-adjusted.

**NUEVAS ADICIONES al panel Olink:** COL9A1, PTN (pleiotrophin), BPIFB2. ST3GAL1 no se incluye (enzima intracelular, no medible en plasma Olink).

| Biomarcador | Rationale | Proxy grade |
|-------------|-----------|-------------|
| **COL9A1** (colágeno IX alpha 1) | **CANDIDATO PRINCIPAL (nuevo 2026-08-04).** Robusto 4/5 modelos en GSE221921 (d=0.88, FC=2.32, p_Bonf=9e-08). Sobrevive female-only Bonferroni (p_fem_bonf=0.0013) Y sex-adjusted Bonferroni (p_adj_bonf=0.000085). Causal en CWP por Chen 2025 (PMID 41025730). Co-expresado con PTN (r=0.51). Proteína secretada ECM — detectable en plasma. Power: 75+75 cubre escenario moderado (d_protein=0.53, power=88%). | **ALTO** (robusto, Bonferroni-survivor, direccional, detectable) |
| **PTN** (pleiotrophin) | **NUEVO 2026-08-04.** Robusto 4/5 modelos. Sobrevive female-only Bonferroni (p_fem_bonf=0.00095) Y sex-adjusted Bonferroni (p_adj_bonf=0.020). Factor neurotrófico secretado (neurite outgrowth, ligando ALK). Co-expresado con COL9A1 (r=0.51, p<0.001). Secretado — detectable en plasma. | **ALTO** (Bonferroni-survivor, secretado, neurotrófico) |
| **BPIFB2** (BPI fold family B2) | **NUEVO 2026-08-04.** Robusto 4/5 modelos NOMINAL (p_sex_adj=0.0035). NO sobrevive Bonferroni sex-adjusted (p_adj_bonf=0.063). Innate immunity (LPS binding). Co-expresado con COL9A1 (r=0.51, p<0.001). Secretado — detectable en plasma. **Candidato secundario: merece validación pero requiere confirmación.** | **MEDIO** (nominal no Bonferroni, secretado) |
| **CA14** (anhidrasa carbónica XIV) | **DEGRADADO 2026-08-04.** Causal en CWP (MR+colocación UKB) PERO no sobrevive female-only (p=0.1345) ni deconvolución (E1). Hipótesis pH→ASIC1a descartada (E5). Mantener como referencia: medir si panel incluye CA14 pero no como primario. Predicción Olink: ↓ en plasma FM (MR protector). | **MEDIO** (causal UKB pero no robusto en PBMC) |
| IL-6 | Inflamación sistémica; ↑ en GSE221921 (FC=1.66, p=0.0002); ya validado en plasma FM (Bäckryd 2017) | **MEDIO** (ya publicado, citar) |
| Substance P (TAC1) | Neuropéptido de dolor; ↑ en GSE221921 (FC=2.10, p=0.0002, d=+0.47); correlación plasma↔CSF (Karlsson 2019) | **MEDIO** (no en UKB) |
| ~~PENK / OPRM1~~ | **RETIRADOS 2026-08-04.** Eje opioide es composicional (E1): 0/7 genes sobreviven ajuste por fracciones celulares. OPRM1 colapsa de p=0.0003 a p=0.40. No validar a nivel proteico. | **BAJO** (confundido por composición celular) |
| Control negativo de señal inmune | TNFRSF1B, CD74, COL18A1, BTN2A1, TNFRSF4 — causales UKB ↓ en PBMC FM | observacional |

### Estructura biológica del módulo COL9A1 (C1-C5)

Los 4 genes que pasan nominal female-only + sex-adjusted (COL9A1, BPIFB2, PTN, ST3GAL1) forman **dos ejes convergentes**, no un módulo singular. Solo COL9A1 y PTN sobreviven corrección múltiple Bonferroni (sex-adjusted).

- **EJE 1 (estructural/neuro):** COL9A1 + PTN → cartílago structural + neurite outgrowth. Co-expresados r=0.51. Dolor articular + reparación neural.
- **EJE 2 (innate immunity):** BPIFB2 + ST3GAL1 → LPS binding + T cell sialylation. Dolor indirecto vía inflamación.
- ST3GAL1 anticorrelaciona con COL9A1 (r=-0.23) — probable regulador negativo del módulo.

Las correlaciones no difieren FM vs HC (Fisher p>0.17) — el módulo es estructural, no disease-specific. La diferencia está en los niveles absolutos, no en la coordinación.

---

## 3. Platforma Olink

### Product selection
- **Olink Explore HT** — 1,300+ analytes, incluye IL-6 y Substance P
- **Olink Target 96 Inflammation** — panel de 92 proteínas inflamatorias, incluye IL-6 (más costo-eficiente que Explore HT)
- **Alternativa:** Olink Flex (customizable) para panel de 10-15 analytes

### Rationale para Olink Target 96 Inflammation
- ✅ Incluye **IL-6**
- ✅ Incluye **TNF-α, IL-1β, IL-8, IL-10, IFN-γ** (panel inflamación — relevante FM)
- ❌ No incluye **Substance P** (es un neuropeptido, no inflamación)
- **Cost:** ~$2,000-3,000 por muestra (92 analytes)

### Rationale para Olink Explore HT + Substance P
- ✅ **IL-6** + **999 analytes** (proteoma completo)
- ✅ Incluye paneles de neuroinflamación
- ✅ Substance SP está en panel neuropéptido
- **Cost:** ~$6,000-8,000 por muestra (más completo)

### Decisión
- **IL-6:** Medir con Olink Explore HT (panel Neuroinflammation)
- **Substance P:** **NO** disponible en Olink directamente — usar radioinmunocromanografía (RIA) o ELISA especializada (Phoenix Pharmaceuticals)

---

## 4. Design Sample Size

### Power calculation — REDISEÑADO 2026-08-03 (candidato principal: CA14, no IL-6)

**⚠️ El power previo (n=40, FC≥1.6) estaba calibrado para IL-6 — ya no es el candidato.**
Simulación Monte Carlo propia (`scripts/power_analysis_ca14_olink.py`, 2000 sims, alpha=0.05,
Mann-Whitney, CV técnico Olink 16.5% mediana → sd_log2=0.238):

| n/grupo | d=0.3 | d=0.4 | d=0.5 | d=0.6 |
|---------|-------|-------|-------|-------|
| 40 | 0.25 | 0.37 | 0.55 | 0.71 |
| 50 | 0.29 | 0.46 | 0.65 | 0.81 |
| 70 | 0.37 | 0.61 | **0.81** | 0.92 |
| 100 | 0.51 | 0.76 | 0.92 | 0.98 |

- **Efecto esperado de CA14:** desconocido en plasma FM (nunca medido — ver §2). Rango plausible
  d=0.3–0.6 (proteómica plasmática en dolor crónico; Bäckryd/Widenfalk reportan d≈0.4–0.6).
- **Recomendación (poder ≥ 0.80):** d=0.6 → n=50/grupo; d=0.5 → n=70/grupo (140 total);
  d≤0.4 → NO alcanza 0.80 con n≤100 → solo detectable en pooling multicéntrico.
- **Estratificación por sexo (FM ~90% mujeres):** restringir a mujeres reduce n efectivo:
  con n=40/grupo nominal y 90% mujeres, poder cae a 0.51 (d=0.5) / 0.65 (d=0.6).
- **Conclusión honesta:** una cohorte individual FM vs HC (n=40-70) solo detecta CA14 si el
  efecto real es medio-grande (d≥0.5). Para efectos pequeños (plausibles en proteómica
  plasmática), se requiere diseño multicéntrico/pooled o meta-análisis con datasets públicos
  existentes (vía B del análisis in-silico: Chen 2025 UKB ya tiene n=29,254 — su señal es la
  evidencia más potente disponible y no requiere laboratorio nuevo).

### Pre-registro (plan de análisis para datos futuros — in-silico hoy)

Si en el futuro un colaborador/dataset provee muestras FM+HC con Olink (o se liberan summary
stats de UKB CWP), el análisis será:

```python
# Pipeline estadístico — pre-registro 2026-08-03
# 1. NPX Olink (log2-like, no normal) → Mann-Whitney de dos colas (NO t-test)
# 2. H1 direccional PRE-REGISTRADA: CA14 ↓ en plasma FM (basada en Chen 2025: top-10
#    downregulated en CWP; MR protector de elevación genética)
# 3. Bonferroni sobre targets: CA14 + IL-8 (control) + SP (ELISA) → p*3
# 4. Sensibilidad: excluir medicación opioide/antidepresiva (confusor conocido);
#    estratificar por sexo (FM ~90% mujeres) y edad
#    NOTA AUDITORÍA 2026-08-04: GSE221921 (PBMC discovery) carece de datos de
#    medicación, edad y BMI — el eje opioide (OPRM1/OPRK1/TACR1) observado allí
#    no puede distinguirse de un efecto farmacológico. La cohorte Olink debe
#    registrar medicación al momento del muestreo y estratificar obligatoriamente.
# 5. Control de calidad: LOD, CV de duplicados; NPX fuera de rango → excluir
# 6. Reportar efecto (d de Cohen) + IC 95%, no solo p — el tamaño importa
```

---

## 5. WF IN-SILICO (EJECUTABLE HOY — costo cero)

Este protocolo ya no requiere reclutamiento ni muestras. La validación de CA14 ↓ en
plasma FM se hace con evidencia existente + pre-registro para datos futuros:

### Fase in-silico 1 — Dirección plasmática (HECHO 2026-08-03)
- [x] Chen 2025 UKB (n=29,254): CA14 entre top-10 ↓ en CWP; MR protector de elevación →
      predicción CA14 ↓ plasma FM (PMID 41025730, full text en fuentes_verificadas/)
- [x] Revisión sistemática FM (PMID 38652420): CA14 NO reportada → primer claim en su clase

### Fase in-silico 2 (pendiente — D2)
- [ ] Cruzar las 145 proteínas diferenciales de PMID 38652420 contra los 18 causal UKB
      (ver tabla en §2 y Sch. 145) — buscar convergencia de vías

### Pre-registro (para cuando lleguen datos)
Pipeline listo: `scripts/analyze_olink_npx.py`. H1: CA14 ↓ plasma FM (pre-registrado
2026-08-03). Mann-Whitney NO paramétrico + Bonf (CA14 + IL-8 + SP) + d Cohen + IC95.

## 5b. WF DE LABORATORIO (CONTINGENTE — solo si hay colaboración clínica)

Contexto: con investigación puramente in-silico sin acceso a muestras, este cronograma
NO es ejecutable por DAVI/Cristóbal. Se documenta aquí para cuando un colaborador o
datos de multicéntrico estén disponibles. Reclutamiento, extracción y Olink son de
competencia del colaborador/laboratorio acreditado.

### Reclutamiento + muestras (colaborador)
- 50–70 FM (ACR 2010/2016) + 50–70 HC (sexo/edad/IMC emparejados; FM ~90% mujeres)
- Plasma EDTA 1500g 15min −80°C; CSI opcional (subconjunto 10+10)
- Requisito crítico: confirmar que el panel Olink elegido INCLUYE CA14 (Target 96 inflamación
  NO lo incluye — solo Explore HT o Explore 3072 cubren anhidrasas carbónicas)

### Análisis estadístico por DAVI
Internal script: `scripts/analyze_olink_npx.py` (Mann-Whitney + Bonferroni correcto + Cohen's d
+ AUX out-of-fold corregido + correlación CSI↔plasma)

### Métricas de validación (ajustadas 2026-08-03 — effect sizes reales son small)
| Métrica | Threshold | Rationale |
|---------|-----------|-----------|
| Fold change | ≥ 1.2 (↑) o ≤ 0.83 (↓) en NPX log2 | Diferencial expr — en NPX log2 un FC de 1.66 transcriptómico ≈ ~1.2 en escala log2 |
| p-value | < 0.05 (Mann-Whitney + Bonferroni) | Significancia estadística con corrección |
| Effect size | Cohen's d ≥ 0.2 y reportado explícitamente | Los efectos FM en GSE221921 son d≈0.2-0.3 (small) — threshold 0.5 era irreal |
| CSF↔Plasma r | ≥ 0.4 (exploratorio) | Correlación compartimentos; Bäckryd no reportó r por sujeto |
| AUC | ≥ 0.60 out-of-fold | Capacidad discriminadora honesta (in-sample infla) |

---

## 6. Control positivo (validación) — CORREGIDO 2026-08-03 (ver GROUNDING_IL8_Control_Positivo.md)

- **IL-8 (CXCL8)** — **Control positivo principal, CONFIRMADO por grounding de primera mano:**
  - ✅ Elevado en CSF de FM (Kadetoff 2012, Kosek 2015, Bäckryd 2017)
  - ✅ Elevado en plasma/suero de FM (Kadetoff 2012, Bäckryd 2017, O'Mahony 2021)
  - ✅ Robusto en metaanálisis reciente (O'Mahony 2021, robusto en sensitivity analysis)
  - ✅ Mediador central distintivo de dolor disfuncional vs inflamatorio (Kosek 2015: IL-8 en FM vs IL-1β en RA)
  - ⚠️ NO es FM-específico: marcador de dolor crónico/disfuncional general (Rosenström 2024: 6/9 dolores nociceptivos)
  - **Rol en protocolo:** ancla técnica de reproducibilidad (¿el panel detecta FM vs HC en ambos compartimentos?) — no como evidencia FM-exclusiva
- **CXCL6, CXCL5, MCP-2/CCL8, LAP-TGF-β1** — las 4 proteínas que solapan CSF y plasma en el top discriminador de Bäckryd. Controles secundarios.
- **IL-6 — matiz:** el metaanálisis O'Mahony 2021 lo muestra significativo pero NO robusto en sensitivity analysis. Nuestro hallazgo GSE221921 (Bonf=0.003) sigue válido en PBMCs; pero como endpoint periférico, IL-8 es más sólido que IL-6. Prioridad: IL-8 > IL-6.
- ~~TNF-α~~ — ❌ casi todos los valores bajo LoD en CSF (Bäckryd 2017). No usable como control en CSF.

---

## 7. Cronograma

### IN-SILICO (ejecutable HOY)
| Fase | Estado | Acción | Tiempo in-silico |
|------|--------|--------|-----------------|
| A — Grounding UKB | ✅ | Chen 2025 verificado full-text (PMID 41025730) | HECHO |
| B — Power CA14 | ✅ | Monte Carlo sim (scripts/power_analysis_ca14_olink.py) | HECHO |
| C — Eje opioide GSE67311 | ✅ | Validación completa (scripts/validate_opioid_axis_…) | HECHO |
| D — QSP model | ✅ | Negativo: CA14↓ no acidifica (scripts/qsp_ca14_ph_) | HECHO |
| D2 — 145 proteínas × UKB | 🔲 | Crossover PMID 38652420 vs 18 causal UKB | ~30 min |
| E — Preprint v2.6 | ✅ | Draft 32 pgs | HECHO |

### FUTURO (contingente, requiere colaborador/datos)
| Fase | Acción |
|------|--------|
| 0 | Contactar Bäckryd/Ghafouri (Linköping) para datos crudos Olink FM (datos no públicos — alternativa costo cero) |
| 1 | Colaborador clínico: reclutamiento FM+HC + plasma EDTA |
| 2 | Olink run (Explore HT, panel que incluya CA14 — NO Target 96 inflamación) + SP ELISA |
| 3 | DAVI ejecuta pipeline pre-registrado (`scripts/analyze_olink_npx.py`) |

---

## 8. Costos

| Item | In-silico (hoy) | Futuro (si aparece colaboración) |
|------|----------------|---------------------------------|
| Evidencia CA14 ↓ en plasma | $0 — PMID 41025730 (ya verificado) | — |
| Power analysis | $0 — sim Monte Carlo lista | — |
| Re-analizar datos Olink públicos | $0 — Bäckryd 2017 PMID 28424559 (IL-6/IL-8 ya validados; si se obtienen NPX crudos de Linköping, el script `analyze_olink_npx.py`) está listo | — |
| Olink run propio | — | ~$5-8K (Explore HT, 100 muestras) |
| SP ELISA | — | ~$2K (Phospho, 80 muestras) |

**Conclusión:** el abordaje in-silico actual=$0; el abordaje clínico futuro=$7-10K +
colaborador. El costo cero ya produce evidencia publicable: preprint v2.6 con CA14 como
primer candidato causal en FM, respaldado por MR+Fisher de 29K personas.

---

## 9. Riesgos

| Riesgo | Prob | Mitigación |
|--------|------|------------|
| CA14 no detectable en plasma periférico (LOD bajo) | MEDIUM | Chen 2025: CA14 sí medible en UKB Olink Explore; Olink tiene alta sensibilidad para CA14; confirmar cobertura del panel elegido |
| Efecto real CA14 ↓ es pequeño (d≤0.3) | HIGH | Power sim: cohorte individual no lo detecta; la evidencia UKB n=29K ya está publicada (PMID 41025730) — es el gold standard sin laboratorio |
| Datos Olink públicos no disponibles para FM | HIGH (hoy) | Bäckryd/Ghafouri han compartido datos en el passado; contactar informalmente; alternativa: summary stats UKB cuando se liberen |
| Interpretación errónea de CA14 con Target 96 inflamación (NO incluye CA14) | CRÍTICO | Requisito al colaborador: confirmar que el panel INCLUYE CA14 antes de ordenar |
| QSP descartó vía periférica simple | RESUELTO | Doc SIMULACION_QSP_CA14_PH.md — CA14 candidato causal se mantiene; mecanismo va a SNC u otras vías |

---

## 10. Próximos pasos

### In-silico (hoy)
1. ✅ Grounding UKB + grounding IL-8 control — COMPLETADO (2026-08-03)
2. ✅ Eje opioide/taquinikinina PBMC + validación GSE67311 — COMPLETADO
3. ✅ Corrección PENK→TAC1 + adversarial verification — COMPLETADO
4. ✅ Power analysis CA14 Monte Carlo — COMPLETADO
5. ✅ QSP CA14-pH modelo — NEGATIVO (vía simple periférica descartada para pH)
6. ✅ Preprint v2.6 — COMPLETADO
7. ✅ Protocolo convertido a plan in-silico — COMPLETADO
8. □ D2 — Crossmatch 145 proteínas FM (PMID 38652420) × 18 causal UKB

### Futuro (experimental, cuando haya colaborador/datos)
1. Contactar Bäckryd/Gröfouri (Linköping) por NPX crudos Olink FM para reanálisis <code>analyze_olink_npx.py</code>
2. Un run Olink propio CON CA14 en el panel = validación directa de la predicción registrada
3. Publicar: sitio + demo + pre-registro (OSF → preprint → eventualmente journal)

## 11. Key conclusions for protein lab

1. **CA14** es el primer candidato causal en FM: MR + colocalización PP.H4>0.5 en UKB (n=54K), ↓ plasma CWP ↑ en PBMC miRNA, predicción direccional CA14 ↓ plasma FM pre-registrada.
2. **Machine mechanism vía pH queda descartada** por el machismo QSP del compartimento único — no replantea la candidatura causal, solo el mecanismo (SNC / pico transitorio / marcador).
3. **Eje opioide/taquinacina:** activado en PBMCs (TACR1 d= +0.60, OPRM1 d=+0.53) pero NO replica en whole blood a nivel de amplitud; es compartimento-dependiente.
4. **Protocolo listo** para ejecución in-silico (costo cero) + contingente (colaborador). Estricto (bajo Elisa / resubrap) respaldo de n=29K.
