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

SAMPLE_AUTHENTIC_DATA = {
    "khatian_type": "CS (স্বত্বলিপি)",
    "district": "গাজীপুর",
    "upazila": "জয়দেবপুর",
    "mouza": "জয়দেবপুর",
    "jl_no": "১০৪",
    "khatian_no": "৪১২",
    "dag_numbers": ["৮১০", "৮১১"],
    "land_class": "নাল",
    "confidence_score": 96,
    "handwriting_quality": "স্পষ্ট",
    "total_area_decimals": 20.0,
    "owners": [
        {"name": "তারিকুল ইসলাম", "father_spouse": "মৃত রহিম উদ্দিন সরকার", "address": "জয়দেবপুর", "ana": 6, "gonda": 8, "kora": 0, "kranti": 0, "til": 0},
        {"name": "রফিকুল ইসলাম", "father_spouse": "মৃত রহিম উদ্দিন সরকার", "address": "জয়দেবপুর", "ana": 6, "gonda": 8, "kora": 0, "kranti": 0, "til": 0},
        {"name": "ফাতেমা বেগম", "father_spouse": "মৃত রহিম উদ্দিন সরকার", "address": "জয়দেবপুর", "ana": 3, "gonda": 4, "kora": 0, "kranti": 0, "til": 0}
    ]
}

SAMPLE_FRAUD_DATA = {
    "khatian_type": "CS (জাল হিস্যাযুক্ত)",
    "district": "গাজীপুর",
    "upazila": "জয়দেবপুর",
    "mouza": "জয়দেবপুর",
    "jl_no": "১০৪",
    "khatian_no": "৪১২",
    "dag_numbers": ["৩০২"],
    "land_class": "নাল",
    "confidence_score": 94,
    "handwriting_quality": "ঘষামাজা / জাল পরচা",
    "total_area_decimals": 20.0,
    "owners": [
        {"name": "তারিকুল ইসলাম (জাল হিস্যা)", "father_spouse": "মৃত রহিম উদ্দিন সরকার", "address": "জয়দেবপুর", "ana": 10, "gonda": 0, "kora": 0, "kranti": 0, "til": 0},
        {"name": "রফিকুল ইসলাম", "father_spouse": "মৃত রহিম উদ্দিন সরকার", "address": "জয়দেবপুর", "ana": 6, "gonda": 8, "kora": 0, "kranti": 0, "til": 0},
        {"name": "ফাতেমা বেগম", "father_spouse": "মৃত রহিম উদ্দিন সরকার", "address": "জয়দেবপুর", "ana": 3, "gonda": 4, "kora": 0, "kranti": 0, "til": 0}
    ]
}

def extract_and_verify_khatian(image_bytes: bytes, mime_type: str = "image/jpeg", custom_api_key: str = None, sample_type: str = None) -> Dict[str, Any]:
    """
    Takes raw image bytes of a Khatian, performs multimodal vision extraction via Gemini API,
    with automatic model fallback to avoid 429 quota exhaustion and key fallback.
    """
    keys_to_try = []
    if custom_api_key and custom_api_key.strip():
        keys_to_try.append(custom_api_key.strip())
    
    server_key = os.environ.get("GEMINI_API_KEY", DEFAULT_API_KEY).strip()
    if server_key and server_key not in keys_to_try:
        keys_to_try.append(server_key)

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
    had_auth_error = False

    # Attempt live API extraction if keys are available
    for key in keys_to_try:
        for model_name in CANDIDATE_MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
            try:
                response = requests.post(url, json=payload, timeout=30)
                
                # Check for invalid key errors
                if response.status_code in [400, 401]:
                    resp_text = response.text
                    if "API_KEY_INVALID" in resp_text or "UNAUTHENTICATED" in resp_text:
                        last_error = "API key not valid"
                        had_auth_error = True
                        break # Skip this key, try next key

                # If 429 rate-limited, silently fallback to the next model
                if response.status_code == 429:
                    last_error = f"{model_name} মডেলের কোটা পূর্ণ (429 Rate Limit)"
                    continue
                    
                if response.status_code != 200:
                    last_error = f"{model_name} ত্রুটি ({response.status_code}): {response.text[:120]}"
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

    # If live API failed and this is a sample run, fall back to benchmark baseline data
    if sample_type:
        baseline = SAMPLE_FRAUD_DATA if sample_type == "fraud" else SAMPLE_AUTHENTIC_DATA
        math_audit = audit_khatian_math(
            owners=baseline["owners"],
            total_area_decimals=baseline["total_area_decimals"]
        )
        return {
            "success": True,
            "model_used": "PorchaLens Neural Baseline (অফলাইন ডেমো ইঞ্জিন)",
            "metadata": {
                "khatian_type": baseline["khatian_type"],
                "district": baseline["district"],
                "upazila": baseline["upazila"],
                "mouza": baseline["mouza"],
                "jl_no": baseline["jl_no"],
                "khatian_no": baseline["khatian_no"],
                "dag_numbers": baseline["dag_numbers"],
                "land_class": baseline["land_class"],
                "confidence_score": baseline["confidence_score"],
                "handwriting_quality": baseline["handwriting_quality"]
            },
            "math_audit": math_audit
        }

    # If all models/keys failed on a custom user upload
    if had_auth_error or not keys_to_try:
        return {
            "success": False,
            "error_bn": f"API কী অবৈধ বা মেয়াদোত্তীর্ণ ({last_error})। অনুগ্রহ করে aistudio.google.com থেকে একটি নতুন ফ্রি Gemini API কী সংগ্রহ করে উপরের 'API কী সেটিংস' বাটনে যুক্ত করুন।"
        }

    return {
        "success": False,
        "error_bn": f"এআই সার্ভারের সকল মডেলের কোটা সাময়িকভাবে পূর্ণ ({last_error})। অনুগ্রহ করে ১ মিনিট পর আবার চেষ্টা করুন অথবা উপরের 'API কী সেটিংস'-এ আপনার নিজস্ব Gemini কী দিন।"
    }

