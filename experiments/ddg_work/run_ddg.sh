#!/bin/bash
# ddG per single mutation: BuildMutant on WT-repaired, then ComputeStability on the model.
# ddG = E(mutant) - E(WT). Positive = destabilizing.
set -u
EVO=/home/gris/.hermes/workspace/ACTIVE/protein-lab/tools/EvoEF2/EvoEF2
W=/home/gris/.hermes/workspace/ACTIVE/protein-lab/experiments/ddg_work
cd "$W"
WT_E=$(grep -E "^Total" wt_stability.txt | awk '{print $3}')
echo "WT reference energy: $WT_E"

for arm in esm3 matched blosum62; do
  out="ddg_${arm}.tsv"
  : > "$out"
  n=0
  while read -r mut; do
    n=$((n+1))
    [ -z "$mut" ] && continue
    d=$(mktemp -d)
    cp oprm1_R_Repair.pdb "$d/s.pdb"
    echo "$mut" > "$d/one.txt"
    ( cd "$d" && "$EVO" --command=BuildMutant --pdb=s.pdb --mutant_file=one.txt >/dev/null 2>&1 )
    model=$(ls "$d"/s_Model_0001.pdb 2>/dev/null | head -1)
    if [ -n "$model" ]; then
      E=$( ( cd "$d" && "$EVO" --command=ComputeStability --pdb=$(basename "$model") 2>/dev/null ) | grep -E "^Total" | awk '{print $3}')
      if [ -n "$E" ]; then
        ddg=$(python3 -c "print(f'{$E - ($WT_E):.3f}')")
        printf "%s\t%s\t%s\n" "$mut" "$E" "$ddg" >> "$out"
      else
        printf "%s\tNA\tNA\n" "$mut" >> "$out"
      fi
    else
      printf "%s\tBUILD_FAIL\tNA\n" "$mut" >> "$out"
    fi
    rm -rf "$d"
    [ $((n % 40)) -eq 0 ] && echo "  $arm: $n done"
  done < "list_${arm}.txt"
  ok=$(awk -F'\t' '$3!="NA"' "$out" | wc -l)
  echo "$arm COMPLETE: $ok/$n succeeded -> $out"
done
echo "ALL_ARMS_DONE"
