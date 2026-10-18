"""
PorchaLens Unit Test Suite
Verifies:
1. 16-Ana Tenancy Math Engine (আনা-গণ্ডা-কড়া-ক্রান্তি-তিল Conversion)
2. Mathematical Fraud & Over-allocation Detection
3. Deficit / Torn Document Margin Detection
4. Faraiz Muslim Succession Law Engine (Quranic fixed shares)
5. 4-Pillar Citizen Land Safety Suite (Khas, Bank Mortgage, Injunction, Tax)
"""

import unittest
from tenancy_math import (
    calculate_share_tils,
    tils_to_ana_breakdown,
    audit_khatian_math,
    FULL_KHATIAN_TILS
)
from faraiz_engine import calculate_faraiz_distribution
from security_registry import verify_land_safety

class TestPorchaLensEngine(unittest.TestCase):

    def test_til_conversion_constants(self):
        """Test base conversions for Bengal land accounting units."""
        # 1 Ana = 4800 Tils
        self.assertEqual(calculate_share_tils(ana=1), 4800)
        # 1 Gonda = 240 Tils
        self.assertEqual(calculate_share_tils(gonda=1), 240)
        # 1 Kora = 60 Tils
        self.assertEqual(calculate_share_tils(kora=1), 60)
        # 1 Kranti = 20 Tils
        self.assertEqual(calculate_share_tils(kranti=1), 20)
        # 16 Anas = 76,800 Tils
        self.assertEqual(calculate_share_tils(ana=16), FULL_KHATIAN_TILS)
        print("✓ Test 1 Passed: Tenancy unit constants mathematically sound (16 Anas = 76,800 Tils).")

    def test_authentic_16_ana_khatian(self):
        """Test a clean authentic 16-Ana Khatian sums to exactly 76,800 Tils."""
        owners = [
            {"name": "তারিকুল ইসলাম", "ana": 6, "gonda": 8, "kora": 0, "kranti": 0, "til": 0},
            {"name": "রফিকুল ইসলাম", "ana": 6, "gonda": 8, "kora": 0, "kranti": 0, "til": 0},
            {"name": "ফাতেমা বেগম", "ana": 3, "gonda": 4, "kora": 0, "kranti": 0, "til": 0}
        ]
        # Total: (6*4800 + 8*240)*2 + (3*4800 + 4*240) = 30720*2 + 15360 = 76,800 Tils
        res = audit_khatian_math(owners=owners, total_area_decimals=20.0)
        self.assertEqual(res["status"], "AUTHENTIC_PERFECT")
        self.assertEqual(res["discrepancy_tils"], 0.0)
        self.assertEqual(res["owners"][0]["calculated_decimals"], 8.0)
        self.assertEqual(res["owners"][2]["calculated_decimals"], 4.0)
        print("✓ Test 2 Passed: Authentic 16-Ana CS Khatian verified with exact decimal conversion.")

    def test_fraud_overallocation_detection(self):
        """Test that an altered/inflated share triggers FRAUD_OVERALLOCATION."""
        owners = [
            {"name": "তারিকুল ইসলাম (জাল হিস্যা)", "ana": 10, "gonda": 0, "kora": 0, "kranti": 0, "til": 0},
            {"name": "রফিকুল ইসলাম", "ana": 6, "gonda": 8, "kora": 0, "kranti": 0, "til": 0},
            {"name": "ফাতেমা বেগম", "ana": 3, "gonda": 4, "kora": 0, "kranti": 0, "til": 0}
        ]
        res = audit_khatian_math(owners=owners, total_area_decimals=20.0)
        self.assertEqual(res["status"], "FRAUD_OVERALLOCATION")
        self.assertGreater(res["discrepancy_tils"], 0)
        print(f"✓ Test 3 Passed: Tampered share caught! (Fraud excess: {res['discrepancy_decimals_bn']} decimals).")

    def test_deficit_torn_margin_detection(self):
        """Test that missing co-sharer or torn margin triggers DEFICIT_OR_TORN."""
        owners = [
            {"name": "তারিকুল ইসলাম", "ana": 6, "gonda": 8, "kora": 0, "kranti": 0, "til": 0},
            {"name": "রফিকুল ইসলাম", "ana": 6, "gonda": 8, "kora": 0, "kranti": 0, "til": 0}
            # Missing Fatima Begum (3 ana 4 gonda)
        ]
        res = audit_khatian_math(owners=owners, total_area_decimals=20.0)
        self.assertEqual(res["status"], "DEFICIT_OR_TORN")
        self.assertLess(res["discrepancy_tils"], 0)
        print("✓ Test 4 Passed: Omitted co-sharer / torn margin detected.")

    def test_faraiz_islamic_succession(self):
        """Test Muslim succession law allocation and female protection alert."""
        res = calculate_faraiz_distribution(
            deceased_name="মৃত রহিম উদ্দিন সরকার",
            total_area_decimals=20.0,
            num_wives=1,
            num_sons=2,
            num_daughters=1
        )
        # Wife: 1/8 (12.5% = 2.5 dec)
        # Residue: 17.5 dec. 2 sons (4 parts) + 1 daughter (1 part) = 5 parts.
        # Each part = 3.5 dec. Each son = 7.0 dec. Daughter = 3.5 dec.
        self.assertEqual(len(res["heirs"]), 4)
        self.assertEqual(res["heirs"][0]["allocated_decimals"], 2.5)
        self.assertEqual(res["heirs"][1]["allocated_decimals"], 7.0)
        self.assertEqual(res["heirs"][3]["allocated_decimals"], 3.5)
        self.assertIn("নারী ওয়ারিশদের মোট", res["female_protection"]["alert_bn"])
        print("✓ Test 5 Passed: Faraiz Succession accurately computes 2:1 ratio and female shares.")

    def test_4_pillar_safety_audit(self):
        """Test the 4-Pillar Citizen Land Safety Audit on clean vs disputed plots."""
        # Clean Plot (Dag 810)
        clean = verify_land_safety(dag_no="810", math_status="AUTHENTIC_PERFECT")
        self.assertEqual(clean["score"], 100)
        self.assertTrue(clean["khas_record"]["is_safe"])
        self.assertTrue(clean["bank_record"]["is_safe"])
        self.assertTrue(clean["court_record"]["is_safe"])

        # Disputed Plot (Dag 302 - Court injunction + Bank mortgage)
        disputed = verify_land_safety(dag_no="302", math_status="AUTHENTIC_PERFECT")
        self.assertLess(disputed["score"], 50)
        self.assertFalse(disputed["bank_record"]["is_safe"])
        self.assertFalse(disputed["court_record"]["is_safe"])
        print(f"✓ Test 6 Passed: Safety scoring valid (Clean Dag 810: {clean['score']}/100, Disputed Dag 302: {disputed['score']}/100).")

if __name__ == "__main__":
    unittest.main()
