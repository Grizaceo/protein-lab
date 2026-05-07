#!/usr/bin/env python3
"""
Fase 1: Caracterizacion Fisicoquimica (ProtParam)
Analiza las propiedades basicas de CsgA (Curli) y ELP (Elastina).
"""
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd

SEQUENCES = {
    "CsgA_mature": "GVVPQVGPGGNASVDAAVASSSAVTVGQVGAVSNAVAQDSSVKVGLTDITAYGNGPNANSVIALANQSNVKVGMTTVVAYGNGPNASNIYALANQSNVEVGMTTIVSYGNGANASAVVALSQQTNVSVGMTTVTAYGNGPN",
    "ELP_10x": "VPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVG",
    "CsgA_ELP_Fusion": "GVVPQVGPGGNASVDAAVASSSAVTVGQVGAVSNAVAQDSSVKVGLTDITAYGNGPNANSVIALANQSNVKVGMTTVVAYGNGPNASNIYALANQSNVEVGMTTIVSYGNGANASAVVALSQQTNVSVGMTTVTAYGNGPNVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVGVPGVG"
}

def analyze_protein(name, seq):
    analyser = ProteinAnalysis(seq)
    
    # Propiedades basicas
    mw = analyser.molecular_weight()
    pi = analyser.isoelectric_point()
    instability = analyser.instability_index() # > 40 es inestable
    gravy = analyser.gravy() # > 0 es hidrofobica (insoluble generalmente)
    
    # Carga neta aproximada a pH 7.0
    charge = pi - 7.0 # Estimacion burda: positiva si pi > 7
    
    return {
        "Nombre": name,
        "MW (kDa)": mw / 1000,
        "pI": pi,
        "Instabilidad": instability,
        "Status": "Estable" if instability < 40 else "Inestable",
        "GRAVY (Hidrofobicidad)": gravy,
        "Carga aprox pH 7": "Positiva" if pi > 7 else "Negativa"
    }

def main():
    results = []
    for name, seq in SEQUENCES.items():
        results.append(analyze_protein(name, seq))
    
    df = pd.DataFrame(results)
    
    print("\n" + "="*70)
    print("FASE 1: RESULTADOS FISICOQUIMICOS (ProtParam)")
    print("="*70)
    
    # Formateo para terminal
    print(df.to_string(index=False))
    
    print("\n" + "="*70)
    print("INTERPRETACION:")
    print("-" * 70)
    print("1. CsgA (Curli):")
    p_csga = [r for r in results if r['Nombre'] == 'CsgA_mature'][0]
    print(f"   - Hidrofobicidad (GRAVY): {p_csga['GRAVY (Hidrofobicidad)']:.3f}")
    print("     (Valores cercanos a 0 o negativos indican tendencia a agregarse)")
    
    print("\n2. ELP (Elastina):")
    p_elp = [r for r in results if r['Nombre'] == 'ELP_10x'][0]
    print(f"   - Instabilidad: {p_elp['Instabilidad']:.2f} ({p_elp['Status']})")
    print("     (ELPs son intrinsecamente desordenadas, lo que les da su elasticidad)")

    print("\n3. CONCLUSION FUSION:")
    p_fus = [r for r in results if r['Nombre'] == 'CsgA_ELP_Fusion'][0]
    print(f"   - El pI de la fusion ({p_fus['pI']:.2f}) determina en que buffers")
    print("     el material sera mas o menos soluble antes de fibrilar.")
    print("="*70)

if __name__ == "__main__":
    main()
