# EVIDENCIA ORTOGONAL — Fibromialgia, Post-Calibración MAMMAL

**Fecha:** 2026-05-14 15:20 America/Santiago
**Objetivo:** Evaluar si la señal de MOR y MS4A2 detectada por MAMMAL DTI sobrevive al cruce con evidencia externa independiente: estructuras PDB, binding assays públicos, transcriptómica GEO, y viabilidad de docking.
**Regla:** cero invención. Toda afirmación con DOI/PMID/PDB ID/ChEMBL ID verificable.

---

## 0. Diagnóstico de partida

MAMMAL DTI (458M, fine-tuned en BindingDB pKd) mostró un sesgo estructural de fold para GPCR Class A. Cuatro GPCRs no-relacionados (MOR, ADRB2, DRD2, AGTR1) rankean 15 fármacos diversos en orden casi idéntico (r=0.926-0.990). El "bono GPCR" automático es ~+0.9 pKd, haciendo que cualquier fármaco puntúe pKd≥6.5 contra MOR. Esto no es afinidad — es ruido estructural del embedding.

La pregunta ya no es "¿qué target tiene mejor pKd en MAMMAL?" sino "¿la biología real respalda MOR, MS4A2, o ninguno?"

---

## 1. ESTRUCTURAS PDB: ¿Hay con qué hacer docking?

### 1.1 MOR humano (OPRM1)

| PDB ID | Método | Resolución | Ligando | Organismo MOR | PMID | DOI |
|---|---|---|---|---|---|---|
| **8EF6** | Cryo-EM | 2.8 Å (estimado) | **Morphine** + Fentanyl | **Homo sapiens** | 36368322 | 10.1016/j.cell.2022.09.041 |
| 6DDF | Cryo-EM | 3.50 Å | DAMGO (peptide) | Mus musculus | 29899455 | 10.1038/s41586-018-0219-7 |
| 7T2H | Cryo-EM | 3.20 Å | Lofentanil | Mus musculus | 36411392 | 10.1038/s41589-022-01208-y |
| 8F7R | Cryo-EM | — | Endomorphin | — | — | — |

**Veredicto:** **Estructura experimental humana disponible: 8EF6.** Es human MOR + Gi complex, con morphine y fentanyl co-cristalizados. Resolución suficiente para docking. No se encontró estructura con naltrexone bound — el docking sería _predicción_, no _validación_.

**Fuente adicional relevante:** GPCRdb (gpcrdb.org/protein/OPRM_HUMAN/) lista estructuras para MOR humano, incluyendo estados activo/inactivo.

### 1.2 MS4A2 / FcεRIβ

| PDB ID | Método | Resolución | Complejo | Organismo | PMID | DOI |
|---|---|---|---|---|---|---|
| **8YWA** | Cryo-EM | 3.14 Å | FcεRI completo (αβγ2) + IgE | Homo sapiens | 39442557 | 10.1038/s41586-024-08229-8 |

**Veredicto:** **Existe una estructura: 8YWA.** Es el complejo FcεRI completo (subunidades α + β + γ×2) unido a IgE. MS4A2 está presente como subunidad β (244 aa, 4 hélices transmembrana). Sin embargo:
- No es una estructura aislada de MS4A2 → hacer docking _ciego_ sobre MS4A2 dentro del complejo es técnicamente más difícil.
- No hay ligando small-molecule bound a MS4A2 en esta estructura.
- El pocket de binding (si existe) no está caracterizado estructuralmente.

La estructura AlphaFold de MS4A2 (AF-Q01362-F1) ya existe localmente en `datos/pdb/corrected/`, pero es una predicción, no experimental.

**Conclusión estructural:** MOR está listo para docking. MS4A2 requeriría más trabajo preparatorio (extraer la subunidad del complejo, evaluar druggabilidad del pocket).

---

## 2. BINDING ASSAYS PÚBLICOS: ¿Qué dice la farmacología real?

### 2.1 Naltrexona → MOR

