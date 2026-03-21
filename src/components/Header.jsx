import { useApp } from '../context/AppContext';

function Header() {
  const { 
    sessionTitle, setSessionTitle, 
    save, exportToJson, 
    lastSavedId 
  } = useApp();

  return (
    <header className="glass-effect border-b border-border sticky top-0 z-50">
      <div className="flex items-center justify-between px-5 py-3">
        {/* Logo + Title */}
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-accent to-purple-500 flex items-center justify-center shadow-lg shadow-accent-glow">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="16 18 22 12 16 6" />
                  <polyline points="8 6 2 12 8 18" />
                  <line x1="14" y1="4" x2="10" y2="20" />
                </svg>
              </div>
              <div className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-success rounded-full border-2 border-bg-primary" />
            </div>
            <div>
              <h1 className="text-base font-bold tracking-tight text-text-primary">
                CodeFlow <span className="text-accent-light">Visualizer</span>
              </h1>
              <p className="text-[0.625rem] text-text-muted font-medium -mt-0.5">Runtime Execution Engine</p>
            </div>
          </div>

          {/* Session Title Input */}
          <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 bg-bg-secondary rounded-lg border border-border group focus-within:border-accent/40 transition-colors">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="text-text-muted">
              <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
              <path d="M18.5 2.5a2.121 2.121 0 113 3L12 15l-4 1 1-4 9.5-9.5z" />
            </svg>
            <input 
              type="text" 
              value={sessionTitle}
              onChange={(e) => setSessionTitle(e.target.value)}
              className="bg-transparent border-none outline-none text-[0.7rem] font-medium text-text-secondary w-40 placeholder:text-text-muted/50"
              placeholder="Session Title..."
            />
          </div>
        </div>

        {/* Navigation & Actions */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1 pr-3 border-r border-border">
            <button
              onClick={save}
              title="Save Session & Create Shareable Link"
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-accent-light bg-accent/10 border border-accent/20 rounded-lg hover:bg-accent/20 transition-all cursor-pointer"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z" />
                <polyline points="17 21 17 13 7 13 7 21" />
                <polyline points="7 3 7 8 15 8" />
              </svg>
              {lastSavedId ? 'Saved' : 'Save'}
            </button>

            <button
              onClick={exportToJson}
              title="Export execution as JSON"
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-text-muted rounded-lg hover:text-text-primary hover:bg-bg-panel-hover transition-all cursor-pointer"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
              </svg>
              Export
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button className="w-8 h-8 rounded-lg bg-bg-secondary border border-border flex items-center justify-center text-text-muted hover:text-text-primary hover:border-border-light transition-all cursor-pointer">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M18.36 18.36l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.66 6.34l1.42-1.42" />
              </svg>
            </button>
            <button className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center text-white shadow-lg shadow-accent/20 cursor-pointer">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M12 5v14M5 12h14" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
