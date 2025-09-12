# pynvl

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/betterinfotech/pynvl_project/blob/main/LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-blue)](https://github.com/betterinfotech/pynvl_project/actions)
[![TestPyPI](https://img.shields.io/badge/TestPyPI-pynvl--test-informational)](https://test.pypi.org/project/pynvl-test/)

**Helper functions for data engineering and analytics workflows in Python, inspired by PL/SQL.**

---

## 📦 Installation

```python
pip install --index-url https://test.pypi.org/simple/ --no-deps pynvl-test
```
---

## ✨ Quick Example

```python
from pynvl import nvl, decode, sign

print(nvl(None, 5))     # 5
print(sign(-7))         # -1
print(decode("A", "A", "Alpha", "B", "Beta", default="Unknown")) # 'Alpha'
```
---
## 👉 Full documentation [here](docs/index.md)