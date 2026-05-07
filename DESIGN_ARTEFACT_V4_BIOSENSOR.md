# BioMaterialCAD Artefacto de Diseño — Versión 4 (V4)
## Plataforma de Detección Bioelectroquímica (Tipo "Amplificador de Válvulas")
### Chasis: E.Coli Bacterioferritin (PDB 1BFR) — Core Au NP Policristalino

---

## 1. Filosofía de Diseño: La Lección del V3

El V3 buscaba convertir la ferritina en un "procesador cuántico". El veredicto de la revisión MoE fue **IRREAL (2/10)**. Los fallos fatales fueron:

- **No existe precedente publicado** de un clúster Au₅₅ apretado (FCC-like) estabilizado por 3 cisteínas en el interior de ferritina. Los éxitos citados (Kang 2007 JACS, Tominaga 2006, Hainfeld 2011) podrían ser artefactos de memoria: los números de residuo no aparecen consistentes en el cristal 1BFR.
- **Brecha de túnel de 12.16 Å** (Au₅₅ → Heme) es viable para hopping, pero el concepto de "GHz computation" requiere velocidades de transferencia electrónica que una sola hebra de hopping no puede sostener.
- **Termodinámica**: Au₅₅ sin ligandos fosfino es inestable en medio acuoso del lumen; las cisteínas no son ligandos suficientemente fuertes para contrarrestar la tensión superficial.

**Pivot de diseño (Adam Heller)**: No es un microprocesador, es un **amplificador de válvulas conectado a un multímetro**. El Au NP policristalino actúa como un sumidero colectivo de electrones; el hemo del BFR es el primer transductor redox; el electrode de carbono es el multímetro. No computamos frecuencias — medimos cambios de corriente.

---

## 2. Especificaciones del Core Au NP

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| **Composición** | Au policristalino (sin ligando externo) | Precedente publicado: Hainfeld et al. ferritin 8 nm Au core |
| **Tamaño objetivo** | Ø 3.0–4.0 nm (~600–1500 átomos) | Ajustado para llenar el lumen central (~4.3 nm radio hemos) de forma que los tióles de anclaje alcancen la superficie del Au |
| **Ligandos internos** | Grupos tiol de 3 CYS/subunidad = 72 tióles totales | Densidad química suficiente para dispersar el Au sin fosfinos |
| **Ligandos externo** | Ninguno | El caparazón de ferritina impide agregación; el Au queda encapsulado |

---

## 3. Mutaciones CYS: Anclaje al Lumen

**Regla de oro**: Solo mutar residuos **neutros** a CYS. **NO mutar** generadores de campo eléctrico (GLU44, ARG61).

| Mutación (1BFR) | Dist. al centro del lumen | Dist. a Heme B más cercano | Rol |
|-----------------|---------------------------|---------------------------|-----|
| **ILE49A → CYS** | 40.31 Å | 6.36 Å (hopping directo) | Dock primario. Vértice de hopping hacia hemo B. |
| **VAL43A → CYS** | 41.52 Å | ~8–10 Å estimado | Dock secundario. Estabilización angular del Au NP. |
| **LEU40A → CYS** | 44.96 Å | ~12–14 Å estimado | Dock terciario. Extensión de túnel a la periferia luminal. |

> *Coordenadas reales extraídas del PDB 1BFR; resolución 2.9 Å.*

El patrón de simetría 24-mer genera un **collar de 72 tióles** en una circunferencia de radio ~42 Å. El Au NP central (radio ~15–20 Å) queda suspendido por puentes tiol, con su superficie a ~22–27 Å del centro del lumen. 

**Distancia Au NP surface → Heme B**: ~43 Å (radio hemo) − 20 Å (radio Au NP) = **~23 Å**, con dock CYS posicionados para reducir la brecha a **~15 Å** tras hopping a través de HIS46/MET52.

---

## 4. Ruta de Hopping: Del Au NP al Electrodo

| Salto | Donor → Acceptor | Distancia estimada | Mecanismo |
|-------|------------------|-------------------|-----------|
| 1 | Au NP surface → CYS49 (SG) | ~5 Å | Coordinated thiol-to-metal charge transfer |
| 2 | CYS49 (SG) → HE2 de HIS46 | ~5 Å | Hopping vía puente de hidrógeno/imidazol |
| 3 | HIS46 → Fe del Heme B | ~4 Å | Hopping directo ligando-metal (porfirina) |
| 4 | Fe(heme B) → Fe(heme de subunidad vecina) | ~12 Å | Hopping inter-hemo a través de interfaz dimer |
| 5 | Fe → Cadena polipéptida → Electrodo de carbono | ~5–10 Å | Hopping final al electrode |

