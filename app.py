"""
BhumiGraph - Flask Web Application & REST API
LandTech 2026 Innovation Hackathon
"""

from flask import Flask, render_template, jsonify, request
from graph_core import engine
import hashlib
import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/parcels", methods=["GET"])
def get_parcels():
    return jsonify(engine.list_all_parcels())

@app.route("/api/graph/<parcel_id>", methods=["GET"])
def get_graph(parcel_id):
    graph_data = engine.build_vis_graph(parcel_id)
    return jsonify(graph_data)

@app.route("/api/health/<parcel_id>", methods=["GET"])
def get_health(parcel_id):
    health_data = engine.compute_land_health_score(parcel_id)
    return jsonify(health_data)

@app.route("/api/audit-transfer", methods=["POST"])
def audit_transfer():
    data = request.json or {}
    parcel_id = data.get("parcel_id", "BS-810")
    seller_nid = data.get("seller_nid", "")
    proposed_area = float(data.get("proposed_area", 0.0))
    claimed_heirs = data.get("claimed_heirs", None)

    audit_result = engine.audit_transfer_attempt(
        parcel_id=parcel_id,
        seller_nid=seller_nid,
        proposed_area_decimals=proposed_area,
        claimed_heirs=claimed_heirs
    )
    return jsonify(audit_result)

@app.route("/api/lock/acquire", methods=["POST"])
def acquire_lock():
    data = request.json or {}
    parcel_id = data.get("parcel_id", "BS-810")
    office = data.get("office", "Gazipur Sadar Sub-Registry")
    area = float(data.get("area", 5.0))
    res = engine.acquire_inter_registry_lock(parcel_id, office, area)
    return jsonify(res)

@app.route("/api/lock/release", methods=["POST"])
def release_lock():
    data = request.json or {}
    parcel_id = data.get("parcel_id", "BS-810")
    res = engine.release_inter_registry_lock(parcel_id)
    return jsonify({"success": res})

@app.route("/api/certificate/<parcel_id>", methods=["GET"])
def get_certificate(parcel_id):
    parcel = engine.get_parcel(parcel_id)
    if not parcel:
        return jsonify({"error": "Not found"}), 404
    
    health = engine.compute_land_health_score(parcel_id)
    timestamp = time.strftime("%d-%b-%Y %H:%M:%S UTC")
    raw_hash_input = f"{parcel_id}:{parcel['khatian_no']}:{health['score']}:{timestamp}"
    cert_hash = hashlib.sha256(raw_hash_input.encode()).hexdigest().upper()

    return jsonify({
        "certificate_id": f"BG-CERT-{cert_hash[:12]}",
        "timestamp": timestamp,
        "parcel": parcel,
        "health": health,
        "cryptographic_hash": cert_hash,
        "status": "OFFICIALLY_VERIFIED" if health["score"] >= 80 else "CAUTION_ENCUMBERED"
    })

if __name__ == "__main__":
    print("=" * 60)
    print(" BhumiGraph Web Server Running on http://127.0.0.1:5000")
    print(" LandTech 2026 - Digital Land Records, Verification & Digitization")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=True)
