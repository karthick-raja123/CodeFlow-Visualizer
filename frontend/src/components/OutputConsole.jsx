import { useEffect, useRef } from 'react';
import { useApp } from '../context/AppContext';

function OutputConsole() {
  const { output, clearOutput, status } = useApp();
  const scrollRef = useRef(null);

  // Auto-scroll to bottom on new output
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [output]);

  const colorMap = {
    info: 'text-sky-400/80',
    success: 'text-success',
    log: 'text-text-secondary',
    output: 'text-yellow-300 font-semibold',
    error: 'text-danger',
  };

  return (
    <div className="panel flex flex-col h-full overflow-hidden animate-slide-up" style={{ animationDelay: '0.2s' }}>
      <div className="panel-header">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="4 17 10 11 4 5" />
          <line x1="12" y1="19" x2="20" y2="19" />
        </svg>
        <span>Output Console</span>

        {/* Running spinner */}
        {status === 'running' && (
          <div className="ml-2 flex items-center gap-1.5 text-warning text-[0.625rem] font-medium">
            <svg className="animate-spin" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
            </svg>
            Running...
          </div>
        )}

        <div className="ml-auto flex items-center gap-1.5">
          <button
            onClick={clearOutput}
            className="p-1 rounded hover:bg-bg-panel-hover text-text-muted hover:text-text-primary transition-colors cursor-pointer"
            title="Clear console"
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6" />
            </svg>
          </button>
        </div>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-auto p-4 font-mono text-xs leading-5">
        {output.length === 0 && (
          <div className="text-text-muted/50 italic">Console output will appear here...</div>
        )}

        {output.map((line, i) => (
          <div
            key={`${i}-${line.timestamp}`}
            className={`${colorMap[line.type] || 'text-text-secondary'} animate-fade-in`}
            style={{ animationDelay: '0.02s' }}
          >
            {line.text}
          </div>
        ))}

        {/* Blinking cursor */}
        <div className="flex items-center mt-1">
          <span className={`mr-1 ${status === 'error' ? 'text-danger' : 'text-success'}`}>❯</span>
          <span className={`w-1.5 h-4 animate-blink ${status === 'error' ? 'bg-danger/80' : 'bg-success/80'}`} />
        </div>
      </div>
    </div>
  );
}

export default OutputConsole;
