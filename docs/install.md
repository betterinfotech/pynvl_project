# Installation

pynvl is distributed as a standard Python package avaialble from **PyPI**.



```bash
pip install pynvl-lib
```

## Optional document support

Plain text, Markdown, HTML, XML, and JSON extraction use the Python standard
library. Install the `documents` extra for PDF and DOCX extraction:

```bash
pip install "pynvl-lib[documents]"
```

This installs `pypdf` for PDF text extraction and `python-docx` for DOCX files.
