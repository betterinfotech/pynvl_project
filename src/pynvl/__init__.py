"""
pynvl: Oracle-inspired helper functions for Python.

Core exports:
    nvl, decode, sign, noneif, nvl2

Optional pandas exports (if pandas is installed):
    pd_sign, pd_nvl, pd_nvl2, pd_noneif, pd_decode
"""

# Public API
from .core import nvl, decode, sign, noneif, nvl2
__all__ = ["nvl", "decode", "sign", "noneif", "nvl2"]

# Package metadata (distribution name is 'pynvl-lib')
try:
    from importlib.metadata import version, PackageNotFoundError  # py>=3.8
except Exception:  # very defensive; shouldn't happen on >=3.10
    __version__ = "0.dev0"
else:
    try:
        __version__ = version("pynvl-lib")
    except PackageNotFoundError:
        # Running from source/tree without an installed dist
        __version__ = "0.dev0"

__url__ = "https://betterinfotech.github.io/pynvl_project/"

# Optional pandas helpers — import only if available
try:
    from .pandas_ext import pd_sign, pd_nvl, pd_nvl2, pd_noneif, pd_decode  # noqa: F401
except ImportError:
    pass
else:
    __all__ += ["pd_sign", "pd_nvl", "pd_nvl2", "pd_noneif", "pd_decode"]
