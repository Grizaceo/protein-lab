#!/usr/bin/env python3
"""
Filter BindCraft accepted designs by grounded competition metrics.

Expected input: BindCraft output folder or CSV with columns such as:
  design_name, sequence, pLDDT, ipTM, pae_inter, ddg (optional)

Usage:
  python binder_design/scripts/filter_bindcraft_designs.py \\
    --input colab_runs/bindcraft_nipah_20260704/raw/Accepted/designs.csv \\
    --output colab_runs/bindcraft_nipah_20260704/filtered_ranked.csv

Thresholds (Sappington 2026 + competition gates):
  ipTM >= 0.5 (competitive >= 0.75)
  pLDDT interface >= 80 (uses global pLDDT if per-residue not available)
  Rosetta cartesian_ddg <= -30 REU (if column present)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

DEFAULT_THRESHOLDS = {
    "iptm_min": 0.5,
    "iptm_competitive": 0.75,
    "plddt_min": 80.0,
    "ddg_max_reu": -30.0,
}


def load_rows(path: Path) -> list[dict]:
    if path.suffix == ".json":
        data = json.loads(path.read_text())
        if isinstance(data, list):
            return data
        return data.get("designs", data.get("results", []))
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({k.strip(): v for k, v in row.items()})
    return rows


def fval(row: dict, *keys: str, default=float("nan")) -> float:
    for k in keys:
        if k in row and row[k] not in (None, "", "nan", "NA"):
            try:
                return float(row[k])
            except ValueError:
                continue
    return default


def passes(row: dict, t: dict) -> tuple[bool, list[str]]:
    reasons = []
    iptm = fval(row, "ipTM", "iptm", "interface_ptm")
    plddt = fval(row, "pLDDT", "plddt", "avg_plddt", "plddt_binder")
    ddg = fval(row, "ddg", "DDG", "cartesian_ddg", "rosetta_ddg")

    if iptm != iptm:
        reasons.append("missing ipTM")
    elif iptm < t["iptm_min"]:
        reasons.append(f"ipTM {iptm:.3f} < {t['iptm_min']}")

    if plddt != plddt:
        reasons.append("missing pLDDT")
    elif plddt < t["plddt_min"]:
        reasons.append(f"pLDDT {plddt:.1f} < {t['plddt_min']}")

    if ddg == ddg and ddg > t["ddg_max_reu"]:
        reasons.append(f"DDG {ddg:.1f} > {t['ddg_max_reu']} REU")

    return len(reasons) == 0, reasons


def rank_key(row: dict) -> tuple:
    iptm = fval(row, "ipTM", "iptm", default=0.0)
    plddt = fval(row, "pLDDT", "plddt", default=0.0)
    ddg = fval(row, "ddg", "DDG", default=0.0)
    return (-iptm, -plddt, ddg if ddg == ddg else 0.0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path, help="CSV or JSON from BindCraft run")
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--iptm-min", type=float, default=DEFAULT_THRESHOLDS["iptm_min"])
    ap.add_argument("--plddt-min", type=float, default=DEFAULT_THRESHOLDS["plddt_min"])
    ap.add_argument("--ddg-max", type=float, default=DEFAULT_THRESHOLDS["ddg_max_reu"])
    args = ap.parse_args()

    thresholds = {
        "iptm_min": args.iptm_min,
        "iptm_competitive": 0.75,
        "plddt_min": args.plddt_min,
        "ddg_max_reu": args.ddg_max,
    }

    if not args.input.exists():
        sys.exit(f"ERROR: input not found: {args.input}")

    rows = load_rows(args.input)
    if not rows:
        sys.exit(f"ERROR: no designs in {args.input}")

    passed, failed = [], []
    for row in rows:
        ok, reasons = passes(row, thresholds)
        row = dict(row)
        row["filter_pass"] = ok
        row["filter_notes"] = "; ".join(reasons) if reasons else "OK"
        (passed if ok else failed).append(row)

    passed.sort(key=rank_key)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({k for r in passed + failed for k in r.keys()})
    with args.output.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in passed:
            w.writerow(r)

    print(f"Total designs: {len(rows)}")
    print(f"Passed filters: {len(passed)}")
    print(f"Failed filters: {len(failed)}")
    if passed:
        best = passed[0]
        print(
            f"Best: {best.get('design_name', best.get('name', '?'))} "
            f"ipTM={fval(best, 'ipTM', 'iptm'):.3f} "
            f"pLDDT={fval(best, 'pLDDT', 'plddt'):.1f}"
        )
    print(f"Ranked output: {args.output}")


if __name__ == "__main__":
    main()
