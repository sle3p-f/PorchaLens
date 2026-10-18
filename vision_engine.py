"""
Vision Engine (হস্তলিখিত খতিয়ান ও পরচা ভিশন এআই প্রসেসর)
Uses Gemini 3.5 Flash Multimodal Vision API to parse handwritten & printed
Bengali land tenancy records into structured data.
"""

import os
import json
import base64
import requests
from typing import Dict, Any
from tenancy_math import audit_khatian_math, to_english_digits

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6J6i-qxlF8lRmitO_V73zIH2MORZTG1McI-6YvWsECi6g")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"

VISION_SYSTEM_PROMPT = """
You are an expert Bengali Land Records Paleographer and Cadastral Surveyor specializing in historical Bengal Tenancy Khatians (CS, SA, RS, and BS Porchas).
Your task is to analyze the provided image of an authentic handwritten or printed Bengali land record (খতিয়ান / পরচা) and extract all administrative and ownership data with maximum precision.

CRITICAL EXTRACTION GUIDELINES FOR BENGALI LAND RECORDS:
1. Administrative Header:
   - Identify: খতিয়ান ধরন (CS / SA / RS / BS / নামজারি)
   - জেলা (District), থানা/উপজেলা (Upazila/Police Station), মৌজা (Mouza), জে.এল. নং (J.L. No.)
   - খতিয়ান নং (Khatian Number), দাগ নং (Dag Numbers)
   - মোট জমির পরিমাণ (Total area in decimals/শতাংশ or acres/একর)
   - জমির শ্রেণী (Land class, e.g. নাল, ভিটি, পুকুর, বাড়ি, পতিত)

2. Co-Sharer / Owner Table (মালিক ও অংশীদারদের তালিকা):
   For each recorded owner/co-sharer, extract:
   - name: পুরো নাম (বাংলায়)
   - father_spouse: পিতা বা স্বামীর নাম
   - address: বাসস্থান / ঠিকানা (যদি থাকে)
   - Share / অংশ (খতিয়ানের অংশ বা হিস্যা):
     Historical Khatians record shares in Ana (আনা), Gonda (গণ্ডা), Kora (কড়া), Kranti (ক্রান্তি), and Til (তিল).
     - 1 Khatian = 16 Anas total.
     - Extract the numeric integer/float values for:
       - ana: আনা (0 to 16)
       - gonda: গণ্ডা (0 to 19)
       - kora: কড়া (0 to 3)
       - kranti: ক্রান্তি (0 to 2)
       - til: তিল (0 to 19.99)
     Note: In Bengali notation, slashes/dashes indicate Anas:
     - '/' = ১ আনা (1 Ana)
     - '//' = ২ আনা (2 Anas)
     - '///' = ৩ আনা (3 Anas)
     - '|' = ৪ আনা (4 Anas বা ১ চৌকা)
     - '।' = ১ আনা বা ৪ আনা প্রতীক
     Translate archaic symbols faithfully into numeric values.
     If a value is not explicitly present, set it to 0.

OUTPUT FORMAT:
Return strictly a valid JSON object matching this schema without any markdown formatting or surrounding backticks:
{
  "khatian_type": "CS / SA / RS / BS",
  "district": "জেলার নাম",
  "upazila": "উপজেলার নাম",
  "mouza": "মৌজার নাম",
  "jl_no": "জে.এল. নম্বর",
  "khatian_no": "খতিয়ান নম্বর",
  "dag_numbers": ["দাগ ১", "দাগ ২"],
  "land_class": "জমির শ্রেণী",
  "total_area_decimals": 0.0,
  "confidence_score": 95,
  "handwriting_quality": "স্পষ্ট / কিছুটা অস্পষ্ট / জীর্ণ বা ছেঁড়া",
  "owners": [
    {
      "name": "মালিকের নাম",
      "father_spouse": "পিতা/স্বামীর নাম",
      "address": "গ্রাম/ঠিকানা",
      "ana": 8,
      "gonda": 0,
      "kora": 0,
      "kranti": 0,
      "til": 0
    }
  ]
}
"""

def extract_and_verify_khatian(image_bytes: bytes, mime_type: str = "image/jpeg") -> Dict[str, Any]:
    """
    Takes raw image bytes of a Khatian, performs multimodal vision extraction via Gemini 3.5 Flash,
    and runs symbolic 16-Ana math verification.
    """
    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": VISION_SYSTEM_PROMPT},
                    {"text": "Analyze this Bengali Khatian / Porcha image and return strictly the structured JSON data as specified:"},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": b64_image
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1
        }
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, timeout=45)
        if response.status_code != 200:
            return {
                "success": False,
                "error_bn": f"এআই ভিশন সার্ভিস ত্রুটি ({response.status_code}): {response.text[:200]}"
            }
        
        resp_json = response.json()
        raw_text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
        
        # Parse JSON
        parsed_data = json.loads(raw_text)
        
        # Clean numeric fields
        try:
            total_area = float(to_english_digits(parsed_data.get("total_area_decimals", 0.0)))
        except (ValueError, TypeError):
            total_area = 0.0
            
        parsed_data["total_area_decimals"] = total_area
        
        # Run Mathematical Verification Engine
        math_audit = audit_khatian_math(
            owners=parsed_data.get("owners", []),
            total_area_decimals=total_area
        )
        
        return {
            "success": True,
            "metadata": {
                "khatian_type": parsed_data.get("khatian_type", "CS/SA"),
                "district": parsed_data.get("district", "অজ্ঞাত"),
                "upazila": parsed_data.get("upazila", "অজ্ঞাত"),
                "mouza": parsed_data.get("mouza", "অজ্ঞাত"),
                "jl_no": parsed_data.get("jl_no", ""),
                "khatian_no": parsed_data.get("khatian_no", ""),
                "dag_numbers": parsed_data.get("dag_numbers", []),
                "land_class": parsed_data.get("land_class", "নাল"),
                "confidence_score": parsed_data.get("confidence_score", 90),
                "handwriting_quality": parsed_data.get("handwriting_quality", "স্বাভাবিক")
            },
            "math_audit": math_audit
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error_bn": "ইমেজ প্রসেসিংয়ে অতিরিক্ত সময় লেগেছে। দয়া করে ইমেজ সাইজ ছোট করে পুনরায় চেষ্টা করুন।"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error_bn": f"এআই আউটপুট পার্স করতে ব্যর্থ হয়েছে: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error_bn": f"অপ্রত্যাশিত ত্রুটি ঘটেছে: {str(e)}"
        }
