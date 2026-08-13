"""Retrieve relevant material chunks for a course from Qdrant.

This is the "R" in RAG: given a course and a natural-language query
describing what's needed (e.g. "key concepts for a quiz"), fetch the most
semantically relevant chunks previously stored by the document-processing
pipeline (see app/workers/tasks.py).
"""

from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.services.embeddings import embed_query
from app.services.vector_store import COLLECTION_NAME, VectorStoreError, get_qdrant_client

DEFAULT_TOP_K = 15


def get_course_context(course_id: int, query: str, top_k: int = DEFAULT_TOP_K) -> list[str]:
    """Return the top-k chunk texts for a course most relevant to `query`.

    Returns an empty list if the course has no processed material yet
    (rather than raising) — callers should treat that as "nothing to
    generate from" and surface a clear message to the user.
    """
    client = get_qdrant_client()

    try:
        if not client.collection_exists(COLLECTION_NAME):
            return []
    except Exception as exc:
        raise VectorStoreError(f"Could not reach Qdrant: {exc}") from exc

    query_vector = embed_query(query)  # raises EmbeddingError on failure, not caught here

    try:
        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter=Filter(
                must=[FieldCondition(key="course_id", match=MatchValue(value=course_id))]
            ),
            limit=top_k,
        )
    except Exception as exc:
        raise VectorStoreError(f"Could not retrieve course context from Qdrant: {exc}") from exc

    return [point.payload["text"] for point in results.points if point.payload]