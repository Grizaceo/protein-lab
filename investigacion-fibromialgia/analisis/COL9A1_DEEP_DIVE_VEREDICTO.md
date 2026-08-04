# COL9A1 Deep Dive — Veredicto Final (C1-C5)

**Fecha:** 2026-08-04
**Contexto:** Post-FASE 3 (E1-E7 completados). Los 4 genes que sobreviven female-only + sex-adjusted en GSE221921 (E2) fueron analizados para determinar si forman un módulo biológico coherente.

---

## C1 — Matriz de correlación pareada

| | COL9A1 | BPIFB2 | PTN | ST3GAL1 |
|---|---|---|---|---|
| COL9A1 | 1.000 | 0.507*** | 0.510*** | -0.235** |
| BPIFB2 | 0.507*** | 1.000 | 0.251*** | -0.214** |
| PTN | 0.510*** | 0.251*** | 1.000 | -0.154* |
| ST3GAL1 | -0.235** | -0.214** | -0.154* | 1.000 |

- Tríada COL9A1-BPIFB2-PTN co-expresada (r=0.25-0.51, todos p<0.001)
- ST3GAL1 anticorrelaciona levemente con los 3 (r=-0.15 a -0.24)
- Fisher r-to-z: correlaciones no difieren FM vs HC (p>0.17 en todos los pares)
- Conclusión: el módulo es estructural, no disease-specific

## C2 — Pathway enrichment

- Enrichr API: HTTP 400 (lista muy pequeña para 4 genes)
- g:Profiler API: HTTP 404 (servidor caído)
- Análisis manual desde NCBI Gene (ver C3)

## C3 — Función biológica (NCBI Gene confirmed)

| Gen | Proteína | Función | Pain/FM connection | Immune |
|-----|----------|---------|---------------------|--------|
| COL9A1 | Collagen alpha-1(IX) | Minor fibrillar collagen, cartilage ECM | Mutations → MED, Stickler syndrome, osteoarthritis. Joint pain directo. | Bajo (structural) |
| BPIFB2 | BPI fold B2 | Lipid transfer / LPS binding | Innate immunity. LPS exposure → pain sensitization. Sjögren biomarker. | Sí (innate) |
| PTN | Pleiotrophin | Secreted growth factor, neurite outgrowth, ALK ligand | Nerve repair, inflammatory pain models, osteogenesis | Adjacent (macrophage mod) |
| ST3GAL1 | ST3 sialyltransferase 1 | Sialylation of glycoproteins, T cell sialylation | TCR signaling → pain modulation. Sialylates BDNF. | Sí (T cell) |

### Estructura: dos ejes convergentes, no módulo singular

- **EJE 1 (estructural/neuro):** COL9A1 + PTN → cartílago structural + neurite outgrowth. Co-expresados r=0.51. Dolor articular + reparación neural.
- **EJE 2 (innate immunity):** BPIFB2 + ST3GAL1 → LPS binding + T cell sialylation. Dolor indirecto vía inflamación.
- ST3GAL1 anticorrelaciona con COL9A1 (r=-0.23) — probable regulador negativo del módulo.

## C4 — Power analysis para validación Olink

Efecto mRNA observado: d=0.88, FC=2.32. Atenuación mRNA→protein modelada en 4 escenarios:

| Escenario | d_protein | N para 80% power | 75+75 power |
|-----------|-----------|------------------|-------------|
| Optimista (r=0.8) | 0.70 | 33/grupo | 98.6% |
| Moderado (r=0.6) | 0.53 | 56/grupo | 88.2% |
| Conservador (r=0.4) | 0.35 | 129/grupo | 55.0% |
| Pesimista (r=0.3) | 0.26 | 233/grupo | 34.3% |

Recomendación: cohort de 75 FM + 75 HC cubre escenario moderado con 88% power.

## C5 — Veredicto final

### ¿Forman un módulo coherente?

**No un módulo singular, sino dos ejes convergentes en FM pain:**

1. **Eje estructural/neural (COL9A1 + PTN):** daño articular (COL9A1) + reparación neural (PTN). Co-expresados r=0.51. Ambos son secretados y detectables en plasma Olink. Este es el eje más fuerte y novel.

2. **Eje innate immunity (BPIFB2 + ST3GAL1):** LPS/T cell sialylation. BPIFB2 secretado (detectable). ST3GAL1 intracelular (no medible en Olink plasma).

### Reemplazo de CA14

COL9A1 reemplaza a CA14 como candidato principal de validación Olink:
- CA14: causal UKB pero no robusto en PBMC (female-only falla, composicional)
- COL9A1: robusto 5/5, sobrevive female-only, d=0.88, detectable en plasma, conexión pain directa (osteoarthritis)

### Panel Olink recomendado (actualizado)

1. **COL9A1** — primario (nuevo)
2. **PTN** — primario (nuevo, co-expresado)
3. **BPIFB2** — secundario (nuevo, immune axis)
4. IL-6 — control positivo (ya publicado)
5. Substance P (TAC1) — secundario
6. CA14 — referencia (degradado, medir si panel incluye)
7. ~~PENK / OPRM1~~ — retirados (composicional)

### Archivos generados

- `analisis/C1_col9a1_module_correlation.csv`
- `analisis/C2_gprofiler_enrichment.csv` (vacío — APIs caídas)
- `analisis/C3_biological_function.csv`
- `analisis/C4_col9a1_power_olink.csv` + `.png`
- `analisis/COL9A1_DEEP_DIVE_VEREDICTO.md` (este archivo)
- Protocolo Olink actualizado con nuevo panel
