# pynvl

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Helper functions for data engineering and analytics workflows in Python, inspired by PL/SQL.**

This package provides concise, battle-tested functions that make common data-wrangling tasks easier.  
It’s designed for Python developers who need simple, reliable transformations that feel natural in code or Pandas pipelines.

## Features
- `nvl(expr, default)` → coalesce None to a default
- `decode(expr, search1, result1, ..., default)` → compact conditional mapping
- `sign(n)` → return -1, 0, or 1 depending on numeric sign
- Special handling: `decode(None, None, ...)` treats `None` = `None` (faithful to PL/SQL semantics)
- Fully tested with `pytest`
- MIT Licensed
