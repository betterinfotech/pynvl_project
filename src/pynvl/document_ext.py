"""Document-to-text helpers inspired by Oracle DBMS_VECTOR_CHAIN.UTL_TO_TEXT."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from html.parser import HTMLParser
from importlib import import_module
from io import BytesIO
from pathlib import Path
from typing import Any
from zipfile import BadZipFile, ZipFile

__all__ = ("UnsupportedDocumentFormatError", "utl_to_text")


class UnsupportedDocumentFormatError(ValueError):
    """Raised when a source's document format is unsupported or undetectable."""


class _DocumentFormat(Enum):
    TEXT = "text"
    MARKDOWN = "markdown"
    HTML = "html"
    XML = "xml"
    JSON = "json"
    PDF = "pdf"
    DOCX = "docx"


@dataclass(frozen=True)
class _LoadedSource:
    data: str | bytes
    extension: str | None = None


_CONTENT_TYPES = {
    "text/plain": _DocumentFormat.TEXT,
    "plain": _DocumentFormat.TEXT,
    "text": _DocumentFormat.TEXT,
    "text/markdown": _DocumentFormat.MARKDOWN,
    "text/x-markdown": _DocumentFormat.MARKDOWN,
    "markdown": _DocumentFormat.MARKDOWN,
    "md": _DocumentFormat.MARKDOWN,
    "text/html": _DocumentFormat.HTML,
    "application/xhtml+xml": _DocumentFormat.HTML,
    "html": _DocumentFormat.HTML,
    "application/xml": _DocumentFormat.XML,
    "text/xml": _DocumentFormat.XML,
    "xml": _DocumentFormat.XML,
    "application/json": _DocumentFormat.JSON,
    "text/json": _DocumentFormat.JSON,
    "json": _DocumentFormat.JSON,
    "application/pdf": _DocumentFormat.PDF,
    "pdf": _DocumentFormat.PDF,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": _DocumentFormat.DOCX,
    "docx": _DocumentFormat.DOCX,
}

_EXTENSIONS = {
    ".txt": _DocumentFormat.TEXT,
    ".text": _DocumentFormat.TEXT,
    ".md": _DocumentFormat.MARKDOWN,
    ".markdown": _DocumentFormat.MARKDOWN,
    ".html": _DocumentFormat.HTML,
    ".htm": _DocumentFormat.HTML,
    ".xhtml": _DocumentFormat.HTML,
    ".xml": _DocumentFormat.XML,
    ".json": _DocumentFormat.JSON,
    ".pdf": _DocumentFormat.PDF,
    ".docx": _DocumentFormat.DOCX,
}

_BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "br",
    "dd",
    "div",
    "dl",
    "dt",
    "figcaption",
    "figure",
    "footer",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "td",
    "th",
    "tr",
    "ul",
}
_HIDDEN_TAGS = {"head", "metadata", "noscript", "script", "style", "template"}


class _VisibleHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._hidden_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        tag = tag.lower()
        if tag in _HIDDEN_TAGS:
            self._hidden_depth += 1
        elif not self._hidden_depth and tag in _BLOCK_TAGS:
            self.parts.append("\n" if tag == "br" else "\n\n")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() in _HIDDEN_TAGS:
            self._hidden_depth -= 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in _HIDDEN_TAGS:
            self._hidden_depth = max(0, self._hidden_depth - 1)
        elif not self._hidden_depth and tag in _BLOCK_TAGS:
            self.parts.append("\n" if tag == "br" else "\n\n")

    def handle_data(self, data: str) -> None:
        if not self._hidden_depth:
            self.parts.append(data)


def utl_to_text(
    source: str | Path | bytes | bytearray | Any,
    *,
    content_type: str | None = None,
    encoding: str = "utf-8",
) -> str:
    """Extract readable plain text from a document source.

    Strings naming an existing file are loaded as paths. Other strings are treated
    as document content. Explicit ``Path`` objects must point to an existing file.
    Supported formats are plain text, Markdown, HTML, XML, JSON, PDF, and DOCX.
    PDF and DOCX extraction require the optional ``documents`` dependencies.
    """
    if not isinstance(encoding, str):
        raise TypeError("encoding must be a string")

    loaded = _load_source(source)
    document_format = _detect_format(loaded, content_type, encoding)
    extractor = _EXTRACTORS[document_format]
    return _normalize_text(extractor(loaded.data, encoding))


