# RESULTADOS PDB CORREGIDO — Targets Fibromialgia

**Fecha de corrección:** 2026-05-13  
**Motivo:** auditoría contra RCSB reveló 4 PDBs mal asignados en `RESULTADOS_PDB.md`. Este archivo supersede el análisis PDB previo.

---

## 1. Corrección crítica

Los siguientes archivos fueron movidos a `datos/pdb/rejected_misassigned/` y NO deben usarse:

| Archivo rechazado | Qué era realmente | Motivo de rechazo |
|---|---|---|
| `7OBN_NRF2.pdb` | L3 DNA ligase | No es NRF2/KEAP1 |
| `7ZYX_CPA3.pdb` | Dimeric i-motif DNA | No es CPA3 |
| `7Q5X_MS4A2.pdb` | HIF prolyl hydroxylase 2/EGLN1 | No es MS4A2 |
| `4E1M_HDC.pdb` | HIV-1 integrase | No es HDC |

Estructuras corregidas agregadas:

| Target | Archivo | Tipo | Estado |
|---|---|---|---|
| HDC | `datos/pdb/corrected/4E1O_HDC.pdb` | PDB experimental | VALIDADO |
| TRPA1 + A-967079 | `datos/pdb/corrected/6V9Y_TRPA1_A967079.pdb` | PDB experimental | VALIDADO |
| CPA3 | `datos/pdb/corrected/AF-P15088-F1_CPA3.pdb` | AlphaFold v6 | PREDICCIÓN, no experimental |
| MS4A2 | `datos/pdb/corrected/AF-Q01362-F1_MS4A2.pdb` | AlphaFold v6 | PREDICCIÓN, no experimental |

---

## 2. Estructuras experimentales útiles que sí quedan

| Target | Archivo/PDB | Verificación RCSB | Uso permitido |
|---|---|---|---|
| NRF2/KEAP1 | `6LRZ_NRF2.pdb` | Keap1 in complex with dimethyl fumarate, 1.54 Å | Modelar DMF/KEAP1/NRF2 pathway, NO NRF2 completo |
| NRF2/KEAP1 | `2FLU_NRF2.pdb` | Kelch-Neh2 complex, 1.5 Å | Interfaz Keap1-Nrf2 |
| Nav1.8 | `7WE4_Nav1.8.pdb` | Human Nav1.8 with A-803467, cryo-EM 2.7 Å | Canal Nav1.8 con bloqueador A-803467 |
| Nav1.8 | `7WFW_Nav1.8.pdb` | Apo human Nav1.8, cryo-EM 3.1 Å | Canal apo, NO suzetrigine |
| IL-1β | `1I1B_IL1B.pdb` | recombinant human IL-1β, 2.0 Å | Estructura clásica IL-1β |
| IL-1β | `2NVH_IL1B.pdb` | IL-1 cavities, 1.53 Å | Estructura IL-1β alta resolución |
| IL-1β | `4G6J_IL1B.pdb` | IL-1β + canakinumab Fab, 2.03 Å | Biologic/antibody interface |
| IL-6 | `1ALU_IL6.pdb` | human IL-6, 1.9 Å | Estructura clásica IL-6 |
| IL-6 | `1IL6_IL6.pdb` | human IL-6 NMR | NMR backup |
| IL-6 | `5FUC_IL6.pdb` | IL-6/gp80 locked antibody complex, 2.7 Å | Biologic/interface context |
| TLR4 | `3FXI_TLR4.pdb` | TLR4/MD-2/LPS complex, 3.1 Å | TLR4 extracellular LPS/MD-2 complex |
| TLR4 | `4G8A_TLR4.pdb` | TLR4 D299G/T399I + MD-2/LPS, 2.4 Å | TLR4 variant/MD-2/LPS, NO TAK-242 |
| TRPA1 | `3J9P_TRPA1.pdb` | TRPA1 cryo-EM, 4.24 Å | Canal TRPA1, baja resolución |
| TRPA1 | `6PQQ_TRPA1.pdb` | human TRPA1 C621S apo, 2.81 Å | Apo state, NO A-967079 |
| TRPA1 | `corrected/6V9Y_TRPA1_A967079.pdb` | TRPA1 bound with A-967079 | Antagonist-binding analysis |
| MOR | `4DKL_MOR.pdb` | mu-opioid receptor + morphinan antagonist, 2.8 Å | Estado antagonista |
| MOR | `5C1M_MOR.pdb` | active MOR + agonist BU72, 2.07 Å | Estado activo agonista |
| FCER1A | `1F6A_FCER1A.pdb` | human IgE-Fc bound to FcεRIα, 3.5 Å | IgE/FcεRIα interface |
| FCER1A | `1RPQ_FCER1A.pdb` | FcεRIα + tight-binding peptide, 3.0 Å | FcεRIα binding interface |
| HDC | `corrected/4E1O_HDC.pdb` | human histidine decarboxylase + histidine methyl ester | HDC active-site/inhibitor context |

---

## 3. Estructuras predichas, no experimentales

| Target | Archivo | Fuente | Uso permitido |
|---|---|---|---|
| CPA3 | `corrected/AF-P15088-F1_CPA3.pdb` | AlphaFold DB v6, UniProt P15088 | Hipótesis geométrica inicial; no docking fuerte sin validación |
| MS4A2 | `corrected/AF-Q01362-F1_MS4A2.pdb` | AlphaFold DB v6, UniProt Q01362 | Topología/visualización; no afirmar pocket experimental |

---

## 4. Druggability corregida

**Alta confianza estructural:** MOR, IL-1β, IL-6, FCER1A, HDC, NRF2/KEAP1, Nav1.8, TRPA1 con 6V9Y.

**Media confianza:** TLR4 extracellular/MD-2/LPS está bien estructurado, pero TAK-242 actúa en el dominio intracelular TIR; por tanto 3FXI/4G8A no modelan directamente TAK-242. TRPA1 6PQQ es apo; usar 6V9Y para A-967079.

**Baja confianza para docking directo:** CPA3 y MS4A2, porque lo local es AlphaFold y/o sin estructura experimental humana adecuada en esta auditoría.

---

## 5. Regla operativa

Desde este punto, ningún análisis usa los PDB rechazados. Si un script o documento referencia 7OBN como NRF2, 7ZYX como CPA3, 7Q5X como MS4A2 o 4E1M como HDC, está usando información inválida.
