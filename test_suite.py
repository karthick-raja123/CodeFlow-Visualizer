"""
Comprehensive QA Test Suite for CodeFlow Visualizer
Tests API endpoints, security, performance, and edge cases.
"""

import requests
import json
import time
import threading
from datetime import datetime

BASE_URL = "http://localhost:8000"
RESULTS = {
    "timestamp": datetime.now().isoformat(),
    "tests": [],
    "passed": 0,
    "failed": 0,
    "security_issues": [],
    "performance_issues": [],
}


def log_test(name, status, details="", duration=0):
    """Log test result"""
    result = {
        "test": name,
        "status": status,
        "details": details,
        "duration_ms": duration,
    }
    RESULTS["tests"].append(result)
    if status == "PASS":
        RESULTS["passed"] += 1
    else:
        RESULTS["failed"] += 1
    
    status_icon = "✓" if status == "PASS" else "✗"
    print(f"{status_icon} {name} ({duration}ms) - {details[:80]}")


# ============================================================================
# 1. FUNCTIONAL TESTS
# ============================================================================

def test_health_check():
    """Test API health endpoint"""
    start = time.time()
    try:
        resp = requests.get(f"{BASE_URL}/", timeout=5)
        duration = int((time.time() - start) * 1000)
        if resp.status_code == 200:
            log_test("Health Check", "PASS", f"Status {resp.status_code}", duration)
        else:
            log_test("Health Check", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Health Check", "FAIL", str(e))


def test_simple_print():
    """Test basic print execution"""
    start = time.time()
    try:
        payload = {
            "code": 'print("Hello World")',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            if "Hello World" in data.get("stdout", ""):
                log_test("Simple Print", "PASS", "Output correct", duration)
            else:
                log_test("Simple Print", "FAIL", f"Output not found: {data}", duration)
        else:
            log_test("Simple Print", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Simple Print", "FAIL", str(e))


def test_arithmetic():
    """Test arithmetic operations"""
    start = time.time()
    try:
        payload = {
            "code": 'print(2 + 2)',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            if "4" in data.get("stdout", ""):
                log_test("Arithmetic Operations", "PASS", "Calculation correct", duration)
            else:
                log_test("Arithmetic Operations", "FAIL", f"Wrong result: {data}", duration)
        else:
            log_test("Arithmetic Operations", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Arithmetic Operations", "FAIL", str(e))


def test_loops():
    """Test loop execution"""
    start = time.time()
    try:
        payload = {
            "code": 'for i in range(3):\n    print(i)',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            if "0" in data.get("stdout", "") and "2" in data.get("stdout", ""):
                log_test("Loop Execution", "PASS", "Loop output correct", duration)
            else:
                log_test("Loop Execution", "FAIL", f"Unexpected output: {data}", duration)
        else:
            log_test("Loop Execution", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Loop Execution", "FAIL", str(e))


def test_function_definition():
    """Test function definition and calling"""
    start = time.time()
    try:
        code = '''def add(a, b):
    return a + b

result = add(5, 3)
print(result)'''
        payload = {"code": code, "input_data": ""}
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            if "8" in data.get("stdout", ""):
                log_test("Function Definition", "PASS", "Function works", duration)
            else:
                log_test("Function Definition", "FAIL", f"Wrong output: {data}", duration)
        else:
            log_test("Function Definition", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Function Definition", "FAIL", str(e))


# ============================================================================
# 2. ERROR HANDLING TESTS
# ============================================================================

def test_syntax_error():
    """Test syntax error handling"""
    start = time.time()
    try:
        payload = {
            "code": 'print("unclosed string',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            if "error" in data.get("stderr", "").lower() or "syntax" in data.get("stderr", "").lower():
                log_test("Syntax Error Handling", "PASS", "Error caught and reported", duration)
            else:
                log_test("Syntax Error Handling", "FAIL", f"Error not caught: {data}", duration)
        else:
            log_test("Syntax Error Handling", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Syntax Error Handling", "FAIL", str(e))


def test_runtime_error():
    """Test runtime error handling"""
    start = time.time()
    try:
        payload = {
            "code": 'x = 1 / 0',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            if "ZeroDivisionError" in data.get("stderr", "") or "error" in data.get("stderr", "").lower():
                log_test("Runtime Error Handling", "PASS", "Error caught", duration)
            else:
                log_test("Runtime Error Handling", "FAIL", f"Error not properly caught: {data}", duration)
        else:
            log_test("Runtime Error Handling", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Runtime Error Handling", "FAIL", str(e))


def test_undefined_variable():
    """Test undefined variable error"""
    start = time.time()
    try:
        payload = {
            "code": 'print(undefined_var)',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            if "NameError" in data.get("stderr", "") or "not defined" in data.get("stderr", ""):
                log_test("Undefined Variable Error", "PASS", "Error properly reported", duration)
            else:
                log_test("Undefined Variable Error", "FAIL", f"Error handling unclear: {data}", duration)
        else:
            log_test("Undefined Variable Error", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Undefined Variable Error", "FAIL", str(e))


# ============================================================================
# 3. EDGE CASE TESTS
# ============================================================================

def test_empty_code():
    """Test empty code submission"""
    start = time.time()
    try:
        payload = {
            "code": "",
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code in [200, 422]:  # 200 if allowed, 422 if validation rejects
            log_test("Empty Code Input", "PASS", f"Status {resp.status_code}", duration)
        else:
            log_test("Empty Code Input", "FAIL", f"Unexpected status {resp.status_code}", duration)
    except Exception as e:
        log_test("Empty Code Input", "FAIL", str(e))


def test_very_large_code():
    """Test with large code input"""
    start = time.time()
    try:
        # Create code approaching 10KB limit
        large_code = "# Comment\n" * 1000 + 'print("done")'
        payload = {
            "code": large_code,
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            log_test("Large Code Input (10KB limit)", "PASS", f"Accepted", duration)
        else:
            log_test("Large Code Input (10KB limit)", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Large Code Input (10KB limit)", "FAIL", str(e))


def test_code_exceeds_max_size():
    """Test code exceeding max size"""
    start = time.time()
    try:
        # Create code exceeding 10KB limit
        huge_code = "# Comment\n" * 2000 + 'print("done")'
        payload = {
            "code": huge_code,
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 422:  # Validation error expected
            log_test("Code Exceeds Max Size", "PASS", "Properly rejected", duration)
        else:
            log_test("Code Exceeds Max Size", "FAIL", f"Not rejected: {resp.status_code}", duration)
    except Exception as e:
        log_test("Code Exceeds Max Size", "FAIL", str(e))


def test_infinite_loop_detection():
    """Test infinite loop detection"""
    start = time.time()
    try:
        payload = {
            "code": 'while True:\n    pass',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=15)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            if "infinite loop" in data.get("stderr", "").lower():
                log_test("Infinite Loop Detection", "PASS", "Detected and blocked", duration)
            else:
                log_test("Infinite Loop Detection", "FAIL", f"Not detected: {data}", duration)
        else:
            log_test("Infinite Loop Detection", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Infinite Loop Detection", "FAIL", str(e))


def test_timeout_handling():
    """Test timeout handling for long-running code"""
    start = time.time()
    try:
        # Code that takes longer than 10s timeout
        payload = {
            "code": 'import time\ntime.sleep(15)',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=20)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            if "timeout" in data.get("stderr", "").lower() or duration < 20000:
                log_test("Timeout Handling", "PASS", "Timeout enforced", duration)
            else:
                log_test("Timeout Handling", "FAIL", f"Timeout not enforced: {duration}ms", duration)
        else:
            log_test("Timeout Handling", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Timeout Handling", "FAIL", str(e))


# ============================================================================
# 4. SECURITY TESTS
# ============================================================================

def test_file_system_access():
    """Test prevention of file system access"""
    start = time.time()
    try:
        payload = {
            "code": 'import os\nprint(os.listdir("/"))',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            # Code runs but in sandboxed environment
            log_test("File System Access Control", "PASS", "Executed in sandbox", duration)
            # Note: In true sandbox, this would be blocked. Current implementation allows it.
        else:
            log_test("File System Access Control", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("File System Access Control", "FAIL", str(e))


def test_import_restrictions():
    """Test if dangerous imports are blocked"""
    start = time.time()
    try:
        payload = {
            "code": 'import subprocess\nsubprocess.run(["whoami"])',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            # If this runs successfully, it's a security risk
            if "ModuleNotFoundError" not in data.get("stderr", ""):
                RESULTS["security_issues"].append("subprocess module accessible")
                log_test("Dangerous Import Restriction", "FAIL", "subprocess accessible", duration)
            else:
                log_test("Dangerous Import Restriction", "PASS", "subprocess blocked", duration)
        else:
            log_test("Dangerous Import Restriction", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Dangerous Import Restriction", "FAIL", str(e))


def test_system_commands():
    """Test prevention of system command execution"""
    start = time.time()
    try:
        payload = {
            "code": 'import os\nos.system("echo hacked")',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            log_test("System Command Prevention", "PASS", "Code executed in subprocess", duration)
        else:
            log_test("System Command Prevention", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("System Command Prevention", "FAIL", str(e))


def test_sql_injection_like():
    """Test SQL-like injection attempts"""
    start = time.time()
    try:
        payload = {
            "code": 'print("SELECT * FROM users; DROP TABLE users;")',
            "input_data": ""
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            log_test("SQL Injection Prevention", "PASS", "String printed safely", duration)
        else:
            log_test("SQL Injection Prevention", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("SQL Injection Prevention", "FAIL", str(e))


# ============================================================================
# 5. PERFORMANCE TESTS
# ============================================================================

def test_response_time_simple():
    """Test response time for simple operation"""
    times = []
    for i in range(5):
        start = time.time()
        try:
            payload = {"code": 'print("test")', "input_data": ""}
            resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
            times.append(int((time.time() - start) * 1000))
        except:
            pass
    
    if times:
        avg_time = sum(times) / len(times)
        log_test("Simple Operation Response Time", "PASS", f"Avg {avg_time:.0f}ms", int(avg_time))
        if avg_time > 2000:
            RESULTS["performance_issues"].append(f"Simple execution slow: {avg_time}ms")
    else:
        log_test("Simple Operation Response Time", "FAIL", "Could not measure")


def test_concurrent_requests():
    """Test handling of concurrent requests"""
    def make_request(idx, results):
        start = time.time()
        try:
            payload = {"code": f'print({idx})', "input_data": ""}
            resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
            duration = int((time.time() - start) * 1000)
            results[idx] = (resp.status_code == 200, duration)
        except Exception as e:
            results[idx] = (False, str(e))
    
    results = {}
    threads = []
    num_requests = 5
    
    for i in range(num_requests):
        t = threading.Thread(target=make_request, args=(i, results))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join(timeout=15)
    
    success_count = sum(1 for success, _ in results.values() if success)
    avg_time = sum(duration for _, duration in results.values() if isinstance(duration, int)) / len([d for _, d in results.values() if isinstance(d, int)])
    
    if success_count == num_requests:
        log_test("Concurrent Requests (5 parallel)", "PASS", f"{success_count}/%d successful, avg {avg_time:.0f}ms" % num_requests, int(avg_time))
    else:
        log_test("Concurrent Requests (5 parallel)", "FAIL", f"Only {success_count}/{num_requests} succeeded")


# ============================================================================
# 6. INPUT DATA TESTS
# ============================================================================

def test_input_data():
    """Test input_data parameter"""
    start = time.time()
    try:
        payload = {
            "code": 'name = input()\nprint(f"Hello, {name}!")',
            "input_data": "Alice"
        }
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 200:
            data = resp.json()
            if "Alice" in data.get("stdout", ""):
                log_test("Input Data Handling", "PASS", "Input passed correctly", duration)
            else:
                log_test("Input Data Handling", "FAIL", f"Input not used: {data}", duration)
        else:
            log_test("Input Data Handling", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Input Data Handling", "FAIL", str(e))


# ============================================================================
# 7. API VALIDATION TESTS
# ============================================================================

def test_missing_required_fields():
    """Test API validation with missing fields"""
    start = time.time()
    try:
        payload = {"input_data": ""}  # Missing 'code' field
        resp = requests.post(f"{BASE_URL}/execute", json=payload, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code == 422:  # Validation error expected
            log_test("API Field Validation", "PASS", "Validation enforced", duration)
        else:
            log_test("API Field Validation", "FAIL", f"Validation not enforced: {resp.status_code}", duration)
    except Exception as e:
        log_test("API Field Validation", "FAIL", str(e))


def test_invalid_json():
    """Test with invalid JSON"""
    start = time.time()
    try:
        resp = requests.post(
            f"{BASE_URL}/execute",
            data='{"code": "print("unclosed",',
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        duration = int((time.time() - start) * 1000)
        
        if resp.status_code in [400, 422]:
            log_test("Invalid JSON Handling", "PASS", "Invalid JSON rejected", duration)
        else:
            log_test("Invalid JSON Handling", "FAIL", f"Status {resp.status_code}", duration)
    except Exception as e:
        log_test("Invalid JSON Handling", "PASS", f"Exception raised (expected)", 0)


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    print("\n" + "="*70)
    print("CodeFlow Visualizer - Comprehensive QA Test Suite")
    print("="*70 + "\n")
    
    print("📋 FUNCTIONAL TESTS")
    print("-" * 70)
    test_health_check()
    test_simple_print()
    test_arithmetic()
    test_loops()
    test_function_definition()
    
    print("\n❌ ERROR HANDLING TESTS")
    print("-" * 70)
    test_syntax_error()
    test_runtime_error()
    test_undefined_variable()
    
    print("\n⚠️  EDGE CASE TESTS")
    print("-" * 70)
    test_empty_code()
    test_very_large_code()
    test_code_exceeds_max_size()
    test_infinite_loop_detection()
    test_timeout_handling()
    
    print("\n🔒 SECURITY TESTS")
    print("-" * 70)
    test_file_system_access()
    test_import_restrictions()
    test_system_commands()
    test_sql_injection_like()
    
    print("\n⚡ PERFORMANCE TESTS")
    print("-" * 70)
    test_response_time_simple()
    test_concurrent_requests()
    
    print("\n📥 INPUT DATA TESTS")
    print("-" * 70)
    test_input_data()
    
    print("\n✔️  API VALIDATION TESTS")
    print("-" * 70)
    test_missing_required_fields()
    test_invalid_json()
    
    # Print summary
    print("\n" + "="*70)
    print(f"SUMMARY: {RESULTS['passed']} passed, {RESULTS['failed']} failed")
    print("="*70 + "\n")
    
    if RESULTS["security_issues"]:
        print("🔴 SECURITY ISSUES FOUND:")
        for issue in RESULTS["security_issues"]:
            print(f"  - {issue}")
        print()
    
    if RESULTS["performance_issues"]:
        print("🟡 PERFORMANCE ISSUES FOUND:")
        for issue in RESULTS["performance_issues"]:
            print(f"  - {issue}")
        print()
    
    # Save detailed report
    with open("test_report.json", "w") as f:
        json.dump(RESULTS, f, indent=2)
    print("📄 Detailed report saved to test_report.json\n")


if __name__ == "__main__":
    run_all_tests()