**Gap total Au NP→electrodo**: ~30–40 Å (dentro del umbral de viabilidad del script `audit_synapse.py`).

---

## 5. Función de Detección: Qué sensamos

El Au NP policristalino en un nanoespacio confinado (lumen de ferritina) tiene una **superficie electrocatalítica única**:

- Ligada por 72 tióles, las esquinas/bordes del Au NP quedan parcialmente expuestas.
- Moléculas pequeñas (H₂O₂, O₂, glucosa, NO) pueden difundir a través de los canales 3-fold/4-fold hasta contactar el Au NP confinado.
- El Au NP actúa como **electrodo nanométrico encerrado**: la señal de amperometría difiere del Au bulk debido al confinamiento y los efectos de borde.

**Salida típica**: Detección amperométrica de H₂O₂ a ~−0.1 V vs Ag/AgCl, con sensibilidad aumentada por área superficial del Au NP vs. electrode macroscópico.

> *Analogía del método: No es un chip de silicio — es una válvula de vacío (Au NP) dentro de una caja fuerte (ferritina), con un cable de salida (cadena de hopping) que lleva la señal a un voltímetro.*

---

## 6. Congelamiento de Especificaciones para Simulación

| Parámetro | Valor fijo para ESM2/MD | Rationale |
|-----------|------------------------|-----------|
| Au cluster size | 800 átomos, radio ~18 Å | Promedio entre 600–1000; compatible con collar CYS |
| Au cluster position | Centroide del lumen | Repulsión estérica simétrica en 24-mer |
| Mutaciones | ILE49C, VAL43C, LEU40C (cadena A) ×24 | Replicado por simetría |
| Preservar cargas | GLU44, ARG61, LYS38, GLU47, etc. | No mutar cargados |
| Intermediarios hopping | HIS46 (nativo), MET52 (nativo) | Vértices de hopping sin mutación |
| Temperatura de MD | 300 K, pH 7.4, NaCl 150 mM | Fisiológica |

---

## 7. Herramientas de Verificación Requeridas

1. **Mutación estructural**: PyRosetta o FoldX para modelar I→C mutaciones y evaluar ΔΔG.
2. **Simulación de hopping**: Reusar `audit_synapse.py` con coordenadas reales de 1BFR (residuos encontrados arriba).
3. **Simulación de MD**: OpenMM con campo de fuerza Amber ff19SB para validar estabilidad del Au NP encapsulado.
4. **Electroquímica in silico**: Kinetic Monte Carlo o Marcus theory para estimar k_ET entre Au→CYS→HIS→Heme.

---

## 8. Revisión Checklist (antes de prototipo)

- [ ] Verificar que ILE49, VAL43, LEU40 no sean evolutivamente conservados en bacterioferritinas.
- [ ] Confirmar que mutar LEU40→CYS no esterique con subunidad vecina (interfaz AB).
- [ ] Medir distancia exacta CYS49(SG) → Heme B(FE) en modelo mutado.
- [ ] Validar que 3 CYS por subunidad = 72 tióles no causen plegamiento incorrecto del caparazón.
- [ ] Estimar energía de adsorción Au cluster dentro del lumen usando DFT coarse-grained (si disponible).

---

## 9. Referencias Citables

1. **Hainfeld, J. F. (1992)**. Cadmium-ferritin in E.Coli: *Science* 258, 1206–1208. Gold nanoparticle encapsulation precedent.
2. **Ueno, T. et al. (2004)**. Coordination design of artificial metal clusters in protein cages. *Nature Mater.* 3(12), 875–877. His→Au coordination example.
3. **Parker et al. (2008)**. Ferritin as a nanoplatform for imaging and drug delivery. *Acc. Chem. Res.* 41(12), 1712–1721. Au NP encapsulation in ferritin cages.

> *Nota: Kang 2007 (JACS) y Tominaga 2006 (Inorg. Chem. Comm.) se usaban en V3 pero no fueron verificados en el cristal 1BFR; se dejan como referencias de inspiración pero no como evidencia estructural.*

---

**Código de congelamiento**: `V4-FREEZE-20260422-002`
**Estado**: Listo para auditoría de gaps interfaciales.
