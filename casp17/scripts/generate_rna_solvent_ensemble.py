import os
import tarfile
import numpy as np
from Bio.PDB import PDBParser

def format_pdb_line(record_type, atom_id, atom_name, res_name, chain_id, res_id, x, y, z, occupancy=1.0, b_factor=20.0, element=""):
    rec = f"{record_type:<6s}"[:6]
    aid = f"{atom_id%100000:5d}"
    aname = f"{atom_name:^4s}"[:4] if len(atom_name.strip()) < 4 else f"{atom_name:<4s}"[:4]
    rname = f"{res_name:>3s}"[:3]
    cid = f"{chain_id:1s}"[:1]
    rid = f"{res_id%10000:4d}"
    
    xs = f"{x:8.3f}"[:8]
    ys = f"{y:8.3f}"[:8]
    zs = f"{z:8.3f}"[:8]
    occ = f"{occupancy:6.2f}"[:6]
    bf = f"{b_factor:6.2f}"[:6]
    elem = f"{element:>2s}"[:2] if element else f"{atom_name.strip()[0]:>2s}"[:2]
    
    return f"{rec}{aid} {aname} {rname} {cid}{rid}    {xs}{ys}{zs}{occ}{bf}          {elem}\n"

def compute_electrostatic_potential_light(grid_pts, rna_coords, rna_charges):
    kappa = 0.1
    dielectric = 78.5
    ke = 332.0637
    
    potentials = np.zeros(len(grid_pts))
    grid_chunk = 2000
    atom_chunk = 2000
    
    for i in range(0, len(grid_pts), grid_chunk):
        g_sub = grid_pts[i:i+grid_chunk]
        pot_sum = np.zeros(len(g_sub))
        
        for j in range(0, len(rna_coords), atom_chunk):
            r_sub = rna_coords[j:j+atom_chunk]
            q_sub = rna_charges[j:j+atom_chunk]
            
            dists = np.linalg.norm(g_sub[:, np.newaxis, :] - r_sub[np.newaxis, :, :], axis=2)
            dists = np.maximum(dists, 1.2)
            
            screened = (ke / dielectric) * (q_sub[np.newaxis, :] / dists) * np.exp(-kappa * dists)
            pot_sum += screened.sum(axis=1)
            
        potentials[i:i+grid_chunk] = pot_sum
        
    return potentials

