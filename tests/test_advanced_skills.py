import unittest
import sys
from pathlib import Path

# Ensure the workspace is in the python path
WORKSPACE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(WORKSPACE / "automated_lab"))

from eac_bridge.literature import CombinedLiteratureProvider
from eac_bridge.ledger import ResearchLedger
from eac_bridge.executor import ProteinLabExecutor

class TestAdvancedScientificSkills(unittest.TestCase):
    def setUp(self):
        # Use a temporary DB path for testing to keep things clean
        self.ledger = ResearchLedger(db_path="artifacts/eac_test_ledger.db")
        self.executor = ProteinLabExecutor(self.ledger)
        self.lit_provider = CombinedLiteratureProvider()

    def test_needleman_wunsch_alignment(self):
        """Test the pure Python global Needleman-Wunsch homology sequence alignment."""
        seq1 = "MALWMRLL"
        seq2 = "MALWCRLL"
        res = self.executor.align_homologs(seq1, seq2)
        
        self.assertIn("percent_identity", res)
        self.assertIn("aligned_seq1", res)
        self.assertIn("aligned_seq2", res)
        self.assertGreater(res["percent_identity"], 80.0)
        self.assertEqual(res["aligned_seq1"].replace("-", ""), seq1)
        self.assertEqual(res["aligned_seq2"].replace("-", ""), seq2)

        # Test alignment with gaps
        seq3 = "MALWMRLL"
        seq4 = "MALWRLL"
        res2 = self.executor.align_homologs(seq3, seq4)
        self.assertIn("-", res2["aligned_seq2"])
        self.assertGreater(res2["percent_identity"], 70.0)

    def test_monitor_preprints(self):
        """Test EuropePMC preprint query and citation grounding filters."""
        results = self.lit_provider.monitor_preprints(query="nipah virus", limit=3)
        
        self.assertIsInstance(results, list)
        for r in results:
            self.assertIn("title", r)
            self.assertIn("authors", r)
            self.assertIn("url", r)
            self.assertEqual(r["source"], "europepmc_preprint")

    def test_query_affinity_experimental(self):
        """Test ChEMBL API and offline fallback lookup for experimental target-drug affinity."""
        mor_affinity = self.executor.query_affinity_experimental("OPRM1", "naltrexone")
        self.assertEqual(mor_affinity, 9.2)

        nipah_affinity = self.executor.query_affinity_experimental("nipah", "naltrexone")
        self.assertEqual(nipah_affinity, 4.5)

        bias = 5.66 - nipah_affinity
        self.assertAlmostEqual(bias, 1.16)

if __name__ == "__main__":
    unittest.main()
