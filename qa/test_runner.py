"""
Comprehensive QA Test Suite - Main Orchestrator
Runs all test modules with proper logging and structured reporting.

Usage:
  python test_runner.py                    # Run all tests
  python test_runner.py --help             # Show options
  python test_runner.py --module functional # Run only functional tests
"""

import json
import time
import logging
import argparse
import sys
from datetime import datetime
from pathlib import Path

# Import test modules
from test_functional import FunctionalTester
from test_performance import PerformanceTester
from test_security import SecurityTester
from test_edge_cases import EdgeCaseTester


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QATestRunner:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": base_url,
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "total_duration_ms": 0
            },
            "modules": {}
        }
        self.start_time = None
    
    def _check_endpoint_availability(self) -> bool:
        """Check if API endpoint is reachable"""
        try:
            import requests
            response = requests.get(self.base_url, timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def run_functional_tests(self) -> bool:
        """Run functional test suite"""
        print("\n" + "="*80)
        print("[FUNCTIONAL TESTS]")
        print("="*80)
        
        try:
            tester = FunctionalTester(self.base_url)
            passed, failed = tester.run_all()
            
            self.results["modules"]["functional"] = {
                "status": "completed",
                "tests": tester.results,
                "passed": passed,
                "failed": failed,
                "total": len(tester.results)
            }
            
            self._print_module_results("Functional", tester.results)
            return True
        
        except Exception as e:
            logger.error(f"Functional tests failed: {e}")
            self.results["modules"]["functional"] = {
                "status": "error",
                "error": str(e)
            }
            return False
    
    def run_performance_tests(self) -> bool:
        """Run performance test suite"""
        print("\n" + "="*80)
        print("[PERFORMANCE TESTS]")
        print("="*80)
        
        try:
            tester = PerformanceTester(self.base_url)
            passed, failed = tester.run_all()
            
            self.results["modules"]["performance"] = {
                "status": "completed",
                "tests": tester.results,
                "passed": passed,
                "failed": failed,
                "total": len(tester.results)
            }
            
            self._print_module_results("Performance", tester.results)
            return True
        
        except Exception as e:
            logger.error(f"Performance tests failed: {e}")
            self.results["modules"]["performance"] = {
                "status": "error",
                "error": str(e)
            }
            return False
    
    def run_security_tests(self) -> bool:
        """Run security test suite"""
        print("\n" + "="*80)
        print("[SECURITY TESTS]")
        print("="*80)
        
        try:
            tester = SecurityTester(self.base_url)
            passed, failed = tester.run_all()
            
            self.results["modules"]["security"] = {
                "status": "completed",
                "tests": tester.results,
                "passed": passed,
                "failed": failed,
                "total": len(tester.results),
                "security_issues": tester.security_issues
            }
            
            self._print_module_results("Security", tester.results)
            
            if tester.security_issues:
                print("\n[SECURITY ISSUES DETECTED]:")
                for issue in tester.security_issues:
                    print(f"  [!] {issue}")
            
            return True
        
        except Exception as e:
            logger.error(f"Security tests failed: {e}")
            self.results["modules"]["security"] = {
                "status": "error",
                "error": str(e)
            }
            return False
    
    def run_edge_case_tests(self) -> bool:
        """Run edge case test suite"""
        print("\n" + "="*80)
        print("[EDGE CASE TESTS]")
        print("="*80)
        
        try:
            tester = EdgeCaseTester(self.base_url)
            passed, failed = tester.run_all()
            
            self.results["modules"]["edge_cases"] = {
                "status": "completed",
                "tests": tester.results,
                "passed": passed,
                "failed": failed,
                "total": len(tester.results)
            }
            
            self._print_module_results("Edge Cases", tester.results)
            return True
        
        except Exception as e:
            logger.error(f"Edge case tests failed: {e}")
            self.results["modules"]["edge_cases"] = {
                "status": "error",
                "error": str(e)
            }
            return False
    
    def _print_module_results(self, module_name: str, results: list):
        """Print formatted results for a test module"""
        for result in results:
            status_icon = "[PASS]" if result["status"] == "PASS" else "[FAIL]"
            duration = result.get("duration_ms", 0)
            error = result.get("error", "")
            
            print(f"{status_icon} {result['name']:<45} [{duration:>4}ms]", end="")
            
            if error:
                print(f" - {error[:60]}")
            else:
                print()
    
    def _calculate_totals(self):
        """Calculate summary statistics"""
        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        for module_name, module_data in self.results.get("modules", {}).items():
            if module_data.get("status") == "completed":
                total_tests += module_data.get("total", 0)
                total_passed += module_data.get("passed", 0)
                total_failed += module_data.get("failed", 0)
        
        self.results["summary"]["total_tests"] = total_tests
        self.results["summary"]["passed"] = total_passed
        self.results["summary"]["failed"] = total_failed
        self.results["summary"]["total_duration_ms"] = int((time.time() - self.start_time) * 1000)
    
    def _print_summary(self):
        """Print test summary"""
        summary = self.results["summary"]
        
        print("\n" + "="*80)
        print("[TEST SUMMARY]")
        print("="*80)
        print(f"Total Tests:     {summary['total_tests']}")
        print(f"Passed:          {summary['passed']}")
        print(f"Failed:          {summary['failed']}")
        print(f"Success Rate:    {(summary['passed']/summary['total_tests']*100):.1f}%" if summary['total_tests'] > 0 else "N/A")
        print(f"Total Duration:  {summary['total_duration_ms']}ms ({summary['total_duration_ms']/1000:.2f}s)")
        print("="*80)
        
        # Overall status
        if summary['failed'] == 0:
            print("[RESULT] ALL TESTS PASSED")
        else:
            print(f"[RESULT] {summary['failed']} TEST(S) FAILED")
    
    def save_report(self, filename: str = "test_report.json"):
        """Save detailed test report"""
        report_path = Path(filename)
        
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n[REPORT] Detailed report saved to {report_path.absolute()}")
    
    def run_all(self) -> int:
        """Run all test suites. Returns exit code (0 for success, 1 for failure)"""
        self.start_time = time.time()
        
        print("\n" + "="*80)
        print("[START] CodeFlow Visualizer - Comprehensive QA Test Suite")
        print("="*80)
        print(f"Target: {self.base_url}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check endpoint availability
        if not self._check_endpoint_availability():
            print(f"\n[ERROR] Cannot reach {self.base_url}")
            print("Please ensure the backend server is running.")
            return 1
        
        print("[OK] API endpoint is reachable\n")
        
        # Run all test modules
        try:
            self.run_functional_tests()
            self.run_performance_tests()
            self.run_security_tests()
            self.run_edge_case_tests()
        except Exception as e:
            logger.error(f"Test execution interrupted: {e}")
            self.results['error'] = str(e)
        
        # Calculate totals and print summary
        self._calculate_totals()
        self._print_summary()
        
        # Save report
        self.save_report()
        
        # Return exit code
        return 0 if self.results["summary"]["failed"] == 0 else 1
    
    def run_specific_module(self, module: str) -> int:
        """Run a specific test module"""
        self.start_time = time.time()
        
        print("\n" + "="*80)
        print(f"[RUNNING] {module.upper()} Tests")
        print("="*80)
        print(f"Target: {self.base_url}\n")
        
        if not self._check_endpoint_availability():
            print(f"[ERROR] Cannot reach {self.base_url}")
            return 1
        
        module_map = {
            "functional": self.run_functional_tests,
            "performance": self.run_performance_tests,
            "security": self.run_security_tests,
            "edge_cases": self.run_edge_case_tests,
        }
        
        if module not in module_map:
            print(f"[ERROR] Unknown module: {module}")
            print(f"Available modules: {', '.join(module_map.keys())}")
            return 1
        
        module_map[module]()
        
        self._calculate_totals()
        self._print_summary()
        self.save_report()
        
        return 0 if self.results["summary"]["failed"] == 0 else 1


def main():
    parser = argparse.ArgumentParser(
        description="CodeFlow Visualizer QA Test Suite"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Backend API URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--module",
        choices=["functional", "performance", "security", "edge_cases"],
        help="Run only a specific test module"
    )
    parser.add_argument(
        "--report",
        default="test_report.json",
        help="Output report filename (default: test_report.json)"
    )
    
    args = parser.parse_args()
    
    runner = QATestRunner(base_url=args.url)
    
    if args.module:
        exit_code = runner.run_specific_module(args.module)
    else:
        exit_code = runner.run_all()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
