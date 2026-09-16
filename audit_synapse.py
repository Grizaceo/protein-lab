
# audit_synapse.py — Rev 2026-04-24 (Fix #7: BioPython parser replaces manual line reader)
import numpy as np
import os
import warnings
from pathlib import Path
from Bio.PDB import PDBParser, Selection
from Bio.PDB.PDBExceptions import PDBConstructionWarning

warnings.filterwarnings('ignore', category=PDBConstructionWarning)
_parser = PDBParser(QUIET=True)


def _load(pdb_path):
    """Carga estructura con BioPython; lanza FileNotFoundError si no existe."""
    p = Path(pdb_path)
    if not p.exists():
        raise FileNotFoundError(f"PDB no encontrado: {p}")
    return _parser.get_structure(p.stem, str(p))[0]


def get_coords(pdb_path, residue_num, atom_name="CA", chain_id=None):
    """Devuelve coordenadas de un átomo específico usando BioPython.
    
    Busca en todos los chains (o en chain_id si se especifica).
    Retorna None si el átomo no se encuentra; no silencia errores de parseo.
    """
    model = _load(pdb_path)
    chains = [model[chain_id]] if chain_id and chain_id in model else model.get_list()
    for chain in chains:
        for res in chain:
            rid = res.get_id()
            # Acepta residuos ATOM normales y HETATM (HEM, etc.)
            if rid[1] == residue_num:
                if atom_name in res:
                    return res[atom_name].get_vector().get_array()
    return None


def get_center_of_mass(pdb_path, atom_filter="FE"):
    """Promedio de coordenadas de todos los átomos que contienen atom_filter en su nombre."""
    model = _load(pdb_path)
    coords = []
    for chain in model:
        for res in chain:
            for atom in res:
                if atom_filter in atom.get_name():
                    coords.append(atom.get_vector().get_array())
    if not coords:
        return None
    return np.mean(coords, axis=0)



if __name__ == "__main__":
    from pathlib import Path
    _script_dir = Path(__file__).resolve().parent
    _mtra_candidates = [
        _script_dir / "data/pdb/MtrA.pdb",
        Path(os.path.expanduser("~/.hermes/workspace/ACTIVE/protein-lab/data/pdb/MtrA.pdb")),
        Path(os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/MtrA.pdb")),
    ]
    mtra_path = str(next((p for p in _mtra_candidates if p.exists()), _mtra_candidates[0]))

    _bfr_candidates = [
        _script_dir / "data/pdb/new_chassis/1BFR.pdb",
        _script_dir / "data/pdb/1BFR.pdb",
        Path(os.path.expanduser("~/.hermes/workspace/ACTIVE/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
        Path(os.path.expanduser("~/.hermes/workspace/protein-lab/data/pdb/new_chassis/1BFR.pdb")),
    ]
    bfr_path = str(next((p for p in _bfr_candidates if p.exists()), _bfr_candidates[0]))


    # 1. MtrA: Distancia Hemo -> CYS 67
    # Buscamos el FE del hemo más cercano a CYS 67
    cys_pos = get_coords(mtra_path, 67, "SG")
    
    hemes = []
    with open(mtra_path, 'r') as f:
        for line in f:
            if "FE" in line[12:16]:
                hemes.append(np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])]))
    
    if cys_pos is not None and hemes:
        dists = [np.linalg.norm(cys_pos - h) for h in hemes]
        min_dist_mtra = min(dists)
        print(f"MtrA: Distancia Hemo (FE) -> Cys67 (SG): {min_dist_mtra:.2f} A")
    
    # 2. BFR: Distancia MET 1 -> Centro del Lumen
    met_pos = get_coords(bfr_path, 1, "SD")
    bfr_center = get_center_of_mass(bfr_path, "FE") # El centro de los hierros es el centro del lumen
    
    if met_pos is not None and bfr_center is not None:
        dist_bfr = np.linalg.norm(met_pos - bfr_center)
        print(f"BFR:  Distancia MET 1 (SD) -> Centro Lumen: {dist_bfr:.2f} A")
        
        total_gap = min_dist_mtra + dist_bfr
        print(f"\nGAP TOTAL ESTIMADO: {total_gap:.2f} A")
        if total_gap < 30.0:
             print("DIAGNÓSTICO: VIABLE (con tunelamiento asistido por clusters intermedios)")
        else:
             print("DIAGNÓSTICO: CRÍTICO. Demasiada distancia para conducción eficiente.")
