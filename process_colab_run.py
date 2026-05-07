#!/usr/bin/env python3
"""
process_colab_run.py — FIX #9 (Rev 2026-04-24)
================================================
Automatiza el procesamiento de ZIPs exportados desde Google Colab (RFdiffusion,
ProteinMPNN, AF2) para el pipeline de diseño de binders (Nipah G / 2VSM).

FUNCIONES:
  1. Detecta ZIPs en colab_runs/ que aún no están procesados (sin INDEX.md)
  2. Extrae el ZIP a la carpeta correspondiente
  3. Busca archivos de puntajes (scores.json, result*.json, plddt*.txt, etc.)
  4. Extrae métricas: pLDDT, pAE, ipTM, ptm, RFdiffusion self-consistency
  5. Genera/actualiza INDEX.md con tabla markdown de resultados
  6. Actualiza colab_runs/INDEX.md con resumen global

Uso:
  python process_colab_run.py                    # procesa todos los ZIPs nuevos
  python process_colab_run.py <path/to/zip>      # procesa ZIP específico
  python process_colab_run.py --rebuild          # reconstruye todos los INDEX.md

Nota: Si no hay JSON de puntajes, extrae lo que encuentre y crea un INDEX
  de marcador de posición para que el investigador complete manualmente.
"""

import sys
import json
import zipfile
import argparse
import re
from pathlib import Path
from datetime import datetime

COLAB_RUNS = Path("colab_runs")
COLAB_RUNS.mkdir(exist_ok=True)


# ─── Detectores de métricas ──────────────────────────────────────────────────

def extract_from_scores_json(filepath):
    """Extrae métricas de archivos *scores*.json (AF2/AlphaFold format)."""
    try:
        with open(filepath) as f:
            data = json.load(f)
        if isinstance(data, list) and data:
            # AlphaFold2 batch format
            entries = []
            for item in data:
                entry = {
                    'name':   item.get('name', item.get('description', '?')),
                    'pLDDT':  round(item.get('plddt', item.get('mean_plddt', float('nan'))), 2),
                    'pAE':    round(item.get('ptm', item.get('mean_pae', float('nan'))), 4),
                    'ipTM':   round(item.get('iptm', float('nan')), 4),
                    'ptm':    round(item.get('ptm', float('nan')), 4),
                }
                entries.append(entry)
            return entries
        elif isinstance(data, dict):
            # Single-model format
            return [{
                'name':  filepath.stem,
                'pLDDT': round(data.get('plddt', data.get('mean_plddt', float('nan'))), 2),
                'pAE':   round(data.get('mean_pae', float('nan')), 4),
                'ipTM':  round(data.get('iptm', float('nan')), 4),
                'ptm':   round(data.get('ptm', float('nan')), 4),
            }]
    except Exception as e:
        return [{'name': filepath.stem, 'error': str(e)}]
    return []

def extract_from_rfdiff_trb(filepath):
    """Extrae datos de archivos .trb de RFdiffusion."""
    try:
        import pickle
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        return [{
            'name': filepath.stem,
            'type': 'RFdiffusion',
            'pLDDT': round(float(data.get('plddt', float('nan'))), 2)
            if 'plddt' in data else float('nan'),
            'note': 'RFdiffusion .trb (ver archivo para detalles)',
        }]
    except Exception:
        return [{'name': filepath.stem, 'type': 'RFdiffusion (.trb)', 'note': 'parseo manual requerido'}]

def scan_folder_for_metrics(folder):
    """Escanea una carpeta buscando archivos de métricas conocidos."""
    results = []
    folder = Path(folder)

    for f in sorted(folder.rglob("*scores*.json")):
        results.extend(extract_from_scores_json(f))
    for f in sorted(folder.rglob("result*.json")):
        results.extend(extract_from_scores_json(f))
    for f in sorted(folder.rglob("*.trb")):
        results.extend(extract_from_rfdiff_trb(f))
    for f in sorted(folder.rglob("plddt*.txt")):
        try:
            lines = f.read_text().strip().splitlines()
            for line in lines:
                parts = line.split()
                if parts:
                    results.append({'name': parts[0], 'pLDDT': float(parts[1]) if len(parts) > 1 else float('nan')})
        except Exception:
            pass

    return results


