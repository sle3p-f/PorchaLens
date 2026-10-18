from vision_engine import extract_and_verify_khatian

print("=" * 60)
print("TEST 1: Evaluating Authentic Sample CS Khatian")
print("=" * 60)
with open("static/samples/sample_authentic_cs_khatian.jpg", "rb") as f:
    res = extract_and_verify_khatian(f.read())

if res.get("success"):
    meta = res["metadata"]
    print(f"ডকুমেন্ট টাইপ: {meta['khatian_type']} | মৌজা: {meta['mouza']} | খতিয়ান নং: {meta['khatian_no']}")
    print(f"দাগ নম্বর: {meta['dag_numbers']} | মোট জমি: {res['math_audit']['total_area_decimals_bn']} শতাংশ")
    print(f"যাচাই ফলাফল: {res['math_audit']['status_bn']}")
    print(f"রিপোর্ট: {res['math_audit']['message_bn']}")
    print("\nঅংশীদারদের আধুনিক শতাংশ রূপান্তর:")
    for o in res["math_audit"]["owners"]:
        print(f" -> {o['name']} ({o['father_spouse']}): হিস্যা {o['share_bn']} = {o['calculated_decimals_bn']} শতাংশ জমি ({o['share_percentage']}%)")
else:
    print("Error:", res.get("error_bn"))

print("\n" + "=" * 60)
print("TEST 2: Evaluating Tampered / Fraudulent Sample Khatian")
print("=" * 60)
with open("static/samples/sample_fraud_cs_khatian.jpg", "rb") as f:
    res_fraud = extract_and_verify_khatian(f.read())

if res_fraud.get("success"):
    print(f"যাচাই ফলাফল: {res_fraud['math_audit']['status_bn']}")
    print(f"রিপোর্ট: {res_fraud['math_audit']['message_bn']}")
else:
    print("Error:", res_fraud.get("error_bn"))
