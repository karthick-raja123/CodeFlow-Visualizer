#!/usr/bin/env python3
"""Kill the uvicorn server and restart it"""

import subprocess
import os
import sys
import time
import psutil

# Kill any existing python processes running uvicorn
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        cmdline = ' '.join(proc.info['cmdline'] or [])
        if 'uvicorn' in cmdline or ('python' in cmdline and 'main:app' in cmdline):
            print(f"Killing process {proc.info['pid']}: {proc.info['name']}")
            proc.kill()
            time.sleep(0.5)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

print("✓ Old processes killed")
time.sleep(2)

# Start new server
print("Starting new FastAPI server...")
os.chdir(r'd:\Git\Code Visualizer\backend')
subprocess.Popen([
    sys.executable, '-m', 'uvicorn',
    'main:app',
    '--port', '8001',
    '--host', '127.0.0.1'
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("✓ fastAPI server started on port 8001")
time.sleep(3)
print("✓ Server ready for requests")
