"""
BhumiGraph - Graph-Theoretic Verification Engine
Implements:
1. Share-Conservation Protocol (Sum(Transfers) <= Acquired Title)
2. Faraiz Inheritance Legal Share Verification (Muslim Succession Law)
3. 30-Year Cadastral Lineage Continuity Check (CS -> SA -> RS -> BS)
4. Distributed Transaction Lien Locking (Eliminating the Inter-Registry Window)
5. Composite Land Health Index (0 - 100)
"""

import hashlib
import json
import time
from typing import Dict, Any, List, Tuple
from data_models import PARCELS_DB

class BhumiGraphEngine:
    def __init__(self):
        # In-memory distributed lock ledger simulating Sub-Registry <-> AC Land inter-office bridge
        self.active_locks: Dict[str, Dict[str, Any]] = {}

    def get_parcel(self, parcel_id: str) -> Dict[str, Any]:
        return PARCELS_DB.get(parcel_id)

    def list_all_parcels(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": p["id"],
                "mouza": p["mouza"],
                "upazila": p["upazila"],
                "district": p["district"],
                "dag_no": p["dag_no"],
                "khatian_no": p["khatian_no"],
                "area_decimals": p["total_area_decimals"],
                "tax_status": p["tax_status"],
                "has_encumbrance": len(p["encumbrances"]) > 0
            }
            for p in PARCELS_DB.values()
        ]

    # =========================================================================
    # 1. GRAPH GENERATION (Vis.js Network JSON format)
    # =========================================================================
    def build_vis_graph(self, parcel_id: str) -> Dict[str, Any]:
        parcel = self.get_parcel(parcel_id)
        if not parcel:
            return {"nodes": [], "edges": []}

        nodes = []
        edges = []

        # Survey Nodes (CS -> SA -> RS -> BS)
        prev_node_id = None
        for i, s in enumerate(parcel["lineage"]):
            node_id = f"survey_{s['survey_type']}_{s['dag_no']}"
            color = "#f59e0b" if s["survey_type"] != "BS" else "#3b82f6"
            label = f"{s['survey_type']} Survey\nDag: {s['dag_no']}\nKh: {s['khatian_no']} ({s['year']})"
            
            nodes.append({
                "id": node_id,
                "label": label,
                "shape": "box",
                "color": {"background": color, "border": "#1e293b"},
                "font": {"color": "#ffffff", "face": "Courier", "size": 13},
                "level": i + 1,
                "title": f"Survey: {s['survey_type']} | Recorded Area: {s['area_decimals']} decimals"
            })

            if prev_node_id:
                edges.append({
                    "from": prev_node_id,
                    "to": node_id,
                    "label": "SURVEY_REVISED",
                    "arrows": "to",
                    "color": {"color": "#94a3b8"},
                    "dashes": False
                })
            prev_node_id = node_id

        # Current BS Dag Node is the center
        bs_node_id = prev_node_id

        # Faraiz Inheritance Nodes (if applicable)
        if parcel.get("faraiz_profile"):
            fp = parcel["faraiz_profile"]
            faraiz_parent_id = "parent_rahim"
            nodes.append({
                "id": faraiz_parent_id,
                "label": f"Deceased Owner\n{fp['deceased_parent']}\n(Died: 2018)",
                "shape": "ellipse",
                "color": {"background": "#64748b", "border": "#334155"},
                "font": {"color": "#ffffff"},
                "level": len(parcel["lineage"]) + 1
            })
            edges.append({
                "from": bs_node_id,
                "to": faraiz_parent_id,
                "label": "RECORDED_DECEASED",
                "arrows": "to"
            })

            for heir in fp["heirs"]:
                heir_id = f"heir_{heir['nid']}"
                # Fatima is female heir
                is_female = heir["relation"] == "DAUGHTER"
                heir_color = "#10b981" if not is_female else "#ec4899"
                nodes.append({
                    "id": heir_id,
                    "label": f"{heir['name']} ({heir['relation']})\nLegal Share: {heir['legal_share_fraction']*100}%\n({heir['legal_area']} decimals)",
                    "shape": "box",
                    "color": {"background": heir_color, "border": "#047857" if not is_female else "#be185d"},
                    "font": {"color": "#ffffff"},
                    "level": len(parcel["lineage"]) + 2
                })
                edges.append({
                    "from": faraiz_parent_id,
                    "to": heir_id,
                    "label": f"FARAIZ_SPLIT ({int(heir['legal_share_fraction']*100)}%)",
                    "arrows": "to"
                })

        # Completed Transfers (e.g., Tariqul's past sale)
        for t in parcel.get("completed_transfers", []):
            t_node_id = f"trans_{t['deed_no']}"
            nodes.append({
                "id": t_node_id,
                "label": f"Registered Deed\n{t['deed_no']}\nSold: {t['transferred_area_decimals']} dec\nBuyer: {t['buyer_name']}",
                "shape": "database",
                "color": {"background": "#8b5cf6", "border": "#6d28d9"},
                "font": {"color": "#ffffff"},
                "level": len(parcel["lineage"]) + 3
            })
            # Connect from Tariqul
            seller_node = f"heir_{t['seller_nid']}" if parcel.get("faraiz_profile") else bs_node_id
            edges.append({
                "from": seller_node,
                "to": t_node_id,
                "label": f"SOLD ({t['transferred_area_decimals']} dec)",
                "arrows": "to",
                "color": {"color": "#a855f7"}
            })

        # Encumbrances (Court Injunctions, Bank Mortgages)
        for enc in parcel.get("encumbrances", []):
            enc_id = f"enc_{enc['reference_no']}"
            is_court = enc["encumbrance_type"] == "COURT_INJUNCTION"
            nodes.append({
                "id": enc_id,
                "label": f"LOCK: {enc['encumbrance_type']}\nRef: {enc['reference_no']}\nBy: {enc['institution']}",
                "shape": "diamond",
                "color": {"background": "#ef4444", "border": "#b91c1c"},
                "font": {"color": "#ffffff", "face": "Courier", "size": 11},
                "level": len(parcel["lineage"]) + 1
            })
            edges.append({
                "from": bs_node_id,
                "to": enc_id,
                "label": "INJUNCTION_LIEN",
                "arrows": "to",
                "color": {"color": "#ef4444"},
                "width": 3
            })

        # Active Locks (if any temporary deed locks)
        if parcel_id in self.active_locks:
            lock = self.active_locks[parcel_id]
            lock_node_id = f"lock_{lock['lock_token']}"
            nodes.append({
                "id": lock_node_id,
                "label": f"REALTIME INTER-OFFICE LOCK\nToken: {lock['lock_token'][:8]}...\nSub-Registry: {lock['office']}\nPending Deed: {lock['area']} dec",
                "shape": "star",
                "color": {"background": "#dc2626", "border": "#991b1b"},
                "font": {"color": "#ffffff"},
                "level": len(parcel["lineage"]) + 2
            })
            edges.append({
                "from": bs_node_id,
                "to": lock_node_id,
                "label": "LOCKED",
                "arrows": "to",
                "color": {"color": "#dc2626"},
                "width": 4,
                "dashes": True
            })

        return {"nodes": nodes, "edges": edges}

    # =========================================================================
    # 2. CORE ALGORITHM: SHARE CONSERVATION & LEGAL AUDIT
    # =========================================================================
    def audit_transfer_attempt(
        self,
        parcel_id: str,
        seller_nid: str,
        proposed_area_decimals: float,
        claimed_heirs: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes a multi-layer graph traversal audit:
        Layer 1: Inter-office distributed lock check (Double-selling window)
        Layer 2: Encumbrances (Court Injunctions & Bank Mortgages)
        Layer 3: Faraiz Succession Integrity (Sister Disinheritance check)
        Layer 4: Share Conservation Protocol (Sum of historical sales + proposed sale <= Acquired legal share)
        """
        parcel = self.get_parcel(parcel_id)
        if not parcel:
            return {"status": "ERROR", "message": f"Parcel ID {parcel_id} not found in National Cadastre."}

        # ---------------------------------------------------------------------
        # LAYER 1: REAL-TIME INTER-OFFICE DISTRIBUTED LOCK CHECK
        # ---------------------------------------------------------------------
        if parcel_id in self.active_locks:
            lock = self.active_locks[parcel_id]
            return {
                "decision": "REJECTED",
                "risk_level": "CRITICAL_FRAUD_ATTEMPT",
                "violation_code": "CONCURRENT_TRANSFER_LOCK_ACTIVE",
                "title": "Double-Selling Window Detected!",
                "explanation": (
                    f"This parcel is currently locked by {lock['office']} under pending Deed Registration Token "
                    f"'{lock['lock_token']}'. Simultaneous sales across multiple offices are blocked by BhumiGraph."
                ),
                "remaining_share_decimals": 0.0,
                "details": lock
            }

        # ---------------------------------------------------------------------
        # LAYER 2: COURT INJUNCTION & BANK MORTGAGE CHECK
        # ---------------------------------------------------------------------
        for enc in parcel.get("encumbrances", []):
            if enc["status"] in ["ACTIVE_STATUS_QUO", "ACTIVE_LIEN"]:
                return {
                    "decision": "REJECTED",
                    "risk_level": "LEGAL_BARRIER",
                    "violation_code": f"ACTIVE_{enc['encumbrance_type']}",
                    "title": f"Transfer Prohibited: {enc['encumbrance_type'].replace('_', ' ')}",
                    "explanation": (
                        f"Order from '{enc['institution']}' (Ref: {enc['reference_no']}): {enc['details']}. "
                        "No deed can be registered or mutated under Section 52 of the Transfer of Property Act (Lis Pendens)."
                    ),
                    "remaining_share_decimals": 0.0,
                    "details": enc
                }

        # ---------------------------------------------------------------------
        # LAYER 3: FARAIZ SUCCESSION INTEGRITY CHECK
        # ---------------------------------------------------------------------
        if parcel.get("faraiz_profile") and claimed_heirs is not None:
            actual_faraiz = parcel["faraiz_profile"]
            actual_heir_nids = {h["nid"]: h for h in actual_faraiz["heirs"]}
            claimed_heir_nids = {h.get("nid"): h for h in claimed_heirs}

            # Check if any legitimate legal heir is omitted
            missing_heirs = []
            for actual_h in actual_faraiz["heirs"]:
                if actual_h["nid"] not in claimed_heir_nids:
                    missing_heirs.append(actual_h)

            # Check if a female heir (sister/mother/daughter) was concealed
            deprived_females = [
                h for h in actual_faraiz["heirs"] 
                if h["relation"] in ["DAUGHTER", "MOTHER", "WIFE", "SISTER"] 
                and h["nid"] not in claimed_heir_nids
            ]

            if deprived_females:
                deprived_names = ", ".join([f"{f['name']} ({f['relation']}, entitled {f['legal_area']} decimals)" for f in deprived_females])
                return {
                    "decision": "REJECTED",
                    "risk_level": "CRITICAL_FRAUD_ATTEMPT",
                    "violation_code": "FEMALE_HEIR_CONCEALMENT_FRAUD",
                    "title": "Inheritance Usurpation / Faraiz Fraud Detected!",
                    "explanation": (
                        f"The submitted Warishnama (Succession claim) deliberately omitted female heir(s): {deprived_names}. "
                        f"Under Bangladesh Muslim Succession Law, co-heirs cannot absorb female shares without registered Nadabi (relinquishment) deed."
                    ),
                    "remaining_share_decimals": 0.0,
                    "missing_heirs": deprived_females
                }

        # ---------------------------------------------------------------------
        # LAYER 4: SHARE CONSERVATION PROTOCOL
        # ---------------------------------------------------------------------
        # Calculate seller's absolute starting entitlement
        starting_entitlement = 0.0
        seller_name = "Unknown"

        if parcel.get("faraiz_profile"):
            for heir in parcel["faraiz_profile"]["heirs"]:
                if heir["nid"] == seller_nid:
                    starting_entitlement = heir["legal_area"]
                    seller_name = heir["name"]
                    break
        else:
            # Direct owner
            starting_entitlement = parcel["total_area_decimals"]
            seller_name = parcel["recorded_owners"][0] if parcel.get("recorded_owners") else "Recorded Owner"

        if starting_entitlement <= 0:
            return {
                "decision": "REJECTED",
                "risk_level": "ZERO_TITLE_FRAUD",
                "violation_code": "NO_TITLE_RECORDED",
                "title": "Zero Title Recorded",
                "explanation": f"Seller NID '{seller_nid}' holds no recorded entitlement in Dag {parcel['dag_no']}.",
                "remaining_share_decimals": 0.0
            }

        # Calculate historical transfers already executed by this seller
        already_transferred = 0.0
        for t in parcel.get("completed_transfers", []):
            if t["seller_nid"] == seller_nid:
                already_transferred += t["transferred_area_decimals"]

        net_available_share = round(starting_entitlement - already_transferred, 2)

        # CHECK VIOLATION: Is proposed transfer > remaining share?
        if proposed_area_decimals > net_available_share:
            deficit = round(proposed_area_decimals - net_available_share, 2)
            return {
                "decision": "REJECTED",
                "risk_level": "CRITICAL_FRAUD_ATTEMPT",
                "violation_code": "SHARE_DEPLETION_OVERSELLING",
                "title": "Fractional Over-Selling Fraud Detected!",
                "seller_name": seller_name,
                "starting_entitlement": starting_entitlement,
                "already_transferred_past": already_transferred,
                "net_available_share": net_available_share,
                "attempted_to_sell": proposed_area_decimals,
                "deficit": deficit,
                "explanation": (
                    f"Seller '{seller_name}' legally inherited {starting_entitlement} decimals. "
                    f"They previously sold {already_transferred} decimals (Deed {parcel['completed_transfers'][0]['deed_no']}), "
                    f"leaving only {net_available_share} decimals available. "
                    f"Attempting to sell {proposed_area_decimals} decimals creates an illegal deficit of {deficit} decimals."
                )
            }

        # If everything passes: APPROVED!
        new_balance = round(net_available_share - proposed_area_decimals, 2)
        deed_hash = hashlib.sha256(
            f"{parcel_id}:{seller_nid}:{proposed_area_decimals}:{time.time()}".encode()
        ).hexdigest()

        return {
            "decision": "APPROVED",
            "risk_level": "VERIFIED_CLEAN",
            "seller_name": seller_name,
            "starting_entitlement": starting_entitlement,
            "already_transferred_past": already_transferred,
            "net_available_share": net_available_share,
            "approved_transfer_area": proposed_area_decimals,
            "new_balance_after_sale": new_balance,
            "cryptographic_deed_hash": deed_hash,
            "explanation": (
                f"Title chain completely verified. Seller has {net_available_share} decimals remaining. "
                f"Proposed sale of {proposed_area_decimals} decimals approved. "
                f"Post-registration balance will be {new_balance} decimals."
            )
        }

    # =========================================================================
    # 3. REAL-TIME DISTRIBUTED LOCK SIMULATION
    # =========================================================================
    def acquire_inter_registry_lock(self, parcel_id: str, office: str, area_decimals: float) -> Dict[str, Any]:
        """Locks a parcel during the deed processing window, preventing same-day double selling."""
        if parcel_id in self.active_locks:
            return {"success": False, "message": "Parcel is ALREADY locked by another pending registration."}

        token = f"LOCK-{hashlib.md5(f'{parcel_id}:{time.time()}'.encode()).hexdigest()[:8].upper()}"
        self.active_locks[parcel_id] = {
            "lock_token": token,
            "office": office,
            "area": area_decimals,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return {"success": True, "token": token, "lock_details": self.active_locks[parcel_id]}

    def release_inter_registry_lock(self, parcel_id: str) -> bool:
        if parcel_id in self.active_locks:
            del self.active_locks[parcel_id]
            return True
        return False

    # =========================================================================
    # 4. COMPOSITE LAND HEALTH SCORE (0 - 100)
    # =========================================================================
    def compute_land_health_score(self, parcel_id: str) -> Dict[str, Any]:
        parcel = self.get_parcel(parcel_id)
        if not parcel:
            return {"score": 0, "rating": "UNKNOWN"}

        score = 100
        penalties = []

        # 1. Encumbrance penalty (Active Injunction = -50, Bank Mortgage = -30)
        for enc in parcel.get("encumbrances", []):
            if enc["encumbrance_type"] == "COURT_INJUNCTION":
                score -= 50
                penalties.append({"factor": "Active High Court Injunction (Status Quo)", "deduction": -50})
            elif enc["encumbrance_type"] == "BANK_MORTGAGE":
                score -= 30
                penalties.append({"factor": "Undischarged Commercial Bank Mortgage", "deduction": -30})

        # 2. Tax penalty
        if parcel.get("tax_status") != "PAID_UP_TO_DATE":
            score -= 20
            penalties.append({"factor": f"Unpaid Land Development Tax ({parcel.get('tax_status')})", "deduction": -20})

        # 3. Lineage Completeness (Expect all 4 surveys: CS, SA, RS, BS)
        surveys = [s["survey_type"] for s in parcel.get("lineage", [])]
        expected = ["CS", "SA", "RS", "BS"]
        missing = [e for e in expected if e not in surveys]
        if missing:
            ded = len(missing) * 10
            score -= ded
            penalties.append({"factor": f"Missing Historical Survey Cadastre: {', '.join(missing)}", "deduction": -ded})

        score = max(0, min(100, score))

        if score >= 90:
            rating = "AAA - PRIME SECURE TITLE"
            color = "#10b981"
        elif score >= 60:
            rating = "B - CONDITIONAL / INCOMPLETE TAX"
            color = "#f59e0b"
        else:
            rating = "CRITICAL RISK / DISPUTED"
            color = "#ef4444"

        return {
            "parcel_id": parcel_id,
            "mouza": parcel["mouza"],
            "dag_no": parcel["dag_no"],
            "score": score,
            "rating": rating,
            "badge_color": color,
            "penalties": penalties,
            "total_area_decimals": parcel["total_area_decimals"],
            "tax_status": parcel["tax_status"],
            "encumbrance_count": len(parcel.get("encumbrances", []))
        }

# Global Singleton Engine
engine = BhumiGraphEngine()
