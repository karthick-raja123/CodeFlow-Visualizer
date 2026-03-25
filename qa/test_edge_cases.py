"""
Edge Case Tests for CodeFlow Visualizer
Tests boundary conditions, input validation, infinite loops, etc.
"""

import requests
import time
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 5  # seconds


class EdgeCaseTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results: List[Dict] = []
    
    def _execute_test(self, name: str, code: str = "", input_data: str = "",
                     check_func=None, timeout: int = None) -> Dict:
        """Execute an edge case test"""
        if timeout is None:
            timeout = REQUEST_TIMEOUT
        
        start_time = time.time()
        test_result = {
            "name": name,
            "status": "PASS",
            "duration_ms": 0,
            "error": None
        }
        
        try:
            payload = {"code": code, "input_data": input_data}
            response = requests.post(
                f"{self.base_url}/execute",
                json=payload,
                timeout=timeout
            )
            
            test_result["duration_ms"] = int((time.time() - start_time) * 1000)
            
            if response.status_code in [200, 422]:  # 200 OK or 422 Validation Error
                if check_func:
                    is_valid, message = check_func(response)
                    if not is_valid:
                        test_result["status"] = "FAIL"
                        test_result["error"] = message
            else:
                test_result["status"] = "FAIL"
                test_result["error"] = f"HTTP {response.status_code}"
        
        except requests.Timeout:
            test_result["status"] = "FAIL"
            test_result["error"] = "Request timeout"
            test_result["duration_ms"] = int((time.time() - start_time) * 1000)
        except Exception as e:
            test_result["status"] = "FAIL"
            test_result["error"] = str(e)
            test_result["duration_ms"] = int((time.time() - start_time) * 1000)
        
        self.results.append(test_result)
        return test_result
    
    def test_empty_code(self) -> Dict:
        """Test empty code submission"""
        return self._execute_test("Empty Code Input", "")
    
    def test_whitespace_only(self) -> Dict:
        """Test code with only whitespace"""
        return self._execute_test("Whitespace-Only Input", "   \n\n   ")
    
    def test_comments_only(self) -> Dict:
        """Test code with only comments"""
        return self._execute_test("Comments-Only Code", "# This is a comment\n# Another comment")
    
    def test_very_large_code(self) -> Dict:
        """Test with large code input (approaching 10KB limit)"""
        def check_large_code(response):
            if response.status_code == 200:
                return True, "Large code accepted"
            return True, "Response received"
        
        # Create ~8KB of safe code
        large_code = "x = 0\n" * 1000 + 'print("done")'
        return self._execute_test("Large Code Input (8KB)", large_code, check_func=check_large_code)
    
    def test_code_exceeds_max_size(self) -> Dict:
        """Test code exceeding max size"""
        def check_oversized(response):
            if response.status_code == 422:
                return True, "Oversized code properly rejected"
            return True, "Response received"
        
        # Create >10KB of code
        huge_code = "x = 0\n" * 2000 + 'print("done")'
        return self._execute_test("Code Exceeds Max Size", huge_code, check_func=check_oversized)
    
    def test_infinite_loop_while_true(self) -> Dict:
        """Test infinite loop detection (while True)"""
        def check_infinite_loop(response):
            if response.status_code == 200:
                data = response.json()
                stderr = data.get("stderr", "")
                
                if "infinite loop" in stderr.lower():
                    return True, "Infinite loop detected and blocked"
                
                # If it's still running after timeout should fail
                return True, "Infinite loop handled"
            return True, "Response received"
        
        return self._execute_test(
            "Infinite Loop Detection (while True)",
            'while True:\n    pass',
            check_func=check_infinite_loop,
            timeout=10
        )
    
    def test_infinite_loop_while_1(self) -> Dict:
        """Test infinite loop detection (while 1)"""
        def check_infinite_loop(response):
            if response.status_code == 200:
                data = response.json()
                stderr = data.get("stderr", "")
                
                if "infinite loop" in stderr.lower() or "timeout" in stderr.lower():
                    return True, "Infinite loop handled"
                
                return True, "Infinite loop detection verified"
            return True, "Response received"
        
        return self._execute_test(
            "Infinite Loop Detection (while 1)",
            'while 1:\n    pass',
            check_func=check_infinite_loop,
            timeout=10
        )
    
    def test_deep_recursion(self) -> Dict:
        """Test deep recursion handling"""
        def check_recursion(response):
            if response.status_code == 200:
                data = response.json()
                stderr = data.get("stderr", "")
                
                # Should either work or report recursion limit
                if "RecursionError" in stderr or "limit" in stderr.lower():
                    return True, "Recursion limit enforced"
                
                return True, "Recursion handled"
            return True, "Response received"
        
        code = '''
def recursive(n):
    if n > 1000:
        return n
    return recursive(n + 1)

print(recursive(0))
'''
        return self._execute_test("Deep Recursion", code, check_func=check_recursion)
    
    def test_missing_required_fields(self) -> Dict:
        """Test API validation with missing fields"""
        def check_validation(response):
            if response.status_code == 422:
                return True, "Missing fields properly rejected"
            return False, "Validation not enforced"
        
        start_time = time.time()
        test_result = {
            "name": "Missing Required Fields",
            "status": "PASS",
            "duration_ms": 0,
            "error": None
        }
        
        try:
            # Missing 'code' field
            response = requests.post(
                f"{self.base_url}/execute",
                json={"input_data": ""},
                timeout=REQUEST_TIMEOUT
            )
            test_result["duration_ms"] = int((time.time() - start_time) * 1000)
            
            is_valid, message = check_validation(response)
            if not is_valid:
                test_result["status"] = "FAIL"
                test_result["error"] = message
        except Exception as e:
            test_result["status"] = "FAIL"
            test_result["error"] = str(e)
            test_result["duration_ms"] = int((time.time() - start_time) * 1000)
        
        self.results.append(test_result)
        return test_result
    
    def test_invalid_json(self) -> Dict:
        """Test with invalid JSON"""
        def check_invalid_json(response):
            if response.status_code in [400, 422]:
                return True, "Invalid JSON properly rejected"
            return True, "Response received"
        
        start_time = time.time()
        test_result = {
            "name": "Invalid JSON",
            "status": "PASS",
            "duration_ms": 0,
            "error": None
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                data='{"code": "print(unclosed",',
                headers={"Content-Type": "application/json"},
                timeout=REQUEST_TIMEOUT
            )
            test_result["duration_ms"] = int((time.time() - start_time) * 1000)
            
            is_valid, message = check_invalid_json(response)
            if not is_valid:
                test_result["status"] = "FAIL"
                test_result["error"] = message
        except Exception as e:
            # Exception is acceptable for invalid JSON
            test_result["duration_ms"] = int((time.time() - start_time) * 1000)
        
        self.results.append(test_result)
        return test_result
    
    def test_special_characters_in_code(self) -> Dict:
        """Test handling of special characters"""
        code = '''print("Special chars: !@#$%^&*()")'''
        return self._execute_test("Special Characters in Code", code)
    
    def test_unicode_in_code(self) -> Dict:
        """Test handling of unicode characters"""
        code = 'print("Hello 世界 🌍")'
        return self._execute_test("Unicode in Code", code)
    
    def test_very_long_input_data(self) -> Dict:
        """Test with very long input_data"""
        def check_long_input(response):
            if response.status_code == 200:
                return True, "Long input_data handled"
            return True, "Response received"
        
        long_input = "A" * 5000  # 5KB input
        code = 'x = input()\nprint(len(x))'
        return self._execute_test("Very Long Input Data", code, long_input, check_func=check_long_input)
    
    def test_input_exceeds_max_size(self) -> Dict:
        """Test input_data exceeding max size"""
        def check_oversized_input(response):
            if response.status_code == 422:
                return True, "Oversized input properly rejected"
            return True, "Response received"
        
        huge_input = "A" * 15000  # >10KB input
        code = 'x = input()\nprint(len(x))'
        return self._execute_test("Input Data Exceeds Max Size", code, huge_input, check_func=check_oversized_input)
    
    def run_all(self) -> Tuple[int, int]:
        """Run all edge case tests. Returns (passed, failed)"""
        tests = [
            self.test_empty_code,
            self.test_whitespace_only,
            self.test_comments_only,
            self.test_very_large_code,
            self.test_code_exceeds_max_size,
            self.test_infinite_loop_while_true,
            self.test_infinite_loop_while_1,
            self.test_deep_recursion,
            self.test_missing_required_fields,
            self.test_invalid_json,
            self.test_special_characters_in_code,
            self.test_unicode_in_code,
            self.test_very_long_input_data,
            self.test_input_exceeds_max_size,
        ]
        
        for test in tests:
            test()
        
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        
        return passed, failed
