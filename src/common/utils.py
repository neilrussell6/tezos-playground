"""Common Utils"""


def add(a, b):
    """Return result of adding the provided 2 values."""
    return a + b


def head(xs):
    """Return head (first item) in provider Iterable."""
    try:
        return xs[0]
    except IndexError:
        return None
