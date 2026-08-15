#!/usr/bin/env python3
"""Dockings Vina con PDBQT Meeko (ROOT/ENDROOT) — ligandos validados 8/8"""
import os, json, subprocess, pathlib, re

BASE = pathlib.Path.home() / ".hermes" / "workspace" / "ACTIVE" / "protein-lab"
LIGAND_DIR = BASE / "investigacion-fibromialgia" / "estructuras" / "ligandos_validados"
DOCKING_DIR = BASE / "investigacion-fibromialgia" / "estructuras" / "dockings_validados"
RECEPTOR_DIR = BASE / "investigacion-fibromialgia" / "estructuras"
ALPHAFOLD_DIR = RECEPTOR_DIR / "alphafold"

DOCKING_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = {
    "DRD2": {
        "receptor_6vms": str(RECEPTOR_DIR / "drd2_receptor_6VMS.pdbqt"),
        "receptor_af": str(ALPHAFOLD_DIR / "DRD2_P14416.pdbqt"),
        "center": (109.7, 127.5, 94.0),
        "size": (20, 20, 20),
    },
    "OPRM1": {
        "receptor_af": str(ALPHAFOLD_DIR / "OPRM1_P35372.pdbqt"),
        "center": (-7.7, 8.1, 7.9),
        "size": (22, 22, 22),
    },
    "TACR1": {
        "receptor_af": str(ALPHAFOLD_DIR / "TACR1_P25103.pdbqt"),
        "center": (-1.976, -1.52457, -9.32114),
        "size": (20, 20, 20),
    },
}

ASSIGN = {
    "dopamine": "DRD2",
    "pramipexole": "DRD2",
    "bromocriptine": "DRD2",
    "naloxone": "OPRM1",
    "morphine": "OPRM1",
    "fentanyl": "OPRM1",
    "rolapitant": "TACR1",
    "aprepitant": "TACR1",
}

EXHAUSTIVENESS = 32
NUM_MODES = 9

def parse_vina_log(log_text):
    """Parse Vina log for best ΔG and all modes"""
    modes = []
    for line in log_text.split('\n'):
        m = re.match(r'\s+(\d+)\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)', line)
        if m:
            modes.append({
                "mode": int(m.group(1)),
                "dg": float(m.group(2)),
                "rmsd_lb": float(m.group(3)),
                "rmsd_ub": float(m.group(4)),
            })
    return modes

results = {}

for ligand_name, target_name in ASSIGN.items():
    pdbqt_path = LIGAND_DIR / f"{ligand_name}_validated.pdbqt"
    if not pdbqt_path.exists():
        results[ligand_name] = {"error": f"PDBQT not found"}
        continue
    
    target = TARGETS[target_name]
    cx, cy, cz = target["center"]
    sx, sy, sz = target["size"]
    
    if target_name == "DRD2" and "receptor_6vms" in target:
        receptor = target["receptor_6vms"]
        suffix = "_6VMS"
    else:
        receptor = target["receptor_af"]
        suffix = "_AF"
    
    out_pdbqt = DOCKING_DIR / f"{ligand_name}_{target_name}{suffix}_validated_docked.pdbqt"
    out_log = DOCKING_DIR / f"{ligand_name}_{target_name}{suffix}_validated_log.txt"
    
    cmd = (
        f"vina --receptor {receptor} --ligand {pdbqt_path} "
        f"--center_x {cx} --center_y {cy} --center_z {cz} "
        f"--size_x {sx} --size_y {sy} --size_z {sz} "
        f"--exhaustiveness {EXHAUSTIVENESS} --num_modes {NUM_MODES} "
        f"--out {out_pdbqt}"
    )
    
    print(f"\n=== {ligand_name} -> {target_name}{suffix} ===")
    
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
    
    log_text = proc.stdout + proc.stderr
    if out_log.exists():
        out_log.write_text(log_text)
    
    modes = parse_vina_log(log_text)
    best_dg = modes[0]["dg"] if modes else None
    
    # Check for "mostly positive" (signature of bad ligand)
    positive_modes = sum(1 for m in modes if m["dg"] > 0)
    
    results[ligand_name] = {
        "target": target_name,
        "best_dg": best_dg,
        "all_modes": modes,
        "positive_modes": positive_modes,
        "total_modes": len(modes),
        "out_pdbqt": str(out_pdbqt) if out_pdbqt.exists() else None,
        "exit_code": proc.returncode,
    }
    
    if best_dg is not None:
        print(f"  Best ΔG: {best_dg:.3f} kcal/mol ({len(modes)} modes, {positive_modes} positive)")
    else:
        print(f"  NO MODES FOUND — exit={proc.returncode}")
        print(f"  STDERR tail: {proc.stderr[-200:]}")

out_json = BASE / "investigacion-fibromialgia" / "scripts" / "docking_validated_results.json"
with open(out_json, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n{'='*60}")
print(f"RESUMEN DOCKING (8 ligandos, {EXHAUSTIVENESS} exhaustiveness)")
print(f"{'='*60}")
for name, v in results.items():
    dg = v.get("best_dg")
    pos = v.get("positive_modes", 0)
    tot = v.get("total_modes", 0)
    flag = "⚠️ mostly positive" if pos > tot/2 else ""
    print(f"  {name:18s} -> {v.get('target','?'):6s} : ΔG = {dg:7.3f} kcal/mol  ({pos}/{tot} positive) {flag}")
