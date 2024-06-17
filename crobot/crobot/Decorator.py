import time
from functools import wraps
# from inspect import signature

import Logger as log

def logThis(func):
    """Decorator that print log before calling function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.debug('Calling function %s() with args: %s' % (func.__name__, str(locals())))
        # print(signature(func))
        return func(*args, **kwargs)
    return wrapper

def minipack3(func):
    """Decorator that print log before calling function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.debug('Calling minipack3 function %s() with args: %s' % (func.__name__, str(locals())))
        # print(signature(func))
        return func(*args, **kwargs)
    return wrapper

def timeThis(func):
    """Decorator that reports the execution time."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        log.debug('Execution time of function %s() is %d seconds'  % (func.__name__, end-start))
        return result
    return wrapper


def deprecated(str = ''):
    """  Decorator that mark a function as deprecated """

    def decorator_wrapper(func):
        @wraps(func)
        def function_wrapper(*args, **kwargs):
            log.debug('Warning: ' + str + '\nAPI name: ' + func.__name__)
            return func(*args, **kwargs)
        return function_wrapper
    return decorator_wrapper
