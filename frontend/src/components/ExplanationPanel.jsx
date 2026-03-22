import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function ExplanationPanel({ code, stepData, prevStep, codeLine, isDark }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetchError, setFetchError] = useState(null);
  const prevLine = useRef(null);

  useEffect(() => {
    if (!stepData || !code) { setData(null); return; }
    if (prevLine.current === stepData.line && data) return;
    prevLine.current = stepData.line;

    const timer = setTimeout(async () => {
      setLoading(true); setFetchError(null);
      try {
        const res = await fetch(`${API}/explain`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code, step_data: stepData, prev_step: prevStep }),
        });
        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        setData(await res.json());
      } catch (e) {
        setFetchError(e.message);
        setData({
          explanation: `📍 Executing line ${stepData.line}.`,
          changes: {}, concept: '', suggestion: '',
          source: codeLine?.trim() || '', line: stepData.line,
        });
      } finally { setLoading(false); }
    }, 100);
    return () => clearTimeout(timer);
  }, [stepData, code, prevStep, codeLine]);

  if (!stepData) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-text3 gap-3 p-6">
        <span className="text-4xl">🤖</span>
        <p className="text-xs text-center">Click <strong className="text-accent-light">🔍 Trace</strong> to get AI-powered explanations</p>
      </div>
    );
  }

  if (loading && !data) {
    return (
      <div className="flex items-center justify-center h-full gap-2 text-text3">
        <span className="spinner" />
        <span className="text-xs">Analyzing...</span>
      </div>
    );
  }

  if (!data) return null;

  const changes = Object.entries(data.changes || {});

  return (
    <div className="p-3.5 space-y-3">
      {/* Error fallback */}
      {fetchError && (
        <div className="error-banner text-xs animate-fade-up">
          ⚠️ Backend unreachable — showing local explanation
        </div>
      )}

      {/* Main explanation */}
      <motion.div key={data.line} initial={{ y: 8, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
        className={`rounded-lg p-3.5 border ${isDark
          ? 'bg-gradient-to-br from-accent/10 to-transparent border-accent/20'
          : 'bg-accent/5 border-accent/15'}`}>
        <div className="flex items-start gap-2.5">
          <span className="text-lg mt-0.5">💡</span>
          <div>
            <h4 className="text-[0.65rem] font-bold text-text2 uppercase tracking-wider mb-1">What's Happening</h4>
            <p className="text-xs text-text leading-relaxed" dangerouslySetInnerHTML={{ __html: markdownBold(data.explanation) }} />
          </div>
        </div>
      </motion.div>

      {/* Variable changes */}
      {changes.length > 0 && (
        <motion.div initial={{ y: 8, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.05 }}
          className={`rounded-lg p-3 border ${isDark ? 'bg-bg2/50 border-border' : 'bg-bg2 border-border'}`}>
          <h4 className="text-[0.6rem] font-bold text-text3 uppercase tracking-wider mb-2">📊 Variable Changes</h4>
          <div className="space-y-1.5">
            {changes.map(([name, ch]) => (
              <div key={name} className="flex items-center gap-2 text-xs font-mono">
                <span className={`px-1.5 py-0.5 rounded text-[0.6rem] font-bold ${ch.status === 'new' ? 'bg-green/20 text-green' : 'bg-orange/20 text-orange'}`}>
                  {ch.status === 'new' ? 'NEW' : 'UPD'}
                </span>
                <span className="text-accent-light font-bold">{name}</span>
                {ch.status === 'changed' && (
                  <><span className="text-text3">{ch.from}</span><span className="text-text3">→</span></>
                )}
                <span className="text-orange font-semibold">{ch.to}</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* CS Concept */}
      {data.concept && (
        <motion.div initial={{ y: 8, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.1 }}
          className={`rounded-lg p-3 border ${isDark ? 'bg-teal/5 border-teal/20' : 'bg-teal/5 border-teal/15'}`}>
          <p className="text-xs text-teal leading-relaxed font-medium" dangerouslySetInnerHTML={{ __html: markdownBold(data.concept) }} />
        </motion.div>
      )}

      {/* Suggestion */}
      {data.suggestion && (
        <motion.div initial={{ y: 8, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.15 }}
          className={`rounded-lg p-3 border ${data.suggestion.startsWith('⚠')
            ? 'bg-orange/5 border-orange/20'
            : 'bg-accent/5 border-accent/20'}`}>
          <p className="text-xs text-text2 leading-relaxed" dangerouslySetInnerHTML={{ __html: markdownBold(data.suggestion) }} />
        </motion.div>
      )}

      {/* Source line */}
      <div className={`flex items-center gap-2 px-3 py-2 rounded-lg border ${isDark ? 'bg-bg border-border' : 'bg-bg2 border-border'}`}>
        <span className="text-[0.55rem] font-bold text-accent bg-accent/15 px-1.5 py-0.5 rounded font-mono">L{data.line}</span>
        <code className="text-xs font-mono text-text truncate">{data.source}</code>
      </div>
    </div>
  );
}

function markdownBold(text) {
  return (text || '').replace(/\*\*(.+?)\*\*/g, '<strong class="text-accent-light">$1</strong>');
}
