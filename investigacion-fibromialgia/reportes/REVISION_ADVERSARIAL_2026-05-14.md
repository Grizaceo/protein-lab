# REVISIÓN ADVERSARIAL — EVIDENCIA_ORTOGONAL_2026-05-14.md

**Revisor:** DAVI en modo adversarial (auto-revisión)
**Fecha:** 2026-05-14 15:45
**Metodología:** verifiqué cada claim del reporte contra fuentes externas, busqué evidencia contradictoria, y detecté omisiones.

---

## A. ERRORES FÁCTICOS ENCONTRADOS

### A1. Resolución de 8EF6: MAL

El reporte dice: "8EF6 | Cryo-EM | 2.8 Å (estimado)"

**Realidad:** La página de RCSB para 8EF6 dice explícitamente **Resolution: 3.20 Å**. No es estimado, es el dato experimental. Mi "2.8 Å (estimado)" fue una invención — probablemente confundí con otra estructura o redondeé mal de memoria.

**Gravedad:** Media. No cambia la conclusión (3.2 Å sigue siendo válido para docking), pero viola mi propia regla de "cero invención." Inaceptable.

### A2. Datos faltantes de 8F7R: INCOMPLETO

El reporte lista 8F7R con guiones en resolución, organismo, PMID, DOI.

**Realidad:** 8F7R tiene datos completos:
- Organismo MOR: **Homo sapiens**
- Ligando: Endomorphin (peptide)
- PMID: del paper "Structures of the entire human opioid receptor family" (Cell 186:413-427.e17, 2023)
- Es parte de una serie de estructuras de TODA la familia de receptores opioides humanos

**Gravedad:** Baja. Los guiones eran marcadores de "no verifiqué esto en esta sesión", pero debí haber sido explícito sobre eso en vez de dejar celdas vacías.

### A3. Corrección de PMID de 8EF6: PARCIALMENTE MAL

El reporte cita PMID 36368322 para 8EF6.

**Realidad:** La página de RCSB muestra PMID **36368306** (no 36368322). DOI 10.1016/j.cell.2022.09.041. Verifiqué: 36368306 es correcto.

**Gravedad:** Media. El DOI sí es correcto (10.1016/j.cell.2022.09.041), así que la referencia es trazable. Pero un PMID inventado en un reporte que promete verificabilidad es un fallo de higiene.

---

## B. PROBLEMAS METODOLÓGICOS

### B1. Comparación directa pKd vs Ki sin justificación

El reporte compara MAMMAL pKd contra Ki experimental como si fueran intercambiables. Para un antagonista competitivo como naltrexona, bajo condiciones específicas Ki ≈ Kd (ecuación de Cheng-Prusoff). Pero esto NO está explicado en el reporte. El lector podría objetar legítimamente: "estás comparando peras con manzanas."

**Qué falta:** Una nota explicando que para antagonistas competitivos en ensayos de binding de radioligando, Ki se aproxima a Kd. Sin esa nota, la comparación es técnicamente imprecisa.

### B2. El factor "×700" es engañoso sin contexto

145 nM / 0.2 nM = 725×. La matemática es correcta. Pero presentar esto como "×700" sugiere una precisión que los datos no tienen:
- El Ki de naltrexona varía entre 0.2 y 3.6 nM según el ensayo
- El pKd de MAMMAL tiene una SD de ~0.1 en las corridas
- Si usamos Ki=3.6 nM (PubChem AID 450029), el factor sería 145/3.6 = 40×, no 700×

El reporte cherry-pickeó el valor más extremo (Ki=0.2) para maximizar el contraste. Esto es un sesgo de confirmación clásico.

### B3. DiffDock puede ser MALA elección para GPCRs

Este es el hallazgo más grave. Encontré un paper reciente (Research Square, 2025-2026): **"Physics beats diffusion: Agentic AI-driven virtual screening benchmark on a GPCR target"** que compara DiffDock vs Uni-Dock (physics-based) en un target GPCR. Resultado: **Uni-Dock supera a DiffDock en GPCRs.**

También hay un paper en ACS JCIM (2025): "Can Deep Learning Blind Docking Methods be Used to Predict GPCR-ligand Binding?" que sugiere que métodos combinados (DiffDock + re-docking local) funcionan mejor que DiffDock solo.

Mi recomendación de "DiffDock vía Colab porque es más fácil" ignoró la posibilidad de que DiffDock tenga limitaciones específicas para GPCRs. No verifiqué si DiffDock funciona bien en GPCRs antes de recomendarlo.

---

## C. OMISIONES GRAVES

### C1. Polimorfismo OPRM1 A118G (rs1799971) y fibromialgia

Encontré un paper directo: **PMID 24671502** — "Assessment of opioid receptor μ1 gene A118G polymorphism and fibromyalgia susceptibility" (2014). Este estudio investigó si el polimorfismo A118G de OPRM1 está asociado con susceptibilidad a fibromialgia e intensidad de dolor.

