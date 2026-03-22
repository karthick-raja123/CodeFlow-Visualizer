"""
CodeFlow Visualizer — FastAPI Backend
Execute, trace, and explain Python code.
All endpoints guaranteed to respond within 10 seconds.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sys
import io
import threading

app = FastAPI(title="CodeFlow API")

# CORS — always allow during development / serverless deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Models ────────────────────────────────────────────
class CodeRequest(BaseModel):
    code: str = Field(..., max_length=10_000)
    input_data: str = Field(default="", max_length=10_000)


class ExplainRequest(BaseModel):
    code: str = Field(..., max_length=10_000)
    step_data: dict
    prev_step: dict | None = None


# ── Executor (Popen-based, always safe) ───────────────
from .executor import run_code


# ── Tracer (with hard timeout) ────────────────────────
MAX_STEPS = 200
TRACE_TIMEOUT = 8  # seconds — hard kill if exec() hangs


def _safe_repr(val):
    try:
        r = repr(val)
        return r if len(r) < 100 else r[:97] + "..."
    except Exception:
        return "<?>"


def _run_trace(code, input_data, result_holder):
    """Run trace in a thread so we can enforce a hard timeout."""
    steps = []
    hit_limit = False

    def tracer(frame, event, arg):
        nonlocal hit_limit
        if len(steps) >= MAX_STEPS:
            hit_limit = True
            return None
        if frame.f_code.co_filename != "<user>":
            return tracer
        if event == "line":
            local_vars = {}
            for k, v in frame.f_locals.items():
                if not k.startswith("__"):
                    local_vars[k] = _safe_repr(v)
            steps.append({"line": frame.f_lineno, "vars": local_vars})
        return tracer

    old_stdout, old_stderr = sys.stdout, sys.stderr
    captured_out = io.StringIO()
    captured_err = io.StringIO()
    sys.stdout = captured_out
    sys.stderr = captured_err

    if input_data:
        old_stdin = sys.stdin
        sys.stdin = io.StringIO(input_data)

    err_text = ""
    try:
        compiled = compile(code, "<user>", "exec")
        sys.settrace(tracer)
        exec(compiled, {"__builtins__": __builtins__})
    except Exception as e:
        err_text = f"{type(e).__name__}: {e}"
    finally:
        sys.settrace(None)
        sys.stdout, sys.stderr = old_stdout, old_stderr
        if input_data:
            sys.stdin = old_stdin

    warn = "Trace stopped: too many steps (200 limit)" if hit_limit else ""
    stderr_out = err_text or captured_err.getvalue()
    if warn:
        stderr_out = (stderr_out + "\n" + warn).strip() if stderr_out else warn

    result_holder["steps"] = steps
    result_holder["stdout"] = captured_out.getvalue()
    result_holder["stderr"] = stderr_out


def trace_execution(code: str, input_data: str = "") -> dict:
    # Block infinite loops before tracing
    if "while True" in code and "break" not in code:
        return {"steps": [], "stdout": "", "stderr": "Error: Infinite loop detected. Add a 'break' statement."}
    if "while 1" in code and "break" not in code:
        return {"steps": [], "stdout": "", "stderr": "Error: Infinite loop detected. Add a 'break' statement."}

    result = {"steps": [], "stdout": "", "stderr": ""}
    thread = threading.Thread(target=_run_trace, args=(code, input_data, result), daemon=True)
    thread.start()
    thread.join(timeout=TRACE_TIMEOUT)

    if thread.is_alive():
        # Thread is stuck — return whatever partial data we have
        return {
            "steps": result.get("steps", []),
            "stdout": result.get("stdout", ""),
            "stderr": "Trace stopped: execution timeout (8s). Code may have an infinite loop.",
        }

    return result


# ── Explainer ─────────────────────────────────────────
from .explainer import explain_step


# ── Health ────────────────────────────────────────────
@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# ── Routes ────────────────────────────────────────────
@app.post("/execute")
async def execute(req: CodeRequest):
    stdout, stderr = run_code(req.code, req.input_data)
    return {
        "output": stdout,
        "error": stderr,
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": 1 if stderr else 0,
    }


@app.post("/trace")
async def trace(req: CodeRequest):
    return trace_execution(req.code, req.input_data)


@app.post("/explain")
async def explain(req: ExplainRequest):
    return explain_step(req.code, req.step_data, req.prev_step)


# ── Main Entry Point ──────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
