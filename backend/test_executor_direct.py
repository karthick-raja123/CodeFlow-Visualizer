#!/usr/bin/env python3
"""Direct test of executor.run_code() function"""

import sys
sys.path.insert(0, r'd:\Git\Code Visualizer\backend')

from executor import run_code

# Test 1: eval should be blocked
print("Test 1: eval() blocking")
stdout, stderr = run_code('print(eval("1+1"))')
print(f"  stdout: {repr(stdout)}")
print(f"  stderr: {repr(stderr)}")
if 'NameError' in stderr and 'eval' in stderr:
    print("  ✓ eval() BLOCKED")
else:
    print("  ✗ eval() NOT BLOCKED")

# Test 2: exec should be blocked
print("\nTest 2: exec() blocking")
stdout, stderr = run_code('exec("print(1)")')
print(f"  stderr: {repr(stderr[:80])}")
if 'NameError' in stderr and 'exec' in stderr:
    print("  ✓ exec() BLOCKED")
else:
    print("  ✗ exec() NOT BLOCKED")

# Test 3: open should be blocked  
print("\nTest 3: open() blocking")
stdout, stderr = run_code('open("/etc/passwd")')
print(f"  stderr: {repr(stderr[:80])}")
if 'NameError' in stderr and 'open' in stderr:
    print("  ✓ open() BLOCKED")
else:
    print("  ✗ open() NOT BLOCKED")

# Test 4: Normal code should work
print("\nTest 4: Normal code execution")
stdout, stderr = run_code('print("hello")')
print(f"  stdout: {repr(stdout)}")
print(f"  stderr: {repr(stderr)}")
if 'hello' in stdout:
    print("  ✓ Normal code works")
else:
    print("  ✗ Normal code broken")
