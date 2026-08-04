"""Split extracted text into overlapping chunks suitable for embedding.

Chunking is done on whitespace-normalized text, trying to break on
paragraph/sentence boundaries where possible so chunks read naturally
rather than cutting mid-word.
"""

import re

DEFAULT_CHUNK_SIZE = 1000  # characters
DEFAULT_CHUNK_OVERLAP = 150  # characters

_WHITESPACE_RE = re.compile(r"\s+")
_SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+")


def _normalize(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text).strip()


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and less than chunk_size")

    normalized = _normalize(text)
    if not normalized:
        return []

    sentences = _SENTENCE_BOUNDARY_RE.split(normalized)

    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        candidate = f"{current} {sentence}".strip() if current else sentence

        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.append(current)
            # Carry the tail of the previous chunk forward for context overlap.
            current = current[-overlap:] if overlap else ""
            candidate = f"{current} {sentence}".strip() if current else sentence

        # A single sentence longer than chunk_size: hard-split it.
        while len(candidate) > chunk_size:
            chunks.append(candidate[:chunk_size])
            candidate = candidate[chunk_size - overlap:]

        current = candidate

    if current:
        chunks.append(current)

    return chunks