import { createContext, useContext, useState, useCallback, useRef, useEffect } from 'react';
import { executeCode, getExplanation, saveSession, getSessionById } from '../services/api';

const AppContext = createContext(null);

export function AppProvider({ children }) {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [output, setOutput] = useState([]);
  const [status, setStatus] = useState('ready');
  const [executionMeta, setExecutionMeta] = useState({ line: 0, step: 0, totalSteps: 0, time: null });
  const [trace, setTrace] = useState([]);
  const [currentStep, setCurrentStep] = useState(-1);
  const [activeLine, setActiveLine] = useState(0);
  const [explanation, setExplanation] = useState(null);
  const [isExplaining, setIsExplaining] = useState(false);
  const [sessionTitle, setSessionTitle] = useState('Untitled Session');
  const [lastSavedId, setLastSavedId] = useState(null);
  const outputRef = useRef([]);
  const explanationAbortController = useRef(null);

  // ── Session: Load from URL ID ────────────────────────
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const sid = urlParams.get('sess');
    if (sid) {
      loadSession(sid);
    }
  }, []);

  const loadSession = useCallback(async (id) => {
    setStatus('running');
    try {
      const data = await getSessionById(id);
      setCode(data.code);
      setLanguage(data.language);
      setTrace(data.trace);
      setSessionTitle(data.title);
      setLastSavedId(data.id);
      
      // Navigate to the start of the trace
      if (data.trace.length > 0) {
        setCurrentStep(0);
        setActiveLine(data.trace[0].line);
        setExecutionMeta({ line: data.trace[0].line, step: 1, totalSteps: data.trace.length, time: 'Loaded' });
      }
      setStatus('stepping');
      addOutput({ type: 'success', text: `[OK]   Session '${data.title}' loaded successfully.`, timestamp: Date.now() });
    } catch (err) {
      addOutput({ type: 'error', text: `[ERR]  Failed to load session: ${err.message}`, timestamp: Date.now() });
      setStatus('error');
    }
  }, []);

  const save = useCallback(async () => {
    if (!code) return;
    try {
      const data = await saveSession({
        code,
        language,
        trace,
        title: sessionTitle
      });
      setLastSavedId(data.id);
      addOutput({ type: 'success', text: `[OK]   Session saved! ID: ${data.id}`, timestamp: Date.now() });
      
      // Update URL without reloading
      const url = new URL(window.location);
      url.searchParams.set('sess', data.id);
      window.history.pushState({}, '', url);
    } catch (err) {
      addOutput({ type: 'error', text: `[ERR]  Save failed: ${err.message}`, timestamp: Date.now() });
    }
  }, [code, language, trace, sessionTitle]);

  const exportToJson = useCallback(() => {
    const data = {
      title: sessionTitle,
      code,
      language,
      trace,
      exportedAt: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `execution-${sessionTitle.toLowerCase().replace(/\s+/g, '-')}.json`;
    link.click();
  }, [code, language, trace, sessionTitle]);

  const addOutput = useCallback((line) => {
    outputRef.current = [...outputRef.current, line];
    setOutput([...outputRef.current]);
  }, []);

  const clearOutput = useCallback(() => {
    outputRef.current = [];
    setOutput([]);
  }, []);

  const setExplanationData = useCallback(async (idx, traceData) => {
    if (idx < 0 || !traceData.length) {
      setExplanation(null);
      return;
    }

    if (explanationAbortController.current) {
      explanationAbortController.current.abort();
    }
    explanationAbortController.current = new AbortController();

    setIsExplaining(true);
    try {
      const stepData = traceData[idx];
      const prevStep = idx > 0 ? traceData[idx - 1] : null;
      const data = await getExplanation(code, stepData, prevStep);
      setExplanation(data);
    } catch (err) {
      if (err.name !== 'AbortError') {
        setExplanation({
          explanation: 'Failed to generate AI explanation.',
          detail: 'Check backend connection.',
          suggestion: 'Ensure GOOGLE_API_KEY is set in .env',
          concept: 'Error',
        });
      }
    } finally {
      setIsExplaining(false);
    }
  }, [code]);

  // ── Direct step navigation (from slider/buttons) ─────
  const setCurrentStepDirect = useCallback((idx) => {
    if (idx < 0 || !trace.length) return;
    const clampedIdx = Math.min(idx, trace.length - 1);
    setCurrentStep(clampedIdx);
    const traceStep = trace[clampedIdx];
    setActiveLine(traceStep.line);
    setExecutionMeta((prev) => ({
      ...prev,
      line: traceStep.line,
      step: clampedIdx + 1,
      totalSteps: trace.length,
    }));
    setExplanationData(clampedIdx, trace);
  }, [trace, setExplanationData]);

  // ── Run: execute all at once, stream output ──────────
  const run = useCallback(async () => {
    clearOutput();
    setTrace([]);
    setCurrentStep(-1);
    setActiveLine(0);
    setStatus('running');
    setExecutionMeta({ line: 0, step: 0, totalSteps: 0, time: null });

    addOutput({ type: 'info', text: `[INFO] Executing ${language} code...`, timestamp: Date.now() });

    try {
      const result = await executeCode(code, language);

      if (result.trace) {
        setTrace(result.trace);
      }

      for (let i = 0; i < result.steps.length; i++) {
        const step = result.steps[i];
        await new Promise((r) => setTimeout(r, 120));
        addOutput({ type: step.type || 'log', text: step.text, timestamp: Date.now() });
        setExecutionMeta((prev) => ({ ...prev, line: step.line || prev.line, step: i + 1, totalSteps: result.steps.length }));
      }

      if (result.output) {
        await new Promise((r) => setTimeout(r, 100));
        addOutput({ type: 'output', text: result.output, timestamp: Date.now() });
      }

      if (result.trace && result.trace.length > 0) {
        setCurrentStep(result.trace.length - 1);
        setActiveLine(result.trace[result.trace.length - 1].line);
      }

      setExecutionMeta((prev) => ({ ...prev, time: result.executionTime }));
      addOutput({ type: 'success', text: `[OK]   Execution completed in ${result.executionTime}`, timestamp: Date.now() });
      setStatus('completed');
    } catch (err) {
      addOutput({ type: 'error', text: `[ERR]  ${err.message}`, timestamp: Date.now() });
      setStatus('error');
    }
  }, [code, language, addOutput, clearOutput]);

  // ── Step: execute all, then step through trace ───────
  const step = useCallback(async () => {
    if (trace.length === 0) {
      clearOutput();
      setStatus('running');
      setExecutionMeta({ line: 0, step: 0, totalSteps: 0, time: null });
      addOutput({ type: 'info', text: `[INFO] Running code for step-through...`, timestamp: Date.now() });

      try {
        const result = await executeCode(code, language);

        if (result.trace && result.trace.length > 0) {
          setTrace(result.trace);
          setCurrentStep(0);
          setActiveLine(result.trace[0].line);
          setExecutionMeta({ line: result.trace[0].line, step: 1, totalSteps: result.trace.length, time: result.executionTime });
          addOutput({ type: 'success', text: `[OK]   Loaded ${result.trace.length} trace steps. Use Step or the timeline to navigate.`, timestamp: Date.now() });
          setExplanationData(0, result.trace);

          if (result.trace[0].output) {
            addOutput({ type: 'output', text: result.trace[0].output, timestamp: Date.now() });
          }
        } else {
          addOutput({ type: 'info', text: '[INFO] No trace steps captured.', timestamp: Date.now() });
        }

        setStatus('stepping');
      } catch (err) {
        addOutput({ type: 'error', text: `[ERR]  ${err.message}`, timestamp: Date.now() });
        setStatus('error');
      }
      return;
    }

    const nextIdx = currentStep + 1;
    if (nextIdx < trace.length) {
      setCurrentStep(nextIdx);
      const traceStep = trace[nextIdx];
      setActiveLine(traceStep.line);
      setExecutionMeta((prev) => ({ ...prev, line: traceStep.line, step: nextIdx + 1 }));
      setStatus('stepping');
      setExplanationData(nextIdx, trace);

      if (traceStep.output) {
        addOutput({ type: 'output', text: traceStep.output, timestamp: Date.now() });
      }

      if (traceStep.event === 'call') {
        addOutput({ type: 'info', text: `  → call ${traceStep.function}()`, timestamp: Date.now() });
      } else if (traceStep.event === 'return' && traceStep.return_value) {
        addOutput({ type: 'info', text: `  ← return ${traceStep.return_value}`, timestamp: Date.now() });
      }
    } else {
      addOutput({ type: 'success', text: '[OK]   End of trace reached.', timestamp: Date.now() });
      setStatus('completed');
    }
  }, [trace, currentStep, code, language, addOutput, clearOutput]);

  // ── Reset ────────────────────────────────────────────
  const reset = useCallback(() => {
    clearOutput();
    setTrace([]);
    setCurrentStep(-1);
    setActiveLine(0);
    setStatus('ready');
    setExecutionMeta({ line: 0, step: 0, totalSteps: 0, time: null });
    addOutput({ type: 'info', text: '[INFO] Environment reset', timestamp: Date.now() });
  }, [clearOutput, addOutput]);

  const value = {
    code, setCode,
    language, setLanguage,
    output, clearOutput,
    status,
    executionMeta,
    trace, currentStep, activeLine,
    explanation, isExplaining,
    sessionTitle, setSessionTitle,
    save, loadSession, exportToJson,
    lastSavedId,
    setCurrentStepDirect,
    run, step, reset,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be used within AppProvider');
  return ctx;
}
