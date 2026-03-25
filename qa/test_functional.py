"""
Functional Tests for CodeFlow Visualizer
Tests core API functionality: execution, input/output correctness
"""

import requests
import time
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 5  # seconds


class FunctionalTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results: List[Dict] = []
    
    def _execute_test(self, name: str, code: str, expected_output: str = None,
                     should_error: bool = False, input_data: str = "") -> Dict:
        """Execute a single test case"""
        start_time = time.time()
        test_result = {
            "name": name,
            "status": "PASS",
            "duration_ms": 0,
            "error": None,
            "output": ""
        }
        
        try:
            payload = {"code": code, "input_data": input_data}
            response = requests.post(
                f"{self.base_url}/execute",
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            
            test_result["duration_ms"] = int((time.time() - start_time) * 1000)
            
            if response.status_code != 200:
                test_result["status"] = "FAIL"
                test_result["error"] = f"HTTP {response.status_code}"
                return test_result
            
            data = response.json()
            stdout = data.get("stdout", "")
            stderr = data.get("stderr", "")
            
            if should_error:
                if stderr and ("error" in stderr.lower() or "exception" in stderr.lower()):
                    test_result["status"] = "PASS"
                    test_result["output"] = stderr
                else:
                    test_result["status"] = "FAIL"
                    test_result["error"] = "Expected error but got none"
            elif expected_output:
                if expected_output in stdout:
                    test_result["status"] = "PASS"
                    test_result["output"] = stdout
                else:
                    test_result["status"] = "FAIL"
                    test_result["error"] = f"Expected '{expected_output}' not found in output"
                    test_result["output"] = stdout
            else:
                # Just check if it executed without error
                if not stderr:
                    test_result["status"] = "PASS"
                    test_result["output"] = stdout
                else:
                    test_result["status"] = "FAIL"
                    test_result["error"] = stderr
        
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
    
    def test_health_check(self) -> Dict:
        """Test API health endpoint"""
        start_time = time.time()
        test_result = {
            "name": "Health Check",
            "status": "PASS",
            "duration_ms": 0,
            "error": None
        }
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=REQUEST_TIMEOUT)
            test_result["duration_ms"] = int((time.time() - start_time) * 1000)
            
            if response.status_code != 200:
                test_result["status"] = "FAIL"
                test_result["error"] = f"HTTP {response.status_code}"
        except Exception as e:
            test_result["status"] = "FAIL"
            test_result["error"] = str(e)
            test_result["duration_ms"] = int((time.time() - start_time) * 1000)
        
        self.results.append(test_result)
        return test_result
    
    def test_simple_print(self) -> Dict:
        """Test basic print execution"""
        return self._execute_test(
            "Simple Print",
            'print("Hello World")',
            expected_output="Hello World"
        )
    
    def test_arithmetic(self) -> Dict:
        """Test arithmetic operations"""
        return self._execute_test(
            "Arithmetic Operations",
            'print(2 + 2)',
            expected_output="4"
        )
    
    def test_loops(self) -> Dict:
        """Test loop execution"""
        return self._execute_test(
            "Loop Execution",
            'for i in range(3):\n    print(i)',
            expected_output="2"  # Just check that loop runs
        )
    
    def test_function_definition(self) -> Dict:
        """Test function definition and calling"""
        code = '''def add(a, b):
    return a + b

result = add(5, 3)
print(result)'''
        return self._execute_test(
            "Function Definition",
            code,
            expected_output="8"
        )
    
    def test_list_operations(self) -> Dict:
        """Test list operations"""
        code = '''numbers = [1, 2, 3]
print(len(numbers))
numbers.append(4)
print(numbers[-1])'''
        return self._execute_test(
            "List Operations",
            code,
            expected_output="4"
        )
    
    def test_dictionary_operations(self) -> Dict:
        """Test dictionary operations"""
        code = '''person = {"name": "Alice", "age": 30}
print(person["name"])'''
        return self._execute_test(
            "Dictionary Operations",
            code,
            expected_output="Alice"
        )
    
    def test_syntax_error(self) -> Dict:
        """Test syntax error handling"""
        return self._execute_test(
            "Syntax Error Handling",
            'print("unclosed string',
            should_error=True
        )
    
    def test_runtime_error(self) -> Dict:
        """Test runtime error handling"""
        return self._execute_test(
            "Runtime Error Handling",
            'x = 1 / 0',
            should_error=True
        )
    
    def test_undefined_variable(self) -> Dict:
        """Test undefined variable error"""
        return self._execute_test(
            "Undefined Variable Error",
            'print(undefined_var)',
            should_error=True
        )
    
    def test_input_data(self) -> Dict:
        """Test input_data parameter"""
        return self._execute_test(
            "Input Data Handling",
            'name = input()\nprint(f"Hello, {name}!")',
            expected_output="Hello, Alice!",
            input_data="Alice"
        )
    
    def test_string_operations(self) -> Dict:
        """Test string operations"""
        code = '''text = "hello"
print(text.upper())'''
        return self._execute_test(
            "String Operations",
            code,
            expected_output="HELLO"
        )
    
    def run_all(self) -> Tuple[int, int]:
        """Run all functional tests. Returns (passed, failed)"""
        tests = [
            self.test_health_check,
            self.test_simple_print,
            self.test_arithmetic,
            self.test_loops,
            self.test_function_definition,
            self.test_list_operations,
            self.test_dictionary_operations,
            self.test_syntax_error,
            self.test_runtime_error,
            self.test_undefined_variable,
            self.test_input_data,
            self.test_string_operations,
        ]
        
        for test in tests:
            test()
        
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        
        return passed, failed
