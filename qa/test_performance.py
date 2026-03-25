"""
Performance Tests for CodeFlow Visualizer
Measures response times, throughput, and concurrent request handling
"""

import requests
import time
import concurrent.futures
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 5  # seconds
MAX_WORKERS = 3  # Limit concurrent threads to avoid overwhelming localhost


class PerformanceTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results: List[Dict] = []
    
    def _measure_request(self, test_name: str, code: str, input_data: str = "") -> Tuple[int, bool]:
        """Measure single request duration. Returns (duration_ms, success)"""
        start_time = time.time()
        
        try:
            payload = {"code": code, "input_data": input_data}
            response = requests.post(
                f"{self.base_url}/execute",
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            duration = int((time.time() - start_time) * 1000)
            return duration, (response.status_code == 200)
        except requests.Timeout:
            duration = int((time.time() - start_time) * 1000)
            return duration, False
        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            return duration, False
    
    def test_simple_operation_response_time(self, iterations: int = 5) -> Dict:
        """Measure response time for simple operations"""
        test_result = {
            "name": "Simple Operation Response Time",
            "status": "PASS",
            "iterations": iterations,
            "durations_ms": [],
            "avg_duration_ms": 0,
            "min_duration_ms": 0,
            "max_duration_ms": 0,
            "error": None
        }
        
        try:
            for _ in range(iterations):
                duration, success = self._measure_request(
                    "simple",
                    'print("test")'
                )
                test_result["durations_ms"].append(duration)
            
            if test_result["durations_ms"]:
                test_result["avg_duration_ms"] = int(sum(test_result["durations_ms"]) / len(test_result["durations_ms"]))
                test_result["min_duration_ms"] = min(test_result["durations_ms"])
                test_result["max_duration_ms"] = max(test_result["durations_ms"])
                
                if test_result["avg_duration_ms"] > 3000:
                    test_result["status"] = "FAIL"
                    test_result["error"] = f"Average response time too high: {test_result['avg_duration_ms']}ms"
        except Exception as e:
            test_result["status"] = "FAIL"
            test_result["error"] = str(e)
        
        self.results.append(test_result)
        return test_result
    
    def test_complex_operation_response_time(self, iterations: int = 3) -> Dict:
        """Measure response time for more complex operations"""
        test_result = {
            "name": "Complex Operation Response Time",
            "status": "PASS",
            "iterations": iterations,
            "durations_ms": [],
            "avg_duration_ms": 0,
            "min_duration_ms": 0,
            "max_duration_ms": 0,
            "error": None
        }
        
        code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(result)
'''
        
        try:
            for _ in range(iterations):
                duration, success = self._measure_request(
                    "complex",
                    code
                )
                test_result["durations_ms"].append(duration)
            
            if test_result["durations_ms"]:
                test_result["avg_duration_ms"] = int(sum(test_result["durations_ms"]) / len(test_result["durations_ms"]))
                test_result["min_duration_ms"] = min(test_result["durations_ms"])
                test_result["max_duration_ms"] = max(test_result["durations_ms"])
        except Exception as e:
            test_result["status"] = "FAIL"
            test_result["error"] = str(e)
        
        self.results.append(test_result)
        return test_result
    
    def test_concurrent_requests(self, num_requests: int = 5) -> Dict:
        """Test handling of concurrent requests"""
        test_result = {
            "name": f"Concurrent Requests ({num_requests} parallel)",
            "status": "PASS",
            "num_requests": num_requests,
            "successful": 0,
            "failed": 0,
            "durations_ms": [],
            "avg_duration_ms": 0,
            "error": None
        }
        
        def execute_request(idx):
            return self._measure_request("concurrent", f'print({idx})')
        
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [executor.submit(execute_request, i) for i in range(num_requests)]
                
                # Wait for all with timeout
                for future in concurrent.futures.as_completed(futures, timeout=REQUEST_TIMEOUT + 5):
                    try:
                        duration, success = future.result()
                        test_result["durations_ms"].append(duration)
                        if success:
                            test_result["successful"] += 1
                        else:
                            test_result["failed"] += 1
                    except Exception as e:
                        test_result["failed"] += 1
            
            if test_result["durations_ms"]:
                test_result["avg_duration_ms"] = int(sum(test_result["durations_ms"]) / len(test_result["durations_ms"]))
            
            if test_result["successful"] < num_requests:
                test_result["status"] = "FAIL"
                test_result["error"] = f"Only {test_result['successful']}/{num_requests} requests succeeded"
        
        except Exception as e:
            test_result["status"] = "FAIL"
            test_result["error"] = str(e)
        
        self.results.append(test_result)
        return test_result
    
    def test_sequential_throughput(self, num_requests: int = 10) -> Dict:
        """Measure throughput of sequential requests"""
        test_result = {
            "name": f"Sequential Throughput ({num_requests} requests)",
            "status": "PASS",
            "num_requests": num_requests,
            "successful": 0,
            "total_duration_ms": 0,
            "avg_duration_ms": 0,
            "throughput_req_per_sec": 0,
            "error": None
        }
        
        start_time = time.time()
        durations = []
        
        try:
            for i in range(num_requests):
                duration, success = self._measure_request("throughput", f'print({i})')
                durations.append(duration)
                if success:
                    test_result["successful"] += 1
            
            total_duration = int((time.time() - start_time) * 1000)
            test_result["total_duration_ms"] = total_duration
            
            if durations:
                test_result["avg_duration_ms"] = int(sum(durations) / len(durations))
            
            if total_duration > 0:
                test_result["throughput_req_per_sec"] = round(num_requests / (total_duration / 1000), 2)
            
            if test_result["successful"] < num_requests:
                test_result["status"] = "FAIL"
                test_result["error"] = f"Only {test_result['successful']}/{num_requests} requests succeeded"
        
        except Exception as e:
            test_result["status"] = "FAIL"
            test_result["error"] = str(e)
        
        self.results.append(test_result)
        return test_result
    
    def run_all(self) -> Tuple[int, int]:
        """Run all performance tests. Returns (passed, failed)"""
        tests = [
            self.test_simple_operation_response_time,
            self.test_complex_operation_response_time,
            self.test_concurrent_requests,
            self.test_sequential_throughput,
        ]
        
        for test in tests:
            test()
        
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        
        return passed, failed