def _load_source(source: Any) -> _LoadedSource:
    if isinstance(source, Path):
        if not source.exists():
            raise FileNotFoundError(source)
        if not source.is_file():
            raise IsADirectoryError(source)
        return _LoadedSource(source.read_bytes(), source.suffix.lower() or None)

    if isinstance(source, str):
        try:
            candidate = Path(source)
        except (OSError, ValueError):
            return _LoadedSource(source)
        try:
            is_existing_file = candidate.is_file()
        except OSError:
            is_existing_file = False
        if is_existing_file:
            return _LoadedSource(
                candidate.read_bytes(), candidate.suffix.lower() or None
            )
        return _LoadedSource(source)

    if isinstance(source, (bytes, bytearray)):
        return _LoadedSource(bytes(source))

    read = getattr(source, "read", None)
    if not callable(read):
        raise TypeError(
            "source must be a path, str, bytes, bytearray, or readable file-like object"
        )

    data = read()
    if isinstance(data, bytearray):
        data = bytes(data)
    if not isinstance(data, (str, bytes)):
        raise TypeError("source.read() must return str, bytes, or bytearray")

    extension = None
    name = getattr(source, "name", None)
    if isinstance(name, (str, Path)):
        extension = Path(name).suffix.lower() or None
    return _LoadedSource(data, extension)


def _detect_format(
    source: _LoadedSource, content_type: str | None, encoding: str
) -> _DocumentFormat:
    if content_type is not None:
        if not isinstance(content_type, str):
            raise TypeError("content_type must be a string or None")
        normalized = content_type.split(";", 1)[0].strip().lower()
        try:
            return _CONTENT_TYPES[normalized]
        except KeyError as exc:
            raise UnsupportedDocumentFormatError(
                f"Unsupported content type: {content_type!r}"
            ) from exc

    if source.extension in _EXTENSIONS:
        return _EXTENSIONS[source.extension]

    if isinstance(source.data, bytes):
        if source.data.startswith(b"%PDF-"):
            return _DocumentFormat.PDF
        if _is_docx(source.data):
            return _DocumentFormat.DOCX
        try:
            text = source.data.decode(encoding)
        except UnicodeDecodeError as exc:
            raise UnsupportedDocumentFormatError(
                "Unable to detect a supported binary document format"
            ) from exc
    else:
        text = source.data

    stripped = text.lstrip("\ufeff\x00\t\r\n ")
    lowered = stripped[:512].lower()
    if not stripped:
        return _DocumentFormat.TEXT
    if re.search(r"<(?:!doctype\s+html|html|head|body|p|div|script|style)\b", lowered):
        return _DocumentFormat.HTML
    if stripped.startswith("<?xml") or re.match(
        r"<[A-Za-z_][\w.:-]*(?:\s|>|/)", stripped
    ):
        return _DocumentFormat.XML
    if (
        stripped[:1] in '{["'
        or stripped in {"true", "false", "null"}
        or re.fullmatch(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?", stripped)
    ):
        return _DocumentFormat.JSON
    if _looks_like_markdown(text):
        return _DocumentFormat.MARKDOWN
    return _DocumentFormat.TEXT


def _is_docx(data: bytes) -> bool:
    if not data.startswith(b"PK"):
        return False
    try:
        with ZipFile(BytesIO(data)) as archive:
            return "word/document.xml" in archive.namelist()
    except BadZipFile:
        return False


def _looks_like_markdown(text: str) -> bool:
    return bool(
        re.search(
            r"(?m)^(?:#{1,6}\s+|\s*(?:[-+*]|\d+[.)])\s+|>\s+|```|~~~|\|.+\|\s*$)",
            text,
        )
        or re.search(r"!?\[[^]]+\]\([^)]+\)|\*\*[^*]+\*\*|__[^_]+__", text)
    )


def _as_text(data: str | bytes, encoding: str) -> str:
    return data if isinstance(data, str) else data.decode(encoding)


def _extract_plain(data: str | bytes, encoding: str) -> str:
    return _as_text(data, encoding)


def _extract_markdown(data: str | bytes, encoding: str) -> str:
    text = _as_text(data, encoding)
    text = re.sub(r"(?s)<!--.*?-->", "", text)
    text = re.sub(r"(?m)^[ \t]*(?:```|~~~)[^\n]*$", "", text)
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"(?m)^[ \t]{0,3}#{1,6}[ \t]*", "", text)
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    text = re.sub(r"(?m)^[ \t]*(?:[-+*]|\d+[.)])[ \t]+", "", text)
    text = re.sub(r"(?m)^[ \t]*(?:-{3,}|_{3,}|\*{3,})[ \t]*$", "", text)
    text = re.sub(r"(?<!\\)\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(
        r"(?<![\w\\])__(?=\S)((?:(?!__).)+?)(?<=\S)__(?![\w.])",
        r"\1",
        text,
    )
    text = re.sub(r"(?<!\\)\*(.+?)\*", r"\1", text)
    text = re.sub(r"(?<![\w\\])_(?!_)(?=\S)(.+?)(?<=\S)_(?![\w_])", r"\1", text)
    text = re.sub(r"(?<!\\)`([^`]+)`", r"\1", text)
    text = re.sub(
        r"(?m)^[ \t]*\|?[ \t]*:?-{3,}:?[ \t]*(?:\|[ \t]*:?-{3,}:?[ \t]*)+\|?[ \t]*$",
        "",
        text,
    )
    text = re.sub(
        r"(?m)^[ \t]*\|(.+)\|[ \t]*$",
        lambda m: "\t".join(part.strip() for part in m.group(1).split("|")),
        text,
    )
    return text.replace("\\*", "*").replace("\\_", "_")


