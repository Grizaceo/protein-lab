# RESULTADOS P1 + P2 — LDN en Fibromialgia: Evidencia Clínica y Mecanismo

**Fecha:** 2026-05-14 17:30
**Pasos del plan:** P1 (RCTs LDN en FM) + P2 (mecanismo TLR4 vs MOR)
**Fuentes verificadas:** PMIDs 23359310, 38226027; PMC4761092, PMC6700752; ACR Convergence 2025

---

## P1: ENSAYOS CLÍNICOS DE LDN EN FIBROMIALGIA

### Tabla de RCTs

| Estudio | PMID | Diseño | n | Dosis | Duración | Resultado dolor | p | Efecto |
|---|---|---|---|---|---|---|---|---|
| Younger 2013 | **23359310** | Crossover, DB, PC | 31 mujeres | 4.5 mg/d | 4 sem c/u | LDN -28.8% vs PLB -18.0% | **0.016** | Δ ~10.8pp significativo |
| 2024 crossover | **38226027** | Crossover, DB, PC | 58 FM | 4.5 mg/d | 3 sem c/u | FIQR Δ -1.65 (ES=0.15) | **0.3 (NS)** | Sin eficacia analgésica clínicamente relevante |
| FINAL Study | NCT04270877 | Paralelo, DB, PC | ? | 4.5 mg/d | 12 sem | — | — | Estado desconocido (¿no publicado?) |

### Meta-análisis ACR 2025
- **Pain:** SMD -0.851 (95% CI -1.290 a -0.412) — significativo
- **FIQ-R:** SMD -0.978 (95% CI -1.926 a -0.030) — significativo
- **Seguridad:** solo sueños vívidos > placebo (OR 2.17)
- Limitación reportada: "lack of robust randomized evidence"

### Interpretación honesta

**La evidencia NO es uniformemente positiva.** El panorama real:

1. **Younger 2013 (n=31):** Ensayo positivo, pero pequeño, single-site, solo mujeres, diseñado como "preliminary evidence." El autor principal (Jarred Younger) es el principal defensor académico de LDN.

2. **2024 crossover (n=58):** Ensayo NEGATIVO. Más grande, más reciente, diseño riguroso. "Outcome data did not indicate any clinically relevant analgesic efficacy." Efecto trivial (ES=0.13-0.15).

3. **Meta-análisis ACR 2025:** Pooled effect positivo, pero probablemente dominado por Younger 2013. Si solo hay 2-3 RCTs publicados y uno es negativo, el meta-análisis puede estar sobre-estimando el efecto.

**Veredicto P1:** LDN es **promisorio pero NO conclusivo.** El RCT más grande y reciente es negativo. El efecto, si existe, es modesto (SMD ~0.4-0.8, con alta heterogeneidad entre estudios). La recomendación del proyecto no debería basarse solo en "LDN funciona."

### ¿Qué explica la discrepancia Younger 2013 vs 2024?

Posibles factores:
- Younger usó medidas diarias repetidas (más poder estadístico para detectar cambios intra-sujeto)
- El crossover de 2024 tuvo períodos más cortos (3 semanas vs 4)
- Diferente población (¿severidad? ¿medicación concomitante?)
- El efecto real de LDN es pequeño y algunos estudios no tienen poder para detectarlo
- Posible sesgo de publicación: los estudios negativos grandes tardan en publicarse

---

## P2: MECANISMO — ¿TLR4 O MOR?

### La hipótesis TLR4: bioquímicamente real, farmacocinéticamente imposible a dosis LDN

**Evidencia bioquímica (sólida):**

