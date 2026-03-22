import { useEffect, useRef } from 'react';
import Editor from '@monaco-editor/react';
import { useApp } from '../context/AppContext';

const sampleCode = {
  python: `def fibonacci(n):
    """Calculate fibonacci sequence"""
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b

    return b

# Main execution
result = fibonacci(10)
print(f"Fibonacci(10) = {result}")
`,
  java: `public class Main {
    /**
     * Calculate fibonacci sequence
     */
    public static int fibonacci(int n) {
        if (n <= 1) return n;

        int a = 0, b = 1;
        for (int i = 2; i <= n; i++) {
            int temp = b;
            b = a + b;
            a = temp;
        }
        return b;
    }

    public static void main(String[] args) {
        int result = fibonacci(10);
        System.out.println("Fibonacci(10) = " + result);
    }
}
`,
};

const languageConfig = {
  python: { label: 'Python', file: 'main.py', icon: '🐍' },
  java: { label: 'Java', file: 'Main.java', icon: '☕' },
};

function CodeEditor() {
  const { code, setCode, language, setLanguage, activeLine, trace, currentStep } = useApp();
  const editorRef = useRef(null);
  const decorationsRef = useRef([]);

  // Set initial code on mount and language change
  useEffect(() => {
    setCode(sampleCode[language]);
  }, [language, setCode]);

  // Highlight the active line in the editor
  useEffect(() => {
    const editor = editorRef.current;
    if (!editor || activeLine <= 0) return;

    const step = trace[currentStep];
    const isCall = step?.event === 'call';
    const isReturn = step?.event === 'return';
    const isException = step?.event === 'exception';

    // Determine highlight color based on event type
    let lineClassName = 'active-line-highlight';
    let glyphClassName = 'active-line-glyph';
    if (isCall) {
      lineClassName = 'call-line-highlight';
      glyphClassName = 'call-line-glyph';
    } else if (isReturn) {
      lineClassName = 'return-line-highlight';
      glyphClassName = 'return-line-glyph';
    } else if (isException) {
      lineClassName = 'error-line-highlight';
      glyphClassName = 'error-line-glyph';
    }

    decorationsRef.current = editor.deltaDecorations(decorationsRef.current, [
      {
        range: {
          startLineNumber: activeLine,
          startColumn: 1,
          endLineNumber: activeLine,
          endColumn: 1,
        },
        options: {
          isWholeLine: true,
          className: lineClassName,
          glyphMarginClassName: glyphClassName,
        },
      },
    ]);

    // Scroll to the active line
    editor.revealLineInCenter(activeLine);
  }, [activeLine, trace, currentStep]);

  // Clear decorations when trace is empty
  useEffect(() => {
    if (trace.length === 0 && editorRef.current) {
      decorationsRef.current = editorRef.current.deltaDecorations(decorationsRef.current, []);
    }
  }, [trace]);

  const handleEditorDidMount = (editor) => {
    editorRef.current = editor;
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const config = languageConfig[language];

  return (
    <div className="panel flex flex-col h-full overflow-hidden animate-slide-up" style={{ animationDelay: '0.1s' }}>
      {/* Tab bar */}
      <div className="flex items-center justify-between border-b border-border">
        <div className="flex items-center">
          <div className="flex items-center gap-2 px-4 py-2.5 bg-bg-panel border-b-2 border-accent text-text-primary text-xs font-medium">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M13 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V9z" />
              <polyline points="13 2 13 9 20 9" />
            </svg>
            {config.file}
            {activeLine > 0 && (
              <span className="ml-1 px-1.5 py-0.5 bg-accent/15 text-accent-light text-[0.5625rem] rounded font-mono">
                :{activeLine}
              </span>
            )}
          </div>
        </div>

        {/* Language Selector */}
        <div className="flex items-center gap-2 px-3">
          <select
            value={language}
            onChange={handleLanguageChange}
            className="appearance-none bg-accent/10 text-accent-light text-[0.6875rem] font-semibold rounded-md px-2.5 py-1 border border-accent/20 hover:border-accent/40 focus:outline-none focus:ring-1 focus:ring-accent/50 cursor-pointer transition-all"
            style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23818cf8' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E")`,
              backgroundRepeat: 'no-repeat',
              backgroundPosition: 'right 6px center',
              paddingRight: '24px',
            }}
          >
            {Object.entries(languageConfig).map(([key, cfg]) => (
              <option key={key} value={key}>
                {cfg.icon} {cfg.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Monaco Editor */}
      <div className="flex-1 min-h-0">
        <Editor
          height="100%"
          language={language}
          value={code}
          onChange={(value) => setCode(value || '')}
          onMount={handleEditorDidMount}
          theme="vs-dark"
          options={{
            fontSize: 14,
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            fontLigatures: true,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            padding: { top: 12, bottom: 12 },
            lineHeight: 22,
            renderLineHighlight: 'none',
            cursorBlinking: 'smooth',
            cursorSmoothCaretAnimation: 'on',
            smoothScrolling: true,
            bracketPairColorization: { enabled: true },
            automaticLayout: true,
            wordWrap: 'on',
            tabSize: 4,
            glyphMargin: true,
            scrollbar: {
              verticalScrollbarSize: 6,
              horizontalScrollbarSize: 6,
              verticalSliderSize: 6,
            },
          }}
        />
      </div>
    </div>
  );
}

export default CodeEditor;
