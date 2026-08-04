# AUDITORÍA DE LIGANDOS — campaign de docking (paper 2)

**Fecha:** 2026-08-04
**Alcance:** los 11 ligandos de referencia de `docking_fm_targets/docking_FM_targets_GPCR.md` v1.1
**Método:** validación de fórmula molecular de cada `.sdf` guardado contra la fórmula publicada del compuesto, más inspección de la composición atómica de las poses realmente dockeadas.

---

## VEREDICTO

**10 de 11 ligandos son moléculas incorrectas.** Solo morfina es correcta.

Todos los valores de ΔG de §3.1, §3.2 y §3.3 del paper 2 corresponden a compuestos que no son los declarados. **El paper 2 no es publicable en su estado actual.**

---

## 1. Evidencia — fórmulas

| ligando | fórmula en `estructuras/ligandos/*.sdf` | fórmula real | MW hallada | MW real | |
|---|---|---|---|---|---|
| morphine | C17H19NO3 | C17H19NO3 | 285.3 | 285.3 | ✅ |
| dopamine | C8H11NO | C8H11NO2 | 137.2 | 153.2 | ❌ falta un OH — es tiramina, no dopamina |
| pramipexole | C15H18N2 | C10H17N3S | 226.3 | 211.3 | ❌ sin azufre; pramipexol es un benzotiazol |
| bromocriptine | C18H15NO2 | C32H40BrN5O5 | 277.3 | 654.6 | ❌ sin bromo; MW menos de la mitad |
| fentanyl | C23H29N3O | C22H28N2O | 363.5 | 336.5 | ❌ N y C de más |
| met-enkephalin | C24H35N5O7 | C27H35N5O7S | 505.6 | 573.7 | ❌ sin azufre (la metionina lo tiene) |
| leu-enkephalin | C24H35N5O7 | C28H37N5O7 | 505.6 | 555.6 | ❌ |
| naloxone | C21H17NO3 | C19H21NO4 | 331.4 | 327.4 | ❌ |
| aprepitant | C26H33NO6 | C23H21F7N4O3 | 455.6 | 534.4 | ❌ **cero flúor** (define el compuesto) |
| rolapitant | C25H25F3N2 | C25H26F6N2O2 | 410.5 | 500.5 | ❌ 3 F en vez de 6, sin oxígenos |
| substance P (1-4) | C25H50N12O5 | C22H41N7O5 | 598.8 | 483.6 | ❌ |

**Señal de alerta que debió detectarse antes:** met-encefalina y leu-encefalina tienen **fórmulas idénticas** en los archivos guardados (C24H35N5O7). Son péptidos distintos; no pueden compartir fórmula.

## 2. Evidencia — poses dockeadas

La composición atómica de las poses confirma que el docking se corrió con estas moléculas incorrectas, no solo que los SDF estén desactualizados:

```
dopamine_drd2_docked        6A 3HD 2C 1OA 1NA     <- 1 oxígeno, debe tener 2
bromocriptine_drd2_docked   14A 4C 2OA 1N 1HD     <- sin Br
pramipexole_drd2_docked     9A 6C 1NA 1N 1HD      <- sin S
aprepitant_TACR1_docked     20C 6OA 6A 1N 1HD     <- sin F, 1 N (debe tener 4)
```

Búsqueda exhaustiva sobre las 14 poses del repositorio: **ninguna contiene bromo ni azufre.**

## 3. Magnitud del error — re-docking con ligandos validados

Ligandos reconstruidos desde SMILES de PubChem, validados por fórmula y MW, optimizados con MMFF94/RDKit. Receptor, caja y semilla idénticos; AutoDock Vina 1.2.5, exhaustiveness 32.

| ligando | ΔG publicado | ΔG con ligando correcto | diferencia |
|---|---|---|---|
| aprepitant (TACR1) | −3.2 | **−10.12** | **6.9 kcal/mol** |
| rolapitant (TACR1) | −6.7 | **−10.21** | 3.5 kcal/mol |
| naloxone (OPRM1) | "FALLO" / −10.42 | **−9.44** | — |

