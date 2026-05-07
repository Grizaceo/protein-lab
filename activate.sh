#!/bin/bash
# Activar environment protein-lab
source ~/.miniconda/etc/profile.d/conda.sh
conda activate protein-lab

# Verificar VRAM disponible
echo "=== GPU Status ==="
nvidia-smi --query-gpu=memory.free,memory.total --format=csv,noheader
echo ""

# Verificar que ESM2 está disponible
python3 -c "import esm; print('ESM2 OK:', esm.__version__)"
