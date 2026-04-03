from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(
        description="Absolute or relative path to the document file to convert (e.g. /docs/report.pdf or ./report.docx)"
    ),
) -> str:
    """Convert a document file on disk to markdown-formatted text.

    Reads the file at the given path, determines its type from the file
    extension, and converts the contents to markdown using markitdown.
    Supports any format accepted by markitdown, including DOCX and PDF.

    When to use:
    - When you have a local file path and need its content as markdown
    - When you need to extract structured text from a DOCX or PDF on disk
    - Not for files already loaded into memory as bytes (use binary_document_to_markdown instead)
    - Not for remote URLs

    Examples:
    >>> document_path_to_markdown("/home/user/report.docx")
    "# Report Title\\n\\nSome content..."
    >>> document_path_to_markdown("./notes.pdf")
    "# Notes\\n\\n- Item one..."
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No file found at path: {file_path}")
    extension = path.suffix.lstrip(".").lower()
    return binary_document_to_markdown(path.read_bytes(), extension)
