"""
Vision Engine (হস্তলিখিত খতিয়ান ও পরচা ভিশন এআই প্রসেসর)
Uses Gemini Vision API with automatic multi-model fallback to bypass 429 quota limits.
"""

import os
import json
import base64
import requests
from typing import Dict, Any
from tenancy_math import audit_khatian_math, to_english_digits

def _load_env_file():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() not in os.environ:
                            os.environ[k.strip()] = v.strip()
        except Exception:
            pass

_load_env_file()
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Models ordered by quota availability and speed (Flash-Lite has higher free-tier quota)
CANDIDATE_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash"
]

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

def extract_and_verify_khatian(image_bytes: bytes, mime_type: str = "image/jpeg", custom_api_key: str = None) -> Dict[str, Any]:
    """
    Takes raw image bytes of a Khatian, performs multimodal vision extraction via Gemini API,
    with automatic model fallback to avoid 429 quota exhaustion.
    """
    api_key = custom_api_key or os.environ.get("GEMINI_API_KEY", DEFAULT_API_KEY)
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

    last_error = ""

    # Iterate through models with fallback
    for model_name in CANDIDATE_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            response = requests.post(url, json=payload, timeout=40)
            
            # If 429 rate-limited, silently fallback to the next model
            if response.status_code == 429:
                last_error = f"{model_name} মডেলের কোটা পূর্ণ (429 Rate Limit)"
                continue
                
            if response.status_code != 200:
                last_error = f"{model_name} ত্রুটি ({response.status_code}): {response.text[:150]}"
                continue

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
                "model_used": model_name,
                "metadata": {
                    "khatian_type": parsed_data.get("khatian_type", "CS/SA"),
                    "district": parsed_data.get("district", "অজ্ঞাত"),
                    "upazila": parsed_data.get("upazila", "অজ্ঞাত"),
                    "mouza": parsed_data.get("mouza", "অজ্ঞাত"),
                    "jl_no": parsed_data.get("jl_no", ""),
                    "khatian_no": parsed_data.get("khatian_no", ""),
                    "dag_numbers": parsed_data.get("dag_numbers", []),
                    "land_class": parsed_data.get("land_class", "নাল"),
                    "confidence_score": parsed_data.get("confidence_score", 92),
                    "handwriting_quality": parsed_data.get("handwriting_quality", "স্বাভাবিক")
                },
                "math_audit": math_audit
            }

        except requests.exceptions.Timeout:
            last_error = f"{model_name} টাইমআউট হয়েছে"
            continue
        except json.JSONDecodeError as e:
            last_error = f"{model_name} আউটপুট পার্স করতে ব্যর্থ: {str(e)}"
            continue
        except Exception as e:
            last_error = f"{model_name} ত্রুটি: {str(e)}"
            continue

    # If all models failed or were quota limited
    return {
        "success": False,
        "error_bn": f"এআই সার্ভারের সকল মডেলের কোটা সাময়িকভাবে পূর্ণ ({last_error})। অনুগ্রহ করে ১ মিনিট পর আবার চেষ্টা করুন অথবা বিকল্প API কী ব্যবহার করুন।"
    }