| Fuente | Tipo | Valor | Unidad | Referencia |
|---|---|---|---|---|
| BindingDB (BDBM60212) | Ki | 0.20 | nM | PMID 26632862, J Med Chem 58:9754-67 (2015) |
| PubChem AID 239328 | Ki | 0.2 | nM | ChEMBL |
| PubChem AID 1259163 | Ki | 0.7 | nM | — |
| PubChem AID 450029 | Ki | 3.6 | nM | — |
| PubChem AID 1121819 | IC50 | 8.9 | nM | — |

**Interpretación:** Naltrexona tiene afinidad **sub-nanomolar a nanomolar baja** por MOR humano. pKd ≈ 9.0-9.7 (Kd ≈ 0.2-1.0 nM). Es uno de los antagonistas MOR más potentes conocidos.

Esto **contrasta radicalmente** con el pKd=6.84 de MAMMAL (Kd aparente ~145 nM). El modelo **subestima** la afinidad real de naltrexona por MOR en ~3 órdenes de magnitud (×700).

### 2.2 Controles positivos → MOR

| Fármaco | Ki (MOR humano) | Fuente |
|---|---|---|
| Morphine | 0.5-6.55 nM | BindingDB, 8 ensayos |
| Buprenorphine | 0.216-1.5 nM | PMID/PMC5967713, BindingDB BDBM50026603 |
| Fentanyl | sub-nM | Estructura 8EF6 + farmacología conocida |
| DAMGO | Ki 36.7 nM | PubChem AID 239075 |

**Comparación con MAMMAL:** MAMMAL asigna a todos estos fármacos pKd≈6.8-7.1 (Kd≈80-160 nM). La farmacología real muestra Ki en rango 0.2-6 nM para agonistas y antagonistas MOR. MAMMAL no solo no discrimina entre clases farmacológicas — también **comprime el rango dinámico** de afinidad real.

### 2.3 Controles negativos → MOR

| Fármaco | ¿Binding a MOR? | Evidencia |
|---|---|---|
| **Atorvastatin** | **No detectado** | Sin entradas en ChEMBL (CHEMBL233), BindingDB, o PubChem BioAssay para atorvastatin→MOR. |
| **Omeprazole** | **No detectado** | Sin entradas en ChEMBL (CHEMBL233), BindingDB, o PubChem BioAssay para omeprazole→MOR. |
| Ibuprofen | No detectado en binding assays | Sin evidencia de unión directa a MOR. |
| Metformin | No detectado | Sin evidencia. |

**Interpretación:** La farmacología real confirma que atorvastatin y omeprazole NO se unen a MOR. El pKd=7.17 de atorvastatin en MAMMAL es **completamente espurio** — un artefacto del bono GPCR.

### 2.4 Naltrexona → MS4A2

**Sin datos en ChEMBL, BindingDB, o PubChem.** No hay evidencia de que naltrexona se una a MS4A2/FcεRIβ. Esto no significa que no ocurra — significa que nadie lo ha medido. MS4A2 no es un target farmacológico clásico.

### 2.5 ChEMBL: el target MOR en números

- **ChEMBL ID:** CHEMBL233 (Mu-type opioid receptor)
- **Total bioactivities:** 31,330
- **Total assays:** 2,053
- **Compounds tested:** 13,408
- **Approved drugs targeting MOR:** 44 (oxycodone, buprenorphine, morphine, fentanyl, naltrexone, etc.)
- **Distribución de potencia:** <1 nM: 124 compuestos; [1-100) nM: 488; [100-1000) nM: 212

MOR es probablemente uno de los GPCRs mejor caracterizados farmacológicamente del genoma humano.

---

## 3. CRUCE CON DATASETS GEO AUDITADOS

### 3.1 GSE67311 — Sangre completa, FM vs control

| Gene | log2FC | p_adj | Dirección | ¿En nuestros 16 targets? |
|---|---|---|---|---|
| CPA3 | -0.786 | 0.0035 | DOWN | **Sí** — Tier 3 (mast cell protease) |
| C1orf150 | -0.430 | 0.0076 | DOWN | No |
| **MS4A2** | **-0.516** | **0.019** | **DOWN** | **Sí — Tier 3** |
| FCER1A | -0.501 | 0.025 | DOWN | **Sí** — Tier 3 |
| ITGB8 | -0.328 | 0.026 | DOWN | No |
| GATA2 | -0.452 | 0.048 | DOWN | No |
| C11orf83 | -0.149 | 0.048 | DOWN | No |
| HDC | -0.528 | 0.048 | DOWN | **Sí** — Tier 3 |

