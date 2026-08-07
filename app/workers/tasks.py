import logging
from pathlib import Path

from app.core.database import SessionLocal
from app.models.material import MaterialStatus
from app.repositories import material_repository
from app.services.chunking import chunk_text
from app.services.embeddings import EmbeddingError, embed_texts
from app.services.text_extraction import ExtractionError, extract_text
from app.services.vector_store import VectorStoreError, store_chunks
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="process_material", bind=True, max_retries=2)
def process_material_task(self, material_id: str) -> None:
    """Extract, chunk, embed, and store a material's content in Qdrant.

    Runs as a background Celery task so the upload request can return
    immediately. Any failure marks the material as FAILED rather than
    leaving it stuck at "queued_for_processing" forever.
    """
    db = SessionLocal()
    try:
        material = material_repository.get_by_id(db, material_id)
        if not material:
            logger.warning("process_material_task: material %s not found", material_id)
            return

        material_repository.update_status(db, material_id, MaterialStatus.PROCESSING)

        text = extract_text(Path(material.storage_path), material.content_type)
        chunks = chunk_text(text)

        if not chunks:
            raise ExtractionError("Extraction produced no usable text chunks.")

        embeddings = embed_texts(chunks)
        store_chunks(
            material_id=material.id,
            course_id=material.course_id,
            chunks=chunks,
            embeddings=embeddings,
        )

        material_repository.update_status(db, material_id, MaterialStatus.PROCESSED)
        logger.info("Processed material %s into %d chunks", material_id, len(chunks))

    except (ExtractionError, EmbeddingError, VectorStoreError) as exc:
        logger.error("Failed to process material %s: %s", material_id, exc)
        material_repository.update_status(db, material_id, MaterialStatus.FAILED)
    except Exception as exc:  # unexpected error: retry a couple of times
        logger.exception("Unexpected error processing material %s", material_id)
        material_repository.update_status(db, material_id, MaterialStatus.FAILED)
        raise self.retry(exc=exc, countdown=30) from exc
    finally:
        db.close()