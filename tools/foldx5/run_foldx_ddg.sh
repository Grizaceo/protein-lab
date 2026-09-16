#!/bin/bash
# run_foldx_ddg.sh — score point mutations with FoldX 5.1 (Windows binary via WSL interop).
# Usage: run_foldx_ddg.sh <unrepaired.pdb> <mutations.txt>
#   mutations.txt: one "<wt><chain><pos><mut>;" per line (e.g. AR113F;) — WT FIRST, then chain.
# Output: ddG table on stdout and ddg_<ts>/ddg.tsv (kcal/mol, positive = destabilizing).
# NOTE: the exe is a Windows binary — all paths passed to it must be RELATIVE (it runs with CWD
# set to the per-run workdir; rotabase.txt is copied there).
set -euo pipefail
PDB="$(readlink -f "$1")"
LIST="$(readlink -f "$2")"
FX=/mnt/c/temp/foldx5
EXE="$FX/foldx_1_20270131.exe"
BASE=$(basename "$PDB" .pdb)
WORK="$FX/ddg_$(date +%s)"
mkdir -p "$WORK"
cp "$PDB" "$WORK/${BASE}.pdb"
cp "$LIST" "$WORK/individual_list.txt"
cp "$FX/rotabase.txt" "$WORK/rotabase.txt"
cd "$WORK"
"$EXE" --command=RepairPDB --pdb="${BASE}.pdb" > repair.log 2>&1
"$EXE" --command=BuildModel --pdb="${BASE}_Repair.pdb" \
  --mutant-file=individual_list.txt --numberOfRuns=1 > buildmodel.log 2>&1
# Dif_*.fxout: row = mutant model, col2 = ddG vs WT (kcal/mol)
awk -F'\t' 'NR>7 && $2!="" {print $1"\t"$2}' "Dif_${BASE}_Repair.fxout" | tee ddg.tsv
echo "DONE: $WORK"