# Protocolo Experimental: Validación de biomarcadores IL-6 + Substance P en plasma FM
## Diseño in-silico de protocolo Olink
## ACTUALIZADO 2026-08-03 — post adversarial verification + grounding de datasets

## Basado en:
- Grounding: `~/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/GROUNDING_FM_Neurobioquimica_Central.md`
- Bäckryd 2017 (PMID 28424559) — 92 proteins multiplex CSF+plasma de 40 FM
- GSE221921 in-silico: IL6 FC=1.66↑, PENK FC=1.38↑ en PBMCs FM (verificado adversarialmente 2026-08-03)
- GSE67311 cross-validation (70 FM vs 70 HC) — paper Wray 2009

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
2. El valor de un run propio sería: correlación directa CSF↔plasma en los mismos sujetos (que Bäckryd no hizo por sujeto) o validación de PENK/Substance P (que no está en panel Olink).
3. **Control positivo correcto: IL-8** (elevado en plasma + CSF, reproducido por múltiples estudios) — no TNF-α (bajo LoD).

---

## 1. Objetivo

Validar **IL-6** y **Substance P (PENK)** como biomarcadores plasmáticos que correlacionan con cambios centrales (CSF) en fibromialgia, usando tecnología Olink PEA (Proximity Extension Assay).

---

## 2. Biomarcadores candidatos

