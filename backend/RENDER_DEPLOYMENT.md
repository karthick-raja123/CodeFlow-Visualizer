# 🚀 FastAPI Backend - Render Deployment Guide

**Deploy your CodeFlow Visualizer backend to Render in minutes.**

---

## ✅ Pre-Deployment Checklist

- [x] **requirements.txt** - Contains `fastapi==0.115.0` and `uvicorn[standard]==0.30.0`
- [x] **main.py** - Contains `if __name__ == "__main__"` guard with uvicorn startup
- [x] **CORS Configuration** - Enabled for cross-origin requests
- [x] **render.yaml** - Configured with proper build and start commands
- [x] **Environment Variables** - Template provided

---

## 📋 Quick Start - 5 Steps

### Step 1️⃣: Push Code to GitHub
```bash
git add .
git commit -m "chore: prepare backend for Render deployment"
git push origin main
```

### Step 2️⃣: Sign Up on Render
Visit **https://render.com** and sign up (free tier available)

### Step 3️⃣: Connect GitHub Repository
1. Go to **Dashboard** → **New** → **Web Service**
2. Select **Deploy an existing repository**
3. Search for `Python-Visualizer` and click **Connect**

### Step 4️⃣: Configure Deployment Settings
```
Service Name:        codeflow-api
Environment:         Python 3
Build Command:       pip install -r backend/requirements.txt
Start Command:       uvicorn backend.main:app --host 0.0.0.0 --port 10000
Free Plan:          Select (or Paid if preferred)
```

### Step 5️⃣: Set Environment Variables
In the **Environment Variables** section, add:
```
ALLOWED_ORIGINS = https://your-frontend-url.vercel.app
APP_ENV = production
PYTHONUNBUFFERED = 1
```

Click **Create Web Service** → Done! 🎉

---

## 🔐 Configuration Details

### render.yaml (Already Configured)
```yaml
services:
  - type: web
    name: codeflow-api
    runtime: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port 10000
    envVars:
      - key: PYTHONUNBUFFERED
        value: "1"
      - key: ALLOWED_ORIGINS
        value: "https://your-frontend.vercel.app"
```

### Environment Variables to Set
| Variable | Value | Purpose |
|----------|-------|---------|
| `ALLOWED_ORIGINS` | `https://your-frontend-url.vercel.app` | CORS configuration |
| `APP_ENV` | `production` | Environment mode |
| `PYTHONUNBUFFERED` | `1` | Real-time logging |

---

## 🛠️ Backend Configuration Files

### requirements.txt
✅ **Already configured with:**
```
fastapi==0.115.0
uvicorn[standard]==0.30.0
pydantic==2.9.0
```

### main.py - Main Guard
✅ **Already added:**
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=10000,
        reload=False,
        log_level="info"
    )
```

### CORS Configuration
✅ **Already enabled:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Set via env var
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔗 Deployment URL

After deployment, your API will be available at:
```
https://codeflow-api.onrender.com
```

Update your frontend's `.env` with:
```env
VITE_API_URL=https://codeflow-api.onrender.com
```

---

## ✨ Start Command Explained

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 10000
```

- **`backend.main:app`** - Module path to FastAPI app
- **`--host 0.0.0.0`** - Listen on all network interfaces (required for Render)
- **`--port 10000`** - Port number (Render requires dynamic port assignment)
- **`--reload=False`** - Disable auto-reload in production
- **`--log_level info`** - Logging level for debugging

---

## 🧪 Test Deployment

### Health Check Endpoint
```bash
curl https://codeflow-api.onrender.com/health
```

Expected response:
```json
{"status": "ok"}
```

### Execute Endpoint
```bash
curl -X POST https://codeflow-api.onrender.com/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello from Render!\")",
    "input_data": ""
  }'
```

---

## 📊 Render Deployment Dashboard

After deployment, monitor your service:
1. Go to **Dashboard** → Select **codeflow-api**
2. **Logs** - View real-time server logs
3. **Metrics** - CPU, memory, request metrics
4. **Settings** - Update environment variables anytime

---

## 🔄 Auto-Deploy on Push

Render automatically redeploys when you push to the default branch:
```bash
# Make changes
git add .
git commit -m "fix: update backend"
git push origin main

# Render will automatically rebuild and redeploy
```

---

## 🐛 Troubleshooting

### Build Failed: "No module named 'backend'"
**Solution**: Ensure `buildCommand` is:
```
pip install -r backend/requirements.txt
```

### CORS Error on Frontend
**Solution**: Update `ALLOWED_ORIGINS`:
```env
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
```

### API Timeout (>30s)
**Solution**: Check logs in Render Dashboard → Logs
- Reduce code execution limits
- Optimize tracer performance
- Check network connectivity

### Port Issues
**Solution**: Render manages ports automatically. Always use `--port 10000` in `startCommand`.

---

## 🚨 Important Notes

1. **Free Tier**: Services spin down after 15 minutes of inactivity. Upgrade for production.
2. **Database**: Current setup has no persistence. Add PostgreSQL if needed.
3. **Secrets**: Store sensitive data in environment variables, not in code.
4. **Logs**: Accessible via Render Dashboard for debugging.

---

## 📈 Next Steps

1. ✅ Deploy backend to Render
2. 🎨 Deploy frontend to Vercel
3. 🔗 Update `VITE_API_URL` in frontend
4. 🧪 Test all API endpoints
5. 🚀 Monitor logs and metrics

---

## 📚 References

- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Uvicorn Docs**: https://www.uvicorn.org/
- **CORS Middleware**: https://fastapi.tiangolo.com/tutorial/cors/

---

## 💬 Support

- **Render Support**: https://render.com/docs/support
- **FastAPI Community**: https://fastapi.tiangolo.com/community/
- **GitHub Issues**: https://github.com/karthick-raja123/Python-Visualizer/issues

---

**Backend Status**: ✅ **READY FOR RENDER DEPLOYMENT**

Deploy with confidence! 🚀
