"""
Digital Verification Registry Engine (নাগরিক ডিজিটাল ভূমি যাচাই ও নিরাপত্তা স্কোর ইঞ্জিন)
Simulates and evaluates:
1. সরকারি ১নং খাস, অর্পিত সম্পত্তি (Vested Property 'ক'/'খ' তফসিল) ও অধিগ্রহণ যাচাই
2. ব্যাংক বন্ধক, ঋণ দায় ও দায়মুক্তি সনদ (Bank Mortgage & Non-Encumbrance)
3. দেওয়ানি আদালতের মামলা, ইনজাংশন ও স্থিতাবস্থা (Court Injunction / Lis Pendens)
4. ভূমি উন্নয়ন কর (খাজনা) পরিশোধের হালনাগাদ তথ্য (Land Development Tax Clearance)
5. সামগ্রিক ভূমি নিরাপত্তা স্কোর (Land Safety Score: 0 - 100)
"""

from typing import Dict, Any, List
import hashlib
import time
from tenancy_math import to_bangla_digits

# Simulated National Digital Registry Database of Encumbrances, Khas Lands, Court Suits & Tax Records
MOCK_SECURITY_REGISTRY = {
    # Joydebpur, Gazipur (CS Dag 104 / RS 455 / BS 810) - Pure Private Land, Zero Encumbrance
    "810": {
        "dag_no": "810",
        "mouza": "জয়দেবপুর",
        "district": "গাজীপুর",
        "ownership_nature": "PRIVATE_JOT",
        "ownership_nature_bn": "সম্পূর্ণ ব্যক্তিগত রায়তী স্বত্ব (নিরাপদ)",
        "is_khas": False,
        "is_vested": False,
        "is_acquired": False,
        "khas_details_bn": "উক্ত দাগটি সরকারি ১নং খাস খতিয়ান, অর্পিত সম্পত্তি কিংবা অধিগ্রহণভুক্ত নয়।",
        
        "bank_mortgage": {
            "has_mortgage": False,
            "bank_name": "কোনো আর্থিক প্রতিষ্ঠানে বন্ধক নেই",
            "loan_amount_bdt": 0,
            "status_bn": "দায়মুক্ত (Non-Encumbered / কোনো লিয়েন নেই)"
        },
        
        "court_litigation": {
            "has_lawsuit": False,
            "case_type": "কোনো মামলা নেই",
            "court_name": "দেওয়ানি আদালতে কোনো মোকদ্দমা বিচারাধীন নেই",
            "status_bn": "মামলামুক্ত ও নিষ্কণ্টক"
        },
        
        "tax_record": {
            "is_paid": True,
            "last_paid_year_bn": "১৪৩১-১৪৩২ বঙ্গাব্দ",
            "receipt_no": "ই-দাখিলা-৯৯৮৭২/২০২৫",
            "arrears_bdt": 0,
            "status_bn": "ভূমি উন্নয়ন কর (খাজনা) সম্পূর্ণ হালনাগাদ পরিশোধিত"
        }
    },

    # Savar, Dhaka (Dag 302) - High Risk Plot: Injunction + Bank Mortgage
    "302": {
        "dag_no": "302",
        "mouza": "সাভার",
        "district": "ঢাকা",
        "ownership_nature": "DISPUTED_ENCUMBERED",
        "ownership_nature_bn": "বিতর্কিত ও দায়যুক্ত সম্পত্তি (উচ্চ ঝুঁকি)",
        "is_khas": False,
        "is_vested": False,
        "is_acquired": False,
        "khas_details_bn": "ব্যক্তিগত সম্পত্তি, তবে বিচারাধীন দেওয়ানি মোকদ্দমা ও ব্যাংকে দায়বদ্ধ।",
        
        "bank_mortgage": {
            "has_mortgage": True,
            "bank_name": "সোনালী ব্যাংক পিএলসি (সাভার শাখা)",
            "loan_amount_bdt": 4500000,
            "status_bn": "সক্রিয় বন্ধকযুক্ত (৪৫,০০,০০০/- টাকা ঋণ দায়বদ্ধ)"
        },
        
        "court_litigation": {
            "has_lawsuit": True,
            "case_type": "স্বত্ব মোকদ্দমা ও স্থিতাবস্থা (Title Suit & Status Quo)",
            "court_name": "বিজ্ঞ ৩য় যুগ্ম জেলা জজ আদালত, ঢাকা (মোকদ্দমা নং ১৪২/২০২৫)",
            "status_bn": "আদালত কর্তৃক জমি হস্তান্তর ও নামজারির উপর নিষেধাজ্ঞা বলবৎ রয়েছে"
        },
        
        "tax_record": {
            "is_paid": False,
            "last_paid_year_bn": "১৪২৯ বঙ্গাব্দ",
            "receipt_no": "বকেয়া",
            "arrears_bdt": 12850,
            "status_bn": "৩ বছরের ভূমি উন্নয়ন কর বকেয়া (১২,৮৫০/- টাকা খেলাপি)"
        }
    },

    # Default / Unknown Plot Template
    "DEFAULT": {
        "ownership_nature": "PRIVATE_JOT",
        "ownership_nature_bn": "ব্যক্তিগত রায়তী স্বত্ব",
        "is_khas": False,
        "is_vested": False,
        "is_acquired": False,
        "khas_details_bn": "সরকারি ১নং খাস বা অর্পিত সম্পত্তি তালিকায় কোনো রেকর্ড পাওয়া যায়নি।",
        "bank_mortgage": {
            "has_mortgage": False,
            "bank_name": "কোনো আর্থিক প্রতিষ্ঠানে বন্ধক নেই",
            "loan_amount_bdt": 0,
            "status_bn": "দায়মুক্ত (কোনো সক্রিয় ব্যাংক লিয়েন নেই)"
        },
        "court_litigation": {
            "has_lawsuit": False,
            "case_type": "কোনো সক্রিয় মামলা নেই",
            "court_name": "দেওয়ানি আদালতে কোনো ইনজাংশন রেকর্ড নেই",
            "status_bn": "মামলামুক্ত"
        },
        "tax_record": {
            "is_paid": True,
            "last_paid_year_bn": "১৪৩১ বঙ্গাব্দ",
            "receipt_no": "ই-দাখিলা-চলতি সন",
            "arrears_bdt": 0,
            "status_bn": "ভূমি উন্নয়ন কর হালনাগাদ"
        }
    }
}

