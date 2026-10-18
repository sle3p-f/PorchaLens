"""
Faraiz Inheritance Calculation Engine (ফারায়েজ ও মুসলিম উত্তরাধিকার আইন ক্যালকুলেটর)
Implements:
1. Muslim Family Laws Ordinance 1961 (Faraiz Rules)
2. Exact Quranic Fixed Shares (Zawil Furud) and Residuaries (Asabah)
3. Dynamic allocation of ancestral land decimals to modern surviving heirs
4. Red alert flag for Female Heir (Sisters/Daughters/Mothers) Disinheritance
"""

from typing import Dict, Any, List
from tenancy_math import to_bangla_digits

def calculate_faraiz_distribution(
    deceased_name: str,
    total_area_decimals: float,
    num_wives: int = 1,
    num_sons: int = 2,
    num_daughters: int = 1,
    has_father: bool = False,
    has_mother: bool = False
) -> Dict[str, Any]:
    """
    Calculates exact legal inheritance shares under Bangladesh Muslim Succession Law.
    - Wives get 1/8 (12.5%) if there are children; 1/4 if no children.
    - Mother gets 1/6 (16.67%) if children exist.
    - Father gets 1/6 (16.67%) if children exist.
    - Remaining residue (Asabah) is split between Sons and Daughters in a 2:1 ratio.
    """
    if total_area_decimals <= 0:
        total_area_decimals = 10.0  # default fallback

    has_children = (num_sons + num_daughters) > 0
    heir_breakdown = []
    consumed_fraction = 0.0

    # 1. Wives (স্ত্রী)
    if num_wives > 0:
        wife_total_share = 0.125 if has_children else 0.250  # 1/8 or 1/4
        share_per_wife = wife_total_share / num_wives
        consumed_fraction += wife_total_share
        for i in range(num_wives):
            area = round(share_per_wife * total_area_decimals, 4)
            heir_breakdown.append({
                "relation_bn": f"স্ত্রী {to_bangla_digits(i+1)}" if num_wives > 1 else "স্ত্রী",
                "gender": "FEMALE",
                "share_fraction": round(share_per_wife, 6),
                "share_percentage": round(share_per_wife * 100, 2),
                "quranic_rule": "১/৮ অংশ (সন্তান থাকায়)",
                "allocated_decimals": area,
                "allocated_decimals_bn": to_bangla_digits(area)
            })

    # 2. Mother (মাতা)
    if has_mother:
        mother_share = 0.166667 if has_children else 0.333333  # 1/6 or 1/3
        consumed_fraction += mother_share
        area = round(mother_share * total_area_decimals, 4)
        heir_breakdown.append({
            "relation_bn": "মাতা",
            "gender": "FEMALE",
            "share_fraction": round(mother_share, 6),
            "share_percentage": round(mother_share * 100, 2),
            "quranic_rule": "১/৬ অংশ (সন্তান থাকায়)",
            "allocated_decimals": area,
            "allocated_decimals_bn": to_bangla_digits(area)
        })

    # 3. Father (পিতা)
    if has_father:
        father_share = 0.166667  # 1/6
        consumed_fraction += father_share
        area = round(father_share * total_area_decimals, 4)
        heir_breakdown.append({
            "relation_bn": "পিতা",
            "gender": "MALE",
            "share_fraction": round(father_share, 6),
            "share_percentage": round(father_share * 100, 2),
            "quranic_rule": "১/৬ অংশ (সন্তান থাকায়)",
            "allocated_decimals": area,
            "allocated_decimals_bn": to_bangla_digits(area)
        })

    # 4. Residue (অবশিষ্ট সম্পত্তি - আসাবা) for Sons and Daughters
    residue_fraction = max(0.0, 1.0 - consumed_fraction)
    
    if num_sons > 0 or num_daughters > 0:
        # Son gets 2 shares, Daughter gets 1 share
        total_parts = (num_sons * 2) + (num_daughters * 1)
        part_fraction = residue_fraction / total_parts if total_parts > 0 else 0

        # Sons (পুত্র)
        for i in range(num_sons):
            son_share = part_fraction * 2
            area = round(son_share * total_area_decimals, 4)
            heir_breakdown.append({
                "relation_bn": f"পুত্র {to_bangla_digits(i+1)}" if num_sons > 1 else "একমাত্র পুত্র",
                "gender": "MALE",
                "share_fraction": round(son_share, 6),
                "share_percentage": round(son_share * 100, 2),
                "quranic_rule": "আসাবা (পুত্রের অংশ কন্যার দ্বিগুণ - ২:১)",
                "allocated_decimals": area,
                "allocated_decimals_bn": to_bangla_digits(area)
            })

        # Daughters (কন্যা)
        for i in range(num_daughters):
            daughter_share = part_fraction * 1
            area = round(daughter_share * total_area_decimals, 4)
            heir_breakdown.append({
                "relation_bn": f"কন্যা {to_bangla_digits(i+1)}" if num_daughters > 1 else "একমাত্র কন্যা",
                "gender": "FEMALE",
                "share_fraction": round(daughter_share, 6),
                "share_percentage": round(daughter_share * 100, 2),
                "quranic_rule": "আসাবা (কন্যার অংশ পুত্রের অর্ধেক - ১:২)",
                "allocated_decimals": area,
                "allocated_decimals_bn": to_bangla_digits(area)
            })

    total_allocated_decimals = round(sum(h["allocated_decimals"] for h in heir_breakdown), 4)

    # Female protection check
    female_heirs = [h for h in heir_breakdown if h["gender"] == "FEMALE"]
    female_total_decimals = round(sum(h["allocated_decimals"] for h in female_heirs), 4)

    return {
        "deceased_name": deceased_name,
        "ancestral_land_decimals": total_area_decimals,
        "ancestral_land_decimals_bn": to_bangla_digits(total_area_decimals),
        "total_heirs_count": len(heir_breakdown),
        "heirs": heir_breakdown,
        "female_protection": {
            "female_heir_count": len(female_heirs),
            "female_total_decimals_bn": to_bangla_digits(female_total_decimals),
            "alert_bn": f"আইনত নারী ওয়ারিশদের মোট {to_bangla_digits(female_total_decimals)} শতাংশ জমি প্রাপ্য। এই জমি বাদ দিয়ে কোনো পুরুষ ওয়ারিশ একা জমি বিক্রি বা নামজারি করতে পারবে না।"
        }
    }
