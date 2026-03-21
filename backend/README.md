# Backend — CodeFlow API

FastAPI backend for code execution, step tracing, and AI explanations.

## Setup

```bash
# From project root
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

pip install -r backend/requirements.txt
```

## Run

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

Server starts at **http://localhost:8000**

## API Endpoints

### POST /execute
Execute Python code.
```json
{
  "code": "print('hello')",
  "input_data": ""
}
```
Response:
```json
{
  "output": "hello\n",
  "error": "",
  "exit_code": 0
}
```

### POST /trace
Trace execution step-by-step.
```json
{
  "code": "x = 5\nprint(x)",
  "input_data": ""
}
```
Response:
```json
{
  "steps": [
    { "line": 1, "vars": { "x": "5" } },
    { "line": 2, "vars": { "x": "5" } }
  ],
  "stdout": "5\n",
  "stderr": ""
}
```

### POST /explain
Get AI explanation for a step.

### GET /health
Health check — returns `{"status": "ok"}`

## Architecture

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app, routes, tracer |
| `executor.py` | subprocess.Popen runner (10s timeout) |
| `explainer.py` | Pattern-based code explanations |
| `tracer.py` | sys.settrace step capture |

## Safety

- Infinite loop detection (`while True` without `break`)
- 10s subprocess timeout with `process.kill()`
- 8s tracer timeout with daemon thread
- 200 step limit for tracing
- Max 10KB code input
