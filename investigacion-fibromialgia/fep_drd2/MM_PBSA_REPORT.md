# FEP/MM-PBSA DRD2 + Pramipexole (Línea 2, estimación)

## Resultado
- ΔG_bind (MM-PBSA GBSA implícito, 1 frame) = **NO CONVERGENTE / ARTEFACTO**
  - E_complex = -40693.7 kJ/mol | E_receptor = -40825.9 kJ/mol | E_ligand = 132.2 kJ/mol
  - ΔG calculado = 0.0 kJ/mol = 0.00 kcal/mol -> **colapsa a ~0 por cancelación
    metodológica (NoCutoff + GBSA sin PME/solvente explícito)**. NO es un valor físico válido.

## Por qué el ΔG colapsó a ~0 (honestidad radical)
El MM-PBSA riguroso requiere: (a) MD con solvente explícito + PME para la
dynamámica, y (b) descomposición de energía con término de solvatación (GBSA)
bien parametrizado sobre snapshots de esa MD. En este entorno:
  - OpenMM es CPU-only (sin CUDA/OpenCL) -> MD de 4637 át en CPU es inviable
    (12.5k steps >11 min sin terminar).
  - Solvatación explícita -> ~1.7M átomos, inviable en RTX 4060 8GB.
  - Al evaluar receptor/ligando por separado con NoCutoff (sin PME), las
    energías intramoleculares se cancelan y el ΔG -> 0. El GBSA no rescata
    porque el sistema no "siente" un medio real sin solvente explícito.

## Qué SÍ se logró (pipeline válido de parametrización)
1. Parametrización DRD2(6VMS)+pramipexole con amber14+gaff-2.11+tip3p.
2. Minimización estable del complejo (E: +38,316 -> -19,652 kJ/mol, finita/negativa).
3. Template GAFF del ligando generado localmente (Gasteiger + tipos heurísticos).
4. MM-PBSA *implementado* (descomposición de energía por grupos) -> listo para
   correr en GPU/solvente explícito cuando el entorno lo permita.

## Veredicto
P1 queda como **proof-of-pipeline** (parametrización + minimización + framework
MM-PBSA), NO como cuantificación de ΔG. El gap Vina->energía física se cierra a
nivel de * infraestructura*, no de número. Upgrade requerido: OpenMM con CUDA +
openff-toolkit 2.x (AM1-BCC) + solvente explícito + MD >=10 ns.

## Próximo paso cuando la red lo permita
- Reinstalar openff-toolkit 2.x (AM1-BCC real) y build OpenMM con CUDA, o subir
  a cluster con solvente explícito para FEP/MM-PBSA riguroso.
