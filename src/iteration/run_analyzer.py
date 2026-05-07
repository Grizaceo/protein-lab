"""
run_analyzer.py — Análisis de resultados de corridas Colab.

Responsabilidades:
- Detectar ZIPs nuevos (no registrados) en colab_runs/
- Parsear mpnn_results.csv, scores.json y .trb de cada run
- Calcular métricas agregadas (mean pLDDT, mean ipTM, mean pAE, best_pLDDT)
- Inferir target (nipah vs ferritin) del nombre de carpeta / contenido
- Retornar run_record listo para state_manager.register_run()
"""

import csv
import json
import math
import re
import zipfile
from pathlib import Path
from datetime import datetime

COLAB_RUNS = Path(__file__).parent.parent.parent / "colab_runs"

# Palabras clave en el nombre de carpeta para inferir target
TARGET_HINTS = {
    "nipah": ["nipah", "2vsm", "2VSM", "glyco", "binder"],
    "ferritin": ["ferritin", "1bfr", "1BFR", "biosensor", "chassis"],
}


def _safe_float(val):
    """Convierte val a float o retorna None."""
    try:
        f = float(val)
        return None if math.isnan(f) else f
    except (TypeError, ValueError):
        return None


def infer_target(run_id: str) -> str:
    """Infiere el target de una corrida por su run_id (nombre de carpeta)."""
    run_lower = run_id.lower()
    for target, hints in TARGET_HINTS.items():
        for hint in hints:
            if hint.lower() in run_lower:
                return target
    # Por defecto nipah (es el loop activo principal)
    return "nipah"


def parse_mpnn_csv(csv_path: Path) -> dict:
    """
    Parsea un mpnn_results.csv y retorna métricas agregadas.

    Columnas esperadas (binder-only): design,n,mpnn,plddt,ptm,pae,rmsd,seq
    Columnas esperadas (complejo AF2): design,n,mpnn,plddt,i_ptm,i_pae,rmsd,seq
    """
    rows = []
    try:
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception:
        return {}

    if not rows:
        return {}

    # Detectar si tiene columnas de complejo (i_ptm / i_pae)
    sample_keys = set(rows[0].keys())
    has_complex = "i_ptm" in sample_keys or "i_pae" in sample_keys

    plddt_vals, iptm_vals, pae_vals = [], [], []

    for row in rows:
        plddt = _safe_float(row.get("plddt"))
        if plddt is not None:
            plddt_vals.append(plddt)

        if has_complex:
            iptm = _safe_float(row.get("i_ptm"))
            pae  = _safe_float(row.get("i_pae"))
        else:
            iptm = None
            pae  = _safe_float(row.get("pae"))

        if iptm is not None:
            iptm_vals.append(iptm)
        if pae is not None:
            pae_vals.append(pae)

    def avg(lst):
        return round(sum(lst) / len(lst), 4) if lst else None

    return {
        "mean_pLDDT":  avg(plddt_vals),
        "best_pLDDT":  round(max(plddt_vals), 4) if plddt_vals else None,
        "mean_ipTM":   avg(iptm_vals),
        "mean_pAE":    avg(pae_vals),
        "n_designs":   len(rows),
        "complex_scored": has_complex,
    }


def parse_scores_json(json_path: Path) -> dict:
    """Parsea *scores*.json al estilo AF2/AlphaFold."""
    try:
        with open(json_path) as f:
            data = json.load(f)
    except Exception:
        return {}

    entries = data if isinstance(data, list) else [data]
    plddt_vals, iptm_vals, pae_vals = [], [], []

    for item in entries:
        v = _safe_float(item.get("plddt") or item.get("mean_plddt"))
        if v is not None:
            plddt_vals.append(v)
        v = _safe_float(item.get("iptm"))
        if v is not None:
            iptm_vals.append(v)
        v = _safe_float(item.get("mean_pae"))
        if v is not None:
            pae_vals.append(v)

    def avg(lst):
        return round(sum(lst) / len(lst), 4) if lst else None

    return {
        "mean_pLDDT":  avg(plddt_vals),
        "best_pLDDT":  round(max(plddt_vals), 4) if plddt_vals else None,
        "mean_ipTM":   avg(iptm_vals),
        "mean_pAE":    avg(pae_vals),
        "n_designs":   len(entries),
        "complex_scored": len(iptm_vals) > 0,
    }


