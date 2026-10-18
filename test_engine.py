import unittest
from graph_core import engine

class TestBhumiGraphEngine(unittest.TestCase):
    def setUp(self):
        # Reset locks
        engine.active_locks.clear()

    def test_scenario_1_fractional_overselling(self):
        """Test that Tariqul cannot sell 10 decimals when only 3 remain."""
        res = engine.audit_transfer_attempt(
            parcel_id="BS-810",
            seller_nid="1988-9901-01",
            proposed_area_decimals=10.0
        )
        self.assertEqual(res["decision"], "REJECTED")
        self.assertEqual(res["violation_code"], "SHARE_DEPLETION_OVERSELLING")
        self.assertEqual(res["deficit"], 7.0)
        print("✓ Test 1 Passed: Fractional Over-Selling correctly blocked!")

    def test_scenario_2_sister_disinheritance(self):
        """Test that omitting female heir Fatima Begum triggers Faraiz fraud block."""
        fraudulent_claim = [
            {"nid": "1988-9901-01", "name": "Tariqul Islam", "relation": "SON"},
            {"nid": "1992-9901-02", "name": "Rafiqul Islam", "relation": "SON"}
        ]
        res = engine.audit_transfer_attempt(
            parcel_id="BS-810",
            seller_nid="1988-9901-01",
            proposed_area_decimals=4.0,
            claimed_heirs=fraudulent_claim
        )
        self.assertEqual(res["decision"], "REJECTED")
        self.assertEqual(res["violation_code"], "FEMALE_HEIR_CONCEALMENT_FRAUD")
        print("✓ Test 2 Passed: Sister Disinheritance / Faraiz fraud caught!")

    def test_scenario_3_court_injunction(self):
        """Test that Dag 302 with active High Court Status Quo injunction is blocked."""
        res = engine.audit_transfer_attempt(
            parcel_id="BS-302",
            seller_nid="1975-4402-19",
            proposed_area_decimals=5.0
        )
        self.assertEqual(res["decision"], "REJECTED")
        self.assertEqual(res["violation_code"], "ACTIVE_COURT_INJUNCTION")
        print("✓ Test 3 Passed: Court Injunction (Lis Pendens) successfully enforced!")

    def test_scenario_4_inter_registry_lock(self):
        """Test that pending deed in one Sub-Registry blocks concurrent registration elsewhere."""
        engine.acquire_inter_registry_lock("BS-810", "Gazipur Sadar Sub-Registry", 3.0)
        res = engine.audit_transfer_attempt(
            parcel_id="BS-810",
            seller_nid="1988-9901-01",
            proposed_area_decimals=3.0
        )
        self.assertEqual(res["decision"], "REJECTED")
        self.assertEqual(res["violation_code"], "CONCURRENT_TRANSFER_LOCK_ACTIVE")
        print("✓ Test 4 Passed: Inter-Registry real-time lock blocked collision!")

    def test_scenario_5_clean_title(self):
        """Test that a clean unbroken title receives cryptographic clearance."""
        res = engine.audit_transfer_attempt(
            parcel_id="BS-1104",
            seller_nid="1985-2201-99",
            proposed_area_decimals=4.0
        )
        self.assertEqual(res["decision"], "APPROVED")
        self.assertIn("cryptographic_deed_hash", res)
        print("✓ Test 5 Passed: Clean title successfully verified with SHA-256 hash!")

    def test_land_health_score(self):
        """Test Land Health Index calculations."""
        h_clean = engine.compute_land_health_score("BS-1104")
        self.assertEqual(h_clean["score"], 100)
        
        h_disputed = engine.compute_land_health_score("BS-302")
        self.assertLess(h_disputed["score"], 50)
        print(f"✓ Test 6 Passed: Health scores calculated accurately (Clean: {h_clean['score']}, Disputed: {h_disputed['score']})")

if __name__ == "__main__":
    unittest.main()
