# 🚀 Deploy CodeFlow Visualizer to Vercel

**Full-Stack Serverless Deployment (Frontend + Backend)**

---

## ✅ What You Get

- **Frontend**: React app deployed on Vercel CDN (fast, global)
- **Backend**: FastAPI serverless API on Vercel Functions
- **Zero servers**: No need to manage infrastructure
- **Auto-scaling**: Handles traffic automatically
- **Custom domain**: Use your own domain

---

## 📋 Pre-Deployment Checklist

- [x] **api/index.py** - Serverless FastAPI handler
- [x] **api/requirements.txt** - Python dependencies
- [x] **vercel.json** - Configuration for both frontend and backend
- [x] **src/services/api.js** - Updated API client with /api/execute
- [x] **.env.example** - Backend URL set to /api
- [x] Code pushed to GitHub

---

## 🎯 Deployment Steps (5 Minutes)

### Step 1️⃣: Sign Up on Vercel
Visit **https://vercel.com** and sign up with GitHub

### Step 2️⃣: Import Project
1. Click **Add New...** → **Project**
2. Select **Import Git Repository**
3. Search for `Python-Visualizer`
4. Click **Import**

### Step 3️⃣: Configure Project Settings
Vercel will auto-detect the project type. You should see:
```
Framework Preset:   Other (Vite)
Build Command:      npm run build
Output Directory:   dist
```

**Leave as is** (Vercel will handle both frontend and API)

### Step 4️⃣: Set Environment Variables (if needed)
In **Settings** → **Environment Variables**, add:
```
VITE_API_URL = /api
```
(Optional: Only needed if you want to override the default)

### Step 5️⃣: Deploy
Click **Deploy** and wait ~2-3 minutes

**🎉 Your site is live!**

```
https://your-project-name.vercel.app
```

---

## 📂 Project Structure for Vercel

```
/
├── api/                          ← Serverless backend
│   ├── index.py                  ← FastAPI handler
│   └── requirements.txt           ← Python dependencies
├── src/                          ← React frontend
│   ├── services/
│   │   └── api.js               ← Updated to use /api
│   └── ...
├── public/                       ← Static assets
├── package.json                  ← Node dependencies
├── vite.config.js                ← Vite config
├── vercel.json                   ← Vercel config (UPDATED)
├── .env.example                  ← Env template (UPDATED)
└── README.md
```

---

## 🔧 How It Works

### Frontend Request Flow
```
Browser Request
    ↓
Vercel CDN (Next.js, Vite, React)
    ↓
User sees the React app
    ↓
Click "Run Code" button
    ↓
JavaScript calls fetch('/api/execute')
    ↓
Vercel Routes to api/index.py
    ↓
Python FastAPI processes request
    ↓
Runs code in subprocess (10s timeout)
    ↓
Returns JSON response
    ↓
JavaScript displays output
```

---

## 🔌 API Endpoints

Your serverless API provides these endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/execute` | `POST` | Execute Python code |
| `/api/trace` | `POST` | Trace code execution |
| `/api/health` | `GET` | Health check |
| `/api/docs` | `GET` | API documentation |

### Example Request
```bash
curl https://your-app.vercel.app/api/execute \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello Vercel!\")",
    "input_data": ""
  }'
```

### Example Response
```json
{
  "output": "Hello Vercel!\n",
  "error": "",
  "status": "success"
}
```

---

## 📝 Configuration Files Explained

### `api/index.py`
```python
# Serverless FastAPI application
app = FastAPI()

@app.post("/api/execute")
async def execute(req: CodeRequest) -> CodeResponse:
    # Executes Python code safely
    # Returns output and errors
