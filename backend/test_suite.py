"""
Automated Integration Test Suite for AI Medicine Analyzer Backend & Endpoints
"""
import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:5000/api"

def make_req(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}"
    req_data = json.dumps(data).encode("utf-8") if data else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))

def run_tests():
    tests = [
        ("Health Check", "/health", "GET", None, 200),
        ("Dashboard Stats", "/stats", "GET", None, 200),
        ("Medicine Search (Paracetamol)", "/medicine/search?q=paracetamol", "GET", None, 200),
        ("Medicine Lookup (Amoxicillin)", "/medicine/Amoxicillin", "GET", None, 200),
        ("Medicine Analyze (Metformin)", "/medicine/analyze", "POST", {"medicine_name": "Metformin"}, 200),
        ("Multi-Drug Interaction (Aspirin + Warfarin)", "/interactions/check", "POST", {"medicines": ["Aspirin", "Warfarin"]}, 200),
        ("AI Chatbot Query", "/chat", "POST", {"message": "What is the common use of Cetirizine?"}, 200),
        ("Search History Ledger", "/history", "GET", None, 200)
    ]

    passed = 0
    print("=" * 60)
    print("RUNNING AI MEDICINE ANALYZER INTEGRATION TEST SUITE")
    print("=" * 60)

    for name, endpoint, method, payload, expected_code in tests:
        status, body = make_req(endpoint, method, payload)
        success = (status == expected_code) and (body.get("status") == "online" or body.get("success") == True)
        if success:
            passed += 1
            print(f"[PASS] {name} [{method} {endpoint}] -> Status {status}")
        else:
            print(f"[FAIL] {name} [{method} {endpoint}] -> Status {status} (Expected {expected_code})")
            print(f"   Response: {body}")

    print("=" * 60)
    print(f"TEST RESULTS: {passed}/{len(tests)} PASSED ({'100% SUCCESS' if passed == len(tests) else 'SOME FAILED'})")
    print("=" * 60)
    return passed == len(tests)

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
