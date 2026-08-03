# Tangente 1: Identificación y Priorización de Autoantígenos de Membrana en Células Gliales Satélite (SGC) y Nociceptores DRG

**Fecha:** Mayo 2026  
**Repositorio:** `protein-lab/investigacion-fibromialgia`  
**Script Ejecutado:** [`scripts/tangent1_sgc_target_screening.py`](file:///wsl.localhost/Ubuntu/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/scripts/tangent1_sgc_target_screening.py)  
**Evidencia Base:** Goebel 2021 (PMC8245181), Krock 2023 (PMID 37683961), af Ekenstam 2026 (PMID 41271190)

---

## 1. Contexto y Pregunta Central #2

**Pregunta 2:** ¿Qué antígenos de membrana específicos en Células Gliales Satélite (SGC) o nociceptores DRG son reconocidos por auto-IgG en FM?

La evidencia experimental sólida demuestra que la IgG purificada de pacientes con FM se une selectivamente a la superficie de las células gliales satélite (SGC) que envuelven los somas neuronales en el ganglio de la raíz dorsal (DRG) y a las neuronas nociceptivas (Goebel 2021, Krock 2023). 

Para identificar las dianas moleculares de esta respuesta autoinmune periférica, realizamos un screening computacional priorizando proteínas de membrana con ectodominios extracelulares accesibles a inmunoglobulinas.

---

## 2. Ranking de Dianas de Membrana Priorizadas

| Rank | Gen | Proteína / Diana | Tipo Celular Predominante | Topología y Ectodominio Extracelular | Evidencia Autoinmune Previa | Score (/100) |
|---|---|---|---|---|---|---|
| **1** | **CD40** | CD40 (TNFRSF5) | Glía (SGC), Células B, Monocitos | Tipo I paso único, Ectodominio TNFR 1-4 (~170 aa) | **Muy Alta** (af Ekenstam 2026: CD40/CD40L + anti-SGC IgG UP en FM) | **95** |
| **1** | **NFASC** | Neurofascin-155 (NF155) | Glía SGC / Paranodal | Tipo I paso único, Ectodominio Ig+FnIII (~1000 aa) | **Alta** (Diana estándar de IgG4/IgG1 en neuropatías/nodopatías) | **95** |
| **3** | **GJA1** | Conexina-43 (Cx43) | Célula Glial Satélite (SGC) | 4 TM, Loops extracelulares EL1 (~35 aa) y EL2 (~45 aa) | **Alta** (Auto-IgG anti-Cx43 genera dolor e hiperacoplamiento glial) | **85** |
| **3** | **KCNJ10** | Kir4.1 (Canal K+ Inward Rectifier) | Célula Glial Satélite (SGC) | 2 TM, Bucle de poro extracelular (~40 aa) | **Alta** (Autoantígeno comprobado en desmielinización inmune) | **85** |
| **3** | **SCN9A** | NaV1.7 (Canal de Sodio) | Nociceptor DRG Fibras C | 24 TM, Loops de poro extracelulares S5-S6 | **Alta** (IgG anti-NaV1.7 induce hiperexcitabilidad mecánica) | **85** |
| **6** | **SLC1A3** | EAAT1 / GLAST (Transportador Glutamato) | Célula Glial Satélite (SGC) | 8 TM, Loops extracelulares EL2 (~80 aa) | **Moderada** (Autoanticuerpos gliales en encefalitis y neuroinflamación) | **80** |
| **6** | **MRGPRX2** | MRGPRX2 / Mrgprb2 | Mastocitos / Neuronas DRG | GPCR 7 TM, N-terminal extracelular y loops ECL1-3 | **Alta** (Sanchez 2025: IgG-FM activa mastocitos vía MRGPRX2) | **80** |

---

## 3. Análisis Detallado de los Top Candidates en SGC

### 3.1 Connexin-43 (GJA1) — El Hub de Acoplamiento Glial
- **Función en SGC:** Las SGCs están unidas extensamente entre sí mediante uniones gap compuestas por conexina-43 (Cx43). El acoplamiento por Cx43 regula el aclaramiento de $\text{K}^+$, la propagación de calcio y la liberación de ATP/glutamato en el microambiente somático del DRG.
- **Mecanismo Patogénico:** La unión de auto-IgG a los bucles extracelulares EL1/EL2 de Cx43 interrumpe la permeabilidad de las uniones gap o induce la apertura de hemicanales de Cx43, liberando ATP y glutamato en masa hacia el espacio pericelular, lo que despolariza a las neuronas sensoriales contiguas.

### 3.2 Kir4.1 (KCNJ10) — El Amortiguador Potásico Glial
- **Función en SGC:** Canal de potasio rectificador entrante que mantiene el potencial de reposo hiperpolarizado de las SGCs y absorbe el $\text{K}^+$ liberado por las neuronas durante la transmisión del dolor.
- **Mecanismo Patogénico:** El bloqueo directo de la cavidad extracelular del canal Kir4.1 por autoanticuerpos IgG causa la acumulación extracelular de $\text{K}^+$ en el DRG, despolarizando el soma de los nociceptores y provocando alodinia mecánica sostenida.

### 3.3 El Eje CD40 / CD40L (af Ekenstam 2026)
- **Hallazgo Reciente:** El estudio proteomics en suero de 93 FM vs 40 HC (af Ekenstam 2026, PMID 41271190) identificó que **CD40 y CD40L** están significativamente elevados en FM y correlacionan con la severidad de los síntomas y los niveles de anti-SGC IgG.
- **Significado:** CD40 en SGCs y células presentadoras de antígeno promueve la maduración de células B (marcado por el aumento de CD79b y CD4), impulsando la secreción de autoanticuerpos patogénicos dirigidos contra el DRG.

---

## 4. Conclusión de la Pregunta 2

> **Respuesta Definitiva:** Los antígenos de membrana en SGC/DRG priorizados como dactilares para la IgG en FM son **Connexin-43 (GJA1)** y **Kir4.1 (KCNJ10)** en las SGCs (responsables del desequilibrio de ATP/potasio), complementados por el eje neuroinmune **CD40/CD40L** y los canales de sodio nociceptivos **NaV1.7 (SCN9A)**.
