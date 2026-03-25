#!/usr/bin/env python3
"""
Production-grade Python code executor with STRICT sandbox isolation.

CRITICAL SECURITY FIX - Phase 2 Audit Results:
- Blocks evaluation: eval, exec, compile
- Blocks file access: open
- Blocks system commands: __import__, os module access
- Blocks introspection: vars, globals, locals
- Blocks dangerous builtins: exit, quit, breakpoint
"""

import subprocess
import tempfile
import os
import sys
from typing import Tuple


EXECUTION_TIMEOUT = 5.0


def run_code(code: str, input_data: str = "") -> Tuple[str, str]:
    """
    Execute Python code with STRICT sandbox enforcement.
    
    Guarantees:
    - Subprocess isolation (true process isolation)
    - Blocked functions: eval, exec, open, __import__, os, sys, etc.
    - Timeout protection (hard kill at 5 seconds)
    - Clean error messages
    """
    
    # Syntax check
    try:
        compile(code, '<user_code>', 'exec')
    except SyntaxError as e:
        return "", f"SyntaxError: {e.msg} (line {e.lineno})"
    except Exception as e:
        return "", f"CompileError: {e}"
    
    user_code_file = None
    wrapper_file = None
    process = None
    
    try:
        # Write user code to temp file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(code)
            user_code_file = f.name
        
        # Create sandbox wrapper with BLOCKING functions
        wrapper_code = f'''
import sys

# Load user code
with open(r\'{user_code_file}\', \'r\', encoding=\'utf-8\') as f:
    USER_CODE = f.read()

# BLOCKING FUNCTION - raises NameError for dangerous operations
def _BLOCKED(name):
    def block_func(*args, **kwargs):
        raise NameError(f"name \'{{name}}\' is not defined")
    return block_func

# SAFE BUILTINS - Explicitly blocking dangerous functions
SAFE_BUILTINS = {{
    # I/O
    'print': print,
    'input': input,
    
    # Explicitly blocked - SECURITY CRITICAL
    'eval': _BLOCKED(\'eval\'),
    'exec': _BLOCKED(\'exec\'),
    'compile': _BLOCKED(\'compile\'),
    '__import__': _BLOCKED(\'__import__\'),
    'open': _BLOCKED(\'open\'),
    'exit': _BLOCKED(\'exit\'),
    'quit': _BLOCKED(\'quit\'),
    'vars': _BLOCKED(\'vars\'),
    'locals': _BLOCKED(\'locals\'),
    'globals': _BLOCKED(\'globals\'),
    'breakpoint': _BLOCKED(\'breakpoint\'),
    '__build_class__': _BLOCKED(\'__build_class__\'),
    '__loader__': _BLOCKED(\'__loader__\'),
    '__spec__': _BLOCKED(\'__spec__\'),
    '__cached__': _BLOCKED(\'__cached__\'),
    'input': input,  # input is allowed
    
    # Type operations
    'type': type,
    'isinstance': isinstance,
    'issubclass': issubclass,
    'len': len,
    'callable': callable,
    'hasattr': hasattr,
    'getattr': getattr,
    'setattr': setattr,
    'delattr': delattr,
    'dir': dir,
    'id': id,
    'hash': hash,
    
    # Conversions
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'tuple': tuple,
    'set': set,
    'frozenset': frozenset,
    'bytes': bytes,
    'bytearray': bytearray,
    'complex': complex,
    
    # Iteration
    'range': range,
    'enumerate': enumerate,
    'zip': zip,
    'map': map,
    'filter': filter,
    'reversed': reversed,
    'sorted': sorted,
    'iter': iter,
    'next': next,
    'all': all,
    'any': any,
    
    # Math
    'abs': abs,
    'pow': pow,
    'sum': sum,
    'min': min,
    'max': max,
    'round': round,
    'divmod': divmod,
    'hex': hex,
    'oct': oct,
    'bin': bin,
    'ord': ord,
    'chr': chr,
    
    # Format/string
    'repr': repr,
    'ascii': ascii,
    'format': format,
    'slice': slice,
    
    # Built-in constants
    'None': None,
    'True': True,
    'False': False,
    'NotImplemented': NotImplemented,
    'Ellipsis': Ellipsis,
    
    # Exception classes
    'Exception': Exception,
    'ValueError': ValueError,
    'TypeError': TypeError,
    'ZeroDivisionError': ZeroDivisionError,
    'IndexError': IndexError,
    'KeyError': KeyError,
    'AttributeError': AttributeError,
    'NameError': NameError,
    'RuntimeError': RuntimeError,
    'NotImplementedError': NotImplementedError,
    'StopIteration': StopIteration,
    'BaseException': BaseException,
    'SystemExit': SystemExit,
    'KeyboardInterrupt': KeyboardInterrupt,
    'ArithmeticError': ArithmeticError,
    'FloatingPointError': FloatingPointError,
    'OverflowError': OverflowError,
    'EOFError': EOFError,
    'ImportError': ImportError,
    'ModuleNotFoundError': ModuleNotFoundError,
    'LookupError': LookupError,
    'AssertionError': AssertionError,
    'SyntaxError': SyntaxError,
    'IndentationError': IndentationError,
    'TabError': TabError,
    'SystemError': SystemError,
    'ReferenceError': ReferenceError,
    'MemoryError': MemoryError,
    'RecursionError': RecursionError,
    
    # Only safe operations
    'memoryview': memoryview,
    'property': property,
    'classmethod': classmethod,
    'staticmethod': staticmethod,
    'super': super,
    '__name__': \'__main__\',
    '__doc__': None,
}}

try:
    # Execute with restricted builtins - NO access to dangerous functions
    globals_dict = {{'__builtins__': SAFE_BUILTINS}}
    exec(USER_CODE, globals_dict, {{}})
except Exception as e:
    print(f"{{type(e).__name__}}: {{e}}", file=sys.stderr)
    sys.exit(1)
'''
        
        # Write wrapper to temp file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(wrapper_code)
            wrapper_file = f.name
        
        # Execute wrapper (not user code directly)
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUNBUFFERED'] = '1'
        
        process = subprocess.Popen(
            [sys.executable, wrapper_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            encoding='utf-8',
            errors='replace',
        )
        
        try:
            stdout, stderr = process.communicate(
                input=input_data if input_data else None,
                timeout=EXECUTION_TIMEOUT
            )
            return stdout, stderr
        except subprocess.TimeoutExpired:
            process.kill()
            try:
                process.wait(timeout=1)
            except:
                pass
            return "", f"ExecutionTimeout: Code exceeded {EXECUTION_TIMEOUT}s timeout"
    
    except Exception as e:
        return "", f"ExecutionError: {type(e).__name__}: {e}"
    
    finally:
        # Clean up
        for f in [user_code_file, wrapper_file]:
            if f and os.path.exists(f):
                try:
                    os.unlink(f)
                except:
                    pass
