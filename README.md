# ⚡ CodeFlow Visualizer

**AI-powered Python code execution and debugging tool** — Execute code, trace step-by-step, visualize memory & flow, and get AI explanations. Built with React + FastAPI.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 What It Does

CodeFlow Visualizer helps developers and learners **understand Python code execution visually**. Write code, run it, and watch as each line executes — see variables change, trace the flow, and get AI-powered explanations.

**Perfect for:**
- 🎓 Students learning Python
- 🐛 Developers debugging logic
- 👩‍🏫 Teachers explaining code concepts

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ▶️ **Code Execution** | Run Python code with full stdout/stderr capture |
| ⌨️ **Input Support** | Handle `input()` functions with stdin textarea |
| 🔍 **Step-by-Step Tracing** | Line-by-line execution with `sys.settrace` |
| 🧠 **Memory Visualization** | Variable boxes with types, NEW/UPD badges, stack frame |
| 🔀 **Flow Diagram** | React Flow graph: Start → Process → Loop → End |
| 🤖 **AI Explanations** | Contextual explanation, CS concepts, coding tips per step |
| 🌙 **Dark / Light Theme** | Toggle with localStorage persistence |
| 📝 **Monaco Editor** | VS Code-quality editor with syntax highlighting |
| 🛡️ **Infinite Loop Protection** | Detects `while True` without `break` |
| ⏱️ **Timeout Safety** | 10s execution limit, 8s trace limit, never hangs |

---

## 🛠️ Tech Stack

**Frontend:**
- React 19 + Vite
- Tailwind CSS + Framer Motion
- Monaco Editor (VS Code engine)
- React Flow (diagram visualization)

**Backend:**
- FastAPI (Python)
- subprocess.Popen (safe execution)
- sys.settrace (step tracer)
- Pattern-based AI explainer

---

## 📦 Installation

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **npm**

### 1. Clone the repository

```bash
git clone https://github.com/karthick-raja123/Python-Visualizer.git
cd Python-Visualizer
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Frontend Setup

```bash
npm install
```

### 4. Environment Variables

```bash
# Copy the example env file
cp .env.example .env
```

---

## 🚀 Running Locally

Open **two terminals**:

**Terminal 1 — Backend:**
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 📖 Usage

1. **Write code** in the Monaco editor (left panel)
2. **Click ▶ Run** to execute — see output in the center panel
3. **Click 🔍 Trace** to debug step-by-step
4. Use **◀ ▶** buttons in the header to step through lines
5. Watch the **Memory panel** (right) show variables changing
6. Switch to **🔀 Flow** tab to see the execution graph
7. Switch to **🤖 AI Explain** tab for line-by-line explanations
8. Need `input()`? Click **▸ stdin** and type values (one per line)
9. Toggle **🌙/☀️** for dark/light theme

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/execute` | Run code and return output |
| `POST` | `/trace` | Trace code step-by-step |
| `POST` | `/explain` | Get AI explanation for a step |
| `GET` | `/health` | Health check |

**Request body:**
```json
{
  "code": "print('Hello')",
  "input_data": ""
}
```

---

## 🌐 Deployment

### Frontend → Vercel
```bash
npm run build
vercel --prod
```
Set `VITE_API_URL` in Vercel dashboard.

### Backend → Render
Use the included `render.yaml` or deploy manually:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 10000
```
Set `ALLOWED_ORIGINS` to your frontend URL.

---

## 📁 Project Structure

```
Python-Visualizer/
├── backend/
│   ├── main.py           # FastAPI server + tracer
│   ├── executor.py       # Popen-based code runner
│   ├── explainer.py      # AI explanation engine
│   ├── tracer.py         # Step tracing module
│   └── requirements.txt  # Python dependencies
├── src/
│   ├── App.jsx           # Main React component
│   ├── index.css         # Tailwind + theme styles
│   ├── main.jsx          # React entry point
│   ├── context/
│   │   └── ThemeContext.jsx
│   └── components/
│       ├── MemoryPanel.jsx
│       ├── FlowDiagram.jsx
│       └── ExplanationPanel.jsx
├── .env.example
├── .gitignore
├── vercel.json
├── render.yaml
├── package.json
├── vite.config.js
├── LICENSE
└── README.md
```

---

## 🔮 Future Improvements

- [ ] Breakpoint support (click gutter to toggle)
- [ ] Multi-file execution
- [ ] Real AI API integration (GPT/Gemini)
- [ ] Collaborative live coding
- [ ] Python package support (pip install in sandbox)
- [ ] Export execution report as PDF

---

## 👨‍💻 Author

**Karthick Raja**

- GitHub: [@karthick-raja123](https://github.com/karthick-raja123)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
