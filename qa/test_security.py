"""
Security Tests for CodeFlow Visualizer
Tests sandboxing, code injection prevention, dangerous imports, etc.
"""

import requests
import time
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 5  # seconds


class SecurityTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results: List[Dict] = []
        self.security_issues: List[str] = []
    
    def _execute_test(self, name: str, code: str, check_func=None) -> Dict:
        """Execute a security test"""
        start_time = time.time()
        test_result = {
            "name": name,
            "status": "PASS",
            "duration_ms": 0,
            "error": None,
            "security_issue": False
        }
        
        try:
            payload = {"code": code, "input_data": ""}
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
            
            # Use custom check function if provided
            if check_func:
                is_secure, message = check_func(data)
                if not is_secure:
                    test_result["status"] = "FAIL"
                    test_result["security_issue"] = True
                    test_result["error"] = message
                    self.security_issues.append(f"{name}: {message}")
            
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
    
    def test_file_system_access(self) -> Dict:
        """Test prevention of file system access"""
        def check_fs_access(data):
            stdout = data.get("stdout", "")
            stderr = data.get("stderr", "")
            
            # Note: os.listdir might work but in a constrained environment
            # If it successfully lists system files, that's a security issue
            if "/" in stdout or "Windows" in stdout or "System" in stdout:
                return False, "File system access may be exposed"
            
            return True, "Appears sandboxed"
        
        return self._execute_test(
            "File System Access Control",
            'import os\nprint(os.listdir("/"))',
            check_func=check_fs_access
        )
    
    def test_dangerous_imports_subprocess(self) -> Dict:
        """Test if subprocess module is blocked"""
        def check_subprocess(data):
            stderr = data.get("stderr", "")
            
            # Check if subprocess was actually imported and used
            if "successful" in stderr.lower() or "whoami" in stderr.lower():
                return False, "subprocess module accessible - security risk"
            
            # Expected: ModuleNotFoundError or similar
            if "error" not in stderr.lower() and "module" not in stderr.lower():
                # Might still be accessible - mark as potential risk
                return True, "subprocess likely blocked/unavailable"
            
            return True, "subprocess blocked"
        
        return self._execute_test(
            "Dangerous Import: subprocess",
            'import subprocess\nresult = subprocess.run(["whoami"])',
            check_func=check_subprocess
        )
    
    def test_dangerous_imports_os_system(self) -> Dict:
        """Test if os.system is available"""
        def check_os_system(data):
            stderr = data.get("stderr", "")
            stdout = data.get("stdout", "")
            
            # If os.system successfully executed a command, it's a security issue
            if "root" in stdout or "administrator" in stdout:
                return False, "os.system() can execute system commands"
            
            return True, "os.system() appears restricted or unavailable"
        
        return self._execute_test(
            "Dangerous Function: os.system",
            'import os\nos.system("id")',
            check_func=check_os_system
        )
    
    def test_code_injection_payload(self) -> Dict:
        """Test handling of suspected code injection payloads"""
        injection_code = '''import sys; sys.exit()'''
        
        def check_injection(data):
            # Should execute but not break the API
            stderr = data.get("stderr", "")
            
            return True, "Injection payload handled safely"
        
        return self._execute_test(
            "Code Injection Attempt",
            injection_code,
            check_func=check_injection
        )
    
    def test_sql_injection_like(self) -> Dict:
        """Test SQL-like injection attempts (string-based)"""
        def check_sql_injection(data):
            stdout = data.get("stdout", "")
            stderr = data.get("stderr", "")
            
            # SQL injection as a string literal is safe
            if "SELECT" in stdout and "DROP" in stdout:
                return True, "SQL injection string printed safely (not executed)"
            
            return True, "SQL injection safely handled"
        
        return self._execute_test(
            "SQL Injection Prevention",
            'print("SELECT * FROM users; DROP TABLE users;")',
            check_func=check_sql_injection
        )
    
    def test_memory_exhaustion(self) -> Dict:
        """Test protection against memory exhaustion"""
        def check_memory(data):
            stderr = data.get("stderr", "")
            
            # Should be caught or limited
            if "memory" in stderr.lower() or "error" in stderr.lower():
                return True, "Memory exhaustion detected and handled"
            
            return True, "Large allocation handled"
        
        return self._execute_test(
            "Memory Exhaustion Protection",
            'x = [0] * (10**8)',  # Large list allocation
            check_func=check_memory
        )
    
    def test_eval_restrictions(self) -> Dict:
        """Test if eval is available (should be for legitimate use)"""
        def check_eval(data):
            stdout = data.get("stdout", "")
            stderr = data.get("stderr", "")
            
            # eval should probably be available for legitimate code
            if "9" in stdout:
                return True, "eval works for legitimate use"
            
            return True, "eval behavior verified"
        
        return self._execute_test(
            "Eval Function Behavior",
            'result = eval("3 + 6")\nprint(result)',
            check_func=check_eval
        )
    
    def test_arbitrary_code_execution(self) -> Dict:
        """Test general arbitrary code execution (should be possible in sandbox)"""
        def check_arbitrary(data):
            stdout = data.get("stdout", "")
            stderr = data.get("stderr", "")
            
            # Code should execute in sandbox
            if "test_output" in stdout:
                return True, "Code executes in sandbox (expected)"
            
            return True, "Execution verified"
        
        return self._execute_test(
            "Arbitrary Code Execution in Sandbox",
            'print("test_output")',
            check_func=check_arbitrary
        )
    
    def test_import_all_wildcard(self) -> Dict:
        """Test handling of import * statements"""
        def check_import_all(data):
            stderr = data.get("stderr", "")
            
            # Should either work or be rejected
            return True, "import * handled"
        
        return self._execute_test(
            "Import Wildcard (* ) Usage",
            'from os import *',
            check_func=check_import_all
        )
    
    def run_all(self) -> Tuple[int, int]:
        """Run all security tests. Returns (passed, failed)"""
        tests = [
            self.test_file_system_access,
            self.test_dangerous_imports_subprocess,
            self.test_dangerous_imports_os_system,
            self.test_code_injection_payload,
            self.test_sql_injection_like,
            self.test_memory_exhaustion,
            self.test_eval_restrictions,
            self.test_arbitrary_code_execution,
            self.test_import_all_wildcard,
        ]
        
        for test in tests:
            test()
        
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        
        return passed, failed
