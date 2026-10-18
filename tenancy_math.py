"""
Tenancy Math Engine (১৬ আনা হিস্যা ও তিল রূপান্তর ইঞ্জিন)
Bespoke mathematical parser and fraud detection engine for historical
Bengal Tenancy land records (CS, SA, RS Khatians).
"""

from typing import Dict, Any, List, Tuple

# Base conversion factors for Bengal land accounting system:
# 1 Ana (আনা) = 20 Gondas (গণ্ডা)
# 1 Gonda (গণ্ডা) = 4 Koras (কড়া)
# 1 Kora (কড়া) = 3 Krantis (ক্রান্তি)
# 1 Kranti (ক্রান্তি) = 20 Tils (তিল)
# 1 Complete Whole (১৬ আনা) = 16 * 20 * 4 * 3 * 20 = 76,800 Tils

TIL_PER_KRANTI = 20
TIL_PER_KORA = 3 * TIL_PER_KRANTI       # 60
TIL_PER_GONDA = 4 * TIL_PER_KORA        # 240
TIL_PER_ANA = 20 * TIL_PER_GONDA        # 4,800
FULL_KHATIAN_TILS = 16 * TIL_PER_ANA    # 76,800

def to_bangla_digits(num_str: Any) -> str:
    """Converts English digits to Bangla numerals."""
    b_map = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', 
             '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯', '.': '.'}
    return "".join(b_map.get(c, c) for c in str(num_str))

def to_english_digits(num_str: Any) -> str:
    """Converts Bangla numerals to English digits."""
    e_map = {'০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', 
             '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'}
    return "".join(e_map.get(c, c) for c in str(num_str))

def calculate_share_tils(ana: float = 0, gonda: float = 0, kora: float = 0, kranti: float = 0, til: float = 0) -> float:
    """Calculates total normalized Tils for a given share."""
    return round(
        (ana * TIL_PER_ANA) + 
        (gonda * TIL_PER_GONDA) + 
        (kora * TIL_PER_KORA) + 
        (kranti * TIL_PER_KRANTI) + 
        til, 
        2
    )

def tils_to_ana_breakdown(total_tils: float) -> Dict[str, Any]:
    """Converts raw Tils back into standard Ana-Gonda-Kora-Kranti-Til representation."""
    rem = round(total_tils)
    ana = rem // TIL_PER_ANA
    rem %= TIL_PER_ANA
    
    gonda = rem // TIL_PER_GONDA
    rem %= TIL_PER_GONDA
    
    kora = rem // TIL_PER_KORA
    rem %= TIL_PER_KORA
    
    kranti = rem // TIL_PER_KRANTI
    til = rem % TIL_PER_KRANTI
    
    fraction_of_16 = round(total_tils / FULL_KHATIAN_TILS, 6)
    
    text_bn = f"{to_bangla_digits(ana)} আনা, {to_bangla_digits(gonda)} গণ্ডা, {to_bangla_digits(kora)} কড়া, {to_bangla_digits(kranti)} ক্রান্তি, {to_bangla_digits(round(til, 1))} তিল"
    
    return {
        "ana": int(ana),
        "gonda": int(gonda),
        "kora": int(kora),
        "kranti": int(kranti),
        "til": round(til, 2),
        "total_tils": total_tils,
        "fraction_of_total": fraction_of_16,
        "formatted_bn": text_bn
    }

