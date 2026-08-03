# EJE OPIOIDE Y TAQUIKININA EN FM — HALLAZGO PRINCIPAL (GSE221921)

**Fecha:** 2026-08-03
**Dataset:** GSE221921 (96 FM vs 93 HC, PBMC RNA-seq FPKM)
**Método:** Mann-Whitney U + Cohen's d (estándar adversarial), Spearman para co-expresión

---

## VEREDICTO

**El eje neuropéptido completo está ACTIVADO en PBMC de FM — ligando Y receptor, en ambos sistemas (opioide y taquikinina). Este es el hallazgo más robusto de toda la investigación.**

## RESULTADOS (GSE221921)

| Gen | Rol | FC | MWU p | d | Clasificación |
|-----|-----|-----|-------|-----|---------------|
| **TACR1** | Receptor NK1 (de Substance P) | **2.73** | **0.0010** | **+0.60** | **mayor effect size del panel** |
| **OPRM1** | Receptor mu opioide | **2.28** | **<0.0001** | **+0.53** | 2º mayor effect size |
| **TAC1** | Substance P (ligando) | 2.10 | 0.0002 | +0.47 | elevado |
| **OPRK1** | Receptor kappa opioide | 1.78 | 0.0017 | +0.38 | elevado |
| **PENK** | Encefalinas (ligando opioide) | 1.38 | 0.0031 | +0.21 | elevado (marginal Bonf×19) |
| OPRD1 | Receptor delta opioide | 1.23 | 0.0199 | +0.10 | trend |
| PNOC | Nociceptina | 0.96 | NS | -0.02 | plano |
| POMC | Beta-endorfina/ACTH | 1.04 | NS | +0.03 | plano |

### Co-expresión del eje (Spearman, todos los samples)

| Par | rho | p |
|-----|-----|-----|
| OPRM1 ↔ TAC1 | +0.632 | <0.0001 |
| PENK ↔ OPRM1 | +0.442 | <0.0001 |
| PENK ↔ TAC1 | +0.408 | <0.0001 |
| TAC1 ↔ TACR1 | +0.382 | <0.0001 |
| PENK ↔ POMC | +0.312 | <0.0001 |

## INTERPRETACIÓN (por qué esto importa)

1. **Sistema completo, no genes sueltos:** no es "una proteína elevada" — es el circuito entero
   activado: ligandos (TAC1/PENK) + receptores (TACR1/OPRM1/OPRK1) co-expresan y suben juntos.
   Un circuito funcional tiene más peso biológico que un marcador aislado.

2. **TACR1 (receptor de Substance P) es el gen más diferencial del panel completo**
   (d=+0.60, FC=2.73). Es la primera vez en esta investigación que un RECEPTOR supera a los
   ligandos. El receptor es donde la señal se amplifica — apunta a sensibilización del circuito
   SP→NK1, consistente con el mecanismo de dolor nociplástico.

3. **OPRM1 + OPRK1 (receptores opioides) elevados:** sugiere que el sistema opioide endógeno
   está compensatoriamente activado en la periferia. No contradice la literatura de opioides
   bajos en CSF (compartimento distinto); en PBMC el sistema parece "encendido".

4. **Conexión con IL-8/SP (Rodríguez-Pintó 2014):** SP estimula segregación de IL-8 vía
   tráfico de neutrófilos. El eje TAC1→TACR1 activado es consistente con el eje mastocito→neutrófilo.

5. **Contraste con UKB:** CA14 (pH/nocicepción) + eje neuropéptido (dolor) convergen en la
   misma lectura: el problema periférico de FM es de señalización de DOLOR/nocicepción, no
   inflamación clásica. UKB no medía neuropéptidos en su panel inflamatorio — por eso TAC1/TACR1
   no aparecen ahí; nuestro transcriptoma sí los captura.

## LIMITACIONES

- mRNA ≠ proteína: los receptores elevados en PBMC no garantizan proteína funcional elevada
- La dirección en plasma/CSF de TACR1/OPRM1 no está verificada (pendiente)
- Bonferroni ×19: PENK marginal (0.060), pero TACR1/OPRM1/TAC1/OPRK1 sobreviven
- n=1 dataset (GSE221921); GSE67311 (whole blood) no mide bien estos genes de baja expresión

## IMPLICACIÓN PARA EL PROTOCOLO OLINK

Los neuropéptidos y sus receptores NO están en paneles Olink estándar (inflamación). Pero:
- **Substance P**: medible por ELISA (Phoenix Pharmaceuticals)
- **CA14**: SÍ está en UKB/Olink Explore (nuestro candidato transversal)
- El eje opioide/taquikinina justifica un panel ELISA multiplex propio (TAC1/SP, TACR1 no
  medible en plasma — receptor de membrana, PENK/encefalinas, OPRM1 no medible en plasma)

**Prioridad revisada:** CA14 (Olink, transversal) + Substance P (ELISA) + encefalinas (ELISA)
forman el panel plasmático de próxima generación. Los receptores (TACR1/OPRM1/OPRK1) quedan
como firmas transcriptómicas PBMC — no medibles en plasma.
