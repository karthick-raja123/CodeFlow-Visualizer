# Render Deployment Instructions

## Prerequisites

- GitHub repository with code committed
- Render account (https://render.com)
- Your Render API key (from account settings)

---

## Part 1: Deploy Backend to Render

### Step 1.1: Prepare Backend for Render

Your `backend/requirements.txt` should exist with all dependencies:

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
+ all other backend dependencies
```

### Step 1.2: Create Web Service on Render

1. **Go to Render Dashboard**
   - https://dashboard.render.com

2. **Click "New +"**
   - Select "Web Service"

3. **Connect Repository**
   - Choose your GitHub repo
   - Click "Connect"

4. **Configure Service**

   Fill in these settings:

   | Setting | Value |
   |---------|-------|
   | **Name** | `codeflow-visualizer-backend` |
   | **Environment** | `Python 3` |
   | **Build Command** | `pip install -r backend/requirements.txt` |
   | **Start Command** | `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000` |
   | **Instance Type** | `Free` (for testing) |

   **Important:** If `requirements.txt` is in root, use:
   ```
   Build: pip install -r requirements.txt
   Start: uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

5. **Click "Create Web Service"**

6. **Wait for Deployment**
   - Takes 2-5 minutes
   - You'll see logs in real-time
   - When done, note the URL: `https://your-service.onrender.com`

### Step 1.3: Verify Backend is Running

```bash
# Test health endpoint (wait 60 seconds after first deployment)
curl https://your-service.onrender.com/health

# Expected response:
# {"status":"ok"}

# Test execute endpoint
curl -X POST https://your-service.onrender.com/execute \
  -H "Content-Type: application/json" \
  -d '{"code":"print(42)","input_data":""}'
```

**Note:** First request after deployment may take 30-60 seconds (cold start).

---

## Part 2: Deploy Frontend to Render

### Step 2.1: Update Frontend Configuration

**Edit `frontend/.env.production`:**

```
VITE_API_URL=https://your-service.onrender.com
```

Replace `your-service` with your actual backend URL.

### Step 2.2: Create Frontend Web Service

1. **Go to Render Dashboard**
   - https://dashboard.render.com

2. **Click "New +"**
   - Select "Web Service"

3. **Connect Repository**
   - Same GitHub repo
   - Click "Connect"

4. **Configure Service**

   | Setting | Value |
   |---------|-------|
   | **Name** | `codeflow-visualizer-frontend` |
   | **Environment** | `Node` |
   | **Root Directory** | `frontend` |
   | **Build Command** | `npm install && npm run build` |
   | **Start Command** | `npm run preview` |
   | **Instance Type** | `Free` |

5. **Add Environment Variables**

   Click "Advanced" → "Environment"

   Add variable:
   ```
   VITE_API_URL=https://your-service.onrender.com
   ```

6. **Click "Create Web Service"**

7. **Wait for Deployment**
   - Takes 3-10 minutes
   - Note the URL when complete

### Step 2.3: Verify Frontend Works

1. Open frontend URL in browser
2. Enter test code:
   ```python
   print("Hello from Frontend!")
   ```
3. Click **▶ Run**
4. Expected output:
   ```
   Hello from Frontend!
   ```

If you see output, **deployment is successful!** 🎉

---

## Alternative: Deploy Both Services from Scratch

### Use Render's One-Click Deploy

If you have a `render.yaml` in your repo root:

```bash
# Push render.yaml to GitHub
git add render.yaml
git commit -m "Add Render deployment config"
git push

# Then visit Render dashboard and select "blueprints"
```

Example `render.yaml`:

```yaml
services:
  - type: web
    name: codeflow-backend
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
    envVars:
      - key: PYTHONUNBUFFERED
        value: true

  - type: static
    name: codeflow-frontend
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/dist
    envVars:
      - key: VITE_API_URL
        value: https://codeflow-backend.onrender.com
```

---

## Troubleshooting Deployment

### Issue: Build Fails

**Check logs:**
1. Render Dashboard → Your Service → Logs
2. Look for errors like:
   - `ModuleNotFoundError` → Missing dependency in requirements.txt
   - `SyntaxError` → Python code has syntax error
   - `npm ERR!` → Node/npm issue

**Solution:**
- Fix error locally
- Commit and push to GitHub
- Render will auto-redeploy

### Issue: Service Won't Start

**Check logs for:**
- `ImportError` → Missing package
- `Address already in use` → Port issue
- `No such file` → Wrong path

**Solution:**
- Verify Start Command is correct
- Check file paths (especially `cd backend/`)
- Redeploy

### Issue: Frontend Can't Reach Backend

**Check:**
1. Health endpoint: `curl https://backend-service.onrender.com/health`
2. Frontend environment: `VITE_API_URL` in Render dashboard
3. Browser console (F12) for CORS errors

**Solution:**
- Ensure backend is running (check logs)
- Update VITE_API_URL to match backend URL
- Rebuild frontend

### Issue: "502 Bad Gateway"

**Cause:** Backend service crashed or won't start

**Solution:**
1. Check backend logs for errors
2. Wait 60 seconds for cold start
3. Check Start Command in Render dashboard
4. Verify requirements.txt exists and all dependencies are listed

---

## Monitoring & Maintenance

### View Live Logs

```bash
# In Render dashboard
Service → Logs (real-time stream)
```

### Redeploy After Changes

1. **Push changes to GitHub**
   ```bash
   git add .
   git commit -m "Update code"
   git push
   ```

2. **Render auto-redeploys** (in ~2 minutes)
   - You can manually trigger: "Redeploy" button in dashboard

### Check Service Metrics

Dashboard shows:
- Build time
- Deployment time
- CPU usage
- Memory usage
- Request count

### Stop or Delete Service

> **Caution:** Deleting removes the service completely

1. Service settings → "Delete Service"
2. Frontend will still load but show "Connection failed"

---

## Cost Considerations

### Free Plan (Render)

- Web services: 750 free hours/month
- Shared CPU (0.5)
- 512 MB RAM
- Auto-pause after 15 minutes inactivity
- Cold starts: 30-60 seconds

### Upgrading

If you need always-on:
- Pay $7/month (paid tier)
- No auto-pause
- Faster cold starts

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Verify backend is running (`GET /health`)
3. ✅ Update frontend `.env.production` with backend URL
4. ✅ Deploy frontend to Render
5. ✅ Test end-to-end in browser
6. ✅ Monitor logs for issues

---

## Quick Reference

| Service | URL | Type |
|---------|-----|------|
| Backend | https://codeflow-backend.onrender.com | Web Service |
| Frontend | https://codeflow-frontend.onrender.com | Web Service |
| Health | `GET /health` | Backend endpoint |
| Execute | `POST /execute` | Backend endpoint |
| Trace | `POST /trace` | Backend endpoint |

---

## Support

- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Vite Docs**: https://vitejs.dev
- **GitHub Issues**: Open an issue in your repo

---

Last updated: March 25, 2026
