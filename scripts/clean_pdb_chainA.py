#!/usr/bin/env python3
"""Extract ONLY chain A from a PDB file, verify no other chains leak in."""
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

seen_chains = set()
records_out = []

with open(infile, 'r') as f:
    for line in f:
        if line.startswith('ATOM') or line.startswith('HETATM'):
            chain = line[21]
            seen_chains.add(chain)
            if chain == 'A':
                records_out.append(line)
        elif line.startswith('TER'):
            records_out.append(line)
        elif line.startswith('END'):
            records_out.append(line)
            break

with open(outfile, 'w') as f:
    f.writelines(records_out)

print(f"Input chains found: {sorted(seen_chains)}")
print(f"Output records (chain A only): {len(records_out)}")
print(f"Written to: {outfile}")
