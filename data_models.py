"""
BhumiGraph - Data Models and Dummy Datasets for LandTech 2026
Contains legally accurate, synthetic land administration records
in compliance with hackathon rules (no real personal or land data).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import datetime

@dataclass
class Owner:
    nid: str
    name: str
    father_name: str
    gender: str
    share_fraction: float  # Fraction of parcel owned (0.0 to 1.0)
    acquired_via: str      # 'INHERITANCE', 'DEED_PURCHASE', 'STATE_ALLOTMENT'
    acquired_date: str
    khatian_no: str

@dataclass
class Encumbrance:
    encumbrance_type: str  # 'BANK_MORTGAGE', 'COURT_INJUNCTION', 'LA_ACQUISITION'
    institution: str
    reference_no: str
    status: str            # 'ACTIVE', 'RELEASED'
    date_imposed: str
    details: str

@dataclass
class SurveyNode:
    survey_type: str       # 'CS', 'SA', 'RS', 'BS'
    dag_no: str
    khatian_no: str
    recorded_year: int
    total_area_decimals: float
    mouza: str
    district: str
    recorded_owners: List[str]

# ==============================================================================
# SYNTHETIC SCENARIO DATASETS
# ==============================================================================

PARCELS_DB = {
    # -------------------------------------------------------------------------
    # SCENARIO 1: The Inherited Share Depletion & Sister Concealment Case
    # Mouza: Joydebpur, Gazipur | BS Dag 810 (Derived from RS 455 -> SA 212 -> CS 104)
    # Story: Father (Late Rahim Uddin) left 20 decimals. Left 2 sons, 1 daughter.
    # By Faraiz: Sons get 8 decimals each, Daughter gets 4 decimals.
    # Son 1 (Tariqul) already sold 5 decimals in 2024. Remaining: 3 decimals.
    # Tariqul now tries to sell 10 decimals to an unsuspecting buyer by pretending
    # he owns 50% (10 decimals) and completely concealing his sister Fatima!
    # -------------------------------------------------------------------------
    "BS-810": {
        "id": "BS-810",
        "mouza": "Joydebpur",
        "upazila": "Gazipur Sadar",
        "district": "Gazipur",
        "jl_no": "42",
        "current_survey": "BS",
        "dag_no": "810",
        "khatian_no": "1042",
        "total_area_decimals": 20.0,
        "tax_status": "PAID_UP_TO_DATE",
        "last_tax_year": "1432 BS",
        
        # Historical Survey Chain
        "lineage": [
            {
                "survey_type": "CS",
                "dag_no": "104",
                "khatian_no": "12",
                "year": 1928,
                "recorded_owners": ["Kafil Uddin Sarkar (Deceased)"],
                "area_decimals": 20.0
            },
            {
                "survey_type": "SA",
                "dag_no": "212",
                "khatian_no": "88",
                "year": 1962,
                "recorded_owners": ["Rahim Uddin Sarkar (Deceased)"],
                "area_decimals": 20.0
            },
            {
                "survey_type": "RS",
                "dag_no": "455",
                "khatian_no": "310",
                "year": 1985,
                "recorded_owners": ["Rahim Uddin Sarkar (Deceased)"],
                "area_decimals": 20.0
            },
            {
                "survey_type": "BS",
                "dag_no": "810",
                "khatian_no": "1042",
                "year": 2012,
                "recorded_owners": [
                    "Tariqul Islam (Son)",
                    "Rafiqul Islam (Son)",
                    "Fatima Begum (Daughter - Legally Entitled)"
                ],
                "area_decimals": 20.0
            }
        ],
        
        # Authentic Legal Faraiz Split of Late Rahim Uddin (2 Sons, 1 Daughter = 5 shares total)
        # Each Son: 2/5 (40% = 8.0 decimals)
        # Daughter: 1/5 (20% = 4.0 decimals)
        "faraiz_profile": {
            "deceased_parent": "Late Rahim Uddin Sarkar",
            "date_of_death": "2018-04-12",
            "heirs": [
                {"nid": "1988-9901-01", "name": "Tariqul Islam", "relation": "SON", "legal_share_fraction": 0.40, "legal_area": 8.0},
                {"nid": "1992-9901-02", "name": "Rafiqul Islam", "relation": "SON", "legal_share_fraction": 0.40, "legal_area": 8.0},
                {"nid": "1995-9901-03", "name": "Fatima Begum", "relation": "DAUGHTER", "legal_share_fraction": 0.20, "legal_area": 4.0}
            ]
        },
        
        # Past completed transfers
        "completed_transfers": [
            {
                "deed_no": "Dalil-4091/2024",
                "date": "2024-02-15",
                "seller_nid": "1988-9901-01",
                "seller_name": "Tariqul Islam",
                "buyer_name": "Abul Kashem",
                "transferred_area_decimals": 5.0,
                "sub_registry": "Gazipur Sadar Sub-Registry",
                "mutation_khatian": "Namjari-881/2024"
            }
        ],
        
        # Active Encumbrances
        "encumbrances": []
    },

    # -------------------------------------------------------------------------
    # SCENARIO 2: The Injunction & Bank Double-Mortgage Case
    # Mouza: Savar, Dhaka | BS Dag 302
    # Story: Owner has an active Court Injunction (Status Quo) from Dhaka Civil Court
    # AND plot is already mortgaged to Rupali Bank.
    # -------------------------------------------------------------------------
    "BS-302": {
        "id": "BS-302",
        "mouza": "Savar",
        "upazila": "Savar",
        "district": "Dhaka",
        "jl_no": "18",
        "current_survey": "BS",
        "dag_no": "302",
        "khatian_no": "450",
        "total_area_decimals": 15.0,
        "tax_status": "DEFAULTER_3_YEARS",
        "last_tax_year": "1429 BS",
        
        "lineage": [
            {"survey_type": "CS", "dag_no": "44", "khatian_no": "09", "year": 1925, "recorded_owners": ["Mohesh Chandra (Deceased)"], "area_decimals": 15.0},
            {"survey_type": "SA", "dag_no": "110", "khatian_no": "52", "year": 1960, "recorded_owners": ["Nurul Huda"], "area_decimals": 15.0},
            {"survey_type": "RS", "dag_no": "201", "khatian_no": "180", "year": 1988, "recorded_owners": ["Nurul Huda"], "area_decimals": 15.0},
            {"survey_type": "BS", "dag_no": "302", "khatian_no": "450", "year": 2015, "recorded_owners": ["Kamal Hossain"], "area_decimals": 15.0}
        ],
        
        "faraiz_profile": None,
        
        "completed_transfers": [],
        
        "encumbrances": [
            {
                "encumbrance_type": "COURT_INJUNCTION",
                "institution": "Dhaka 3rd Joint District Judge Court",
                "reference_no": "Title Suit No. 142/2025",
                "status": "ACTIVE_STATUS_QUO",
                "date_imposed": "2025-08-11",
                "details": "Temporary injunction restraining alienation, mutation, and construction on Dag 302."
            },
            {
                "encumbrance_type": "BANK_MORTGAGE",
                "institution": "Sonali Bank PLC (Savar Branch)",
                "reference_no": "Mtg-Reg-774/2023",
                "status": "ACTIVE_LIEN",
                "date_imposed": "2023-11-20",
                "details": "Registered Equitable Mortgage against loan BDT 45,00,000/-"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SCENARIO 3: The Flawless, Clean Title Plot (100% Verified)
    # Mouza: Dhanmondi, Dhaka | BS Dag 1104
    # Story: Fully unbroken chain, zero encumbrances, fully mutated, all taxes paid.
    # -------------------------------------------------------------------------
    "BS-1104": {
        "id": "BS-1104",
        "mouza": "Dhanmondi",
        "upazila": "Dhanmondi",
        "district": "Dhaka",
        "jl_no": "04",
        "current_survey": "BS",
        "dag_no": "1104",
        "khatian_no": "2291",
        "total_area_decimals": 10.0,
        "tax_status": "PAID_UP_TO_DATE",
        "last_tax_year": "1433 BS",
        
        "lineage": [
            {"survey_type": "CS", "dag_no": "15", "khatian_no": "03", "year": 1922, "recorded_owners": ["A. R. Khan (Deceased)"], "area_decimals": 10.0},
            {"survey_type": "SA", "dag_no": "45", "khatian_no": "19", "year": 1958, "recorded_owners": ["Dr. M. A. Jalil"], "area_decimals": 10.0},
            {"survey_type": "RS", "dag_no": "310", "khatian_no": "904", "year": 1984, "recorded_owners": ["Dr. M. A. Jalil"], "area_decimals": 10.0},
            {"survey_type": "BS", "dag_no": "1104", "khatian_no": "2291", "year": 2011, "recorded_owners": ["Tahmina Chowdhury"], "area_decimals": 10.0}
        ],
        
        "faraiz_profile": None,
        "completed_transfers": [
            {
                "deed_no": "Dalil-9901/2018",
                "date": "2018-09-04",
                "seller_nid": "1970-1200-88",
                "seller_name": "Dr. M. A. Jalil",
                "buyer_name": "Tahmina Chowdhury",
                "transferred_area_decimals": 10.0,
                "sub_registry": "Dhanmondi Sub-Registry",
                "mutation_khatian": "Namjari-2291/2018"
            }
        ],
        "encumbrances": []
    }
}