# ─── Generador de INDEX.md ────────────────────────────────────────────────────

def make_index_md(run_dir, results, zip_name=None):
    """Genera el contenido del INDEX.md para una carpeta de run."""
    run_dir = Path(run_dir)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# {run_dir.name}",
        f"",
        f"**Procesado:** {timestamp}  ",
        f"**Fuente:** {zip_name or 'extracción manual'}  ",
        f"**Pipeline:** RFdiffusion → ProteinMPNN → AF2 (Colab T4)  ",
        f"**Target:** Nipah G / 2VSM  ",
        f"",
    ]

    if results:
        # Determinar columnas disponibles
        all_keys = set()
        for r in results:
            all_keys.update(r.keys())
        cols = ['name']
        for col in ['type', 'pLDDT', 'pAE', 'ipTM', 'ptm', 'note', 'error']:
            if col in all_keys:
                cols.append(col)

        # Tabla markdown
        header = "| " + " | ".join(f"**{c}**" for c in cols) + " |"
        sep    = "| " + " | ".join("---" for _ in cols) + " |"
        lines += ["## Resultados", "", header, sep]

        for r in results:
            row = []
            for c in cols:
                val = r.get(c, "—")
                if isinstance(val, float):
                    val = f"{val:.3f}" if not (val != val) else "N/A"  # nan check
                row.append(str(val))
            lines.append("| " + " | ".join(row) + " |")

        lines.append("")

        # Resumen estadístico
        plddt_vals = [r['pLDDT'] for r in results
                      if isinstance(r.get('pLDDT'), float) and r['pLDDT'] == r['pLDDT']]
        if plddt_vals:
            lines += [
                "## Resumen",
                "",
                f"- **n diseños:** {len(results)}",
                f"- **pLDDT medio:** {sum(plddt_vals)/len(plddt_vals):.2f}",
                f"- **pLDDT máx:**  {max(plddt_vals):.2f}",
                f"- **pLDDT mín:**  {min(plddt_vals):.2f}",
                "",
                "### Criterio de selección (Sappington 2026)",
                "- pLDDT > 70 → candidato para Rosetta DDG",
                "- ipTM > 0.7 → alta confianza de interfaz",
                "- **DDG Rosetta < −30 kcal/mol** → candidato final (Paso 4.5 del pipeline)",
                "",
            ]
    else:
        lines += [
            "## Resultados",
            "",
            "> ⚠ No se encontraron archivos de métricas en este run.",
            "> Completar manualmente o verificar que el ZIP contenga",
            "> `*scores*.json`, `result*.json`, o `plddt*.txt`.",
            "",
            "| Campo | Valor |",
            "| --- | --- |",
            "| Modelos generados | ? |",
            "| pLDDT medio | ? |",
            "| ipTM medio | ? |",
            "",
        ]

    lines += [
        "## Archivos",
        "",
        "```",
    ]
    # Listar archivos en la carpeta (excluyendo esta misma INDEX.md)
    all_files = sorted(run_dir.rglob("*"))
    for fp in all_files[:40]:  # máx 40 para no saturar
        if fp.is_file() and fp.name != "INDEX.md":
            rel = fp.relative_to(run_dir)
            size = fp.stat().st_size
            size_str = f"{size/1024:.1f} KB" if size > 1024 else f"{size} B"
            lines.append(f"  {rel}  ({size_str})")
    if len(all_files) > 40:
        lines.append(f"  ... ({len(all_files) - 40} archivos más)")
    lines += ["```", ""]

    return "\n".join(lines)


# ─── Procesamiento de ZIP ─────────────────────────────────────────────────────

