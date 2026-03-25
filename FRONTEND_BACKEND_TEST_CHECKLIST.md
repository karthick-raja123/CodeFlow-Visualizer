# Frontend-Backend Connection Test Checklist

## Quick Test Guide

### ✅ Step 1: Backend Health Check

```bash
# Test the health endpoint
curl https://codeflow-visualizer-1.onrender.com/health

# Expected response:
# {"status":"ok"}

# Alternative (browser):
# Open: https://codeflow-visualizer-1.onrender.com/health
```

### ✅ Step 2: Test Execute Endpoint

```bash
# Send test code to backend
curl -X POST https://codeflow-visualizer-1.onrender.com/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello from Backend!\")",
    "input_data": ""
  }'

# Expected response:
# {
#   "output": "Hello from Backend!\n",
#   "error": "",
#   "stdout": "Hello from Backend!\n",
#   "stderr": "",
#   "exit_code": 0
# }
```

### ✅ Step 3: Test Frontend to Backend Connection

#### Browser Console Test

1. Open frontend in browser
2. Press F12 to open Developer Tools
3. Go to Console tab
4. Paste the following:

```javascript
// Test 1: Check if API URL is configured correctly
console.log('Testing API connection...');

// Test 2: Make a test request
fetch('https://codeflow-visualizer-1.onrender.com/health')
  .then(r => r.json())
  .then(d => console.log('✅ Health check passed:', d))
  .catch(e => console.error('❌ Health check failed:', e));

// Test 3: Test execute endpoint
fetch('https://codeflow-visualizer-1.onrender.com/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ code: 'print(42)', input_data: '' })
})
  .then(r => r.json())
  .then(d => console.log('✅ Execute endpoint works:', d.output))
  .catch(e => console.error('❌ Execute endpoint failed:', e));
```

### ✅ Step 4: Test Frontend UI

1. Enter code in code editor:
```python
x = 5
y = 10
print(x + y)
```

2. Click **▶ Run** button

3. Expected output in Results panel:
```
15
```

4. If error appears, check Section "Debug Errors" below

### ✅ Step 5: Test Trace Feature

1. Enter code:
```python
for i in range(3):
    print(i)
```

2. Click **🔍 Trace** button

3. Click ▶ to step through execution

4. Variables should update at each step

---

## Debug: Network Request Inspection

### Using Browser DevTools

1. Open **Developer Tools** (F12 or Ctrl+Shift+I)
2. Go to **Network** tab
3. Click **Run** button in app
4. Look for request to `/execute`

**Check the request:**
- **URL**: Should be `https://codeflow-visualizer-1.onrender.com/execute`
- **Method**: Should be `POST`
- **Status**: Should be `200` (success) or `201`

**Check the response:**
- Click on the request to expand
- Go to **Response** tab
- Should see JSON with `output` and `error` fields

**Check headers:**
- Go to **Headers** tab
- Request should have: `Content-Type: application/json`
- Response should have: `access-control-allow-origin: *` (CORS)

### Network Errors

| Error | Cause | Solution |
|-------|-------|----------|
| **0 (failed)** | Network unreachable | Check internet, backend URL |
| **404** | Endpoint not found | Verify `/execute` path exists |
| **301/302** | Redirect | Check if URL needs trailing slash |
| **500** | Server error | Check backend logs |
| **CORS error** | Missing CORS header | CORS is enabled in backend |

---

## Debug: Environment Variable Check

### Verify Frontend Configuration

Check what URL the frontend is actually using:

**Option 1: Browser Console**
```javascript
// Add this to src/App.jsx or paste in console
console.log('API_HOST:', API_HOST);
console.log('API_PREFIX:', API_PREFIX);
console.log('Full URL:', buildUrl('/execute'));

// Expected output (for Render production):
// API_HOST: https://codeflow-visualizer-1.onrender.com
// API_PREFIX: (empty)
// Full URL: https://codeflow-visualizer-1.onrender.com/execute
```

