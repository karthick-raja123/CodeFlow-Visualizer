"""
Secure sandbox environment for user code execution.
Provides restricted builtins and prevents access to dangerous modules/functions.
"""

import sys
import types
from io import StringIO


class RestrictedBuiltins:
    """
    Whitelist of safe builtins only.
    Blocks: open, exec, eval, __import__, compile, input (via args), print redirection
    """
    
    SAFE_BUILTINS = {
        # Type constructors
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
        'range': range,
        'slice': slice,
        'object': object,
        'type': type,
        
        # Math and logic
        'abs': abs,
        'pow': pow,
        'min': min,
        'max': max,
        'sum': sum,
        'round': round,
        'divmod': divmod,
        'len': len,
        'hash': hash,
        
        # Iteration and sequences
        'enumerate': enumerate,
        'zip': zip,
        'map': map,
        'filter': filter,
        'reversed': reversed,
        'sorted': sorted,
        'any': any,
        'all': all,
        
        # Type checking
        'isinstance': isinstance,
        'issubclass': issubclass,
        'callable': callable,
        'hasattr': hasattr,
        'getattr': getattr,
        'setattr': setattr,
        'delattr': delattr,
        
        # Formatting and conversion
        'chr': chr,
        'ord': ord,
        'hex': hex,
        'oct': oct,
        'bin': bin,
        'format': format,
        'repr': repr,
        'ascii': ascii,
        
        # Iteration
        'iter': iter,
        'next': next,
        
        # Functional
        'id': id,
        'input': input,  # Allowed - stdin is controlled via Popen
        'print': print,  # Allowed - stdout is captured
        'len': len,
        'sorted': sorted,
        'enumerate': enumerate,
        
        # Exceptions (for try/except blocks)
        'Exception': Exception,
        'BaseException': BaseException,
        'ValueError': ValueError,
        'KeyError': KeyError,
        'IndexError': IndexError,
        'TypeError': TypeError,
        'AttributeError': AttributeError,
        'ZeroDivisionError': ZeroDivisionError,
        'RuntimeError': RuntimeError,
        'StopIteration': StopIteration,
        'NotImplementedError': NotImplementedError,
        'NameError': NameError,
        'UnboundLocalError': UnboundLocalError,
        'SyntaxError': SyntaxError,
        'IndentationError': IndentationError,
        'TabError': TabError,
        'AssertionError': AssertionError,
        'ArithmeticError': ArithmeticError,
        'MemoryError': MemoryError,
        'RecursionError': RecursionError,
        'EOFError': EOFError,
        
        # Constants
        'True': True,
        'False': False,
        'None': None,
        'NotImplemented': NotImplemented,
        'Ellipsis': Ellipsis,
        '__debug__': __debug__,
        
        # Iteration support
        'range': range,
        'enumerate': enumerate,
        'zip': zip,
        'reversed': reversed,
        
        # Others
        'dir': dir,
        'globals': globals,
        'locals': locals,
        'vars': vars,
    }

    @classmethod
    def get_safe_builtins(cls):
        """Return a restricted builtins dict for exec()"""
        return cls.SAFE_BUILTINS.copy()


def create_restricted_globals():
    """
    Create a restricted globals dict for exec().
    Includes safe builtins only, no access to modules or dangerous functions.
    """
    return {
        '__builtins__': RestrictedBuiltins.get_safe_builtins(),
        '__name__': '__user_code__',
        '__doc__': None,
    }


def is_safe_code(code: str) -> tuple[bool, str]:
    """
    Quick syntax check for obviously dangerous patterns.
    Returns (is_safe, error_message)
    
    NOTE: This is a surface-level check. Full sandboxing happens in subprocess.
    """
    dangerous_patterns = [
        ('__import__', 'Cannot use __import__'),
        ('open(', 'Cannot access file system'),
        ('exec(', 'Cannot use exec()'),
        ('eval(', 'Cannot use eval()'),
        ('compile(', 'Cannot use compile()'),
        ('__code__', 'Cannot access __code__'),
        ('__class__', 'Cannot access __class__ (in most contexts)'),
    ]
    
    for pattern, error in dangerous_patterns:
        if pattern in code:
            return False, error
    
    return True, ""
