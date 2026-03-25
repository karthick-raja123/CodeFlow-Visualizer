#!/usr/bin/env python3
"""
Comprehensive test suite for the production-grade execution engine.
Tests all 10 core requirements.
"""

from executor import run_code
from tracer import trace_execution


def test_basic_execution():
    """Test 1: Basic code execution"""
    print("\n" + "="*60)
    print("TEST 1: BASIC CODE EXECUTION")
    print("="*60)
    
    code = 'print("Hello, World!")'
    out, err = run_code(code)
    
    print(f"Code: {code}")
    print(f"Output: {repr(out)}")
    print(f"Error: {repr(err)}")
    assert out.strip() == "Hello, World!", f"Expected 'Hello, World!', got {repr(out)}"
    assert err == "", f"Expected no error, got {repr(err)}"
    print("✓ PASSED")


def test_input_handling():
    """Test 2: Interactive input handling (multiple inputs)"""
    print("\n" + "="*60)
    print("TEST 2: INTERACTIVE INPUT HANDLING")
    print("="*60)
    
    code = '''name = input("Name: ")
age = input("Age: ")
print(f"Hello {name}, you are {age} years old")'''
    
    out, err = run_code(code, "Alice\n25")
    
    print(f"Code:\n{code}")
    print(f"Input: 'Alice\\n25'")
    print(f"Output: {repr(out)}")
    print(f"Error: {repr(err)}")
    assert "Alice" in out and "25" in out, f"Expected input to be reflected in output"
    assert err == "", f"Expected no error, got {repr(err)}"
    print("✓ PASSED")


def test_error_handling():
    """Test 3: Runtime error handling"""
    print("\n" + "="*60)
    print("TEST 3: ERROR HANDLING")
    print("="*60)
    
    code = "x = 1 / 0"
    out, err = run_code(code)
    
    print(f"Code: {code}")
    print(f"Output: {repr(out)}")
    print(f"Error: {repr(err)}")
    assert "ZeroDivisionError" in err or "division" in err.lower(), f"Expected ZeroDivisionError, got {repr(err)}"
    print("✓ PASSED")


def test_loop_execution():
    """Test 4: Loop execution (no false infinite loop detection)"""
    print("\n" + "="*60)
    print("TEST 4: LOOP EXECUTION")
    print("="*60)
    
    code = """for i in range(5):
    print(i)"""
    
    out, err = run_code(code)
    
    print(f"Code:\n{code}")
    print(f"Output: {repr(out)}")
    print(f"Error: {repr(err)}")
    assert "0" in out and "4" in out, f"Expected loop output 0-4"
    assert err == "", f"Expected no error, got {repr(err)}"
    print("✓ PASSED")


def test_timeout_protection():
    """Test 5: Timeout protection for infinite loops"""
    print("\n" + "="*60)
    print("TEST 5: TIMEOUT PROTECTION")
    print("="*60)
    
    code = """while True:
    x = 1"""
    
    out, err = run_code(code)
    
    print(f"Code:\n{code}")
    print(f"Output: {repr(out)}")
    print(f"Error: {repr(err[:100])}")
    assert "Timeout" in err or "timeout" in err, f"Expected timeout error, got {repr(err)}"
    print("✓ PASSED (Execution timed out as expected)")


def test_variable_snapshot():
    """Test 6: Variable snapshot in traces"""
    print("\n" + "="*60)
    print("TEST 6: VARIABLE SNAPSHOTS")
    print("="*60)
    
    code = """x = 5
y = x + 3
print(y)"""
    
    result = trace_execution(code)
    
    print(f"Code:\n{code}")
    print(f"Number of steps: {len(result['steps'])}")
    print(f"Stdout: {repr(result['stdout'])}")
    print(f"Stderr: {repr(result['stderr'])}")
    if result['steps']:
        print(f"Sample step: {result['steps'][0]}")
    
    assert len(result['steps']) > 0, "Expected trace steps"
    assert result['stdout'].strip() == "8", f"Expected output '8', got {repr(result['stdout'])}"
    assert result['stderr'] == "", f"Expected no error, got {repr(result['stderr'])}"
    print("✓ PASSED")


def test_isolation():
    """Test 7: Execution isolation between runs"""
    print("\n" + "="*60)
    print("TEST 7: EXECUTION ISOLATION")
    print("="*60)
    
    # First execution
    code1 = "x = 100\nprint(x)"
    out1, err1 = run_code(code1)
    
    # Second execution (should not have x from first)
    code2 = "print(x)"  # This should fail since x is not defined
    out2, err2 = run_code(code2)
    
    print(f"First execution output: {repr(out1)}")
    print(f"Second execution error: {repr(err2[:100])}")
    
    assert out1.strip() == "100", f"First execution should output 100"
    assert "NameError" in err2 or "not defined" in err2, f"Second execution should fail with NameError"
    print("✓ PASSED (Isolation confirmed)")


def test_unicode_handling():
    """Test 8: Unicode character handling"""
    print("\n" + "="*60)
    print("TEST 8: UNICODE HANDLING")
    print("="*60)
    
    code = 'print("Hello 🌍 世界 مرحبا")'
    out, err = run_code(code)
    
    print(f"Code: {code}")
    print(f"Output: {repr(out)}")
    print(f"Error: {repr(err)}")
    
    assert "🌍" in out or "世界" in out, f"Expected unicode characters in output"
    assert err == "", f"Expected no error"
    print("✓ PASSED")


def test_syntax_error():
    """Test 9: Syntax error detection"""
    print("\n" + "="*60)
    print("TEST 9: SYNTAX ERROR DETECTION")
    print("="*60)
    
    code = "print('missing closing quote"
    out, err = run_code(code)
    
    print(f"Code: {code}")
    print(f"Output: {repr(out)}")
    print(f"Error: {repr(err[:100])}")
    
    assert "SyntaxError" in err, f"Expected SyntaxError, got {repr(err)}"
    print("✓ PASSED")


def test_multiple_inputs():
    """Test 10: Multiple sequential inputs"""
    print("\n" + "="*60)
    print("TEST 10: MULTIPLE SEQUENTIAL INPUTS")
    print("="*60)
    
    code = """a = input()
b = input()
c = input()
print(f"{a} {b} {c}")"""
    
    out, err = run_code(code, "one\ntwo\nthree")
    
    print(f"Code:\n{code}")
    print(f"Input: 'one\\ntwo\\nthree'")
    print(f"Output: {repr(out)}")
    print(f"Error: {repr(err)}")
    
    assert "one two three" in out, f"Expected 'one two three' in output, got {repr(out)}"
    assert err == "", f"Expected no error"
    print("✓ PASSED")


if __name__ == "__main__":
    tests = [
        test_basic_execution,
        test_input_handling,
        test_error_handling,
        test_loop_execution,
        test_timeout_protection,
        test_variable_snapshot,
        test_isolation,
        test_unicode_handling,
        test_syntax_error,
        test_multiple_inputs,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ FAILED: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("="*60)
