import logging
from app.services.vector_store import VectorStoreError, search_similar_chunks

logger = logging.getLogger(__name__)


def get_course_context(course_id: int, query: str, top_k: int = 5) -> list[str]:
    """Retrieve relevant context text chunks from Qdrant vector store for a given course query."""
    try:
        results = search_similar_chunks(course_id=course_id, query=query, top_k=top_k)
        return [res.get("text", "") for res in results if res.get("text")]
    except VectorStoreError as exc:
        logger.warning(f"Vector store retrieval failed for course {course_id}: {exc}")
        return []
