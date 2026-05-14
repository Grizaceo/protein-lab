# Análisis Ruta B v2 — Panel Focalizado (180 experimentos)

Fecha: 2026-05-14 13:25
Run: `automated_lab/results/fibromialgia_ruta_b_v2_20260514_132237`

## Veredicto corto

El panel v2 confirma lo que sospechábamos: **MOR tiene sesgo de modelo.** No es biología — es un artefacto de MAMMAL para GPCRs. La evidencia es brutal: atorvastatin, una estatina que nunca ha mostrado actividad opioide, obtiene pKd=7.165 en MOR — más alto que el 80% de los controles positivos opioides.

## 1. Sesgo MOR confirmado

30 fármacos en MOR tienen media pKd=6.928 y SD=0.104. Eso significa que **casi todos los fármacos — opioides, antiinflamatorios, estatinas, PPIs — caen en [6.77, 7.21].** Es una banda increíblemente estrecha para moléculas tan diversas.

Controles positivos (opioides reales) vs negativos (sin actividad MOR conocida):

| Droga | Clase | MOR pKd | ¿Esperado? |
|---|---|---|---|
| buprenorphine | MOR partial agonist | 7.113 | ✅ Sí |
| fentanyl | MOR agonist | 6.945 | ✅ Sí |
| methadone | MOR agonist | 6.928 | ✅ Sí |
| naloxone | MOR antagonist | 6.915 | ✅ Sí |
| naltrexone | MOR antagonist | 6.844 | ✅ Sí |
| morphine | MOR agonist | 6.818 | ✅ Sí |
| **atorvastatin** | **statina** | **7.165** | ❌ **NO** |
| **celecoxib** | **COX-2** | **6.973** | ❌ **NO** |
| **prednisone** | **corticosteroide** | **6.973** | ❌ **NO** |
| omeprazole | PPI | 6.883 | ❌ NO |
| melatonin | hormona | 6.877 | ❌ NO |
| ibuprofen | NSAID | 6.840 | ❌ NO |
| metformin | biguanide | 6.810 | ❌ NO |

**Atorvastatin > morphine en MOR. Eso no es farmacología — es ruido del modelo.**

## 2. Ranking por target

| Target | Media pKd | SD | ≥7.0 | ≥6.5 |
|---|---|---|---|---|
| MOR | 6.928 | 0.104 | 5 | 30 |
| MS4A2 | 6.228 | 0.077 | 0 | 0 |
| HDC | 5.957 | 0.100 | 0 | 0 |
| NRF2 | 5.942 | 0.074 | 0 | 0 |
| TLR4 | 5.896 | 0.143 | 0 | 0 |
| TRPA1 | 5.762 | 0.100 | 0 | 0 |

MOR separa +0.70 pKd del segundo target. Ningún otro target tiene un solo compuesto ≥6.5.

## 3. MS4A2: segunda señal pero con asteriscos

Todos los fármacos tienen su mejor pKd non-MOR en MS4A2 — sin excepción. Eso también huele a sesgo, aunque más débil que MOR. Posiblemente MAMMAL asigna afinidad basal más alta a ciertos folds/estructuras de proteína (GPCRs, tetraspaninas, ciertos canales) independientemente del ligando.

MS4A2 como "mast-cell target" en fibromialgia tiene plausibilidad biológica, pero con este nivel de ruido no podemos afirmar señal específica.

## 4. Qué SÍ podemos concluir

- Naltrexona/MOR **se recupera** consistente: pKd ~6.84-6.91 en múltiples runs.
- La afinidad de naltrexona por MOR es moderada (~120-150 nM predicha), dentro del rango de LDN oral.
- **El modelo MAMMAL no distingue controles positivos de negativos para GPCRs.** MOR es el caso extremo, pero MS4A2 también muestra inflación basal.
- Los targets no-GPCR no-MOR (HDC, NRF2, TLR4, TRPA1) tienen varianza baja y medias bajas, lo cual es más creíble como "poco binding general" que como screening útil.

## 5. Qué NO podemos concluir

- No podemos decir que atorvastatin, celecoxib o prednisone "pegan a MOR" — es casi seguro ruido del modelo.
- No podemos usar pKd de MAMMAL en MOR como ranking de afinidad real para ningún fármaco que no sea opioide canónico.
- No podemos afirmar señal específica en MS4A2 sin decoys y controles de fold/GPCR.

## 6. Próximo paso

**Ruta B v3: controles de especificidad.** Panel de 3-4 GPCRs no relacionados + MOR + MS4A2 + 2 negative-control proteins (ej. GFP o secuencia scrambled). Si MOR y otros GPCRs muestran la misma inflación, confirmamos el sesgo de fold. Si MOR es único en su inflación, hay algo más específico.

La Ruta B v2 cumplió su propósito: **falsar la especificidad del modelo.** Ahora sabemos que MAMMAL DTI no sirve para rankear afinidad MOR sin un filtro de GPCR-bias. Bien invertido.
