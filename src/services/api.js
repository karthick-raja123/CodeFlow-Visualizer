const REQUEST_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT ?? 10_000);
const SESSIONS_ENABLED = import.meta.env.VITE_ENABLE_SESSIONS === 'true';

const API_HOST = resolveApiHost();
const API_PREFIX = resolveApiPrefix();

function resolveApiHost() {
	const envValue = import.meta.env.VITE_API_URL?.trim();
	if (envValue) {
		return stripTrailingSlash(envValue);
	}
	if (typeof window !== 'undefined') {
		const { hostname, origin } = window.location;
		if (hostname === 'localhost' || hostname.startsWith('127.')) {
			return 'http://localhost:8000';
		}
		return stripTrailingSlash(origin);
	}
	return 'http://localhost:8000';
}

function resolveApiPrefix() {
	const envValue = import.meta.env.VITE_API_PREFIX?.trim();
	if (envValue) {
		return normalizePrefix(envValue);
	}
	if (typeof window !== 'undefined') {
		return window.location.hostname.includes('vercel.app') ? '/api' : '';
	}
	return '';
}

function stripTrailingSlash(value = '') {
	return value.replace(/\/+$/, '');
}

function normalizePrefix(value = '') {
	if (!value || value === '/') return '';
	return `/${value.replace(/^\/+/, '').replace(/\/+$/, '')}`;
}

function buildUrl(path) {
	const normalizedPath = path.startsWith('/') ? path : `/${path}`;
	return `${API_HOST}${API_PREFIX}${normalizedPath}`;
}

function logError(scope, error, extra = {}) {
	if (typeof console !== 'undefined') {
		console.error(`[CodeFlow API] ${scope}`, {
			message: error.message,
			status: error.status,
			url: error.url,
			...extra,
		});
	}
}

function createError(message, meta = {}) {
	const err = new Error(message);
	Object.assign(err, meta);
	return err;
}

function isNetworkFailure(error) {
	if (error?.isNetworkError) return true;
	if (!error?.message) return false;
	return /Failed to fetch|NetworkError/i.test(error.message);
}

async function parseResponse(res) {
	const contentType = res.headers.get('content-type') || '';
	if (contentType.includes('application/json')) {
		return res.json().catch(() => ({}));
	}
	const text = await res.text();
	if (!text) return {};
	try {
		return JSON.parse(text);
	} catch {
		return text;
	}
}

async function request(path, options = {}) {
	const { method = 'GET', body, timeout = REQUEST_TIMEOUT } = options;
	const url = buildUrl(path);
	const controller = new AbortController();
	const timer = setTimeout(() => controller.abort(), timeout);

	const headers = { ...(options.headers || {}) };
	const init = { method, signal: controller.signal };

	if (body !== undefined) {
		init.body = typeof body === 'string' ? body : JSON.stringify(body);
		if (!headers['Content-Type']) {
			headers['Content-Type'] = 'application/json';
		}
	}

	if (Object.keys(headers).length > 0) {
		init.headers = headers;
	}

	try {
		const res = await fetch(url, init);
		const data = await parseResponse(res);
		if (!res.ok) {
			const message = typeof data === 'string' && data
				? data
				: data?.error || `Server error (${res.status})`;
			throw createError(message, { status: res.status, url });
		}
		return data;
	} catch (error) {
		const isAbort = error.name === 'AbortError';
		const wrapped = createError(
			isAbort ? `Request timed out after ${timeout / 1000}s` : error.message || 'Network error',
			{
				cause: error,
				url,
				isNetworkError: isAbort || isNetworkFailure(error),
			}
		);
		logError(`request ${path}`, wrapped);
		throw wrapped;
	} finally {
		clearTimeout(timer);
	}
}

const postJson = (path, body, options) => request(path, { ...options, method: 'POST', body });
const postExecute = (code, input = '') => postJson('/execute', { code, input_data: input });
const postTrace = (code, input = '') => postJson('/trace', { code, input_data: input });

export async function runCode(code, input = '') {
	try {
		const data = await postExecute(code, input);
		return {
			output: data.output || '',
			error: data.error || '',
			status: data.error ? 'error' : 'success',
		};
	} catch (err) {
		return {
			output: '',
			error: err.message || 'Connection failed',
			status: 'error',
		};
	}
}

export async function traceCode(code, input = '') {
	try {
		const data = await postTrace(code, input);
		return {
			trace: data.steps || [],
			steps: data.steps || [],
			stdout: data.stdout || '',
			stderr: data.stderr || '',
			status: data.stderr ? 'error' : 'success',
		};
	} catch (err) {
		return {
			trace: [],
			steps: [],
			stdout: '',
			stderr: err.message || 'Connection failed',
			status: 'error',
		};
	}
}

export async function getExplanation(code, stepData, prevStep = null) {
	try {
		return await postJson('/explain', { code, step_data: stepData, prev_step: prevStep });
	} catch (err) {
		logError('getExplanation', err, { step: stepData?.line });
		throw err;
	}
}

export async function saveSession(sessionData) {
	if (!SESSIONS_ENABLED) {
		throw new Error('Session storage is disabled. Enable VITE_ENABLE_SESSIONS when the backend is ready.');
	}
	try {
		return await postJson('/sessions', sessionData);
	} catch (err) {
		if (err.status === 404) {
			throw new Error('Session API endpoint is missing on the backend.');
		}
		throw err;
	}
}

export async function getSessionById(sessionId) {
	if (!SESSIONS_ENABLED) {
		throw new Error('Session storage is disabled.');
	}
	try {
		return await request(`/sessions/${sessionId}`);
	} catch (err) {
		if (err.status === 404) {
			throw new Error('Session not found or API endpoint missing.');
		}
		throw err;
	}
}

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

function formatTraceSteps(traceSteps) {
	return traceSteps.map((step, idx) => {
		const vars = Object.entries(step.vars || {})
			.map(([key, value]) => `${key}=${value}`)
			.join(', ');
		return {
			text: vars ? `L${step.line}: ${vars}` : `L${step.line}: (no locals)`,
			type: idx === 0 ? 'info' : 'log',
			line: step.line,
		};
	});
}

async function callBackend(code, language) {
	const tracePayload = await postTrace(code);
	return {
		success: !tracePayload.stderr,
		executionTime: tracePayload.executionTime || 'trace-mode',
		steps: formatTraceSteps(tracePayload.steps || []),
		trace: tracePayload.steps || [],
		output: tracePayload.stdout || '',
		stdout: tracePayload.stdout || '',
		stderr: tracePayload.stderr || '',
		language,
	};
}

export async function executeCode(code, language = 'python') {
	try {
		return await callBackend(code, language);
	} catch (err) {
		if (isNetworkFailure(err) || err.status === 404) {
			console.warn('[CodeFlow] Backend unreachable, using mock response');
			await new Promise((resolve) => setTimeout(resolve, 600));
			return mockExecute(code, language);
		}
		throw err;
	}
}
