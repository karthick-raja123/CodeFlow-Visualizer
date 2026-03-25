#!/usr/bin/env python3
"""
Test the API endpoints of the production-grade execution engine.
"""

import json
import urllib.request
import urllib.error
import time

BASE_URL = "http://127.0.0.1:8001"


def test_execute_endpoint():
    """Test the /execute endpoint"""
    print("\n" + "="*60)
    print("TEST: /execute API Endpoint")
    print("="*60)
    
    # Test 1: Simple print
    print("\nTest 1: Simple print")
    data = json.dumps({
        "code": 'print("Hello API World")',
        "input_data": ""
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/execute",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"✓ Output: {repr(result.get('output'))}")
            print(f"✓ Error: {repr(result.get('error'))}")
            assert "Hello API World" in result.get("output", ""), "Output not found"
    except urllib.error.URLError as e:
        print(f"✗ Connection failed: {e}")
        return False
    
    # Test 2: With input
    print("\nTest 2: With input")
    data = json.dumps({
        "code": "x = input()\nprint(x.upper())",
        "input_data": "hello"
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/execute",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"✓ Output: {repr(result.get('output'))}")
            assert "HELLO" in result.get("output", ""), "Expected uppercase output"
    except urllib.error.URLError as e:
        print(f"✗ Connection failed: {e}")
        return False
    
    # Test 3: Error handling
    print("\nTest 3: Error handling")
    data = json.dumps({
        "code": "x = 1 / 0",
        "input_data": ""
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/execute",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            error = result.get("error", "")
            print(f"✓ Error captured: {repr(error[:50])}")
            assert "ZeroDivisionError" in error, "Expected ZeroDivisionError"
    except urllib.error.URLError as e:
        print(f"✗ Connection failed: {e}")
        return False
    
    print("\n✓ All /execute tests passed!")
    return True


def test_trace_endpoint():
    """Test the /trace endpoint"""
    print("\n" + "="*60)
    print("TEST: /trace API Endpoint")
    print("="*60)
    
    print("\nTest: Trace execution")
    data = json.dumps({
        "code": "x = 5\ny = x + 3\nprint(y)",
        "input_data": ""
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/trace",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            steps = result.get("steps", [])
            print(f"✓ Number of steps: {len(steps)}")
            print(f"✓ Output: {repr(result.get('stdout'))}")
            print(f"✓ Exceeded: {result.get('exceeded')}")
            
            if steps:
                print(f"✓ Sample step: {steps[0]}")
            
            assert len(steps) > 0, "Expected trace steps"
            assert "8" in result.get("stdout", ""), "Expected output '8'"
    except urllib.error.URLError as e:
        print(f"✗ Connection failed: {e}")
        return False
    
    print("\n✓ All /trace tests passed!")
    return True


def test_health_endpoint():
    """Test the /health endpoint"""
    print("\n" + "="*60)
    print("TEST: /health API Endpoint")
    print("="*60)
    
    try:
        with urllib.request.urlopen(f"{BASE_URL}/health") as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"✓ Health status: {result.get('status')}")
            assert result.get("status") == "ok", "Expected status 'ok'"
    except urllib.error.URLError as e:
        print(f"✗ Connection failed: {e}")
        return False
    
    print("\n✓ Health endpoint working!")
    return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PRODUCTION-GRADE EXECUTION ENGINE - API TESTS")
    print("="*60)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    results = []
    
    # Test endpoints
    results.append(("Health", test_health_endpoint()))
    results.append(("Execute", test_execute_endpoint()))
    results.append(("Trace", test_trace_endpoint()))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name:20} {status}")
    
    all_passed = all(passed for _, passed in results)
    print("\n" + "="*60)
    if all_passed:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("="*60)
