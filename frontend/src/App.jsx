import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Editor from '@monaco-editor/react';
import { useTheme } from './context/ThemeContext';
import MemoryPanel from './components/MemoryPanel';
import FlowDiagram from './components/FlowDiagram';
import ExplanationPanel from './components/ExplanationPanel';
import { runCode, traceCode, getExplanation } from './services/api';
import './index.css';

const SAMPLE = `x = 10
y = 20
total = x + y
print(f"Sum = {total}")

for i in range(3):
    total += i
    print(f"  + {i} = {total}")

print(f"Final = {total}")
`;

export default function App() {
  const { isDark, toggle } = useTheme();
  const [code, setCode] = useState(SAMPLE);
  const [userInput, setUserInput] = useState('');
  const [showInput, setShowInput] = useState(false);
  const [output, setOutput] = useState('');
  const [running, setRunning] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('output');

  // Trace
  const [steps, setSteps] = useState([]);
  const [currentStep, setCurrentStep] = useState(-1);

  const editorRef = useRef(null);
  const monacoRef = useRef(null);
  const decorationsRef = useRef([]);

  const cur = currentStep >= 0 && currentStep < steps.length ? steps[currentStep] : null;
  const prev = currentStep > 0 ? steps[currentStep - 1] : null;
  const codeLines = code.split('\n');

  // ── Monaco ────────────────────────────────────────
  const handleEditorMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    applyTheme(monaco, isDark);
  };

  function applyTheme(monaco, dark) {
    monaco.editor.defineTheme('codeflow-dark', {
      base: 'vs-dark', inherit: true, rules: [],
      colors: {
        'editor.background': '#0f172a',
        'editor.lineHighlightBackground': '#1e293b00',
        'editorLineNumber.foreground': '#475569',
        'editorLineNumber.activeForeground': '#818cf8',
        'editor.selectionBackground': '#6366f140',
        'editorCursor.foreground': '#818cf8',
      },
    });
    monaco.editor.defineTheme('codeflow-light', {
      base: 'vs', inherit: true, rules: [],
      colors: {
        'editor.background': '#f8fafc',
        'editor.lineHighlightBackground': '#f1f5f900',
        'editorLineNumber.foreground': '#94a3b8',
        'editorLineNumber.activeForeground': '#6366f1',
        'editor.selectionBackground': '#6366f130',
        'editorCursor.foreground': '#6366f1',
      },
    });
    monaco.editor.setTheme(dark ? 'codeflow-dark' : 'codeflow-light');
  }

  useEffect(() => {
    if (monacoRef.current) applyTheme(monacoRef.current, isDark);
  }, [isDark]);

  // ── Line decoration ───────────────────────────────
  useEffect(() => {
    const editor = editorRef.current;
    const monaco = monacoRef.current;
    if (!editor || !monaco) return;
    if (cur && cur.line > 0) {
      decorationsRef.current = editor.deltaDecorations(decorationsRef.current, [{
        range: new monaco.Range(cur.line, 1, cur.line, 1),
        options: { isWholeLine: true, className: 'active-line-decoration', glyphMarginClassName: 'active-line-glyph' },
      }]);
      editor.revealLineInCenter(cur.line);
    } else {
      decorationsRef.current = editor.deltaDecorations(decorationsRef.current, []);
    }
  }, [cur]);

  // ── Run ───────────────────────────────────────────
  const run = async () => {
    setRunning(true); setOutput(''); setError(null); setSteps([]); setCurrentStep(-1);
    try {
      const result = await runCode(code, userInput);
      setOutput(result.output || '(no output)');
      if (result.error) setError(result.error);
    } catch (e) {
      const msg = e.name === 'AbortError' ? 'Request timed out (10s). Code may have an infinite loop.' : `Connection failed: ${e.message}`;
      setError(msg);
      setOutput('');
    } finally { setRunning(false); }
  };

  // ── Trace ─────────────────────────────────────────
  const trace = async () => {
    setRunning(true); setOutput(''); setError(null); setSteps([]); setCurrentStep(-1);
    try {
      const result = await traceCode(code, userInput);
      if (result.steps?.length > 0) {
        setSteps(result.steps); setCurrentStep(0);
        setOutput(result.stdout || '(no output)');
        if (result.stderr) setError(result.stderr);
        setActiveTab('explain');
      } else {
        setOutput(result.stderr || 'No steps captured.');
      }
    } catch (e) {
      const msg = e.name === 'AbortError' ? 'Trace timed out (10s). Code may be too complex.' : `Connection failed: ${e.message}`;
      setError(msg);
    } finally { setRunning(false); }
  };

  const reset = () => { setSteps([]); setCurrentStep(-1); setOutput(''); setError(null); };

  // ── Step button helper ────────────────────────────
  const StepBtn = ({ label, fn, dis }) => (
    <button onClick={fn} disabled={dis}
      className={`px-2.5 py-1 border rounded-md text-xs font-bold transition-all cursor-pointer disabled:cursor-default
        ${isDark
          ? 'border-border bg-bg2 text-text2 hover:bg-accent hover:text-white hover:border-accent disabled:opacity-25'
          : 'border-border bg-white text-text2 hover:bg-accent hover:text-white hover:border-accent disabled:opacity-25'
        }`}>
      {label}
    </button>
  );

  return (
    <div className="h-screen flex flex-col bg-bg">
      {/* ── Header ────────────────────────────────── */}
      <motion.header
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className={`flex items-center justify-between px-5 py-2.5 border-b border-border z-10 backdrop-blur-xl
          ${isDark ? 'bg-panel/80' : 'bg-white/80'}`}
      >
        <div className="flex items-center gap-3">
          <span className="text-xl">⚡</span>
          <h1 className="text-base font-extrabold bg-gradient-to-r from-accent-light to-purple-400 bg-clip-text text-transparent"
              style={{ fontFamily: "'Times New Roman', serif" }}>
            CodeFlow
          </h1>
        </div>

        {/* Step controls */}
        {steps.length > 0 && (
          <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
            className="flex items-center gap-1">
            <StepBtn label="⏮" fn={() => setCurrentStep(0)} dis={currentStep === 0} />
            <StepBtn label="◀" fn={() => setCurrentStep(s => Math.max(0, s - 1))} dis={currentStep === 0} />
            <div className="px-3 py-1 bg-accent/10 rounded-lg text-xs font-mono font-bold text-accent-light mx-1">
              Step {currentStep + 1}/{steps.length} · L{cur?.line}
            </div>
            <StepBtn label="▶" fn={() => setCurrentStep(s => Math.min(steps.length - 1, s + 1))} dis={currentStep >= steps.length - 1} />
            <StepBtn label="⏭" fn={() => setCurrentStep(steps.length - 1)} dis={currentStep >= steps.length - 1} />
          </motion.div>
        )}

        <div className="flex items-center gap-2.5">
          {/* Theme toggle */}
          <button onClick={toggle}
            className={`w-9 h-9 rounded-full flex items-center justify-center border transition-all cursor-pointer text-base
              ${isDark
                ? 'border-border bg-bg2 hover:bg-accent/20 hover:border-accent'
                : 'border-border bg-white hover:bg-accent/10 hover:border-accent shadow-sm'}`}>
            {isDark ? '🌙' : '☀️'}
          </button>
          <span className="text-[0.6rem] font-bold bg-accent text-white px-2.5 py-1 rounded-full">Python</span>
        </div>
      </motion.header>

      {/* ── Main ──────────────────────────────────── */}
      <main className="flex-1 grid grid-cols-[1fr_1fr_280px] gap-2.5 p-2.5 min-h-0">

        {/* LEFT — Editor */}
        <motion.div
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.05 }}
          className={`border rounded-xl flex flex-col overflow-hidden min-h-0 shadow-lg
            ${isDark ? 'bg-panel border-border' : 'bg-white border-border shadow-gray-200'}`}
        >
          <div className="flex items-center justify-between px-3.5 py-2 border-b border-border">
            <span className="text-xs font-semibold text-text2">📝 Editor</span>
            <span className="text-[0.6rem] font-mono text-text3 bg-bg2 px-2 py-0.5 rounded">
              main.py{cur && <span className="text-accent-light font-bold">:{cur.line}</span>}
            </span>
          </div>
          <div className="flex-1 min-h-0">
            <Editor
              defaultLanguage="python"
              value={code}
              onChange={v => { setCode(v || ''); reset(); }}
              onMount={handleEditorMount}
              options={{
                fontSize: 14,
                fontFamily: "'JetBrains Mono', monospace",
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                renderLineHighlight: 'none',
                glyphMargin: true,
                padding: { top: 10 },
                smoothScrolling: true,
                cursorSmoothCaretAnimation: 'on',
              }}
            />
          </div>
          {/* Actions */}
          <div className="flex items-center gap-2 px-3.5 py-2 border-t border-border">
            <button onClick={run} disabled={running}
              className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-green text-white text-xs font-bold hover:brightness-110 hover:-translate-y-px hover:shadow-lg hover:shadow-green/20 disabled:opacity-50 transition-all cursor-pointer disabled:cursor-not-allowed">
              {running ? <><span className="spinner" /> Running...</> : <>▶ Run</>}
            </button>
            <button onClick={trace} disabled={running}
              className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-accent text-white text-xs font-bold hover:brightness-110 hover:-translate-y-px hover:shadow-lg hover:shadow-accent/20 disabled:opacity-50 transition-all cursor-pointer disabled:cursor-not-allowed">
              🔍 Trace
            </button>
            <button onClick={() => setShowInput(!showInput)}
              className="text-[0.65rem] font-mono text-text3 border border-border rounded-md px-2.5 py-1 hover:text-accent-light hover:border-accent transition-all cursor-pointer">
              {showInput ? '▾' : '▸'} stdin
            </button>
          </div>
          <AnimatePresence>
            {showInput && (
              <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }} className="overflow-hidden border-t border-border">
                <div className="px-3.5 py-2">
                  <div className="text-[0.55rem] font-bold text-text3 uppercase tracking-wider mb-1">⌨ stdin</div>
                  <textarea value={userInput} onChange={e => setUserInput(e.target.value)}
                    placeholder="One value per line..." spellCheck={false} rows={2}
                    className="w-full resize-none border border-border rounded-md px-2.5 py-1.5 bg-bg font-mono text-xs text-accent-light outline-none focus:border-accent" />
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* CENTER — Tabs */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className={`border rounded-xl flex flex-col overflow-hidden min-h-0 shadow-lg
            ${isDark ? 'bg-panel border-border' : 'bg-white border-border shadow-gray-200'}`}
        >
          <div className="flex items-center gap-0 border-b border-border">
            {[
              { id: 'output', label: '💻 Output' },
              { id: 'flow', label: '🔀 Flow' },
              { id: 'explain', label: '🤖 AI Explain' },
            ].map(t => (
              <button key={t.id} onClick={() => setActiveTab(t.id)}
                className={`flex-1 px-3 py-2 text-xs font-semibold transition-all cursor-pointer
                  ${activeTab === t.id
                    ? 'text-accent-light border-b-2 border-accent bg-accent/5'
                    : 'text-text3 hover:text-text2'}`}>
                {t.label}
              </button>
            ))}
            {output && !running && (
              <button onClick={reset}
                className="text-[0.6rem] text-text3 border border-border rounded px-2 py-0.5 mr-2 hover:text-text hover:border-text3 transition-all cursor-pointer">
                Clear
              </button>
            )}
          </div>

          <div className="flex-1 min-h-0 overflow-hidden">
            <AnimatePresence mode="wait">
              {activeTab === 'output' && (
                <motion.div key="output" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  className="h-full flex flex-col">
                  {/* Error banner */}
                  {error && (
                    <div className="error-banner m-2.5 animate-fade-up">
                      ❌ {error}
                    </div>
                  )}
                  <pre className={`flex-1 p-3.5 font-mono text-xs leading-relaxed overflow-auto whitespace-pre-wrap break-all
                    ${error && !output ? 'text-red' : 'text-green'}`}>
                    {output || (error ? '' : 'Output will appear here...')}
                  </pre>
                </motion.div>
              )}
              {activeTab === 'flow' && (
                <motion.div key="flow" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  className="h-full" style={{ background: isDark ? '#080c14' : '#f1f5f9' }}>
                  <FlowDiagram code={code} currentLine={cur?.line} steps={steps} currentStep={currentStep} isDark={isDark} />
                </motion.div>
              )}
              {activeTab === 'explain' && (
                <motion.div key="explain" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  className="h-full overflow-auto">
                  <ExplanationPanel code={code} stepData={cur} prevStep={prev}
                    codeLine={cur ? codeLines[cur.line - 1] : ''} isDark={isDark} />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        {/* RIGHT — Memory */}
        <motion.div
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.15 }}
          className={`border rounded-xl flex flex-col overflow-hidden min-h-0 shadow-lg
            ${isDark ? 'bg-panel border-border' : 'bg-white border-border shadow-gray-200'}`}
        >
          <div className="flex items-center justify-between px-3.5 py-2 border-b border-border">
            <span className="text-xs font-semibold text-text2">🧠 Memory</span>
            {cur && (
              <span className="text-[0.6rem] font-mono font-bold text-accent-light bg-accent/10 px-2 py-0.5 rounded-full">
                Line {cur.line}
              </span>
            )}
          </div>
          <div className="flex-1 overflow-y-auto">
            <MemoryPanel vars={cur?.vars || {}} prevVars={prev?.vars || {}}
              line={cur?.line} codeLine={cur ? codeLines[cur.line - 1] : ''} isDark={isDark} />
          </div>
        </motion.div>
      </main>
    </div>
  );
}
