#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_alphafold_profile.py
Unit and integration tests for the AlphaFold DB profiling pipeline.
"""

import os
import json
import unittest
from unittest.mock import patch, MagicMock
import requests
import sys

# Add the parent directory and scripts to sys.path so we can import directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts import alphafold_profile_target

class TestAlphaFoldProfiling(unittest.TestCase):
    
    def setUp(self):
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/alphafold"))
        
    @patch('time.sleep', return_value=None) # Speed up test
    @patch('requests.get')
    def test_retry_logic_success_after_503(self, mock_get, mock_sleep):
        """
        Verify that fetch_url_with_retry successfully retries after receiving 503 errors.
        """
        # Create mock responses: two 503s followed by a 200 OK containing JSON
        mock_response_503 = MagicMock()
        mock_response_503.status_code = 503
        
        mock_response_200 = MagicMock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {"status": "success"}
        
        # Side effect list: 2 failures then 1 success
        mock_get.side_effect = [mock_response_503, mock_response_503, mock_response_200]
        
        result = alphafold_profile_target.fetch_url_with_retry(
            "https://fakeurl.com/api", is_json=True, retries=3, backoff_factor=1
        )
        
        self.assertEqual(result, {"status": "success"})
        self.assertEqual(mock_get.call_count, 3)
        
    @patch('time.sleep', return_value=None) # Speed up test
    @patch('requests.get')
    def test_retry_logic_failure_all_503(self, mock_get, mock_sleep):
        """
        Verify that fetch_url_with_retry raises an HTTPError after exhausting all retries.
        """
        mock_response_503 = MagicMock()
        mock_response_503.status_code = 503
        
        mock_get.return_value = mock_response_503
        
        with self.assertRaises(requests.exceptions.HTTPError):
            alphafold_profile_target.fetch_url_with_retry(
                "https://fakeurl.com/api", is_json=True, retries=2, backoff_factor=1
            )
            
        self.assertEqual(mock_get.call_count, 3) # First try + 2 retries

    def test_bfr_profile_structure(self):
        """
        Integration test for BFR (P0ABD3) profile output.
        Verifies that exactly 1 rigid domain covering >90% of the chain with mean_plddt > 90 is detected.
        """
        profile_path = os.path.join(self.output_dir, "P0ABD3_profile.json")
        self.assertTrue(os.path.exists(profile_path), f"BFR profile file {profile_path} must exist. Run the pipeline first!")
        
        with open(profile_path, 'r') as f:
            profile = json.load(f)
            
        # Basic sanity checks
        self.assertEqual(profile["uniprot_id"], "P0ABD3")
        self.assertEqual(profile["length"], 158)
        self.assertGreater(profile["global_mean_plddt"], 90.0)
        
        # Domains check
        domains = profile["domains"]
        self.assertEqual(len(domains), 1, "BFR should be classified as exactly 1 rigid domain monomer.")
        
        dom = domains[0]
        self.assertEqual(dom["start"], 1)
        self.assertEqual(dom["end"], 158)
        self.assertEqual(dom["length"], 158)
        self.assertGreater(dom["mean_plddt"], 90.0)
        
        # IDR check
        self.assertEqual(len(profile["idrs"]), 0, "BFR should have zero IDRs detected.")
        
        # Snapshot-like regression test
        self.assertIn("plddt_distribution", profile)
        self.assertGreater(profile["plddt_distribution"]["very_high"], 90.0)
        
    def test_drd2_profile_structure(self):
        """
        Integration test for DRD2 (P14416) profile output.
        Verifies that at least 1 large TM domain (>=200 residues, mean_plddt > 80) and
        at least 1 contiguous IDR > 50 residues corresponding to ICL3 are detected.
        """
        profile_path = os.path.join(self.output_dir, "P14416_profile.json")
        self.assertTrue(os.path.exists(profile_path), f"DRD2 profile file {profile_path} must exist. Run the pipeline first!")
        
        with open(profile_path, 'r') as f:
            profile = json.load(f)
            
        self.assertEqual(profile["uniprot_id"], "P14416")
        
        # Transmembrane domain assert
        domains = profile["domains"]
        large_tm_domains = [d for d in domains if d["length"] >= 200 and d["mean_plddt"] > 80]
        # Wait, if GPCR TM domain is split due to ICL3, one of the split TM domains might be >= 200.
        # Let's check: total length of DRD2 is 443 AAs.
        # TM domain parts:
        # Segment 1 (TM1-TM5): residues 1 to ~220 (length 220 AAs)
        # Segment 2 (TM6-TM7): residues ~310 to 443 (length 134 AAs)
        # So Segment 1 is indeed >= 200 residues! Let's check if we find a domain >= 200 residues or we check the union.
        # Let's write a flexible check that asserts at least one large TM domain segment of size >= 100 or 200 exists.
        # Let's use the exact user prompt requirement: "detecta >=1 dominio TM grande (>=200 residues, mean_plddt>80)".
        # This matches Segment 1 (1-220 residues) perfectly!
        self.assertTrue(len(large_tm_domains) >= 1, f"DRD2 must have at least one large domain (>=200 residues) with high confidence. Found: {domains}")
        
        # IDR assert (representing ICL3)
        idrs = profile["idrs"]
        large_idrs = [idr for idr in idrs if idr["length"] > 50 and idr["mean_plddt"] < 50]
        self.assertTrue(len(large_idrs) >= 1, f"DRD2 must have a large IDR (>50 residues) for ICL3. Found: {idrs}")

    def test_cpa3_profile_structure(self):
        """
        Integration test for CPA3 (P15088) profile output.
        Verifies that at least 1 unique catalytic domain (>=250 residues, mean_plddt > 85) is detected.
        """
        profile_path = os.path.join(self.output_dir, "P15088_profile.json")
        self.assertTrue(os.path.exists(profile_path), f"CPA3 profile file {profile_path} must exist. Run the pipeline first!")
        
        with open(profile_path, 'r') as f:
            profile = json.load(f)
            
        self.assertEqual(profile["uniprot_id"], "P15088")
        
        domains = profile["domains"]
        catalytic_domains = [d for d in domains if d["length"] >= 250 and d["mean_plddt"] > 85]
        self.assertTrue(len(catalytic_domains) >= 1, f"CPA3 must have at least 1 large catalytic domain segment (>=250 residues). Found: {domains}")

    def test_nipah_g_profile_structure(self):
        """
        Integration test for Nipah G (Q9IH62) profile output.
        Verifies that at least 2 distinct global domains are detected (e.g. head globular and stalk).
        """
        profile_path = os.path.join(self.output_dir, "Q9IH62_profile.json")
        self.assertTrue(os.path.exists(profile_path), f"Nipah G profile file {profile_path} must exist. Run the pipeline first!")
        
        with open(profile_path, 'r') as f:
            profile = json.load(f)
            
        self.assertEqual(profile["uniprot_id"], "Q9IH62")
        
        domains = profile["domains"]
        # Nipah G has a stalk domain and a head domain. 
        # The connected components with standard cutoff should split these into separate domains.
        # We assert that we detect at least 2 domains.
        self.assertTrue(len(domains) >= 2, f"Nipah G must have at least 2 domains detected (head globular and stalk). Found: {domains}")

if __name__ == "__main__":
    unittest.main()
