"""Generate text embeddings via the OpenAI API."""

from openai import OpenAI

from app.core.config import get_settings

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536


class EmbeddingError(Exception):
    """Raised when embeddings cannot be generated."""


def _client() -> OpenAI:
    settings = get_settings()
    if not settings.openai_api_key:
        raise EmbeddingError(
            "BUDDYLEARN_OPENAI_API_KEY is not set. Add it to your .env to enable embeddings."
        )
    return OpenAI(api_key=settings.openai_api_key)


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    try:
        response = _client().embeddings.create(model=EMBEDDING_MODEL, input=texts)
    except Exception as exc:
        raise EmbeddingError(f"Embedding request failed: {exc}") from exc

    return [item.embedding for item in response.data]