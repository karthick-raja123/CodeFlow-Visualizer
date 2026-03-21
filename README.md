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
│   ├── flow_analyzer.py  # Flow diagram generation
│   ├── database.py       # Database models (future)
│   ├── requirements.txt  # Python dependencies
│   └── README.md         # Backend documentation
├── src/
│   ├── App.jsx           # Main React component
│   ├── index.css         # Tailwind + theme styles
│   ├── main.jsx          # React entry point
│   ├── context/          # Global state
│   ├── components/       # Reusable UI components
│   └── services/         # API communication
├── public/               # Static assets
├── .env.example          # Environment template
├── .gitignore            # Git exclusions
├── vercel.json           # Vercel config
├── render.yaml           # Render deployment config
├── package.json          # Node dependencies
├── vite.config.js        # Vite configuration
├── eslint.config.js      # ESLint rules
├── LICENSE               # MIT License
└── README.md             # This file
```

---

## 🎓 Examples

### Basic Execution
```python
x = 5
y = 10
print(x + y)
```

### With Traces
```python
numbers = [1, 2, 3]
for i in numbers:
    print(i * 2)
```

### With Input
```python
name = input("Enter name: ")
print(f"Hello, {name}!")
```

---

## 📸 Screenshots

*(Placeholders — Add actual screenshots here)*
- **Code Editor & Output** - Main interface with Monaco editor
- **Memory Visualization** - Variables panel showing state changes
- **Flow Diagram** - Execution flow visualization
- **AI Explanations** - Step-by-step code explanations

---

## 🚀 Future Improvements

- [ ] **Debugger Breakpoints** - Set breakpoints and pause execution
- [ ] **Recursion Visualization** - Visual call stack for recursive functions
- [ ] **Variable History** - Timeline of variable changes
- [ ] **Code Snippets Library** - Pre-built example programs
- [ ] **Collaborative Mode** - Real-time code sharing
- [ ] **Multi-language Support** - JavaScript, Java, C++ execution
- [ ] **Performance Analytics** - Execution time profiling
- [ ] **Mobile App** - Native mobile version
- [ ] **GPU Acceleration** - Large dataset visualization
- [ ] **Export Features** - Save traces as PDF/JSON

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Port already in use" | Change port: `--port 8001` |
| "Module not found" | Run `pip install -r backend/requirements.txt` |
| "API not responding" | Check backend is running on `http://localhost:8000` |
| "CORS error" | Verify `ALLOWED_ORIGINS` in backend `.env` |
| "Infinite loop timeout" | Code exceeded 10-second limit; optimize logic |

---

## 🤝 Contributing

Contributions are welcome! Please:
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request
6. Follow the **commit message convention** below

### Commit Message Convention
```
feat:  New feature (e.g., feat: add dark mode)
fix:   Bug fix (e.g., fix: resolve timeout issue)
docs:  Documentation (e.g., docs: update README)
chore: Maintenance (e.g., chore: update dependencies)
test:  Tests (e.g., test: add unit tests)
```

---

## 📞 Support & Issues

- 🐛 **Bug Reports**: [Open an Issue](https://github.com/karthick-raja123/Python-Visualizer/issues)
- 💡 **Feature Requests**: [Discuss Ideas](https://github.com/karthick-raja123/Python-Visualizer/discussions)
- 📧 **Contact**: Reach out to [@karthick-raja123](https://github.com/karthick-raja123)

---

## 📚 Resources

- [Python Docs](https://docs.python.org/3/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

```
MIT License | Copyright (c) 2026 Karthick Raja
Permission granted for personal, commercial, and private use.
```

---

## 🙏 Acknowledgments

- **Inspired by**: [Thonny](https://thonny.org/), [Python Tutor](https://pythontutor.com/), VSCode
- **Built with**: React, FastAPI, Tailwind CSS
- **Icons**: [Lucide Icons](https://lucide.dev/)

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/karthick-raja123/Python-Visualizer?style=social)
![GitHub forks](https://img.shields.io/github/forks/karthick-raja123/Python-Visualizer?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/karthick-raja123/Python-Visualizer?style=social)

---

**Made with ❤️ by [@karthick-raja123](https://github.com/karthick-raja123)**

⭐ **Found this helpful? Please star this repository!**


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
