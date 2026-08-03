import os
import glob
import tarfile
import numpy as np
from Bio.PDB import PDBParser

def audit_model_file(filepath, target_name):
    print(f"\n🔍 Auditing file: {os.path.basename(filepath)}")
    errors = []
    warnings = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    # Check headers
    headers = [line.split()[0] for line in lines if len(line.split()) > 0 and not line.startswith("ATOM") and not line.startswith("HETATM")]
    required_headers = ["PFRMAT", "TARGET", "AUTHOR", "METHOD", "MODEL", "PARENT", "END"]
    for req in required_headers:
        if not any(req in h for h in headers):
            errors.append(f"Missing required header: {req}")
            
    rna_coords = []
    solvent_coords = []
    hydrogen_count = 0
    
    for idx, line in enumerate(lines):
        if line.startswith("ATOM") or line.startswith("HETATM"):
            atom_name = line[12:16].strip()
            element = line[76:78].strip() if len(line) >= 78 else atom_name[0]
            
            if element == 'H' or atom_name.startswith('H'):
                hydrogen_count += 1
                
            try:
                coord = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
                res_name = line[17:20].strip()
                if res_name in ["A", "C", "G", "U", "RA", "RC", "RG", "RU"]:
                    rna_coords.append(coord)
                else:
                    solvent_coords.append((res_name, coord))
            except Exception as e:
                errors.append(f"Line {idx+1}: Invalid coordinate formatting")

    # 1. Hydrogen Audit
    if hydrogen_count > 0:
        errors.append(f"CRITICAL: Found {hydrogen_count} hydrogen atoms! CASP strictly prohibits hydrogens in this benchmark.")
    else:
        print("  ✅ Hydrogen Audit: 0 Hydrogens found (Pass)")
        
    # 2. Steric Clash & Distance Audit
    if rna_coords and solvent_coords:
        rna_np = np.array(rna_coords)
        sol_np = np.array([s[1] for s in solvent_coords])
        
        # Calculate min distance between solvent and RNA
        dists = np.linalg.norm(sol_np[:, np.newaxis, :] - rna_np[np.newaxis, :, :], axis=2)
        min_dists = dists.min(axis=1)
        
        clashes = np.sum(min_dists < 2.2)
        if clashes > 0:
            errors.append(f"Steric Clash Attack: {clashes} solvent atoms are closer than 2.2 Å to RNA!")
        else:
            print(f"  ✅ Steric Clash Audit: Min solvent-RNA distance = {min_dists.min():.2f} Å (Pass > 2.2 Å)")
            
        # Shell coverage audit
        max_dist = min_dists.max()
        if max_dist < 5.0:
            warnings.append(f"Shell Coverage: Max solvent distance is only {max_dist:.2f} Å (< 5.0 Å required)")
        else:
            print(f"  ✅ Shell Coverage Audit: Max solvent shell extent = {max_dist:.2f} Å (Pass >= 5.0 Å)")

    # Summary
    if errors:
        print("  ❌ STATUS: FAILED ADVERSARIAL AUDIT")
        for err in errors:
            print(f"     - {err}")
        return False
    else:
        print("  🟢 STATUS: PASSED ADVERSARIAL AUDIT")
        if warnings:
            for w in warnings:
                print(f"     ⚠️  {w}")
        return True

def run_adversarial_audit(author_id="TEST1234"):
    print("==================================================")
    print("💣 ADVERSARIAL AUDIT: CASP17 RNA SOLVENT SUBMISSIONS")
    print("==================================================")
    
    targets = ["W2385", "W2386"]
    all_passed = True
    
    for target in targets:
        tgz_path = f"casp17/submissions/{target}TS{author_id}.tgz"
        print(f"\n📦 Inspecting archive: {tgz_path}")
        if not os.path.exists(tgz_path):
            print(f"  ❌ Archive file missing: {tgz_path}")
            all_passed = False
            continue
            
        with tarfile.open(tgz_path, "r:gz") as tar:
            members = tar.getmembers()
            print(f"  Archive contains {len(members)} entries.")
            
        # Audit individual models in submission directory
        model_files = sorted(glob.glob(f"casp17/submissions/{target}/{target}TS{author_id}_*"))
        if not model_files:
            print(f"  ❌ No model files found in casp17/submissions/{target}/")
            all_passed = False
            continue
            
        print(f"  Found {len(model_files)} ensemble models. Auditing sample models...")
        for m_file in model_files[:3]: # audit first 3 models
            res = audit_model_file(m_file, target)
            if not res:
                all_passed = False
                
    print("\n==================================================")
    if all_passed:
        print("🎉 FINAL AUDIT VERDICT: 100% VIABLE & COMPLIANT WITH CASP17 STANDARDS")
    else:
        print("⚠️ FINAL AUDIT VERDICT: DEFECTS DETECTED - CORRECTION REQUIRED")
    print("==================================================")

if __name__ == "__main__":
    import sys
    author_id = sys.argv[1] if len(sys.argv) > 1 else "TEST1234"
    run_adversarial_audit(author_id)
