"""
Step-by-step Python execution tracer using sys.settrace.

Captures:
  - Line execution order
  - Variable values at each step (locals snapshot)
  - Function call/return events
  - stdout output per step
"""

import sys
import io
import copy

# Maximum number of trace steps to avoid runaway execution
MAX_STEPS = 500
# Maximum variable value string length
MAX_VAR_STR_LEN = 100


def _safe_repr(value):
    """Safely convert a value to a string representation, truncating if too long."""
    try:
        r = repr(value)
        if len(r) > MAX_VAR_STR_LEN:
            return r[:MAX_VAR_STR_LEN] + "..."
        return r
    except Exception:
        return "<unrepresentable>"


def _safe_type(value):
    """Get a clean type name for a value."""
    try:
        t = type(value).__name__
        return t
    except Exception:
        return "unknown"


def _snapshot_variables(local_vars):
    """
    Create a JSON-safe snapshot of local variables.
    Filters out internal/dunder names and non-serializable objects.
    """
    snapshot = {}
    for name, value in local_vars.items():
        # Skip dunder names and internal vars
        if name.startswith("_") and name != "_":
            continue
        # Skip modules, functions, classes, types
        if callable(value) and not isinstance(value, (int, float, str, bool)):
            continue
        if isinstance(value, type):
            continue

        snapshot[name] = {
            "value": _safe_repr(value),
            "type": _safe_type(value),
        }

    return snapshot


class StepTracer:
    """
    Trace function for sys.settrace that records execution steps.

    Each step records:
      - step number (1-indexed)
      - line number in user code
      - event type (line, call, return, exception)
      - function name (if applicable)
      - variable snapshot (locals at that point)
      - stdout output captured since last step
    """

    def __init__(self, stdout_capture):
        self.steps = []
        self.stdout = stdout_capture
        self._last_stdout_pos = 0
        self._step_count = 0
        self._exceeded = False

    def _get_new_output(self):
        """Get stdout written since last check."""
        current = self.stdout.getvalue()
        new_output = current[self._last_stdout_pos:]
        self._last_stdout_pos = len(current)
        return new_output.strip()

    def trace_calls(self, frame, event, arg):
        """Top-level trace function. Only trace user code (<user_code>)."""
        if frame.f_code.co_filename != "<user_code>":
            return None
        return self.trace_lines

    def trace_lines(self, frame, event, arg):
        """Line-level trace function. Records each step."""
        if self._exceeded:
            return None

        if frame.f_code.co_filename != "<user_code>":
            return self.trace_lines

        self._step_count += 1

        if self._step_count > MAX_STEPS:
            self._exceeded = True
            self.steps.append({
                "step": self._step_count,
                "line": frame.f_lineno,
                "event": "limit",
                "function": frame.f_code.co_name,
                "variables": {},
                "output": f"[Trace limit reached: {MAX_STEPS} steps max]",
            })
            return None

        # Snapshot variables
        variables = _snapshot_variables(frame.f_locals)

        # Capture any new stdout
        new_output = self._get_new_output()

        step_data = {
            "step": self._step_count,
            "line": frame.f_lineno,
            "event": event,  # 'call', 'line', 'return', 'exception'
            "function": frame.f_code.co_name if frame.f_code.co_name != "<module>" else "<module>",
            "variables": variables,
            "output": new_output if new_output else "",
        }

        # For return events, capture the return value
        if event == "return":
            step_data["return_value"] = _safe_repr(arg)

        # For exception events, capture the exception info
        if event == "exception" and arg:
            exc_type, exc_value, _ = arg
            step_data["exception"] = f"{exc_type.__name__}: {exc_value}"

        self.steps.append(step_data)
        return self.trace_lines

    def get_steps(self):
        """Return all recorded steps."""
        return self.steps

    def was_exceeded(self):
        """Return whether the step limit was hit."""
        return self._exceeded