| Biomarcador | Rationale | Proxy grade |
|-------------|-----------|-------------|
| IL-6 | Inflamación sistémica; significante ↑ en GSE221921 (FC=1.66, p=0.033); documentada elevación plasmática en FM (O'Mahony 2021) | **HIGH** |
| Substance P (PENK) | Neuropeptido de dolor; ↑ trend en GSE221921 (FC=1.38, p=0.157); correlación plasma↔CSF documentada (Karlsson 2019) | **MEDIUM** |

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

### Power calculation
- Effect size esperado: IL-6 FC ≥ 1.6 (GSE221921)
- Alpha: 0.05, Power: 0.80, Ratio FM:HC = 1:1
- **Mínimo:** 36 pares FM+HC (total 72)
- **Planeado:** 40 FM + 40 HC (buffer 10%)

### Rationale n=40
- Bäckryd 2017 usó n=40 FM vs 20 HC (92 proteínas)
- GSE221921: n=96 FM vs 93 HC
- GSE67311: n=70 FM vs 70 HC

---

## 5. Workflow Experimental

### Fase 1: Reclutamiento
- 40 pacientes FM (diagnóstico ACR 2010/2016)
- 40 controles santé (HC) emparejados (edad, sexo, IMC)

### Fase 2: Recolección de muestras
- **Plasma:** EDTA, centrifugado 1500g 15min a 4°C, almacenado -80°C
- **CSF:** opcional (subconjunto de 10 FM + 10 HC para correlación directa)
- Fasting ≥ 8 horas previo a extracción

### Fase 3: Análisis Olink
- **Olink Explore HT** para IL-6 + panel neuroinflamación (96 analytes)
- **Olink Target 96 Inflammation** como panel secundario
- Substance SP: ELISA (Phoenix Pharmaceuticals kit) o RIA

### Fase 4: Análisis estadístico
```python
# Pipeline estadístico — CORREGIDO 2026-08-03 (ver adversarial verification)
# NPX Olink es log2-like y no-normal → Mann-Whitney, NO t-test
# Usar directamente: scripts/analyze_olink_npx.py
from scipy import stats
import numpy as np

# 1. Fold change FM vs HC
fc = np.mean(fm_plasma) / np.mean(hc_plasma)

# 2. Mann-Whitney U (NPX no es normal; t-test paramétrico era inapropiado)
u_stat, p_val = stats.mannwhitneyu(fm_plasma, hc_plasma)

# 3. Bonferroni sobre N targets (ej: 3 proxies → p * 3)
p_bonf = min(1.0, p_val * n_targets)

# 4. Correlación CSF↔Plasma (si se mide CSF en los mismos sujetos)
r, p_corr = stats.pearsonr(plasma_values, csf_values)

# 5. AUC OUT-OF-FOLD honesta (no in-sample — ver validate_fm_biomarkers_iter2.py)
#    StratifiedKFold 5 + LogisticRegression, predict_proba en el fold de test

# 6. Effect size (Cohen's d pooled)
from numpy import std, mean
sp = np.sqrt(((n1-1)*std(fm_plasma, ddof=1)**2 + (n2-1)*std(hc_plasma, ddof=1)**2)/(n1+n2-2))
cohens_d = (mean(fm_plasma) - mean(hc_plasma)) / sp
```

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

## 7. Timeline

| Week | Fase | Deliverable |
|------|------|-------------|
| 1 | Protocol setup | IRB draft + Olink order |
| 2-4 | Reclutamiento | 40 FM + 20 HC |
| 5 | Sample collection | Plasma + CSF (subset) |
| 6 | Olink run | Raw NPX values |
| 7 | Statistical analysis | Fold change + p-values |
| 8 | Correlación CSF↔plasma | Pearson r |
| 9 | Report generation | Final report |

---

## 8. Budget estimado — CORREGIDO 2026-08-03 (costos previos inflados)

| Item | Cost (USD) | Nota |
|------|-----------|------|
| Olink Target 96 Inflammation (40 FM + 40 HC) | $4,000-6,000 | ~$50-75/muestra académico; un run de 96 muestras ≈ $5K |
| Substance SP ELISA (80 samples) | $2,400 | Phoenix Pharmaceuticals kit |
| IL-8 control (incluido en panel) | $0 | Ya viene en Target 96 |
| **Total estimado** | **$6,400-8,400** | Previo decía $9-11K — corregido |

**Alternativa de costo cero (inmediata):** la validación Olink de IL-6 en plasma FM YA está publicada (Bäckryd 2017, p<0.001). El run propio solo se justifica si se añade valor: correlación CSF↔plasma por sujeto, o validación de PENK/SP con ELISA.

---

## 9. Riesgos y mitigaciones

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|------------|
| Substance SP no detectable en plasma | HIGH | Medir como proxy el IL-6 + TNF-α, usar SP como secondary endpoint |
| LGALS3BP discordancia (ya confirmada) | RESOLVED | No incluir en protocolo — usar como control negativo |
| Niveles de IL-6 variables por circadiano | MEDIUM | Establecer horarios fijos de extracción (fasting AM) |
| No se puede acceder a CSF | HIGH | Subestudio con consentimiento separado; usar plasma como proxy primario |

---

## 10. Next steps

### In-silico (hecho)
1. ✅ Validar proxies in GSE221921 — COMPLETADO + verificado adversarialmente (2026-08-03): IL6 Bonf=0.003, PENK Bonf=0.047, LGALS3BP unsuitable, PCSK1N re-clasificado
2. ✅ Cross-validation GSE67311 — COMPLETADO (Wray 2009 panel)
3. ✅ Grounding datasets públicos (2026-08-03): NO hay dataset Olink FM en GEO; Bäckryd 2017 ya validó IL-6 plasma (p<0.001) y mostró IL-8 como solapamiento CSF+plasma real
4. ✅ Pipeline Olink listo: `scripts/analyze_olink_npx.py` (Mann-Whitney + Bonferroni + Cohen's d + AUC OOF + correlación CSF)

### Experimental (requiere colaboración o IRB)
1. ⏸️ Un run Olink propio SOLO se justifica con valor agregado: correlación CSF↔plasma por sujeto o validación PENK/SP (ELISA, no está en panel Olink)
2. ⏸️ Alternativa costo cero: contactar a Bäckryd/Ghafouri (Linköping) por datos crudos Olink FM para reanálisis independiente — los datos NPX no están en repositorio público
3. ⏸️ Draft IRB solo si se recluta cohorte propia

---

## 11. Key conclusions for protein lab

1. **IL-6** es el mejor proxy periférico validado computationalmente (HIGH grade)
2. **Substance SP (PENK)** es prometedor pero no está en paneles Olink directos — usar como endpoint secundario con ELISA
3. **LGALS3BP** no es un proxy viable (discordancia confirmada)
4. **Protocolo listo** para implementación en protein lab cuando IRB esté aprobado
