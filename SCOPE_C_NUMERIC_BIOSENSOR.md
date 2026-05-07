# Scope C — Verificación Numérica de la Ruta que Sí Funciona

Fecha: 2026-04-22

Rol: Adam Heller — bioelectroquímica molecular

## Objetivo
Validar numéricamente la línea que sí sobrevive a la auditoría: ferritina/bacterioferritina como chasis, Au in situ/excéntrico como mediador redox, y lectura electroquímica como salida.

Este Scope C no evalúa el “computador biológico”. Ese camino queda archivado por ahora.

## Hipótesis de trabajo
La arquitectura es plausible si se cumple todo lo siguiente:
1. El Au NP puede anclarse químicamente dentro del lumen sin desestabilizar el chasis.
2. La red de hopping entre Au, Cys, His, Met y hemo mantiene distancias compatibles con ET proteico.
3. La salida experimental no es lógica booleana sino corriente medible.
4. El pH puede modular la señal lo suficiente como para ser útil como biosensor.

## Geometría base usada
Tomamos la versión V4b como referencia:
- Au NP excéntrico de radio ~10 Å.
- Distancia Au surface → CYS49 SG: ~3.13 Å.
- Distancia CYS49 SG → HIS46 NE2: ~4.78 Å.
- Distancia HIS46 NE2 → MET52 SD: ~9.25 Å.
- Distancia MET52 SD → Heme B FE: ~5.65 Å.

## Cálculo rápido de tasas
Usando el modelo de decaimiento exponencial:

k_hop ≈ k0 · exp(-βd)

con:
- k0 = 10^13 s^-1
- β = 1.4 Å^-1

La etapa limitante es HIS46 → MET52:
- d = 9.25 Å
- exp(-βd) ≈ 2.38 × 10^-6
- k ≈ 2.38 × 10^7 s^-1
- tiempo característico ≈ 42 ns

## Corrección importante de la auditoría
Durante la verificación se detectó un error aritmético en la versión anterior del análisis:
- donde decía “40 μs por electrón”, el valor correcto es del orden de “42 ns por electrón”.
- donde decía “4 fA por evento”, el orden correcto es del orden de “3.8 pA por evento de saturación”, bajo el supuesto de descarga secuencial de ~1000 electrones en ~42 μs.

Esto no destruye la hipótesis biosensorial; al contrario, la hace más rápida de lo que la versión previa sugería.

## Interpretación física
La diferencia entre 42 ns y 40 μs importa mucho. En la práctica:
- 42 ns por hop sí está dentro de un régimen compatible con una señal electroquímica observable.
- 40 μs habría sido mucho más lento y más problemático para amplificación.

En otras palabras, la ruta funcional queda mejor parada de lo que creíamos cuando el objetivo es un biosensor, no un procesador.

## Qué sí queda respaldado
- Ferritina/bacterioferritina como chasis robusto: sí.
- Formación de oro in situ dentro del lumen: sí.
- Uso de cisteínas para anclaje Au–S: sí, con restricciones geométricas.
- Salida electroquímica medible: sí, al menos en principio.
- Modulación por pH: plausible como hipótesis de trabajo.

## Qué sigue siendo débil
- La señal exacta de pH aún depende de validación estructural y electroquímica real.
- El anclaje de 3 Cys sigue siendo sensible a geometría fina y dinámica molecular.
- La estimación de corriente sigue siendo de primer orden, no un dato experimental.
- El sistema requiere inmovilización en electrodo; en solución libre es demasiado débil para lucirse.

## Veredicto Scope C
La línea que funciona no es “computación biológica”.
La línea que sí se sostiene es:

ferritina + oro in situ + ET secuencial + lectura electroquímica + posible gating por pH.

Eso no es humo. Es un biosensor / amplificador bioelectroquímico todavía especulativo, pero bastante más realista que el computador.

## Decisión de proyecto
Continuar solo con la ruta de biosensor y descartar, por ahora, cualquier narrativa de procesador.

## Próximo paso recomendado
1. Congelar el diseño como V4b biosensor.
2. Revisar si conviene bajar la ambición del gating pH.
3. Hacer una validación estructural más dura: qué mutaciones son realmente tolerables.
4. Pasar después a un chequeo experimental mínimo: señal esperada, densidad de inmovilización y orden de magnitud de corriente.