| Referencia | Hallazgo |
|---|---|
| Wang 2016, PMC4761092 | (+)-Naltrexona y (+)-naloxona son antagonistas TLR4 equipotentes. Inhiben la vía TRIF-IRF3 (NO, TNF-α, ROS). NO inhiben NF-κB ni IL-1β. Independiente de receptores opioides (no estereoselectivo). |
| Zhang 2018, PMC6700752 | (+)-Naltrexona se une al pocket hidrofóbico de MD-2 (co-receptor de TLR4). **Kd = 13.7 μM.** IC50 para inhibición de NO en microglía BV-2 = **105 μM.** |
| Hutchinson/Watkins lab (múltiples) | TLR4 en microglía media dolor neuropático en roedores. (+)-Naltrexona revierte dolor neuropático en ratas. |

**El problema farmacocinético (devastador):**

| Parámetro | Valor | Fuente |
|---|---|---|
| Dosis LDN | 4.5 mg/día oral | — |
| Cmax naltrexona (estimada) | ~3-10 ng/mL → ~10-30 nM | FDA label, PK estándar |
| 6β-naltrexol Cmax | ~2-3× mayor, vida media más larga | FDA label |
| Kd (+)-naltrexona → MD-2 | **13.7 μM = 13,700 nM** | PMC6700752 |
| IC50 TLR4 (NO, microglía) | **105 μM = 105,000 nM** | PMC4761092 |

**GAP entre [plasma] LDN y [efectiva] TLR4:**

```
LDN Cmax plasmática:      ~20 nM
Kd MD-2 (+)-naltrexona:   13,700 nM  →  gap ~685×
IC50 TLR4 funcional:       105,000 nM  →  gap ~5,250×
```

**A dosis LDN, la concentración plasmática de naltrexona está 2-3 órdenes de magnitud por debajo del Kd para MD-2, y 3-4 órdenes por debajo del IC50 funcional.** Esto hace que la hipótesis de antagonismo TLR4 directo por naltrexona a dosis LDN sea **farmacocinéticamente inviable**, a menos que exista alguno de estos factores:

1. **Acumulación en SNC:** ¿naltrexona/6β-naltrexol se concentran en cerebro 100-1000× sobre plasma? Improbable. Son moléculas pequeñas lipofílicas con distribución relativamente uniforme.

2. **6β-naltrexol es mucho más potente en TLR4 que naltrexona:** No hay evidencia de esto. La literatura se enfoca en (+)-naltrexona y (+)-naloxona.

3. **Efecto crónico ≠ efecto agudo:** La inhibición parcial y sostenida de TLR4 durante semanas podría tener efectos distintos a la inhibición aguda in vitro. Pero el gap es tan grande (1000×) que incluso con acumulación crónica es difícil de cerrar.

4. **La hipótesis TLR4 es incorrecta para LDN.** Esta es la explicación más parsimoniosa.

### ¿Entonces cuál es el mecanismo de LDN?

Si descartamos TLR4 a dosis LDN, quedan:

**A. Bloqueo MOR parcial + upregulation compensatoria**
- LDN 4.5 mg bloquea MOR parcialmente (no totalmente como 50 mg)
- El bloqueo parcial + la corta vida media (4h naltrexona, 13h 6β-naltrexol) crea una ventana diaria de "rebote opioide"
- Durante esa ventana, los receptores MOR upregulados responden a endorfinas endógenas → analgesia
- Consistente con: LDN se toma de noche (bloqueo durante el sueño, rebote durante el día)
- PET [11C]carfentanil: 50 mg bloquea ~90% MOR. 4.5 mg podría bloquear ~20-40%. Esto sí es farmacocinéticamente plausible (naltrexona Ki=0.2 nM → ocupación significativa a concentraciones nanomolares).

**B. Efecto sobre células gliales distinto a TLR4**
- Naltrexona podría tener otros targets no-opioides además de TLR4
- Modulación de la actividad microglial por mecanismo no caracterizado

**C. Efecto sobre el eje hipotálamo-hipófisis-adrenal (HPA)**
- Opioides endógenos modulan el eje HPA
- El bloqueo intermitente de MOR podría normalizar un eje HPA disfuncional en FM

### Veredicto P2

