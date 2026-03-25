#!/usr/bin/env python3
"""
SANDBOX WRAPPER - Executes user code with strict sandbox restrictions
This wrapper is created dynamically and executed by executor.py
"""

import sys
import json

# This is populated by executor.py
USER_CODE = """
# User code will be injected here
"""

# Restricted builtins - BLOCKING all dangerous functions
SAFE_BUILTINS = {
    # I/O operations
    'print': print,
    'input': input,
    
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
    
    # Collections helpers
    'memoryview': memoryview,
    'property': property,
    'classmethod': classmethod,
    'staticmethod': staticmethod,
    'super': super,
    
    # Metadata
    '__name__': '__main__',
    '__doc__': None,
}

# These are EXPLICITLY BLOCKED and must not be accessible
BLOCKED_NAMES = {
    'eval',           # CODE INJECTION
    'exec',           # CODE INJECTION
    'compile',        # CODE INJECTION
    '__import__',     # MODULE LOADING
    'open',           # FILE ACCESS
    'exit',           # PROCESS CONTROL
    'quit',           # PROCESS CONTROL
    'vars',           # INTROSPECTION/ESCAPE
    'locals',         # INTROSPECTION/ESCAPE
    'globals',        # INTROSPECTION/ESCAPE
    'breakpoint',     # DEBUGGING
    '__build_class__',# INTERNAL
    '__loader__',     # INTERNAL
    '__spec__',       # INTERNAL
    '__cached__',     # INTERNAL
}

# Remove any blocked items that might have snuck in
for blocked in BLOCKED_NAMES:
    SAFE_BUILTINS.pop(blocked, None)

def execute_safe_code():
    """Execute user code with restricted builtins"""
    try:
        # Create a restricted namespace
        restricted_globals = {
            '__builtins__': SAFE_BUILTINS,
            '__name__': '__main__',
            '__doc__': None,
        }
        
        # Execute user code with restricted builtins
        exec(USER_CODE, restricted_globals)
        
    except Exception as e:
        # Write error to stderr
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    execute_safe_code()
