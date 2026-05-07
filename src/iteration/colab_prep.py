"""
colab_prep.py — Preparación de la carpeta next_run/ para la próxima corrida Colab.

Para cada target genera:
  next_run/{target}/
    target.pdb            ← copia del PDB objetivo
    colab_config.json     ← parámetros listos para copy-paste en Colab
    COLAB_INSTRUCTIONS.md ← instrucciones paso a paso (tabla de params + archivos)
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent.parent
NEXT_RUN  = WORKSPACE / "next_run"

COLAB_URL = (
    "https://colab.research.google.com/github/sokrypton/ColabDesign/"
    "blob/main/rf/examples/diffusion.ipynb"
)

# Tiempo estimado por configuración (minutos en T4 Colab)
TIME_ESTIMATES = {
    (8,  50): 45,
    (8,  25): 30,
    (8, 100): 70,
    (16, 50): 80,
    (4,  50): 25,
}


def _estimate_time(num_designs: int, T: int) -> int:
    return TIME_ESTIMATES.get((num_designs, T), 45)


def _copy_pdb(src_path_str: str, dest_dir: Path) -> bool:
    """Copia el PDB destino a next_run/{target}/target.pdb. Retorna True si OK."""
    if not src_path_str:
        return False
    src = WORKSPACE / src_path_str
    if not src.exists():
        # Buscar por nombre en data/pdb/
        candidates = list((WORKSPACE / "data" / "pdb").rglob(src.name))
        if candidates:
            src = candidates[0]
        else:
            return False
    shutil.copy2(src, dest_dir / "target.pdb")
    return True


def _make_colab_instructions(target_name: str, target_display: str,
                              params: dict, strategy: str, rationale: str,
                              target_info: dict, pdb_copied: bool) -> str:
    """Genera COLAB_INSTRUCTIONS.md completo."""
    iteration = target_info.get("iteration", 0) + 1  # próxima iteración
    best_score = target_info.get("best_score", 0.0) or 0.0
    best_run   = target_info.get("best_run") or "ninguno"
    stuck      = target_info.get("stuck_count", 0)
    T          = params.get("T", 50)
    nd         = params.get("num_designs", 8)
    eta        = _estimate_time(nd, T)

    pdb_upload = "target.pdb → /content/input/target.pdb" if pdb_copied else \
                 "⚠ PDB no encontrado localmente — descarga manualmente de RCSB"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# Instrucciones Colab — {target_display}",
        f"**Iteración:** {iteration}  ",
        f"**Generado:** {timestamp}  ",
        f"**Estrategia:** {strategy.upper()}  ",
        "",
        "---",
        "",
        "## Estado actual",
        "",
        f"- Mejor score hasta ahora: **{best_score:.4f}** (`{best_run}`)",
        f"- Iteraciones sin mejora (stuck_count): {stuck}",
        "",
        "---",
        "",
        "## Archivos a subir en Colab",
        "",
        f"| Archivo local | Ruta en Colab |",
        f"| --- | --- |",
        f"| `next_run/{target_name}/target.pdb` | `/content/input/target.pdb` |",
        "",
        f"> {pdb_upload}",
        "",
        "---",
        "",
        "## Parámetros a configurar",
        "",
        rationale,
        "",
        "---",
        "",
        "## Pasos",
        "",
        f"1. Abre el notebook: [{COLAB_URL}]({COLAB_URL})",
        "2. En el menú lateral (carpeta 📁), crea la carpeta `/content/input/`",
        "3. Sube `target.pdb` a `/content/input/target.pdb`",
        "4. En la celda de configuración, ajusta los siguientes valores:",
        "",
        "   ```python",
        f"   target_pdb  = '/content/input/target.pdb'",
        f"   contigs     = '{params.get('contigs', '')}'",
        f"   hotspot     = '{params.get('hotspot', '')}'",
        f"   num_designs = {params.get('num_designs', 8)}",
        f"   T           = {params.get('T', 50)}",
        f"   guide_scale = {params.get('guide_scale', 10)}",
        "   ```",
        "",
        "5. `Runtime → Run all` (o Ctrl+F9)",
        f"6. Espera ≈{eta} min (T4 Google Colab)",
        "7. Al terminar, descarga el ZIP resultante",
        "   - Generalmente se llama `test.result.zip` o similar",
        "8. Mueve el ZIP a la carpeta `colab_runs/` del workspace local",
        "9. Ejecuta el loop:",
        "",
        "   ```bash",
        "   python lab_iterate.py",
        "   ```",
        "",
        "---",
        "",
        "## Criterios de éxito (Sappington 2026)",
        "",
        "| Métrica | Umbral mínimo | Umbral óptimo |",
        "| --- | --- | --- |",
        "| pLDDT binder | > 0.85 | > 0.90 |",
        "| ipTM (complejo AF2) | > 0.50 | > 0.75 |",
        "| i_pAE | < 15 Å | < 10 Å |",
        "| Rosetta ΔΔG | < −30 REU | < −50 REU |",
        "",
        "> **Nota:** Si el notebook no ejecuta scoring de complejo (AF2 multimer),",
        "> el ipTM no estará disponible. En ese caso usar solo pLDDT > 0.90 como",
        "> filtro de primera ronda.",
        "",
        "---",
        "",
        "## colab_config.json (referencia)",
        "",
        "```json",
        json.dumps(params, indent=2, ensure_ascii=False),
        "```",
    ]
    return "\n".join(lines)


def prepare_next_run(target_name: str, target_info: dict,
                     params: dict, strategy: str, rationale_text: str) -> Path:
    """
    Genera la carpeta next_run/{target_name}/ con los 3 archivos necesarios.
    Sobreescribe si ya existe.

    Returns: Path a la carpeta generada.
    """
    out_dir = NEXT_RUN / target_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. colab_config.json
    config = {
        "target":         target_name,
        "iteration":      target_info.get("iteration", 0) + 1,
        "strategy":       strategy,
        "generated":      datetime.now().strftime("%Y-%m-%d %H:%M"),
        "params":         params,
        "colab_notebook": COLAB_URL,
    }
    (out_dir / "colab_config.json").write_text(
        json.dumps(config, indent=2, ensure_ascii=False)
    )

    # 2. Copiar PDB
    pdb_copied = _copy_pdb(target_info.get("pdb_source", ""), out_dir)

    # 3. COLAB_INSTRUCTIONS.md
    instructions = _make_colab_instructions(
        target_name=target_name,
        target_display=target_info.get("display_name", target_name),
        params=params,
        strategy=strategy,
        rationale=rationale_text,
        target_info=target_info,
        pdb_copied=pdb_copied,
    )
    (out_dir / "COLAB_INSTRUCTIONS.md").write_text(instructions)

    return out_dir
