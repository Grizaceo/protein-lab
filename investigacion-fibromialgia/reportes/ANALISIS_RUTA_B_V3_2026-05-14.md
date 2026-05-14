# Análisis Ruta B v3 — Calibración de Sesgo GPCR

Fecha: 2026-05-14 13:40
Run: `automated_lab/results/fibromialgia_ruta_b_v3_20260514_133507`

## Veredicto

**MAMMAL DTI tiene un sesgo estructural de fold para GPCR Class A. El pKd absoluto en GPCRs no es informativo sin calibración.** La Ruta B v3 lo demuestra con 4 GPCRs no-relacionados que rankean 15 fármacos diversos en orden casi idéntico (r=0.926-0.990 entre targets). La conclusión de v2 se confirma y se cuantifica.

## 1. El sesgo en números

| Target | Clase | Media pKd | SD | ≥6.5 |
|---|---|---|---|---|
| MOR | GPCR Class A (opioide) | 6.907 | 0.102 | 15/15 |
| DRD2 | GPCR Class A (dopamina) | 6.289 | 0.097 | 1/15 |
| MS4A2 | Tetraspanina (semi-GPCR) | 6.218 | 0.091 | 0/15 |
| ADRB2 | GPCR Class A (adrenérgico) | 6.100 | 0.090 | 0/15 |
| AGTR1 | GPCR Class A (angiotensina) | 6.080 | 0.102 | 0/15 |
| GFP | GFP (Aequorea, β-barrel) | 5.840 | 0.177 | 0/15 |
| **ALB** | **Albúmina sérica humana** | **5.050** | **0.115** | **0/15** |

Delta GPCR Class A (4 targets) − ALB = +1.294 pKd
Delta GPCR Class A − nonGPCR (MS4A2+ALB+GFP) = +0.641 pKd

**Interpretación:** cada fármaco recibe ~0.9-1.3 pKd de "bono" automático solo por ser evaluado contra un GPCR. Esto no es afinidad — es ruido estructural del embedding.

## 2. Correlación entre GPCRs: la firma del sesgo

| r | MOR | ADRB2 | DRD2 | AGTR1 |
|---|---|---|---|---|
| MOR | 1.000 | 0.955 | 0.936 | 0.944 |
| ADRB2 | 0.955 | 1.000 | 0.935 | 0.990 |
| DRD2 | 0.936 | 0.935 | 1.000 | 0.926 |
| AGTR1 | 0.944 | 0.990 | 0.926 | 1.000 |

Cuatro GPCRs con farmacología completamente distinta (opioide, adrenérgico, dopaminérgico, angiotensinérgico) rankean 15 fármacos en orden casi idéntico. La probabilidad de que esto sea biología y no sesgo es esencialmente cero.

## 3. El bono GPCR es uniforme por fármaco

Todos los fármacos — opioides, estatinas, PPIs, AINEs — muestran Δ(GPCR−nonGPCR) consistente:

| Fármaco | Δ | ¿Opioide real? |
|---|---|---|
| omeprazole | +0.959 | No |
| fentanyl | +0.955 | Sí |
| melatonin | +0.946 | No |
| ibuprofen | +0.934 | No |
| pregabalin | +0.923 | No |
| duloxetine | +0.925 | No (SNRI) |
| aspirin | +0.924 | No |
| gabapentin | +0.911 | No |
| naloxone | +0.907 | Sí |
| morphine | +0.896 | Sí |
| naltrexone | +0.895 | Sí |
| metformin | +0.880 | No |
| celecoxib | +0.884 | No |
| buprenorphine | +0.808 | Sí |
| atorvastatin | +0.741 | No |

El delta es remarcablemente constante: todos reciben entre +0.74 y +0.96. El modelo no distingue — solo recompensa el fold.

## 4. Lectura corregida de la afinidad MOR de naltrexona

Si corregimos naltrexona→MOR (pKd=6.844) por el delta promedio GPCR→nonGPCR (~0.9), la afinidad "real" estimada sería:

```
pKd_corregido ≈ 6.84 − 0.9 = 5.94 → Kd ≈ 1.1 µM
```

Esto es mucho más compatible con la farmacología conocida de LDN (low-dose naltrexone, 1.5-4.5 mg/día), donde las concentraciones plasmáticas están en rango nM-bajo pero el mecanismo no es ocupación MOR canónica.

## 5. Lecciones sobre cada target control

- **ALB (pKd=5.05):** el piso real. Albúmina une drogas de verdad, y MAMMAL le asigna afinidad baja. Esto es creíble.
- **GFP (pKd=5.84):** sorprendentemente alto para una proteína inerte no-humana. Sugiere que el piso de ruido de MAMMAL es ≈5.7-5.9 para cualquier proteína con estructura definida. No es específico de mamíferos ni de función.
- **MS4A2 (pKd=6.22):** significativamente sobre ALB pero bajo los GPCRs puros. ¿Señal real débil o semi-GPCR-like por ser proteína de membrana? Imposible distinguir sin más controles de membrana no-GPCR.
- **ADRB2/DRD2/AGTR1 (6.08-6.29):** todos muestran el mismo patrón de inflación. Ninguno debería interpretarse como "off-target" real sin evidencia ortogonal.

## 6. Diagnóstico final del modelo

MAMMAL DTI (ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd):

- **Útil para:** ranking de afinidad relativa DENTRO de un mismo fold (ej. comparar fármacos entre sí para un target dado).
- **No útil para:** comparar afinidad absoluta entre targets de distinto fold, especialmente si uno es GPCR.
- **Requiere:** calibración por familia de proteínas. Sin ella, cualquier cribado masivo contra GPCRs devuelve ranking espurio dominado por el fold, no por el ligando.

## 7. Implicaciones para el proyecto fibromialgia

- La señal MOR/LDN **no está confirmada ni refutada** — solo sabemos que no podemos confiar en el pKd absoluto.
- La ruta mastocito/MS4A2 **tampoco puede evaluarse** con este modelo sin controles de proteínas de membrana no-GPCR.
- Para seguir, necesitamos una fuente de afinidad ortogonal: docking molecular (AutoDock Vina/DiffDock), datos de BindingDB/ChEMBL/PubChem BioAssay, o literatura de binding assays.
- MAMMAL sigue siendo útil para priorizar qué validar, pero NO como endpoint de "descubrimiento".

## 8. Próximo paso

Dejar de correr DTI masivo. La calibración ya está hecha. El próximo paso no es más experimentos MAMMAL — es cruzar los targets priorizados (MOR, MS4A2, TLR4) con evidencia externa verificable: docking, bioassays públicos, literature binding data, y los datasets GEO que ya tenemos auditados.

Ruta B v3 cumplió: calibró el instrumento. Ahora sabemos exactamente qué mide y qué no.
