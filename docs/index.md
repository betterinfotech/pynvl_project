# pynvl

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/betterinfotech/pynvl_project/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pynvl-lib.svg)](https://pypi.org/project/pynvl-lib/)

`pynvl` is an actively maintained Python library that brings familiar,
Oracle-inspired data utilities to Python applications. It combines predictable
scalar and pandas helpers with document text extraction for modern search and
AI-enabled data pipelines.

## Features

- `nvl(expr, default)` — substitutes a value when `None` is encountered
- `decode(expr, search1, result1, ..., default)` — provides concise conditional mapping
- `sign(n)` — returns a value indicating the sign of a number
- `noneif(expr1, expr2)` — returns `None` when two expressions are equal
- `nvl2(expr, value_if_not_null, value_if_null)` — extends `nvl`
- `coalesce(expr1, expr2, ..., expr_n)` — returns the first non-`None` value
- `extract(datetime, fmt)` — extracts formatted values from datetime objects
- `utl_to_text(source, ...)` — extracts readable text from common document formats

`utl_to_text`, inspired by Oracle AI Database's
`DBMS_VECTOR_CHAIN.UTL_TO_TEXT`, normalizes documents into text suitable for
chunking, retrieval, LLM, and RAG workflows. It does not perform embedding or
model inference itself.

## Pandas integration

`pynvl` provides optional pandas-native helpers that operate element-wise on
`pd.Series` values.

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

## Installation from PyPI

```bash
pip install pynvl-lib
```

Install optional PDF and DOCX extraction support with:

```bash
pip install "pynvl-lib[documents]"
```

See [Document text extraction](documents.md) for supported inputs, examples, and
limitations, or visit the [demo page](demo.md) for additional examples.
