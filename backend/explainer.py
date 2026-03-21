"""
AI-powered code explanation engine.
Generates contextual explanations for each execution step.
"""

import ast
import re


def explain_step(code: str, step_data: dict, prev_step: dict | None = None) -> dict:
    line_num = step_data.get("line", 0)
    event = step_data.get("event", "line")
    variables = step_data.get("vars", {})
    lines = code.split("\n")
    source = lines[line_num - 1].strip() if 0 < line_num <= len(lines) else ""

    # Detect changes
    prev_vars = prev_step.get("vars", {}) if prev_step else {}
    changes = {}
    for name, val in variables.items():
        prev = prev_vars.get(name)
        if prev is None:
            changes[name] = {"from": "undefined", "to": val, "status": "new"}
        elif prev != val:
            changes[name] = {"from": prev, "to": val, "status": "changed"}

    explanation = _explain_line(source, line_num, variables, changes)
    concept = _concept(source)
    suggestion = _suggest(source, variables)

    return {
        "explanation": explanation,
        "changes": changes,
        "concept": concept,
        "suggestion": suggestion,
        "source": source,
        "line": line_num,
    }


def _explain_line(source, line, variables, changes):
    if source.startswith("for "):
        return f"📍 Entering the **for loop**. Python evaluates the iterable and assigns the loop variable for each iteration."
    if source.startswith("while "):
        return f"📍 Evaluating the **while condition** to decide if the loop body should execute again."
    if source.startswith("if "):
        return f"📍 Evaluating the **if condition** to decide which branch to take."
    if source.startswith("elif "):
        return f"📍 Previous condition was False, now checking this **elif** condition."
    if source.startswith("else:"):
        return f"📍 All previous conditions were False, entering the **else** branch."
    if source.startswith("def "):
        name = source.split("(")[0].replace("def ", "")
        return f"📍 Defining function **{name}()**. This creates a function object — the body won't execute yet."
    if source.startswith("return"):
        val = source.replace("return", "").strip()
        return f"📍 Returning **{val}** from this function back to the caller."
    if "print(" in source:
        return f"📍 Calling **print()** to display output to the console."
    if "input(" in source:
        return f"📍 Calling **input()** to read user input from stdin."

    # Assignments
    if "=" in source and "==" not in source and not source.startswith("="):
        target = source.split("=")[0].strip()
        if changes:
            parts = []
            for name, ch in changes.items():
                if ch["status"] == "new":
                    parts.append(f"**{name}** is created with value `{ch['to']}`")
                else:
                    parts.append(f"**{name}** changes from `{ch['from']}` to `{ch['to']}`")
            return f"📍 Assigning value — " + ", ".join(parts) + "."
        return f"📍 Assigning a value to **{target}**. Python evaluates the right side first, then stores it."

    return f"📍 Executing line {line}."


def _concept(source):
    if "for " in source:
        return "🎓 **Iteration** — Repeating a block of code for each item in a sequence."
    if "while " in source:
        return "🎓 **While Loop** — Repeats as long as a condition is True."
    if "if " in source or "elif " in source:
        return "🎓 **Conditional** — Making decisions based on True/False conditions."
    if "def " in source:
        return "🎓 **Function Definition** — Reusable block of code that can be called later."
    if "+=" in source or "-=" in source:
        return "🎓 **Augmented Assignment** — Shorthand for update-in-place operations."
    if "print(" in source:
        return "🎓 **Standard Output** — Displaying results to the user."
    if "=" in source and "==" not in source:
        return "🎓 **Variable Assignment** — Storing a value in memory with a name."
    return ""


def _suggest(source, variables):
    if "while True" in source:
        return "⚠️ **Caution**: Infinite loop — ensure there's a `break` statement."
    if "== None" in source:
        return "💡 **Tip**: Use `is None` instead of `== None` for identity checks."
    if "except:" in source:
        return "💡 **Tip**: Avoid bare `except:` — specify the exception type."
    if "print(" in source:
        return "💡 **Tip**: For production code, consider the `logging` module instead of print()."
    if "range(" in source:
        return "💡 **Tip**: `range()` creates a lazy sequence — memory efficient for large ranges."
    return ""
