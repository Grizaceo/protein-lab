# AUDITORÍA — literatura/adicional_grounding

**Fecha:** 2026-05-13  
**Carpeta auditada:** `investigacion-fibromialgia/literatura/adicional_grounding/`  
**Criterio aplicado:** si un paper/claim no tiene identificador resoluble y evidencia local suficiente, no se usa para enriquecer rutas. Si tiene identificador pero no full-text local, queda como `metadata-only / usable con cautela`. Si el título/DOI/PMID está cruzado o no corresponde, queda como `alucinación o error`.

---

## 1. Inventario de problemas encontrados

### Archivos basura o incompletos

- `Krock_et_al_2023_SGC.pdf`: archivo vacío, 0 bytes. No sirve como paper local.
- `Sanchez_et_al_2025_MRGPRX2.pdf`: no era PDF; era página HTML de Cloudflare. No sirve como paper local.

Ambos quedan reemplazados por verificación vía PubMed/bioRxiv/metadata donde corresponda, pero NO cuentan como PDF descargado.

---

## 2. Papers/identificadores verificados

Se creó `verified/PUBMED_VERIFICATION_TABLE.md` usando NCBI E-utilities, y `verified/fulltext_xml/` con JATS XML para artículos PMC disponibles.

### Full-text local verificable vía PMC/JATS XML

Estos sí quedan como papers locales en formato XML oficial, aunque no PDF:

| Paper | ID local | Estado |
|---|---|---|
| Jones et al. 2016, *Genome-wide expression profiling in peripheral blood of patients with fibromyalgia* | PMID 27157394 / PMC4888802 | VALIDADO, fulltext XML local |
| Ang et al. 2015, *Ketotifen in Fibromyalgia* | PMID 25370135 / PMC4417653 | VALIDADO, fulltext XML local |
| Goebel et al. 2021, *Passive transfer of fibromyalgia symptoms from patients to mice* | PMID 34196305 / PMC8245181 | VALIDADO, fulltext XML local |
| Younger et al. 2009, LDN pilot | PMID 19453963 / PMC2891387 | VALIDADO, fulltext XML local |
| Theoharides et al. 2019, *Mast Cells, Neuroinflammation and Pain in Fibromyalgia Syndrome* | PMID 31427928 / PMC6687840 / DOI 10.3389/fncel.2019.00353 | VALIDADO, fulltext XML local |
| Atiakshin et al. 2022, CPA3 review | PMID 35159379 / PMC8834431 / DOI 10.3390/cells11030570 | VALIDADO, fulltext XML local |
| HDC review | PMID 30654600 / PMC6359378 / DOI 10.3390/ijms20020376 | VALIDADO, fulltext XML local |

### Identificador/metadata verificada, pero sin full-text local

Estos existen, pero se usan con cautela hasta tener PDF/XML/full text local:

| Paper | ID | Estado |
|---|---|---|
| Seefried et al. 2025, *Autoantibodies in patients with fibromyalgia syndrome* | PMID 39907533 / DOI 10.1097/j.pain.0000000000003535 | METADATA-ONLY |
| af Ekenstam et al. 2026, *Searching for blood biomarkers and treatment targets... anti-satellite glia cell IgG* | PMID 41271190 / DOI 10.1016/j.bbi.2025.106185 | METADATA-ONLY |
| Blanco et al. 2010, skin mastocytes | PMID 20428906 / DOI 10.1007/s10067-010-1474-7 | METADATA-ONLY |
| Krock et al. 2023, anti-SGC IgG | PMID 37683961 / DOI 10.1016/j.bbi.2023.09.003 | METADATA-ONLY |
| Naltrexone 6 mg Lancet Rheumatology trial | PMID 38258677 / DOI 10.1016/S2665-9913(23)00278-3 | METADATA-ONLY |
| LDN meta-analysis 2025 | PMID 40540205 / DOI 10.1007/s11916-025-01411-1 | METADATA-ONLY |
| Sanchez et al. 2025 bioRxiv Mrgprb2/MRGPRX2 | DOI 10.1101/2025.05.15.652596 | EXTERNO VERIFICADO, NO LOCAL; no usar como pilar fuerte bajo criterio estricto |

---

## 3. Alucinaciones / errores corregidos

### Error 1 — DOI equivocado para Jones 2016

En `CITAS_BIBLIOGRAFIA.md` se decía:

> DOI: 10.1111/jcmm.12782

Eso NO corresponde al paper Jones/GSE67311. El paper correcto está en PubMed/PMC como:

