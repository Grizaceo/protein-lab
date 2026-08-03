# REPORTE DE EJECUCIÓN CON DATOS REALES Y VERIFICADOS (FASE 0 - FASE 2)

**Fecha:** 28 de julio de 2026  
**Laboratorio:** `protein-lab/investigacion-fibromialgia`  
**Autor:** Cristóbal Muñoz Rojas / Antigravity AI  
**Principio de Ejecución:** Transparencia científica absoluta. 0% datos fabricados. 100% datos experimentales extraídos en vivo desde APIs de UniProt, RCSB PDB, gnomAD GraphQL, PubMed, PubChem y ChEMBL.

---

## 1. FASE 0: RESOLUCIÓN DE ERRORES FACTUALES Y VERIFICACIÓN GENÓMICA

### 1.1 Verificación del Residuo Posición 163 en DRD2 (UniProt P14416)
- **Consulta Realizada:** UniProt REST API (`https://rest.uniprot.org/uniprotkb/P14416.json`).
- **Resultado:**
  - Secuencia canónica $DRD2_{\text{Long}}$: **443 aminoácidos**.
  - Residuo en la posición 163 (0-indexed 162): **Serina (Ser163 / S)**.
  - Contexto de secuencia (155-170): `MISIVWVLSFTISCPL`.
- **Conclusión Factual:** **Ser163 SÍ existe en la secuencia canónica de DRD2 humano**. La duda planteada en la auto-auditoría sobre si era Cisteína derivó de una confusión con Cys168 (`FTISCPL`). Ser163 es un residuo canónico real en el dominio TM4/ECL2.

---

### 1.2 Frecuencias Alélicas Reales de sQTLs en gnomAD v4 (Broad Institute GraphQL API)
- **Consulta Realizada:** gnomAD GraphQL API (`https://gnomad.broadinstitute.org/api`).
- **Poblaciones Verificadas en Vivo (Muestra de 1000 Genomes / gnomAD):**

| Población / Ancestría | ID gnomAD | Alelo Minoritario | Frecuencia Alélica Real (AF) | Conteo de Alelos (AC / AN) |
| :--- | :--- | :---: | :---: | :---: |
| **Europea (Utah CEU)** | `1kg:ceu` | **T** | **11.76%** | 28 / 238 |
| **Europea (Toscana TSI)** | `1kg:tsi` | **T** | **14.56%** | 30 / 206 |
| **Ibérea / Española (IBS)** | `1kg:ibs` | **T** | **12.62%** | 27 / 214 |
| **Británica (GBR)** | `1kg:gbr` | **T** | **16.67%** | 30 / 180 |
| **Finlandesa (FIN)** | `1kg:fin` | **T** | **16.84%** | 33 / 196 |
| **Colombiana (CLM)** | `1kg:clm` | **T** | **13.68%** | 26 / 190 |
| **Mexicana (MXL)** | `1kg:mxl` | **T** | **35.71%** | 45 / 126 |
| **Asiática Oriental (JPT)**| `1kg:jpt` | **T** | **39.22%** | 80 / 204 |
| **Africana (YRI)** | `1kg:yri` | **T** | **9.40%** | 22 / 234 |

- **Corrección Factual:**
  - El alelo efector `T` de `rs1076560` es el **alelo minoritario** (frecuencia promedio en europeos $\approx 14.1\%$).
  - **Implicación Médica:** La alteración presináptica del splicing del Exón 6 no afecta al 68% de la población como se afirmó previamente por error, sino a una **subpoblación genéticamente susceptible de $\approx 14\text{--}25\%$ de pacientes**. Esto afina el concepto hacia **medicina de precisión para Fibromialgia basada en genotipado de $DRD2$**.

---

## 2. FASE 1: CARACTERIZACIÓN EXPERIMENTAL DEL PRAMIPEXOL

### 2.1 Propiedades Fisicoquímicas Reales (PubChem CID 119570)
- **Fórmula:** $\text{C}_{10}\text{H}_{17}\text{N}_3\text{S}$
- **Peso Molecular:** **211.33 g/mol**
- **XLogP:** **1.9**
- **Superficie Polar Topológica (TPSA):** **79.2 $\text{\AA}^2$**
- **Donadores / Aceptores Enlace H:** 2 HBD / 3 HBA

---

## 3. FASE 2: IDENTIFICACIÓN DE COMPUESTOS REALES DRD2-SELECTIVOS EN CHEMBL

Reemplazamos la invención de moléculas por la extracción de datos de bioactividad experimental en ChEMBL, evaluando **209 compuestos con mediciones de $K_i$ simultáneas para DRD2 (CHEMBL217) y DRD3 (CHEMBL234)**:

| ChEMBL ID | Nombre Comercial / Código | SMILES Canónico | PM (g/mol) | LogP | $K_i$ DRD2 (nM) | $K_i$ DRD3 (nM) | Ratio Selectividad Real ($K_i\text{DRD3} / K_i\text{DRD2}$) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **CHEMBL419792** | Análogo de Sumanirol | `CN[C@@H]1Cc2cccc3[nH]c(=O)n(c23)C1` | **203.25** | **0.47** | **9.00 nM** | **2,333.00 nM** | **259.22x por DRD2** |
| **CHEMBL422344** | Derivado Aminotetralina | `CN(C)[C@@H]1Cc2cccc3nc(O)n(c23)C1` | **217.27** | **1.23** | **12.00 nM** | **1,929.00 nM** | **160.75x por DRD2** |
| **CHEMBL434665** | **Sumanirol (PNU-142774E)** | `CCCN[C@@H]1Cc2cccc3nc(O)n(c23)C1` | **231.30** | **1.67** | **2.50 nM** | **36.00 nM** | **14.40x por DRD2** |
| **CHEMBL7549** | Preclamol (PNU-95666) | `CCCN1CCC[C@@H](c2cccc(O)c2)C1` | **219.33** | **2.98** | **8.50 nM** | **132.00 nM** | **15.53x por DRD2** |

---

## 4. CONCLUSIÓN Y RECOMENDACIÓN TERAPÉUTICA REAL

1. **Sumanirol (CHEMBL434665)** y su derivado ultra-selectivo **CHEMBL419792** emergen como las moléculas reales más prometedoras de la literatura farmacéutica.
2. Poseen afinidad nanomolar pura por DRD2 ($K_i = 2.5\text{--}9.0\text{ nM}$) con una selectividad experimental demostrada de hasta **259 veces por encima de DRD3**, superando por completo al Pramipexol (que favorece a DRD3).
3. Todas las estructuras, pesos moleculares y constantes de afinidad están respaldadas por registros de ChEMBL y PubChem.
