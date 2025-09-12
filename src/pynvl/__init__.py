"""
pynvl: Oracle-inspired helper functions for Python.
Core exports: nvl, decode, sign, noneif, nvl2
Optional pandas exports: pd_sign, pd_nvl, pd_nvl2, pd_noneif, pd_decode
"""
from .core import nvl, decode, sign, noneif, nvl2

__all__ = ["nvl", "decode", "sign", "noneif", "nvl2"]

# Expose pandas helpers only if pandas is installed
# so importing pynvl doesn't force a pandas dependency.
try:
    from .pandas_ext import pd_sign, pd_nvl, pd_nvl2, pd_noneif, pd_decode
except ImportError:
    # pandas not installed (or other import issue) — skip optional exports
    pass
else:
    __all__ += ["pd_sign", "pd_nvl", "pd_nvl2", "pd_noneif", "pd_decode"]
