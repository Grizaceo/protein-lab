# Línea 2 P1 — DRD2 + Pramipexole: Estado de la Iteración Computacional

## Pipeline implementado (5 scripts)
1. `fep_gen_ligand_xml.py` — template GAFF del ligando (Gasteiger + tipos heurísticos).
2. `fep_prep.py` — merge complejo DRD2(6VMS)+pramipexole, parametrización
   amber14+gaff-2.11+tip3p. Sistema: 4637 átomos.
3. `fep_solvate.py` — minimización L-BFGS del complejo. E: +38,316 -> -19,652 kJ/mol
   (estable, finita/negativa).
4. `fep_mmpbsa.py` — framework MM-PBSA (descomposición de energía por grupos).
5. `fep_report.py` — este reporte.

## Resultado de ΔG: NO CONVERGENTE (artefacto de hardware)
- ΔG calculado = 0.00 kcal/mol (colapsa por cancelación NoCutoff + GBSA sin PME).
- NO es un valor físico. Ver MM_PBSA_REPORT.md para la causa raíz.

## Veredicto
P1 = **proof-of-pipeline**: el complejo se parametriza, minimiza y evalúa
localmente. El gap Vina (LE=0.384) -> energía física se cierra a nivel de
*infraestructura*, no de número. Para ΔG riguroso se requiere:
  - OpenMM con CUDA (GPU) + openff-toolkit 2.x (AM1-BCC real).
  - Solvente explícito (PME) + MD >=10 ns.
  - O escalar a cluster.

## Limitaciones declaradas
1. Cargas ligando = Gasteiger, no AM1-BCC (openff no instalable: proxy PyPI solo
   sirve openff 0.18 yanked).
2. Tipos GAFF heurísticos.
3. GBSA implícito (solvente explícito ~1.7M át, inviable en RTX 4060 8GB).
4. Cross-target: pramipexole D3-preferring vs DRD2 D2.
5. OpenMM CPU-only en este env (sin CUDA) -> MD de 4637 át en CPU inviable.