```
HIPÓTESIS TLR4 PARA LDN:
├── Evidencia bioquímica: SÓLIDA (naltrexona antagoniza TLR4 vía MD-2)
├── Evidencia farmacocinética: CONTRADICTORIA (gap ~1000×)
└── Veredicto: TLR4 NO es el mecanismo de LDN a dosis 4.5 mg/día
    (a menos que exista evidencia de acumulación masiva en SNC
    o un metabolito mucho más potente que naltrexona en MD-2)

HIPÓTESIS MOR PARA LDN:
├── Evidencia bioquímica: SÓLIDA (Ki=0.2-3.6 nM MOR)
├── Evidencia farmacocinética: PLAUSIBLE ([plasma] ~10 nM > Ki 0.2 nM)
├── Mecanismo: bloqueo parcial + upregulation compensatoria
└── Veredicto: MOR es el mecanismo más plausible para LDN en FM
    (aunque el mecanismo exacto —rebote, upregulation, modulación glial
    indirecta— sigue sin estar completamente caracterizado)
```

---

## DECISIÓN: IMPACTO EN EL PROYECTO

### ¿LDN como recomendación principal?

**No por ahora.** La evidencia clínica es mixta (RCT positivo pequeño + RCT negativo más grande). Si el proyecto quiere hacer una recomendación terapéutica fuerte, LDN no tiene el nivel de evidencia necesario. Si el proyecto es exploratorio/hipótesis, LDN sigue siendo un candidato interesante.

### ¿Docking MOR?

**Sí, pero con expectativas ajustadas.** Sabemos que naltrexona se une potentemente a MOR. El docking no va a descubrir nada nuevo sobre esa interacción. Su valor sería:
1. Validar el pipeline de docking para futuros screenings
2. Demostrar que Vina-GPU recapitula el modo de unión conocido (morphine en 8EF6)
3. Comparar scores de controles positivos vs negativos
4. Si funciona, usarlo para screening virtual de nuevos candidatos MOR (no para FM necesariamente, pero útil como herramienta)

### ¿Pivotar a TLR4?

**No como mecanismo de LDN.** Pero TLR4 sigue siendo un target interesante para FM por otras razones:
- Neuroinflamación glial en dolor crónico
- TAK-242 (resatorvid) y otros antagonistas TLR4 puros existen
-La evidencia de TLR4 en FM no depende de naltrexona

### ¿Qué hacer con el proyecto?

Tres caminos, no mutuamente excluyentes:

1. **LDN como caso de estudio de repurposing:** "LDN en FM: evidencia clínica mixta, mecanismo probablemente MOR (no TLR4 como se creía), justifica estudios mecanísticos adicionales."

2. **Mastocitos/MS4A2 como línea paralela:** Señal transcriptómica sólida en GSE67311. No depende de naltrexona. Apunta a disfunción inmune periférica.

3. **GWAS-guided:** DRD2 está en los 26 loci. La vía dopaminérgica en FM está inexplorada en nuestro proyecto. Podría conectar con duloxetina/milnacipran (SNRIs aprobados para FM que aumentan dopamina).

---

## PRÓXIMA ACCIÓN CONCRETA

**Docking Vina-GPU (P5) ya tiene justificación.** Sabiendo que:
- MOR es el mecanismo más plausible (P2)
- LDN tiene evidencia clínica mixta pero suficiente para mantener interés (P1)
- MAMMAL no sirvió para evaluar afinidad (Ruta B)
- El docking validaría el pipeline y daría scores comparables a binding assays reales

Pero con expectativas ajustadas: no va a "descubrir" que naltrexona se une a MOR. Eso ya se sabe. Va a validar una herramienta.

**Si quieres priorizar impacto clínico sobre herramienta:** saltar a P3 (OPRM1 A118G) o P4 (DRD2/dopamina). Esas rutas tienen más potencial de novedad.

---

*Síntesis P1+P2. Commit siguiente.*
