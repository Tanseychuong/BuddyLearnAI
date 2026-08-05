# importing the important modules and libraries for the development of the uploads helper modules
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.core.database import get_db
from app.models.user import User
from app.repositories import course_repository, material_repository
from app.schemas import MaterialRead
from app.workers.tasks import process_material_task

logger = logging.getLogger(__name__)

# initializing router for the uploads modules
router = APIRouter(prefix="/uploads", tags=["Document Processing"])


# Endpoint to handle file uploads
@router.post("", response_model=MaterialRead, status_code=status.HTTP_202_ACCEPTED)
async def upload_material(
    course_id: int = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MaterialRead:
    course = course_repository.get_for_owner(db, course_id=course_id, owner_id=current_user.id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    settings = get_settings()
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    material_id = str(uuid4())
    safe_name = Path(file.filename or "material").name
    destination = upload_dir / f"{material_id}-{safe_name}"
    destination.write_bytes(await file.read())

    material = material_repository.create(
        db,
        material_id=material_id,
        course_id=course_id,
        filename=safe_name,
        content_type=file.content_type,
        storage_path=str(destination),
    )

    try:
        process_material_task.delay(material.id)
    except Exception:
        # Broker (Redis) unreachable in this environment — the material stays
        # "queued_for_processing" and can be picked up once the worker/broker
        # are running, e.g. via `docker-compose up -d redis` and a Celery worker.
        logger.warning(
            "Could not enqueue processing for material %s (broker unreachable).",
            material.id,
        )

    return MaterialRead.model_validate(material)