"""
Safe Python code executor using subprocess.Popen.
Never hangs — always returns output or error within timeout.
"""

import subprocess
import tempfile
import os


def run_code(code: str, input_data: str = ""):
    # Infinite loop detection
    if "while True" in code and "break" not in code:
        return "", "Error: Infinite loop detected (while True without break). Modify your code."
    if "while 1" in code and "break" not in code:
        return "", "Error: Infinite loop detected (while 1 without break). Modify your code."

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            filename = f.name

        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1"}

        process = subprocess.Popen(
            ["python", filename],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )

        try:
            stdout, stderr = process.communicate(input=input_data, timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            return "", "Execution stopped: timeout (infinite loop or waiting input)"

        return stdout, stderr

    except Exception as e:
        return "", str(e)
    finally:
        try:
            os.unlink(filename)
        except (OSError, UnboundLocalError):
            pass
