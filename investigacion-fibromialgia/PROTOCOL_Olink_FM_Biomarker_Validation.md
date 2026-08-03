# Protocolo Experimental: Validación de biomarcadores IL-6 + Substance P en plasma FM
## Diseño in-silico de protocolo Olink

## Basado en:
- Grounding: `~/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/GROUNDING_FM_Neurobioquimica_Central.md`
- Bäckryd 2017 (PMID 28424559) — 92 proteins multiplex CSF+plasma de 40 FM
- GSE221921 in-silico: IL6 FC=1.66↑, PENK FC=1.38↑ en PBMCs FM
- GSE67311 cross-validation (70 FM vs 70 HC) — paper Wray 2009

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
# Pipeline estadístico
from scipy import stats
import numpy as np

# 1. Fold change FM vs HC
fc = np.mean(fm_plasma) / np.mean(hc_plasma)

# 2. T-test (unpaired)
t_stat, p_val = stats.ttest_ind(fm_plasma, hc_plasma)

# 3. Correlación CSF↔Plasma (si se mide CSF)
r, p_corr = stats.pearsonr(plasma_values, csf_values)

# 4. Receiver Operating Characteristic
from sklearn.metrics import roc_auc_score
auc = roc_auc_score(group_labels, plasma_values)

# 5. Effect size (Cohen's d)
from numpy import std, mean
cohens_d = (mean(fm_plasma) - mean(hc_plasma)) / np.sqrt((std(fm_plasma)**2 + std(hc_plasma)**2)/2)
```

### Métricas de validación
| Métrica | Threshold | Rationale |
|---------|-----------|-----------|
| Fold change | ≥ 1.5 (↑) o ≤ 0.67 (↓) | Diferencial expr |
| p-value | < 0.05 (unpaired t-test) | Significancia estadística |
| Effect size | Cohen's d ≥ 0.5 | Magnitud del efecto |
| CSF↔Plasma r | ≥ 0.6 | Correlación compartimentos |
| AUC | ≥ 0.70 | Capacidad discriminadora |

---

## 6. Control positivo (validación)

- **TNF-α** — documentada ↑ en plasma FM (Bäckryd 2017) — valida protocolo
- **IL-8 (CXCL8)** — documentada ↑ en CSF + plasma FM (Bäckryd 2017 PMID 28424559)

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

## 8. Budget estimado

| Item | Cost (USD) |
|------|-----------|
| Olink Explore HT (40 FM + 40 HC) | $6,000-8,000 |
| Substance SP ELISA (80 samples) | $2,400 |
| TNF-α/IL-8 control panel | $800 |
| **Total estimado** | **$9,200-11,200** |

**Alternativa de bajo costo:** Olink Target 96 Inflammation ($2,000-3,000) — cubre IL-6 + 91 inflamatorios más

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

### In-silico (inmediato)
1. ✅ Validar proxies in GSE221921 — **COMPLETADO** (IL6: FC=1.66, PENK: FC=1.38)
2. ✅ Cross-validation GSE67311 — **COMPLETADO** (Wray 2009 panel)
3. ⏳ Confirmar LGALS3BP discordancia — **CONFIRMADA** (CSF↑ / PBMC↓)

### Experimental (para futuro IRB)
1. Order Olink Explore HT panel
2. Draft IRB protocol (human subjects)
3. Establish sample collection protocol
4. Statistical analysis plan

---

## 11. Key conclusions for protein lab

1. **IL-6** es el mejor proxy periférico validado computationalmente (HIGH grade)
2. **Substance SP (PENK)** es prometedor pero no está en paneles Olink directos — usar como endpoint secundario con ELISA
3. **LGALS3BP** no es un proxy viable (discordancia confirmada)
4. **Protocolo listo** para implementación en protein lab cuando IRB esté aprobado
