#!/usr/bin/env python3
"""Quick test of sandbox enforcement"""
import json
import urllib.request

# Test 1: eval should be blocked
code = 'print(eval("1+1"))'
data = json.dumps({'code': code, 'input_data': ''}).encode('utf-8')
req = urllib.request.Request(
    'http://127.0.0.1:8001/execute',
    data=data,
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        print("Response:", result)
        if result.get('error') and 'eval' in result.get('error'):
            print("✓ eval() is BLOCKED")
        elif '2' in result.get('output', ''):
            print("✗ eval() is ALLOWED - SECURITY ISSUE")
        else:
            print("? Unknown result")
except Exception as e:
    print(f"Error: {e}")

# Test 2: open should be blocked
code2 = 'open("/etc/passwd")'
data2 = json.dumps({'code': code2, 'input_data': ''}).encode('utf-8')
req2 = urllib.request.Request(
    'http://127.0.0.1:8001/execute',
    data=data2,
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req2) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        if result.get('error') and 'open' in result.get('error'):
            print("✓ open() is BLOCKED")
        else:
            print("✗ open() not properly blocked")
except Exception as e:
    print(f"Error: {e}")
