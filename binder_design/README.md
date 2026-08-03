# Binder Design — Pipeline BindCraft para competencias

**Línea activa del lab** | Actualizado: 2026-07-04

Reemplaza el pipeline fallido RFdiffusion+AF2 vanilla (ipTM max 0.16) por **BindCraft** (Nature 2025, `10.1038/s41586-025-09429-6`).

## Quick start

```bash
# 0. Dependencias (solo para prep local de PDB)
pip install -r binder_design/requirements.txt

# 1. Preparar targets (descarga 2VSM de RCSB si no existe)
python binder_design/scripts/prepare_bindcraft_target.py --mode both

# 2. Ejecutar BindCraft en Colab (ver COLAB_INSTRUCTIONS.md)

# 3. Procesar resultados
python binder_design/scripts/process_bindcraft_run.py \
  --zip ~/Downloads/bindcraft_output.zip \
  --run-id bindcraft_nipah_YYYYMMDD

# 4. Filtrar candidatos
python binder_design/scripts/filter_bindcraft_designs.py \
  --input colab_runs/bindcraft_nipah_YYYYMMDD/raw/Accepted/designs.csv \
  --output colab_runs/bindcraft_nipah_YYYYMMDD/filtered_ranked.csv
```

## Estructura

```
binder_design/
├── README.md                    ← este archivo
├── COLAB_INSTRUCTIONS.md        ← pasos Colab paso a paso
├── COMPETITION_STATUS.md        ← estado de competencias Proteinbase
├── TARGET_SELECTION.md          ← por qué Nipah G
├── BASELINE_COMPARISON.md       ← viejo vs nuevo pipeline
├── COMPETE_CHECKLIST.md         ← checklist de envío
├── METHOD_DESCRIPTION_TEMPLATE.md
├── configs/nipah_bindcraft.json
├── scripts/
│   ├── prepare_bindcraft_target.py
│   ├── filter_bindcraft_designs.py
│   ├── process_bindcraft_run.py
│   └── monitor_competitions.py
└── targets/                     ← PDBs generados (gitignored si pesados)
```

## Métricas de éxito (grounded)

| Métrica | Umbral mínimo | Competitivo | Fuente |
|---------|---------------|-------------|--------|
| ipTM | > 0.50 | > 0.75 | Sappington 2026; colab_runs/INDEX.md |
| pLDDT interfaz | > 80 | > 90 | Estándar AF2 |
| Rosetta ΔΔG | < −30 REU | < −40 REU | PIPELINE_CLOUD_BINDER_DESIGN.md |

**Criterio de validación de migración:** obtener ipTM > 0.5 (el pipeline viejo nunca lo logró).

## Compute

- **Local RTX 4060 8GB:** no soportado para BindCraft
- **Colab Free T4:** smoke test con `nipah_target_minimal.pdb`
- **Colab Pro A100:** campañas de 500+ trayectorias

## Documentos relacionados (legacy)

- `PIPELINE_CLOUD_BINDER_DESIGN.md` — pipeline RFdiffusion (supersedido, conservado como referencia histórica)
- `colab_runs/INDEX.md` — baseline RFdiffusion (11 corridas Nipah, ipTM max 0.16)
