import os
import pytest
from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self) -> None:
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_converts_docx_by_path(self) -> None:
        """Test that a DOCX file path is converted to markdown."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    def test_converts_pdf_by_path(self) -> None:
        """Test that a PDF file path is converted to markdown."""
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    def test_raises_file_not_found_for_missing_file(self) -> None:
        """Test that a missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown("/nonexistent/path/file.docx")

    def test_result_matches_binary_helper(self) -> None:
        """Test that path-based and binary-based conversion produce identical output."""
        with open(self.DOCX_FIXTURE, "rb") as f:
            binary_data = f.read()

        expected = binary_document_to_markdown(binary_data, "docx")
        actual = document_path_to_markdown(self.DOCX_FIXTURE)

        assert actual == expected
