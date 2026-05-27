# Estrategia 3 — GTEx: Distribución normal de DRD2/MDGA2

**Fecha:** 2026-05-27
**Dataset:** GTEx v8, 948 donantes sanos post-mortem, 54 tejidos
**Métrica:** Mediana de TPM por gen y tejido

## Hallazgo principal

**DRD2 y MDGA2 son INDETECTABLES (TPM = 0) en sangre periférica de donantes sanos.**

Esto contrasta con los valores reportados en GSE221921:
- DRD2: FM 0.72 FPKM, HC 0.27 FPKM
- MDGA2: FM 2.58 FPKM, HC 1.07 FPKM

## Implicaciones

1. **Si GTEx es correcto** (TPM=0 en sangre sana), entonces la señal en GSE221921 podría deberse a:
   - Diferencias técnicas (FPKM vs TPM, pipeline de cuantificación)
   - Diferencias poblacionales (GTEx: mayoría caucásica/afroamericana EEUU; GSE221921: cohorte india)
   - Contaminación o artefacto de biblioteca en GSE221921
   - O BIEN: la expresión de DRD2/MDGA2 en PBMCs está realmente elevada en FM (los HC de GSE221921 también tienen valores bajos pero detectables: 0.27 y 1.07 FPKM)

2. **Si GSE221921 es correcto**, DRD2/MDGA2 SÍ se expresan a niveles bajos pero detectables en PBMCs, y GTEx simplemente no los captura (diferente pipeline, límite de detección más alto, donantes post-mortem con posible degradación).

3. **En ambos casos**, la expresión en sangre es órdenes de magnitud menor que en cerebro (DRD2: 40-52 TPM en caudado/putamen). Esto es esperado para un gen de expresión principalmente neuronal.

## Tabla de valores

| Tejido                                    |       DRD2 |      MDGA2 |      SIK1 |     ACTB |    GAPDH |
|:------------------------------------------|-----------:|-----------:|----------:|---------:|---------:|
| Whole Blood                               |  0         | 0          | 0.0754514 | 4803.94  | 1773.91  |
| Brain - Caudate (basal ganglia)           | 40.6964    | 0.564859   | 0.245288  | 1181.18  | 1073.59  |
| Brain - Putamen (basal ganglia)           | 45.7365    | 0.430045   | 0.165131  |  970.669 |  908.523 |
| Brain - Nucleus accumbens (basal ganglia) | 51.9149    | 0.653321   | 0.178288  | 1227.76  | 1141.44  |
| Brain - Hypothalamus                      |  6.49551   | 1.05859    | 0.309509  | 1026.04  | 1198.77  |
| Brain - Substantia nigra                  |  8.65936   | 0.521214   | 0.215275  | 1020.03  | 1084.1   |
| Brain - Frontal Cortex (BA9)              |  1.0411    | 1.1396     | 0.280223  | 1524.55  | 1651.41  |
| Brain - Spinal cord (cervical c-1)        |  0.650998  | 1.55071    | 0.28591   | 2143.56  | 1402.76  |
| Nerve - Tibial                            |  4.03365   | 0.0110735  | 2.97298   | 3385.87  | 1125.88  |
| Muscle - Skeletal                         |  0.310595  | 0          | 0.972744  |  395.993 | 5597.4   |
| Spleen                                    |  0.0312403 | 0.0110966  | 0.69809   | 3837.74  |  716.393 |
| Liver                                     |  0.0121022 | 0.00480872 | 0.745953  |  760.447 |  512.029 |

## Conclusión

GTEx no respalda la expresión basal de DRD2/MDGA2 en sangre periférica sana. Esto NO invalida GSE221921 (los HC de ese estudio tienen expresión baja pero detectable), pero sí sugiere que la señal en PBMCs depende de factores técnicos o poblacionales que no están presentes en GTEx. La comparación directa requiere cautela debido a diferencias en pipeline, población y condición pre-mortem vs post-mortem.

## Nota metodológica

GTEx v8 usa TPM normalizado desde alineación con STAR + cuantificación con RNA-SeQC. GSE221921 usa FPKM calculado con un pipeline diferente (no especificado en detalle). La comparación directa de valores absolutos entre estudios no es rigurosa; solo la dirección de la diferencia FM vs HC dentro de cada estudio es interpretable.
