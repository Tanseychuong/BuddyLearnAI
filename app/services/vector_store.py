"""Thin wrapper around Qdrant for storing and retrieving material chunk embeddings."""

import uuid
from functools import lru_cache

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import get_settings
from app.services.embeddings import EMBEDDING_DIMENSIONS

COLLECTION_NAME = "material_chunks"

# Deterministic namespace so re-processing the same material/chunk always
# produces the same point ID (upsert overwrites rather than duplicating).
_POINT_ID_NAMESPACE = uuid.UUID("5e3f6b0a-9d1a-4a3e-8b7a-3f1e9a2b4c6d")


def _point_id(material_id: str, chunk_index: int) -> str:
    return str(uuid.uuid5(_POINT_ID_NAMESPACE, f"{material_id}:{chunk_index}"))


class VectorStoreError(Exception):
    """Raised when Qdrant is unreachable or a store operation fails."""


@lru_cache
def get_qdrant_client() -> QdrantClient:
    settings = get_settings()
    return QdrantClient(url=settings.qdrant_url)


def ensure_collection(client: QdrantClient | None = None) -> None:
    client = client or get_qdrant_client()
    try:
        if not client.collection_exists(COLLECTION_NAME):
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=EMBEDDING_DIMENSIONS, distance=Distance.COSINE),
            )
    except Exception as exc:
        raise VectorStoreError(f"Could not ensure Qdrant collection: {exc}") from exc


def store_chunks(
    *,
    material_id: str,
    course_id: int,
    chunks: list[str],
    embeddings: list[list[float]],
    client: QdrantClient | None = None,
) -> None:
    if len(chunks) != len(embeddings):
        raise VectorStoreError("chunks and embeddings must be the same length")
    if not chunks:
        return

    client = client or get_qdrant_client()
    ensure_collection(client)

    points = [
        PointStruct(
            id=_point_id(material_id, i),
            vector=embedding,
            payload={
                "material_id": material_id,
                "course_id": course_id,
                "chunk_index": i,
                "text": chunk,
            },
        )
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]

    try:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
    except Exception as exc:
        raise VectorStoreError(f"Could not upsert chunks into Qdrant: {exc}") from exc