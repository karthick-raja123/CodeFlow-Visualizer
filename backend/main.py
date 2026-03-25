"""
CodeFlow Visualizer — FastAPI Backend
Execute, trace, and explain Python code.
All endpoints guaranteed to respond within 10 seconds.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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
from backend.executor import run_code


# ── Tracer (subprocess-based with proper isolation) ──
from backend.tracer import trace_execution


# ── Explainer ─────────────────────────────────────────
from backend.explainer import explain_step


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
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
