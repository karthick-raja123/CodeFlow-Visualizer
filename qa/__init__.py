"""
CodeFlow Visualizer QA Test Suite

A comprehensive, modular testing framework for the CodeFlow Visualizer API.

Modules:
- test_functional.py: Core functionality tests
- test_performance.py: Performance and throughput tests
- test_security.py: Security and sandboxing tests
- test_edge_cases.py: Boundary conditions and edge cases
- test_runner.py: Main orchestrator with reporting

Usage:
    python test_runner.py                      # Run all tests
    python test_runner.py --module functional  # Run specific module
    python test_runner.py --url http://api.example.com  # Custom URL
"""

__version__ = "2.0"
__all__ = [
    "FunctionalTester",
    "PerformanceTester",
    "SecurityTester",
    "EdgeCaseTester",
    "QATestRunner"
]
