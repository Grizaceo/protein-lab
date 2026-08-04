# P1: TACR1 (NK1) DOCKING — APREPITANT, ROLAPITANT, SUSTANCIA P

**Fecha:** 2026-08-04
**Objetivo:** Validar docking contra TACR1 (receptor de sustancia P, segundo neurotransmisor más implicado en FM)
**Receptor:** AlphaFold P25103 (pLDDT 78.4, mejor estructura de los 5 targets FM)
**Pocket:** Residuos clave NK1: D78, Y92, T205, Y272, F288, N305 (Ballesteros-Weinstein GPCR numbering)

---

## Resultados

| Ligando | ΔG (kcal/mol) | Ki estimado (µM) | Clase |
|---------|---------------|-------------------|-------|
| Rolapitant | -6.7 | 12.3 | Moderado |
| Sustancia P (1-4 fragmento) | -5.3 | 138 | Débil (peptídico) |
| Aprepitant | -3.2 | 4398 | Pobre (ver análisis) |

## Análisis

### Rolapitant (-6.7 kcal/mol, Ki 12 µM)
NK1 antagonist clínico (antiemético, aprobado FDA 2015). Moderado en nuestro docking. Rolapitant es más rígido que aprepitant (menos centros estereoquímicos flexibles), lo que favorece docking con scoring function simplificada de Vina.

### Sustancia P fragmento 1-4 (-5.3, Ki 138 µM)
RPKP (Arg-Pro-Lys-Pro) — fragmento N-terminal de sustancia P. Unión débil esperada: es un péptido, altamente flexible, pocos contactos en pocket rígido. La sustancia P endógena completa (11 aa) es demasiado grande para Vina standard.

### Aprepitant (-3.2, Ki 4.4 mM) — ANÓMALO
Aprepitant es NK1 antagonist de alta afinidad experimental (Ki ~0.1-1 nM). Nuestro score es ~1000x más débil. Causas identificadas:

1. **Receptor PDBQT sin cargas AD4.** obabel no asigna cargas parciales. Sin H-bond directionality scoring, aprepitant (que tiene 3 H-bond acceptors críticos) se scored mal.
2. **Aprepitant es altamente flexible.** 4 centros estereoquímicos + morfolinico ring, múltiples conformeros. Vina rígido no captura esto.
3. **AlphaFold apo state.** TACR1 en AlphaFold está en conformación inactiva (sin ligando). Aprepitant estabiliza la conformación antagonista via induced fit que no está modelado.
4. **Sin estructura experimental TACR1 humana.** No hay PDB con aprepitant bound para validar el pocket directo.

## Limitaciones honestas

1. **P1 confirma que AlphaFold + obabel + Vina funciona para ranking aproximado pero pierde precisión en antagonistas flexibles de alta afinidad.** Rolapitant (más rígido) se scored mejor que aprepitant (más flexible), contradiciendo la realidad experimental (aprepitant > rolapitant).
2. **Para TACR1 sin PDB experimental, no podemos validar el pocket directamente.** El pocket center se estimó por residuos clave de literatura (Ballesteros-Weinstein numbering), no por ligando cristalográfico.
3. **Docking rígido sin induced fit es insuficiente para antagonist design.** AlphaFold 3 / Protenix (P4) resolverían esto.

## Conexión con FM

- Sustancia P elevada en CSF de FM (Russell 1994, PMID 7526868)
- TACR1 upregulated en PBMC (d=+0.60, nuestro análisis)
- Pero: eje opioide + substance P sufre confound composicional (E1: 0/7 genes sobreviven deconvolución)
- TACR1 NK1 antagonists (aprepitant) fallaron en trials de FM pain
- **Veredicto TACR1: target estructural más confiable que DRD2 (pLDDT 78.4), pero relevancia FM más contaminada por confound composicional.** Rolapitant y aprepitant son ensayos negativos en FM (no efficacy), consistente con этой confound.

## Comparación P0 vs P1

| Aspecto | P0 (DRD2) | P1 (TACR1) |
|---------|-----------|------------|
| Receptor | 6VMS + AlphaFold P14416 | AlphaFold P25103 solo |
| pLDDT | 72.4 | 78.4 (mejor) |
| Validación pocket | 08Y crystal ligand | Residuos literarios |
| Ranking preservado | SÍ | PARCIAL (rolapitant > aprepitant, real es aprepitant > rolapitant) |
| Mejor ligando | Bromocriptine -9.4 | Rolapitant -6.7 |
| Dopamina vs SP | Dopamina endógena débil como esperado | SP fragmento débil como esperado |

## Conclusión P1

El pipeline funciona mejor con estructuras experimentales (P0) que con AlphaFold solo (P1). El ranking de TACR1 se invirtió para aprepitant vs rolapitant — aprepitant altamente flexible sin induced fit se scored peor de lo que es. Esto limita el screening de antagonistas flexibles con Vina rígido.

**Próximo paso (P2):** OPRM1 (opioide mu) docking con beta-endorfina y encefalinas — pero ojo con el confound composicional (E1).
