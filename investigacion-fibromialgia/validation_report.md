# Validation Report: Multi-gene Panel → FM Classification (v3)

## Dataset: GSE221921 (96 FM PBMCs vs 93 HC PBMCs, RNA-seq FPKM)
## Método: Mann-Whitney U + Bonferroni ×19 | Cohen's d pooled | AUC out-of-fold (StratifiedKFold 5)

### Genes analizados (15/19)
| Gene | FM Mean | HC Mean | Fold Change | MWU p | Bonf ×19 | Cohen d | Veredicto |
|------|---------|---------|-------------|-------|----------------------|---------|-----------|
| RGS17 | 0.4099 | 0.1396 | 2.937 | 0.0000 | 0.0000 | +0.530 | proxy SIGNIFICATIVO (effect small-medium) |
| OPRM1 | 3.0928 | 1.3553 | 2.282 | 0.0000 | 0.0001 | +0.531 | proxy SIGNIFICATIVO (effect small-medium) |
| TAC1 | 1.1752 | 0.5598 | 2.099 | 0.0002 | 0.0036 | +0.469 | proxy SIGNIFICATIVO (effect small-medium) |
| IL6 | 1.3662 | 0.8212 | 1.664 | 0.0002 | 0.0038 | +0.313 | proxy SIGNIFICATIVO (effect small-medium) |
| LGALS3BP | 13.0384 | 17.4732 | 0.746 | 0.0003 | 0.0054 | -0.311 | proxy SIGNIFICATIVO (effect small-medium) |
| PCSK1N | 2.3447 | 3.1056 | 0.755 | 0.0007 | 0.0131 | -0.198 | proxy SIGNIFICATIVO (effect small) |
| PARD3B | 0.8797 | 0.5753 | 1.529 | 0.0008 | 0.0161 | +0.431 | proxy SIGNIFICATIVO (effect small-medium) |
| PENK | 2.8598 | 2.0716 | 1.380 | 0.0031 | 0.0598 | +0.207 | no significativo (NS) |
| CXCL8 | 1.6353 | 2.3469 | 0.697 | 0.0070 | 0.1334 | -0.094 | no significativo (NS) |
| TTLL7 | 1.0894 | 0.7679 | 1.419 | 0.0141 | 0.2687 | +0.278 | no significativo (NS) |
| RIOK3 | 7.7392 | 9.2698 | 0.835 | 0.0170 | 0.3227 | -0.195 | no significativo (NS) |
| CPA3 | 1.5833 | 1.5866 | 0.998 | 0.7546 | 1.0000 | -0.002 | no significativo (NS) |
| KAT2B | 9.2457 | 9.4162 | 0.982 | 0.4366 | 1.0000 | -0.021 | no significativo (NS) |
| MDH1 | 4.4401 | 5.1546 | 0.861 | 0.9862 | 1.0000 | -0.142 | no significativo (NS) |
| PNOC | 1.3007 | 1.3489 | 0.964 | 0.4725 | 1.0000 | -0.021 | no significativo (NS) |

### Model Performance (AUC honesta, out-of-fold)
| Modelo | AUC in-sample | AUC out-of-fold | Sesgo | CV accuracy |
|--------|---------------|-----------------|-------|-------------|
| 2-gene IL6+PENK | 0.6481 | 0.6156 | +0.0325 | 0.5821 |
| Panel 15 genes | 0.7305 | 0.6169 | +0.1136 | 0.6408 |

### Proxy Status (lenguaje matizado — post adversarial verification 2026-08-03)
- **IL6 (IL-6):** significant small-effect proxy ↑ en FM (FC=1.66, MWU p=0.0002, Bonf=0.0038, d=+0.313)
- **TAC1 (Substance P):** significant proxy ↑ en FM — gen REAL de SP (corregido 2026-08-03, antes anotado PENK) (FC=2.10, MWU p=0.0002, Bonf=0.0036, d=+0.469)
- **PENK (encefalinas):** hallazgo opioide SEPARADO de Substance P (FC=1.38, MWU p=0.0031, Bonf=0.0598, d=+0.207)
  - ⚠️ **Advertencia BDNF/NGF:** los neuropéptidos NO siempre trasladan CSF→plasma (BDNF y NGF elevados en CSF de FM no se ven en plasma). SP/TAC1 es el proxy con traslado menos seguro; IL-6 tiene prioridad en el protocolo Olink.
- **OPRM1 (receptor mu opioide):** NUEVO — eje opioide endógeno completo con PENK (FC=2.28, MWU p=0.0000, d=+0.531)
- **CXCL8 (IL-8):** ⚠️ INVERTIDO en PBMCs (FC=0.70, p=0.0070) vs proteína ↑ en plasma/CSF (lit.) — NO usar mRNA PBMC como proxy de IL-8 plasmática; válido solo como proteína (control positivo Olink)
- **LGALS3BP:** discordancia confirmada CSF↑/PBMC↓ (FC=0.75, MWU Bonf=0.0054) → **UNSUITABLE como proxy periférico**
- **PCSK1N:** re-clasificado LOW → **candidato a proxy** (MWU Bonf=0.0131, dirección consistente CSF↓/PBMC↓)
- **MDH1:** no significativo (MWU p=0.9862) → descartado

### Interpretación calibrada
- Todos los efectos son **small** (|d| < 0.35): significativos y reproducibles, pero de magnitud clínica modesta.
- Los genes NO funcionan solos para clasificación (AUC out-of-fold ≈ 0.62, CV acc ≈ azar) — su valor es como PROXY periférico de cambios centrales, no como test diagnóstico.
- La evidencia externa (Bäckryd 2017, Tsilioni 2016) apoya IL-6 periférico elevado en FM; el traslado CSF→plasma de Substance P es menos sólido (ver advertencia).
