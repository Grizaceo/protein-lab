# Estrategia 1 — Replicación intrasujeto: GSE274134

**Fecha:** 2026-05-27
**Dataset:** GSE274134 (Bonastre-Férez et al. 2024, PMID 39273470)
**Diseño:** 6 pacientes FM, PBMCs, RNA-seq NovaSeq 6000, pre/post terapia manual (4 semanas)

## Resultados

### DRD2
- **Expresión detectable: 0/6 pacientes** (todos los valores = 0)
- No es posible evaluar cambio con MT porque el gen no se expresa en PBMCs en este dataset
- **No replica** el hallazgo de GSE221921 (FM_mean=0.72 FPKM)

### MDGA2
- **Expresión detectable: 0/6 pacientes** (todos los valores = 0 o near-zero)
- No es posible evaluar cambio con MT
- **No replica** el hallazgo de GSE221921 (FM_mean=2.58 FPKM)

### SIK1 (control positivo)
- **Expresión detectable: 6/6 pacientes**
- Downregulated post-MT en 4/6 pacientes (FM1, FM2, FM5, FM6)
- **Replica** el hallazgo del paper original

## Interpretación

La no detección de DRD2/MDGA2 en GSE274134 NO invalida automáticamente GSE221921. Posibles explicaciones:
1. **Profundidad de secuenciación diferente**: GSE221921 usó HiSeq 2500 con libraries específicas; GSE274134 usó NovaSeq 6000 con protocolo distinto. Genes de baja expresión pueden caer bajo el límite de detección en una plataforma pero no en otra.
2. **Cohorte diferente**: GSE221921 = cohorte india (Mohapatra 2024); GSE274134 = cohorte española (Oltra 2024). Diferencias genéticas poblacionales o criterios de inclusión.
3. **Procesamiento diferente**: GSE221921 proporciona FPKM normalizado; GSE274134 proporciona DEA pre-computada con conteos crudos. El pipeline de alineación/cuantificación puede afectar genes de baja expresión.
4. **Tamaño muestral**: n=6 con expresión cero no permite distinguir 'ausencia real' de 'bajo el límite de detección'.

El control positivo SIK1 funciona correctamente, lo que descarta problemas técnicos globales con los datos.

## Conclusión

GSE274134 **no puede usarse como replicación independiente** de DRD2/MDGA2 porque estos genes no alcanzan el umbral de detección en esta plataforma/cohorte. Esto no fortalece ni debilita el hallazgo original; simplemente es un dataset no informativo para estos genes específicos.
