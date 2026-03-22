import { useApp } from '../context/AppContext';

function TimelineSlider() {
  const { trace, currentStep, setCurrentStepDirect, status } = useApp();

  if (trace.length === 0) return null;

  const step = trace[currentStep] || null;
  const progress = trace.length > 1 ? (currentStep / (trace.length - 1)) * 100 : 0;

  // Group steps by event type for the dot indicators
  const eventColors = {
    call: 'bg-sky-400',
    return: 'bg-emerald-400',
    line: 'bg-accent-light',
    exception: 'bg-danger',
    limit: 'bg-warning',
  };

  return (
    <div className="panel animate-fade-in px-4 py-3">
      {/* Header row */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2 text-xs text-text-secondary">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
          <span className="font-semibold">Execution Timeline</span>
        </div>

        <div className="flex items-center gap-3 text-[0.6875rem]">
          {/* Step navigation buttons */}
          <div className="flex items-center gap-1">
            <button
              onClick={() => setCurrentStepDirect(0)}
              disabled={currentStep === 0}
              className="p-1 rounded hover:bg-bg-panel-hover text-text-muted hover:text-text-primary disabled:opacity-30 transition-colors cursor-pointer disabled:cursor-default"
              title="First step"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <polyline points="11 17 6 12 11 7" /><polyline points="18 17 13 12 18 7" />
              </svg>
            </button>
            <button
              onClick={() => setCurrentStepDirect(Math.max(0, currentStep - 1))}
              disabled={currentStep === 0}
              className="p-1 rounded hover:bg-bg-panel-hover text-text-muted hover:text-text-primary disabled:opacity-30 transition-colors cursor-pointer disabled:cursor-default"
              title="Previous step"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <polyline points="15 18 9 12 15 6" />
              </svg>
            </button>
            <span className="px-2 font-mono text-text-primary font-semibold min-w-[60px] text-center">
              {currentStep + 1} / {trace.length}
            </span>
            <button
              onClick={() => setCurrentStepDirect(Math.min(trace.length - 1, currentStep + 1))}
              disabled={currentStep >= trace.length - 1}
              className="p-1 rounded hover:bg-bg-panel-hover text-text-muted hover:text-text-primary disabled:opacity-30 transition-colors cursor-pointer disabled:cursor-default"
              title="Next step"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <polyline points="9 18 15 12 9 6" />
              </svg>
            </button>
            <button
              onClick={() => setCurrentStepDirect(trace.length - 1)}
              disabled={currentStep >= trace.length - 1}
              className="p-1 rounded hover:bg-bg-panel-hover text-text-muted hover:text-text-primary disabled:opacity-30 transition-colors cursor-pointer disabled:cursor-default"
              title="Last step"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <polyline points="13 17 18 12 13 7" /><polyline points="6 17 11 12 6 7" />
              </svg>
            </button>
          </div>

          {/* Current event */}
          {step && (
            <span className={`px-2 py-0.5 rounded text-[0.625rem] font-mono font-medium ${
              step.event === 'call' ? 'bg-sky-500/15 text-sky-300' :
              step.event === 'return' ? 'bg-emerald-500/15 text-emerald-300' :
              step.event === 'exception' ? 'bg-red-500/15 text-red-300' :
              'bg-accent/15 text-accent-light'
            }`}>
              {step.event === 'call' && `→ ${step.function}()`}
              {step.event === 'return' && `← return`}
              {step.event === 'line' && `line ${step.line}`}
              {step.event === 'exception' && `⚠ error`}
              {step.event === 'limit' && `limit`}
            </span>
          )}
        </div>
      </div>

      {/* Slider track */}
      <div className="relative">
        {/* Background track */}
        <div className="h-1.5 bg-bg-secondary rounded-full overflow-hidden">
          {/* Progress fill */}
          <div
            className="h-full bg-gradient-to-r from-accent to-accent-light rounded-full transition-all duration-200 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Range input */}
        <input
          type="range"
          min={0}
          max={trace.length - 1}
          value={currentStep}
          onChange={(e) => setCurrentStepDirect(Number(e.target.value))}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />

        {/* Event dot markers (show key events on the track) */}
        <div className="absolute inset-0 flex items-center pointer-events-none">
          {trace.map((t, i) => {
            // Only show dots for call/return events to avoid clutter
            if (t.event !== 'call' && t.event !== 'return' && t.event !== 'exception') return null;
            const left = trace.length > 1 ? (i / (trace.length - 1)) * 100 : 0;
            return (
              <div
                key={i}
                className={`absolute w-2 h-2 rounded-full -translate-x-1/2 ${eventColors[t.event] || 'bg-text-muted'} ${
                  i === currentStep ? 'ring-2 ring-white/30 scale-125' : 'opacity-60'
                } transition-all duration-200`}
                style={{ left: `${left}%` }}
              />
            );
          })}
        </div>

        {/* Current position thumb */}
        <div
          className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-3.5 h-3.5 rounded-full bg-accent border-2 border-bg-primary shadow-lg shadow-accent-glow transition-all duration-200 ease-out pointer-events-none"
          style={{ left: `${progress}%` }}
        />
      </div>

      {/* Legend */}
      <div className="flex items-center gap-3 mt-2 text-[0.5625rem] text-text-muted">
        <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-sky-400 inline-block" /> call</span>
        <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" /> return</span>
        <span className="flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-accent-light inline-block" /> line</span>
        {step && (
          <span className="ml-auto font-mono text-text-secondary">
            {step.function}() : {step.line}
          </span>
        )}
      </div>
    </div>
  );
}

export default TimelineSlider;