def analyze_run_folder(run_dir: Path) -> dict:
    """
    Analiza la carpeta de un run ya extraído y retorna métricas agregadas.
    Prioriza mpnn_results.csv; si no, busca scores.json.
    """
    run_dir = Path(run_dir)
    metrics = {}

    # Prioridad 1: mpnn_results.csv
    csv_files = sorted(run_dir.rglob("mpnn_results.csv"))
    if csv_files:
        # Usar el más reciente (más profundo o más en la ruta raw/outputs/)
        best_csv = max(csv_files, key=lambda p: len(p.parts))
        metrics = parse_mpnn_csv(best_csv)

    # Prioridad 2: *scores*.json si no tenemos métricas
    if not metrics:
        for json_file in run_dir.rglob("*scores*.json"):
            metrics = parse_scores_json(json_file)
            if metrics:
                break
        if not metrics:
            for json_file in run_dir.rglob("result*.json"):
                metrics = parse_scores_json(json_file)
                if metrics:
                    break

    return metrics


def extract_zip_to_run_dir(zip_path: Path) -> Path:
    """
    Extrae un ZIP a colab_runs/<YYYY-MM-DD_stem>/.
    Si la carpeta ya existe, simplemente retorna su path.
    Retorna la carpeta destino.
    """
    zip_path = Path(zip_path)
    stem = re.sub(r":.*", "", zip_path.stem)  # quitar :Zone.Identifier etc.
    today = datetime.now().strftime("%Y-%m-%d")

    # ¿Existe ya una carpeta con ese stem exacto?
    existing = [d for d in COLAB_RUNS.iterdir()
                if d.is_dir() and stem in d.name]
    if existing:
        dest = existing[0]
    else:
        dest = COLAB_RUNS / f"{today}_{stem}"

    dest.mkdir(parents=True, exist_ok=True)

    if zipfile.is_zipfile(zip_path):
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(dest)

    return dest


def get_known_run_ids(state: dict) -> set:
    """Retorna el conjunto de run_ids ya registrados en el estado."""
    ids = set()
    for target in state.get("targets", {}).values():
        for run in target.get("runs", []):
            ids.add(run["run_id"])
    return ids


def find_new_runs(state: dict) -> list[dict]:
    """
    Detecta carpetas en colab_runs/ que NO están en el estado.
    Extrae ZIPs pendientes si los hay.
    Retorna lista de dicts: {run_id, run_dir, metrics, target, complex_scored}.
    """
    known = get_known_run_ids(state)
    new_runs = []

    # Primero extraer ZIPs no procesados
    zips = [z for z in COLAB_RUNS.glob("**/*.zip") if ":" not in z.name]
    for zp in zips:
        dest = extract_zip_to_run_dir(zp)
        # El ZIP en sí no es un run_id; la carpeta destino sí
        if dest.name not in known:
            pass  # se detectará abajo como carpeta nueva

    # Escanear carpetas
    for d in sorted(COLAB_RUNS.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        if d.name not in known:
            metrics = analyze_run_folder(d)
            target = infer_target(d.name)
            new_runs.append({
                "run_id": d.name,
                "run_dir": str(d),
                "metrics": metrics,
                "target": target,
                "complex_scored": metrics.get("complex_scored", False),
            })

    return new_runs


def build_run_record(run_id: str, metrics: dict, params: dict = None,
                     notes: str = "", target: str = "nipah") -> dict:
    """Construye un run_record completo para pasar a state_manager.register_run()."""
    return {
        "run_id":        run_id,
        "target":        target,
        "params":        params or {},
        "metrics":       metrics,
        "complex_scored": metrics.get("complex_scored", False),
        "promoted":      False,
        "notes":         notes,
    }
