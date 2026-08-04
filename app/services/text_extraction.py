"""Extract raw text from uploaded course materials.

Supports PDFs (native text via PyMuPDF, falling back to OCR via Tesseract
for scanned/image-only pages) and plain text files. Add new content types
here as the platform grows to support them (docx, pptx, etc).
"""

from pathlib import Path

import fitz  # PyMuPDF
import pytesseract
from PIL import Image


class ExtractionError(Exception):
    """Raised when text cannot be extracted from a material."""


# Pages with fewer extractable characters than this are assumed to be
# scanned images and are routed through OCR instead.
MIN_CHARS_PER_PAGE_BEFORE_OCR = 20

# Render scanned pages at this zoom factor before OCR-ing them, to keep
# text legible for Tesseract without producing enormous images.
OCR_RENDER_ZOOM = 2.0


def _ocr_page(page: "fitz.Page") -> str:
    zoom_matrix = fitz.Matrix(OCR_RENDER_ZOOM, OCR_RENDER_ZOOM)
    pixmap = page.get_pixmap(matrix=zoom_matrix)
    image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    return pytesseract.image_to_string(image)


def extract_text_from_pdf(path: Path) -> str:
    pages: list[str] = []
    try:
        with fitz.open(path) as doc:
            for page in doc:
                native_text = page.get_text().strip()
                if len(native_text) >= MIN_CHARS_PER_PAGE_BEFORE_OCR:
                    pages.append(native_text)
                else:
                    pages.append(_ocr_page(page).strip())
    except Exception as exc:  # fitz raises its own exception types
        raise ExtractionError(f"Could not open or read PDF: {exc}") from exc

    text = "\n\n".join(p for p in pages if p)
    if not text.strip():
        raise ExtractionError("No extractable text found in PDF (all pages blank).")
    return text


def extract_text_from_plain_text(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise ExtractionError(f"Could not read text file: {exc}") from exc

    if not text.strip():
        raise ExtractionError("File is empty.")
    return text


def extract_text(path: Path, content_type: str | None) -> str:
    """Dispatch to the right extractor based on content type / extension."""
    suffix = path.suffix.lower()

    if content_type == "application/pdf" or suffix == ".pdf":
        return extract_text_from_pdf(path)

    if content_type in ("text/plain", "text/markdown") or suffix in (".txt", ".md"):
        return extract_text_from_plain_text(path)

    raise ExtractionError(
        f"Unsupported material type: content_type={content_type!r}, suffix={suffix!r}. "
        "Supported: PDF, .txt, .md."
    )