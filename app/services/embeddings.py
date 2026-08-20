"""Generate text embeddings via the Gemini API.

Uses Google's free-tier-friendly Gemini embedding model instead of OpenAI.
Get a key at https://aistudio.google.com/apikey and set it as
BUDDYLEARN_GEMINI_API_KEY in your .env.
"""

from google import genai
from google.genai import types

from app.core.config import get_settings

# Constants for the Gemini embedding model and its configuration. The model name, embedding dimensions, and maximum batch size for embedding requests are defined here.
EMBEDDING_MODEL = "gemini-embedding-001"
# Gemini embeddings support flexible output size via Matryoshka Representation
# Learning (up to 3072). 768 keeps Qdrant storage/latency small while still
# being one of Google's recommended dimensions.
EMBEDDING_DIMENSIONS = 768

# The Gemini API caps embed_content batches; chunk larger material sets
# into batches of this size before sending.
MAX_BATCH_SIZE = 100

# Define a custom exception class for embedding-related errors. This allows for more specific error handling in the embedding functions.

class EmbeddingError(Exception):
    """Raised when embeddings cannot be generated."""

# Define a function to create and return a Gemini API client. It retrieves the API key from the application settings and raises an EmbeddingError if the key is not set.
def _client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise EmbeddingError(
            "BUDDYLEARN_GEMINI_API_KEY is not set. Add it to your .env to enable "
            "embeddings (get a free key at https://aistudio.google.com/apikey)."
        )
    return genai.Client(api_key=settings.gemini_api_key)

# Defining the _embed_batch function to embed a batch of texts using the Gemini API. It handles exceptions and returns a list of embeddings for the input texts.

def _embed_batch(
    client: genai.Client, texts: list[str], task_type: str
) -> list[list[float]]:
    try:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texts,
            config=types.EmbedContentConfig(
                output_dimensionality=EMBEDDING_DIMENSIONS,
                task_type=task_type,
            ),
        )
    except Exception as exc:
        raise EmbeddingError(f"Embedding request failed: {exc}") from exc

    return [embedding.values for embedding in response.embeddings]

# Defining the embed_texts function to embed material chunks for storage/indexing. It processes texts in batches to respect the Gemini API's batch size limit and uses a specific task_type for document embeddings.

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed material chunks for storage/indexing."""
    if not texts:
        return []

    client = _client()
    embeddings: list[list[float]] = []
    for i in range(0, len(texts), MAX_BATCH_SIZE):
        batch = texts[i : i + MAX_BATCH_SIZE]
        embeddings.extend(_embed_batch(client, batch, task_type="RETRIEVAL_DOCUMENT"))

    return embeddings


# Defining the embed query function to embed a search query for retrieval against stored chunks. It uses a different task_type than embed_texts, as Gemini optimizes query and document embeddings differently for retrieval quality. 

def embed_query(text: str) -> list[float]:
    """Embed a search query for retrieval against stored chunks.

    Uses a different task_type than embed_texts — Gemini optimizes query
    and document embeddings differently for retrieval quality.
    """
    return _embed_batch(_client(), [text], task_type="RETRIEVAL_QUERY")[0]