"""
pynvl: Oracle-inspired functions for Python.

Core exports:
    nvl, decode, sign, noneif, nvl2

Optional pandas exports (if pandas is installed):
    pd_sign, pd_nvl, pd_nvl2, pd_noneif, pd_decode
"""

from importlib.metadata import PackageNotFoundError, version as _version

# ---- Package metadata ----
try:
    __version__ = _version("pynvl-lib")
except PackageNotFoundError:
    # Running from source/tree without the distribution installed
    __version__ = "0.dev0"

__url__ = "https://betterinfotech.github.io/pynvl_project/"

# ---- Public API (core) ----
from .core import decode, noneif, nvl, nvl2, sign  # noqa: F401

__all__ = ("nvl", "decode", "sign", "noneif", "nvl2")

# ---- Optional pandas helpers ----
# Import only if available otherwise leave them absent.
try:
    from .pandas_ext import (
        pd_decode,
        pd_noneif,
        pd_nvl,
        pd_nvl2,
        pd_sign,
    )
except ImportError:
    pass
else:
    __all__ += ("pd_sign", "pd_nvl", "pd_nvl2", "pd_noneif", "pd_decode")
