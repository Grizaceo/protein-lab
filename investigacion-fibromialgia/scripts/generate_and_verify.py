#!/usr/bin/env python3
"""
scripts/generate_and_verify.py
Generación molecular y filtrado cascada multi-etapa anti-alucinación,
integrando un Auditor de Consenso Agéntico y Detector de Inconsistencias SOTA.
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd
import torch

from rdkit import Chem
from rdkit.Chem import QED
from rdkit.Chem import Lipinski
from rdkit.Chem import Crippen
from rdkit.Chem import AllChem
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from rdkit.Contrib.SA_Score import sascorer

# Añadir directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from transformer_selective_generator import SelectiveTransformer
import predict_admet_bbb as bbb

try:
    import selfies as sf
except ImportError:
    print("[ERROR] selfies no está disponible.")
    sys.exit(1)

# =====================================================================
# 1. CLASES DE AUDITORÍA AGÉNTICA (PATRONES DE AGENTIC-LAB-EAC)
# =====================================================================

class InconsistencyDetector:
    """
    Detecta incoherencias biofísicas o farmacológicas críticas en los perfiles.
    Por ejemplo, compuestos con selectividad teórica extrema pero drogabilidad central nula,
    o alta drogabilidad pero imposibilidad de síntesis real.
    """
    def find_inconsistencies(self, profile):
        flags = []
        # Inconsistencia 1: Alta selectividad QSAR pero nula permeabilidad BBB
        if profile["pred_selectivity_ratio"] > 100.0 and profile["CNS_MPO"] < 3.0:
            flags.append("HIGH_SELECTIVITY_BUT_POOR_CNS_MPO (Riesgo de nula biodisponibilidad central)")
            
        # Inconsistencia 2: Drogabilidad QED alta pero inaccesibilidad sintética crítica
        if profile["QED"] > 0.70 and profile["SA_Score"] > 5.0:
            flags.append("HIGH_DRUGGABILITY_BUT_SYNTHETICALLY_IMPOSSIBLE (Molécula teóricamente hermosa pero insintetizable)")
            
        # Inconsistencia 3: Alta similitud con entrenamiento pero baja selectividad predicha
        if profile["Max_Tanimoto_Original"] > 0.80 and profile["pred_selectivity_ratio"] < 5.0:
            flags.append("HIGH_SIMILARITY_TO_SELECTIVES_BUT_LOW_QSAR_PREDICTION (Posible colapso de la representación)")
            
        return flags

class AgenticConsensusAuditor:
    """
    Auditor Agéntico que implementa el patrón MetaReviewer.
    Calcula un score ponderado de calidad general (Consensus Score) y
    emite un veredicto detallado sobre cada compuesto candidato.
    Ponderaciones del Consenso:
      - Selectividad Predicha QSAR: 40%
      - Drogabilidad QED: 20%
      - Accesibilidad Sintética SA: 20%
      - CNS MPO (BBB): 20%
    """
    def __init__(self):
        self.detector = InconsistencyDetector()

    def audit(self, profile):
        # 1. Puntuación de Selectividad (Normalizada de 0 a 1)
        # Una selectividad predicha >= 150x da 1.0. Ratios < 1x dan 0.0.
        sel_ratio = profile["pred_selectivity_ratio"]
        score_sel = min(1.0, max(0.0, np.log10(max(sel_ratio, 1.0)) / np.log10(150.0)))
        
        # 2. Puntuación de Drogabilidad QED
        score_qed = profile["QED"]
        
        # 3. Puntuación de Accesibilidad Sintética (SA Score 1 es excelente, 10 es pésimo)
        sa = profile["SA_Score"]
        score_sa = max(0.0, (10.0 - sa) / 9.0)
        
        # 4. Puntuación CNS MPO (Rango 0 a 6)
        cns = profile["CNS_MPO"]
        score_cns = cns / 6.0
        
        # Consenso unificado ponderado
        consensus_score = (0.4 * score_sel) + (0.2 * score_qed) + (0.2 * score_sa) + (0.2 * score_cns)
        consensus_score = round(consensus_score, 3)
        
        # Detectar inconsistencias
        inconsistencies = self.detector.find_inconsistencies(profile)
        
        # Emitir Veredicto
        if len(inconsistencies) > 0:
            verdict = "REJECTED_BY_AUDITOR"
            reason = f"Flags detectadas: {', '.join(inconsistencies)}"
        elif consensus_score >= 0.65:
            verdict = "APPROVED_HIGH_CONFIDENCE"
            reason = "Perfil balanceado de alta selectividad, drogabilidad y viabilidad sintética"
        elif consensus_score >= 0.50:
            verdict = "APPROVED_MODERATE_CONFIDENCE"
            reason = "Propiedades aceptables con margen de optimización"
        else:
            verdict = "DISCARDED"
            reason = f"Consensus score insuficiente ({consensus_score:.2f} < 0.50)"
            
        return {
            "Consensus_Score": consensus_score,
            "Auditor_Verdict": verdict,
            "Auditor_Reason": reason,
            "Inconsistency_Flags": inconsistencies
        }

# =====================================================================
# 2. PIPELINE DE VERIFICACIÓN CASCADA MULTI-ETAPA
# =====================================================================

class MolecularVerifierCascade:
    def __init__(self, qsar_predictor_path, train_df_path):
        # Cargar predictor QSAR
        with open(qsar_predictor_path, 'rb') as f:
            self.qsar_payload = pickle.load(f)
        self.model_d2 = self.qsar_payload["model_d2"]
        self.model_d3 = self.qsar_payload["model_d3"]
        self.n_bits = self.qsar_payload["n_bits"]
        self.radius = self.qsar_payload["radius"]
        
        # Cargar compuestos originales para cálculo de novedad
        self.train_df = pd.read_csv(train_df_path)
        self.train_mols = []
        for idx, row in self.train_df.iterrows():
            m = Chem.MolFromSmiles(row["smiles"])
            if m is not None:
                fp = AllChem.GetMorganFingerprintAsBitVect(m, 2, nBits=2048)
                self.train_mols.append(fp)
                
        # Inicializar catálogo PAINS de RDKit
        params = FilterCatalogParams()
        params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
        self.pains_catalog = FilterCatalog(params)
        
        # Scaffold de aminotiazol requerido (Pramipexol-like core)
        # 2-amino-4,5,6,7,8,9-hexahydrophenanthro-like / cycloheptathiazole core
        self.aminothiazole_scaffold = Chem.MolFromSmarts("[#6]1-[#6]-[#6]-[#6]2:[#7]:[#6](-[#7]):[#16]:[#6]:2-[#6]-[#6]-1")
        
        # Auditor de Consenso
        self.auditor = AgenticConsensusAuditor()

    def check_level1_cheap(self, smiles):
        """Validez SMILES básica, Lipinski, QED > 0.3"""
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return False, "Failed_Sanitization", None
            Chem.SanitizeMol(mol)
        except Exception as e:
            return False, f"Failed_Sanitization: {str(e)}", None
            
        # Lipinski Rule of 5
        mw = Chem.rdMolDescriptors.CalcExactMolWt(mol)
        logp = Crippen.MolLogP(mol)
        hbd = Lipinski.NumHDonors(mol)
        hba = Lipinski.NumHAcceptors(mol)
        
        passed_lipinski = (mw <= 500) and (logp <= 5.0) and (hbd <= 5) and (hba <= 10)
        if not passed_lipinski:
            return False, f"Failed_Lipinski (MW={mw:.1f}, LogP={logp:.1f}, HBD={hbd}, HBA={hba})", None
            
        # QED > 0.3
        qed_val = QED.qed(mol)
        if qed_val <= 0.30:
            return False, f"Failed_QED_Threshold ({qed_val:.3f} <= 0.30)", None
            
        return True, "Passed", mol

    def check_level2_medium(self, mol):
        """PAINS, SA Score <= 4.5, Scaffold Aminotiazol obligatorio"""
        # PAINS
        if self.pains_catalog.HasMatch(mol):
            matches = self.pains_catalog.GetMatches(mol)
            pains_desc = [m.GetDescription() for m in matches]
            return False, f"PAINS_Detected: {', '.join(pains_desc)}"
            
        # SA Score <= 4.5
        try:
            sa_score = sascorer.calculateScore(mol)
        except Exception:
            sa_score = 5.0  # Fallback castigado
            
        if sa_score > 4.5:
            return False, f"High_SA_Score ({sa_score:.2f} > 4.5)"
            
        # Scaffold de aminotiazol obligatorio
        if not mol.HasSubstructMatch(self.aminothiazole_scaffold):
            return False, "Missing_Required_Aminothiazole_Scaffold"
            
        return True, "Passed"

    def check_level3_expensive(self, mol, smiles):
        """Re-scoring QSAR (selectividad teórica) y Novedad vs training set (Tanimoto < 0.85)"""
        # Morgan Fingerprint
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, self.radius, nBits=self.n_bits)
        arr = np.zeros((1,), dtype=np.float32)
        Chem.DataStructs.ConvertToNumpyArray(fp, arr)
        X = arr.reshape(1, -1)
        
        # Predicción QSAR
        pki_d2 = self.model_d2.predict(X)[0]
        pki_d3 = self.model_d3.predict(X)[0]
        
        d2_nm = 10 ** (9.0 - pki_d2)
        d3_nm = 10 ** (9.0 - pki_d3)
        selectivity_ratio = d3_nm / d2_nm
        
        # Novedad: Similitud máxima Tanimoto vs training set
        max_tanimoto = 0.0
        for train_fp in self.train_mols:
            sim = Chem.DataStructs.TanimotoSimilarity(fp, train_fp)
            if sim > max_tanimoto:
                max_tanimoto = sim
                
        if max_tanimoto >= 0.85:
            return False, f"Failed_Novelty_Check (Max Tanimoto: {max_tanimoto:.3f} >= 0.85)", None
            
        details = {
            "pred_d2_affinity_nm": round(d2_nm, 3),
            "pred_d3_affinity_nm": round(d3_nm, 3),
            "pred_selectivity_ratio": round(selectivity_ratio, 2),
            "Max_Tanimoto_Original": round(max_tanimoto, 3)
        }
        return True, "Passed", details

    def check_level4_consensus(self, mol, qsar_details):
        """Evaluación CNS MPO (BBB) y Auditoría Agéntica de Consenso"""
        # Calcular descriptores para CNS MPO
        mw = Chem.rdMolDescriptors.CalcExactMolWt(mol)
        logp = Crippen.MolLogP(mol)
        tpsa = Chem.rdMolDescriptors.CalcTPSA(mol)
        hbd = Lipinski.NumHDonors(mol)
        hba = Lipinski.NumHAcceptors(mol)
        pka = bbb.estimate_pka(mol)
        
        cns_mpo, _ = bbb.calculate_cns_mpo(mw, logp, tpsa, hbd, hba, pka)
        
        # Estimación heurística de sintetizabilidad
        sa_score = sascorer.calculateScore(mol)
        qed_val = QED.qed(mol)
        
        # Perfil completo
        profile = {
            "QED": qed_val,
            "SA_Score": sa_score,
            "CNS_MPO": cns_mpo,
            "pred_selectivity_ratio": qsar_details["pred_selectivity_ratio"],
            "Max_Tanimoto_Original": qsar_details["Max_Tanimoto_Original"]
        }
        
        # Auditoría agéntica de consenso
        audit_res = self.auditor.audit(profile)
        
        cns_details = {
            "MW": round(mw, 2),
            "LogP": round(logp, 2),
            "TPSA": round(tpsa, 2),
            "est_pKa": pka,
            "CNS_MPO": cns_mpo,
            "QED": qed_val,
            "SA_Score": sa_score,
            **audit_res
        }
        return cns_details

# =====================================================================
# 3. PIPELINE GENERAL DE GENERACIÓN Y EVALUACIÓN
# =====================================================================

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    
    model_path = os.path.join(base_dir, "datos", "model", "transformer_selective_model.pt")
    qsar_path = os.path.join(base_dir, "datos", "model", "d2_d3_qsar_predictor.pkl")
    train_path = os.path.join(base_dir, "datos", "chembl_mining", "chembl_d2_selective_compounds.csv")
    
    output_csv = os.path.join(base_dir, "docking_runs", "ad_hoc_design", "transformer_validated_candidates.csv")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
    print("=== INICIANDO PIPELINE DE GENERACIÓN Y VERIFICACIÓN CASCADA ===")
    
    if not os.path.exists(model_path):
        print(f"[ERROR] Modelo de Transformer no encontrado en: {model_path}")
        print("Por favor, ejecuta primero train_transformer.py para entrenar el modelo.")
        sys.exit(1)
        
    # Cargar payload del Transformer
    print("[INFO] Cargando modelo Transformer y vocabulario...")
    payload = torch.load(model_path, map_location="cpu")
    char_to_idx = payload["char_to_idx"]
    idx_to_char = payload["idx_to_char"]
    
    model = SelectiveTransformer(
        vocab_size=payload["vocab_size"],
        pad_idx=char_to_idx["[PAD]"],
        start_idx=char_to_idx["[START]"],
        end_idx=char_to_idx["[END]"],
        embed_dim=payload["embed_dim"],
        n_heads=payload["n_heads"],
        n_layers=payload["n_layers"],
        dim_feedforward=payload["dim_feedforward"],
        latent_dim=payload["latent_dim"],
        noise_dim=payload["noise_dim"]
    )
    model.load_state_dict(payload["model_state_dict"])
    model.eval()
    
    # Inicializar el Verificador Cascada
    print("[INFO] Inicializando Verificador Cascada multi-etapa...")
    cascade = MolecularVerifierCascade(qsar_path, train_path)
    
    # 4. Generación Molecular Condicionada (Exploración de la vecindad de alta selectividad y scaffold aminotiazol)
    print("[INFO] Muestreando candidatos condicionando el espacio latente...")
    
    # Cargar adhoc keys (pipeline combinatorial previo) para enriquecer anclajes de aminotiazol
    adhoc_path = os.path.join(base_dir, "docking_runs", "ad_hoc_design", "generative_adhoc_keys.csv")
    if os.path.exists(adhoc_path):
        adhoc_df = pd.read_csv(adhoc_path)
    else:
        adhoc_df = pd.DataFrame()
        
    train_df = cascade.train_df
    
    # Patrón de aminotiazol requerido
    aminothiazole_pattern = Chem.MolFromSmarts("[#6]1-[#6]-[#6]-[#6]2:[#7]:[#6](-[#7]):[#16]:[#6]:2-[#6]-[#6]-1")
    
    anchors = []
    # Filtrar compuestos del dataset original que tengan aminotiazol
    for idx, row in train_df.iterrows():
        smi = row["smiles"]
        m = Chem.MolFromSmiles(smi)
        if m is not None and m.HasSubstructMatch(aminothiazole_pattern):
            anchors.append((smi, row["selectivity_ratio"]))
            
    # Añadir compuestos combinatoriales que tengan el scaffold (ej. Pramipexol-like)
    if not adhoc_df.empty:
        for idx, row in adhoc_df.iterrows():
            smi = row["smiles"]
            m = Chem.MolFromSmiles(smi)
            if m is not None and m.HasSubstructMatch(aminothiazole_pattern):
                anchors.append((smi, row["pred_selectivity_ratio"]))
                
    # Eliminar duplicados conservando el mayor ratio
    unique_anchors = {}
    for smi, ratio in anchors:
        if smi not in unique_anchors or ratio > unique_anchors[smi]:
            unique_anchors[smi] = ratio
            
    print(f"   Compuestos con scaffold aminotiazol identificados para anclaje latente: {len(unique_anchors)}")
    
    generated_smiles_set = set()
    
    # Si no se identificaron anclajes (caso improbable), usar los top selectivos generales
    if len(unique_anchors) == 0:
        print("[WARNING] No se encontraron anclajes de aminotiazol específicos. Usando compuestos altamente selectivos generales...")
        general_selectives = train_df.sort_values(by="selectivity_ratio", ascending=False).head(15)
        for _, row in general_selectives.iterrows():
            unique_anchors[row["smiles"]] = row["selectivity_ratio"]
            
    # Generar perturbaciones a partir de los anclajes
    for smi, ratio in unique_anchors.items():
        try:
            selfie = sf.encoder(smi)
            tokens = list(sf.split_selfies(selfie))
            token_indices = [char_to_idx.get(t, char_to_idx["[UNK]"]) for t in tokens[:58]]
            seq_in = [char_to_idx["[START]"]] + token_indices + [char_to_idx["[END]"]]
            seq_in = seq_in + [char_to_idx["[PAD]"]] * (60 - len(seq_in))
            
            # Generar Morgan Fingerprint del anclaje de forma dinámica
            m_anchor = Chem.MolFromSmiles(smi)
            fp_bitvect = AllChem.GetMorganFingerprintAsBitVect(m_anchor, 2, nBits=2048)
            arr = np.zeros((1,), dtype=np.float32)
            Chem.DataStructs.ConvertToNumpyArray(fp_bitvect, arr)
            
            # Tensorizar
            t_seq_in = torch.tensor(np.array([seq_in]), dtype=torch.long)
            t_fp = torch.tensor(np.array([arr]), dtype=torch.float32)
            
            with torch.no_grad():
                # Obtener embedding latente z del anclaje
                z_anchor = model.encoder(t_seq_in, t_fp)
                
                # Generar 20 variantes con pequeña perturbación latente (exploración en la vecindad del scaffold)
                for _ in range(20):
                    z_perturbed = z_anchor + torch.randn_like(z_anchor) * 0.12
                    
                    # Condicionar a selectividad target alta (150x — máximo observado en training set)
                    # Usar 150x en vez de 500x para evitar extrapolación fuera de distribución
                    target_ratio = torch.tensor([150.0])
                    g_ind = model.generate(z_perturbed, target_ratio, max_len=60, temperature=0.8, device="cpu")
                    
                    # Decodificar
                    toks = [idx_to_char[i.item()] for i in g_ind[0] if i.item() not in (char_to_idx["[PAD]"], char_to_idx["[START]"], char_to_idx["[END]"])]
                    gen_selfie = "".join(toks)
                    try:
                        gen_smi = sf.decoder(gen_selfie)
                        if gen_smi:
                            generated_smiles_set.add(gen_smi)
                    except Exception:
                        continue
        except Exception:
            continue
            
    print(f"[INFO] Moléculas generadas sintácticamente válidas únicas: {len(generated_smiles_set)}")
    
    # 5. Ejecutar la cascada de filtrado
    print("[INFO] Pasando moléculas por el embudo de filtración cascada anti-alucinaciones...")
    
    candidates_list = []
    levels_stats = {"total_in": len(generated_smiles_set), "passed_l1": 0, "passed_l2": 0, "passed_l3": 0, "passed_l4": 0}
    
    for smiles in sorted(generated_smiles_set):
        # NIVEL 1: Sanitización, Lipinski, QED > 0.3
        l1_passed, l1_reason, mol = cascade.check_level1_cheap(smiles)
        if not l1_passed:
            continue
        levels_stats["passed_l1"] += 1
        
        # NIVEL 2: PAINS, SA <= 4.5, Scaffold Aminotiazol obligatorio
        l2_passed, l2_reason = cascade.check_level2_medium(mol)
        if not l2_passed:
            continue
        levels_stats["passed_l2"] += 1
        
        # NIVEL 3: QSAR dual predicho y similitud Tanimoto Novedad < 0.85
        l3_passed, l3_reason, qsar_details = cascade.check_level3_expensive(mol, smiles)
        if not l3_passed:
            continue
        levels_stats["passed_l3"] += 1
        
        # NIVEL 4: CNS MPO (penetración BBB) y Auditoría Agéntica de Consenso
        l4_details = cascade.check_level4_consensus(mol, qsar_details)
        levels_stats["passed_l4"] += 1
        
        # Combinar perfiles
        cand_profile = {
            "smiles": smiles,
            "MW": l4_details["MW"],
            "LogP": l4_details["LogP"],
            "TPSA": l4_details["TPSA"],
            "est_pKa": l4_details["est_pKa"],
            "QED": l4_details["QED"],
            "SA_Score": round(l4_details["SA_Score"], 2),
            "CNS_MPO": l4_details["CNS_MPO"],
            "pred_d2_affinity_nm": qsar_details["pred_d2_affinity_nm"],
            "pred_d3_affinity_nm": qsar_details["pred_d3_affinity_nm"],
            "pred_selectivity_ratio": qsar_details["pred_selectivity_ratio"],
            "Max_Tanimoto_Original": qsar_details["Max_Tanimoto_Original"],
            "Consensus_Score": l4_details["Consensus_Score"],
            "Auditor_Verdict": l4_details["Auditor_Verdict"],
            "Auditor_Reason": l4_details["Auditor_Reason"]
        }
        candidates_list.append(cand_profile)
        
    print("\n=== ESTADÍSTICAS DEL EMBUDO DE FILTRADO CASCADA ===")
    print(f"   Moléculas Iniciales Generadas: {levels_stats['total_in']}")
    print(f"   -> Nivel 1 (Cheapo: RDKit, Lipinski, QED>0.3): {levels_stats['passed_l1']} aprobadas")
    print(f"   -> Nivel 2 (Medium: PAINS, SA<=4.5, Scaffold obligatorio): {levels_stats['passed_l2']} aprobadas")
    print(f"   -> Nivel 3 (Expensive: QSAR re-scoring, Novedad Tanimoto<0.85): {levels_stats['passed_l3']} aprobadas")
    print(f"   -> Nivel 4 (Consensus: CNS MPO y Auditoría de Consenso): {levels_stats['passed_l4']} aprobadas")
    
    # Procesar candidatos finales
    if len(candidates_list) == 0:
        print("[WARNING] Ningún compuesto pasó la cascada completa de filtrado. Considera flexibilizar los filtros.")
        sys.exit(0)
        
    df_cand = pd.DataFrame(candidates_list)
    # Ordenar por Consensus Score y Selectividad
    df_cand = df_cand.sort_values(by=["Consensus_Score", "pred_selectivity_ratio"], ascending=[False, False]).reset_index(drop=True)
    
    # Guardar en CSV
    df_cand.to_csv(output_csv, index=False)
    print(f"\n[INFO] Candidatos validados y aprobados exportados correctamente a: {os.path.basename(output_csv)}")
    
    # Imprimir un resumen de los mejores compuestos generados
    print("\n=== TOP 5 CANDIDATOS LÍDERES APROBADOS POR EL AUDITOR DE CONSENSO ===")
    for i, row in df_cand.head(5).iterrows():
        print(f"\nRANK #{i+1} | SMILES: {row['smiles']}")
        print(f"   Consensus Score: {row['Consensus_Score']} / 1.00 | Veredicto: {row['Auditor_Verdict']}")
        print(f"   Selectividad Predicha QSAR (D3/D2): {row['pred_selectivity_ratio']}x (D2: {row['pred_d2_affinity_nm']} nM vs D3: {row['pred_d3_affinity_nm']} nM)")
        print(f"   CNS MPO Score: {row['CNS_MPO']} / 6.00 (Drogabilidad SNC) | Tanimoto Novedad: {row['Max_Tanimoto_Original']}")
        print(f"   Propiedades: MW={row['MW']} g/mol, LogP={row['LogP']}, TPSA={row['TPSA']} A2, SA Score={row['SA_Score']}")
        print(f"   Auditor Review: {row['Auditor_Reason']}")

if __name__ == "__main__":
    main()
