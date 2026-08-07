# pynvl

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/betterinfotech/pynvl_project/blob/main/LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-blue)](https://github.com/betterinfotech/pynvl_project/actions)
[![PyPI](https://img.shields.io/pypi/v/pynvl-lib.svg)](https://pypi.org/project/pynvl-lib/)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-success)](https://betterinfotech.github.io/pynvl_project/)

**General purpose data utilities, inspired by PL/SQL.**

---

## 🔹 Installation

```python
pip install pynvl-lib
```
---

## 🔹 Quick Examples

```python
from pynvl import nvl, decode, sign

print(nvl(None, 5))     # 5
print(sign(-7))         # -1
print(decode("A", "A", "Alpha", "B", "Beta", default="Unknown")) # 'Alpha'
```

## Document text extraction

`utl_to_text` provides one Pythonic API for extracting readable text from plain
text, Markdown, HTML, XML, JSON, PDF, and DOCX input:

```python
from pynvl import utl_to_text

text = utl_to_text("report.pdf")
text = utl_to_text("<html><body><p>Hello</p></body></html>")
text = utl_to_text(
    b'{"title": "Example", "active": true}',
    content_type="application/json",
)
```

PDF and DOCX support use optional dependencies:

```bash
pip install "pynvl-lib[documents]"
```

The function is inspired by Oracle `DBMS_VECTOR_CHAIN.UTL_TO_TEXT`, but it is
not an Oracle Text implementation and does not guarantee identical extraction
output. It does not perform OCR, download URLs, or support legacy Office or
password-protected documents.

---
## 🔹 Full documentation: [Docs site](https://betterinfotech.github.io/pynvl_project/)