- PMID 27157394
- PMC4888802
- título: *Genome-wide expression profiling in the peripheral blood of patients with fibromyalgia*

**Acción:** el DOI `10.1111/jcmm.12782` queda descartado para Jones/GSE67311.

### Error 2 — Sánchez con DOI cruzado en DOWNLOAD_LIST

En `DOWNLOAD_LIST.md` aparece `10.1101/2025.01.24.634685v1`, pero ese DOI corresponde a un preprint ecológico no relacionado con fibromialgia.

El DOI correcto para Sanchez/Mrgprb2 es:

- `10.1101/2025.05.15.652596v1`

**Acción:** el DOI `10.1101/2025.01.24.634685v1` queda marcado como alucinación/error de grounding.

### Error 3 — Seefried 2025 título exagerado

El archivo local decía:

> Autoantibody binding to dorsal root ganglion neurons defines clinical subsets in fibromyalgia

El paper verificado por PubMed se llama:

> Autoantibodies in patients with fibromyalgia syndrome

PMID 39907533. El contenido sobre clusters/surface binding puede existir en el abstract o full text, pero no hay full text local todavía. No usar esos detalles como hechos fuertes hasta conseguir el paper.

### Error 4 — Theoharides 2024 / PMID 39451237

`CITAS_BIBLIOGRAFIA.md` decía que PMID 39451237 correspondía a “Mast cells and neuroinflammation in chronic pain syndromes”. PubMed muestra que PMID 39451237 corresponde a otro paper:

> Association Between Systemic Neuroinflammation, Pain Perception and Clinical Status in Fibromyalgia Patients: Cross-Sectional Study

Por tanto, ese ítem está cruzado. Para mastocitos/FM usar el paper validado:

- Theoharides et al. 2019
- PMID 31427928
- PMC6687840
- DOI 10.3389/fncel.2019.00353

### Error 5 — claims mecanísticos demasiado fuertes sobre DYRK3/RGS17

`ARTEFACTO_GROUNDING_EXPANDIDO.md` afirma:

- DYRK3 promueve degranulación de mastocitos downstream de receptores Fc.
- RGS17 modula neuroinflamación inducida por TNF-alpha.

En esta auditoría no hay paper local verificado que sostenga esos mecanismos específicos en FM. Pueden quedar como hipótesis bibliográficas a verificar, pero NO como hechos.

### Error 6 — “FM redefinida como enfermedad autoinmune con base en mastocitos”

Esto es excesivo. Lo validado es:

- Hay evidencia de un componente IgG/autoinmune en modelos animales y subsets.
- Hay evidencia/hypótesis seria de participación de mastocitos.
- No hay consenso de que toda FM sea enfermedad autoinmune mastocitaria.

---

## 4. Claims que sobreviven

### Sólidos

- GSE67311/Jones 2016 existe y es el dataset original de sangre completa.
- Nuestro análisis local de GSE67311 confirma CPA3/MS4A2/FCER1A/HDC down en sangre completa.
- Goebel 2021 muestra transferencia pasiva de síntomas FM por IgG a ratones; fulltext local PMC.
- Theoharides 2019 es una hipótesis publicada de mastocitos/neuroinflamación/dolor en FM; fulltext local PMC.
- Ang 2015 ketotifen trial fue negativo; fulltext local PMC.
- Younger 2009 LDN pilot existe; fulltext local PMC.

### Cautela

- Blanco 2010 reporta más mastocitos en biopsias de piel FM, pero por ahora solo metadata/abstract local.
- Krock 2023 anti-SGC IgG existe, pero por ahora solo metadata/abstract local.
- Seefried 2025 autoantibodies existe, pero por ahora solo metadata/abstract local.
- af Ekenstam 2026 CD40/anti-SGC existe, pero por ahora solo metadata/abstract local.
- Sanchez 2025 Mrgprb2/MRGPRX2 existe y fue legible externamente, pero no hay full text local limpio; bajo criterio estricto queda fuera como pilar fuerte.

---

## 5. Regla operativa

Desde ahora, `ARTEFACTO_GROUNDING_EXPANDIDO.md`, `RESUMEN_GROUNDING_2025.md`, `CITAS_BIBLIOGRAFIA.md` y `DOWNLOAD_LIST.md` son historial contaminado. Para rutas futuras usar:

1. Este archivo.
2. `verified/PUBMED_VERIFICATION_TABLE.md`.
3. `verified/PUBMED_MOR_LDN_TABLE.md`.
4. `verified/fulltext_xml/*.xml`.
5. `CHECKPOINT_AUDITADO_2026-05-13.md`.
