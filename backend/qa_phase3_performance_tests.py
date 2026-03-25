#!/usr/bin/env python3
"""
PHASE 3: Performance & Concurrency Testing
Senior DevOps Engineer - Load & Stress Testing

Tests:
- Response time under normal load
- Concurrent execution (50+ users)
- Memory stability
- Timeout handling
- Large input processing
- Recursion limits
"""

import subprocess
import json
import urllib.request
import urllib.error
import time
import threading
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed


BASE_URL = "http://127.0.0.1:8001"


class PerformanceMetrics:
    def __init__(self):
        self.response_times = []
        self.errors = []
        self.timeouts = 0
        self.successes = 0
    
    def add_result(self, elapsed_ms: float, success: bool, error: str = ""):
        self.response_times.append(elapsed_ms)
        if success:
            self.successes += 1
        else:
            self.errors.append(error)
            if "timeout" in error.lower() or "TimeoutExpired" in error:
                self.timeouts += 1
    
    def get_stats(self) -> Dict:
        if not self.response_times:
            return {}
        
        times = sorted(self.response_times)
        return {
            'count': len(times),
            'min_ms': min(times),
            'max_ms': max(times),
            'avg_ms': sum(times) / len(times),
            'p50_ms': times[len(times) // 2],
            'p95_ms': times[int(len(times) * 0.95)],
            'p99_ms': times[int(len(times) * 0.99)] if len(times) > 100 else times[-1],
        }
    
    def report(self):
        stats = self.get_stats()
        print(f"  Total Requests: {len(self.response_times)}")
        print(f"  Successful: {self.successes}")
        print(f"  Failed: {len(self.errors)}")
        print(f"  Timeouts: {self.timeouts}")
        if stats:
            print(f"  Min: {stats['min_ms']:.1f}ms")
            print(f"  Avg: {stats['avg_ms']:.1f}ms")
            print(f"  P50: {stats['p50_ms']:.1f}ms")
            print(f"  P95: {stats['p95_ms']:.1f}ms")
            print(f"  Max: {stats['max_ms']:.1f}ms")


class Phase3PerformanceTester:
    def __init__(self):
        self.metrics = PerformanceMetrics()
    
    def _execute_api_call(self, code: str, input_data: str = "") -> float:
        """Execute code and return response time in ms. Raises on error."""
        start = time.time()
        try:
            json_data = json.dumps({
                "code": code,
                "input_data": input_data
            }).encode('utf-8')
            req = urllib.request.Request(
                f"{BASE_URL}/execute",
                data=json_data,
                headers={'Content-Type': 'application/json'},
                timeout=30  # Network timeout
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                elapsed_ms = (time.time() - start) * 1000
                
                # Check if execution succeeded
                if result.get('error') and 'TimeoutExpired' in result.get('error', ''):
                    raise TimeoutError("Code execution timeout")
                
                return elapsed_ms
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP Error: {e.code}")
        except Exception as e:
            raise Exception(str(e))
    
    # ─────── BASIC PERFORMANCE TESTS ───────
    
    def test_simple_execution_speed(self):
        """Test 1: Simple command response time"""
        print("\n[TEST 1] Simple Execution Speed")
        
        code = 'print("test")'
        times = []
        
        for i in range(10):
            try:
                elapsed = self._execute_api_call(code)
                times.append(elapsed)
                self.metrics.add_result(elapsed, True)
            except Exception as e:
                self.metrics.add_result(0, False, str(e))
        
        if times:
            avg = sum(times) / len(times)
            print(f"  Average: {avg:.1f}ms (10 runs)")
            print(f"  Target: <500ms ✓" if avg < 500 else f"  Target: <500ms ✗")
    
    def test_arithmetic_speed(self):
        """Test 2: Arithmetic operations speed"""
        print("\n[TEST 2] Arithmetic Operations Speed")
        
        code = '''
result = 0
for i in range(1000):
    result += i * 2 + 1
print(result)
'''
        times = []
        
        for i in range(5):
            try:
                elapsed = self._execute_api_call(code)
                times.append(elapsed)
                self.metrics.add_result(elapsed, True)
            except Exception as e:
                self.metrics.add_result(0, False, str(e))
        
        if times:
            avg = sum(times) / len(times)
            print(f"  Average: {avg:.1f}ms (5 runs)")
            print(f"  Target: <800ms ✓" if avg < 800 else f"  Target: <800ms ✗")
    
    # ─────── CONCURRENCY TESTS ───────
    
    def test_concurrent_users_10(self):
        """Test 3: 10 concurrent users"""
        print("\n[TEST 3] 10 Concurrent Users")
        self._run_concurrent_test(10, 'print("user")')
    
    def test_concurrent_users_25(self):
        """Test 4: 25 concurrent users"""
        print("\n[TEST 4] 25 Concurrent Users")
        self._run_concurrent_test(25, 'print("user")')
    
    def test_concurrent_users_50(self):
        """Test 5: 50 concurrent users"""
        print("\n[TEST 5] 50 Concurrent Users (Production Load)")
        self._run_concurrent_test(50, 'print("user")')
    
    def _run_concurrent_test(self, num_users: int, code: str):
        """Run concurrent execution test"""
        results = []
        local_metrics = PerformanceMetrics()
        
        def execute_user():
            try:
                elapsed = self._execute_api_call(code)
                local_metrics.add_result(elapsed, True)
                return True, elapsed
            except Exception as e:
                local_metrics.add_result(0, False, str(e))
                return False, str(e)
        
        with ThreadPoolExecutor(max_workers=min(num_users, 20)) as executor:
            futures = [executor.submit(execute_user) for _ in range(num_users)]
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append((False, str(e)))
        
        # Aggregate results
        stats = local_metrics.get_stats()
        success_count = sum(1 for s, _ in results if s)
        
        print(f"  Completed: {success_count}/{num_users}")
        if stats:
            print(f"  Avg Response: {stats['avg_ms']:.1f}ms")
            print(f"  P95 Response: {stats['p95_ms']:.1f}ms")
            print(f"  Max Response: {stats['max_ms']:.1f}ms")
        print(f"  Target: >95% success ✓" if success_count / num_users > 0.95 else f"  Target: >95% success ✗")
        
        # Add to overall metrics
        for elapsed in local_metrics.response_times:
            self.metrics.add_result(elapsed, True)
    
    # ─────── INPUT HANDLING TESTS ───────
    
    def test_large_input_processing(self):
        """Test 6: Large input processing (8KB+)"""
        print("\n[TEST 6] Large Input Processing")
        
        large_input = "x\n" * 1000  # ~5KB of newlines
        code = '''
lines = []
while True:
    try:
        line = input()
        lines.append(line)
    except EOFError:
        break
print(len(lines))
'''
        
        try:
            start = time.time()
            elapsed = self._execute_api_call(code, large_input)
            self.metrics.add_result(elapsed, True)
            print(f"  Processed {len(large_input)} bytes in {elapsed:.1f}ms")
            print(f"  Target: <1500ms ✓" if elapsed < 1500 else f"  Target: <1500ms ✗")
        except Exception as e:
            self.metrics.add_result(0, False, str(e))
            print(f"  ✗ Failed: {e}")
    
    def test_large_output_generation(self):
        """Test 7: Large output generation (100KB+)"""
        print("\n[TEST 7] Large Output Generation")
        
        code = '''
for i in range(10000):
    print(f"Line {i}: {'x' * 8}")
'''
        
        try:
            elapsed = self._execute_api_call(code)
            self.metrics.add_result(elapsed, True)
            print(f"  Generated ~100KB output in {elapsed:.1f}ms")
            print(f"  Target: <2000ms ✓" if elapsed < 2000 else f"  Target: <2000ms ✗")
        except Exception as e:
            self.metrics.add_result(0, False, str(e))
            print(f"  ✗ Failed: {e}")
    
    # ─────── TIMEOUT & RESOURCE TESTS ───────
    
    def test_timeout_enforcement(self):
        """Test 8: Timeout enforcement at 5 seconds"""
        print("\n[TEST 8] Timeout Enforcement")
        
        code = '''
while True:
    pass
'''
        
        try:
            elapsed = self._execute_api_call(code)
            print(f"  ✗ Code ran for {elapsed:.1f}ms (should have timed out)")
            self.metrics.add_result(elapsed, False, "Timeout not enforced")
        except Exception as e:
            if "TimeoutExpired" in str(e) or "timeout" in str(e).lower():
                print(f"  ✓ Timeout enforced correctly")
                self.metrics.add_result(5000, True)
            else:
                print(f"  ? Unknown error: {e}")
    
    def test_recursion_limit(self):
        """Test 9: Recursion depth handling"""
        print("\n[TEST 9] Recursion Limit")
        
        code = '''
def recursive(n):
    if n == 0:
        return 1
    return recursive(n - 1) + 1

try:
    result = recursive(1000)
    print(result)
except RecursionError:
    print("RecursionError")
'''
        
        try:
            elapsed = self._execute_api_call(code)
            self.metrics.add_result(elapsed, True)
            print(f"  ✓ Recursion handled in {elapsed:.1f}ms")
        except Exception as e:
            self.metrics.add_result(0, False, str(e))
    
    def test_memory_stability(self):
        """Test 10: Memory stability across executions"""
        print("\n[TEST 10] Memory Stability (10 executions)")
        
        code = 'x = list(range(100000)); print(len(x))'
        
        times = []
        for i in range(10):
            try:
                elapsed = self._execute_api_call(code)
                times.append(elapsed)
                self.metrics.add_result(elapsed, True)
            except Exception as e:
                self.metrics.add_result(0, False, str(e))
        
        if len(times) >= 10:
            avg_first = sum(times[:3]) / 3
            avg_last = sum(times[-3:]) / 3
            degradation = ((avg_last - avg_first) / avg_first) * 100
            
            print(f"  First 3 executions avg: {avg_first:.1f}ms")
            print(f"  Last 3 executions avg: {avg_last:.1f}ms")
            print(f"  Degradation: {degradation:.1f}%")
            
            if abs(degradation) < 20:
                print(f"  Target: <20% degradation ✓")
            else:
                print(f"  Target: <20% degradation ✗ (CONCERN)")
    
    def test_sequential_vs_concurrent(self):
        """Test 11: Sequential vs Concurrent comparison"""
        print("\n[TEST 11] Sequential vs Concurrent Comparison")
        
        code = 'print(1+1)'
        
        # Sequential
        seq_times = []
        for i in range(20):
            try:
                elapsed = self._execute_api_call(code)
                seq_times.append(elapsed)
            except:
                pass
        
        # Concurrent
        conc_times = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self._execute_api_call, code) for _ in range(20)]
            for future in as_completed(futures):
                try:
                    conc_times.append(future.result())
                except:
                    pass
        
        seq_avg = sum(seq_times) / len(seq_times) if seq_times else 0
        conc_avg = sum(conc_times) / len(conc_times) if conc_times else 0
        
        print(f"  Sequential avg: {seq_avg:.1f}ms")
        print(f"  Concurrent avg: {conc_avg:.1f}ms")
        if conc_avg > 0 and seq_avg > 0:
            overhead = ((conc_avg - seq_avg) / seq_avg) * 100
            print(f"  Concurrent overhead: {overhead:.1f}%")
    
    def run_all(self):
        """Run all Phase 3 tests"""
        print("\n" + "="*70)
        print("PHASE 3: PERFORMANCE & CONCURRENCY TESTING")
        print("="*70)
        
        tests = [
            self.test_simple_execution_speed,
            self.test_arithmetic_speed,
            self.test_concurrent_users_10,
            self.test_concurrent_users_25,
            self.test_concurrent_users_50,
            self.test_large_input_processing,
            self.test_large_output_generation,
            self.test_timeout_enforcement,
            self.test_recursion_limit,
            self.test_memory_stability,
            self.test_sequential_vs_concurrent,
        ]
        
        for test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"  ✗ EXCEPTION: {e}")
        
        # Summary
        print("\n" + "="*70)
        print("PHASE 3 PERFORMANCE SUMMARY")
        print("="*70)
        self.metrics.report()
        
        return True


if __name__ == "__main__":
    import sys
    tester = Phase3PerformanceTester()
    tester.run_all()
    sys.exit(0)
