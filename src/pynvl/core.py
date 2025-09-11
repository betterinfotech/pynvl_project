from typing import Any

__all__ = ["nvl", "decode", "sign", "noneif", "nvl2"]


def nvl(expr, default):
    """Return expr if not None, else default."""
    if expr is None:
        return default
    else:
        return expr


_MISSING = object()  # Sentinel to distinguish "not provided" from None


def decode(expr: Any, *pairs: Any, default: Any = _MISSING) -> Any:
    """
    Conditional mapping with optional trailing implicit default.
    Special case: within decode, None equals None.
    """
    implicit_default = _MISSING
    n = len(pairs)

    if n == 0:
        return None if default is _MISSING else default

    # If odd count, last is implicit default; strip it from pairs
    if n % 2 == 1:
        implicit_default = pairs[-1]
        pairs = pairs[:-1]

    # Iterate search/result pairs
    it = iter(pairs)
    for search, result in zip(it, it):
        # For decode, None equals None
        if expr == search or (expr is None and search is None):
            return result

    # Choose default: explicit overrides implicit; else None
    if default is not _MISSING:
        return default
    if implicit_default is not _MISSING:
        return implicit_default
    return None


def sign(n: float | int) -> int:
    if n < 0:
        return -1
    elif n > 0:
        return 1
    else:
        return 0


def _nullif(a: Any, b: Any) -> Any:
    """Return None if a == b, else a."""
    return None if a == b else a


def noneif(a: Any, b: Any) -> Any:
    return _nullif(a, b)


def nvl2(expr: Any, value_if_not_null: Any, value_if_null: Any) -> Any:
    return value_if_not_null if expr is not None else value_if_null
