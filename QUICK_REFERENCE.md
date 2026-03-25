# Quick Reference Card

## URLs & Endpoints

```
# Backend (Render)
Base URL: https://codeflow-visualizer-1.onrender.com
Health:   GET  https://codeflow-visualizer-1.onrender.com/health
Execute:  POST https://codeflow-visualizer-1.onrender.com/execute
Trace:    POST https://codeflow-visualizer-1.onrender.com/trace
Explain:  POST https://codeflow-visualizer-1.onrender.com/explain

# Backend (Local Development)  
Base URL: http://localhost:8000
Health:   GET  http://localhost:8000/health
Execute:  POST http://localhost:8000/execute

# Frontend (Local Development)
Dev:      http://localhost:5173
```

## Configuration Files

```
frontend/.env.local (DEV)
  VITE_API_URL=http://localhost:8000

frontend/.env.production (PROD)
  VITE_API_URL=https://codeflow-visualizer-1.onrender.com
```

## Test Commands

```bash
# Health check
curl https://codeflow-visualizer-1.onrender.com/health

# Execute test code
curl -X POST https://codeflow-visualizer-1.onrender.com/execute \
  -H "Content-Type: application/json" \
  -d '{"code":"print(42)","input_data":""}'

# Expected response:
# {"output":"42\n","error":"","stdout":"42\n","stderr":"","exit_code":0}
```

## Request/Response Format

### POST /execute

**Request:**
```json
{
  "code": "print('Hello World')",
  "input_data": ""
}
```

**Response:**
```json
{
  "output": "Hello World\n",
  "error": "",
  "stdout": "Hello World\n",
  "stderr": "",
  "exit_code": 0
}
```

## Key Files Modified

```
frontend/src/App.jsx
  ✓ Removed hardcoded localhost
  ✓ Uses API service functions

frontend/src/services/api.js
  ✓ Improved environment detection

frontend/.env.local (NEW)
  ✓ Dev configuration

frontend/.env.production (NEW)
  ✓ Prod configuration

backend/main.py
  ✓ CORS already configured (no changes needed)
```

## Deployment Checklist

- [ ] Backend deployed to Render
- [ ] Backend health check passes
- [ ] Frontend .env.production updated with backend URL
- [ ] Frontend deployed to Render/Vercel
- [ ] Test end-to-end: Enter code → Run → See output
- [ ] Monitor logs for errors

## Troubleshooting Flowchart

```
Frontend shows "Connection failed"
    ↓
1. Test backend: curl /health endpoint
    ├─ Works? → 2. Check API URL in env vars
    └─ Fails? → Backend not running
              → Check Render logs

2. Check API URL
    ├─ Points to backend URL? → 3. Check CORS
    └─ Points to localhost? → Update .env.production
                             → Rebuild frontend

3. Check CORS
    ├─ Response has access-control-allow-origin header? → Might be caching issue
    │   Clear browser cache → Reload
    └─ No header? → Backend CORS not enabled
                  → Check backend/main.py
```

## Environment Variable Resolution

```javascript
// Development (localhost:5173)
detected: localhost
resolved: http://localhost:8000

// Production (vercel.app)
env var: VITE_API_URL (if set)
fallback: window.location.origin
resolved: https://your-frontend.vercel.app (unless env var overrides)

// Production (Render)
env var: VITE_API_URL=https://codeflow-backend.onrender.com
resolved: https://codeflow-backend.onrender.com
```

## Code Examples

### Using Frontend API Service

```javascript
import { runCode, traceCode, getExplanation } from './services/api';

// Run code
const result = await runCode("print(42)", "");
console.log(result.output);  // "42\n"

// Trace with steps
const trace = await traceCode("x = 10\nprint(x)", "");
console.log(trace.steps);    // [step1, step2, ...]

// Get explanation
const explanation = await getExplanation(code, stepData);
```

### Direct fetch (if needed)

```javascript
const response = await fetch('https://codeflow-visualizer-1.onrender.com/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: "print('test')",
    input_data: ""
  })
});

const data = await response.json();
console.log(data.output);
```

## Environment Variables Reference

| Variable | Value | Used By |
|----------|-------|---------|
| VITE_API_URL | Backend URL | Frontend builds |
| VITE_API_PREFIX | Path prefix | Frontend API service |
| VITE_API_TIMEOUT | Request timeout in ms | Frontend API service |
| VITE_ENABLE_SESSIONS | true/false | Frontend feature flag |

## Render Configuration

### Backend Service
```
Name: codeflow-backend
Runtime: Python
Build: pip install -r backend/requirements.txt
Start: cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
Region: Any
Instance: Free tier OK
```

### Frontend Service
```
Name: codeflow-frontend  
Runtime: Node
Root: frontend
Build: npm install && npm run build
Start: npm run preview
Output: dist
Env: VITE_API_URL=https://codeflow-backend.onrender.com
```

## Common HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | ✓ Working |
| 404 | Not Found | Check endpoint path |
| 500 | Server Error | Check backend logs |
| 0 | Network Error | Check URL, internet |
| (CORS) | Cross-origin | CORS enabled but check origin |

## Browser DevTools Tips

```javascript
// Check API URL being used (paste in console)
console.log('API Host:', API_HOST);

// Test health endpoint
fetch('https://codeflow-visualizer-1.onrender.com/health')
  .then(r => r.json())
  .then(d => console.log('Status:', d));

// Test execute endpoint
fetch('https://codeflow-visualizer-1.onrender.com/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ code: 'print(42)', input_data: '' })
})
  .then(r => r.json())
  .then(d => console.log('Output:', d.output));
```

## Log File Locations

```
Backend (Render): Dashboard → Service → Logs
Frontend (Render): Dashboard → Service → Logs
Frontend (Browser): F12 → Console
Frontend (Network): F12 → Network tab
```

## Important Notes

⚠️ **Do not use `http://localhost:8000` in production**
⚠️ **Always set VITE_API_URL for production deployments**
⚠️ **Clear browser cache if changes don't appear**
⚠️ **First requests to Render may take 30-60 seconds (cold start)**
⚠️ **Check both frontend and backend logs when debugging**

---

**Last Updated:** March 25, 2026
