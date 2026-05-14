# EXPERIMENTO 2: ESM2 Embeddings — Caracterización Estructural de Targets FM
## Documentación de resultados

**Fecha:** 2026-05-13
**Modelo:** ESM2 650M (esm2_t33_650M_UR50D)
**Embedding dim:** 1280
**GPU:** RTX 4060, VRAM desde 7.4 GB → 1.2 GB libre tras carga del modelo
**Tiempo total:** ~4 segundos para 11 proteínas
**Archivo:** target_embeddings.json

---

## MATRIZ DE SIMILITUD DE COSENO

```
                         CPA3  FceRIα   HDC  IL1B   IL6   MOR  FceRIβ  NRF2 Nav1.8  TLR4 TRPA1
CPA3                       --   .852   .937  .926  .901  .608   .893  .893   .915  .934  .941
FCER1A/FceRIα            .852     --   .902  .909  .924  .750   .927  .899   .896  .922  .908
HDC                      .937   .902     --  .966  .951  .677   .943  .954   .957  .963  .963
IL-1β                    .926   .909   .966    --  .965  .634   .950  .965   .951  .963  .951
IL-6                     .901   .924   .951  .965    --  .662   .958  .961   .947  .955  .936
MOR                      .608   .750   .677  .634  .662    --   .686  .661   .718  .674  .703
MS4A2/FceRIβ             .893   .927   .943  .950  .958  .686     --  .943   .943  .947  .937
NRF2                     .893   .899   .954  .965  .961  .661   .943    --   .956  .943  .930
Nav1.8                   .915   .896   .957  .951  .947  .718   .943  .956     --  .952  .952
TLR4                     .934   .922   .963  .963  .955  .674   .947  .943   .952    --  .965
TRPA1                    .941   .908   .963  .951  .936  .703   .937  .930   .952  .965    --
```

---

## INTERPRETACIÓN

### Hallazgo 1: MOR es el outlier estructural

MOR (mu opioid receptor) tiene similitudes de coseno **0.61-0.75** con todos los demás targets, mientras que el resto de la matriz oscila entre **0.85-0.97**.

**Explicación:** MOR es un GPCR (receptor acoplado a proteína G) con una topología de 7 hélices transmembrana muy distinta a los demás targets. Los demás son enzimas (CPA3, HDC, NRF2), citocinas (IL-1β, IL-6), canales iónicos (Nav1.8, TRPA1), receptores de membrana más complejos (TLR4, FcεRI). ESM2 captura esta diferencia fundamental.

**Implicación para FM:** MOR es el target de la low-dose naltrexone (LDN), que es el único fármaco Tier 2 con evidencia positiva en meta-análisis de FM. Su singularidad estructural podría explicar por qué LDN funciona cuando otros fármacos fallan — está targeteando un espacio conformacional diferente.

### Hallazgo 2: Los mastocitos no forman un cluster separado

CPA3, MS4A2, FCER1A y HDC NO están más cerca entre sí que del resto. CPA3 es más similar a TRPA1 (0.941) que a FCER1A (0.852). HDC es más similar a IL-1β/NRF2 (~0.96) que a CPA3 (0.937).

**Explicación:** ESM2 con mean pooling sobre toda la secuencia captura propiedades *globales* de la proteína (composición aminoacídica, longitud, plegamiento general), NO las características *locales* que definen la función específica (sitio activo de CPA3 vs sitio de unión de IgE de FcεRIα).

**Implicación metodológica:** Necesitamos embeddings **per-residuo**, no mean pooling, para identificar pockets de binding funcionales.

### Hallazgo 3: Alta similitud general — ¿señal o ruido?

La mayoría de las similitudes están en 0.85-0.97. Esto podría ser:
- **(a)** Real: proteínas humanas comparten propiedades fisicoquímicas capturadas por ESM2
- **(b)** Limitación de ESM2: el mean pooling produce embeddings "promediados" que pierden especificidad
- **(c)** Sesgo de longitud: proteínas más cortas (IL-6, 212 aa) vs largas (Nav1.8, 1956 aa) podrían sesgar

La respuesta más probable es **(a)+(b)**: ESM2 captura propiedades globales reales pero el mean pooling diluye las señales locales específicas de cada target.

### Hallazgo 4: Los pares más cercanos tienen sentido funcional

| Par | Similitud | ¿Tiene sentido biológico? |
|-----|-----------|--------------------------|
| TLR4 ↔ TRPA1 | 0.965 | Ambos son canales/receptores de membrana con dominios LRR/ankyrin |
| IL-1β ↔ NRF2 | 0.965 | Ambos son proteínas de respuesta a estrés/inflamación |
| HDC ↔ IL-1β | 0.966 | Sin relación funcional obvia — probablemente artefacto de mean pooling |
| HDC ↔ NRF2 | 0.954 | Igual que arriba |
| MOR ↔ cualquiera | 0.60-0.75 | Consistente con su unicidad estructural |

---

## PRÓXIMOS PASOS

### Paso 3a: Embeddings per-residuo (pendiente para Kaggle/Colab)
Generar embeddings por posición aminoacídica (no mean pooling) para mapear:
- Pockets de binding en NRF2, Nav1.8, TLR4
- Regiones transmembrana vs extracelulares en canales iónicos
- Sitios activos de CPA3 y HDC

### Paso 3b: Estructuras PDB (local)
Cada target tiene estructura conocida:
- NRF2: múltiples PDB del dominio bZip
- Nav1.8: PDB 6J8E, 7WE4 (canal completo)
- TLR4: PDB 3FXI, 4G8A (complejo con MD-2)
- TRPA1: PDB 3J9P, 6PQQ
- MOR: PDB 4DKL, 5C1M
- IL-1β: PDB 1I1B, 2NVH
- IL-6: PDB 1ALU, 1IL6

### Paso 3c: Docking (Colab/Kaggle si se necesita)
Para targets con fármacos aprobados (NRF2→DMF, Nav1.8→suzetrigine, MOR→LDN):
- Docking del fármaco conocido en la estructura PDB
- Comparar con docking de nuevos candidatos

---

## ARCHIVOS GENERADOS
- `target_sequences.fasta` — 11 secuencias de UniProt
- `target_embeddings.json` — embeddings ESM2 + matriz de similitud (1.5 MB)
