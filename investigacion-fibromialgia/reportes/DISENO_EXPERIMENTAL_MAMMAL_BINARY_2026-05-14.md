# DISEÑO EXPERIMENTAL — MAMMAL Binary DTI Classification
**Fecha:** 2026-05-14 20:15
**Script:** `analisis/run_mammal_binary_drd2.py`

## Hipótesis

MAMMAL puede clasificar correctamente fármacos como binders/no-binders de DRD2 usando modo encoder-decoder con prompt `BINDING_AFFINITY_CLASS`.

## Por qué esto es diferente de lo que hicimos antes

| Antes (mal) | Ahora (correcto) |
|---|---|
| Regresión (pKd continua) | Clasificación binaria (bind/no-bind) |
| Encoder-only (`forward_encoder_only`) | Encoder-decoder (`model.generate()`) |
| Prompt `<MASK>` (escalar) | Prompt `<BINDING_AFFINITY_CLASS><SENTINEL_ID_0>` (token) |
| Fine-tuned DTI regression model | Base model (pre-entrenado en PPI classification) |
| Pregunta: "¿cuánto se une?" | Pregunta: "¿se une o no?" |

## Fundamento

El modelo base `ibm/biomed.omics.bl.sm.ma-ted-458m` fue pre-entrenado en:
- **PPI classification:** 780M pares positivos/negativos de STRING con prompt `⟨BINDING_AFFINITY_CLASS⟩⟨SENTINEL_ID_0⟩`
- La tarea de clasificación binaria de binding está en el ADN del modelo base
- El formato de prompt es idéntico al usado en TCR-epitope binding (AUROC > 0.85)

## Panel de prueba

### Positivos (binders conocidos de DRD2, n=5)
| Fármaco | Evidencia | Ki D2 |
|---|---|---|
| Dopamina | Agonista endógeno | 1.8-15,000 nM |
| Pramipexol | D3/D2 agonista, RCT+ FM | 3.9 nM |
| Ropinirol | D2/D3 agonista, abierto FM | 2.5 nM |
| Bromocriptina | Co-cristalizada en 6VMS | 0.62-110 nM |
| Cabergolina | D2 agonista ergoline | ~0.7 nM |

### Negativos (no binders, n=4)
| Fármaco | Target real |
|---|---|
| Atorvastatina | HMG-CoA reductasa |
| Ibuprofeno | COX-1/2 |
| Metformina | AMPK / Complejo I mitocondrial |
| Omeprazol | Bomba de protones gástrica |

## Métricas objetivo
- Accuracy ≥ 0.78 (mejor que random balanceado)
- Precision ≥ 0.70 (no llamar "binder" a cosas que no lo son)
- Recall ≥ 0.80 (no perder binders reales)
- AUROC ≥ 0.80 (discriminación razonable)

## Prompt exacto
```
<@TOKENIZER-TYPE=AA><BINDING_AFFINITY_CLASS><SENTINEL_ID_0>
<@TOKENIZER-TYPE=AA><MOLECULAR_ENTITY><MOLECULAR_ENTITY_GENERAL_PROTEIN>
<SEQUENCE_NATURAL_START>[DRD2_SEQUENCE]<SEQUENCE_NATURAL_END>
<@TOKENIZER-TYPE=SMILES><MOLECULAR_ENTITY><MOLECULAR_ENTITY_SMALL_MOLECULE>
<SEQUENCE_NATURAL_START>[DRUG_SMILES]<SEQUENCE_NATURAL_END>
<EOS>
```

El decoder genera `<0>` (no binder) o `<1>` (binder) en la posición `<SENTINEL_ID_0>`.

## Limitaciones declaradas
- n=9 (5 positivos, 4 negativos) — muestra pequeña, resultados preliminares
- El modelo base no fue fine-tuneado específicamente para DTI binario
- La clasificación puede verse afectada por el sesgo de training en PPI (STRING)
- Sin validación externa independiente