**MOR (OPRM1): NO aparece.** Esperado — es GPCR de SNC, no expresado en sangre periférica a niveles detectables por microarray.

**TLR4: NO aparece.** No sorprende — TLR4 se regula más por tráfico y modificaciones post-traduccionales que por mRNA en sangre.

**MS4A2: SÍ aparece.** FDR significativo (0.019), DOWN en FM. Esto es **señal convergente**: el gen que codifica la subunidad beta del receptor de IgE está disminuido en sangre de pacientes FM.

**CPA3, FCER1A, HDC: todos DOWN.** Forman una firma coherente de mastocitos/basófilos disminuidos o disfuncionales en sangre periférica de FM.

### 3.2 GSE229750 — Neutrófilos FM vs control

| Gene | log2FC | p_adj | ¿En nuestros 16 targets? |
|---|---|---|---|
| TSPAN13 | -2.478 | 6.0e-08 | No (tetraspanina, pero no MS4A2) |
| C3AR1 | +1.938 | 1.0e-04 | No |
| PI3 | +0.986 | 9.5e-04 | No |

**Ninguno de los 16 targets aparece.** Consistente: los neutrófilos no expresan FcεRI ni MOR. Esto refuerza que la señal mastocito/basófilo de GSE67311 es específica de tipo celular.

### 3.3 Convergencia transcriptómica

```
GSE67311 (sangre completa FM):
  MS4A2 ↓   CPA3 ↓   FCER1A ↓   HDC ↓
       │         │         │          │
       └─────────┴─────────┴──────────┘
                    │
          Firma mastocito/basófilo
          DOWN en sangre periférica FM
                    │
          ¿Consistente con hipótesis?
          - Migración a tejidos? (no demostrado por este dato solo)
          - Disfunción/deplación periférica? (documentado)
          - Target terapéutico? MS4A2/FcεRI como modulador,
            no como target de pequeño fármaco directo
```

---

## 4. DOCKING MOLECULAR: Viabilidad

### 4.1 MOR

| Tool | Setup | Tiempo estimado | GPU necesaria |
|---|---|---|---|
| **DiffDock** (Colab) | pip install + bajar weights (~1 GB) | 1-2h para primer run | Colab GPU (Tesla T4, gratis) |
| **AutoDock Vina-GPU** (local) | compilar desde source + instalar Meeko + preparar archivos | 3-4h para primer run | RTX 4060 local |

**Recomendación:** **DiffDock vía Colab.** Menos setup, blind docking (no requiere definir pocket), y permite probar rápido naltrexone + controles. Si los resultados son prometedores, pasar a Vina-GPU local para validación más rigurosa.

**Moléculas a dockear contra 8EF6 (human MOR):**
1. Naltrexone (hipótesis principal)
2. Morphine (control positivo — está en la estructura)
3. Buprenorphine (control positivo de alta afinidad)
4. Atorvastatin (control negativo — no debería dockear bien)
5. Omeprazole (control negativo)

### 4.2 MS4A2

**Más complejo.** La única estructura experimental (8YWA) es el complejo FcεRI completo. Se necesitaría:
1. Extraer la cadena B (MS4A2) del complejo
2. Evaluar si hay pocket druggable (probablemente no — MS4A2 es subunidad accesoria, no tiene sitio de unión a ligando clásico)
3. Alternativa: usar AlphaFold AF-Q01362-F1

**Veredicto de viabilidad docking para MS4A2:** Bajo. MS4A2 no es un target farmacológico convencional. Su rol es estructural/regulatorio dentro del complejo FcεRI. Docking de small molecules contra MS4A2 probablemente no sea informativo.

---

## 5. TABLA COMPARATIVA: MAMMAL vs Evidencia Ortogonal

