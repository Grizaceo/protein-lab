import sys
import logging
import asyncio
from pathlib import Path
from typing import List, Dict, Any

# Ensure agentic-lab-eac src directory is in sys.path
EAC_SRC = Path("/home/gris96/.hermes/workspace/agentic-lab-eac/src")
if EAC_SRC.exists() and str(EAC_SRC) not in sys.path:
    sys.path.insert(0, str(EAC_SRC))

from agentic_lab_eac.models import Hypothesis, LabConfig
from eac_bridge.reasoning import LLMReasoningBridge
from eac_bridge.falsifier import FalsifierAdversary

logger = logging.getLogger(__name__)

class BruteHypothesisGenerator:
    """
    High-Throughput parallel generation engine (inspired by KISS Discovery Engine).
    Generates dozens of hypothesis variants in parallel, verifies them
    concurrently through the FalsifierAdversary, and yields only valid, robust winners.
    """
    def __init__(self):
        self.bridge = LLMReasoningBridge()
        self.adversary = FalsifierAdversary()

    async def generate_variants_async(
        self, goal: str, lab: LabConfig, prior_evidence: List[Dict], count: int = 10
    ) -> List[Hypothesis]:
        """
        Generate N variants in parallel batches.
        """
        logger.info(f"Starting parallel brute generation of ~{count} candidates...")
        
        # We'll run multiple parallel reasoning generation queries
        # (each query yields 3 hypotheses, so we run count/3 tasks in parallel)
        num_tasks = max(1, count // 3)
        loop = asyncio.get_running_loop()

        def sync_call():
            return self.bridge.generate(goal, lab, prior_evidence)

        # Run tasks in ThreadPoolExecutor since CloudResearcher uses synchronous subprocess/curl calls
        tasks = [loop.run_in_executor(None, sync_call) for _ in range(num_tasks)]
        batches = await asyncio.gather(*tasks)

        all_candidates = []
        for batch in batches:
            if batch:
                all_candidates.extend(batch)

        logger.info(f"Generated {len(all_candidates)} candidates total. Running parallel falsification audits...")

        # Run parallel verifications using the FalsifierAdversary
        async def verify_candidate(hyp: Hypothesis) -> Hypothesis | None:
            # We run the synchronous check_hypothesis in the executor
            def check():
                return self.adversary.check_hypothesis(hyp.statement, hyp.rationale)
            
            passed, msg = await loop.run_in_executor(None, check)
            if passed:
                logger.info(f"Candidate {hyp.id} PASSED verification: {msg}")
                return hyp
            else:
                logger.warning(f"Candidate {hyp.id} FALSIFIED: {msg}")
                return None

        verification_tasks = [verify_candidate(h) for h in all_candidates]
        verified_results = await asyncio.gather(*verification_tasks)

        # Keep only the ones that survived
        winners = [h for h in verified_results if h is not None]
        logger.info(f"Verification complete: {len(winners)} passed, {len(all_candidates) - len(winners)} failed.")
        
        # Re-index ids to avoid conflicts
        for idx, w in enumerate(winners):
            w.id = f"hyp-eac-{idx:03d}"
        
        return winners
