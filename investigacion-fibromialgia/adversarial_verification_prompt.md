# PROMPT: Adversarial Verification Agent
## Para validar hallazgos in-silico de IL-6 + PENK + LGALS3BP en FM

---

## Instrucciones para el agente adversarial

Actúas como un revisor científico adversarial que evalúa el trabajo in-silico realizado sobre biomarcadores plasmáticos en fibromialgia (FM). Tu objetivo: encontrar fallos, puntos ciegos, y limitaciones en el análisis.

### Archivo a auditar:
- Grounding principal: `~/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/GROUNDING_FM_Neurobioquimica_Central.md`
- Protocolo Olink: `~/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/PROTOCOL_Olink_FM_Biomarker_Validation.md`
- Script in-silico: `~/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/validate_fm_biomarkers_iter2.py`

### Dataset fuente:
- GSE221921 (96 FM PBMCs vs 93 HC PBMCs, RNA-seq FPKM)
- GSE67311 (70 FM vs 70 HC, cross-validation)

### Hallazgos a auditar:
1. IL-6 FC=1.66↑, p=0.033, AUC=0.66 (validated proxy)
2. PENK FC=1.38↑ trend, p=0.157 NS (trend proxy)
3. LGALS3BP discordancia CSF↑/PBMC↓ (unsuitable)
4. 2-gene model AUC=0.65 (low)

---

## Cuestión 1: Data integrity
Verifica:
- ¿El parsing del archivo `validate_fm_biomarkers_iter2.py` mapea correctamente etiquetas `Etiology` a samples?
- Busca: `sample_map`, `fm_samples`, `hc_samples`
- ¿Hay samples excluidos o mal etiquetados?

Instrucciones: Lee `validate_fm_biomarkers_iter2.py` y verifica la lógica de mapeo etiqueta->sample. Cuenta cuántos samples se usan. Identifica cualquier sample cuyo valor sea > 3 SD del mean (outlier). Reporta count.

## Cuestión 2: Statistical robustness
Verifica:
- ¿Usar t-test unpaired asumiendo normalidad es correcto para datos FPKM (no normalmente distribuidos)?
- ¿Hay multiple testing correction? (Bonferroni/Holm)
- ¿AUC=0.66 es suficiente para claim "validated proxy"?

Instrucciones: Para IL6 y PENK, calcula:
1. Shapiro-Wilk normality test (p<0.05 = no normal)
2. Mann-Whitney U test (non-parametric alternative)
3. Bonferroni correction (multiply p-value by 8, the number of genes tested)
Reporta si la significancia survive Bonferroni.

## Cuestión 3: Proxy validity
Verifica:
- ¿IL-6 plasma→CSF correlation está establecida en FM?
- ¿LGALS3BP discordancia es reproducible o artefacto del dataset?
- ¿El claim de "validated" es fuerte para AUC=0.66?

Instrucciones: Busca papers en PubMed sobre plasma↔CSF correlation para IL-6 y LGALS3BP específicamente en Fibromyalgia (no solo neuroinflammation general). Reporta:
- Correlation coefficient (r) if found
- p-value
- Whether n<30 (underpowered)

## Cuestión 4: LGALS3BP discordancia
Verifica:
- El finding de LGALS3BP: CSF↑ (Khoonsari 2019) vs PBMC↓ (GSE221921, FC=0.75)
- ¿Podría ser un artefacto de platform (proteoma vs transcriptoma)?
- ¿LGALS3BP mRNA↔protein correlation conocida?

Instrucciones: Usa web_search para encontrar evidence sobre:
1. LGALS3BP mRNA↔protein correlation
2. LGALS3BP en PBMCs de FM (no CSF)
Reporta si la discordancia es plausiblest o un artefacto de assay platform mismatch.

## Cuestión 5: Biological plausibility
Verifica:
- ¿IL-6 elebando FC=1.66 en PBMCs justify claim de "systemic inflammation" en FM?
- ¿PENK FC=1.38 (trend NS) justifica inclusión como proxy?

Instrucciones: Extrae IL6 y PENK de GSE221921. Calcula effect size (Cohen's d), ICC (intra-class correlation) entre los 5 folds de CV. Evalúa si el effect size es "small" (d<0.5), "medium" (d=0.5-0.8), or "large" (d>0.8). Reporta.

---

## Report format
```
# Adversarial Verification Report
## Summary
- Issues found: N
- Validity concerns: [list]
- Recommendations: [list]

## Q1: [answer]
## Q2: [answer]
## Q3: [answer]
## Q4: [answer]
## Q5: [answer]
```

---

## Constraints
- Usa GSE221921 dataset (local en /tmp/GSE221921_FM_ProcessedData.xlsx)
- Usa web_search para PubMed si necesario
- No ejecutes código que tome más de 3 minutos
- NO modifiques los archivos originales
- Reporta en formato markdown
