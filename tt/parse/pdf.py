from pathlib import Path
import fitz  # PyMuPDF


def extract_text(path: str | Path) -> tuple[str, list[int]]:
    """Return (text, pages_without_text_layer). OCR is a later fallback; here we only flag."""
    pages, empty = [], []
    with fitz.open(path) as doc:
        for i, p in enumerate(doc):
            t = p.get_text("text")
            if len(t.strip()) < 20:
                empty.append(i)
            pages.append(t)
    return "\n".join(pages), empty
