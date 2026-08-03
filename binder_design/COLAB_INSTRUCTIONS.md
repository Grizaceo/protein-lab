# BindCraft en Colab — Nipah G validation run

**Target:** Nipah Virus G (2VSM chain A)  
**Notebook oficial:** https://colab.research.google.com/github/martinpacesa/BindCraft/blob/main/notebooks/BindCraft.ipynb

## Pre-requisitos (local)

```bash
python binder_design/scripts/prepare_bindcraft_target.py --mode both
```

Sube a Colab:
- `binder_design/targets/nipah_target_minimal.pdb` (T4 free)
- `binder_design/targets/nipah_target_full.pdb` (A100 / si cabe en VRAM)
- `binder_design/targets/hotspots.txt`

## Pasos en Colab

### 1. Runtime

`Runtime → Change runtime type → GPU (T4 o A100)`

### 2. Instalar BindCraft

Seguir celdas del notebook oficial. Aceptar licencia académica PyRosetta cuando se solicite.

### 3. Configurar target

```python
# Upload minimal target for T4
target_pdb = "/content/nipah_target_minimal.pdb"

# Hotspots (chain A)
hotspot_residues = "A489,A504,A505,A506"

# Binder length range (aa)
binder_length = "65-150"

# Trajectories — start with 50 for smoke test, scale to 500 for production
num_trajectories = 50
```

### 4. Smoke test (50 trayectorias)

- Esperar a que aparezca carpeta `Accepted/` con diseños filtrados internamente por BindCraft.
- Verificar que al menos 1 diseño tenga ipTM reportado en logs/CSV.
- Si OOM en T4: usar `nipah_target_minimal.pdb` (no full).

### 5. Production run (500 trayectorias)

Recomendado en Colab Pro A100. Config en `binder_design/configs/nipah_bindcraft.json`.

### 6. Filtro Rosetta ΔΔG (opcional pero recomendado)

Notebook PyRosetta: https://colab.research.google.com/github/RosettaCommons/PyRosetta.notebooks/blob/master/notebooks/06.08-Docking-and-Design.ipynb

Criterio: cartesian_ddg < −30 REU por diseño candidato.

### 7. Descargar y procesar localmente

```bash
# Mover ZIP a colab_runs/
python binder_design/scripts/process_bindcraft_run.py \
  --zip bindcraft_nipah_smoke.zip \
  --run-id bindcraft_nipah_smoke_001

python binder_design/scripts/filter_bindcraft_designs.py \
  --input colab_runs/bindcraft_nipah_smoke_001/raw/Accepted/designs.csv \
  --output colab_runs/bindcraft_nipah_smoke_001/filtered_ranked.csv
```

## Criterio de éxito

| Fase | Métrica | Umbral |
|------|---------|--------|
| Smoke test | Pipeline completa sin OOM | OK |
| Smoke test | ≥1 diseño con ipTM > 0.5 | Migración validada |
| Production | ≥10 diseños ipTM > 0.5 | Listo para competir |
| Production | ≥3 diseños ipTM > 0.75 | Competitivo |

## Troubleshooting

| Problema | Solución |
|----------|----------|
| CUDA OOM | Usar minimal PDB; reducir binder_length a 65-100 |
| 0 Accepted | Normal en pocas trayectorias; escalar a 200-500 |
| ipTM sigue < 0.5 tras 500 traj | Revisar hotspots; probar BindCraft + RFdiffusion en paralelo |
