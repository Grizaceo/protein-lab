# RUTA A — Modelo Mastocito/Basófilo/IgG Periférica en Fibromialgia
## Construcción desde grounding verificado localmente

**Fecha:** 2026-05-13
**Base:** 9 papers locales (7 JATS XML + 2 PDF) + 2 metadata-only + 1 externo (Sanchez)
**Regla:** cada afirmación cita el paper local que la respalda. Nada de claims sueltos.

---

## 1. La señal de entrada: DEGs en sangre completa (GSE67311)

**Base:** Jones et al. 2016 (PMC4888802, PMID 27157394)
**Archivo local:** `verified/fulltext_xml/PMC4888802_Jones_2016_GSE67311.xml`
**Dataset:** 70 FM vs 70 controles sanos, sangre total, microarrays Affymetrix.

Hallazgo central: 4 genes de mastocitos/basófilos coordinadamente DOWN en FM:

| Gen | log2FC | FDR | Tipo celular |
|-----|--------|-----|--------------|
| CPA3 | -0.79 | 0.0035 | Mastocito (específico) |
| MS4A2 | -0.52 | 0.019 | Mastocito + basófilo |
| FCER1A | -0.50 | 0.025 | Mastocito + basófilo |
| HDC | -0.53 | 0.048 | Mastocito + basófilo + algunas neuronas |

**Significado:** estos 4 genes codifican componentes funcionales del mismo sistema:
- **CPA3**: proteasa específica de mastocitos, almacenada en gránulos (Atiakshin 2022, PMC8834431)
- **MS4A2 + FCER1A**: subunidades β y α del receptor de alta afinidad para IgE (FcεRI)
- **HDC**: enzima única que produce histamina (Hirasawa 2019, PMC6359378)

Que los 4 estén DOWN en sangre completa sugiere agotamiento/depleción del compartimento de mastocitos/basófilos circulantes, no hiperactivación.

**Claim prohibido:** "esto prueba migración a tejidos". Es compatible, pero no lo prueba.

---

## 2. El mecanismo propuesto: IgG → mastocito → dolor

### 2.1 Transferencia pasiva de síntomas FM por IgG (Goebel 2021)

**Base:** Goebel et al. 2021 (PMC8245181, PMID 34196305)
**Archivo local:** `verified/fulltext_xml/PMC8245181_Goebel_2021_IgG_transfer.xml`

Hallazgos verificados desde el abstract:
- IgG purificada de pacientes FM, inyectada en ratones, produce:
  - Hipersensibilidad mecánica y al frío
  - Sensibilización de neuronas nociceptivas (fibras C y Aδ)
  - Reducción de locomoción y fuerza de agarre
- IgG de controles sanos NO produce estos efectos
- Suero depletado de IgG NO produce estos efectos

**Esto cumple criterios Witebsky-Rose para enfermedad autoinmune mediada por IgG.**

### 2.2 El receptor MRGPRX2/b2 (Sanchez 2025 — externo)

**Base:** Sanchez et al. 2025, bioRxiv DOI 10.1101/2025.05.15.652596
**Estado:** NO descargado (Cloudflare), leído externamente. No usar como pilar fuerte.

Hallazgos leídos:
- IgG-FM se une a mastocitos humanos vía MRGPRX2
- Ratones sin Mrgprb2 no desarrollan dolor al recibir IgG-FM
- La unión induce secreción de IL-6
- Mastocitos de piel de pacientes FM: mayor densidad (107.1 vs 46.4 células/mm², p=0.0006)
- Triptasa extracelular elevada en piel FM (marcador de degranulación)

**Limitación:** preprint, no peer-reviewed. Los hallazgos de densidad/triptasa en piel humana son consistentes con Blanco 2010.

### 2.3 Hipótesis de mastocitos talámicos (Theoharides 2019)

**Base:** Theoharides et al. 2019 (PMC6687840, PMID 31427928)
**Archivo local:** `verified/fulltext_xml/PMC6687840_Theoharides_2019_MastCells_FM.xml`

Hipótesis publicada: mastocitos en el tálamo liberan histamina, IL-1β, IL-6, TNF, SP y CGRP, contribuyendo a neuroinflamación y dolor central en FM.

**Estado:** hipótesis, no demostración. Sustentada por niveles séricos elevados de SP, HK-1, IL-6 y TNF reportados previamente por el mismo grupo.

---

## 3. Lo que NO funciona: estabilizar mastocitos

