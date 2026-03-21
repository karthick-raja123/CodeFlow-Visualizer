import { useMemo } from 'react';
import { motion } from 'framer-motion';

export default function MemoryPanel({ vars, prevVars, line, codeLine, isDark }) {
  const entries = Object.entries(vars || {});

  const changes = useMemo(() => {
    const c = {};
    for (const [key, value] of entries) {
      const prev = prevVars?.[key];
      if (prev === undefined) c[key] = 'new';
      else if (prev !== value) c[key] = 'changed';
    }
    return c;
  }, [entries, prevVars]);

  if (entries.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-text3 gap-3 p-6">
        <span className="text-4xl">📦</span>
        <p className="text-xs">No variables in scope</p>
        <p className="text-[0.65rem] opacity-60">Click <strong>🔍 Trace</strong> and step through code</p>
      </div>
    );
  }

  return (
    <div className="p-2.5 space-y-2.5">
      {codeLine && (
        <div className={`flex items-center gap-2 px-2.5 py-1.5 rounded-md font-mono text-[0.7rem]
          ${isDark ? 'bg-bg' : 'bg-bg2'}`}>
          <span className="text-[0.55rem] font-bold text-accent bg-accent/15 px-1.5 py-0.5 rounded shrink-0">L{line}</span>
          <code className="text-text truncate">{codeLine.trim()}</code>
        </div>
      )}

      <div className="text-[0.55rem] font-bold text-text3 uppercase tracking-wider">Variables</div>
      <div className="grid grid-cols-2 gap-1.5">
        {entries.map(([name, value]) => {
          const status = changes[name];
          return (
            <motion.div key={name} layout
              initial={status === 'new' ? { scale: 0.9, opacity: 0 } : false}
              animate={{ scale: 1, opacity: 1 }}
              className={`rounded-lg p-2 border transition-all
                ${status === 'new'
                  ? 'border-green/50 bg-green/5 animate-box-new'
                  : status === 'changed'
                  ? 'border-orange/50 bg-orange/5 animate-box-pulse'
                  : isDark
                  ? 'border-border bg-bg2 hover:border-accent/40'
                  : 'border-border bg-bg2 hover:border-accent/40'}`}>
              <div className="flex items-center justify-between mb-0.5">
                <span className="font-mono text-[0.7rem] font-bold text-accent-light">{name}</span>
                {status === 'new' && <span className="text-[0.45rem] font-bold bg-green text-white px-1.5 py-px rounded">NEW</span>}
                {status === 'changed' && <span className="text-[0.45rem] font-bold bg-orange text-white px-1.5 py-px rounded">UPD</span>}
              </div>
              <div className="font-mono text-sm font-semibold text-orange break-all leading-tight">{value}</div>
              <div className="font-mono text-[0.5rem] text-text3 mt-0.5">{detectType(value)}</div>
            </motion.div>
          );
        })}
      </div>

      <div className="text-[0.55rem] font-bold text-text3 uppercase tracking-wider">Stack Frame</div>
      <div className={`border rounded-lg overflow-hidden ${isDark ? 'bg-bg border-border' : 'bg-bg2 border-border'}`}>
        <div className="flex items-center gap-1.5 px-2.5 py-1.5 bg-accent/8 border-b border-border text-[0.65rem] font-bold font-mono text-accent-light">
          📚 &lt;module&gt;
        </div>
        <div className="py-1">
          {entries.map(([name, value]) => (
            <div key={name} className="flex items-center gap-1.5 px-2.5 py-0.5 font-mono text-[0.6rem] hover:bg-accent/5">
              <span className="text-accent-light font-bold min-w-[50px]">{name}</span>
              <span className="text-text3">→</span>
              <span className="text-orange">{value.length > 20 ? value.slice(0, 18) + '…' : value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function detectType(val) {
  if (val === 'True' || val === 'False') return 'bool';
  if (val === 'None') return 'NoneType';
  if (/^-?\d+$/.test(val)) return 'int';
  if (/^-?\d+\.\d+$/.test(val)) return 'float';
  if (val.startsWith("'") || val.startsWith('"')) return 'str';
  if (val.startsWith('[')) return 'list';
  if (val.startsWith('{')) return 'dict';
  return 'object';
}
