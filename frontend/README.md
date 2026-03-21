# CodeFlow Visualizer - Frontend

Professional React-based frontend for CodeFlow Visualizer, built with Vite and Tailwind CSS.

## 🔧 Installation

### Prerequisites
- **Node.js 18+**
- **npm 9+** or **yarn 3+**

### Steps

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create `.env.local` file (optional):
   ```bash
   cp ../.env.example .env.local
   ```

3. Update API endpoint if needed in `src/services/api.js`:
   ```javascript
   const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';
   ```

---

## 🚀 Running Development Server

Start the development server with hot module replacement (HMR):

```bash
npm run dev
```

The application will be available at:
- **Local**: `http://localhost:5173/`
- **Network**: Use `--host` flag to expose on network

---

## 📦 Build for Production

Create an optimized production build:

```bash
npm run build
```

Output will be in the `dist/` directory.

---

## 👁️ Preview Build

Preview the production build locally:

```bash
npm run preview
```

---

## 📝 Linting

Check code quality with ESLint:

```bash
npm run lint
```

---

## 📂 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── CodeEditor.jsx      # Monaco code editor
│   ├── ExecutionControls.jsx # Run/pause/step buttons
│   ├── ExplanationPanel.jsx   # AI explanation display
│   ├── FlowDiagram.jsx        # React Flow visualization
│   ├── MemoryPanel.jsx        # Variable state display
│   ├── OutputConsole.jsx      # Execution output
│   └── ...
├── context/             # Global state management
│   ├── AppContext.jsx      # App state provider
│   └── ThemeContext.jsx     # Theme switching logic
├── services/            # API communication
│   └── api.js             # Client for backend
├── App.jsx              # Main app component
├── main.jsx             # Entry point
└── index.css            # Global styles
```

---

## 🎨 Features

- **Monaco Editor**: Professional code editor with syntax highlighting
- **Real-time Visualization**: Watch variables change during execution
- **Flow Diagrams**: Automatic flowchart generation
- **Dark/Light Theme**: Toggle with persistent storage
- **Responsive Design**: Works on desktop, tablet, mobile
- **Accessibility**: ARIA labels, keyboard navigation

---

## 🔗 API Integration

The frontend communicates with the FastAPI backend via `src/services/api.js`.

**Main Endpoints:**
- `POST /api/execute` - Run code
- `POST /api/trace` - Get step-by-step trace
- `POST /api/explain` - Get AI explanation

---

## 🛠️ Tech Stack

- **React 19**: UI framework
- **Vite**: Build tool & dev server
- **Tailwind CSS**: Utility-first CSS
- **Framer Motion**: Animations
- **Monaco Editor**: Code editing
- **React Flow**: Diagram visualization
- **Lucide Icons**: Icon system

---

## 📚 Dependencies

Check `package.json` for the complete list of dependencies and dev dependencies.

---

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

## 📄 License

MIT License - See LICENSE file for details.

---

**Made with ❤️ by [@karthick-raja123](https://github.com/karthick-raja123)**
