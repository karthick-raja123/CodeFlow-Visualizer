"""
CodeFlow Visualizer - Vercel Serverless Backend
FastAPI application for executing and tracing Python code.
Deployed as serverless function on Vercel.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import subprocess
import tempfile
import os
import sys
import io
import threading

# Initialize FastAPI app
app = FastAPI(title="CodeFlow Serverless API")

# ── CORS Configuration ────────────────────────────────
ALLOWED_ORIGINS = [
    "https://your-frontend.vercel.app",  # Production
    "http://localhost:5173",              # Development
    "http://localhost:3000",              # Development
    "http://127.0.0.1:5173",             # Development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request/Response Models ───────────────────────────
class CodeRequest(BaseModel):
    code: str = Field(..., max_length=10_000, description="Python code to execute")
    input_data: str = Field(default="", max_length=10_000, description="Input for stdin")


class CodeResponse(BaseModel):
    output: str = Field(description="Standard output")
    error: str = Field(description="Standard error")
    status: str = Field(default="success", description="Execution status")


# ── Code Execution Function ───────────────────────────
def run_code(code: str, input_data: str = "") -> tuple[str, str]:
    """
    Safely execute Python code in a subprocess.
    
    Args:
        code: Python code string to execute
        input_data: Input data for stdin
    
    Returns:
        Tuple of (stdout, stderr)
    """
    try:
        # Create temporary file with code
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_filename = f.name

        try:
            # Execute code in subprocess with timeout
            result = subprocess.run(
                [sys.executable, temp_filename],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=10  # 10 second timeout
            )
            
            return result.stdout, result.stderr
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_filename)
            except:
                pass
    
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timeout (10 seconds)"
    except Exception as e:
        return "", f"Error: {type(e).__name__}: {str(e)}"


# ── Health Check Endpoint ─────────────────────────────
@app.get("/api/health")
async def health():
    """Health check endpoint for Vercel."""
    return {"status": "ok", "service": "CodeFlow Serverless API"}


# ── Execute Code Endpoint ─────────────────────────────
@app.post("/api/execute")
async def execute(req: CodeRequest) -> CodeResponse:
    """
    Execute Python code and return output.
    
    Endpoint: POST /api/execute
    
    Request body:
    {
        "code": "print('Hello')",
        "input_data": ""
    }
    
    Response:
    {
        "output": "Hello\\n",
        "error": "",
        "status": "success"
    }
    """
    try:
        # Check for infinite loops
        if "while True" in req.code and "break" not in req.code:
            return CodeResponse(
                output="",
                error="Error: Infinite loop detected (while True without break)",
                status="error"
            )
        
        if "while 1" in req.code and "break" not in req.code:
            return CodeResponse(
                output="",
                error="Error: Infinite loop detected (while 1 without break)",
                status="error"
            )
        
        # Execute the code
        stdout, stderr = run_code(req.code, req.input_data)
        
        return CodeResponse(
            output=stdout,
            error=stderr,
            status="error" if stderr else "success"
        )
    
    except Exception as e:
        return CodeResponse(
            output="",
            error=f"Server error: {str(e)}",
            status="error"
        )


# ── Trace Endpoint (Simplified) ───────────────────────
class TraceRequest(BaseModel):
    code: str = Field(..., max_length=10_000)
    input_data: str = Field(default="")


class TraceStep(BaseModel):
    line: int
    vars: dict


class TraceResponse(BaseModel):
    steps: list[TraceStep] = []
    stdout: str = ""
    stderr: str = ""
    status: str = "success"


@app.post("/api/trace")
async def trace(req: TraceRequest) -> TraceResponse:
    """
    Trace code execution step-by-step (simplified for serverless).
    Note: Full tracing requires more resources. This is a simplified version.
    """
    try:
        # For serverless, we simplify to just execute
        # Full tracing would require more compute time
        stdout, stderr = run_code(req.code, req.input_data)
        
        return TraceResponse(
            steps=[],  # Simplified: no step-by-step in serverless
            stdout=stdout,
            stderr=stderr,
            status="error" if stderr else "success"
        )
    
    except Exception as e:
        return TraceResponse(
            steps=[],
            stdout="",
            stderr=str(e),
            status="error"
        )


# ── Root Endpoint ─────────────────────────────────────
@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "CodeFlow Visualizer - Serverless Backend",
        "version": "1.0.0",
        "platform": "Vercel",
        "endpoints": {
            "health": "GET /api/health",
            "execute": "POST /api/execute",
            "trace": "POST /api/trace",
            "docs": "/api/docs"
        }
    }


# ── API Documentation Redirect ─────────────────────────
@app.get("/api/docs")
async def api_docs():
    """
    Redirect to interactive API documentation.
    Visit /api/docs (Swagger UI) or /api/redoc (ReDoc)
    """
    return {
        "message": "API Documentation available at:",
        "swagger": "/api/docs",
        "redoc": "/api/redoc"
    }


# ── Error Handlers ────────────────────────────────────
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    """Global exception handler."""
    return {
        "error": "Internal server error",
        "message": str(exc),
        "status": "error"
    }


# ── Vercel Serverless Handler ─────────────────────────
# For Vercel, we need to export the FastAPI app
# This is automatically used by Vercel's Python runtime
handler = app

# Allow direct execution for testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