def audit_khatian_math(owners: List[Dict[str, Any]], total_area_decimals: float = 0.0) -> Dict[str, Any]:
    """
    Performs rigorous 16-Ana mathematical verification across all extracted co-sharers.
    Identifies fraud (over-allocation), torn paper defects, and calculates precise decimal lands.
    """
    total_tils = 0.0
    processed_owners = []

    for idx, owner in enumerate(owners):
        ana = float(owner.get("ana", 0))
        gonda = float(owner.get("gonda", 0))
        kora = float(owner.get("kora", 0))
        kranti = float(owner.get("kranti", 0))
        til = float(owner.get("til", 0))

        owner_tils = calculate_share_tils(ana, gonda, kora, kranti, til)
        total_tils += owner_tils
        
        share_ratio = owner_tils / FULL_KHATIAN_TILS
        owner_decimals = round(share_ratio * total_area_decimals, 4) if total_area_decimals > 0 else 0.0

        processed_owners.append({
            "serial": idx + 1,
            "name": owner.get("name", ""),
            "father_spouse": owner.get("father_spouse", ""),
            "address": owner.get("address", ""),
            "ana": ana,
            "gonda": gonda,
            "kora": kora,
            "kranti": kranti,
            "til": til,
            "owner_tils": owner_tils,
            "share_percentage": round(share_ratio * 100, 2),
            "share_bn": tils_to_ana_breakdown(owner_tils)["formatted_bn"],
            "calculated_decimals": owner_decimals,
            "calculated_decimals_bn": to_bangla_digits(owner_decimals)
        })

    discrepancy_tils = round(total_tils - FULL_KHATIAN_TILS, 2)
    discrepancy_ratio = discrepancy_tils / FULL_KHATIAN_TILS
    discrepancy_decimals = round(discrepancy_ratio * total_area_decimals, 4) if total_area_decimals > 0 else 0.0

    # If no owners or shares could be read from blurry/torn document
    if len(processed_owners) == 0:
        return {
            "status": "UNDETECTED_OR_EMPTY",
            "status_bn": "তথ্য সনাক্ত করা যায়নি (Can't Find)",
            "badge_color": "bg-slate-700",
            "message_bn": "কাগজটি অত্যন্ত ঝাপসা, অস্পষ্ট বা ছেঁড়া হওয়ায় কোনো অংশীদারের হিস্যা সনাক্ত করা সম্ভব হয়নি (Can't Find)। অনুগ্রহ করে স্পষ্ট স্ক্যান কপি আপলোড করুন।",
            "total_tils": 0.0,
            "total_tils_bn": "০",
            "full_khatian_tils": FULL_KHATIAN_TILS,
            "full_khatian_tils_bn": to_bangla_digits(FULL_KHATIAN_TILS),
            "discrepancy_tils": 0.0,
            "discrepancy_tils_bn": "০",
            "discrepancy_decimals": 0.0,
            "discrepancy_decimals_bn": "০.০",
            "total_area_decimals": total_area_decimals,
            "total_area_decimals_bn": to_bangla_digits(total_area_decimals),
            "owners": []
        }

    # Classify verification outcome
    if abs(discrepancy_tils) < 0.1:
        status = "AUTHENTIC_PERFECT"
        status_bn = "সম্পূর্ণ নির্ভুল (১৬ আনা পূর্ণ)"
        badge_color = "bg-green-700"
        message_bn = (
            f"খতিয়ানের সকল অংশীদারের হিস্যা যোগ করে হুবহু ১৬ আনা ({to_bangla_digits(FULL_KHATIAN_TILS)} তিল) পাওয়া গেছে। "
            f"কোনো ধরনের গাণিতিক অসঙ্গতি বা জালিয়াতি সনাক্ত হয়নি।"
        )
    elif discrepancy_tils > 0:
        status = "FRAUD_OVERALLOCATION"
        status_bn = "জালিয়াতি সনাক্ত! (অতিরিক্ত হিস্যা বণ্টন)"
        badge_color = "bg-red-700"
        over_breakdown = tils_to_ana_breakdown(discrepancy_tils)["formatted_bn"]
        message_bn = (
            f"সতর্কতা: খতিয়ানের অংশীদারদের মোট হিস্যা ১৬ আনার বেশি ({to_bangla_digits(total_tils)} তিল)! "
            f"এখানে {over_breakdown} ({to_bangla_digits(discrepancy_decimals)} শতাংশ জমি) অবৈধভাবে অতিরিক্ত প্রদর্শন করা হয়েছে। "
            f"এটি নিশ্চিতভাবে ঘষামাজা, জাল এন্ট্রি বা অবৈধ অংশ বৃদ্ধির লক্ষণ।"
        )
    else:
        status = "DEFICIT_OR_TORN"
        status_bn = "অসম্পূর্ণ বা ছেঁড়া পাতা (হিস্যা ঘাটতি)"
        badge_color = "bg-amber-600"
        deficit_tils = abs(discrepancy_tils)
        deficit_breakdown = tils_to_ana_breakdown(deficit_tils)["formatted_bn"]
        message_bn = (
            f"সতর্কতা: খতিয়ানে মোট হিস্যার ঘাটতি রয়েছে। মোট হিস্যা ১৬ আনার চেয়ে {deficit_breakdown} "
            f"({to_bangla_digits(abs(discrepancy_decimals))} শতাংশ জমি) কম পাওয়া গেছে। "
            f"সম্ভাব্য কারণ: খতিয়ানের পাতা ছেঁড়া/অস্পষ্ট হওয়া, অথবা কোনো অংশীদারের নাম বেআইনিভাবে গোপন রাখা।"
        )

    return {
        "status": status,
        "status_bn": status_bn,
        "badge_color": badge_color,
        "message_bn": message_bn,
        "total_tils": total_tils,
        "expected_tils": FULL_KHATIAN_TILS,
        "discrepancy_tils": discrepancy_tils,
        "discrepancy_decimals": discrepancy_decimals,
        "discrepancy_decimals_bn": to_bangla_digits(abs(discrepancy_decimals)),
        "total_area_decimals": total_area_decimals,
        "total_area_decimals_bn": to_bangla_digits(total_area_decimals),
        "owners": processed_owners
    }