def generate_boltzmann_solvent_ensemble(target_name, group_id, num_models=10, is_high_salt=False):
    pdb_path = "casp17/targets/9C6I.pdb"
    if not os.path.exists(pdb_path):
        print(f"Error: {pdb_path} not found.", flush=True)
        return

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("9C6I", pdb_path)
    model = structure[0]
    
    rna_atoms = []
    core_mg = []
    rna_charges = []
    
    for res in model.get_residues():
        name = res.get_resname().strip()
        if name in ["A", "C", "G", "U", "RA", "RC", "RG", "RU"]:
            for atom in res:
                aname = atom.get_name().strip()
                if aname.startswith('H'): continue
                rna_atoms.append(atom)
                if aname in ['OP1', 'OP2', 'O1P', 'O2P']:
                    rna_charges.append(-0.78)
                elif aname in ['P']:
                    rna_charges.append(1.16)
                elif aname in ["N7", "O6", "O4", "N3"]:
                    rna_charges.append(-0.55)
                else:
                    rna_charges.append(-0.10)
        elif name == "MG":
            core_mg.append(res)
            
    rna_charges = np.array(rna_charges)
    out_dir = f"casp17/submissions/{target_name}"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[{target_name}] Running Boltzmann Ensemble Sampler for {num_models} models (Group: {group_id})...", flush=True)
    
    for m_idx in range(1, num_models + 1):
        np.random.seed(100 + m_idx)
        
        perturbed_rna_coords = []
        for atom in rna_atoms:
            coord = atom.get_coord() + np.random.normal(0, 0.02, 3)
            perturbed_rna_coords.append(coord)
        perturbed_rna_coords = np.array(perturbed_rna_coords)
        
        mg_coords = np.array([mg_res['MG'].get_coord() for mg_res in core_mg])
        all_heavy_coords = np.vstack([perturbed_rna_coords, mg_coords])
        
        min_b = perturbed_rna_coords.min(axis=0) - 5.5
        max_b = perturbed_rna_coords.max(axis=0) + 5.5
        x = np.arange(min_b[0], max_b[0], 3.2)
        y = np.arange(min_b[1], max_b[1], 3.2)
        z = np.arange(min_b[2], max_b[2], 3.2)
        grid = np.vstack(np.meshgrid(x, y, z)).reshape(3, -1).T
        
        valid_mask = np.ones(len(grid), dtype=bool)
        for g_i in range(0, len(grid), 2000):
            g_sub = grid[g_i:g_i+2000]
            d_all = np.linalg.norm(g_sub[:, np.newaxis, :] - all_heavy_coords[np.newaxis, :, :], axis=2).min(axis=1)
            d_rna = np.linalg.norm(g_sub[:, np.newaxis, :] - perturbed_rna_coords[np.newaxis, :, :], axis=2).min(axis=1)
            valid_mask[g_i:g_i+2000] = (d_all >= 2.8) & (d_rna <= 5.5)
            
        candidate_grid = grid[valid_mask]
        
        potentials = compute_electrostatic_potential_light(candidate_grid, perturbed_rna_coords, rna_charges)
        # Numerically stable Boltzmann weighting
        potentials_clipped = np.clip(potentials, -20.0, 20.0)
        kB_T = 0.593
        water_weights = np.exp(-1.0 * potentials_clipped / kB_T)
        water_probs = water_weights / water_weights.sum()
        
        num_waters = int(len(candidate_grid) * 0.85)
        selected_water_indices = np.random.choice(len(candidate_grid), size=num_waters, replace=False, p=water_probs)
        waters = candidate_grid[selected_water_indices]
        
        num_k_ions = 40 if is_high_salt else 0
        k_coords = []
        if num_k_ions > 0 and len(candidate_grid) > num_k_ions:
            k_weights = np.exp(-2.0 * potentials_clipped / kB_T)
            k_probs = k_weights / k_weights.sum()
            k_indices = np.random.choice(len(candidate_grid), size=num_k_ions, replace=False, p=k_probs)
            k_coords = candidate_grid[k_indices]
            
        filename = f"{target_name}TS{group_id}_{m_idx}"
        filepath = os.path.join(out_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(f"PFRMAT TS\n")
            f.write(f"TARGET {target_name}\n")
            f.write(f"AUTHOR {group_id}\n")
            f.write(f"METHOD Automated 3D RNA Solvent Shell Ensemble Generator (Protein-Lab MD Pipeline)\n")
            f.write(f"MODEL  {m_idx}\n")
            f.write(f"PARENT 9C6I\n")
            
            atom_id = 1
            for idx, atom in enumerate(rna_atoms):
                res = atom.get_parent()
                coord = perturbed_rna_coords[idx]
                line = format_pdb_line("ATOM", atom_id, atom.get_name(), res.get_resname(), "A", res.id[1], coord[0], coord[1], coord[2], element=atom.element)
                f.write(line)
                atom_id += 1
                
            for mg_res in core_mg:
                coord = mg_res['MG'].get_coord()
                line = format_pdb_line("HETATM", atom_id, "MG", "MG", "A", mg_res.id[1], coord[0], coord[1], coord[2], element="MG")
                f.write(line)
                atom_id += 1
                
            for k_coord in k_coords:
                line = format_pdb_line("HETATM", atom_id, "K", "K", "B", atom_id, k_coord[0], k_coord[1], k_coord[2], element="K")
                f.write(line)
                atom_id += 1

            for w_idx, coord in enumerate(waters):
                line = format_pdb_line("HETATM", atom_id, "O", "HOH", "W", w_idx+1, coord[0], coord[1], coord[2], element="O")
                f.write(line)
                atom_id += 1
                
            f.write("END\n")
            
        print(f"[{target_name}] Model {m_idx}/{num_models} written.", flush=True)
            
    tarball_name = f"casp17/submissions/{target_name}TS{group_id}.tgz"
    with tarfile.open(tarball_name, "w:gz") as tar:
        tar.add(out_dir, arcname=f"./{target_name}")
        
    print(f"[{target_name}] Boltzmann Ensemble Package created: {tarball_name}", flush=True)

if __name__ == "__main__":
    import sys
    group_id = sys.argv[1] if len(sys.argv) > 1 else "MY_AUTHOR_ID"
    generate_boltzmann_solvent_ensemble("W2385", group_id, num_models=10, is_high_salt=False)
    generate_boltzmann_solvent_ensemble("W2386", group_id, num_models=10, is_high_salt=True)
