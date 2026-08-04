# REVISIÓN ADVERSARIAL — 2026-08-04

**Rubric aplicada:** Investigación / Research + Research Repo Audit
**Verificador:** Cristóbal/DAVI (self-adversarial, acceso completo a archivos)

---

## 1. Verificador automático (audit_verify_claims.py)

**Resultado: 3/11 PASS estable (pre y post FASE 3)**

| Check | Veredicto | Esperado |
|-------|-----------|----------|
| Tablas 2 y 4 reproducen matriz cruda | PASS | PASS |
| Co-expresión PBMC (5 pares) reproduce | PASS | PASS |
| CA14 sobrevive female-only | FAIL | FAIL esperado (hallazgo auditoría) |
| "HC consistently weaker" | FAIL | FAIL esperado (4/10 pares contradicen) |
| >1 par difiere FM vs HC | FAIL | FAIL esperado (solo 1 par significativo) |
| 10 pares reportados sin selección | FAIL | FAIL esperado (5/10 reportados) |
| Genes sobre ruido en whole blood | FAIL | FAIL esperado (3 genes en decil inferior) |
| Keq termodinámico respetado | FAIL | FAIL esperado (3.8x desviación) |
| ΔpH sobrevive corrección | FAIL | FAIL esperado (ΔpH=0) |
| pH basal reproduce H-H | FAIL | FAIL esperado (7.83/7.21/6.76 vs 7.33) |
| Eje opioide sobrevive ajuste sexo | PASS | PASS (hallazgo genuino robusto al confusor) |

Veredicto: consistente. Los 8 FAIL son hallazgos genuinos reconocidos en el texto del preprint.

## 2. Verificación independiente de constantes numéricas

Recalculé COL9A1, BPIFB2, PTN, ST3GAL1 desde la matriz cruda GSE221921 sin usar resultados previos:

| Gen | FC reportado | FC verificado | d reportado | d verificado | Match |
|-----|-------------|---------------|------------|-------------|-------|
| COL9A1 | 2.320 | 2.320 | 0.880 | 0.880 | ✅ |
| BPIFB2 | 2.171 | 2.171 | 0.597 | 0.597 | ✅ |
| PTN | 2.910 | 2.910 | 0.609 | 0.609 | ✅ |
| ST3GAL1 | 0.765 | 0.765 | -0.229 | -0.229 | ✅ |

Constantes exactas.

## 3. HALLAZGOS ADVERSARIALES

### ISSUE-1 (SEVERIDAD ALTA): "Robust 5/5" incorrecto

**Claim dokumental:** Protocolo Olink y veredicto COL9A1 dicen "Robusto 5/5 modelos" para COL9A1, PTN y BPIFB2.

**Realidad (CSV E2):** La columna `Robust_5of5` es un CONTADOR (cuántos de 5 modelos dan p<0.05 nominal), no un booleano. Valores reales:
- COL9A1: 4/5 (falla male-only p=0.30)
- PTN: 4/5 (falla male-only p=0.60)
- BPIFB2: 4/5 (falla male-only p=0.16)
- ST3GAL1: 3/5 (falla male-only p=0.97 Y Welch p=0.12)

Ningún gen pasa 5/5. El "5/5" en la documentación es incorrecto.

**Corrección aplicada:** Cambiado a "Robusto 4/5 modelos" en protocolo y veredicto.

### ISSUE-2 (SEVERIDAD ALTA): BPIFB2 no sobrevive Bonferroni sex-adjusted

**Claim dokumental:** BPIFB2 listado como "Robusto 5/5" al mismo nivel que COL9A1 y PTN.

**Realidad:**
- COL9A1: p_adj_bonf18 = 0.000085 ✅ sobrevive
- PTN: p_adj_bonf18 = 0.020 ✅ sobrevive
- BPIFB2: p_adj_bonf18 = 0.063 ❌ NO sobrevive
- ST3GAL1: p_adj_bonf18 = 0.697 ❌ NO sobrevive

Solo 2 genes (COL9A1, PTN) sobreviven corrección múltiple Bonferroni sex-adjusted. BPIFB2 es nominal (p=0.0035) pero no Bonferroni. Reportarlo como "robusto" al mismo nivel infla el hallazgo.

**Corrección aplicada:** BPIFB2 degradado a "MEDIO — nominal no Bonferroni, candidato secundario". Panel Olink mantiene BPIFB2 pero con caveat.

### ISSUE-3 (SEVERIDAD MEDIA): ST3GAL1 mal caracterizado

**Claim dokumental:** ST3GAL1 listado entre "los 4 genes robustos" que forman el módulo.

**Realidad:**
- ST3GAL1 está DOWNREGULADO en FM (FC=0.765, d=-0.229) — dirección OPUESTA a COL9A1/PTN/BPIFB2
- Robust 3/5 no 4/5 (falla male-only p=0.97 y Welch p=0.12)
- No sobrevive Bonferroni sex-adjusted (p=0.697)
- Anticorrelaciona con la tríada (r=-0.15 a -0.24)

ST3GAL1 no es parte del módulo co-expresado — es un regulador negativo candidato, no un biomarcador. Incluirlo como "4to gen robusto" fue inflar el hallazgo.

**Corrección aplicada:** Documentación clarifica que solo COL9A1+PTN sobreviven Bonferroni. ST3GAL1 se describe como anticorrelacionado, no como robusto.

### ISSUE-4 (SEVERIDAD BAJA): 67 archivos de datos GEO trackeados en git

**Hallazgo:** 67 archivos bajo datos/ están trackeados en git. El .gitignore excluye datos/ pero los archivos fueron commiteados antes de la exclusión.

**Riesgo:** Repo innecesariamente pesado. No es issue de seguridad (datos son públicos de GEO).

### NO-ISSUE: Token expuesto

El token de Zenodo/GitHub pegado en chat NO está en archivos trackeados del repo. .env está en .gitignore.

## 4. Veredicto final

| Dimensión | Veredicto |
|-----------|-----------|
| Claims numéricos (FC, d, p-values) | ✅ VERIFIED — todos exactos |
| Verificador 3/11 PASS | ✅ VERIFIED — consistente, FAIL esperados |
| "Robust 5/5" | ❌ FALSE — corregido a 4/5 |
| BPIFB2 Bonferroni survival | ❌ FALSE — no sobrevive, degradado a nominal |
| ST3GAL1 como robusto | ❌ FALSE — downregulado, anticorrelacionado |
| Eje opioide composicional (E1) | ✅ VERIFIED — 0/7 genes sobreviven |
| CA14 no sobrevive female-only | ✅ VERIFIED — p=0.1345 |
| QSP ΔpH descartado | ✅ VERIFIED — ΔpH=0 |
| Hallazgos negativos reconocidos en preprint | ✅ VERIFIED |
| Security scan | ✅ VERIFIED — sin secrets en repo |

**Veredicto: PARTIAL → CORREGIDO**

3 issues encontrados (ALTA x2, MEDIA x1), todos corregidos en esta revisión. Los claims numéricos son exactos. Los issues eran de caracterización/categorización (inflar "robusto" y "Bonferroni-survivor"), no de datos.

El trabajo de fondo (FASE 0-3, E1-E7, deep-dive COL9A1) es sólido. Los hallazgos adversariales detectados son de documentación, no de análisis. El núcleo — COL9A1 y PTN como únicos Bonferroni-survivors — se mantiene.
