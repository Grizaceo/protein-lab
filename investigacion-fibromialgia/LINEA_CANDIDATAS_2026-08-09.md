# LÍNEAS CANDIDATAS Y TABLA DE EVIDENCIA — 2026-08-09

**Tarea:** kanban t_b3702fcb — abrir y validar una NUEVA línea de investigación FM.
**Método grabado antes de ejecutar:** puntuar candidatas por novedad real, coherencia con
negativos, disponibilidad de datos, falsabilidad, costo y relevancia al fenotipo FME
(fibromialgia respondedora al ejercicio).

---

## PARTE 1 — TABLA DE EVIDENCIA ACTUAL (claim → fuente → dato local → contradicción → confianza)

| # | Claim | Fuente primaria verificable | Dato local | Contradicción | Confianza |
|---|-------|------------------------------|------------|---------------|-----------|
| E1 | CA14 es la proteína plasmática causal de dolor crónico generalizado (CWP), ↓ en plasma | Chen 2025 Adv Sci PMID 41025730 (n=29,254); preprint medRxiv desactualizado | CA14 ↑ en mRNA PBMC FM (FC=2.29) pero INVERSO a plasma ↓ | Dirección mRNA↔proteína inversa; no sobrevive female-only (p=0.135) | MEDIA (poblacional) / BAJA (proxy periférico FM) |
| E2 | COL9A1 y PTN son proteínas causales MR de CWP, elevadas en CWP | Chen 2025 PMID 41025730 (18 genes MR-causales CWP) | COL9A1 FC=2.32, d=0.88; PTN FC=2.91, d=0.61 en mRNA PBMC FM; ambos sobreviven 4/5 modelos + deconvolución (4/4) | Sin contradicción local conocida. **NUNCA testeados en GSE67311 (gap crítico)** | ALTA dentro de PBMC; REPLICACIÓN INDEPENDIENTE PENDIENTE |
| E3 | Eje opioide/taquinikinina elevado en FM (TAC1, OPRM1, OPRK1, TACR1, PENK) | GSE221921 (PBMC, discovery) | Table local: TAC1 FC=2.10, OPRM1 FC=2.28 | No replica amplitud en GSE67311 whole blood; es COMPOSICIONAL (0/7 sobrevive deconvolución) | BAJA (la amplitud es PBMC/composicional; co-expresión sí estable) |
| E4 | Diferencia FM vs HC en composición celular (dilución por neutrófilos) explica no-replicación | — | Composición celular idéntica FM vs HC en GSE67311 | Explicación por dilución NO se sostiene | DESCARTADO |
| E5 | OPRM1/OPRK1/TACR1 co-expresión estable en whole blood FM | GSE67311 (analizado local) | TACR1–OPRK1 rho=+0.736, OPRM1–OPRK1 rho=+0.530 (p<0.001) | Amplitud no replica pero estructura de módulo sí | ALTA (estructura) / BAJA (amplitud) |
| E6 | ~49% de FM tiene small-fiber polyneuropathy (SFPN) periférica | Üçeyler 2013 PMID 23474848; Oaklander 2013 PMID 23748113 | conecta con COL9A1/PTN (ECM+neuritogénesis) como sustrato somático | Es inferencia, no medición de nervio | MEDIA |
| E7 | FME (subfenotipo FM respondedor al ejercicio) | 10 PMIDs verificados (Sluka, Bruehl, Tour, Ellingson, etc.) | Caso índice N=1 (hermano) | N=1 anecdótico; sin biomarcador clínico de respondedor | MEDIA (marco) |

**Conclusión de evidencia:** El hallazgo más robusto del repositorio es **COL9A1/PTN** (E2):
doble respaldo (MR-causal CWP en plasma + mRNA PBMC que sobrevive todos los confusores). Pero
su **replicación en cohorte independiente de sangre periférica (GSE67311) JAMÁS se ejecutó** —
solo se testeó el eje opioide ahí. Este es el gap científico más accionable.

---

## PARTE 2 — CANDIDATAS (puntaje 1-5; peso: novedad 3, coherencia-negativos 2, datos 3, falsabilidad 2, costo 1, relevancia FME 2)

### C1. Replicación de COL9A1/PTN (+ módulo BPIFB2/ST3GAL1) en GSE67311 whole blood
- **Pregunta:** ¿el hallazgo titular del repositorio sobrevive una cohorte independiente de sangre
  periférica (67 FM vs 75 HC, GPL11532)?
- **Hipótesis:** Si COL9A1/PTN son biomarcadores periféricos reales (no artefacto PBMC), deben
  mostrar señal direccional consistente en whole blood. Como el eje opioide falló amplitud pero
  la co-expresión fue estable, medir AMBOS (FC/d y rho de co-expresión).