def verify_land_safety(dag_no: str, mouza: str = "", district: str = "", math_status: str = "AUTHENTIC_PERFECT") -> Dict[str, Any]:
    """
    Executes the 4-Pillar Citizen Land Safety Audit and computes the composite Land Safety Score (0-100).
    Pillars:
    1. Khas / Vested / State Acquisition Check
    2. Bank Mortgage & Encumbrance Check
    3. Court Injunction & Lis Pendens Check
    4. Land Development Tax (Khajna) Clearance
    """
    # Normalize Dag number
    clean_dag = str(dag_no).replace("দাগ", "").replace("নং", "").strip()
    clean_dag = "".join({'০':'0','১':'1','২':'2','৩':'3','৪':'4','৫':'5','৬':'6','৭':'7','৮':'8','৯':'9'}.get(c, c) for c in clean_dag)

    record = MOCK_SECURITY_REGISTRY.get(clean_dag, MOCK_SECURITY_REGISTRY["DEFAULT"])

    score = 100
    risk_factors = []
    safety_points = []

    # 1. Math Authenticity check (-40 if 16-Ana math has fraud)
    if math_status == "FRAUD_OVERALLOCATION":
        score -= 40
        risk_factors.append({
            "pillar": "খতিয়ানের গাণিতিক সততা",
            "deduction": "-৪০ নম্বর",
            "severity": "CRITICAL",
            "title": "১৬ আনা হিস্যা জালিয়াতি সনাক্ত",
            "desc": "খতিয়ানের কাগজে অতিরিক্ত জমি প্রদর্শন করে ১৬ আনার গাণিতিক ভারসাম্য নষ্ট করা হয়েছে।"
        })
    elif math_status == "DEFICIT_OR_TORN":
        score -= 15
        risk_factors.append({
            "pillar": "খতিয়ানের গাণিতিক সততা",
            "deduction": "-১৫ নম্বর",
            "severity": "MEDIUM",
            "title": "ছেঁড়া পাতা বা অংশীদার বাদ পড়ার শঙ্কা",
            "desc": "খতিয়ানে ১৬ আনা পূর্ণ হয়নি, হিস্যায় ঘাটতি রয়েছে।"
        })
    else:
        safety_points.append("খতিয়ানের ১৬ আনা হিস্যা ও স্বত্ব গাণিতিকভাবে শতভাগ নির্ভুল।")

    # 2. Khas & Vested check (-50 if government property)
    if record["is_khas"] or record["is_vested"]:
        score -= 50
        risk_factors.append({
            "pillar": "সরকারি স্বত্ব ও খাস জমি",
            "deduction": "-৫০ নম্বর",
            "severity": "CRITICAL",
            "title": "সরকারি ১নং খাস বা অর্পিত সম্পত্তি",
            "desc": "উক্ত দাগের জমি ব্যক্তি নামে হস্তান্তরযোগ্য নয়। সরকারি জমিতে ক্রয়-বিক্রয় নিষিদ্ধ।"
        })
    else:
        safety_points.append("উক্ত জমি সরকারি ১নং খাস, অর্পিত বা অধিগ্রহণ তালিকার বাইরে সম্পূর্ণ ব্যক্তিগত সম্পত্তি।")

    # 3. Bank Mortgage check (-30 if mortgaged)
    if record["bank_mortgage"]["has_mortgage"]:
        score -= 30
        risk_factors.append({
            "pillar": "ব্যাংক দায় ও বন্ধক স্ট্যাটাস",
            "deduction": "-৩০ নম্বর",
            "severity": "HIGH",
            "title": "আর্থিক প্রতিষ্ঠানে বন্ধকযুক্ত",
            "desc": f"{record['bank_mortgage']['bank_name']}-এ ঋণ গ্রহণের বিপরীতে জমিটি দায়বদ্ধ রয়েছে।"
        })
    else:
        safety_points.append("কোনো তফসিলি ব্যাংক বা আর্থিক প্রতিষ্ঠানে ঋণ দায় বা বন্ধক নেই (দায়মুক্ত সম্পত্তি)।")

    # 4. Court litigation & injunction check (-35 if injunction active)
    if record["court_litigation"]["has_lawsuit"]:
        score -= 35
        risk_factors.append({
            "pillar": "আদালতের নিষেধাজ্ঞা ও মামলা",
            "deduction": "-৩৫ নম্বর",
            "severity": "CRITICAL",
            "title": "আদালতের স্থিতাবস্থা (Status Quo) বলবৎ",
            "desc": f"{record['court_litigation']['court_name']} কর্তৃক জমি হস্তান্তর ও নামজারিতে নিষেধাজ্ঞা আরোপিত আছে।"
        })
    else:
        safety_points.append("দেওয়ানি বা ফৌজদারি আদালতে কোনো প্রকার মামলা বা নিষেধাজ্ঞা নেই (নিষ্কণ্টক জমি)।")

    # 5. Tax record check (-10 if unpaid)
    if not record["tax_record"]["is_paid"]:
        score -= 10
        risk_factors.append({
            "pillar": "ভূমি উন্নয়ন কর (খাজনা)",
            "deduction": "-১০ নম্বর",
            "severity": "LOW",
            "title": "ভূমি উন্নয়ন কর বকেয়া",
            "desc": f"সর্বশেষ কর {record['tax_record']['last_paid_year_bn']}-এ পরিশোধিত। বকেয়া পরিশোধ করতে হবে।"
        })
    else:
        safety_points.append(f"ভূমি উন্নয়ন কর (খাজনা) সম্পূর্ণ হালনাগাদ পরিশোধিত ({record['tax_record']['last_paid_year_bn']})।")

    score = max(0, min(100, score))

    # Rating determination
    if score >= 85:
        rating_bn = "গ্রিন ক্যাটাগরি — নিরাপদ ও নিষ্কণ্টক জমি (ক্রয়যোগ্য)"
        color_class = "text-emerald-700 bg-emerald-50 border-emerald-300"
        badge_bg = "bg-emerald-600"
        recommendation_bn = "জমিটি আইনগতভাবে নিষ্কণ্টক, দায়মুক্ত এবং ক্রয় বা নামজারির জন্য সম্পূর্ণ নিরাপদ।"
    elif score >= 50:
        rating_bn = "হলুদ ক্যাটাগরি — সতর্কতামূলক পর্যবেক্ষণ প্রয়োজন"
        color_class = "text-amber-800 bg-amber-50 border-amber-300"
        badge_bg = "bg-amber-600"
        recommendation_bn = "জমিতে কর বকেয়া বা আংশিক নথির ঘাটতি রয়েছে। ক্রয় করার পূর্বে কাগজপত্র যাচাই ও বকেয়া পরিশোধ প্রয়োজন।"
    else:
        rating_bn = "রেড ক্যাটাগরি — উচ্চ ঝুঁকিপূর্ণ / বিতর্কিত জমি (লেনদেন ঝুঁকিপূর্ণ)"
        color_class = "text-red-800 bg-red-50 border-red-300"
        badge_bg = "bg-red-700"
        recommendation_bn = "সতর্কতা: এই জমিতে আদালতের নিষেধাজ্ঞা, ব্যাংক বন্ধক অথবা খতিয়ানের গুরুতর জালিয়াতি সনাক্ত হয়েছে। কোনো প্রকার বায়নানামা বা লেনদেন করবেন না।"

    cert_hash = hashlib.sha256(f"{dag_no}:{mouza}:{score}:{time.time()}".encode()).hexdigest().upper()

    return {
        "dag_no": dag_no,
        "score": score,
        "score_bn": to_bangla_digits(score),
        "rating_bn": rating_bn,
        "badge_bg": badge_bg,
        "color_class": color_class,
        "recommendation_bn": recommendation_bn,
        "ownership_nature_bn": record["ownership_nature_bn"],
        "khas_record": {
            "status_bn": "ব্যক্তিগত সম্পত্তি" if not (record["is_khas"] or record["is_vested"]) else "সরকারি খাস/অর্পিত জমি",
            "details_bn": record["khas_details_bn"],
            "is_safe": not (record["is_khas"] or record["is_vested"])
        },
        "bank_record": {
            "status_bn": record["bank_mortgage"]["status_bn"],
            "bank_name": record["bank_mortgage"]["bank_name"],
            "is_safe": not record["bank_mortgage"]["has_mortgage"]
        },
        "court_record": {
            "status_bn": record["court_litigation"]["status_bn"],
            "court_name": record["court_litigation"]["court_name"],
            "is_safe": not record["court_litigation"]["has_lawsuit"]
        },
        "tax_record": {
            "status_bn": record["tax_record"]["status_bn"],
            "receipt_no": record["tax_record"]["receipt_no"],
            "is_safe": record["tax_record"]["is_paid"]
        },
        "risk_factors": risk_factors,
        "safety_points": safety_points,
        "verification_hash": cert_hash
    }
