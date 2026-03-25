"""
Step-by-step Python execution tracer with proper input handling.
Captures line execution order, variable snapshots, and output per step.

Uses subprocess-based execution for true isolation and proper stdin streaming.
"""

import subprocess
import tempfile
import sys
import os
from typing import Dict, List, Any
import json


MAX_STEPS = 200  # Maximum steps before stopping trace
MAX_VAR_STR_LEN = 100  # Max string length for variable repr


def _safe_repr(value) -> str:
    """Safely represent a value as string, truncating if too long."""
    try:
        r = repr(value)
        if len(r) > MAX_VAR_STR_LEN:
            return r[:MAX_VAR_STR_LEN] + "..."
        return r
    except Exception:
        return "<unrepresentable>"


def _safe_type(value) -> str:
    """Get type name safely."""
    try:
        return type(value).__name__
    except Exception:
        return "unknown"


def create_trace_wrapper(code: str, input_data: str) -> str:
    """
    Wrap user code with tracing instrumentation using sys.settrace.
    """
    
    trace_script = '''import sys
import io
import json

# Global state for tracing
steps_recorded = []
current_step = 0
max_steps = {max_steps}
step_exceeded = False
last_output_pos = 0
output_capture = io.StringIO()

def safe_snapshot_vars(local_vars):
    """Create JSON-safe snapshot of local variables."""
    snapshot = {{}}
    for name, value in local_vars.items():
        if name.startswith('_'):
            continue
        if callable(value) and not isinstance(value, (int, float, str, bool)):
            continue
        if isinstance(value, type):
            continue
        
        try:
            snapshot[name] = {{
                "value": repr(value)[:100] if len(repr(value)) <= 100 else repr(value)[:97] + "...",
                "type": type(value).__name__
            }}
        except:
            pass
    
    return snapshot

def trace_function(frame, event, arg):
    """Trace function for sys.settrace."""
    global current_step, step_exceeded, last_output_pos, output_capture
    
    # Only trace user code
    if frame.f_code.co_filename != '<user_code>':
        return None
    
    if step_exceeded:
        return None
    
    # Only care about line events
    if event != 'line':
        return trace_function
    
    current_step += 1
    
    if current_step > max_steps:
        step_exceeded = True
        return None
    
    # Get new output since last step
    current_output = output_capture.getvalue()
    new_output = current_output[last_output_pos:].strip()
    last_output_pos = len(current_output)
    
    # Record step
    step_info = {{
        "step": current_step,
        "line": frame.f_lineno,
        "function": frame.f_code.co_name if frame.f_code.co_name != "<module>" else "<module>",
        "variables": safe_snapshot_vars(frame.f_locals),
        "output": new_output
    }}
    
    steps_recorded.append(step_info)
    return trace_function

# Redirect stdout to capture
old_stdout = sys.stdout
sys.stdout = output_capture

stderr_output = ""

# Execute user code with tracing
try:
    code = """{user_code}"""
    compiled = compile(code, '<user_code>', 'exec')
    
    sys.settrace(trace_function)
    exec(compiled, {{'__builtins__': __builtins__}})
    sys.settrace(None)

except Exception as e:
    sys.settrace(None)
    import traceback
    stderr_output = traceback.format_exc()

# Restore stdout and output result
sys.stdout = old_stdout
result = {{
    "steps": steps_recorded,
    "stdout": output_capture.getvalue(),
    "stderr": stderr_output,
    "exceeded": step_exceeded
}}

if step_exceeded:
    result["stderr"] = f"Trace stopped: step limit ({{max_steps}}) reached"

print(json.dumps(result))
'''.format(user_code=code, max_steps=MAX_STEPS)
    
    return trace_script


def trace_execution(code: str, input_data: str = "") -> Dict[str, Any]:
    """
    Execute code with step-by-step tracing.
    
    Returns:
    {{
        "steps": [...],           # Array of step objects
        "stdout": "...",          # Combined stdout output
        "stderr": "...",          # Error messages
        "exceeded": bool          # True if step limit reached
    }}
    
    Guarantees:
    - Proper input handling (stdin streaming)
    - Step-level variable snapshots
    - Output captured per step
    - Timeout enforced
    - Isolated execution
    """
    
    # Syntax check
    try:
        compile(code, '<user_code>', 'exec')
    except SyntaxError as e:
        return {
            "steps": [],
            "stdout": "",
            "stderr": f"SyntaxError: {e.msg} (line {e.lineno})"
        }
    except Exception as e:
        return {
            "steps": [],
            "stdout": "",
            "stderr": f"CompileError: {e}"
        }
    
    filename = None
    try:
        # Create wrapper code
        wrapper = create_trace_wrapper(code, input_data)
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(wrapper)
            filename = f.name
        
        # Set up environment
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUNBUFFERED'] = '1'
        
        # Execute tracer
        process = subprocess.Popen(
            [sys.executable, filename],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        
        try:
            stdout, stderr = process.communicate(
                input=input_data if input_data else None,
                timeout=8.0
            )
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            return {
                "steps": [],
                "stdout": "",
                "stderr": "TraceTimeout: Execution exceeded timeout (possible infinite loop)"
            }
        
        # Parse result from subprocess
        try:
            result = json.loads(stdout)
            return result
        except (json.JSONDecodeError, ValueError):
            return {
                "steps": [],
                "stdout": stdout,
                "stderr": stderr if stderr else "Trace produced invalid output"
            }
    
    except Exception as e:
        return {
            "steps": [],
            "stdout": "",
            "stderr": f"TraceError: {type(e).__name__}: {e}"
        }
    
    finally:
        if filename and os.path.exists(filename):
            try:
                os.unlink(filename)
            except OSError:
                pass
