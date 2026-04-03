# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e .

# Run MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

This is a **FastMCP server** that exposes Python functions as tools to AI assistants via the [Model Context Protocol](https://modelcontextprotocol.io/).

**Registration flow:** `main.py` creates a `FastMCP("docs")` instance and registers tools by calling `mcp.tool()(function)`. Each registered function becomes an MCP tool with a JSON schema auto-generated from its type hints and Pydantic `Field` descriptions.

**Adding a new tool:**
1. Define the function in `tools/<domain>.py` using `Field` for parameter descriptions
2. Import it in `main.py` and register with `mcp.tool()(your_function)`

**Tool definition pattern:**
```python
from pydantic import Field

def my_tool(
    param: str = Field(description="Detailed description"),
) -> str:
    """One-line summary.

    Detailed explanation of functionality.

    When to use:
    - Use case A
    - Not for use case B

    Examples:
    >>> my_tool("input")
    "output"
    """
    ...
```

**Current tools:**
- `tools/math.py` — `add()`: registered in `main.py`, serves as the canonical example
- `tools/document.py` — `binary_document_to_markdown()`: converts binary DOCX/PDF to markdown via `markitdown`; defined but **not yet registered** in `main.py`

## Code Standards

- Always apply appropriate types annotations to all function arguments and return values.

## Notes

- `uv run` respects `uv.lock`. If a locked dependency is incompatible with the active Python version (e.g., `onnxruntime` on Python 3.14), run `uv lock --upgrade-package <package>` before `uv run`.
- Tests use real fixture files in `tests/fixtures/` (`.docx`, `.pdf`) — no mocking of document conversion.