def process_zip(zip_path, force=False):
    zip_path = Path(zip_path)
    if not zip_path.exists():
        print(f"  ERROR: {zip_path} no existe")
        return False

    # Determinar directorio destino
    stem = zip_path.stem
    # Limpiar suffix :Zone.Identifier si existe
    clean_stem = re.sub(r':.*', '', stem)
    dest = zip_path.parent / clean_stem if (zip_path.parent / clean_stem).is_dir() \
           else zip_path.parent / f"{datetime.now().strftime('%Y-%m-%d')}_{clean_stem}"

    index_file = dest / "INDEX.md"
    if index_file.exists() and not force:
        print(f"  SKIP {zip_path.name} → {dest.name}/INDEX.md ya existe (usar --rebuild para regenerar)")
        return False

    print(f"  Procesando: {zip_path.name}")
    dest.mkdir(parents=True, exist_ok=True)

    # Extraer ZIP
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(dest)
        print(f"    Extraído → {dest}/")
    except zipfile.BadZipFile as e:
        print(f"    ⚠ No es un ZIP válido ({e}) — creando INDEX de marcador")

    # Escanear métricas
    results = scan_folder_for_metrics(dest)
    print(f"    Métricas encontradas: {len(results)} entradas")

    # Escribir INDEX.md
    index_content = make_index_md(dest, results, zip_name=zip_path.name)
    index_file.write_text(index_content)
    print(f"    ✓ INDEX.md generado ({index_file})")
    return True


def update_global_index():
    """Actualiza colab_runs/INDEX.md con resumen de todas las subcarpetas."""
    runs = sorted([d for d in COLAB_RUNS.iterdir() if d.is_dir()])
    lines = [
        "# colab_runs — Índice Global",
        "",
        f"**Actualizado:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Pipeline:** RFdiffusion → ProteinMPNN → AF2 → (DDG Rosetta pendiente)  ",
        "",
        "| Run | Modelos | pLDDT máx | Estado |",
        "| --- | --- | --- | --- |",
    ]
    for run_dir in runs:
        idx = run_dir / "INDEX.md"
        if not idx.exists():
            lines.append(f"| {run_dir.name} | ? | ? | ⚠ Sin INDEX.md |")
            continue
        content = idx.read_text()
        # Extraer pLDDT máx del INDEX.md
        m_max = re.search(r'pLDDT máx.*?(\d+\.\d+)', content)
        m_n   = re.search(r'n diseños.*?(\d+)', content)
        plddt_max = m_max.group(1) if m_max else "?"
        n_designs  = m_n.group(1) if m_n else "?"
        lines.append(f"| {run_dir.name} | {n_designs} | {plddt_max} | ✓ Procesado |")

    lines += [
        "",
        "## Pendiente",
        "- [ ] Rosetta DDG filtering (DDG < -30 kcal/mol) — ver PIPELINE_CLOUD_BINDER_DESIGN.md § Paso 4.5",
        "",
    ]
    (COLAB_RUNS / "INDEX.md").write_text("\n".join(lines))
    print(f"  ✓ colab_runs/INDEX.md actualizado ({len(runs)} runs)")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Procesa ZIPs de Colab y genera INDEX.md")
    parser.add_argument('zip', nargs='?', help='ZIP a procesar (opcional; por defecto todos los nuevos)')
    parser.add_argument('--rebuild', action='store_true', help='Reconstruir todos los INDEX.md')
    args = parser.parse_args()

    print("=" * 60)
    print("process_colab_run.py — Rev 2026-04-24")
    print("=" * 60)

    if args.zip:
        process_zip(args.zip, force=True)
    else:
        # Detectar todos los ZIPs en colab_runs/
        zips = list(COLAB_RUNS.glob("**/*.zip"))
        # Filtrar :Zone.Identifier files
        zips = [z for z in zips if ':' not in z.name]
        print(f"\nZIPs encontrados: {len(zips)}")
        processed = 0
        for z in zips:
            if process_zip(z, force=args.rebuild):
                processed += 1
        print(f"\nProcesados: {processed} | Omitidos: {len(zips) - processed}")

    update_global_index()
    print("\nDone.")

# ─── API importable ───────────────────────────────────────────────────────────

def ingest_new_zips(verbose: bool = True) -> list:
    """
    Detecta y procesa todos los ZIPs nuevos en colab_runs/.
    Retorna lista de carpetas run generadas/actualizadas (Path objects).
    Pensado para ser llamado desde lab_iterate.py.
    """
    zips = list(COLAB_RUNS.glob("**/*.zip"))
    zips = [z for z in zips if ':' not in z.name]
    processed = []
    for z in zips:
        if process_zip(z, force=False):
            processed.append(z.parent)
            if verbose:
                print(f"  [ingest] Procesado: {z.name}")
    update_global_index()
    return processed


if __name__ == "__main__":
    main()
