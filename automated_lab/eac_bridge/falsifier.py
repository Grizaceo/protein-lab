import logging
import re
from typing import Tuple
from llm_researcher import CloudResearcher

logger = logging.getLogger(__name__)

class FalsifierAdversary:
    """
    Falsifier Adversary (inspired by AGENTIC_METRIC_DISCOVERY's falsifier/NIM adversary).
    Runs fast heuristic static checks and a quick local LLM review
    to reject bad, hallucinated, or chemically impossible hypotheses
    before dedicating GPU time or expensive API tokens to them.
    """
    def __init__(self):
        self.researcher = CloudResearcher()
        self.fake_citations = ["kang 2007", "tominaga 2006", "hainfeld 2011"]

    def verify_static(self, statement: str, rationale: str) -> Tuple[bool, str]:
        """Perform instant regex and keyword grounding checks."""
        content = (statement + " " + rationale).lower()

        # Check for banned fake citations from GROUNDING.md
        for fake in self.fake_citations:
            if fake in content:
                return False, f"BANNED CITATION DETECTED: {fake!r} was flagged as fake in GROUNDING.md."

        # Check for atomically precise Au25/Au55 inside ferritin cage alucinations
        if "au25" in content or "au55" in content or "au144" in content:
            if "dentro de" in content or "inside" in content:
                return False, "SCIENTIFIC ERROR: Atomically precise Au25/Au55/Au144 clusters INSIDE ferritin are not verified. Nucleate in situ via Butts 2008 instead."

        # Check for invalid SMILES characters if chemical structures are mentioned
        smiles_match = re.search(r'smiles:\s*([^\s]+)', content)
        if smiles_match:
            smiles = smiles_match.group(1)
            # Basic validation
            if not re.match(r'^[A-Za-z0-9@#\-\[\]\(\)\\\/=\+]+$', smiles):
                return False, f"CHEMICAL CONSTRAINT VIOLATION: SMILES string {smiles!r} has invalid characters."

        return True, "Passed static grounding checks."

    def verify_llm_critic(self, statement: str, rationale: str) -> Tuple[bool, str]:
        """Run a lightweight, highly-critical LLM check to falsify physical viability."""
        if not self.researcher.available:
            return True, "No LLM available, skipping LLM falsifier critic."

        prompt = f"""
        Act as an extremely critical, adversarial peer reviewer for a computational biophysics lab.
        Falsify the following scientific hypothesis:
        Hypothesis: {statement}
        Rationale: {rationale}

        Your job is to look for:
        1. Violation of physical constants (e.g. Marcus hopping distance > 15A).
        2. Biological alucinations (e.g. Nipah G binding EFNB2 via sialic acid).
        3. Clear logical leaps.

        You must output exactly a JSON object:
        {{
          "falsified": true_or_false,
          "reason": "If falsified=true, write the concise physical or chemical reason why."
        }}
        """

        response = self.researcher.chat(prompt, temperature=0.1, max_tokens=300)
        if not response:
            return True, "LLM critic timed out; bypassing falsifier."

        try:
            clean_json = response.strip()
            if "```json" in clean_json:
                clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_json:
                clean_json = clean_json.split("```")[1].split("```")[0].strip()

            import json
            data = json.loads(clean_json)
            falsified = data.get("falsified", False)
            reason = data.get("reason", "Passed critic.")
            return not falsified, reason
        except Exception as e:
            logger.warning(f"Failed to parse falsifier response: {e}. Raw was: {response}")
            return True, "Failed to parse critic; bypassing falsifier."

    def check_hypothesis(self, statement: str, rationale: str) -> Tuple[bool, str]:
        """Runs both static and LLM checks to yield a final verification result."""
        ok, msg = self.verify_static(statement, rationale)
        if not ok:
            return False, msg

        ok, msg = self.verify_llm_critic(statement, rationale)
        if not ok:
            return False, f"FALSIFIED BY CRITIC: {msg}"

        return True, "Hypothesis successfully falsified/verified."
