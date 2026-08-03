#!/usr/bin/env python3
"""
Ingest BindCraft Colab output into colab_runs/ with honest metrics indexing.

Usage:
  python binder_design/scripts/process_bindcraft_run.py \\
    --zip ~/Downloads/bindcraft_nipah_run.zip \\
    --run-id bindcraft_nipah_20260704

Creates:
  colab_runs/{run_id}/raw/          — extracted files
  colab_runs/{run_id}/INDEX.md      — per-run metrics table
  Updates colab_runs/INDEX.md       — global summary (BindCraft section)
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COLAB_RUNS = ROOT / "colab_runs"
GLOBAL_INDEX = COLAB_RUNS / "INDEX.md"


def extract_metrics_from_dir(raw_dir: Path) -> list[dict]:
    """Find CSV/JSON metric files in BindCraft output."""
    designs: list[dict] = []

    for csv_path in raw_dir.rglob("*.csv"):
        if "Accepted" not in str(csv_path) and "final" not in csv_path.name.lower():
            continue
        try:
            with csv_path.open(newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    designs.append(normalize_row(row, source=csv_path.name))
        except Exception:
            continue

    for json_path in raw_dir.rglob("*.json"):
        try:
            data = json.loads(json_path.read_text())
            items = data if isinstance(data, list) else data.get("designs", [])
            for row in items:
                designs.append(normalize_row(row, source=json_path.name))
        except Exception:
            continue

    return designs


def normalize_row(row: dict, source: str = "") -> dict:
    def g(*keys):
        for k in keys:
            if k in row and row[k] not in ("", None):
                return row[k]
        return ""

    return {
        "name": g("design_name", "name", "Description"),
        "sequence": g("sequence", "Sequence"),
        "pLDDT": g("pLDDT", "plddt", "avg_plddt"),
        "ipTM": g("ipTM", "iptm", "interface_ptm"),
        "pAE": g("pAE", "pae_inter", "mean_pae"),
        "ddg": g("ddg", "DDG", "cartesian_ddg"),
        "source": source,
    }


def best_iptm(designs: list[dict]) -> float:
    vals = []
    for d in designs:
        try:
            v = float(d.get("ipTM") or 0)
            if v > 0:
                vals.append(v)
        except (TypeError, ValueError):
            pass
    return max(vals) if vals else 0.0


def write_run_index(run_dir: Path, run_id: str, designs: list[dict]) -> None:
    idx = run_dir / "INDEX.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# BindCraft run: {run_id}",
        f"",
        f"**Processed:** {now}",
        f"**Pipeline:** BindCraft (Nature 2025)",
        f"**Designs parsed:** {len(designs)}",
        f"**Best ipTM:** {best_iptm(designs):.4f}",
        f"",
        f"| Name | pLDDT | ipTM | pAE | DDG |",
        f"|------|-------|------|-----|-----|",
    ]
    sorted_d = sorted(
        designs,
        key=lambda d: float(d.get("ipTM") or 0),
        reverse=True,
    )
    for d in sorted_d[:50]:
        lines.append(
            f"| {d.get('name', '?')} | {d.get('pLDDT', '-')} | "
            f"{d.get('ipTM', '-')} | {d.get('pAE', '-')} | {d.get('ddg', '-')} |"
        )
    idx.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_global_index(run_id: str, designs: list[dict]) -> None:
    section_header = "## BindCraft runs"
    entry = (
        f"| {run_id} | BindCraft | {len(designs)} | "
        f"{best_iptm(designs):.4f} | pending |"
    )

    if not GLOBAL_INDEX.exists():
        GLOBAL_INDEX.write_text(
            "# colab_runs — Índice Global\n\n"
            "## BindCraft runs\n\n"
            "| Run | Pipeline | Designs | Best ipTM | Status |\n"
            "|-----|----------|---------|-----------|--------|\n"
            f"{entry}\n",
            encoding="utf-8",
        )
        return

    text = GLOBAL_INDEX.read_text(encoding="utf-8")
    if run_id in text:
        return
    if section_header not in text:
        text += (
            f"\n\n{section_header}\n\n"
            "| Run | Pipeline | Designs | Best ipTM | Status |\n"
            "|-----|----------|---------|-----------|--------|\n"
        )
    text += entry + "\n"
    GLOBAL_INDEX.write_text(text, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", type=Path, help="ZIP downloaded from Colab")
    ap.add_argument("--dir", type=Path, help="Already extracted directory")
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()

    run_dir = COLAB_RUNS / args.run_id
    raw_dir = run_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    if args.zip:
        with zipfile.ZipFile(args.zip, "r") as zf:
            zf.extractall(raw_dir)
        print(f"Extracted {args.zip} -> {raw_dir}")
    elif args.dir:
        import shutil
        for item in args.dir.iterdir():
            dest = raw_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
    else:
        ap.error("Provide --zip or --dir")

    designs = extract_metrics_from_dir(raw_dir)
    write_run_index(run_dir, args.run_id, designs)
    append_global_index(args.run_id, designs)
    print(f"Parsed {len(designs)} designs. Best ipTM: {best_iptm(designs):.4f}")


if __name__ == "__main__":
    main()