```

**Key Features:**
- Subprocess execution (safe sandbox)
- 10-second timeout protection
- Infinite loop detection
- CORS enabled for frontend

### `api/requirements.txt`
```
fastapi==0.115.0
uvicorn==0.30.0
pydantic==2.9.0
```

**Why these?**
- **fastapi**: Web framework (extremely fast)
- **uvicorn**: ASGI server (serverless compatible)
- **pydantic**: Input validation

### `vercel.json`
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "functions": {
    "api/index.py": {
      "runtime": "python3.9",
      "maxDuration": 30
    }
  },
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

**Routing:**
- Requests to `/api/*` → Handled by `api/index.py`
- All other requests → Served from `dist/` (frontend)

### `src/services/api.js`
```javascript
const API_BASE = process.env.VITE_API_URL || '/api';

async function callBackend(code, input_data = '') {
  const res = await fetch(`${API_BASE}/execute`, {
    method: 'POST',
    body: JSON.stringify({ code, input_data })
  });
  return res.json();
}
```

**Why this works:**
- Uses relative path `/api` (works on Vercel)
- Falls back to `process.env.VITE_API_URL` if set
- No hardcoded localhost (serverless compatible)

---

## 🧪 Test Your Deployment

### 1. Check Frontend
Visit: `https://your-app.vercel.app`

You should see the React app loaded.

### 2. Check Backend
Visit: `https://your-app.vercel.app/api/health`

You should see:
```json
{"status": "ok", "service": "CodeFlow Serverless API"}
```

### 3. Test Code Execution
In the React app, write code and click **Run**

Example:
```python
x = 5
y = 10
print(x + y)
```

Should output: `15`

### 4. Check API Docs
Visit: `https://your-app.vercel.app/api/docs`

Interactive Swagger documentation (if accessing via /api/docs endpoint)

---

## 📊 Vercel Dashboard

After deployment, you can monitor your app:

1. **Deployments** tab:
   - View deployment history
   - Rollback to previous versions

2. **Logs** tab:
   - See real-time logs from your serverless functions
   - Debug API errors

3. **Analytics** tab:
   - Response times
   - Request counts
   - Error rates

4. **Settings** tab:
   - Add custom domain
   - Configure environment variables
   - Set up GitHub integration

---

## 🔄 Auto-Deploy on Push

Vercel automatically redeploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "feat: add new feature"
git push origin main

# Vercel detects the push and redeploys automatically
```

---

## 💰 Pricing & Limits

### Free Tier
- **Serverless Functions**: 100GB/month bandwidth
- **Execution Time**: 10 seconds per function call
- **Memory**: 512MB per function
- **Concurrent Executions**: Limited but sufficient for most apps

### For High Traffic
Upgrade to Professional ($20/month):
- Priority support
- 100 concurrent functions
- No bandwidth limits

---

## 🐛 Troubleshooting

### API Not Responding
**Error**: `Failed to fetch /api/execute`

**Solution**:
1. Check Vercel logs: Dashboard → Logs
2. Ensure `api/index.py` exists
3. Ensure `vercel.json` routes are correct

### CORS Errors
**Error**: `Access-Control-Allow-Origin`

**Solution**:
Ensure `src/services/api.js` uses `/api` path:
```javascript
const API_BASE = process.env.VITE_API_URL || '/api';
```

### Timeout Errors
**Error**: `Code execution timeout`

**Solution**:
- Code execution is limited to 10 seconds
- Optimize your code or upgrade Vercel plan

### Cold Start (First Request Slow)
**Normal**: First request takes 2-5 seconds

**Why**: Vercel spins up a new container
**Solution**: First request is slow, subsequent requests are fast

---

## 📈 Optimization Tips

### 1. Cache Assets
Vercel automatically caches static assets (CSS, JS, images)

### 2. Incremental Static Generation
Not applicable for this project, but useful for future optimization

### 3. Database Connection Pooling
If you add a database later, use connection pooling:
```python
# Example: Prisma, SQLAlchemy connection pool
```

### 4. Request Bundling
The frontend already bundles requests efficiently with Vite

---

## 🔐 Security Considerations

### 1. Environment Variables
Never commit `.env`:
```bash
# .gitignore
.env
.env.local
```

### 2. API Rate Limiting
Consider adding rate limiting for production:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/execute")
@limiter.limit("10/minute")  # 10 requests per minute
async def execute(req: CodeRequest):
    ...
```

### 3. Input Validation
Already done with Pydantic in `api/index.py`:
```python
class CodeRequest(BaseModel):
    code: str = Field(..., max_length=10_000)  # Max 10KB
    input_data: str = Field(default="", max_length=10_000)
```

---

## 📚 Documentation

- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Vercel Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/python)

---

## ✨ Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy on Vercel
3. 🎨 Add custom domain
4. 📊 Monitor logs and performance
5. 🚀 Share your app!

---

## 🎉 You're Ready to Deploy!

Everything is configured and ready for Vercel:

```
✅ Frontend code
✅ Serverless API (api/index.py)
✅ Dependencies configured
✅ Vercel config ready
✅ API client updated
✅ Environment template prepared
```

Visit **https://vercel.com** and deploy! 🚀

---

**Questions?** Check the [README](../README.md) or view the [API documentation](../backend/README.md).

*Last Updated: March 21, 2026*
