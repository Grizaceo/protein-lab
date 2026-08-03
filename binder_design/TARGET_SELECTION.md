# Selección de target de validación

**Decisión:** Nipah G (PDB 2VSM, chain A)  
**Fecha:** 2026-07-04

## Por qué Nipah G

| Criterio | Nipah G | RBX1 (cerrado) | EGFR |
|----------|---------|----------------|------|
| Target prep en lab | Script existente (`scripts/prepare_target_2vsm.py`) | Requiere descarga nueva | Requiere descarga |
| Benchmark wet-lab público | Sí (9.3% hit, KD 370 pM) | Sí (2.8% hit) | Sí (más fácil) |
| Dificultad | Media-alta (virus G, ~400 aa domain) | Muy alta (disordered) | Media |
| Corridas previas en lab | 11 iteraciones RFdiffusion | Ninguna | Ninguna |
| Comparación directa | ipTM viejo 0.16 vs BindCraft nuevo | Solo post-hoc | Sin baseline local |

Nipah permite comparar honestamente el pipeline viejo (RFdiffusion+AF2, ipTM max 0.16) contra BindCraft en el **mismo target**.

## Recursos de compute

| Opción | VRAM | Costo | Viabilidad BindCraft |
|--------|------|-------|---------------------|
| Colab Free T4 | 16 GB | $0 | Sí, si target recortado (<550 res target+binder) |
| Colab Pro A100 | 40–80 GB | ~$10/mes | Recomendado para producción |
| RTX 4060 local | 8 GB | — | **No** — ESMFold crashea; BindCraft requiere ≥32 GB ideal |

**Recomendación:** Colab Free T4 para smoke test; Colab Pro A100 para campañas de cientos de trayectorias.

## Hotspots (focal patch, iteración 4)

Residuos para condicionar BindCraft: `489, 504, 505, 506` (chain A).

Dominio receptor-binding recortado: residuos 212–600 (389 aa) en `target_clean.pdb`.  
Para T4, usar recorte adicional hotspot-centric (~120 aa) via `prepare_bindcraft_target.py --mode minimal`.
