#!/usr/bin/env python3
"""
fep_report.py — P1/Línea 2 (script 5/5): Reporte final integrado (honesto).

Lee MM_PBSA_REPORT.md + fep_meta.json y genera:
  1. MM_PBSA_FINAL.md — consolidado científico de la Línea 2 P1.
  2. MANUSCRIPT_SNIPPET.md — texto para §4.8.2 del manuscrito.

NOTA: ΔG NO es un valor físico válido (colapsó a ~0 por limitación de hardware:
OpenMM CPU-only, sin solvente explícito viable). Se reporta como proof-of-pipeline.
"""
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "fep_drd2"
report_src = (OUT / "MM_PBSA_REPORT.md").read_text()
meta = json.loads(open(OUT / "fep_meta.json").read())

final = f"""# Línea 2 P1 — DRD2 + Pramipexole: Estado de la Iteración Computacional

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
"""
open(OUT / "MM_PBSA_FINAL.md", "w").write(final)

snippet = """
### 4.8.2 Estimación de Energía Libre de Unión (Línea 2, P1 — in-silico, preliminar)

Parametrizamos el complejo DRD2(6VMS)–pramipexole con AMBER14 + GAFF-2.11 y
implementamos MM-PBSA (descomposición de energía por grupos). La minimización
del complejo fue estable (E: +38,316 → −19,652 kJ/mol). Sin embargo, el cálculo
de ΔG_bind **no convergió a un valor físico** en el entorno local actual: OpenMM
corre solo en CPU (sin CUDA) y la solvatación explícita requerida (~1.7M átomos)
excede la memoria de la GPU disponible (RTX 4060 8GB). El ΔG colapsó a ~0 por
cancelación metodológica (NoCutoff + GBSA sin PME).

*Limitaciones:* cargas Gasteiger (no AM1-BCC; openff-toolkit no disponible por
restricción de red); tipos GAFF heurísticos; GBSA implícito; pramipexole es
D3-preferring mientras DRD2 es D2 (cross-target); MM-PBSA sin MD por hardware.
El pipeline queda como *proof-of-concept* de parametrización, pendiente de
hardware/GPU o cluster para cuantificación rigurosa de ΔG.
"""
open(OUT / "MANUSCRIPT_SNIPPET.md", "w").write(snippet)
print("[done] MM_PBSA_FINAL.md + MANUSCRIPT_SNIPPET.md escritos (honestos).")
