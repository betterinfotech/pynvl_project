import pandas as pd
import numpy as np
from typing import Any

__all__ = ["pd_sign", "pd_nvl", "pd_nvl2", "pd_noneif", "pd_decode"]


def pd_sign(series: pd.Series) -> pd.Series:
    pos = series.gt(0).astype("Int8")   # 1 where >0, else 0
    neg = series.lt(0).astype("Int8")   # 1 where <0, else 0
    out = (pos - neg).astype("object")  # 1 - 0 = 1, 0 - 1 = -1, 0 - 0 = 0
    # set None where original is null
    out = out.where(series.notna(), None)
    return out


def pd_nvl(series: pd.Series, default: Any) -> pd.Series:
    return series.fillna(default)


def pd_nvl2(series: pd.Series, value_if_not_null: Any, value_if_null: Any) -> pd.Series:
    return series.notna().map(lambda cond: value_if_not_null if cond else value_if_null)


def pd_noneif(series_a: pd.Series, series_b: pd.Series) -> pd.Series:
    # Treat NaN==NaN as equal
    equal = series_a.eq(series_b) | (series_a.isna() & series_b.isna())

    # Work in object dtype and assign None explicitly at equal positions
    out = series_a.astype("object").copy()
    out.loc[equal] = None
    return out


def pd_decode(series: pd.Series, *pairs: Any, default: Any = None) -> pd.Series:
    n = len(pairs)
    implicit_default = None

    if n == 0:
        return pd.Series([default] * len(series), index=series.index)

    if n % 2 == 1:
        implicit_default = pairs[-1]
        pairs = pairs[:-1]

    # start with default
    out = pd.Series(default if default is not None else implicit_default,
                    index=series.index)

    it = iter(pairs)
    for search, result in zip(it, it):
        mask = (series == search) | (series.isna() & pd.isna(search))
        out = out.where(~mask, result)

    return out
