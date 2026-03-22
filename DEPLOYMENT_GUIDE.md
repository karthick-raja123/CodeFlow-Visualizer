# 🚀 Deployment & GitHub Setup Guide

## Project Summary
**CodeFlow Visualizer** - An AI-powered Python code execution and debugging tool with real-time visualization built with React + FastAPI.

---

## ✅ Completed Setup Tasks

### 1. Professional Documentation
- ✅ **Main README.md** - Comprehensive project overview with features, tech stack, installation, usage
- ✅ **backend/README.md** - Backend API documentation, setup guide, endpoint specifications
- ✅ **frontend/README.md** - Frontend setup, development server, build instructions, project structure

### 2. Configuration Files
- ✅ **.gitignore** - Enhanced with comprehensive exclusions for Node.js, Python, IDE, OS, and secrets
- ✅ **.env.example** - Template for environment configuration
- ✅ **LICENSE** - MIT License included

### 3. Project Structure
```
codeflow-visualizer/
├── backend/                  # FastAPI Server
│   ├── main.py              # Entry point & routes
│   ├── executor.py          # Code execution module
│   ├── tracer.py            # Step tracing module
│   ├── explainer.py         # AI explanation engine
│   ├── flow_analyzer.py     # Flow diagram generator
│   ├── database.py          # Database models
│   ├── requirements.txt      # Python dependencies
│   └── README.md            # Backend documentation
├── src/                     # React Frontend (Alt: frontend/)
│   ├── components/          # UI components
│   ├── context/            # Global state
│   ├── services/           # API communication
│   ├── App.jsx             # Main app
│   └── main.jsx            # Entry point
├── public/                 # Static assets
├── .env.example           # Environment template
├── .gitignore             # Git exclusions
├── package.json           # Node dependencies
├── vite.config.js         # Build configuration
├── LICENSE                # MIT License
└── README.md              # Project documentation
```

### 4. Git Commit History
```
f997308 chore: upgrade .gitignore, .env.example, and add MIT LICENSE
252f09b docs: enhance documentation with comprehensive sections and examples
69e1d6e feat: CodeFlow Visualizer - AI-powered Python debugging tool
```

---

## 🔧 Initial Setup Commands

### Clone & Setup
```bash
git clone https://github.com/karthick-raja123/Python-Visualizer.git
cd Python-Visualizer
```

### Backend Setup
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Windows PowerShell
# OR
.\.venv\Scripts\activate.bat    # Windows CMD
# OR
source .venv/bin/activate       # macOS/Linux

pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
npm install
npm run dev
```

---

## 📊 Deployment Options

### Frontend Deployment (Vercel)
```bash
npm run build
npm install -g vercel
vercel --prod
```
**Env Vars to Set:**
- `VITE_API_URL` → Backend API URL

### Backend Deployment (Render)
```bash
git push origin main
```
**In Render Dashboard:**
1. Create new Web Service
2. Connect GitHub repository
3. Set Build Command: `pip install -r backend/requirements.txt`
4. Set Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`
5. Set Environment Variables:
   - `ALLOWED_ORIGINS` → Frontend URL
   - `APP_ENV` → production

---

## 🔐 Environment Variables

Create `.env` in root directory:

```env
# Backend
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000

# Frontend
VITE_API_URL=http://localhost:8000
VITE_API_PREFIX=
VITE_API_TIMEOUT=10000
VITE_ENABLE_SESSIONS=false

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Environment
APP_ENV=development
```

---

## 📡 API Endpoints

### Development
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- Django Admin: `http://localhost:8000/docs`

### Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/execute` | Execute Python code |
| POST | `/trace` | Trace step-by-step |
| POST | `/explain` | Get AI explanation |
| GET | `/health` | Health check |

---

## 🔄 Git Workflow

### Making Changes
```bash
git checkout -b feature/your-feature
# Make changes
git add .
git commit -m "feat: describe your feature"
git push origin feature/your-feature
```

### Commit Convention
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `chore:` - Maintenance
- `test:` - Tests
- `refactor:` - Code refactoring

### Merging to Main
```bash
git checkout main
git pull origin main
git merge feature/your-feature
git push origin main
```

---

## 📋 Pre-deployment Checklist

- [ ] All tests passing
- [ ] No console errors
- [ ] Environment variables configured
- [ ] .gitignore properly set
- [ ] Dependencies locked (package-lock.json, requirements.txt)
- [ ] License included
- [ ] README documentation complete
- [ ] Code commits are meaningful
- [ ] No sensitive data in repo
- [ ] Backend API responding
- [ ] Frontend builds successfully