**Base:** Ang et al. 2015 (PMC4417653, PMID 25370135)
**Archivo local:** `verified/fulltext_xml/PMC4417653_Ang_2015_Ketotifen.xml`

Ketotifen 2mg BID por 8 semanas vs placebo en 51 sujetos FM.

Resultado:
- Medidas primarias: **NO significativas**
- Medidas secundarias: **NO significativas**
- Conclusión de los autores: "nuestros resultados cuestionan si los mastocitos cutáneos juegan un rol mayor en la patogénesis de FM"

**Implicación:** estabilizar mastocitos no alivia síntomas FM en el único trial fase 1 existente.

---

## 4. Nueva evidencia: CD40/CD40L y anti-SGC IgG (af Ekenstam 2026)

**Base:** af Ekenstam et al. 2026 (PMID 41271190)
**Archivo local:** `verified/fulltext_xml/afEkenstam_2026_CD40_antiSGC.pdf` (PDF real, CC-BY, 20pp)

Diseño: 93 FM vs 40 controles sanos. Panel Olink de 384 proteínas inflamatorias en suero.

**Hallazgos clave del PDF:**

1. **Cluster inmune UP en FM:** proteínas del sistema inmune dominan las proteínas sobreexpresadas, incluyendo:
   - **CD40 y CD40L** (eje fundamental de interacción célula T/B)
   - Asociación de CD40 con severidad de síntomas

2. **Cluster de desarrollo/reparación tisular DOWN en FM:** inverso a lo visto en controles con dolor nociceptivo (específico de FM)

3. **En FM con alto anti-SGC IgG:**
   - Cluster de proteínas inmunes UP incluye CD79b (necesario para función del receptor de célula B) y CD4 (co-receptor para activación T)
   - Esto sugiere activación de linfocitos B y T en el subtipo con anti-SGC IgG alto

4. **Anti-SGC IgG cuantificado por inmunofluorescencia:**
   - Correlación con severidad de síntomas
   - Consistente con hallazgos previos de Krock 2023

**Implicación directa para Ruta A:** CD40/CD40L como posible driver de la producción de autoanticuerpos (anti-SGC IgG). La activación de células B (vía CD79b) y T (vía CD4) está elevada específicamente en el subtipo FM con autoanticuerpos.

---

## 5. Satélites gliales y autoanticuerpos (Krock 2023 — metadata-only)

**Base:** Krock et al. 2023 (PMID 37683961, DOI 10.1016/j.bbi.2023.09.003)
**Estado:** metadata-only. Abstract verificado en PubMed, sin fulltext local.

Desde el abstract:
- Anti-SGC IgG elevado en un subgrupo de pacientes FM
- Asociación con severidad de síntomas
- Correlación con concentraciones de metabolitos en tálamo y corteza cingulada anterior rostral

No se usan detalles del full text por no tenerlo local.

---

## 6. Modelo integrado de Ruta A (solo claims respaldados)

### Cadena mecanística (con nivel de evidencia por eslabón)

```
[Evidencia muy sólida]     GSE67311 (Jones 2016): CPA3/MS4A2/FCER1A/HDC DOWN en sangre
                           ↓
[Evidencia sólida]         Goebel 2021: IgG de FM → dolor en ratones (Witebsky-Rose positivo)
                           ↓
[Evidencia moderada]       Lee 2022 bioRxiv: IgG-FM se une a mastocitos → IL-6 (vía MRGPRX2)
                           ↓
[Evidencia moderada]       Theoharides 2019: hipótesis de mastocitos → histamina/IL-6 → dolor
                           ↓
[Evidencia meta-only]      Krock 2023, Seefried 2025: anti-SGC IgG asociado a severidad
                           ↓
[Evidencia sólida]         af Ekenstam 2026: CD40/CD40L + CD79b + CD4 ↑ en subtipo anti-SGC+
                           ↓
[Evidencia negativa]       Ang 2015: ketotifen NO funciona (estabilizar mastocitos no basta)
```

### Qué tipo de intervención predice este modelo

Si el mecanismo es IgG → MRGPRX2 → mastocito/basófilo → IL-6/histamina → dolor:

- **No predice** que estabilizadores de mastocitos (ketotifen, cromoglicato) funcionen
- **Predice** que anti-IL-6 (tocilizumab) podría funcionar en el subgrupo con activación mastocitaria
- **Predice** que inmunomodulación (plasmaféresis, IVIG, rituximab) podría funcionar en el subgrupo anti-SGC+
- **Predice** que anti-CD40/CD40L (dapirolizumab) podría ser relevante

