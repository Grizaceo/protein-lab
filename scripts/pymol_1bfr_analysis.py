# /// script
# requires-python = ">=3.10, <3.13"
# dependencies = [
#     "pymol-open-source-whl",
#     "numpy",
#     "biopython",
# ]
# ///

import os
import sys

# Set environment variable for headless rendering
os.environ["PYOPENGL_PLATFORM"] = "osmesa"

import pymol
pymol.pymol_argv = ["pymol", "-cq"]
pymol.finish_launching()

from pymol import cmd, util


def run_analysis():
    pdb_path = "data/pdb/new_chassis/1BFR.pdb"
    if not os.path.exists(pdb_path):
        print(f"ERROR: PDB file not found at {pdb_path}")
        cmd.quit()
        sys.exit(1)

    print("Loading 1BFR...")
    cmd.load(pdb_path, "bfr")
    
    n_atoms = cmd.count_atoms("bfr")
    print(f"Successfully loaded 1BFR with {n_atoms} atoms.")
    if n_atoms == 0:
        print("ERROR: Loaded 0 atoms.")
        cmd.quit()
        sys.exit(1)

    # 1. basic structure analysis
    chains = cmd.get_chains("bfr")
    print(f"Chains found: {', '.join(chains)} ({len(chains)} chains)")
    
    n_hemes = cmd.count_atoms("resn HEM and name FE")
    print(f"Number of Heme iron atoms found: {n_hemes}")

    # 2. Distance from native residues on Chain A to nearest Heme FE
    # Let's find the nearest Heme FE to chain A residues 40, 43, 49
    # The hemes are shared at the interfaces, e.g., HEM B 200, etc.
    # Let's write a small loop to find the nearest Heme Fe and measure CA distances
    residues = [40, 43, 49]
    print("\n--- NATIVE STATE DISTANCE MEASUREMENTS (Chain A) ---")
    for resi in residues:
        res_sel = f"chain A and resi {resi} and name CA"
        heme_sel = "resn HEM and name FE"
        
        # Measure distance to all Heme irons and find the minimum
        min_dist = 999.0
        nearest_heme_info = ""
        
        # We can use PyMOL to find the nearest atom
        # Get coordinates of CA
        ca_coord = cmd.get_coords(res_sel)
        if ca_coord is None or len(ca_coord) == 0:
            print(f"Could not get coordinates for residue {resi} CA")
            continue
        ca_pos = ca_coord[0]
        
        # Get coordinates and identifiers of all heme irons
        heme_atoms = []
        cmd.iterate(heme_sel, "heme_atoms.append((chain, resi, name))", space={'heme_atoms': heme_atoms})
        
        for ch, r_num, at_name in heme_atoms:
            h_pos = cmd.get_coords(f"chain {ch} and resi {r_num} and name {at_name}")[0]
            dist = ((ca_pos[0]-h_pos[0])**2 + (ca_pos[1]-h_pos[1])**2 + (ca_pos[2]-h_pos[2])**2)**0.5
            if dist < min_dist:
                min_dist = dist
                nearest_heme_info = f"HEM chain {ch} resi {r_num}"
                
        print(f"  Residue A-{resi} (CA) to nearest Heme ({nearest_heme_info}): {min_dist:.2f} A")

    # 3. Perform in silico mutagenesis: ILE49C, VAL43C, LEU40C on Chain A
    print("\n--- IN SILICO MUTAGENESIS (Chain A: L40C, V43C, I49C) ---")
    cmd.wizard("mutagenesis")
    w = cmd.get_wizard()
    
    for resi in residues:
        sel = f"chain A and resi {resi}"
        print(f"  Mutating {sel} to CYS...")
        w.set_mode("CYS")
        w.do_select(sel)
        w.apply()
    cmd.set_wizard()
    
    # 4. Measure distances from mutated CYS sidechain (SG) to Heme FE
    print("\n--- MUTATED CYS SG SIDECHAIN DISTANCES TO NEAREST HEME FE ---")
    for resi in residues:
        res_sel = f"chain A and resi {resi} and name SG"
        
        sg_coords = cmd.get_coords(res_sel)
        if sg_coords is None or len(sg_coords) == 0:
            print(f"Could not get coordinates for mutated residue A-{resi} SG")
            continue
        sg_pos = sg_coords[0]
        
        min_dist = 999.0
        nearest_heme_info = ""
        nearest_heme_sel = ""
        
        heme_atoms = []
        cmd.iterate("resn HEM and name FE", "heme_atoms.append((chain, resi, name))", space={'heme_atoms': heme_atoms})
        
        for ch, r_num, at_name in heme_atoms:
            h_pos = cmd.get_coords(f"chain {ch} and resi {r_num} and name {at_name}")[0]
            dist = ((sg_pos[0]-h_pos[0])**2 + (sg_pos[1]-h_pos[1])**2 + (sg_pos[2]-h_pos[2])**2)**0.5
            if dist < min_dist:
                min_dist = dist
                nearest_heme_info = f"HEM chain {ch} resi {r_num}"
                nearest_heme_sel = f"chain {ch} and resi {r_num} and name {at_name}"
                
        print(f"  Mutated CYS{resi} (SG) to nearest Heme ({nearest_heme_info}): {min_dist:.2f} A")
        # Draw distance line in PyMOL for visualization
        cmd.distance(f"dist_CYS{resi}_HEM", res_sel, nearest_heme_sel)

    # 5. Styling and rendering outputs
    print("\nStyling and rendering images...")
    
    # Create output directory
    os.makedirs("data/processed", exist_ok=True)

    # Global View: 24-mer capsid
    cmd.hide("all")
    cmd.show("cartoon", "bfr")
    cmd.color("gray90", "bfr")
    
    # Color chains with spectrum or custom colors
    chain_colors = ["cyan", "salmon", "green", "yellow", "magenta",
                    "orange", "slate", "limon", "deeppurple", "wheat"]
    for i, ch in enumerate(chains):
        cmd.color(chain_colors[i % len(chain_colors)], f"chain {ch}")
        
    cmd.show("spheres", "resn HEM")
    cmd.color("red", "resn HEM")
    cmd.set("sphere_scale", 0.8, "resn HEM")
    
    cmd.orient()
    cmd.set("ray_opaque_background", 1)
    cmd.png("data/processed/1BFR_24mer_global.png", width=1200, height=900, dpi=150)
    print("  Saved data/processed/1BFR_24mer_global.png")

    # Zoomed-in View: Inner lumen and mutated pocket
    # Let's focus on chain A, chain B, and the shared HEM (HEM B 200)
    cmd.hide("all")
    # Show cartoon for Chain A and B
    cmd.show("cartoon", "chain A or chain B")
    cmd.color("cyan", "chain A")
    cmd.color("salmon", "chain B")
    cmd.set("cartoon_transparency", 0.3, "chain A or chain B")
    
    # Show mutant residues as sticks
    mutant_sel = "chain A and resi 40+43+49"
    cmd.show("sticks", mutant_sel)
    cmd.color("green", mutant_sel)
    cmd.show("labels", mutant_sel + " and name CA")
    
    # Show Heme B 200 as sticks
    heme_sel = "chain B and resi 200 and resn HEM"
    cmd.show("sticks", heme_sel)
    util.cnc(heme_sel)
    
    # Show coordinated MET 52 residues
    met_sel = "(chain A or chain B) and resi 52 and resn MET"
    cmd.show("sticks", met_sel)
    util.cnc(met_sel)
    
    # Zoom and focus
    focus_sel = f"({mutant_sel}) or ({heme_sel}) or ({met_sel})"
    cmd.zoom(focus_sel, buffer=5.0)
    cmd.orient(focus_sel)
    
    # Show distance lines
    cmd.show("dashes")
    cmd.set("dash_color", "yellow")
    cmd.set("dash_radius", 0.05)
    
    cmd.png("data/processed/1BFR_lumen_mutations_zoom.png", width=1200, height=900, dpi=150)
    print("  Saved data/processed/1BFR_lumen_mutations_zoom.png")

    # Hopping channel close-up
    cmd.zoom("chain A and resi 49 or (chain B and resi 200 and resn HEM)", buffer=3.0)
    cmd.png("data/processed/1BFR_chainA_hopping_channel.png", width=1200, height=900, dpi=150)
    print("  Saved data/processed/1BFR_chainA_hopping_channel.png")

    # Save session file
    session_path = "data/processed/1BFR_engineered.pse"
    cmd.save(session_path)
    print(f"  Saved PyMOL session file to {session_path}")
    
    print("\n--- PyMOL analysis completed successfully! ---")
    cmd.quit()

if __name__ == "__main__":
    run_analysis()
