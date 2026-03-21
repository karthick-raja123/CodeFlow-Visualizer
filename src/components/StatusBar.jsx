function StatusBar() {
  return (
    <footer className="flex items-center justify-between px-4 py-1.5 bg-bg-secondary border-t border-border text-[0.6875rem] text-text-muted animate-fade-in">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-1.5">
          <div className="w-2 h-2 rounded-full bg-success" />
          <span>Connected</span>
        </div>
        <span className="text-border-light">|</span>
        <span>Python 3.11</span>
        <span className="text-border-light">|</span>
        <span>UTF-8</span>
      </div>
      <div className="flex items-center gap-3">
        <span>Ln 7, Col 12</span>
        <span className="text-border-light">|</span>
        <span>Spaces: 4</span>
        <span className="text-border-light">|</span>
        <span className="flex items-center gap-1">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
          0.003s
        </span>
      </div>
    </footer>
  );
}

export default StatusBar;
