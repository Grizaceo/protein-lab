# Simulaciones de Dinámica Molecular

## Objetivo

Evaluar la estabilidad del cluster Au55 en la posición asimétrica y el impacto de las mutaciones en la estructura de la ferritina.

## Plan de Simulación

1. **Preparación de la estructura**:

   - Utilizar la estructura PDB 1BFR como base.
   - Introducir las mutaciones necesarias (ARG y GLU a CYS).
   - Insertar el cluster Au55 en la posición propuesta.

2. **Configuración de la simulación**:

   - Software: GROMACS o AMBER.
   - Parámetros:
     - Campo de fuerza: CHARMM o AMBER con parámetros personalizados para Au-S.
     - Condiciones: pH 7.4, temperatura 310 K (37°C).
     - Tiempo de simulación: 100 ns.

3. **Análisis**:

   - Evaluar la estabilidad estructural (RMSD, RMSF).
   - Analizar las interacciones Au-S.
   - Determinar la viabilidad del diseño.

## Resultados esperados

- Identificar si el cluster Au55 permanece estable en la posición propuesta.
- Evaluar si las mutaciones afectan la estructura global de la ferritina.

## Próximos pasos

- Ajustar el diseño según los resultados obtenidos.
- Validar experimentalmente los hallazgos.