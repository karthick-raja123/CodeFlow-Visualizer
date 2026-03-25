#!/usr/bin/env python3
"""
PHASE 1: Comprehensive Functional & Input Handling Testing
Senior QA - Backend Validation Suite

Tests:
- Valid Python execution
- Input handling (single, multiple, loop-based)
- Output correctness
- Error handling (syntax, runtime, edge cases)
- API endpoint validation
"""

import subprocess
import json
import time
import sys
import urllib.request
import urllib.error
from typing import Dict, Tuple, List


BASE_URL = "http://127.0.0.1:8001"


class QATestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = True
        self.errors = []
        self.performance_ms = 0.0
        self.details = {}
    
    def fail(self, reason: str):
        self.passed = False
        self.errors.append(reason)
    
    def report(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        print(f"\n{status} - {self.name}")
        if self.errors:
            for error in self.errors:
                print(f"    Error: {error}")
        print(f"    Time: {self.performance_ms:.1f}ms")


class Phase1QATester:
    def __init__(self):
        self.results = []
        self.api_health_ok = False
    
    def check_api_health(self):
        """Verify API is online"""
        try:
            with urllib.request.urlopen(f"{BASE_URL}/health") as response:
                result = json.loads(response.read().decode('utf-8'))
                self.api_health_ok = result.get('status') == 'ok'
                return self.api_health_ok
        except Exception as e:
            print(f"✗ API Health Check Failed: {e}")
            return False
    
    def _api_call(self, endpoint: str, data: Dict) -> Tuple[Dict, float]:
        """Make API call and return (response, time_ms)"""
        start = time.time()
        try:
            json_data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                f"{BASE_URL}{endpoint}",
                data=json_data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                elapsed_ms = (time.time() - start) * 1000
                return result, elapsed_ms
        except Exception as e:
            raise Exception(f"API call failed: {e}")
    
    # ─────── FUNCTIONAL TESTS ───────
    
    def test_basic_print(self):
        """Test 1: Basic print functionality"""
        test = QATestResult("Basic Print Statement")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'print("Hello, World!")',
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            if "Hello, World!" not in result.get('output', ''):
                test.fail(f"Expected 'Hello, World!' in output, got {repr(result.get('output'))}")
            if result.get('error'):
                test.fail(f"Unexpected error: {result.get('error')}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_arithmetic(self):
        """Test 2: Arithmetic operations"""
        test = QATestResult("Arithmetic Operations")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'print(2 + 2)\nprint(10 * 5)\nprint(100 / 4)',
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            output = result.get('output', '')
            if '4' not in output or '50' not in output or '25' not in output:
                test.fail(f"Expected 4, 50, 25 in output, got {repr(output)}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_variables_and_assignments(self):
        """Test 3: Variables and assignments"""
        test = QATestResult("Variables & Assignments")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'x = 10\ny = 20\nz = x + y\nprint(z)',
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            if '30' not in result.get('output', ''):
                test.fail(f"Expected 30 in output, got {repr(result.get('output'))}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_loops(self):
        """Test 4: Loop execution"""
        test = QATestResult("Loop Execution")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'for i in range(3):\n    print(i)',
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            output = result.get('output', '')
            if '0' not in output or '1' not in output or '2' not in output:
                test.fail(f"Expected 0,1,2 in output, got {repr(output)}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_lists(self):
        """Test 5: List operations"""
        test = QATestResult("List Operations")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'x = [1,2,3]\nprint(len(x))\nprint(x[0])',
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            output = result.get('output', '')
            if '3' not in output or '1' not in output:
                test.fail(f"Expected 3 and 1 in output, got {repr(output)}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    # ─────── INPUT HANDLING TESTS ───────
    
    def test_single_input(self):
        """Test 6: Single input() call"""
        test = QATestResult("Single input() Call")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'x = input("Enter: ")\nprint(x)',
                "input_data": "test_value"
            })
            test.performance_ms = elapsed
            
            if "test_value" not in result.get('output', ''):
                test.fail(f"Expected 'test_value' in output, got {repr(result.get('output'))}")
            if "Enter:" in result.get('output', '') and result.get('output', '').index("Enter:") == 0:
                # Check prompt is not mixed with input
                output = result.get('output', '')
                if output.startswith("Enter: test_value"):
                    test.fail("Prompt mixed with input value (should be separate)")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_multiple_inputs(self):
        """Test 7: Multiple input() calls"""
        test = QATestResult("Multiple input() Calls")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'a = input()\nb = input()\nc = input()\nprint(f"{a}-{b}-{c}")',
                "input_data": "first\nsecond\nthird"
            })
            test.performance_ms = elapsed
            
            if "first-second-third" not in result.get('output', ''):
                test.fail(f"Expected 'first-second-third', got {repr(result.get('output'))}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_loop_with_input(self):
        """Test 8: Loop-based input()"""
        test = QATestResult("Loop-Based input()")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'for i in range(2):\n    x = input()\n    print(x)',
                "input_data": "line1\nline2"
            })
            test.performance_ms = elapsed
            
            output = result.get('output', '')
            if "line1" not in output or "line2" not in output:
                test.fail(f"Expected both line1 and line2, got {repr(output)}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    # ─────── ERROR HANDLING TESTS ───────
    
    def test_syntax_error(self):
        """Test 9: Syntax error detection"""
        test = QATestResult("Syntax Error Detection")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": "print('missing quote",
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            if "SyntaxError" not in result.get('error', ''):
                test.fail(f"Expected SyntaxError in error, got {repr(result.get('error'))}")
            if result.get('error') == '':
                test.fail("Expected error message, got empty error")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_runtime_error(self):
        """Test 10: Runtime error detection"""
        test = QATestResult("Runtime Error Detection")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": "x = 1 / 0",
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            if "ZeroDivisionError" not in result.get('error', ''):
                test.fail(f"Expected ZeroDivisionError, got {repr(result.get('error'))}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_name_error(self):
        """Test 11: NameError detection"""
        test = QATestResult("NameError Detection")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": "print(undefined_variable)",
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            if "NameError" not in result.get('error', ''):
                test.fail(f"Expected NameError, got {repr(result.get('error'))}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    # ─────── EDGE CASE TESTS ───────
    
    def test_empty_code(self):
        """Test 12: Empty code"""
        test = QATestResult("Empty Code")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": "",
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            # Should execute without error
            if result.get('error') and "SyntaxError" not in result.get('error', ''):
                test.fail(f"Unexpected error: {result.get('error')}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_large_output(self):
        """Test 13: Large output"""
        test = QATestResult("Large Output (1000 lines)")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": "for i in range(1000):\n    print(i)",
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            output = result.get('output', '')
            line_count = output.count('\n')
            if line_count < 900:  # Should have ~1000 lines
                test.fail(f"Expected ~1000 lines, got {line_count}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_unicode_support(self):
        """Test 14: Unicode support"""
        test = QATestResult("Unicode Support")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'print("Hello 🌍 世界 مرحبا")',
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            if "🌍" not in result.get('output', '') and "世界" not in result.get('output', ''):
                test.fail(f"Unicode not preserved, got {repr(result.get('output'))}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    # ─────── API ENDPOINT TESTS ───────
    
    def test_execute_endpoint_response_format(self):
        """Test 15: /execute response format"""
        test = QATestResult("/execute Response Format")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'print("test")',
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            required_fields = ['output', 'error', 'stdout', 'stderr', 'exit_code']
            for field in required_fields:
                if field not in result:
                    test.fail(f"Missing required field: {field}")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def test_trace_endpoint_response_format(self):
        """Test 16: /trace response format"""
        test = QATestResult("/trace Response Format")
        try:
            result, elapsed = self._api_call("/trace", {
                "code": 'x = 5\nprint(x)',
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            required_fields = ['steps', 'stdout', 'stderr']
            for field in required_fields:
                if field not in result:
                    test.fail(f"Missing required field: {field}")
            
            if not isinstance(result.get('steps'), list):
                test.fail("steps must be a list")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    # ─────── PERFORMANCE REQUIREMENT TESTS ───────
    
    def test_response_time(self):
        """Test 17: Response time < 1000ms"""
        test = QATestResult("Response Time (<1000ms)")
        try:
            result, elapsed = self._api_call("/execute", {
                "code": 'print("fast")',
                "input_data": ""
            })
            test.performance_ms = elapsed
            
            if elapsed > 1000:
                test.fail(f"Response time {elapsed:.1f}ms exceeds 1000ms limit")
        except Exception as e:
            test.fail(str(e))
        
        self.results.append(test)
        return test.passed
    
    def run_all(self):
        """Run all Phase 1 tests"""
        print("\n" + "="*70)
        print("PHASE 1: COMPREHENSIVE FUNCTIONAL & INPUT HANDLING TESTING")
        print("="*70)
        
        if not self.check_api_health():
            print("✗ API is not online. Cannot proceed with tests.")
            return False
        
        print("✓ API Health OK - Proceeding with tests...\n")
        
        tests_to_run = [
            self.test_basic_print,
            self.test_arithmetic,
            self.test_variables_and_assignments,
            self.test_loops,
            self.test_lists,
            self.test_single_input,
            self.test_multiple_inputs,
            self.test_loop_with_input,
            self.test_syntax_error,
            self.test_runtime_error,
            self.test_name_error,
            self.test_empty_code,
            self.test_large_output,
            self.test_unicode_support,
            self.test_execute_endpoint_response_format,
            self.test_trace_endpoint_response_format,
            self.test_response_time,
        ]
        
        for test_func in tests_to_run:
            try:
                test_func()
            except Exception as e:
                print(f"✗ EXCEPTION in {test_func.__name__}: {e}")
        
        # Summary
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        print("\n" + "="*70)
        print(f"PHASE 1 RESULTS: {passed}/{total} tests passed")
        print("="*70)
        
        # Print failing tests summary
        if passed < total:
            print("\nFailing Tests:")
            for result in self.results:
                if not result.passed:
                    print(f"  ✗ {result.name}")
                    for error in result.errors:
                        print(f"    - {error}")
        
        # Print each test
        for result in self.results:
            result.report()
        
        return passed == total


if __name__ == "__main__":
    tester = Phase1QATester()
    success = tester.run_all()
    sys.exit(0 if success else 1)
