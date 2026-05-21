import json
import yaml
import pathlib
from agentic_lab_eac.models import Hypothesis, EvidenceRef, HypothesisStatus
from agentic_lab_eac.eac import load_lab_config, lab_state_from_config

BASE_DIR = pathlib.Path(__file__).resolve().parent

def load_protein_lab():
    """Loads the protein lab configuration and state from agentic-lab-eac."""
    eac_lab_yaml = pathlib.Path("/home/gris/.hermes/workspace/agentic-lab-eac/examples/labs/protein_lab.yaml")
    if not eac_lab_yaml.exists():
        eac_lab_yaml = BASE_DIR.parent.parent / "agentic-lab-eac" / "examples" / "labs" / "protein_lab.yaml"
    
    with open(eac_lab_yaml, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
        
    config = load_lab_config(config_data)
    state = lab_state_from_config(config)
    return config, state

# Formalize the DRD2 Dopaminergic Pathway Hypothesis in FM
DRD2_HYPOTHESIS = Hypothesis(
    id="fm-drd2-v1",
    statement="DRD2 dopaminergic pathway is pathophysiologically relevant in FM",
    rationale="GWAS 2.5M (Kerrebijn 2025), neuroendocrine challenge (Malt 2003), RCT pramipexole (Holman 2005)",
    novelty_claim="First multi-evidence convergence analysis linking GWAS DRD2 signal to FM transcriptomics",
    test_strategy="Sensitivity analysis of GWAS-prioritized neural genes in GSE221921 PBMCs",
    evidence=[
        EvidenceRef("PMID:41001472", "Kerrebijn 2025 FM GWAS 2.5M", "https://pubmed.ncbi.nlm.nih.gov/41001472/"),
        EvidenceRef("PMID:16052595", "Holman 2005 pramipexole RCT", "https://pubmed.ncbi.nlm.nih.gov/16052595/"),
        EvidenceRef("PMID:12781354", "Malt 2003 buspirone challenge", "https://pubmed.ncbi.nlm.nih.gov/12781354/"),
    ],
    score=0.92,
    status=HypothesisStatus.GENERATED
)

def save_hypothesis():
    """Saves the formalized hypothesis to the hypotheses directory."""
    hypotheses_dir = BASE_DIR / "hypotheses"
    hypotheses_dir.mkdir(exist_ok=True)
    
    out_file = hypotheses_dir / "fm_drd2_hypothesis.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(DRD2_HYPOTHESIS.to_dict(), f, indent=2)
    print(f"✓ Hypothesis successfully serialized and saved to {out_file}")

if __name__ == "__main__":
    save_hypothesis()
    try:
        config, state = load_protein_lab()
        print(f"✓ Lab config loaded: {config.name} (id={config.id})")
        print(f"✓ Lab state resources: {[r.name for r in state.resources]}")
    except Exception as e:
        print(f"Error loading lab config: {e}")
