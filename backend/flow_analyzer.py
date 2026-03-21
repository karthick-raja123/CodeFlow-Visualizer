"""
AST-based control flow analyzer for Python code.

Parses Python source into an AST, then extracts a simplified flow graph
with nodes (Start, Assignment, Loop, Condition, Return, FunctionCall, Output, End)
and edges between them. Each node maps to source line numbers so the frontend
can highlight the active node based on the current trace step.
"""

import ast

# ── Node types ────────────────────────────────────────
NODE_TYPES = {
    "start": {"label": "Start", "color": "#22c55e"},
    "end": {"label": "End", "color": "#ef4444"},
    "function_def": {"label": "Function", "color": "#6366f1"},
    "assignment": {"label": "Assignment", "color": "#818cf8"},
    "loop": {"label": "Loop", "color": "#f59e0b"},
    "condition": {"label": "Condition", "color": "#3b82f6"},
    "return": {"label": "Return", "color": "#ec4899"},
    "call": {"label": "Call", "color": "#8b5cf6"},
    "output": {"label": "Output", "color": "#14b8a6"},
    "expression": {"label": "Expression", "color": "#64748b"},
}


def analyze_flow(code: str) -> dict:
    """
    Analyze Python code and return a flow graph structure.

    Returns:
        {
            "nodes": [{"id", "type", "label", "line", "color"}],
            "edges": [{"source", "target", "label"}]
        }
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            "nodes": [
                _node("start", "start", "Start", 0),
                _node("error", "end", f"SyntaxError: {e.msg}", e.lineno or 0),
            ],
            "edges": [{"source": "start", "target": "error", "label": ""}],
        }

    nodes = []
    edges = []
    _id_counter = [0]

    def _next_id(prefix="node"):
        _id_counter[0] += 1
        return f"{prefix}_{_id_counter[0]}"

    def _node(node_id, node_type, label, line):
        info = NODE_TYPES.get(node_type, NODE_TYPES["expression"])
        return {
            "id": node_id,
            "type": node_type,
            "label": label,
            "line": line,
            "color": info["color"],
        }

    def process_body(stmts, prev_id):
        """Process a list of AST statements, chaining them from prev_id."""
        current = prev_id
        for stmt in stmts:
            current = process_stmt(stmt, current)
        return current

    def process_stmt(stmt, prev_id):
        """Process a single AST statement, returning the exit node id."""

        # ── Function definition ─────────────────────
        if isinstance(stmt, ast.FunctionDef):
            nid = _next_id("func")
            nodes.append(_node(nid, "function_def", f"def {stmt.name}()", stmt.lineno))
            edges.append({"source": prev_id, "target": nid, "label": ""})

            # Process function body
            body_start = _next_id("body")
            nodes.append(_node(body_start, "start", f"→ {stmt.name}()", stmt.lineno))
            edges.append({"source": nid, "target": body_start, "label": "body"})
            body_end = process_body(stmt.body, body_start)

            # Don't chain into function body for the main flow
            return nid

        # ── If / elif / else ────────────────────────
        if isinstance(stmt, ast.If):
            cond_id = _next_id("cond")
            cond_text = _expr_text(stmt.test)
            nodes.append(_node(cond_id, "condition", f"if {cond_text}", stmt.lineno))
            edges.append({"source": prev_id, "target": cond_id, "label": ""})

            # Merge point after if/else
            merge_id = _next_id("merge")
            nodes.append(_node(merge_id, "expression", "•", stmt.end_lineno or stmt.lineno))

            # True branch
            if stmt.body:
                true_end = process_body(stmt.body, cond_id)
                edges[-1]  # The edge to cond was already added
                # Add true label to the first edge from cond
                true_first = None
                for e in edges:
                    if e["source"] == cond_id and e["target"] != merge_id:
                        e["label"] = "True"
                        true_first = e["target"]
                        break
                if true_first is None:
                    # Body was empty, connect directly
                    edges.append({"source": cond_id, "target": merge_id, "label": "True"})
                else:
                    edges.append({"source": true_end, "target": merge_id, "label": ""})

            # False branch
            if stmt.orelse:
                false_end = process_body(stmt.orelse, cond_id)
                # Label the edge
                for e in reversed(edges):
                    if e["source"] == cond_id and not e.get("_marked"):
                        e["label"] = "False"
                        e["_marked"] = True
                        break
                edges.append({"source": false_end, "target": merge_id, "label": ""})
            else:
                edges.append({"source": cond_id, "target": merge_id, "label": "False"})

            return merge_id

        # ── For loop ────────────────────────────────
        if isinstance(stmt, ast.For):
            loop_id = _next_id("loop")
            iter_text = _expr_text(stmt.iter)
            target_text = _expr_text(stmt.target)
            nodes.append(_node(loop_id, "loop", f"for {target_text} in {iter_text}", stmt.lineno))
            edges.append({"source": prev_id, "target": loop_id, "label": ""})

            if stmt.body:
                body_end = process_body(stmt.body, loop_id)
                # Label the entry edge
                for e in edges:
                    if e["source"] == loop_id and e != edges[-1]:
                        e["label"] = "iterate"
                        break
                edges.append({"source": body_end, "target": loop_id, "label": "next"})

            exit_id = _next_id("loop_exit")
            nodes.append(_node(exit_id, "expression", "•", stmt.end_lineno or stmt.lineno))
            edges.append({"source": loop_id, "target": exit_id, "label": "done"})
            return exit_id

        # ── While loop ──────────────────────────────
        if isinstance(stmt, ast.While):
            loop_id = _next_id("loop")
            cond_text = _expr_text(stmt.test)
            nodes.append(_node(loop_id, "loop", f"while {cond_text}", stmt.lineno))
            edges.append({"source": prev_id, "target": loop_id, "label": ""})

            if stmt.body:
                body_end = process_body(stmt.body, loop_id)
                edges.append({"source": body_end, "target": loop_id, "label": "loop"})

            exit_id = _next_id("loop_exit")
            nodes.append(_node(exit_id, "expression", "•", stmt.end_lineno or stmt.lineno))
            edges.append({"source": loop_id, "target": exit_id, "label": "done"})
            return exit_id

        # ── Return ──────────────────────────────────
        if isinstance(stmt, ast.Return):
            ret_id = _next_id("ret")
            val = _expr_text(stmt.value) if stmt.value else ""
            nodes.append(_node(ret_id, "return", f"return {val}", stmt.lineno))
            edges.append({"source": prev_id, "target": ret_id, "label": ""})
            return ret_id

        # ── Assignment ──────────────────────────────
        if isinstance(stmt, ast.Assign):
            assign_id = _next_id("assign")
            targets = ", ".join(_expr_text(t) for t in stmt.targets)
            val = _expr_text(stmt.value)
            label = f"{targets} = {val}"
            if len(label) > 30:
                label = f"{targets} = ..."
            nodes.append(_node(assign_id, "assignment", label, stmt.lineno))
            edges.append({"source": prev_id, "target": assign_id, "label": ""})
            return assign_id

        # ── Augmented assignment (+=, etc) ──────────
        if isinstance(stmt, ast.AugAssign):
            assign_id = _next_id("assign")
            target = _expr_text(stmt.target)
            nodes.append(_node(assign_id, "assignment", f"{target} ⊕= ...", stmt.lineno))
            edges.append({"source": prev_id, "target": assign_id, "label": ""})
            return assign_id

        # ── Expression (print, function calls) ──────
        if isinstance(stmt, ast.Expr):
            if isinstance(stmt.value, ast.Call):
                call_id = _next_id("call")
                func_name = _expr_text(stmt.value.func)
                if func_name == "print":
                    nodes.append(_node(call_id, "output", f"print(...)", stmt.lineno))
                else:
                    nodes.append(_node(call_id, "call", f"{func_name}()", stmt.lineno))
                edges.append({"source": prev_id, "target": call_id, "label": ""})
                return call_id
            # Generic expression
            expr_id = _next_id("expr")
            nodes.append(_node(expr_id, "expression", "expr", stmt.lineno))
            edges.append({"source": prev_id, "target": expr_id, "label": ""})
            return expr_id

        # ── Fallback for other statements ───────────
        generic_id = _next_id("stmt")
        nodes.append(_node(generic_id, "expression", type(stmt).__name__, getattr(stmt, 'lineno', 0)))
        edges.append({"source": prev_id, "target": generic_id, "label": ""})
        return generic_id

    # ── Build the flow ────────────────────────────────
    start_id = "start"
    nodes.append(_node(start_id, "start", "Start", 0))

    last_id = process_body(tree.body, start_id)

    end_id = "end"
    nodes.append(_node(end_id, "end", "End", 0))
    edges.append({"source": last_id, "target": end_id, "label": ""})

    # Clean edges
    for e in edges:
        e.pop("_marked", None)

    return {"nodes": nodes, "edges": edges}


def _expr_text(node) -> str:
    """Get a short text representation of an AST expression node."""
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return "..."
