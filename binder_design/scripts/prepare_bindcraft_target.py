#!/usr/bin/env python3
"""
Prepare Nipah G (2VSM) target PDBs for BindCraft on Colab T4.

Modes:
  full    — chain A, residues 212-600 (~389 aa), same as prepare_target_2vsm.py
  minimal — hotspot-centric window ±25 aa around focal patch (~120 aa)

Outputs:
  binder_design/targets/nipah_target_full.pdb
  binder_design/targets/nipah_target_minimal.pdb
  binder_design/targets/hotspots.txt
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

try:
    from Bio.PDB import PDBIO, PDBParser, Select
except ImportError:
    sys.exit("ERROR: biopython required. Install: pip install biopython")

ROOT = Path(__file__).resolve().parents[2]
TARGETS_DIR = ROOT / "binder_design" / "targets"
PDB_ID = "2VSM"
RCSB_URL = f"https://files.rcsb.org/download/{PDB_ID}.pdb"

FOCAL_HOTSPOTS = [489, 504, 505, 506]
DOMAIN_RANGE = (212, 600)
MINIMAL_PADDING = 25


class ResidueRangeSelect(Select):
    def __init__(self, chain_id: str, res_range: tuple[int, int]):
        self.chain_id = chain_id
        self.lo, self.hi = res_range

    def accept_chain(self, chain):
        return chain.id == self.chain_id

    def accept_residue(self, residue):
        if residue.get_id()[0].strip():
            return False
        num = residue.get_id()[1]
        return self.lo <= num <= self.hi

    def accept_atom(self, atom):
        return True


def download_pdb(dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return dest
    print(f"Downloading {PDB_ID} from RCSB...")
    urllib.request.urlretrieve(RCSB_URL, dest)
    return dest


def save_trimmed(source: Path, dest: Path, chain: str, res_range: tuple[int, int]) -> int:
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(PDB_ID, str(source))
    io = PDBIO()
    io.set_structure(structure)
    dest.parent.mkdir(parents=True, exist_ok=True)
    io.save(str(dest), ResidueRangeSelect(chain, res_range))
    clean = parser.get_structure("clean", str(dest))
    n = sum(1 for _ in clean.get_residues())
    return n


def minimal_window(hotspots: list[int], padding: int) -> tuple[int, int]:
    lo = max(DOMAIN_RANGE[0], min(hotspots) - padding)
    hi = min(DOMAIN_RANGE[1], max(hotspots) + padding)
    return lo, hi


def write_hotspots(path: Path, hotspots: list[int]) -> None:
    lines = ["# BindCraft hotspot residues (chain A, 2VSM)\n"]
    for res in hotspots:
        lines.append(f"A{res}\n")
    path.write_text("".join(lines))


def main() -> None:
    ap = argparse.ArgumentParser(description="Prepare BindCraft target PDBs for Nipah G")
    ap.add_argument("--mode", choices=["full", "minimal", "both"], default="both")
    ap.add_argument("--pdb-in", type=Path, default=TARGETS_DIR / f"{PDB_ID}.pdb")
    args = ap.parse_args()

    pdb_in = download_pdb(args.pdb_in)

    if args.mode in ("full", "both"):
        full_out = TARGETS_DIR / "nipah_target_full.pdb"
        n = save_trimmed(pdb_in, full_out, "A", DOMAIN_RANGE)
        print(f"[OK] full target: {full_out} ({n} residues)")

    if args.mode in ("minimal", "both"):
        win = minimal_window(FOCAL_HOTSPOTS, MINIMAL_PADDING)
        min_out = TARGETS_DIR / "nipah_target_minimal.pdb"
        n = save_trimmed(pdb_in, min_out, "A", win)
        print(f"[OK] minimal target: {min_out} ({n} residues, window {win[0]}-{win[1]})")

    hotspots_path = TARGETS_DIR / "hotspots.txt"
    write_hotspots(hotspots_path, FOCAL_HOTSPOTS)
    print(f"[OK] hotspots: {hotspots_path}")


if __name__ == "__main__":
    main()