**El reporte no menciona esta línea de evidencia en absoluto.** Si el polimorfismo de OPRM1 está asociado con FM, eso sería evidencia genética convergente fuerte para la hipótesis MOR. Si NO está asociado, debilita la hipótesis. En cualquier caso, es una omisión inexcusable para un reporte que pretende ser comprehensivo.

### C2. PET imaging de ocupancia MOR

El reporte menciona datos de PET brevemente en la tabla de binding, pero no desarrolla esta línea. Existen múltiples estudios PET con [11C]carfentanil que miden ocupancia de MOR por naltrexona en cerebro humano. Esto es evidencia ortogonal directa y no la exploré.

### C3. GWAS de fibromialgia

No busqué si hay estudios GWAS de fibromialgia que hayan identificado loci cerca de OPRM1, MS4A2, o cualquiera de los 16 targets. Si existen, serían evidencia genética invaluable. Si no existen, documentar esa ausencia también es informativo.

---

## D. SESGOS DEL AUTOR (DAVI)

### D1. Favorecimiento de la narrativa MOR

El reporte dedica mucho más espacio y entusiasmo a MOR que a MS4A2, a pesar de que:
- MS4A2 tiene señal transcriptómica DIRECTA (FDR=0.019)
- MOR no tiene NINGUNA señal transcriptómica en los datasets disponibles
- La evidencia de binding para MOR es irrelevantemente fuerte (ya sabemos que naltrexona se une a MOR — eso nunca estuvo en duda)

El reporte construye una narrativa de "MOR es el target real, MAMMAL solo lo mide mal" vs "MS4A2 es solo biomarcador." Esto puede ser correcto, pero el sesgo es evidente en el tono y espacio dedicado.

### D2. La analogía final es propaganda, no ciencia

"El joyero confirma que naltrexona es oro de 24 quilates para MOR" — esta analogía es literariamente efectiva pero científicamente engañosa. No necesitábamos un "joyero" para saber que naltrexona se une a MOR. Eso se sabe desde los años 70. La pregunta relevante es si LDN funciona en FM, y el reporte no aporta nada nuevo sobre eso.

La analogía sirve para cerrar con fuerza retórica, pero oculta que el reporte no resolvió la pregunta central.

---

## E. LO QUE EL REPORTE HIZO BIEN

Para ser justo:
1. Las citas de PDB ID, DOI, y PMID (con la excepción del error en 8EF6) son trazables
2. La sección 7 (descartados) es honesta y útil
3. Respeta la prohibición del checkpoint de no afirmar "migración a tejidos"
4. La tabla comparativa (sección 5) es el producto más valioso del reporte
5. MS4A2 como subunidad estructural de FcεRI está correctamente caracterizado
6. La distinción entre "target farmacológico" y "biomarcador" es clínicamente relevante

---

## F. VEREDICTO GLOBAL

El reporte es **útil pero con fallas corregibles.** No es fraudulento ni malintencionado, pero:

- Cometió 2 errores fácticos (resolución 8EF6, PMID 8EF6)
- Hizo cherry-picking del Ki más extremo para maximizar el contraste
- Recomendó DiffDock sin verificar su rendimiento en GPCRs
- Omitió evidencia genética clave (OPRM1 A118G en FM)
- Tiene sesgo de narrativa pro-MOR

**No recomendaría usarlo para tomar decisiones sin corregir estos puntos.**

---

## G. CORRECCIONES NECESARIAS (antes de actuar)

1. Corregir resolución 8EF6: 3.20 Å (no 2.8)
2. Corregir PMID 8EF6: 36368306 (no 36368322)
3. Agregar datos de 8F7R: human MOR, endomorphin, Cell 2023, PMID correspondiente
4. Incluir nota sobre Ki≈Kd para antagonistas competitivos
5. Reportar el rango completo del factor: 40-725× (según qué Ki se use), no solo 700×
6. Reconsiderar DiffDock vs Vina-GPU a la luz del benchmark GPCR
7. Buscar y resumir PMID 24671502 (OPRM1 A118G en FM)
8. Agregar sección de "evidencia faltante" con PET, GWAS, y datos genéticos
9. Balancear el tono entre MOR y MS4A2
10. La analogía final debe incluir la advertencia de que saber que naltrexona se une a MOR no prueba que LDN funcione en FM

---

## H. RECOMENDACIÓN FINAL

**No hacer docking todavía.** Primero:
1. Corregir el reporte con los puntos G.1-G.9
2. Buscar OPRM1 A118G en FM (PMID 24671502)
3. Evaluar DiffDock vs AutoDock Vina-GPU para GPCRs con datos reales de benchmarks
4. Solo después de corregir, decidir si docking es el siguiente paso o si hay una ruta mejor (genética, PET, GWAS)

---

*Revisión adversarial completada. Procedo a commit para trazabilidad.*