def _extract_html(data: str | bytes, encoding: str) -> str:
    parser = _VisibleHTMLParser()
    parser.feed(_as_text(data, encoding))
    parser.close()
    return "\n".join(line.strip() for line in "".join(parser.parts).splitlines())


def _extract_xml(data: str | bytes, encoding: str) -> str:
    text = _as_text(data, encoding)
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise ValueError(f"Malformed XML: {exc}") from exc
    return "\n".join(part for part in root.itertext())


def _extract_json(data: str | bytes, encoding: str) -> str:
    text = _as_text(data, encoding)
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc.msg}") from exc
    return "\n".join(_json_lines(value))


def _json_lines(value: Any, indent: int = 0) -> list[str]:
    prefix = "  " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(_json_lines(item, indent + 1))
            else:
                lines.append(f"{prefix}{key}: {_json_scalar(item)}")
        return lines
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(_json_lines(item, indent + 1))
            else:
                lines.append(f"{prefix}- {_json_scalar(item)}")
        return lines
    return [f"{prefix}{_json_scalar(value)}"]


def _json_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def _extract_pdf(data: str | bytes, encoding: str) -> str:
    del encoding
    if isinstance(data, str):
        data = data.encode("latin-1")
    try:
        PdfReader = import_module("pypdf").PdfReader
    except ModuleNotFoundError as exc:
        if exc.name != "pypdf":
            raise
        raise ImportError(
            'PDF extraction requires pypdf. Install with pip install "pynvl-lib[documents]" or pip install pypdf.'
        ) from exc

    reader = PdfReader(BytesIO(data))
    if reader.is_encrypted:
        raise ValueError("Password-protected PDF documents are not supported")
    pages = [(page.extract_text() or "") for page in reader.pages]
    return "\n\n--- Page Break ---\n\n".join(pages)


def _extract_docx(data: str | bytes, encoding: str) -> str:
    del encoding
    if isinstance(data, str):
        raise TypeError("DOCX content must be supplied as binary data")
    try:
        Document = import_module("docx").Document
        Table = import_module("docx.table").Table
        Paragraph = import_module("docx.text.paragraph").Paragraph
    except ModuleNotFoundError as exc:
        if exc.name != "docx" and not (exc.name or "").startswith("docx."):
            raise
        raise ImportError(
            'DOCX extraction requires python-docx. Install with pip install "pynvl-lib[documents]" or pip install python-docx.'
        ) from exc

    document = Document(BytesIO(data))
    lines: list[str] = []
    for child in document.element.body.iterchildren():
        if child.tag.endswith("}p"):
            paragraph = Paragraph(child, document)
            lines.append(paragraph.text)
        elif child.tag.endswith("}tbl"):
            table = Table(child, document)
            for row in table.rows:
                lines.append("\t".join(cell.text for cell in row.cells))
    return "\n".join(lines)


def _normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[ \t]+$", "", line) for line in text.split("\n")]
    normalized: list[str] = []
    blank = False
    for line in lines:
        if line.strip():
            normalized.append(
                line.strip() if not line.startswith("  ") else line.rstrip()
            )
            blank = False
        elif normalized and not blank:
            normalized.append("")
            blank = True
    while normalized and not normalized[-1]:
        normalized.pop()
    return "\n".join(normalized)


_Extractor = Callable[[str | bytes, str], str]
_EXTRACTORS: dict[_DocumentFormat, _Extractor] = {
    _DocumentFormat.TEXT: _extract_plain,
    _DocumentFormat.MARKDOWN: _extract_markdown,
    _DocumentFormat.HTML: _extract_html,
    _DocumentFormat.XML: _extract_xml,
    _DocumentFormat.JSON: _extract_json,
    _DocumentFormat.PDF: _extract_pdf,
    _DocumentFormat.DOCX: _extract_docx,
}
