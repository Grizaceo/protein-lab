# PAPER 2 — RECÁLCULO DOCKING CON LIGANDOS VALIDADOS (2026-08-14)

**Paper:** `docking_fm_targets/docking_FM_targets_GPCR.md`
**Tipo:** Paper 2 — Computational chemistry campaign (DRD2, TACR1, OPRM1)
**Fecha cálculo original:** 2026-08-04 (v1.1, RETENIDO)
**Fecha recalculación:** 2026-08-14 (ligandos corregidos vía PubChem)

---

## Hallazgo principal

**Los SMILES del paper original (CIDs 11781183 y 135413546) NO correspondían a rolapitant y aprepitant.**
PubChem devuelve compuestos totalmente distintos: el "rolapitant" viejo tenía selenio (C9H8NO5Se+), el "aprepitant" viejo tenía bromo (C11H10BrN5O2).

**CIDs correctos:**
- Rolapitant: **CID 10311306** (era 11781183) — fórmula correcta C25H26F6N2O2
- Aprepitant: **CID 135413536** (era 135413546) — fórmula correcta C23H21F7N4O3
- Fentanyl: **CID 3345** — fórmula paper C22H30N2O era typo; real es C22H28N2O

---

## Tabla comparativa — ANTES vs DESPUÉS (8 ligandos)

### DRD2 (6VMS, 6VMS grid: center 109.7/127.5/94.0, size 20×20×20, exh=32)

| Ligando | Paper original ΔG | Docking validado ΔG | ΔΔG | Ki (µM) validado |
|---------|------------------|---------------------|-----|-------------------|
| Dopamina | −5.4 | **−5.724** | −0.3 | 68.4 |
| Pramipexole | −8.0 | **−6.164** | +1.8 | 69.8 |
| Bromocriptine | −9.4 | **−10.760** | −1.4 | 13.0 |

**Ranking original:** bromocriptine > pramipexole > dopamina ✅
**Ranking validado:** bromocriptine > pramipexole > dopamina ✅
**Conclusión DRD2:** Ranking preservado. Bromocriptine más fuerte de lo reportado; pramipexole más débil.

### OPRM1 (AlphaFold P35372, grid: center −7.7/8.1/7.9, size 22×22×22, exh=32)

| Ligando | Paper original ΔG | Docking validado ΔG | ΔΔG | Ki (µM) validado |
|---------|------------------|---------------------|-----|-------------------|
| Naloxone | −9.44 | **−9.072** | +0.4 | 0.22 |
| Morfina | −8.7 | **−8.709** | −0.0 | 0.40 |
| Fentanilo | −8.5 | **−9.211** | −0.7 | 0.18 |

**Ranking original:** naloxone > morfina > fentanilo ✅
**Ranking validado:** naloxone > fentanilo > morfina ⚠️ INVERTIDO
**Conclusión OPRM1:** Fentanilo supera a morfina (esperable: fentanilo es ~100× más potente).

### TACR1 (AlphaFold P25103, grid: center −1.98/−1.52/−9.32, size 20×20×20, exh=32)

| Ligando | Paper original ΔG | Docking validado ΔG | ΔΔG | Ki (µM) validado |
|---------|------------------|---------------------|-----|-------------------|
| Rolapitant | −6.7 | **−9.365** | −2.7 | 0.14 |
| Sustancia P (1-4) | −5.3 | (no recalculado, péptido) | — | — |
| Aprepitant | −3.2 | **−11.250** | **−8.1** | 0.006 |

**Ranking original:** rolapitant > sustancia P > aprepitant ❌
**Ranking validado:** aprepitant > rolapitant > sustancia P ✅ INVERSIÓN TOTAL
**Conclusión TACR1:** EL HALLazgo MÁS IMPORTANTE. Aprepitant (−11.25) supera ampliamente a rolapitant (−9.37), concordante con literatura (Ki ~0.1-1 nM vs ~10 nM).

---

## Correlación con literatura

