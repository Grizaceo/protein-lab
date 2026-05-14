# REFERENCIAS AUDITADAS — Fibromialgia

**Fecha:** 2026-05-13  
**Motivo:** corregir el estado local de archivos: varios documentos estaban guardados con extensión `.pdf` pero eran HTML/texto o páginas de error. Este archivo supersede el resumen de estado de PDFs de `literatura/REFERENCIAS.md`, sin reemplazar aún toda la bibliografía.

---

## Leyenda nueva

- `PDF real local`: `file` confirma documento PDF.
- `HTML/full text local`: hay contenido local o extracción web, pero no es PDF real.
- `Identificador verificado`: DOI/PMID/PMC resoluble, pero sin full text local fiable todavía.
- `Pendiente de re-verificación`: no usar para decisiones fuertes hasta re-chequear.

---

## Estado local auditado

| Archivo local | Estado real | Acción |
|---|---|---|
| `Ghasemikhah_2025_FrontiersNeurosci_LipidMetabolism.pdf` | PDF real local | Usable |
| `Goebel_2021_PainMed_ResearchRecommendations.pdf` | PDF real local | Usable |
| `Ho_2025_FrontiersPain_RedoxChronicPain.pdf` | PDF real local | Usable |
| `Zhao_2025_FrontiersGenetics_DYRK3_RGS17_ARHGEF37.pdf` | PDF real local | Usable |
| `Ang_2015_PMC4417653_Ketotifen_FM_Trial.pdf` | HTML/texto con extensión .pdf | Usable como extracción local, no como PDF |
| `Atiakshin_2022_PMC8834431_CPA3_MastCell_Review.pdf` | HTML/texto con extensión .pdf | Usable como extracción local, no como PDF |
| `Cai_2025_Neuron_GutMicrobiotaPain.pdf` | HTML/texto con extensión .pdf | Verificado por DOI/PMID, full text local débil |
| `Gimenez-Orenga_2025_PMC_HERV_FM_MECFS.pdf` | HTML/texto con extensión .pdf | Usable con cautela |
| `Ichikawa_2019_PMC6359378_HDC_Inflammation.pdf` | HTML/texto con extensión .pdf | Usable como extracción local, no como PDF |
| `Krock_2023_BrainBehavImmun_AntiSGC_IgG.pdf` | HTML/texto con extensión .pdf | Verificado por DOI/PMID, full text local no es PDF |
| `Li_2025_FrontiersPharm_FibroPharmaUpdate.pdf` | HTML/texto con extensión .pdf | Verificado, pero full text local no es PDF |
| `Theoharides_2019_PMC6687840_MastCells_Neuroinflammation_FM.pdf` | HTML/texto con extensión .pdf | Usable como extracción local, no como PDF |

---

## Referencias críticas validadas externamente durante auditoría

- GSE67311 existe en GEO como estudio de sangre completa: 70 pacientes FM y 70 controles sanos.
- Ang et al. ketotifen trial existe como PMC4417653 / PMID 25370135; resultado negativo para medidas primarias.
- Theoharides et al. 2019 mast cells/FM existe como PMC6687840 / PMID 31427928 / DOI 10.3389/fncel.2019.00353; es hipótesis publicada.
- Atiakshin et al. 2022 CPA3 review existe como PMC8834431 / PMID 35159379 / DOI 10.3390/cells11030570.
- Hirasawa/Ichikawa 2019 HDC/inflammation existe como PMC6359378 / PMID 30654600 / DOI 10.3390/ijms20020376.
- Krock et al. 2023 anti-SGC IgG existe como PMID 37683961 / DOI 10.1016/j.bbi.2023.08.012.
- Goebel/passive transfer line exists via PMC8245181 and recommendations via PMC9157149.

---

## Regla operativa

No volver a decir “8 PDFs descargados y verificados”. La forma correcta es: `4 PDF reales locales + varias extracciones HTML/full-text + identificadores DOI/PMID/PMC verificados`. Para cualquier paper que pase a sostener una conclusión fuerte, volver a descargar el PDF real o guardar extracción markdown completa con URL y fecha.
