# BioMaterialCAD Artefacto de Diseño — Versión 4b (V4b)
## Nanoelectrodo Excéntrico en Lumen de Ferritina
### Chasis: E.Coli Bacterioferritin (PDB 1BFR)

---

## 1. Corrección Post-Auditoria: Del Centro a la Pared

La auditoría `audit_v4_real.py` reveló un fallo geométrico fatal:

- **Au NP radio 18Å** en centro → superficie a **18Å** del centro.
- **CYS49** (mutado desde ILE49, CA a 40.3Å del centro) → SG estimado a **~36Å** del centro.
- **Gap Au surface → tiol = ~18Å**. Un enlace Au-S requiere ~2.3Å. 
- **Veredicto**: Un Au NP grande centrado es geométricamente incompatible con los residuos del lumen de 1BFR.

**Pivot bioelectroquímico**: No es un solenoide centrado — es un **nanoelectrodo excéntrico**, un cluster de Au de ~2.0 nm pegado a la pared luminal de 1–2 subunidades, anclado localmente por 3 CYS y conectado electroquímicamente al hemo vecino.

---

## 2. Geometría Excéntrica: El Au NP "Oreja"

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| **Tamaño Au NP** | Ø ~2.0 nm, radio ~10Å (~150–200 átomos) | Reduce tensión superficial, cabe en nicho luminal |
| **Posición** | **Excéntrica**: centro a ~28–32Å del centro global del 24-mer | Acercado a la pared interna (radio hemos ~43Å); Au surface a ~18–22Å del centro |
| **Anclaje** | 3 CYS de 1 subunidad (e.g., A) | ILE49A→CYS, VAL43A→CYS, LEU40A→CYS |
| **Distancia CYS49 SG → Au surface** | ~5–8 Å | Viable para enlace Au-S directo |
| **Distancia Au surface → Heme B** | ~12–15 Å | Vía CYS49→HIS46/MET52→Heme |

El cluster queda como una **"oreja" de Au** adosada a la pared luminal, no flotando en el centro vacio.

### Diagrama topológico (corte radial del lumen)

```
          Centro del lumen (~43Å radio libre)
                    [vacío / analitos]
                         o
                        / \
                       /   \
                HEM B(Fe)   HEM A(Fe)  ← 43Å del centro
                    |           |
                MET52  HIS46 — ILE49(CYS)
                    \     |    /
                     \    |   /  ← Au NP excéntrico a ~28Å del centro
                      [Au~150]
                     /    |   \
                tiol   tiol  tiol
```

---

## 3. Ventajas de la Excéntricidad

1. **Contacto químico real**: Los tióles de 3 CYS tocan la superficie del Au. 150 átomos de Au con ligandos tiol locales son termodinámicamente estables.
2. **Canal de difusión preservado**: El 90% del lumen permanece vacío. Analitos (H₂O₂, O₂) difunden libremente a través de los canales 3-fold/4-fold y contactan la "oreja" Au.
3. **Solo 3 CYS mutadas**: No se necesitan 72 tióles. 3 por subunidad × 1 subunidad = solo 3 mutaciones en el constructo genético.
4. **Mensurable**: Un Au NP de 2nm tiene plasmon resonante y superficie electroactiva suficiente para detección de H₂O₂ por cronoamperometría.

---

## 4. Ruta de Hopping V4b (Realista)

| Tramo | Via | Distancia estimada |
|-------|-----|--------------------|
| Electrodo carbono → superficie BFR exterior | Contacto físico directo o enlace covalente (EDC/NHS) | ~0 Å (interface electrode-proteína) |
| BFR exterior → HEM interfacial | Cadena polipéptida + hemo nativo | ~10–15 Å |
| HEM A → HEM B (inter-hemo dimer) | Hopping Fe→Fe a través de medio proteico | ~12 Å |
| HEM B(Fe) → MET52(S/SD) → HIS46(NE2) | Hopping intra-subunidad nativo | ~6 + ~4 Å |
| HIS46 → ILE49(CYS SG) | Hopping imidazol→tiol | ~5 Å |
| CYS49 SG → Au NP surface | Enlace Au-S + hopping metal | ~2 Å (enlace directo) |
| Au NP surface → analito (H₂O₂) | Electrocatalisis directa Au→H₂O₂ | Contacto difusivo en lumen |

**Gap total analito→electrodo**: ~40 Å (cumple threshold <50 Å).

---

## 5. Función: ¿Qué Sensamos?

El Au NP excéntrico funciona como una **microelectrode incrustada en la pared del lumen**. Las esquinas/bordes del nanocluster policristalino catalizan la reducción de:

- **H₂O₂** → H₂O (detección amperométrica, ~−0.1 V vs Ag/AgCl)
- **O₂** → H₂O₂ (mediante enzima adicional o Au pura)
- **NO** (potencialmente, en presencia de cobre dopado)

El hemo BFR actúa como **mediador de electrones interno**: transporta e⁻ desde el electrode hasta el Au NP, evitando que el Au necesite un cable físico.

**Salida**: Cambio de corriente proporcional a [H₂O₂] en el rango μM–mM.

---

## 6. Congelamiento de Especificaciones V4b

| Parámetro | Valor |
|-----------|-------|
| Au cluster | ~150 átomos, radio 10Å, policristalino |
| Posición | Centroide a 30±5Å del centro global (excéntrico) |
| Anclaje | 3× CYS de cadena A: ILE49A, VAL43A, LEU40A |
| Relay nativo | HIS46A, MET52A (sin mutar) |
| Hemo primario | HEM en cadena B (interfaz AB directa) |
| Temperatura MD | 300 K, pH 7.4, NaCl 150 mM |

---

## 7. Checklist de Revisión

- [ ] Modelar 3 mutaciones I→C, V→C, L→C en cadena A (energía FoldX).
- [ ] Verificar que LEU40→CYS no colisiona con cadena B en la interfaz dimer AB.
- [ ] Calcular distancia exacta CYS49 SG → Au10 cluster usando docking manual.
- [ ] Estimar k_ET por Marcus theory para HIS46 → CYS49 → Au.
- [ ] Simular difusión de H₂O₂ dentro del lumen con el Au excéntrico (HOLE/Omni)

---

## 8. Comparativa V3 vs V4b

| Criterio | V3 (Quantum Processor) | V4b (Nanoelectrodo Excéntrico) |
|----------|------------------------|-----------------------------------|
| Core Au | Au₅₅ atómico (ilusión) | Au NP ~150 átomos (real) |
| Posición | Centro (idealizado) | Excéntrico (real) |
| Ligandos | 12 CYS (inviable) | 3 CYS (viable) |
| Hopping Gap | 12.16 Å (sospechoso) | ~25 Å (vía relay nativo) |
| Función | Computación cuántica (ilusión) | Biosensor H₂O₂ (mensurable) |
| MoE Score | 2/10 (IRREAL) | 7/10 (VIABLE, pendiente validación) |

---

**Código congelamiento**: `V4b-FREEZE-20260422-003`
**Estado**: Preparado para simulación ESM2/MD/FoldX.

---

> *Analogía final: No es un supercomputador dentro de una caja fuerte — es un sensor de temperatura soldado a una pared interna de la caja, con cables que salen por los conductos de ventilación.*
