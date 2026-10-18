"""
PorchaLens (পর্চালেন্স) - স্মার্ট ভূমি রেকর্ড ডিজিটাইজেশন ও গাণিতিক যাচাই প্ল্যাটফর্ম
Bangladesh Government Land Ministry Theme (mutation.land.gov.bd style)
"""

import os
import io
import time
import hashlib
from flask import Flask, render_template, request, jsonify, send_from_directory
from vision_engine import extract_and_verify_khatian
from tenancy_math import audit_khatian_math, to_bangla_digits

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/process-upload", methods=["POST"])
def process_upload():
    """Handles real user-uploaded Khatian image for Vision AI parsing and mathematical audit."""
    if "file" not in request.files:
        return jsonify({"success": False, "error_bn": "কোনো ফাইল নির্বাচন করা হয়নি।"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error_bn": "ফাইলের নাম পাওয়া যায়নি।"}), 400

    image_bytes = file.read()
    mime_type = file.mimetype or "image/jpeg"

    # Save uploaded file temporarily for display
    filename = f"upload_{int(time.time())}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    # Process using Gemini Vision & Tenancy Math Engine
    result = extract_and_verify_khatian(image_bytes, mime_type=mime_type)
    if result.get("success"):
        result["image_url"] = f"/static/uploads/{filename}"

    return jsonify(result)

@app.route("/api/process-sample", methods=["POST"])
def process_sample():
    """Processes one of the pre-loaded authentic or fraudulent sample images."""
    data = request.json or {}
    sample_type = data.get("sample_type", "authentic")

    if sample_type == "fraud":
        filename = "sample_fraud_cs_khatian.jpg"
    else:
        filename = "sample_authentic_cs_khatian.jpg"

    sample_path = os.path.join(app.root_path, "static", "samples", filename)
    if not os.path.exists(sample_path):
        return jsonify({"success": False, "error_bn": "নমুনা ফাইল পাওয়া যায়নি।"}), 404

    with open(sample_path, "rb") as f:
        image_bytes = f.read()

    result = extract_and_verify_khatian(image_bytes, mime_type="image/jpeg")
    if result.get("success"):
        result["image_url"] = f"/static/samples/{filename}"

    return jsonify(result)

@app.route("/api/recalculate-math", methods=["POST"])
def recalculate_math():
    """Recalculates 16-Ana math when an officer or citizen edits values in the table."""
    data = request.json or {}
    owners = data.get("owners", [])
    total_area = float(data.get("total_area_decimals", 0.0))

    math_result = audit_khatian_math(owners=owners, total_area_decimals=total_area)
    return jsonify({"success": True, "math_audit": math_result})

@app.route("/api/generate-certificate", methods=["POST"])
def generate_certificate():
    """Generates an official Bangladesh Smart e-Porcha verification certificate."""
    data = request.json or {}
    metadata = data.get("metadata", {})
    math_audit = data.get("math_audit", {})

    cert_raw = f"{metadata.get('khatian_no')}:{metadata.get('mouza')}:{math_audit.get('status')}:{time.time()}"
    cert_hash = hashlib.sha256(cert_raw.encode()).hexdigest().upper()

    return jsonify({
        "success": True,
        "certificate_id": f"BD-LAND-PORCHA-{cert_hash[:10]}",
        "qr_payload": f"https://land.gov.bd/verify?cert={cert_hash[:16]}",
        "issued_timestamp": time.strftime("%d-%m-%Y %H:%M:%S"),
        "cert_hash": cert_hash
    })

if __name__ == "__main__":
    print("=" * 65)
    print(" স্মার্ট ভূমি রেকর্ড ও খতিয়ান যাচাইকরণ প্ল্যাটফর্ম (PorchaLens)")
    print(" ওয়েবসাইট চালু হচ্ছে: http://127.0.0.1:5000")
    print("=" * 65)
    app.run(host="127.0.0.1", port=5000, debug=True)
