import inspect
import time


def func_name(func):
    if hasattr(func, '__self__'):
        return f"{func.__self__.__class__.__name__}.{func.__name__}"
    else:
        return func.__name__


def timed(func):
    if inspect.isgeneratorfunction(func):
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            result = yield from func(*args, **kwargs)
            print(f"{func_name(func)}() runtime (+ generator value consumption): {time.monotonic() - start:.3f}s")
            return result
        return wrapper
    else:
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            result = func(*args, **kwargs)
            print(f"{func_name(func)}() runtime: {time.monotonic() - start:.3f}s")
            return result
        return wrapper