---

## 🚀 Production Deployment Steps

> **Optional frontend envs**
> - `VITE_API_PREFIX` — set to `/api` when deploying behind a proxy such as Vercel edge functions. Leave blank for direct FastAPI usage.
> - `VITE_API_TIMEOUT` — client timeout (ms) for all API requests. Defaults to `10000`.
> - `VITE_ENABLE_SESSIONS` — keep `false` until the `/sessions` endpoints are implemented server-side.

---

## 🛡️ Backend Fallback & Mock Mode

- The frontend now auto-detects the correct API origin. If `VITE_API_URL` is missing, localhost (`http://localhost:8000`) is used during dev and the page origin is used in production. When the app is served from `*.vercel.app`, it automatically adds the `/api` prefix so calls route to Vercel serverless functions.
- Every request enforces a shared timeout (`VITE_API_TIMEOUT`). When the FastAPI backend is offline or returns 404, the UI falls back to a deterministic mock execution so demos keep working. A banner is logged in the console: `[CodeFlow] Backend unreachable, using mock response`.
- To disable the mock fallback, simply keep the backend reachable (recommended for production). The moment a healthy response is returned, the mock path is bypassed automatically.
- Session APIs (`/sessions`) stay guarded behind `VITE_ENABLE_SESSIONS` so that the UI only attempts persistence when the backend exposes those endpoints.

---

### Step 1: Verify Locally
```bash
# Backend
python -m uvicorn backend.main:app --reload --port 8000

# Frontend (new terminal)
npm run dev
```
Validation checklist:
- Visit `http://localhost:5173` and run a snippet (e.g., `print("hello")`).
- Confirm the Network tab shows requests to `http://localhost:8000/execute` and `http://localhost:8000/trace` (no `/api` prefix for local dev).
- Hit `http://localhost:8000/health` to ensure the FastAPI service reports `{"status":"ok"}`.
- Confirm any backend errors surface in the in-app banner instead of generic `Connection failed` messages.

### Step 2: Create Production Build
```bash
npm run build
```
Output in `dist/` directory

### Step 3: Verify Production Build
```bash
npm run preview
```

### Step 4: Push to GitHub
```bash
git add .
git commit -m "chore: production ready"
git push origin main
```

### Step 5: Deploy Frontend (Vercel)
```bash
npm install -g vercel
vercel --prod
```

### Step 6: Deploy Backend (Render)
Connect GitHub repo and set configuration in Render dashboard

### Step 7: Configure Environment Variables
- Frontend: Set `VITE_API_URL` on Vercel
- Backend: Set `ALLOWED_ORIGINS` on Render

### Step 8: Test Production
- Visit production frontend URL
- Verify API connectivity (check `/health` or `/docs` on the backend host)
- Test code execution
- Check error logs

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Module Not Found
```bash
# Python
pip install -r backend/requirements.txt

# Node
npm install
```

### CORS Errors
Check `ALLOWED_ORIGINS` in `backend/.env`

### Backend Falling Back to Mock Responses
- Ensure `VITE_API_URL` matches the deployed FastAPI/Render URL exactly (include https scheme)
- For Vercel frontend + Render backend combos, set `VITE_API_PREFIX=/api` only when routing through the serverless wrapper. Leave it blank when calling Render directly.
- Watch the browser console for `[CodeFlow API] request ...` logs; these indicate which endpoint failed.

### Build Errors
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

---

## 📞 Support Resources

- GitHub Issues: https://github.com/karthick-raja123/Python-Visualizer/issues
- FastAPI Docs: https://fastapi.tiangolo.com/
- React Docs: https://react.dev/
- Vite Guide: https://vitejs.dev/guide/

---

## 📄 Files Status

| File | Status | Purpose |
|------|--------|---------|
| README.md | ✅ | Main project documentation |
| backend/README.md | ✅ | Backend setup & API docs |
| frontend/README.md | ✅ | Frontend setup guide |
| .gitignore | ✅ | Git file exclusions |
| .env.example | ✅ | Environment template |
| LICENSE | ✅ | MIT License |
| package.json | ✅ | Node.js dependencies |
| requirements.txt | ✅ | Python dependencies |

---

**GitHub Repository**: https://github.com/karthick-raja123/Python-Visualizer

**Last Updated**: March 21, 2026

---

*Project prepared for professional GitHub deployment by GitHub Copilot*
