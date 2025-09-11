import pandas as pd
import numpy as np

from pynvl.pandas_ext import pd_sign, pd_nvl, pd_nvl2, pd_noneif, pd_decode


def to_list(s: pd.Series):
    """Helper to compare with Python values (preserve None)."""
    return s.astype("object").tolist()


def test_pd_sign_basic():
    s = pd.Series([-5, 0, 3, None])
    out = pd_sign(s)
    assert to_list(out) == [-1, 0, 1, None]


def test_pd_nvl_basic():
    s = pd.Series([1, None, 3, np.nan])
    out = pd_nvl(s, default=99)
    assert to_list(out) == [1, 99, 3, 99]


def test_pd_nvl2_basic():
    s = pd.Series([10, None, 20])
    out = pd_nvl2(s, value_if_not_null="Y", value_if_null="N")
    assert to_list(out) == ["Y", "N", "Y"]


def test_pd_noneif_basic_and_null_handling():
    a = pd.Series([1, 2, 3, None, np.nan])
    b = pd.Series([1, 9, 3, None, np.nan])
    out = pd_noneif(a, b)
    # Expected semantics: return None when equal (including None==None / NaN==NaN), else return a
    # If your implementation doesn't treat NaN==NaN as equal, update it accordingly.
    assert to_list(out) == [None, 2, None, None, None]


def test_pd_decode_basic_mapping():
    s = pd.Series(["A", "B", "C", None])
    out = pd_decode(s, "A", "Alpha", "B", "Beta", default="Other")
    assert to_list(out) == ["Alpha", "Beta", "Other", "Other"]


def test_pd_decode_none_equals_none():
    s = pd.Series([None, "X", None])
    # Special rule: in DECODE, None == None
    out = pd_decode(s, None, "NullMatch", default="Nope")
    assert to_list(out) == ["NullMatch", "Nope", "NullMatch"]


def test_pd_decode_implicit_default():
    s = pd.Series(["Z", "A"])
    # Odd number of args after expr → last is implicit default
    out = pd_decode(s, "A", "Alpha", "Implicit")
    assert to_list(out) == ["Implicit", "Alpha"]
