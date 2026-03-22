from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import subprocess
import tempfile
import os
import sys
import io
import threading

TRACE_MAX_STEPS = 200
TRACE_TIMEOUT = 8  # seconds


def _safe_repr(value: object) -> str:
    """Best-effort repr that never explodes and stays short."""
    try:
        text = repr(value)
        return text if len(text) <= 100 else text[:97] + "..."
    except Exception:
        return "<unrepr>"


app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request model
class CodeRequest(BaseModel):
    code: str
    input_data: str = ""

# ✅ Root / health check
@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ✅ Execute code
@app.post("/execute")
def execute_code(req: CodeRequest):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
            f.write(req.code.encode())
            filename = f.name

        result = subprocess.run(
            ["python", filename],
            input=req.input_data,
            text=True,
            capture_output=True,
            timeout=5
        )

        os.remove(filename)

        return {
            "output": result.stdout,
            "error": result.stderr,
            "status": "success"
        }

    except Exception as e:
        return {
            "output": "",
            "error": str(e),
            "status": "error"
        }

def _run_trace(code: str, input_data: str, result_holder: dict):
    steps = []
    hit_limit = False
    code_lines = code.splitlines()

    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    old_stdout, old_stderr, old_stdin = sys.stdout, sys.stderr, sys.stdin
    sys.stdout, sys.stderr = stdout_capture, stderr_capture
    if input_data:
        sys.stdin = io.StringIO(input_data)

    def tracer(frame, event, arg):
        nonlocal hit_limit
        if frame.f_code.co_filename != "<user_code>":
            return tracer
        if event == "line":
            if len(steps) >= TRACE_MAX_STEPS:
                hit_limit = True
                return None
            locals_snapshot = {
                name: _safe_repr(val)
                for name, val in frame.f_locals.items()
                if not name.startswith("__")
            }
            line_no = frame.f_lineno
            line_text = code_lines[line_no - 1] if 0 < line_no <= len(code_lines) else ""
            steps.append({
                "line": line_no,
                "code": line_text,
                "vars": locals_snapshot,
            })
        return tracer

    error_text = ""
    try:
        compiled = compile(code, "<user_code>", "exec")
        exec_globals = {"__builtins__": __builtins__}
        sys.settrace(tracer)
        exec(compiled, exec_globals, exec_globals)
    except Exception as exc:  # capture runtime errors inside tracer
        error_text = f"{type(exc).__name__}: {exc}"
    finally:
        sys.settrace(None)
        sys.stdout, sys.stderr = old_stdout, old_stderr
        sys.stdin = old_stdin

    stderr_output = error_text or stderr_capture.getvalue()
    if hit_limit:
        stderr_output = (stderr_output + "\n" if stderr_output else "") + f"Trace stopped: {TRACE_MAX_STEPS} step limit reached"

    result_holder["steps"] = steps
    result_holder["stdout"] = stdout_capture.getvalue()
    result_holder["stderr"] = stderr_output.strip()


def trace_execution(code: str, input_data: str = "") -> dict:
    if "while True" in code and "break" not in code:
        return {"steps": [], "stdout": "", "stderr": "Error: Infinite loop detected (while True without break)."}
    if "while 1" in code and "break" not in code:
        return {"steps": [], "stdout": "", "stderr": "Error: Infinite loop detected (while 1 without break)."}

    result = {"steps": [], "stdout": "", "stderr": ""}
    worker = threading.Thread(target=_run_trace, args=(code, input_data, result), daemon=True)
    worker.start()
    worker.join(timeout=TRACE_TIMEOUT)

    if worker.is_alive():
        return {
            "steps": result.get("steps", []),
            "stdout": result.get("stdout", ""),
            "stderr": "Trace stopped: execution timeout (8s). Code may contain an infinite loop.",
        }

    return result


# ✅ Trace code
@app.post("/trace")
def trace_code(req: CodeRequest):
    result = trace_execution(req.code, req.input_data)
    status = "error" if result.get("stderr") else "success"
    return {
        "steps": result.get("steps", []),
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "status": status,
    }


# ✅ AI Explanation endpoint
class ExplainRequest(BaseModel):
    code: str
    step_data: dict
    prev_step: Optional[dict] = None

@app.post("/explain")
def explain_step(req: ExplainRequest):
    """Provide AI explanation for a code step."""
    try:
        step_data = req.step_data
        line_num = step_data.get("line", 0)
        vars_dict = step_data.get("vars", {})
        
        # Build a simple explanation
        explanation = f"Line {line_num}: "
        if vars_dict:
            var_names = ", ".join(vars_dict.keys())
            explanation += f"Variables: {var_names}"
        else:
            explanation += "No local variables yet"
        
        return {
            "explanation": explanation,
            "detail": f"Executing line {line_num} of the code",
            "suggestion": "Step through the code to see how variables change",
            "concept": "Code Execution"
        }
    except Exception as e:
        return {
            "explanation": f"Error: {str(e)}",
            "detail": "Could not generate explanation",
            "suggestion": "Check the code for syntax errors",
            "concept": "Error Handling"
        }


# ── Vercel Serverless Handler ─────────────────────────
# For Vercel, we need to export the FastAPI app
# This is automatically used by Vercel's Python runtime
handler = app

# Allow direct execution for testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
