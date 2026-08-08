
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