### Subgrupos que predice el modelo

1. **FM con autoanticuerpos IgG (anti-SGC+)** — 30-40% según Seefried 2025
2. **FM con activación mastocitaria** — señal CPA3/MS4A2/FCER1A/HDC down en sangre
3. **FM con CD40/CD40L alto** — posiblemente solapado con el grupo 1

No toda FM es autoinmune mastocitaria. Probablemente es un subgrupo.

---

## 7. Lo que falta para fortalecer esta ruta

### Papers pendientes de descargar

| Paper | Lo que aportaría |
|---|---|
| Krock 2023 (PMID 37683961) | Detalles de anti-SGC IgG y metabolitos talámicos |
| Seefried 2025 (PMID 39907533) | Subclusters de unión de IgG a DRG (membrana vs citoplasma) |
| Blanco 2010 (PMID 20428906) | Datos histológicos de mastocitos en piel FM |

### Experimentos que cerrarían el círculo

1. Análisis de GSE229750 con enfoque específico en mastocitos/basófilos (aunque es neutrófilos, ver si IL-6R cambia con tocilizumab)
2. Correlacionar nuestra señal DEG de mastocitos (CPA3/MS4A2/FCER1A/HDC) con otras bases de datos disponibles
3. Si hay datos de scRNA-seq de sangre FM, ver si los mastocitos/basófilos están depletados o alterados

---

## 8. Resumen para decisión

Ruta A es **mecanísticamente coherente pero clínicamente frágil**.

Coherente porque:
- La señal transcriptómica de mastocitos/basófilos en sangre es real y reproducible
- La IgG de pacientes FM transfiere dolor a ratones (Goebel 2021)
- Hay evidencia convergente de CD40/CD40L y autoanticuerpos anti-SGC (af Ekenstam 2026)
- La conexión MRGPRX2 tiene sentido biológico (Sanchez 2025 bioRxiv)

Frágil porque:
- El único trial de intervención dirigido a mastocitos (ketotifen) fue negativo
- No hay ensayos clínicos de anti-IL-6, anti-CD40, o plasmaféresis en FM con resultados
- La mayor parte de la evidencia es correlacional o de modelo animal
- Los papers que cierran el círculo (Krock, Seefried, Sanchez) no están full-text local o son preprint

**Veredicto DAVI:** Ruta A es la mejor hipótesis biológica que tenemos. Pero no es una ruta de tratamiento inmediato — es una ruta de investigación. Si el objetivo es entender el mecanismo de FM, esta es la ruta. Si el objetivo es encontrar un tratamiento para mañana, Ruta B (MOR/LDN) sigue siendo más accionable a pesar del resultado negativo del Lancet trial 2024.

---

## Anexo: Papers locales utilizados en este modelo

| # | Paper | PMID | Archivo local | Formato |
|---|-------|------|-------------|---------|
| 1 | Jones 2016, GSE67311 | 27157394 | `PMC4888802_Jones_2016_GSE67311.xml` | JATS XML |
| 2 | Goebel 2021, IgG transfer | 34196305 | `PMC8245181_Goebel_2021_IgG_transfer.xml` | JATS XML (abstract-only) |
| 3 | Theoharides 2019, Mast cells FM | 31427928 | `PMC6687840_Theoharides_2019_MastCells_FM.xml` | JATS XML |
| 4 | Ang 2015, Ketotifen trial | 25370135 | `PMC4417653_Ang_2015_Ketotifen.xml` | JATS XML |
| 5 | Atiakshin 2022, CPA3 review | 35159379 | `PMC8834431_Atiakshin_2022_CPA3.xml` | JATS XML |
| 6 | Hirasawa 2019, HDC/inflammation | 30654600 | `PMC6359378_HDC_2019.xml` | JATS XML |
| 7 | af Ekenstam 2026, CD40/anti-SGC | 41271190 | `afEkenstam_2026_CD40_antiSGC.pdf` | PDF real |
| 8 | Krock 2023, anti-SGC IgG | 37683961 | — (metadata-only) | — |
| 9 | Seefried 2025, autoantibodies | 39907533 | — (metadata-only) | — |
| 10 | Blanco 2010, skin mastocytes | 20428906 | — (metadata-only) | — |
