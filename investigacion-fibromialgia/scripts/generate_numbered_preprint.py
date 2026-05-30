#!/usr/bin/env python3
import pathlib

def main():
    script_dir = pathlib.Path(__file__).resolve().parent
    base_dir = script_dir.parent
    
    input_file = base_dir / "preprint_dopaminergic_convergence_FM.md"
    output_file = base_dir / "preprint_dopaminergic_convergence_FM_numbered.md"
    
    if not input_file.exists():
        print(f"Error: Input preprint not found at {input_file}")
        return
        
    print(f"[INFO] Reading: {input_file.name}")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    numbered_lines = []
    for i, line in enumerate(lines, 1):
        # Format line with 3-digit padding followed by a colon and a space
        numbered_lines.append(f"{i:03d}: {line}")
        
    print(f"[INFO] Writing numbered preprint: {output_file.name}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(numbered_lines)
        
    print("[INFO] Done!")

if __name__ == "__main__":
    main()
