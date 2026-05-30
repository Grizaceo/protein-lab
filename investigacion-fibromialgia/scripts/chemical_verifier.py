#!/usr/bin/env python3
"""
Filtro de Verificación de Alucinaciones Químicas (Anti-Hallucination Pipeline)
Diseñado para la validación rápida de SMILES generados por IA.
Fases:
1. RDKit Sanitization (Física básica de valencias)
2. QED & Lipinski's Rule of 5 (Propiedades de drogabilidad)
3. PAINS Filters (Compuestos reactivos / interferentes)
4. Synthetic Accessibility Estimator (Sintetizabilidad)
"""

import sys
import os

try:
    from rdkit import Chem
    from rdkit.Chem import QED
    from rdkit.Chem import Lipinski
    from rdkit.Chem import Fragments
    from rdkit.Chem import Crippen
    from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
except ImportError:
    print("[ERROR] RDKit no está instalado en este entorno de Python.")
    print("Por favor, asegúrate de instalar RDKit antes de ejecutar el verificador.")
    sys.exit(1)

class ChemicalVerifier:
    def __init__(self):
        # Inicializar el catálogo oficial de filtros PAINS (más de 400 subestructuras de la industria)
        params = FilterCatalogParams()
        params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
        self.pains_catalog = FilterCatalog(params)
        
    def sanitize_check(self, smiles):
        """Filtro 1: Verifica si el SMILES es legible y químicamente válido en valencias."""
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return None, "FAILED_PARSING"
            
            # Forzar la sanitización completa
            Chem.SanitizeMol(mol)
            return mol, "PASSED"
        except Exception as e:
            return None, f"FAILED_VALENCY: {str(e)}"

    def check_lipinski(self, mol):
        """Filtro 2a: Regla de 5 de Lipinski (Drogabilidad básica)."""
        mw = Chem.rdMolDescriptors.CalcExactMolWt(mol)
        logp = Crippen.MolLogP(mol)
        hbd = Lipinski.NumHDonors(mol)
        hba = Lipinski.NumHAcceptors(mol)
        rot_bonds = Lipinski.NumRotatableBonds(mol)
        
        # Criterios de Lipinski
        passed = (mw <= 500) and (logp <= 5.0) and (hbd <= 5) and (hba <= 10)
        
        details = {
            "MW": round(mw, 2),
            "logP": round(logp, 2),
            "HBD": hbd,
            "HBA": hba,
            "RotBonds": rot_bonds,
            "Passed_Lipinski": passed
        }
        return passed, details

    def check_qed_drogabilidad(self, mol):
        """Filtro 2b: Puntuación de QED (Quantitative Estimate of Drug-likeness)."""
        qed_value = QED.qed(mol)
        # Un score QED > 0.50 suele considerarse óptimo para compuestos farmacológicos
        return qed_value >= 0.40, round(qed_value, 3)

    def check_pains(self, mol):
        """Filtro 3: Identifica grupos químicos reactivos / interferentes indeseables (PAINS completo de RDKit)."""
        detected_pains = []
        if self.pains_catalog.HasMatch(mol):
            matches = self.pains_catalog.GetMatches(mol)
            detected_pains = [m.GetDescription() for m in matches]
        
        passed = len(detected_pains) == 0
        return passed, detected_pains

    def estimate_synthetic_accessibility(self, mol):
        """
        Filtro 4: Accesibilidad Sintética real usando el score de Ertl-Schuffenhauer (2009).
        Evalúa la sintetizabilidad combinando contribuciones de fragmentos y penalizaciones de complejidad.
        Score: 1 (Fácil de sintetizar) a 10 (Muy difícil / no sintetizable).
        """
        try:
            from rdkit.Contrib.SA_Score import sascorer
            sa_score = sascorer.calculateScore(mol)
            # Filtro: SA <= 4.5 es generalmente considerado sintetizable sin problemas críticos
            passed = sa_score <= 4.5
            return passed, round(sa_score, 2)
        except Exception as e:
            # Fallback heurístico en caso de que sascorer no esté accesible
            num_atoms = mol.GetNumAtoms()
            num_rings = mol.GetRingInfo().NumRings()
            num_chiral = len(Chem.FindMolChiralCenters(mol, includeUnassigned=True))
            complexity = (num_atoms * 0.1) + (num_rings * 0.5) + (num_chiral * 0.8)
            sa_score = 1.0 + min(complexity, 9.0)
            passed = sa_score <= 5.0
            return passed, round(sa_score, 2)

    def verify_smiles(self, smiles):
        """Ejecuta todo el embudo de verificación para una molécula SMILES."""
        # 1. Sanitización
        mol, status = self.sanitize_check(smiles)
        if mol is None:
            return {
                "SMILES": smiles,
                "Passed_All_Filters": False,
                "Reason": status,
                "Verdict": "DISCARDED_HALLUCINATION"
            }
            
        # 2. Lipinski
        passed_lipinski, lipinski_details = self.check_lipinski(mol)
        
        # 3. QED
        passed_qed, qed_score = self.check_qed_drogabilidad(mol)
        
        # 4. PAINS (Reactivos)
        passed_pains, reactive_groups = self.check_pains(mol)
        
        # 5. Accesibilidad Sintética
        passed_sa, sa_score = self.estimate_synthetic_accessibility(mol)
        
        # Veredicto general
        passed_all = passed_lipinski and passed_qed and passed_pains and passed_sa
        
        return {
            "SMILES": smiles,
            "Passed_All_Filters": passed_all,
            "QED": qed_score,
            "SAScore": sa_score,
            "Lipinski_Details": lipinski_details,
            "PAINS_Detected": reactive_groups,
            "Verdict": "VALIDATED" if passed_all else "DISCARDED_HALLUCINATION"
        }

if __name__ == "__main__":
    # Test rápido de validación con compuestos reales y alucinaciones obvias
    verifier = ChemicalVerifier()
    
    compuestos_test = {
        "Pramipexole (Real)": "CCCNC1CCc2nc(N)sc2CC1", # SMILES corregido y aromáticamente correcto
        "Pentavalent Carbon (Hallucination)": "C(C)(C)(C)(C)C", # Estructura con carbono sobrecargado
        "Reactive Epoxide (Toxic Hallucination)": "CC1OC1C(=O)Cl", # Reactivo (epóxido + cloruro de ácido)
    }
    
    print("=== INICIANDO VALIDACIÓN DE PRUEBA ===")
    for name, smiles in compuestos_test.items():
        print(f"\nProbando: {name} | SMILES: {smiles}")
        result = verifier.verify_smiles(smiles)
        print(f"-> Veredicto: {result['Verdict']}")
        if result['Verdict'] == "VALIDATED":
            print(f"   QED Score: {result['QED']} (Drogabilidad)")
            print(f"   SAScore: {result['SAScore']} (Accesibilidad)")
        else:
            print(f"   Motivo / Alucinación detectada: {result.get('Reason', 'Fallas en Filtros Biofísicos/PAINS')}")
            if result.get("PAINS_Detected"):
                print(f"   Grupos reactivos detectados: {result['PAINS_Detected']}")