**Option 2: Check Environment Variables**
```bash
# Local development - check .env.local
cat frontend/.env.local
# Should show: VITE_API_URL=http://localhost:8000

# Production - check .env.production
cat frontend/.env.production
# Should show: VITE_API_URL=https://codeflow-visualizer-1.onrender.com
```

### Verify Build Output

```bash
# Check what was baked into the build
cat dist/index.html | grep -i "api\|render"

# Look for any hardcoded URLs in:
ls -la dist/assets/
file dist/assets/*.js
```

---

## Common Issues & Solutions

### Issue 1: "Connection failed"

**Checklist:**
- [ ] Backend is deployed to Render (`https://codeflow-visualizer-1.onrender.com`)
- [ ] Backend health check passes: `GET /health`
- [ ] Frontend URL matches backend: `VITE_API_URL=https://codeflow-visualizer-1.onrender.com`
- [ ] No CORS errors in browser console

**Solution:**
```bash
# Test backend directly
curl -I https://codeflow-visualizer-1.onrender.com/health

# If fails, check Render logs:
# 1. Go to Render dashboard
# 2. Select your service
# 3. Click "Logs" tab
# 4. Look for errors
```

### Issue 2: CORS Error (blocked by browser)

**Error message:** `Access to XMLHttpRequest has been blocked...`

**Solution:**
- Verify backend has CORS enabled
- Check response headers: `access-control-allow-origin: *`
- If missing, add CORS middleware to `backend/main.py`

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 3: 404 Not Found

**Error message:** `POST /execute - 404 Not Found`

**Solution:**
- Verify endpoint exists in backend
- Check URL spelling: `/execute` (not `/api/execute`)
- Check backend is running: `GET /health`

### Issue 4: Request Timeout

**Error message:** `Request timed out after 10s`

**Possible causes:**
- Render backend is cold-starting (first request after idle period)
- Code has infinite loop
- Backend is overloaded

**Solutions:**
1. Wait 30-60 seconds for Render to warm up first request
2. Check code for infinite loops
3. Increase timeout in `api.js` if needed

### Issue 5: Wrong API URL

**Problem:** Frontend is still using `http://localhost:8000` in production

**Verify:**
```bash
# Check .env.production exists and has correct URL
cat frontend/.env.production
# VITE_API_URL=https://codeflow-visualizer-1.onrender.com

# Rebuild frontend
npm run build

# Check dist/
ls -la dist/
```

**If still wrong:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Clear `node_modules` and `.vite`
3. Reinstall: `npm install`
4. Rebuild: `npm run build`

---

## Success Indicators

✅ **You'll know it's working when:**

- [ ] Health check returns `{"status":"ok"}`
- [ ] Execute request returns JSON with `output` and `error` fields
- [ ] Frontend code executes and shows output in UI
- [ ] No console errors in browser developer tools
- [ ] No CORS errors
- [ ] Response time is < 1 second (after warm-up)

---

## Still Having Issues?

### Collect Debug Info

Run this script and share the output:

```bash
# Backend test
echo "=== Backend Health ==="
curl -s https://codeflow-visualizer-1.onrender.com/health | jq .

# Frontend test (in browser console)
# F12 → Console → paste:
console.log(
  'Frontend Config:',
  {
    api_url: import.meta.env.VITE_API_URL,
    hostname: window.location.hostname,
    origin: window.location.origin,
  }
);

# Network test
# F12 → Network → Click "Run" → share screenshot showing:
# - Request URL
# - Status code
# - Response headers
# - Response body
```

### Check Logs

**Backend (Render):**
1. Go to https://render.com/
2. Select your service
3. Click "Logs"
4. Check for errors

**Frontend (Vercel/Netlify/Render):**
1. Go to hosting dashboard
2. Find Deployments
3. Click recent deployment
4. Check build logs
5. Check runtime logs

---

Last updated: 2026-03-25