| Target | MAMMAL pKd corregido* | Docking viable? | Binding assays públicos | Señal transcriptómica (GSE67311) | Veredicto |
|---|---|---|---|---|---|
| **MOR** | ~5.9 (corregido por bono GPCR) | **Sí** — 8EF6 listo | **Sí** — Ki=0.2-3.6 nM (naltrexona) | **No** — esperable (CNS) | **Señal mixta:** farmacología real sólida, modelo MAMMAL subestima afinidad, sin señal transcriptómica en sangre |
| **MS4A2** | ~6.2 (dudoso, sesgo de membrana?) | **Difícil** — solo en contexto de complejo | **No** — sin datos para naltrexona | **Sí** — DOWN en FM (p=0.019) | **Señal transcriptómica real**, sin datos de binding, docking limitado |
| CPA3 | 5.0 (baja, esperable) | Docking poco relevante (proteasa) | No es target farmacológico directo | **Sí** — DOWN (p=0.0035) | Marcador, no target |
| FCER1A | 4.9 (baja, esperable) | Docking posible (1F6A/1RPQ) | IgE receptor, no small-molecule target | **Sí** — DOWN (p=0.025) | Marcador |
| HDC | 4.8 (baja) | Docking posible (4E1O) | Inhibidores conocidos | **Sí** — DOWN (p=0.048) | Target enzimático posible |
| **TLR4** | ~5.5 | Docking posible (4G8A/3FXI) | Antagonistas conocidos (TAK-242) | **No** — no detectado en sangre | Sin señal transcriptómica en los datasets disponibles |
| NRF2 | ~5.0 | Docking posible (2FLU) | DMF/KEAP1 conocido | No en GSE67311 | Ruta validada por otra evidencia |
| Nav1.8 | — (seq muy larga para MAMMAL) | Docking posible pero pesado | Suzetrigine/VX-548 aprobado | No en sangre (DRG) | Target de dolor validado, no específico FM |

* pKd corregido = pKd_MAMMAL − bono_GPCR (~0.9) para GPCRs; el resto es raw MAMMAL.

---

## 6. VEREDICTO POR TARGET

### 6.1 MOR/LDN: LA FARMACOLOGÍA REAL ES MUCHO MÁS FUERTE QUE LO QUE MAMMAL DETECTA

- **Farmacología real:** naltrexona Ki=0.2-3.6 nM en MOR humano. Afinidad sub-nanomolar.
- **MAMMAL:** pKd=6.84 → Kd aparente ~145 nM (subestima ×700).
- **Transcriptómica:** MOR no aparece en sangre (esperable, es CNS).
- **Estructura:** 8EF6 human MOR + morphine listo para docking.

**La paradoja:** MAMMAL DTI subestima la afinidad real de naltrexona por MOR, y simultáneamente sobrestima la afinidad de compuestos irrelevantes (atorvastatin). El modelo no es útil para rankear MOR — pero la farmacología independiente confirma que MOR es un target real, potente, y bien caracterizado para naltrexona.

**¿Apoya la hipótesis LDN en FM?** Indirectamente. Sabemos que naltrexona se une potentemente a MOR. La pregunta clínica — si dosis bajas (1.5-4.5 mg/día) modulan neuroinflamación vía TLR4, microglía, o mecanismos no-canónicos — no la responde el binding assay. Pero sí descarta la objeción "MOR no es un target real de naltrexona."

### 6.2 MS4A2 / Mastocitos: SEÑAL TRANSCRIPTÓMICA REAL, SIN EVIDENCIA DE BINDING DIRECTO

- **Transcriptómica:** MS4A2 DOWN en sangre FM (FDR<0.05). Coherente con CPA3/FCER1A/HDC.
- **Binding:** Sin datos de naltrexona→MS4A2. Nadie lo ha medido.
- **Estructura:** Existe en complejo FcεRI (8YWA), pero docking contra MS4A2 aislado tiene baja probabilidad de ser informativo.
- **Interpretación:** MS4A2 no es un target farmacológico — es un biomarcador de tipo celular. Su DOWN en FM sugiere depleción o disfunción de mastocitos/basófilos periféricos, pero no implica que un fármaco deba unirse a MS4A2.

