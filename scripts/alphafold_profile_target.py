#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
alphafold_profile_target.py
Automated AlphaFold DB structure downloading, pLDDT analysis, and PAE-based domain clustering.
"""

import argparse
import json
import os
import sys
import time
import requests
import networkx as nx
import numpy as np

# API Endpoint
AF_API_URL = "https://alphafold.ebi.ac.uk/api/prediction/"

def fetch_url_with_retry(url, is_json=False, timeout=30, retries=3, backoff_factor=2):
    """
    Fetches a URL with exponential backoff and timeout.
    """
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 503:
                raise requests.exceptions.HTTPError("503 Service Unavailable")
            response.raise_for_status()
            if is_json:
                return response.json()
            return response.content
        except (requests.exceptions.RequestException, ValueError) as e:
            if attempt < retries:
                sleep_time = backoff_factor ** (attempt + 1)
                print(f"[!] Error fetching {url}: {e}. Retrying in {sleep_time}s... (Attempt {attempt + 1}/{retries})")
                time.sleep(sleep_time)
            else:
                print(f"[!] Failed to fetch {url} after {retries} retries.")
                raise e

def parse_plddt_from_cif(cif_path):
    """
    Parses per-residue pLDDT scores from the B-factor column of an mmCIF file.
    Uses the _atom_site.B_iso_or_equiv field.
    """
    residue_plddt = {}
    with open(cif_path, 'r') as f:
        in_atom_site = False
        columns = []
        for line in f:
            line = line.strip()
            if line.startswith('loop_'):
                in_atom_site = False
                columns = []
                continue
            if line.startswith('_atom_site.'):
                in_atom_site = True
                columns.append(line)
                continue
            if in_atom_site and (line.startswith('ATOM') or line.startswith('HETATM')):
                parts = line.split()
                try:
                    seq_id_idx = columns.index('_atom_site.label_seq_id')
                    b_iso_idx = columns.index('_atom_site.B_iso_or_equiv')
                    
                    res_num = int(parts[seq_id_idx])
                    plddt = float(parts[b_iso_idx])
                    
                    # Store first atom pLDDT of each residue (they are identical)
                    if res_num not in residue_plddt:
                        residue_plddt[res_num] = plddt
                except (ValueError, IndexError):
                    pass
            elif line.startswith('#') or line.startswith('data_'):
                in_atom_site = False
                
    if not residue_plddt:
        return []
    
    max_res = max(residue_plddt.keys())
    plddts = [0.0] * max_res
    for r, val in residue_plddt.items():
        plddts[r-1] = val
    return plddts

def load_pae_matrix(pae_path):
    """
    Loads and parses the PAE matrix from a JSON file, handling all standard EBI shapes.
    """
    with open(pae_path, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        data = data[0]
        
    if "predicted_aligned_error" in data:
        pae = data["predicted_aligned_error"]
    elif "distance" in data:
        pae = data["distance"]
    else:
        raise ValueError(f"Could not locate PAE matrix in JSON keys: {list(data.keys())}")
          
    if isinstance(pae, list) and len(pae) > 0:
        if isinstance(pae[0], list):
            return pae
        elif isinstance(pae[0], (int, float)):
            n_res = int(len(pae) ** 0.5)
            pae_2d = [pae[i * n_res : (i + 1) * n_res] for i in range(n_res)]
            return pae_2d
          
    if "residue1Id" in data and "distance" in data:
        res1 = data["residue1Id"]
        res2 = data["residue2Id"]
        dist = data["distance"]
        n_res = max(res1)
        pae_2d = [[0.0] * n_res for _ in range(n_res)]
        for r1, r2, d in zip(res1, res2, dist):
            pae_2d[r1 - 1][r2 - 1] = d
        return pae_2d
          
    raise ValueError("Unsupported PAE JSON format.")

def cluster_domains_pae(pae_matrix, plddts, pae_power=1.0, min_domain_size=15):
    """
    Performs PAE-based rigid domain clustering.
    Builds a co-rigidity graph using standard cutoff of 5.0 Å scaled by pae_power.
    Finds connected components and filters by minimum size.
    """
    n_res = len(pae_matrix)
    cutoff = 5.0 * pae_power
    
    G = nx.Graph()
    G.add_nodes_from(range(n_res))
    
    # Build co-rigidity graph
    for i in range(n_res):
        if plddts[i] < 50:
            continue
        for j in range(i + 1, n_res):
            if plddts[j] < 50:
                continue
            if pae_matrix[i][j] < cutoff and pae_matrix[j][i] < cutoff:
                G.add_edge(i, j)
                
    components = list(nx.connected_components(G))
    domains = []
    
    for comp in components:
        sorted_nodes = sorted(list(comp))
        # Find contiguous segments in the component
        segments = []
        current_segment = []
        for r in sorted_nodes:
            if not current_segment:
                current_segment.append(r)
            elif r == current_segment[-1] + 1:
                current_segment.append(r)
            else:
                segments.append(current_segment)
                current_segment = [r]
        if current_segment:
            segments.append(current_segment)
            
        for seg in segments:
            if len(seg) >= min_domain_size:
                start = seg[0] + 1
                end = seg[-1] + 1
                length = len(seg)
                seg_plddts = [plddts[r] for r in seg if r < len(plddts)]
                mean_plddt = float(np.mean(seg_plddts)) if seg_plddts else 0.0
                domains.append({
                    "start": start,
                    "end": end,
                    "length": length,
                    "mean_plddt": round(mean_plddt, 2)
                })
                
    # Sort domains by start residue
    domains.sort(key=lambda d: d["start"])
    return domains

def segment_idrs(plddts, min_length=10):
    """
    Finds contiguous segments of residues with pLDDT < 50 of length >= min_length.
    """
    idrs = []
    current_idr = []
    
    for idx, plddt in enumerate(plddts):
        if plddt < 50:
            current_idr.append(idx)
        else:
            if len(current_idr) >= min_length:
                start = current_idr[0] + 1
                end = current_idr[-1] + 1
                length = len(current_idr)
                mean_plddt = float(np.mean([plddts[i] for i in current_idr]))
                idrs.append({
                    "start": start,
                    "end": end,
                    "length": length,
                    "mean_plddt": round(mean_plddt, 2)
                })
            current_idr = []
            
    if len(current_idr) >= min_length:
        start = current_idr[0] + 1
        end = current_idr[-1] + 1
        length = len(current_idr)
        mean_plddt = float(np.mean([plddts[i] for i in current_idr]))
        idrs.append({
            "start": start,
            "end": end,
            "length": length,
            "mean_plddt": round(mean_plddt, 2)
        })
        
    return idrs

def analyze_plddt_distribution(plddts):
    """
    Computes percentage of residues falling into standard AlphaFold confidence bins.
    """
    total = len(plddts)
    if total == 0:
        return {"very_high": 0.0, "high": 0.0, "low": 0.0, "very_low": 0.0}
        
    very_high = sum(1 for p in plddts if p > 90)
    high = sum(1 for p in plddts if 70 <= p <= 90)
    low = sum(1 for p in plddts if 50 <= p < 70)
    very_low = sum(1 for p in plddts if p < 50)
    
    return {
        "very_high": round((very_high / total) * 100, 2),
        "high": round((high / total) * 100, 2),
        "low": round((low / total) * 100, 2),
        "very_low": round((very_low / total) * 100, 2)
    }

def update_global_index(output_dir, new_profile):
    """
    Updates or creates an INDEX.md summary table file inside output_dir.
    """
    index_path = os.path.join(output_dir, "INDEX.md")
    profiles = {}
    
    if os.path.exists(index_path):
        # We can scan the directory for all *_profile.json files instead of parsing the markdown
        for filename in os.listdir(output_dir):
            if filename.endswith("_profile.json"):
                try:
                    with open(os.path.join(output_dir, filename), 'r') as f:
                        prof = json.load(f)
                        profiles[prof["uniprot_id"]] = prof
                except Exception:
                    pass
    else:
        profiles[new_profile["uniprot_id"]] = new_profile
        
    # Always include the new profile (possibly overwriting)
    profiles[new_profile["uniprot_id"]] = new_profile
    
    # Write a beautiful INDEX.md
    with open(index_path, "w") as f:
        f.write("# AlphaFold Target Profiles Index\n\n")
        f.write("This file index consolidates the automated structural analysis results for the profiled targets.\n\n")
        f.write("## Summary Table\n\n")
        f.write("| UniProt ID | Length (AAs) | Global Mean pLDDT | Domains Detected | IDRs Detected | Very High pLDDT (>90) % | Very Low pLDDT (<50) % |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- |\n")
        
        for uid in sorted(profiles.keys()):
            p = profiles[uid]
            dist = p["plddt_distribution"]
            n_doms = len(p["domains"])
            n_idrs = len(p["idrs"])
            f.write(f"| [{uid}](file:///./{uid}_profile.json) | {p['length']} | {p['global_mean_plddt']:.2f} | {n_doms} | {n_idrs} | {dist['very_high']}% | {dist['very_low']}% |\n")
            
        f.write("\n\n*Generated automatically by `alphafold_profile_target.py` on {}*\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))

def main():
    parser = argparse.ArgumentParser(description="Profile structural features of an EBI AlphaFold target.")
    parser.add_argument("uniprot_id", help="UniProt Accession ID of the target (e.g. P14416)")
    parser.add_argument("--output", "-o", default="data/alphafold", help="Output directory to save results")
    parser.add_argument("--pae-power", type=float, default=1.0, help="Scaling factor for PAE-based rigid domain detection (default: 1.0)")
    parser.add_argument("--min-domain-size", type=int, default=15, help="Minimum residue length to define a domain (default: 15)")
    
    args = parser.parse_args()
    
    uniprot_id = args.uniprot_id.strip().upper()
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"[*] Starting profiling pipeline for UniProt ID: {uniprot_id}")
    
    # 1. Fetch AlphaFold DB Metadata
    api_url = f"{AF_API_URL}{uniprot_id}"
    print(f"[*] Requesting AlphaFold metadata from EBI API: {api_url}")
    
    try:
        api_data = fetch_url_with_retry(api_url, is_json=True)
    except Exception as e:
        print(f"[!] Critical Error fetching API metadata: {e}")
        sys.exit(1)
        
    if not api_data:
        print(f"[!] Error: No AlphaFold entry found for {uniprot_id}")
        sys.exit(1)
        
    # Match canonical entry
    entry = None
    for e in api_data:
        if e.get("uniprotAccession") == uniprot_id:
            entry = e
            break
    if entry is None:
        entry = max(api_data, key=lambda e: e.get("sequenceEnd", 0))
        print(f"[!] WARNING: Using non-canonical/longest isoform entry for {uniprot_id}")
        
    entry_acc = entry.get("uniprotAccession", uniprot_id)
    print(f"[+] Found entry: {entry_acc} ({entry.get('sequenceEnd', 0)} residues)")
    
    # Save API metadata
    metadata_filename = f"AF-{entry_acc}-F1-metadata.json"
    metadata_path = os.path.join(output_dir, metadata_filename)
    with open(metadata_path, 'w') as f:
        json.dump(entry, f, indent=2)
    print(f"[+] Saved EBI API metadata to: {metadata_path}")
    
    # 2. Download mmCIF and PAE matrix files
    cif_url = entry.get("cifUrl")
    pae_url = entry.get("paeDocUrl")
    
    if not cif_url or not pae_url:
        print("[!] Error: Entry does not contain both mmCIF and PAE matrix URLs.")
        sys.exit(1)
        
    cif_filename = cif_url.split("/")[-1]
    pae_filename = pae_url.split("/")[-1]
    
    cif_path = os.path.join(output_dir, cif_filename)
    pae_path = os.path.join(output_dir, pae_filename)
    
    print(f"[*] Fetching mmCIF structure from: {cif_url}")
    try:
        cif_content = fetch_url_with_retry(cif_url)
        with open(cif_path, 'wb') as f:
            f.write(cif_content)
        print(f"[+] Saved mmCIF structure to: {cif_path}")
    except Exception as e:
        print(f"[!] Error downloading mmCIF structure: {e}")
        sys.exit(1)
        
    print(f"[*] Fetching PAE matrix from: {pae_url}")
    try:
        pae_content = fetch_url_with_retry(pae_url)
        with open(pae_path, 'wb') as f:
            f.write(pae_content)
        print(f"[+] Saved PAE matrix to: {pae_path}")
    except Exception as e:
        print(f"[!] Error downloading PAE matrix: {e}")
        sys.exit(1)
        
    # 3. Parse pLDDT from CIF
    print("[*] Parsing pLDDT values from mmCIF...")
    plddts = parse_plddt_from_cif(cif_path)
    if not plddts:
        print("[!] Error: Failed to parse pLDDT scores from the mmCIF file.")
        sys.exit(1)
    print(f"[+] Parsed {len(plddts)} residue pLDDT values.")
    
    # 4. Load PAE Matrix
    print("[*] Loading PAE matrix...")
    try:
        pae_matrix = load_pae_matrix(pae_path)
    except Exception as e:
        print(f"[!] Error loading PAE matrix: {e}")
        sys.exit(1)
    print(f"[+] Loaded PAE matrix of shape {len(pae_matrix)}x{len(pae_matrix[0])}")
    
    if len(pae_matrix) != len(plddts):
        print(f"[!] WARNING: PAE dimension ({len(pae_matrix)}) differs from parsed residue count ({len(plddts)}). Using minimum.")
        n_res = min(len(pae_matrix), len(plddts))
        pae_matrix = [row[:n_res] for row in pae_matrix[:n_res]]
        plddts = plddts[:n_res]
        
    # 5. Core analysis
    print("[*] Performing structural analysis...")
    global_mean_plddt = float(np.mean(plddts))
    plddt_dist = analyze_plddt_distribution(plddts)
    idrs = segment_idrs(plddts, min_length=10)
    domains = cluster_domains_pae(pae_matrix, plddts, pae_power=args.pae_power, min_domain_size=args.min_domain_size)
    
    # Save target profile
    profile = {
        "uniprot_id": uniprot_id,
        "entry_accession": entry_acc,
        "length": len(plddts),
        "global_mean_plddt": round(global_mean_plddt, 2),
        "plddt_distribution": plddt_dist,
        "domains": domains,
        "idrs": idrs,
        "pae_power": args.pae_power,
        "min_domain_size": args.min_domain_size,
        "cif_file": cif_filename,
        "pae_file": pae_filename,
        "metadata_file": metadata_filename
    }
    
    profile_path = os.path.join(output_dir, f"{uniprot_id}_profile.json")
    with open(profile_path, 'w') as f:
        json.dump(profile, f, indent=2)
        
    print(f"[+] Saved structural profile to: {profile_path}")
    print(f"    Global Mean pLDDT: {global_mean_plddt:.2f}")
    print(f"    Domains Detected: {len(domains)}")
    print(f"    IDRs Detected: {len(idrs)}")
    
    # 6. Update global index
    update_global_index(output_dir, profile)
    print(f"[+] Updated global summary index in {output_dir}/INDEX.md")
    print("[*] Pipeline execution completed successfully!")

if __name__ == "__main__":
    main()
