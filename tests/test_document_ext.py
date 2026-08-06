import importlib.util
import json
from io import BytesIO, StringIO
from pathlib import Path

import pytest

from pynvl import UnsupportedDocumentFormatError, document_ext, utl_to_text

DOCX_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


def test_plain_text_from_content_string():
    assert utl_to_text("Hello\r\nworld  \r\n\r\n\r\nAgain") == "Hello\nworld\n\nAgain"


def test_plain_text_from_path():
    path = Path(".utl_to_text_path_test.txt")
    try:
        path.write_text("From a file", encoding="utf-8")
        assert utl_to_text(path) == "From a file"
        assert utl_to_text(str(path)) == "From a file"
    finally:
        path.unlink(missing_ok=True)


def test_plain_text_from_bytes_with_encoding():
    assert utl_to_text("café".encode("latin-1"), encoding="latin-1") == "café"


def test_text_and_binary_file_like_inputs():
    assert utl_to_text(StringIO("text stream")) == "text stream"
    assert utl_to_text(BytesIO(b"binary stream")) == "binary stream"


def test_explicit_content_type_has_priority():
    assert utl_to_text(b"# heading", content_type="text/plain") == "# heading"
    assert utl_to_text("# heading", content_type="text/markdown") == "heading"


def test_string_is_a_path_only_when_it_names_an_existing_file():
    path = Path(".utl_to_text_detection_test.txt")
    assert utl_to_text(str(path)) == str(path)
    try:
        path.write_text("file contents", encoding="utf-8")
        assert utl_to_text(str(path)) == "file contents"
    finally:
        path.unlink(missing_ok=True)


def test_html_returns_visible_text_with_boundaries():
    html = """
    <html><head><title>Hidden title</title><meta name="x" content="hidden"></head>
    <body><p>Hello <strong>world</strong></p><div>Second<br>line</div></body></html>
    """
    assert utl_to_text(html) == "Hello world\n\nSecond\nline"


def test_html_excludes_scripts_styles_and_non_visible_elements():
    html = """
    <body>Visible<script>alert('hidden')</script><style>.hidden {}</style>
    <template>template text</template><noscript>fallback</noscript>End</body>
    """
    output = utl_to_text(html)
    assert output == "Visible\nEnd"
    assert "hidden" not in output


def test_xml_extracts_text_in_document_order():
    xml = "<catalog><book><title>First</title><author>Ada</author></book><book>Second</book></catalog>"
    assert utl_to_text(xml) == "First\nAda\nSecond"


def test_nested_json_preserves_keys_values_and_order():
    data = {
        "title": "Example",
        "details": {"active": True, "count": 2},
        "missing": None,
    }
    output = utl_to_text(json.dumps(data))
    assert output == (
        "title: Example\n"
        "details:\n"
        "  active: true\n"
        "  count: 2\n"
        "missing: null"
    )


@pytest.mark.parametrize(
    "source,expected",
    [
        ('["one", 2, false, null]', "- one\n- 2\n- false\n- null"),
        ('"hello"', "hello"),
        ("42", "42"),
        ("true", "true"),
        ("null", "null"),
    ],
)
def test_json_arrays_and_scalar_values(source, expected):
    assert utl_to_text(source, content_type="application/json") == expected


def test_markdown_cleanup_preserves_words_and_structure():
    markdown = """# Report

This is **important** and [documented](https://example.test).

- First item
- Second `item`
"""
    assert utl_to_text(markdown) == (
        "Report\n\n"
        "This is important and documented.\n\n"
        "First item\n"
        "Second item"
    )


@pytest.mark.parametrize("source", ["", b"", StringIO("")])
def test_empty_valid_document_returns_empty_string(source):
    assert utl_to_text(source) == ""


def test_unsupported_content_type():
    with pytest.raises(
        UnsupportedDocumentFormatError, match="Unsupported content type"
    ):
        utl_to_text("data", content_type="application/octet-stream")


def test_undetectable_binary_format():
    with pytest.raises(UnsupportedDocumentFormatError, match="binary document format"):
        utl_to_text(b"\x00\xff\x00\xfe")


def test_malformed_json_is_not_silently_swallowed():
    with pytest.raises(ValueError, match="Malformed JSON"):
        utl_to_text('{"broken": }')


def test_malformed_xml_is_not_silently_swallowed():
    with pytest.raises(ValueError, match="Malformed XML"):
        utl_to_text("<root><broken></root>")


@pytest.mark.parametrize("source", [123, object()])
def test_invalid_source_type(source):
    with pytest.raises(TypeError, match="source must be"):
        utl_to_text(source)


def test_file_like_object_must_return_supported_data():
    class BadReader:
        def read(self):
            return 123

    with pytest.raises(TypeError, match=r"source\.read\(\)"):
        utl_to_text(BadReader())


def test_missing_explicit_path():
    with pytest.raises(FileNotFoundError):
        utl_to_text(Path("definitely-does-not-exist.txt"))


def test_missing_pdf_dependency_has_install_instructions(monkeypatch):
    def missing_pypdf(name):
        if name == "pypdf":
            error = ModuleNotFoundError("No module named 'pypdf'")
            error.name = "pypdf"
            raise error
        return importlib.import_module(name)

    monkeypatch.setattr(document_ext, "import_module", missing_pypdf)
    with pytest.raises(ImportError, match=r"pynvl-lib\[documents\].*pypdf"):
        utl_to_text(b"%PDF-1.4\n", content_type="application/pdf")


def test_missing_docx_dependency_has_install_instructions(monkeypatch):
    def missing_docx(name):
        if name == "docx" or name.startswith("docx."):
            error = ModuleNotFoundError("No module named 'docx'")
            error.name = name
            raise error
        return importlib.import_module(name)

    monkeypatch.setattr(document_ext, "import_module", missing_docx)
    with pytest.raises(ImportError, match=r"pynvl-lib\[documents\].*python-docx"):
        utl_to_text(b"PK\x03\x04", content_type=DOCX_CONTENT_TYPE)


@pytest.mark.skipif(
    importlib.util.find_spec("pypdf") is None, reason="pypdf not installed"
)
def test_pdf_fixture_is_created_programmatically():
    PdfWriter = pytest.importorskip("pypdf").PdfWriter

    stream = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(stream)
    assert utl_to_text(stream.getvalue(), content_type="application/pdf") == ""


@pytest.mark.skipif(
    importlib.util.find_spec("docx") is None, reason="python-docx not installed"
)
def test_docx_paragraphs_and_tables_in_document_order():
    Document = pytest.importorskip("docx").Document

    document = Document()
    document.add_paragraph("Before table")
    table = document.add_table(rows=1, cols=2)
    table.cell(0, 0).text = "A"
    table.cell(0, 1).text = "B"
    document.add_paragraph("After table")
    stream = BytesIO()
    document.save(stream)

    assert utl_to_text(stream.getvalue()) == "Before table\nA\tB\nAfter table"


def test_top_level_export_and_all():
    import pynvl
    from pynvl import utl_to_text as public_utl_to_text

    assert public_utl_to_text is pynvl.utl_to_text
    assert "utl_to_text" in pynvl.__all__
    assert "UnsupportedDocumentFormatError" in pynvl.__all__
