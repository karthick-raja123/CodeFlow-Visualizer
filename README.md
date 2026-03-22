# 🚀 CodeFlow Visualizer

**CodeFlow Visualizer** is a professional, AI-powered tool designed to execute, trace, and visualize Python code in real-time. It provides developers and students with a deep understanding of code execution by generating interactive flowcharts and tracking variable state changes step-by-step.

![CodeFlow Demo](https://via.placeholder.com/800x450?text=CodeFlow+Visualizer+Demo)

## ✨ Features

- **⚡ Real-time Execution**: Run Python code instantly in a secured environment.
- **🔍 Step-by-Step Tracing**: Visualize exactly how your code executes line-by-line.
- **🧠 AI-Powered Explanations**: Get deep insights into your logic with AI-generated explanations for every step.
- **📊 Interactive Flowcharts**: Automatically generate AST-based flowcharts to visualize control flow (If/Else, Loops, Functions).
- **💾 Memory Tracking**: Monitor variable state changes and stack frames in a dedicated visualization panel.
- **🛡️ Safety First**: Built-in protections against infinite loops and resource exhaustion.

## 🛠️ Tech Stack

- **Frontend**: React 19, Vite, Tailwind CSS, Framer Motion, Lucide React.
- **Backend**: FastAPI (Python 3.10+), Uvicorn.
- **Editor**: Monaco Editor (@monaco-editor/react).
- **Flowchart**: React Flow (@xyflow/react).
- **Deployment**: Vercel (Frontend + Serverless API), Render (Backend Service).

## 🚀 Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.10+)
- npm or yarn

### Local Development Links

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/karthick-raja123/CodeFlow-Visualizer.git
   cd CodeFlow-Visualizer
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Backend Setup**:
   ```bash
   cd ../backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python main.py
   ```

## 📡 API Usage

The backend provides several endpoints for code analysis:

### `POST /execute`
Executes the provided code and returns the output.

**Request Body**:
```json
{
  "code": "print('Hello World')",
  "input_data": ""
}
```

### `POST /trace`
Traces the execution and returns step-by-step state snapshots.

### `POST /explain`
Provides AI-driven explanations for a specific execution step.

## 🌐 Deployment

### Vercel (Frontend & Serverless)
The project is optimized for Vercel. Simply connect your GitHub repository and it will automatically deploy using the `vercel.json` configuration.

### Render (Backend)
The backend can be deployed as a Web Service on Render using the provided `render.yaml`.

## 👤 Author

**Karthick Raja**
- GitHub: [@karthick-raja123](https://github.com/karthick-raja123)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Made with ❤️ for the Developer Community.
