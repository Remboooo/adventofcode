import inspect
import math
import time


def func_name(func):
    if hasattr(func, '__self__'):
        return f"{func.__self__.__class__.__name__}.{func.__name__}"
    else:
        return func.__name__


def format_timedelta(delta):
    if delta >= 1:
        return f"{delta:.3f}s"
    elif delta >= .001:
        return f"{delta*1e3:.3f}ms"
    else:
        return f"{delta * 1e6:.3f}µs"


def timed(func):
    if inspect.isgeneratorfunction(func):
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            result = yield from func(*args, **kwargs)
            print(f"{func_name(func)}() runtime (+ generator value consumption): {format_timedelta(time.monotonic() - start)}")
            return result
        return wrapper
    else:
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            result = func(*args, **kwargs)
            print(f"{func_name(func)}() runtime: {format_timedelta(time.monotonic() - start)}")
            return result
        return wrapper


def _transform_arg(arg):
    if isinstance(arg, set):
        return frozenset(arg)
    elif isinstance(arg, dict):
        return tuple(sorted(arg.items()))
    return arg


def memoized(*key_args):
    """
    Memo-ize the given function using the given argument list as key.
    The given argument list should contain argument numbers (for args) and/or names (for kwargs).
    Only hashable types can be included in the argument list.
    Generator functions cannot be memoized.
    :param key_args: The arguments of the function to memoize
    :return: Memoized version of the function
    """
    def wrapper_wrapper(func):
        if inspect.isgeneratorfunction(func):
            raise ValueError("Cannot memoize generator function")
        else:
            cache = {}

            def memoizer(*args, **kwargs):
                key = tuple(args[a] if isinstance(a, int) else kwargs[a] for a in key_args)

                if key not in cache:
                    cache[key] = func(*args, **kwargs)
                return cache[key]

            return memoizer

    return wrapper_wrapper


def egcd(a, b):
    """
    Extended Euclidean algorithm to solve for x, a, and gcd(a, b):
    x * a + y * b = gcd(a, b)
    :return: gcd(a, b), x, y
    """
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = egcd(b % a, a)
        return gcd, y - (b // a) * x, x


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)
