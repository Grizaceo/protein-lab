import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

# Ensure agentic-lab-eac src directory is in sys.path
EAC_SRC = Path("/home/gris/.hermes/workspace/agentic-lab-eac/src")
if EAC_SRC.exists() and str(EAC_SRC) not in sys.path:
    sys.path.insert(0, str(EAC_SRC))

from agentic_lab_eac.models import (
    Hypothesis,
    EvidenceRef,
    Review,
    ReviewBatch,
    HypothesisStatus,
    LabConfig
)

from llm_researcher import CloudResearcher

logger = logging.getLogger(__name__)

class LLMReasoningBridge:
    """
    LLM reasoning plane bridge that implements the four core Co-Scientist ports.
    Delegates to the custom CloudResearcher curls and uses specialized prompts
    for drug-target binding affinity (DTI) and biophysics.
    """
    def __init__(self):
        self.researcher = CloudResearcher()
        if not self.researcher.available:
            logger.warning("CloudResearcher is NOT available. Falling back to mock reasoning.")

    def generate(self, goal: str, lab: LabConfig, prior_evidence: List[Dict]) -> List[Hypothesis]:
        if not self.researcher.available:
            return self._mock_generate(goal, lab)

        evidence_str = json.dumps(prior_evidence, indent=2)
        system_prompt = (
            "You are a Senior Computational Biophysicist Swarm specializing in protein engineering and DTI. "
            "Your swarm includes:\n"
            "- GeometryAgent (structural coordinates & longitudes)\n"
            "- SpectralAgent (electrochemistry & eigen-gaps)\n"
            "- MacroStrategist (design regime constraints)\n"
            "Return a strictly valid JSON list of 3 high-probability hypotheses. Do not include markdown wrappers except the JSON itself."
        )

        prompt = f"""
        Objective / Goal: {goal}
        Domain: {lab.domain}
        Available Capabilities: {lab.capabilities}
        Grounding Evidence:
        {evidence_str}

        Propose 3 promising drug-target or protein engineering hypotheses.
        You must return a raw JSON list. Each object in the list MUST exactly have the following keys:
        - "id": A unique identifier string (e.g. "hyp-001", "hyp-002", ...)
        - "statement": A clear, concise hypothesis statement.
        - "rationale": The scientific mechanism (Marcus theory, Ihara zeta metric, or DTI docking).
        - "novelty_claim": What makes this hypothesis unique and not a known hallucination.
        - "test_strategy": How to test it computationally (e.g. 'dti.predict' using MAMMAL local, followed by 'structure.fold' via Colab).

        Example Format:
        [
          {{
            "id": "hyp-01",
            "statement": "Naltrexone binds EFNB2 with higher affinity than standard antagonists by forming a salt bridge with Leu40.",
            "rationale": " Leu40 is situated in a high-density rotamer pocket which can form direct ionic interaction...",
            "novelty_claim": "First model of Naltrexone interface conditioning on EFNB2 beta-strand.",
            "test_strategy": "Run DTI prediction on MAMMAL local, then run AlphaFold2 fold on Colab to analyze Leu40 rotamers."
          }}
        ]
        """
        
        response = self.researcher.chat(prompt, system=system_prompt, temperature=0.3)
        if not response:
            logger.warning("Hypothesis generation LLM call returned empty. Falling back to mocks.")
            return self._mock_generate(goal, lab)

        try:
            # Clean response from potential markdown formatting
            clean_json = response.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0].strip()

            parsed = json.loads(clean_json)
            hyps = []
            for item in parsed:
                hyps.append(Hypothesis(
                    id=item["id"],
                    statement=item["statement"],
                    rationale=item["rationale"],
                    novelty_claim=item["novelty_claim"],
                    test_strategy=item["test_strategy"],
                    evidence=[EvidenceRef(source_id=r.get("id", "grounding"), title=r.get("title", "Evidence")) for r in prior_evidence[:2]],
                    status=HypothesisStatus.GENERATED,
                    score=0.0,
                    metadata={"source": "llm_bridge"}
                ))
            return hyps
        except Exception as e:
            logger.error(f"Failed to parse LLM generated hypotheses: {e}. Output was: {response}")
            return self._mock_generate(goal, lab)

    def review(self, hypotheses: List[Hypothesis], lab: LabConfig) -> ReviewBatch:
        if not self.researcher.available:
            return self._mock_review(hypotheses)

        reviews = []
        for h in hypotheses:
            prompt = f"""
            Review the following biophysics hypothesis for safety, novelty, and computational feasibility:
            Statement: {h.statement}
            Rationale: {h.rationale}
            Novelty: {h.novelty_claim}
            Test Strategy: {h.test_strategy}

            You must return a raw JSON object with exactly the following keys:
            - "strengths": List of strings listing the mathematical or structural strengths.
            - "weaknesses": List of strings listing weak points (e.g. VRAM constraints, low resolution).
            - "risks": List of safety or cost risks.
            - "novelty_score": A float between 0.0 and 1.0.
            - "feasibility_score": A float between 0.0 and 1.0.
            - "evidence_score": A float between 0.0 and 1.0.
            - "overall_score": A float between 0.0 and 1.0.
            - "verdict": A single string: "PASS" or "REJECT".

            Do not wrap your output in anything other than the raw JSON object.
            """
            
            response = self.researcher.chat(prompt, temperature=0.1)
            if not response:
                logger.warning(f"Failed to get review for {h.id}, using default review.")
                reviews.append(self._default_review(h.id))
                continue

            try:
                clean_json = response.strip()
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].split("```")[0].strip()

                item = json.loads(clean_json)
                reviews.append(Review(
                    hypothesis_id=h.id,
                    reviewer="LLMReasoningBridge",
                    strengths=item.get("strengths", []),
                    weaknesses=item.get("weaknesses", []),
                    risks=item.get("risks", []),
                    novelty_score=float(item.get("novelty_score", 0.5)),
                    feasibility_score=float(item.get("feasibility_score", 0.5)),
                    evidence_score=float(item.get("evidence_score", 0.5)),
                    overall_score=float(item.get("overall_score", 0.5)),
                    verdict=item.get("verdict", "PASS")
                ))
            except Exception as e:
                logger.error(f"Failed to parse review for {h.id}: {e}")
                reviews.append(self._default_review(h.id))

        return ReviewBatch(reviews=reviews, meta_summary="Batched biophysical peer-review completed.")

    def rank(self, hypotheses: List[Hypothesis], reviews: List[Review]) -> List[Hypothesis]:
        # Associate reviews to update the score on the hypotheses
        review_map = {r.hypothesis_id: r for r in reviews}
        for h in hypotheses:
            rev = review_map.get(h.id)
            if rev:
                h.score = rev.overall_score
                h.status = HypothesisStatus.RANKED if rev.verdict == "PASS" else HypothesisStatus.REJECTED
        
        # Sort by score descending
        ranked_hyps = [h for h in hypotheses if h.status != HypothesisStatus.REJECTED]
        ranked_hyps.sort(key=lambda x: x.score, reverse=True)
        return ranked_hyps

    def evolve(self, ranked: List[Hypothesis], reviews: List[Review], lab: LabConfig) -> List[Hypothesis]:
        if not self.researcher.available or not ranked:
            return ranked

        review_map = {r.hypothesis_id: r for r in reviews}
        evolved_hyps = []

        for h in ranked[:2]: # Evolve top 2
            rev = review_map.get(h.id)
            weaknesses_str = ", ".join(rev.weaknesses) if rev else "None"
            
            prompt = f"""
            Evolve and refine the following hypothesis by addressing its listed biophysical weaknesses.
            Hypothesis: {h.statement}
            Rationale: {h.rationale}
            Weaknesses: {weaknesses_str}

            You must return a raw JSON object with the evolved statement:
            - "statement": Refined hypothesis addressing the weaknesses.
            - "rationale": Refined biophysical rationale.

            Do not wrap your output in anything other than raw JSON.
            """
            
            response = self.researcher.chat(prompt, temperature=0.4)
            if not response:
                evolved_hyps.append(h)
                continue

            try:
                clean_json = response.strip()
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].split("```")[0].strip()

                item = json.loads(clean_json)
                evolved_hyps.append(Hypothesis(
                    id=f"{h.id}-evolved",
                    statement=item["statement"],
                    rationale=item["rationale"],
                    novelty_claim=h.novelty_claim,
                    test_strategy=h.test_strategy,
                    evidence=h.evidence,
                    status=HypothesisStatus.EVOLVED,
                    score=h.score,
                    metadata={"source": "llm_bridge_evolve", "ancestor": h.id}
                ))
            except Exception as e:
                logger.error(f"Failed to parse evolved hypothesis: {e}")
                evolved_hyps.append(h)

        return evolved_hyps

    # --- Mocks for offline testing ---
    def _mock_generate(self, goal: str, lab: LabConfig) -> List[Hypothesis]:
        logger.info("Generating mock hypotheses...")
        g_clean = goal.lower()
        if "fibromialgia" in g_clean or "fibromyalgia" in g_clean or "ruta_b" in g_clean:
            return [
                Hypothesis(
                    id="hyp-mock-01",
                    statement="Naltrexone binds OPRM1 (MOR) with a high predicted affinity of pKd=7.2, but exhibits a similar inflated binding score across other non-related GPCR Class A receptors (ADRB2, DRD2, AGTR1) due to structural embedding training bias in MAMMAL.",
                    rationale="Class A GPCRs share a conserved 7TM helical bundle and transmembrane pocket topology. DTI models like MAMMAL often over-generalize pocket representations, leading to shared inflated predictions rather than receptor-specific pharmacology.",
                    novelty_claim="First systematic GPCR fold-specific training bias calibration using a control panel under EaC.",
                    test_strategy="Predict binding affinity on MOR and ADRB2 via MAMMAL local, perform sequence alignment, and check literature preprints.",
                    evidence=[],
                    status=HypothesisStatus.GENERATED,
                    score=0.0
                ),
                Hypothesis(
                    id="hyp-mock-02",
                    statement="Atorvastatin (negative control) exhibits an unexpectedly high predicted binding affinity (pKd > 7.1) for OPRM1 and other GPCR Class A receptors in MAMMAL local DTI, indicating a hydrophobic embedding bias.",
                    rationale="Atorvastatin is highly lipophilic. MAMMAL DTI's latent space representation of GPCR pocket embeddings overweights hydrophobic contact terms, artificially inflating pKd values for lipophilic compounds regardless of biological target relevance.",
                    novelty_claim="A systematic negative control profiling to expose hydrophobic bias in deep DTI models.",
                    test_strategy="Predict binding of Atorvastatin on ADRB2, query experimental affinity database, and perform literature search.",
                    evidence=[],
                    status=HypothesisStatus.GENERATED,
                    score=0.0
                ),
                Hypothesis(
                    id="hyp-mock-03",
                    statement="Inert non-GPCR targets like GFP and ALB exhibit low predicted binding affinities (pKd < 5.0) for naltrexone and atorvastatin, confirming that MAMMAL DTI's inflation bias is specific to the GPCR fold.",
                    rationale="GFP (beta-barrel) and ALB (soluble carrier) lack the 7TM pocket topology. Comparing their predictions against GPCRs isolates structural bias from general pocket size/hydrophobicity factors.",
                    novelty_claim="Inert beta-barrel fold control validation for machine learning bias isolation.",
                    test_strategy="Predict binding on GFP via MAMMAL local, query experimental affinity database, and perform Needleman-Wunsch sequence alignment.",
                    evidence=[],
                    status=HypothesisStatus.GENERATED,
                    score=0.0
                )
            ]
        return [
            Hypothesis(
                id="hyp-mock-01",
                statement="Gold clusters stabilized by cysteines form a highly active redox synapse with apo-ferritin ferroxidase centers.",
                rationale="The 96 cysteines inside modified ferritin cages allow sub-nanometer gold nucleations, improving the local Marcus hopping coefficient by 1.4 nm^-1.",
                novelty_claim="First Ihara zeta topological audit of ferritin-gold bio-synapses.",
                test_strategy="Run topological audit 'topology.audit' to measure Ihara Zeta, then MAMMAL local DTI.",
                evidence=[],
                status=HypothesisStatus.GENERATED,
                score=0.0
            ),
            Hypothesis(
                id="hyp-mock-02",
                statement="Naltrexone blocks Ephrin-B2 binding on Nipah G glycoprotein by sterically hindering the hydrophobic residue Phe120.",
                rationale="Bowden 2008 shows Phe120 is critical for Ephrin-B2 binding; Naltrexone docking blocks this pocket.",
                novelty_claim="Targeting Bowden's 2008 receptor-binding hotspots with naltrexone analogs.",
                test_strategy="Run DTI prediction 'dti.predict' via MAMMAL local.",
                evidence=[],
                status=HypothesisStatus.GENERATED,
                score=0.0
            )
        ]

    def _mock_review(self, hypotheses: List[Hypothesis]) -> ReviewBatch:
        reviews = [self._default_review(h.id) for h in hypotheses]
        return ReviewBatch(reviews=reviews, meta_summary="Offline mock peer-review completed.")

    def _default_review(self, hyp_id: str) -> Review:
        return Review(
            hypothesis_id=hyp_id,
            reviewer="LLMReasoningBridgeMock",
            strengths=["Clear biophysical mechanism", "Feasible local computation"],
            weaknesses=["Lacks clinical validation"],
            risks=["GPU time budget risk"],
            novelty_score=0.7,
            feasibility_score=0.8,
            evidence_score=0.6,
            overall_score=0.7,
            verdict="PASS"
        )
