import functools
import logging


def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logging.debug(f"call :: {func.__name__}({signature})")
        value = func(*args, **kwargs)
        logging.debug(f"call :: {func.__name__!r} :: return :: {value!r}")
        return value
    return wrapper_debug