Control descartando la caja como causa: con el centro de caja original ([5.15, 0.50, −9.00], inferido del centroide de las poses viejas) el aprepitant validado da **−10.27**. Con el centro derivado de los residuos del pocket ([−1.28, −1.34, −7.82]) da −10.12. **La caja no era el problema; el ligando sí.**

Firma diagnóstica adicional: el aprepitant incorrecto producía 9 modos de los cuales **8 tenían afinidad positiva** (+0.35 a +4.05 kcal/mol, es decir choque estérico). El aprepitant correcto produce 9 modos, todos negativos (−10.12 a −6.47). Una corrida cuyos modos son mayoritariamente positivos es un indicador de ligando mal preparado y debería tratarse como fallo, no como resultado.

---

## 4. Claims del paper 2 que caen

1. **§3.2 — "Ranking partially inverted vs experiment"** (rolapitant mejor que aprepitant). Con ligandos correctos: aprepitant −10.12 vs rolapitant −10.21, prácticamente empatados. No hay inversión. La explicación que daba el paper (cargas AD4 ausentes, flexibilidad, estado apo de AlphaFold) explicaba un artefacto.

2. **§4.1 y abstract — la tesis de los enlaces rotables.** Introducida en el commit `12b5e95` de hoy a partir de la corrección de naloxona, con aprepitant como dato principal ("off by ~9 kcal/mol"). Con el ligando correcto el error es de ~2–3 kcal/mol, dentro del error normal de Vina. **La tesis pierde su punto de apoyo y queda falsada.** También los MW que se tabularon ahí (aprepitant 516, rolapitant 485) provenían de SMILES no validados; los correctos son 534.4 y 500.5.

3. **§3.1 y §3.3 — "Ranking preserved"** (bromocriptina > pramipexol > dopamina; morfina > encefalinas). El orden puede o no sostenerse, pero no está demostrado: esas no son esas moléculas. Morfina es el único punto de anclaje válido.

4. **§3.5 — validación in silico de la biblioteca de novo.** Corrió por el mismo pipeline de preparación de ligandos; requiere re-verificación independiente.

Los resultados que **no** dependen de este pipeline y siguen en pie: el mapeo de determinantes de selectividad DRD2/DRD3 por alineamiento estructural (§3.4), y el QSAR/Transformer entrenados sobre ChEMBL (§3.6), cuyo insumo son SMILES de ChEMBL, no ligandos preparados localmente.

---

## 5. Causa raíz probable

Los SMILES se generaron sin validación de fórmula. Los errores son del tipo que produce escribir un SMILES de memoria: falta un hidroxilo (dopamina→tiramina), falta el heteroátomo del núcleo (pramipexol sin S, met-encefalina sin S), falta el halógeno característico (bromocriptina sin Br, aprepitant sin F).

**Control mínimo que lo habría evitado:** comparar `rdMolDescriptors.CalcMolFormula(mol)` contra la fórmula de PubChem antes de dockear. Cuesta una línea por ligando.

---

## 6. Recomendación

1. **No someter paper 2.** Marcarlo como retenido hasta re-correr.
2. Re-preparar los 11 ligandos desde SMILES de PubChem/ChEMBL con validación obligatoria de fórmula y MW.
3. Re-dockear los tres receptores y regenerar §3.1–§3.3 y §3.5.
4. Añadir al pipeline un gate que rechace cualquier ligando cuya fórmula no coincida con la referencia, y que trate como fallo toda corrida con mayoría de modos positivos.
5. Re-evaluar §4.1 con los datos nuevos: la tesis de la flexibilidad puede seguir siendo cierta, pero hay que probarla de nuevo.

El paper 1 (transcriptómica) **no está afectado** — no comparte pipeline ni datos con este campaign.
