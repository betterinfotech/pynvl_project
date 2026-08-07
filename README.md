# pynvl

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/betterinfotech/pynvl_project/blob/main/LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-blue)](https://github.com/betterinfotech/pynvl_project/actions)
[![PyPI](https://img.shields.io/pypi/v/pynvl-lib.svg)](https://pypi.org/project/pynvl-lib/)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-success)](https://betterinfotech.github.io/pynvl_project/)

`pynvl` is an actively maintained, open-source Python library for familiar
data-handling operations inspired by Oracle SQL and PL/SQL. It provides small,
predictable utilities for scalar values and pandas data, together with document
text extraction designed to prepare common formats for search, chunking, embedding,
and other AI-enabled workflows.

The package keeps its core dependency-free, exposes a documented top-level API,
and uses optional dependencies only where document formats require them.

## Features

- Oracle-inspired helpers including `nvl`, `nvl2`, `decode`, `coalesce`,
  `noneif`, `sign`, and datetime `extract`
- Optional pandas-native equivalents for element-wise data processing
- `utl_to_text` extraction for plain text, Markdown, HTML, XML, JSON, PDF, and DOCX
- Format detection across paths, content strings, bytes, and file-like objects
- A pytest test suite, type checking, linting, published documentation, and CI

## Installation

```bash
pip install pynvl-lib
```

Install optional PDF and DOCX support with:

```bash
pip install "pynvl-lib[documents]"
```

## Quick examples

```python
from pynvl import decode, nvl, sign

print(nvl(None, 5))  # 5
print(sign(-7))  # -1
print(decode("A", "A", "Alpha", "B", "Beta", default="Unknown"))  # 'Alpha'
```

## Document text extraction

`utl_to_text` provides one Pythonic API for extracting readable text from
common structured and document formats:

```python
from pynvl import utl_to_text

text = utl_to_text("report.pdf")
text = utl_to_text("<html><body><p>Hello</p></body></html>")
text = utl_to_text(
    b'{"title": "Example", "active": true}',
    content_type="application/json",
)
```

The API is inspired by Oracle AI Database's
`DBMS_VECTOR_CHAIN.UTL_TO_TEXT`. It is a practical Python implementation, not
an Oracle Text implementation, and does not guarantee identical extraction
output. It does not perform OCR, download URLs, or support legacy Office or
password-protected documents.

See the [full documentation](https://betterinfotech.github.io/pynvl_project/)
for the public API, supported inputs, format behavior, and limitations.
