# CodeFlow Visualizer

**🚀 AI-powered Python code execution and visualization platform** — Execute code, trace execution step-by-step, visualize memory states, and get intelligent AI explanations. Built with React + FastAPI, optimized for learners and developers.

![Python](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Build](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## Overview

CodeFlow Visualizer is a cutting-edge educational and debugging tool that helps developers and students **understand Python code execution visually**. Write or paste Python code, execute it, and watch as each line executes — see variables change in real-time, trace the control flow through functions and loops, visualize memory allocation, and receive AI-powered explanations for every step.

### Who Should Use It?

- 🎓 **Students & Learners** — Master Python fundamentals with visual step-through execution
- 👨‍💻 **Developers** — Debug complex logic and understand code flow instantly
- 👨‍🏫 **Educators** — Teach Python concepts with interactive visualization
- 🔬 **Researchers** — Analyze algorithm behavior and execution patterns

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| ▶️ **Code Execution** | Execute Python code with complete stdout/stderr capture, stdin support for `input()` |
| 🔍 **Step-by-Step Tracing** | Line-by-line execution using Python's `sys.settrace()` with variable tracking |
| 🧠 **Memory Visualization** | Real-time variable display with types, NEW/UPDATE badges, stack frame hierarchy |
| 🔀 **Flow Diagram** | Interactive React Flow graphs showing execution path: Start → Process → Loops → End |
| 🤖 **AI Explanations** | Context-aware explanations, CS concepts, and coding suggestions for each execution step |
| 🌙 **Theme Switching** | Dark and Light mode with localStorage persistence |
| 📝 **Monaco Editor** | VS Code-quality editor with Python syntax highlighting and formatting |
| 🛡️ **Safety Features** | Infinite loop detection, timeout protection (8s trace limit), memory-safe execution |
| ⏱️ **Performance** | All operations guaranteed to complete within 10 seconds |
| 📱 **Responsive Design** | Works seamlessly on desktop, tablet, and mobile devices |

---

## 🛠️ Technology Stack

### Frontend
- **React 19** — Latest UI framework with hooks and concurrent rendering
- **Vite 8** — Lightning-fast build tool and dev server
- **Tailwind CSS 4** — Utility-first CSS framework
- **Monaco Editor** — VS Code's editor engine directly embedded
- **React Flow 12** — Interactive diagram and node-based graph library
- **Framer Motion** — Smooth animations and transitions
- **Lucide React** — Beautiful, consistent icon library

### Backend
- **FastAPI** — Modern, fast (as fast as Node & Go) Python web framework
- **Uvicorn** — Lightning-fast ASGI web server
- **Pydantic** — Data validation and type hints
- **Python sys.settrace** — Low-level code tracing mechanism
- **subprocess** — Safe Python code execution in isolated processes

### Deployment
- **Vercel** — Frontend deployment (zero-config, serverless)
- **Render** — Backend deployment (managed container platform)

---

## 📦 Installation & Setup

### Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.10 or higher** ([Download](https://www.python.org/downloads/))
- **Node.js 18 or higher** ([Download](https://nodejs.org/))
- **npm 9+ or yarn** (comes with Node.js)
- **Git** ([Download](https://git-scm.com/))

### Step 1: Clone the Repository

```bash
git clone https://github.com/karthick-raja123/CodeFlow-Visualizer.git
cd CodeFlow-Visualizer
```

### Step 2: Backend Setup

```bash
# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
pip install -r api/requirements.txt
```

### Step 3: Frontend Setup

```bash
# Install Node dependencies
npm install

# Install Tailwind CSS (included in dependencies)
```

### Step 4: Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Configure for local development (already set in .env.example)
# VITE_API_URL=http://localhost:8000
```

### Step 5: Start Development Servers

**Terminal 1 - Backend (FastAPI on port 8000):**
```bash
.venv\Scripts\activate  # or: source .venv/bin/activate
cd api
python -m uvicorn index:app --reload --port 8000
```

**Terminal 2 - Frontend (Vite dev server on port 5173):**
```bash
npm run dev
```

The application will be available at: **http://localhost:5173**

---

## 🚀 Usage

### Basic Workflow

1. **Write Code** — Use the Monaco editor to write Python code
2. **Execute** — Click "Execute" to run code immediately
3. **Trace Step** — Click "Trace" to step through line-by-line execution
4. **Observe** — Watch variables change in the memory panel
5. **Understand** — Click "Explain" to get AI insights for each step

### Example Code

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(5)
print(f"Fibonacci(5) = {result}")
```

---

## 📡 API Documentation

### Backend Endpoints

All endpoints return JSON responses. The backend runs on `http://localhost:8000` by default.

#### 1. Health Check
```
GET /health
```
**Response:**
```json
{"status": "ok"}
```

#### 2. Execute Code
```
POST /execute
```
**Request:**
```json
{
  "code": "print('Hello, World!')",
  "input_data": ""
}
```
**Response:**
```json
{
  "output": "Hello, World!\n",
  "error": "",
  "status": "success"
}
```

#### 3. Trace Execution
```
POST /trace
```
**Request:**
```json
{
  "code": "x = 10\ny = x + 5\nprint(y)",
  "input_data": ""
}
```
**Response:**
```json
{
  "steps": [
    {"line": 1, "vars": {}},
    {"line": 2, "vars": {"x": 10}},
    {"line": 3, "vars": {"x": 10, "y": 15}},
    {"line": 4, "vars": {"x": 10, "y": 15}}
  ],
  "stdout": "15\n",
  "stderr": ""
}
```

#### 4. Explain Code Step
```
POST /explain
```
**Request:**
```json
{
  "code": "result = factorial(5)",
  "step_data": {"line": 1, "vars": {"result": 120}},
  "prev_step": null
}
```
**Response:**
```json
{
  "explanation": "Line 1: Variables: result",
  "detail": "Executing line 1 of the code",
  "suggestion": "Step through the code to see how variables change",
  "concept": "Code Execution"
}
```

### OpenAPI Documentation

Interactive API documentation is available at:
- **http://localhost:8000/docs** (Swagger UI)
- **http://localhost:8000/redoc** (ReDoc)

---

## 🧪 Testing

Run the test suite:

```bash
# Frontend tests
npm run lint

# Backend tests (if available)
pytest api/
```

---

## 🌐 Deployment

### Deploy Frontend to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Configuration:** `vercel.json` is pre-configured:
- Builds with `npm run build`
- Routes API requests to `/api` (serverless function)
- Serves SPA with fallback to `index.html`

### Deploy Backend to Render

1. **Create Render Account** — Visit [render.com](https://render.com)
2. **Connect GitHub** — Authorize Render to access this repository
3. **Create Web Service**:
   - Environment: Python
   - Start Command: `uvicorn api.index:app --host 0.0.0.0 --port 10000`
   - Set environment variable: `ALLOWED_ORIGINS=<your-vercel-frontend-url>`
4. **Update .env.production**:
   ```
   VITE_API_URL=https://your-render-backend-url.onrender.com
   ```
5. **Redeploy Frontend**:
   ```bash
   vercel --prod
   ```

**Configuration:** `render.yaml` is pre-configured with both frontend and backend deployment specs.

---

## 📁 Project Structure

```
CodeFlow-Visualizer/
├── api/                          # FastAPI backend (production)
│   ├── index.py                  # Main app with all endpoints
│   ├── requirements.txt           # Python dependencies
│   └── __pycache__/              # Compiled Python files
│
├── backend/                      # Legacy backend (reference only)
│   ├── main.py                   # Old implementation
│   ├── executor.py               # Code execution module
│   ├── tracer.py                 # Code tracing module
│   └── requirements.txt           # Legacy dependencies
│
├── src/                          # React frontend
│   ├── components/               # React components
│   │   ├── CodeEditor.jsx        # Monaco editor wrapper
│   │   ├── ExecutionControls.jsx # Execute/Trace/Explain buttons
│   │   ├── ExplanationPanel.jsx  # AI explanation display
│   │   ├── FlowDiagram.jsx       # React Flow visualization
│   │   ├── MemoryPanel.jsx       # Variable visualization
│   │   ├── OutputConsole.jsx     # Execution output display
│   │   └── ...more components
│   ├── context/
│   │   ├── AppContext.jsx        # Global app state
│   │   └── ThemeContext.jsx      # Dark/Light theme
│   ├── services/
│   │   └── api.js                # API client library
│   ├── App.jsx                   # Root component
│   ├── main.jsx                  # Entry point
│   ├── index.css                 # Global styles
│   └── assets/                   # images, icons, etc.
│
├── public/                       # Static assets
│
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── package.json                  # Node dependencies
├── vite.config.js                # Vite build configuration
├── vercel.json                   # Vercel deployment config
├── render.yaml                   # Render IaC configuration
├── LICENSE                       # MIT License
├── README.md                     # This file
└── DEPLOYMENT_GUIDE.md           # Detailed deployment docs
```

---

## 🔐 Security Considerations

- ✅ **Code Execution Safety** — Uses subprocess isolation, never `eval()` or `exec()`
- ✅ **Timeout Protection** — Hard kill after 8 seconds to prevent infinite loops
- ✅ **CORS Configuration** — Properly configured for cross-origin requests
- ✅ **Input Validation** — Pydantic models validate all API inputs
- ✅ **Memory Limits** — Traces limited to 200 steps to prevent memory exhaustion
- ✅ **No Arbitrary System Access** — Cannot execute system commands or access files

---

## 🚨 Troubleshooting

### Backend Connection Failed
```
Error: Backend unreachable - showing local explanation
```
**Solution:**
- Ensure backend is running: `python -m uvicorn api.index:app --port 8000`
- Check VITE_API_URL in `.env` matches backend port
- Refresh browser (Ctrl+R)

### Trace Not Working
```
Error: Network Error
```
**Solution:**
- Check Python version (need 3.10+)
- Verify CORS enabled in api/index.py
- Check browser DevTools Network tab for failed requests

### Port Already in Use
```
Error: Address already in use
```
**Solution:**
```bash
# Windows: Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# macOS/Linux: 
lsof -ti:8000 | xargs kill -9
```

### Frontend Not Updating
```
Changes to code not showing
```
**Solution:**
- Restart Vite dev server: `npm run dev`
- Clear browser cache: Ctrl+Shift+Del
- Check that .env file is correct

---

## 📊 Performance Metrics

| Operation | Time Limit | Status |
|-----------|-----------|--------|
| Code Execution | 5 seconds | ⏱️ Safe |
| Code Tracing | 8 seconds | ⏰ Allow for complex code |
| API Request Timeout | 10 seconds | ✅ Generous |
| Trace Step Limit | 200 steps | 🎯 Prevents memory issues |

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository** — Click the fork button on GitHub
2. **Create a feature branch** — `git checkout -b feature/amazing-feature`
3. **Make your changes** — Follow the project's code style
4. **Commit with clarity** — `git commit -m 'Add amazing feature'`
5. **Push to your fork** — `git push origin feature/amazing-feature`
6. **Open a Pull Request** — Describe your changes and why they matter

### Development Guidelines
- Write clean, readable code with comments for complex logic
- Test your changes thoroughly before committing
- Update documentation if you change behavior
- Follow the existing code style and patterns

---

## 📝 Code Examples

### Array Visualization
```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()
print(numbers)
```

### Function Tracing
```python
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

print(power(2, 3))  # 8
```

### Recursion Visualization
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(f"5! = {result}")
```

---

## 📸 Screenshots

> Screenshots will be added here in the future. See [Issues](https://github.com/karthick-raja123/CodeFlow-Visualizer/issues) for feature requests.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details. Freely use, modify, and distribute this project for personal and commercial purposes.

---

## 👤 Author

**Karthick Raja** — Full Stack Developer & EdTech Enthusiast
- GitHub: [@karthick-raja123](https://github.com/karthick-raja123)
- Project: CodeFlow Visualizer — Learning Python, Visualized

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) — Modern Python web framework
- [React](https://react.dev/) — JavaScript UI library
- [Vite](https://vitejs.dev/) — Next generation build tool
- [Tailwind CSS](https://tailwindcss.com/) — Utility-first CSS
- [Monaco Editor](https://microsoft.github.io/monaco-editor/) — VS Code editor
- [React Flow](https://reactflow.dev/) — Node-based UI library

---

## 📞 Support

Have questions or found a bug?
- **Check [Issues](https://github.com/karthick-raja123/CodeFlow-Visualizer/issues)** — Search for similar problems
- **Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** — Detailed setup instructions
- **Open a new issue** — Describe what's happening with steps to reproduce

---

**Made with ❤️ for Python learners and developers everywhere.**

⭐ If you found this project helpful, please give it a star on GitHub!
