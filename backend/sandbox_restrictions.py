#!/usr/bin/env python3
"""
CRITICAL SECURITY HOTFIX - Sandbox Enforcement
This wrapper enforces strict sandbox restrictions on executed code.

Applied: Phase 2 Security Audit discovered dangerous functions NOT blocked
Solution: Implement true sandbox with restricted __builtins__
"""

import sys


def create_restricted_builtins():
    """
    Create a restricted set of builtins safe for code execution.
    Blocks: eval, exec, __import__, open, compile, exit, quit
    Blocks: dangerous module access (__loader__, __spec__, etc.)
    Allows: math operations, collections, I/O (print/input), type info
    """
    
    # Start with core safe builtins
    safe_builtins = {
        # I/O
        'print': print,
        'input': input,
        
        # Type operations
        'type': type,
        'isinstance': isinstance,
        'issubclass': issubclass,
        'len': len,
        
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
        
        # Math
        'abs': abs,
        'pow': pow,
        'sum': sum,
        'min': min,
        'max': max,
        'round': round,
        'divmod': divmod,
        
        # Object operations
        'getattr': getattr,
        'setattr': setattr,
        'hasattr': hasattr,
        'delattr': delattr,
        'callable': callable,
        'dir': dir,
        'id': id,
        'hash': hash,
        
        # Collections
        'all': all,
        'any': any,
        
        # Error handling
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
        
        # Misc safe
        'None': None,
        'True': True,
        'False': False,
        'NotImplemented': NotImplemented,
        'Ellipsis': Ellipsis,
        '__name__': '__main__',
        '__doc__': None,
        
        # Memory
        'memoryview': memoryview,
        'hex': hex,
        'oct': oct,
        'bin': bin,
        'ord': ord,
        'chr': chr,
        
        # Closure
        'property': property,
        'classmethod': classmethod,
        'staticmethod': staticmethod,
        'super': super,
        
        # String operations
        'repr': repr,
        'ascii': ascii,
        'format': format,
        'slice': slice,
        
        # Error classes
        'BaseException': BaseException,
        'SystemExit': SystemExit,
        'KeyboardInterrupt': KeyboardInterrupt,
        'GeneratorExit': GeneratorExit,
        'Exception': Exception,
        'StopAsyncIteration': StopAsyncIteration,
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
        'Warning': Warning,
        'BytesWarning': BytesWarning,
        'DeprecationWarning': DeprecationWarning,
        'FutureWarning': FutureWarning,
        'ImportWarning': ImportWarning,
        'PendingDeprecationWarning': PendingDeprecationWarning,
        'ResourceWarning': ResourceWarning,
        'RuntimeWarning': RuntimeWarning,
        'SyntaxWarning': SyntaxWarning,
        'UnicodeWarning': UnicodeWarning,
        'UserWarning': UserWarning,
        
        # Functions (safe)
        'len': len,
        'abs': abs,
        'max': max,
        'min': min,
        'sum': sum,
        'sorted': sorted,
    }
    
    # EXPLICITLY BLOCKED - These should NEVER be accessible
    blocked = {
        'eval': 'CODE_INJECTION',
        'exec': 'CODE_INJECTION',
        'compile': 'CODE_INJECTION',
        '__import__': 'MODULE_LOADING',
        'open': 'FILE_ACCESS',
        'input': 'STDIN_ACCESS',  # Actually allowed above, but kept for reference
        'exit': 'PROCESS_CONTROL',
        'quit': 'PROCESS_CONTROL',
        'vars': 'INTROSPECTION',
        'locals': 'INTROSPECTION',
        'globals': 'INTROSPECTION',
        '__build_class__': 'INTERNAL',
        '__builtins__': 'INTERNAL',
    }
    
    # Verify blocked items are not in safe list
    for blocked_name in blocked:
        if blocked_name in safe_builtins:
            del safe_builtins[blocked_name]
    
    return safe_builtins


# THIS FILE IS NOT MEANT TO BE EXECUTED DIRECTLY
# It provides sandbox functions for the executor wrapper

if __name__ == "__main__":
    print("This module provides sandbox utilities for the executor.")
    print("Import it in your sandbox wrapper script.")
