# Document text extraction

`utl_to_text` extracts readable plain text from several common document formats
through one API:

```python
from pynvl import utl_to_text

text = utl_to_text("report.pdf")
text = utl_to_text("<html><body><p>Hello</p></body></html>")
text = utl_to_text(
    b'{"title": "Example", "active": true}',
    content_type="application/json",
)
```

The design is inspired by Oracle `DBMS_VECTOR_CHAIN.UTL_TO_TEXT`. It is a
practical Python utility, not an implementation of Oracle Text, and it does not
guarantee the same extraction output as Oracle.

## API

```python
utl_to_text(source, *, content_type=None, encoding="utf-8")
```

`source` may be:

- A `str` or `pathlib.Path` file path
- A text content string
- `bytes` or `bytearray`
- A binary file-like object
- A text file-like object

A string is treated as a path only when it identifies an existing file. Any
other string is treated as document content. An explicit `Path` must exist and
must identify a file.

Format detection considers, in order:

1. Explicit `content_type`
2. A recognized file extension
3. PDF and DOCX binary signatures
4. Inspection for HTML, XML, JSON, Markdown, or plain text

Use `content_type` when content is ambiguous. MIME types and short aliases are
accepted, including `text/plain`, `text/markdown`, `text/html`,
`application/xml`, `text/xml`, `application/json`, `application/pdf`, and the
DOCX MIME type.

## Supported formats

| Format | Behaviour | Dependency |
| --- | --- | --- |
| Plain text | Decodes with `encoding` and normalizes whitespace | Standard library |
| Markdown | Removes common markup while retaining words and line structure | Standard library |
| HTML | Extracts visible text and excludes non-visible elements | Standard library |
| XML | Returns text nodes in document order | Standard library |
| JSON | Traverses objects and arrays into readable lines | Standard library |
| PDF | Extracts pages in page order with explicit page separators | `pypdf` |
| DOCX | Extracts paragraphs and table rows in document order | `python-docx` |

Install PDF and DOCX support with:

```bash
pip install "pynvl-lib[documents]"
```

The base package remains importable without these dependencies. Calling PDF or
DOCX extraction without its dependency raises an `ImportError` with installation
instructions.

## JSON output

JSON objects retain their parsed insertion order. Scalar fields are emitted as
`key: value`. Nested object and array keys become headings followed by indented
content. Arrays preserve item order. Strings and numbers use their readable
values, booleans are written as `true` or `false`, and JSON null is written as
`null`. JSON syntax punctuation is not copied into the result.

## Output normalization

The function always returns `str`. It converts line endings to `\n`, removes
trailing spaces, limits consecutive blank lines to one, and preserves useful
paragraph, table-row, and PDF page boundaries. An empty valid document returns
an empty string. Malformed JSON and XML raise `ValueError` rather than being
silently treated as text.

## Limitations

- No OCR or image extraction
- No embeddings, chunking, summarisation, or remote AI services
- No automatic URL downloads
- No legacy binary Microsoft Office formats
- No password-protected documents
- PDF extraction is limited to text already represented in the PDF
- Markdown handling covers common syntax rather than implementing a complete renderer
- Extraction output may differ from browsers, office applications, and Oracle Text
