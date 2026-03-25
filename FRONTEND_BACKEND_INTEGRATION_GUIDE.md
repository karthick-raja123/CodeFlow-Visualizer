# Frontend-Backend Integration Guide

## Overview
This guide explains how the frontend (React/Vite) connects to the FastAPI backend deployed on Render.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Frontend (Vercel/Netlify/Local)                 │
│        • React + Vite                                    │
│        • src/services/api.js (API client)                │
│        • VITE_API_URL env variable                       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ HTTPS API Calls
                       │ (JSON over HTTP)
                       ▼
┌─────────────────────────────────────────────────────────┐
│    Backend (Render: codeflow-visualizer-1.onrender.com) │
│        • FastAPI Application                             │
│        • CORS enabled for all origins (*)                │
│        • Endpoints: /execute, /trace, /explain           │
└─────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Frontend API Service (`src/services/api.js`)

The API client automatically resolves the backend URL:

- **Development (localhost)**
  - Detects `localhost` in browser URL
  - Uses `http://localhost:8000`

- **Production (Render)**
  - Reads `VITE_API_URL` environment variable
  - Uses `https://codeflow-visualizer-1.onrender.com`

### 2. Environment Variables

Create these files in `frontend/` directory:

**`.env.local`** (local development)
```
VITE_API_URL=http://localhost:8000
```

**`.env.production`** (Render deployment)
```
VITE_API_URL=https://codeflow-visualizer-1.onrender.com
```

### 3. Backend Configuration

**CORS is enabled** in `backend/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This allows the frontend to make requests from any domain.

### 4. API Endpoints

**POST /execute** - Execute Python code
```json
Request:
{
  "code": "print('Hello World')",
  "input_data": ""
}

Response:
{
  "output": "Hello World\n",
  "error": "",
  "stdout": "Hello World\n",
  "stderr": "",
  "exit_code": 0
}
```

**POST /trace** - Trace code execution with steps
```json
Request:
{
  "code": "x = 10\nprint(x)",
  "input_data": ""
}

Response:
{
  "steps": [...execution steps...],
  "stdout": "10\n",
  "stderr": ""
}
```

**GET /health** - Health check
```json
Response:
{
  "status": "ok"
}
```

## Local Development Setup

### Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
# or
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: `http://localhost:8000`

### Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# Vite will open http://localhost:5173
# API calls will automatically use http://localhost:8000
```

## Production Deployment (Render)

### Step 1: Deploy Backend to Render

1. Connect GitHub repo to Render
2. Create new Web Service from repo
3. Configure:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000`
   - **Root Directory**: `./` (if backend is in subdir, use `./backend`)
4. Deploy and note the URL: `https://codeflow-visualizer-1.onrender.com`

### Step 2: Verify Backend Health

```bash
# Test health endpoint
curl https://codeflow-visualizer-1.onrender.com/health
# Response: {"status":"ok"}

# Test execute endpoint
curl -X POST https://codeflow-visualizer-1.onrender.com/execute \
  -H "Content-Type: application/json" \
  -d '{"code":"print(42)","input_data":""}'
# Response: {"output":"42\n","error":"","...}
```

### Step 3: Update Frontend Environment

Update `frontend/.env.production`:
```
VITE_API_URL=https://codeflow-visualizer-1.onrender.com
```

### Step 4: Deploy Frontend

1. Connect frontend directory to Vercel/Netlify/Render
2. Configure build:
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Environment**: Set `VITE_API_URL=https://codeflow-visualizer-1.onrender.com`
3. Deploy

### Step 5: Test End-to-End

1. Open frontend in browser
2. Enter Python code in editor
3. Click "▶ Run"
4. Verify output appears

## Troubleshooting

### Issue: "Connection failed" or CORS error

**Check 1**: Verify backend is running
```bash
curl https://codeflow-visualizer-1.onrender.com/health
```

**Check 2**: Verify correct URL in frontend
```javascript
// Check browser console
console.log(API_HOST); // Should show Render URL
```

**Check 3**: Verify CORS is enabled
Backend should log CORS initialization on startup.

### Issue: 404 Not Found

Verify endpoint exists:
- Backend: `http://localhost:8000/execute`
- Render: `https://codeflow-visualizer-1.onrender.com/execute`

### Issue: Timeout errors

- Code may have infinite loop → set timeout limit
- Backend may be cold-starting on Render → allow 30-60 seconds
- Check Render logs: `Logs` tab in Render dashboard

### Issue: Wrong API URL being used

Frontend uses environment variable `VITE_API_URL`. Verify:

```bash
# Build output should show correct URL
npm run build
# Check dist/index.html for any hardcoded URLs
```

## Request Flow Diagram

```
User enters code in frontend
        ↓
User clicks "Run" button
        ↓
App.jsx calls runCode() from api.js
        ↓
api.js buildUrl() constructs full URL:
  API_HOST + API_PREFIX + /execute
        ↓
fetch() sends POST request with:
  - URL: https://codeflow-visualizer-1.onrender.com/execute
  - Headers: Content-Type: application/json
  - Body: { code, input_data }
        ↓
Backend receives request → CORS check passes (allow_origins=*)
        ↓
FastAPI routes to POST /execute handler
        ↓
run_code() executes Python code
        ↓
Response returned with output/error
        ↓
Frontend receives JSON response
        ↓
Output displayed in OutputConsole component
```

## Files Changed

1. **`frontend/src/App.jsx`**
   - Removed hardcoded localhost API URL
   - Now uses `runCode()` and `traceCode()` from api.js
   - Proper error handling

2. **`frontend/src/services/api.js`**
   - Improved `resolveApiHost()` function
   - Handles Render backend deployments
   - Falls back to environment variable

3. **`frontend/.env.local`** (new)
   - Development configuration
   - Points to `http://localhost:8000`

4. **`frontend/.env.production`** (new)
   - Production configuration
   - Points to Render backend URL

5. **`backend/main.py`**
   - ✅ CORS already configured correctly
   - No changes needed

## Environment Variable Reference

| Variable | Purpose | Development | Production |
|----------|---------|-------------|-----------|
| VITE_API_URL | Backend base URL | http://localhost:8000 | https://codeflow-visualizer-1.onrender.com |
| VITE_API_PREFIX | Optional path prefix | (empty) | (empty) |
| VITE_API_TIMEOUT | Request timeout (ms) | 10000 | 10000 |

## Next Steps

1. ✅ Verify backend health: `GET /health`
2. ✅ Test backend locally: `POST /execute` with sample code
3. ✅ Update `.env.production` with correct Render URL
4. ✅ Deploy backend to Render
5. ✅ Deploy frontend to Vercel/Netlify/Render
6. ✅ Test end-to-end in production
7. ✅ Monitor logs for any connection issues

---

**Questions?** Check the browser console (F12) for detailed error messages and network logs.