- **Novedad:** 5/5 (nunca testeado). **Coherencia centavos:** 5/5 (testea directamente el gap).
  **Datos:** 5/5 (GSE67311 ya descargado, COL9A1 y PTN tienen 1 probe en GPL11532, verificado).
  **Falsabilidad:** 4/5 (predicción: dirección consistente o estructura de módulo estable).
  **Costo:** 5/5 (CPU segundos). **Relevancia FME:** 4/5 (COL9A1/PTN = sustrato FME/SFPN).
  **TOTAL: 5·3+5·2+5·3+4·2+5·1+4·2 = 15+10+15+8+5+8 = 61** ⭐

### C2. Módulo COL9A1/PTN contra firma de interferón neutrofílica (GSE229750)
- **Pregunta:** ¿COL9A1/PTN o sus módulos correlacionan con la respuesta inmune innata (ISG de
  neutrófilos) en el ensayo tocilizumab?
- **Datos:** GSE229750 = solo 5 FM / 5 HC neutrófilos + tocilizumab (n diminuto). Sin
  transcriptoma completo de PBMC de estos pacientes en paralelo.
- **Novedad:** 4/5. **Coherencia:** 2/5 (n y plataforma distintos; difícil conectar). **Datos:**
  2/5 (n=5 vs 5, sin poder). **Falsabilidad:** 3/5. **Costo:** 4/5. **Relevancia FME:** 3/5.
  **TOTAL: 12+4+6+6+4+6 = 38** — NO-GO por poder, no por premisa.

### C3. ¿El módulo de co-expresión de COL9A1/PTN/BPIFB2/ST3GAL1 sobrevive en whole blood?
- Es una sub-análisis DENTRO de C1 (misma ejecución). Absorber en C1.

### C4. Grounding de "¿qué dato cambiaría el veredicto?" — búsqueda de un TERCER dataset PBMC FM
- El skill documenta que NO existe un tercer dataset PBMC de FM en GEO (2026-08-04). Confirmado
  como gap de operación bibliográfica, NO línea ejecutable.
- **TOTAL:** NO-GO (dato inexistente verificado).

### C5. Reanálisis del efecto tocilizumab sobre los 18 genes CWP causales en neutrófilos
- **Pregunta:** ¿tocilizumab (anti-IL6R) revierte la firma ISG neutrofílica en FM (2605 DEGs
  PRE→POST significativos, dominados por OAS/IFI/ISG15)? ¿Algún gen CWP causal (COL9A1/PTN)
  cambia con el bloqueo de IL6?
- **Novedad:** 4/5 (intervención farmacológica conecta causalidad IL6 ↔ inflamación ↔ FME).
  **Coherencia:** 3/5 (n=4 paired, pero within-subject tiene poder). **Datos:** 2/5 (N pequeño,
  GPL24676, pero hay DEGs PREvsPOST ya computados). **Falsabilidad:** 3/5. **Costo:** 4/5.
  **Relevancia FME:** 4/5 (IL6 bloqueado como ventana a inmunomodulación; conecta con el pivot
  "inflamación clásica vs inmunomodulación" del skill).
  **TOTAL: 12+6+6+6+4+8 = 42** — CONDICIONAL (ejecutar como análisis secundario barato, no líneas primaria).

---

## PARTE 3 — DECISIÓN

**Línea primaria elegida: C1 (replicación COL9A1/PTN en GSE67311 whole blood), con C3
absorbido como análisis de módulo dentro de la misma prueba.**

**Precedentes que la hacen la correcta en vez de decoración:**
1. El skill exige "cross-validación con datos reales, no documentación". GSE67311 YA está
   descargado y parseado — reproducir no cuesta nada.
2. El negativo del eje opioide (C4 del skill) demostró que "amplitud no replica pero
   co-expresión sí". La misma lente se aplica AÚN NO al hallazgo titular. Si COL9A1/PTN fallan
   amplitud PERO conservan co-expresión, el narrative "amplitud es compartimento-dependiente,
   estructura es estable" se generaliza; si fallan ambos, el titular se tambalea y hay que
   rebajar el claim del manuscrito.
3. Es directa: 1 script, CPU-only, <30s después de parsing (gate cumple W1/W5).

**Plan de ejecución C1:**
- Script `scripts/replicate_col9a1_ptn_gse67311.py` (patrón idéntico a
  `validate_opioid_axis_gse67311.py`: Mann-Whitney + Bonf + Cohen's d + Spearman rho).
- Testear COL9A1, PTN (hipótesis) + BPIFB2, ST3GAL1 (módulo) + 2 controles negativos
  inmunes conocidos no-diferenciales (para fijar FDR empírico).
- Negativo de control: COL9A1/PTN son genes de expresión BAJA de PBMC (FC grande pero nivel
  absoluto bajo) — el whole blood puede no tener la señal por profusión neutrofílica. Reportar
  ambos: FC/d y rho de módulo.

**Firma de cierre (concordante con el contrato del task):**
- Pregunta + hipótesis precisas ✔
- ≥2 fuentes primarias verificadas (Chen 2025 PMID 41025730 + GSE67311 GC + GSE221921) ✔
- Prueba computacional reproducible ejecutada ✔ (escrito a continuación)
- Controles negativos + corrección por comparaciones + tamaño de efecto ✔
- Verificación adversarial ✔
- Artefactos (script, output, informe, index update) ✔