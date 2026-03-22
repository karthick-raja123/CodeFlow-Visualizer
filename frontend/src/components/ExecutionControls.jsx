import { useApp } from '../context/AppContext';

function ExecutionControls() {
  const { status, executionMeta, run, step, reset } = useApp();

  const isRunning = status === 'running';

  const buttons = [
    {
      label: 'Run',
      shortcut: 'F5',
      color: 'bg-success hover:shadow-[0_0_20px_rgba(34,197,94,0.3)]',
      hoverBg: 'hover:bg-green-500',
      disabled: isRunning,
      icon: isRunning ? (
        <svg className="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
          <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
        </svg>
      ) : (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <polygon points="5 3 19 12 5 21 5 3" />
        </svg>
      ),
      onClick: run,
    },
    {
      label: 'Step',
      shortcut: 'F10',
      color: 'bg-info hover:shadow-[0_0_20px_rgba(59,130,246,0.3)]',
      hoverBg: 'hover:bg-blue-500',
      disabled: isRunning,
      icon: (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="9 18 15 12 9 6" />
        </svg>
      ),
      onClick: step,
    },
    {
      label: 'Reset',
      shortcut: 'Ctrl+R',
      color: 'bg-danger hover:shadow-[0_0_20px_rgba(239,68,68,0.3)]',
      hoverBg: 'hover:bg-red-500',
      disabled: false,
      icon: (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="1 4 1 10 7 10" />
          <path d="M3.51 15a9 9 0 102.13-9.36L1 10" />
        </svg>
      ),
      onClick: reset,
    },
  ];

  const statusConfig = {
    ready: { text: 'Ready', dot: 'bg-success', pulse: false },
    running: { text: 'Running...', dot: 'bg-warning', pulse: true },
    stepping: { text: 'Step Mode', dot: 'bg-info', pulse: true },
    completed: { text: 'Completed', dot: 'bg-success', pulse: false },
    error: { text: 'Error', dot: 'bg-danger', pulse: false },
  };

  const currentStatus = statusConfig[status] || statusConfig.ready;

  return (
    <div className="panel animate-slide-up" style={{ animationDelay: '0.3s' }}>
      <div className="flex items-center justify-between px-4 py-3 flex-wrap gap-3">
        {/* Buttons */}
        <div className="flex items-center gap-2">
          {buttons.map(({ label, shortcut, color, hoverBg, icon, onClick, disabled }) => (
            <button
              key={label}
              onClick={onClick}
              disabled={disabled}
              className={`group flex items-center gap-2 px-4 py-2 rounded-lg text-white text-sm font-semibold transition-all duration-200 cursor-pointer active:scale-95 ${color} ${hoverBg} ${disabled ? 'opacity-50 cursor-not-allowed active:scale-100' : ''}`}
            >
              {icon}
              <span>{label}</span>
              <kbd className="hidden sm:inline-block ml-1 px-1.5 py-0.5 text-[0.6rem] bg-white/15 rounded font-mono">
                {shortcut}
              </kbd>
            </button>
          ))}
        </div>

        {/* Status + Meta */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-xs text-text-secondary">
            <div className="flex items-center gap-1.5">
              <div className={`w-2 h-2 rounded-full ${currentStatus.dot} ${currentStatus.pulse ? 'animate-pulse' : ''}`} />
              <span className="font-medium">{currentStatus.text}</span>
            </div>
          </div>

          <div className="hidden sm:flex items-center gap-2 text-xs text-text-muted">
            <span>Speed:</span>
            <div className="flex items-center gap-0.5">
              {['0.5x', '1x', '2x'].map((speed) => (
                <button
                  key={speed}
                  className={`px-2 py-0.5 rounded text-[0.625rem] font-mono transition-all cursor-pointer ${
                    speed === '1x'
                      ? 'bg-accent/20 text-accent-light'
                      : 'hover:bg-bg-panel-hover text-text-muted hover:text-text-secondary'
                  }`}
                >
                  {speed}
                </button>
              ))}
            </div>
          </div>

          {executionMeta.step > 0 && (
            <div className="hidden md:flex items-center gap-2 text-xs text-text-muted">
              {executionMeta.line > 0 && (
                <>
                  <span>Line:</span>
                  <span className="text-text-secondary font-mono">{executionMeta.line}</span>
                  <span className="mx-1 text-border-light">|</span>
                </>
              )}
              <span>Step:</span>
              <span className="text-text-secondary font-mono">{executionMeta.step}/{executionMeta.totalSteps}</span>
              {executionMeta.time && (
                <>
                  <span className="mx-1 text-border-light">|</span>
                  <span className="text-success font-mono">{executionMeta.time}</span>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ExecutionControls;