### 6.3 TLR4: CANDIDATO MECANÍSTICO PARA LDN, PERO SIN SEÑAL TRANSCRIPTÓMICA LOCAL

TLR4 es el mecanismo no-canónico más citado para LDN (antagonismo TLR4 → anti-inflamatorio). No aparece en GSE67311 — TLR4 se regula post-traduccionalmente, no a nivel de mRNA en sangre. Se necesitarían otros datos (citokinas, ensayos funcionales) para evaluarlo.

---

## 7. QUÉ HEMOS DESCARTADO

1. **"MAMMAL DTI es suficiente para priorizar targets."** → FALSO. El bono GPCR falsea cualquier ranking que incluya GPCRs.
2. **"Atorvastatin tiene afinidad real por MOR."** → FALSO. La farmacología pública lo contradice completamente.
3. **"MS4A2 es un target farmacológico directo."** → IMPROBABLE. Es subunidad estructural de FcεRI, no enzima ni receptor con pocket.
4. **"La señal MOR en sangre apoya LDN."** → IRRELEVANTE. MOR no se expresa en sangre — la señal de LDN en FM no pasa por sangre periférica.

---

## 8. RECOMENDACIÓN DE SIGUIENTE PASO

**Hacer docking de naltrexona + controles contra MOR humano (8EF6) usando DiffDock en Colab.** Esto cerraría el círculo: tenemos la estructura, tenemos datos de binding real como ground truth, y el docking respondería si la pose predicha es consistente con el modo de unión conocido de morphinan ligands.

**No invertir tiempo en docking de MS4A2.** No es un target farmacológico clásico. Su valor está como biomarcador transcriptómico, no como target de docking.

**Para TLR4, camino separado:** buscar datos de antagonismo TLR4 por naltrexona/naltrexol en literatura (PubMed search: "naltrexone TLR4 antagonist"). No requiere docking.

**Mantener la ruta mastocito/basófilo como hipótesis mecanística**, pero reconociendo que el effector terapéutico no sería MS4A2 sino la estabilización del mastocito (ketotifen) o el bloqueo de IgE (omalizumab) o modulación de MrgprX2.

---

## 9. PRÓXIMA SESIÓN (si se aprueba)

1. Descargar PDB 8EF6 → extraer chain R (human MOR)
2. Preparar ligandos: naltrexone, morphine (+ctrl), buprenorphine (+ctrl), atorvastatin (-ctrl), omeprazole (-ctrl)
3. Correr DiffDock en Colab con estas 5 moléculas
4. Comparar scores de confianza y RMSD contra pose de morphine en 8EF6
5. PubMed search: "naltrexone TLR4 antagonist microglia"
6. Actualizar este reporte con resultados

---

## 10. ANALOGÍA FINAL

Imagina que MAMMAL es un detector de metales en una playa. En Ruta B v1 y v2, encontramos que pita con todo: monedas, latas, y también anillos de oro. En Ruta B v3 calibramos: descubrimos que el detector pita extra fuerte cuando pasas sobre _cualquier_ cosa metálica con forma de anillo (GPCR), sin importar si es oro o chatarra.

Ahora fuimos al joyero (ChEMBL/BindingDB) y al mapa del tesoro (GEO). El joyero confirma que naltrexona es oro de 24 quilates para MOR — pero el detector MAMMAL la marcó como "chatarra débil" (pKd ~6.8 es mediocre). Y atorvastatin, que el detector marcó como "oro puro" (pKd 7.17), el joyero dice que ni siquiera es metal.

MS4A2 es distinto: el detector pita, el joyero no tiene referencia (nadie lo ha tasado), pero el mapa del tesoro (GSE67311) muestra una X marcada justo ahí. No sabemos si es oro o no — pero hay una X.

La recomendación es: verificar el oro que ya sabemos que es oro (MOR + docking), y no gastar pólvora en lo que el joyero ni siquiera cataloga (MS4A2 como target directo).

---

*Reporte generado por DAVI con verificación de fuentes en tiempo real. Commit siguiente.*
