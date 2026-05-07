# Baseline inicial — Colab diffusion test

## Objetivo
Establecer una corrida base reproducible en Google Colab para el flujo de diseño por difusión de ColabDesign / RFdiffusion, separando claramente:
- configuración usada,
- salidas observadas,
- criterio de selección,
- y próximos pasos de validación.

## Entorno de ejecución
- Plataforma: Google Colab
- Notebook: https://colab.research.google.com/github/sokrypton/ColabDesign/blob/v1.1.1/rf/examples/diffusion.ipynb
- Motivo: las dependencias y el runtime no son adecuados para ejecutarlo de forma estable en la RTX 4060 8GB local.

## Insumo de esta baseline
- Archivo fuente: `../test.result.zip`
- Extracto ordenado: `../raw/`
- Registro técnico: `../doc/README.md`

## Configuración recuperada del run
- `input_pdb`: `/content/RFdiffusion/inference/../examples/input_pdbs/1qys.pdb`
- `contigs`: `['100-100']`
- `num_designs`: `1`
- `design_startnum`: `0`
- `radius`: `10.0`
- `T`: `50`
- `b_0`: `0.01`
- `b_T`: `0.07`
- `write_trajectory`: `True`
- `scaffold_guided`: `False`
- `align_motif`: `True`
- `symmetric_self_cond`: `True`
- `guide_scale`: `10`

## Salidas principales
- `outputs/test/design.fasta`
- `outputs/test/mpnn_results.csv`
- `outputs/test/best.pdb`
- `outputs/test/best_design0.pdb`
- `outputs/test/all_pdb/`
- `outputs/test_0.trb`
- `outputs/traj/`

## Resultados resumidos
- Diseños generados: 8
- Mejor pLDDT: diseño 1, ~0.935
- Mejor pTM: diseño 1, ~0.792
- Menor PAE: diseño 1, ~3.210
- Mejor ProteinMPNN: diseño 7, ~1.081
- Menor RMSD: diseño 3, ~0.417

## Regla de selección provisional
Para decidir cuál diseño avanza a la siguiente ronda, usar este orden:
1. pLDDT alto
2. PAE bajo
3. pTM alto
4. ProteinMPNN alto
5. RMSD bajo

Candidato preferente inicial:
- Diseño 1: mejor balance estructural global.

Candidato alternativo:
- Diseño 7: mejor score de ProteinMPNN, útil como comparación.

## Qué hace que esta corrida sea la baseline
Esta corrida sirve como baseline porque:
- completó sin errores aparentes,
- produjo múltiples candidatos,
- generó archivos de trazabilidad (`.trb`, PDBs, CSV, FASTA),
- y permite comparar cualquier corrida futura contra una referencia concreta.

## Qué comparar en la siguiente corrida
Cuando salgan nuevos resultados, comparar contra esta baseline:
- número de diseños totales,
- distribución de pLDDT / pTM / PAE / RMSD,
- estabilidad del mejor candidato,
- consistencia entre secuencias y estructuras,
- reproducibilidad bajo la misma semilla o una semilla cercana.

## Criterio para avanzar
Una nueva corrida supera esta baseline si:
- mantiene o mejora pLDDT y pTM del mejor candidato,
- no empeora de forma marcada PAE o RMSD,
- y produce al menos un candidato claramente más estable o más útil para el objetivo biológico.

## Siguiente paso sugerido
1. Repetir exactamente el notebook en Colab.
2. Guardar la salida con un nuevo timestamp.
3. Comparar side-by-side con esta baseline.
4. Solo después pasar a diseño dirigido por target/scaffold.
