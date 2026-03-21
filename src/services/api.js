/**
 * API service for code execution.
 * Connects to the FastAPI backend at /api/execute.
 * Supports both local development and Vercel serverless deployment.
 */

// Use relative /api path for serverless, or localhost for development
const API_BASE = process.env.VITE_API_URL || '/api';

// ── Real API call ────────────────────────────────────
async function callBackend(code, language, input_data = '') {
  try {
    const endpoint = `${API_BASE}/execute`;
    console.log(`[API] Calling ${endpoint}`);

    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, input_data }),
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `Server error: ${res.status}`);
    }

    const data = await res.json();

    // Handle serverless response format
    return {
      success: !data.error,
      output: data.output || '',
      error: data.error || '',
      status: data.status || 'success',
      executionTime: data.execution_time,
      steps: data.steps || [],
      trace: data.trace || [],
      traceExceeded: data.trace_exceeded || false,
    };
  } catch (err) {
    console.error('[API] Error:', err);
    return {
      success: false,
      output: '',
      error: err.message || 'Failed to connect to backend',
      status: 'error',
    };
  }
}

/**
 * Get AI explanation for a specific step.
 */
export async function getExplanation(code, stepData, prevStep = null) {
  const endpoint = `${API_BASE}/explain`;
  
  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, step_data: stepData, prev_step: prevStep }),
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `Server error: ${res.status}`);
    }

  return await res.json();
}

/**
 * Save user session to MongoDB.
 */
export async function saveSession(sessionData) {
  const res = await fetch(`${API_BASE}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sessionData),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Server error: ${res.status}`);
  }

  return await res.json();
}

/**
 * Fetch a session by its shareable ID.
 */
export async function getSessionById(sessionId) {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`);

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Server error: ${res.status}`);
  }

  return await res.json();
}

// ── Mock fallback ────────────────────────────────────
function mockExecute(code, language) {
  const hasFib = /fibonacci/i.test(code);

  if (language === 'python') {
    return {
      success: true,
      executionTime: '0.003s',
      steps: [
        { text: '[INFO] Python 3.11 runtime loaded (mock)', type: 'info', line: 1 },
        { text: '[OK]   Module compiled successfully', type: 'success', line: 1 },
        ...(hasFib
          ? [
              { text: '  → a=0, b=1', type: 'log', line: 6 },
              { text: '  → a=1, b=1', type: 'log', line: 7 },
              { text: '  → a=1, b=2', type: 'log', line: 7 },
              { text: '  → a=2, b=3', type: 'log', line: 7 },
              { text: '  → a=3, b=5', type: 'log', line: 7 },
            ]
          : [{ text: '  → Executing...', type: 'log', line: 1 }]),
      ],
      output: hasFib ? 'Fibonacci(10) = 55' : null,
    };
  }

  return {
    success: true,
    executionTime: '0.047s',
    steps: [
      { text: `[INFO] ${language} mock execution`, type: 'info', line: 1 },
      { text: '[OK]   Done (mock)', type: 'success', line: 1 },
    ],
    output: null,
  };
}

// ── Public API ───────────────────────────────────────
/**
 * Execute code. Tries real backend first, falls back to mock.
 */
export async function executeCode(code, language) {
  try {
    return await callBackend(code, language);
  } catch (err) {
    // If backend is unreachable, fall back to mock
    if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
      console.warn('[CodeFlow] Backend unreachable, using mock response');
      await new Promise((r) => setTimeout(r, 600));
      return mockExecute(code, language);
    }
    throw err;
  }
}