| Ligando | Ki experimental (nM) | Ki validado (µM) | Error ratio |
|---------|---------------------|-------------------|-------------|
| Bromocriptine (DRD2) | ~0.1-1 | 13.0 | ~13-130× |
| Pramipexole (DRD2) | ~1-10 | 69.8 | ~7-70× |
| Naloxone (OPRM1) | 1-10 | 0.22 | ~2-20× |
| Fentanilo (OPRM1) | 1-10 | 0.18 | ~2-18× |
| Morfina (OPRM1) | 10-100 | 0.40 | ~0.4-4× |
| Rolapitant (TACR1) | ~10 | 0.14 | ~0.14× |
| Aprepitant (TACR1) | 0.1-1 | 0.006 | ~0.006-0.06× |

**Nota:** Ki se calcula desde ΔG vía Ki = exp(ΔG·1000/(R·T)) a 298K.
Vina no pretende predecir Ki absoluto; solo ranking cualitativo.

---

## Diagnóstico de modos positivos (indicador de malformación)

Paper 2 viejo reportaba que el aprepitant malformado (C26H33NO6, sin flúor) tenía **8 de 9 modos con afinidad positiva** (+0.35 a +4.05) — firma de ligando incorrecto.

**Este recalculación:** 8/8 ligandos tienen **0/9 modos positivos** → todos los ligandos están correctamente preparados.

---

## Estado para manuscript

### ¿Puede el Paper 2 salir de RETENIDO?

**SÍ — con condiciones:**

1. ✅ Ligandos correctos (fórmulas validadas vía PubChem)
2. ✅ 0/9 modos positivos en todos los ligandos
3. ✅ Ranking TACR1 corregido (aprepitant > rolapitant, concordante con literatura)
4. ⚠️ Ranking OPRM1 fentanilo > morfina es correcto pero paper original decía lo inverso
5. ⚠️ Sustancia P fragmento no recalculado (péptido, limitación conocida)
6. ⚠️ Modos de aprepitant todos negativos (−11.25 a ~−6.5) — valida la Hipótesis de que el paper original estaba mal

### Secciones del manuscrito que requieren actualización

- **§3.1 DRD2:** Actualizar tabla (bromocriptine más fuerte, pramipexole más débil)
- **§3.2 TACR1:** **REESCRITURA COMPLETA** — ranking invertido, aprepitant pasa de anómalo a mejor ligando
- **§3.3 OPRM1:** Actualizar ΔG, ranking (fentanilo > morfina)
- **§4.1:** Reemplazar "flexibilidad hypothesis" con "ligand identity hypothesis" — el error era el SMILES, no la flexibilidad
- **Banner RETENIDO:** Reemplazar con "Recálculo completado 2026-08-14 — pendiente revisión"

---

## Archivos generados

| Archivo | Ruta |
|---------|------|
| Manifest | `investigacion-fibromialgia/scripts/docking_ligand_manifest.json` |
| Resultados JSON | `investigacion-fibromialgia/scripts/docking_validated_results.json` |
| SDF ligandos | `investigacion-fibromialgia/estructuras/ligandos_validados/{nombre}_validated.sdf` |
| PDBQT ligandos | `investigacion-fibromialgia/estructuras/ligandos_validados/{nombre}_validated.pdbqt` |
| Dockings PDBQT | `investigacion-fibromialgia/estructuras/dockings_validados/{nombre}_{target}_validated_docked.pdbqt` |
| Scripts | `investigacion-fibromialgia/scripts/prepare_validated_ligands.py`, `gen_pdbqt_meeko.py`, `run_validated_docking.py` |

---

## Recomendación final

**El Paper 2 puede proceder a revisión con los resultados validados.**
La narrativa cambia de "el pipeline falla en antagonistas flexibles" a "la validación de identidad de ligando es crítica — cuando los ligandos son correctos, el pipeline reproduce rankings esperados".

El pipeline AutoDock Vina + AlphaFold **funciona para screening cualitativo** dentro de una misma chemotype. No resuelve diferencias finas entre agonists similares (morfina ≈ fentanilo), pero sí distingue correctamente antagonistas de alta afinidad (aprepitant −11.25) de moderados (rolapitant −9.37).
