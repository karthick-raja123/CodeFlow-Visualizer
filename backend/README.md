# CodeFlow Visualizer - Backend

FastAPI-based backend service for CodeFlow Visualizer. Handles code execution, tracing, and AI-powered explanations.

## 🔧 Installation

### Prerequisites
- **Python 3.10+**
- **pip** or **poetry**

### Steps

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate virtual environment:
   
   **Windows (PowerShell):**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   **Windows (CMD):**
   ```cmd
   .\.venv\Scripts\activate.bat
   ```
   
   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create `.env` file (optional):
   ```bash
   cp ../.env.example .env
   ```

---

## 🚀 Running the Server

### Development Mode (with auto-reload)

```bash
python -m uvicorn main:app --reload --port 8000
```

The API will be available at:
- **Server**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

### Production Mode

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📚 API Endpoints

### 1. **Execute Code**
```http
POST /api/execute
Content-Type: application/json

{
  "code": "print('Hello, World!')",
  "input": ""
}
```

**Response:**
```json
{
  "status": "success",
  "output": "Hello, World!\n",
  "error": null
}
```

---

### 2. **Trace Execution (Step-by-step)**
```http
POST /api/trace
Content-Type: application/json

{
  "code": "x = 5\ny = x + 3",
  "input": ""
}
```

**Response:**
```json
{
  "status": "success",
  "trace": [
    {
      "line": 1,
      "event": "line",
      "locals": {"x": 5}
    },
    {
      "line": 2,
      "event": "line",
      "locals": {"x": 5, "y": 8}
    }
  ],
  "output": ""
}
```

---

### 3. **Get AI Explanation**
```http
POST /api/explain
Content-Type: application/json

{
  "code": "x = 5",
  "step_index": 0
}
```

**Response:**
```json
{
  "status": "success",
  "explanation": "Variable x is assigned the value 5"
}
```

---

### 4. **Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## 📂 Project Structure

```
backend/
├── main.py               # FastAPI app & routes
├── executor.py           # Safe code execution
├── tracer.py             # Step-by-step tracing
├── explainer.py          # AI-powered explanations
├── flow_analyzer.py      # Flow diagram generation
├── database.py           # Database models (future)
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

---

## 🔒 Security Features

- **Isolated Execution**: Code runs in isolated subprocess
- **Timeout Protection**: 10-second execution limit
- **Resource Limits**: Prevents infinite loops
- **Input Validation**: Pydantic validation for all inputs
- **CORS Configuration**: Secure cross-origin requests
- **No Arbitrary Code Access**: Sandboxed environment

---

## 🛠️ Core Modules

### `main.py`
- FastAPI application setup
- Route definitions
- CORS middleware configuration
- Health endpoint

### `executor.py`
- `execute_code()`: Safely runs Python code
- `detect_infinite_loop()`: Loop detection
- Timeout handling

### `tracer.py`
- `trace_execution()`: Step-by-step execution tracing
- Stack frame extraction
- Variable state capture

### `explainer.py`
- `explain_code()`: Pattern-based explanations
- Concept identification
- Tip generation

### `flow_analyzer.py`
- `generate_flow()`: AST-based flow diagram
- Node creation (Start, Process, Decision, End)
- Edge relationships

---

## 📦 Dependencies

Key dependencies (see `requirements.txt` for versions):
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **requests**: HTTP client

---

## 🧪 Testing

Run tests (when available):
```bash
pytest
```

---

## 🔧 Configuration

Set environment variables in `.env`:
```
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
APP_ENV=development
```

---

## 📝 Logging

Logs are output to console. For production, configure file-based logging:
```python
# Add to main.py
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
```

---

## 🚀 Deployment

For production deployment:
1. Use a production ASGI server (Gunicorn + Uvicorn)
2. Set `APP_ENV=production`
3. Configure proper CORS origins
4. Use environment variables for secrets
5. Enable HTTPS
6. Set up monitoring and logging

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Change port: `--port 8001` |
| Module not found | Ensure venv is activated and dependencies installed |
| CORS error | Check `ALLOWED_ORIGINS` in `.env` |
| Timeout errors | Reduce timeout or optimize code |

---

## 🤝 Contributing

Contributions welcome! Please:
1. Create feature branch
2. Add tests
3. Submit pull request

---

## 📄 License

MIT License - See LICENSE file for details.

---

**Made with ❤️ by [@karthick-raja123](https://github.com/karthick-raja123)**
