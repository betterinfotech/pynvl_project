# pynvl

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/betterinfotech/pynvl_project/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pynvl.svg)](https://pypi.org/project/pynvl-lib/)
[![PyPI](https://img.shields.io/pypi/v/pynvl.svg)](https://pypi.org/project/pynvl-lib/)

**Helper functions for data engineering in Python, inspired by PL/SQL.**

This package contains a suite of functions which flatten out data handling.  
It’s complemented by helpers for use with pandas as well which I hope people find useful.

---

## ✨ Features

- `nvl(expr, default)` => coalesce `None` to a default  
- `decode(expr, search1, result1, ..., default)` => compact conditional mapping  
- `sign(n)` => return `-1`, `0`, or `1` depending on numeric sign  
- Special handling: `decode(None, None, ...)` treats `None == None` (follows PL/SQL)  
- Fully tested with `pytest`  
- MIT Licensed  

---

## 📊 Pandas Integration

`pynvl` also provides optional pandas-native helpers for use with `pd.Series` and operates element-wise.

```python
import pandas as pd
from pynvl import pd_sign, pd_nvl, pd_nvl2, pd_noneif, pd_decode

s = pd.Series([-5, 0, 3, None])

print(pd_sign(s).tolist())
# [-1, 0, 1, None]

print(pd_nvl(s, 99).tolist())
# [-5, 0, 3, 99]

print(pd_nvl2(s, "not-null", "is-null").tolist())
# ['not-null', 'not-null', 'not-null', 'is-null']

print(pd_noneif(s, 0).tolist())
# [-5, None, 3, None]

print(pd_decode(s, -5, "neg", 0, "zero", 3, "pos", default="other").tolist())
# ['neg', 'zero', 'pos', 'other']
```

---

## 📦 Installation From PyPI
```bash
pip install pynvl-lib
```
---

## 👉 [Demo page](demo.md)
