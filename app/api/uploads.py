# importing the important modules and libraries for the development of the uploads helper modules
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, UploadFile, status
from pydantic import BaseModel

from app.core.config import get_settings

# initializing router for the uploads modules
router = APIRouter(prefix="/uploads", tags=["Document Processing"])

# UploadResponse model to represent the response after uploading a file
class UploadResponse(BaseModel):
    id: str
    course_id: int
    filename: str
    content_type: str | None
    status: str

# Endpoint to handle file uploads
@router.post("", response_model=UploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_material(
    course_id: int = Form(...),
    file: UploadFile = File(...),
) -> UploadResponse:
    settings = get_settings()
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    material_id = str(uuid4())
    safe_name = Path(file.filename or "material").name
    destination = upload_dir / f"{material_id}-{safe_name}"
    destination.write_bytes(await file.read())
# return the response with the uploaded file details
    return UploadResponse(
        id=material_id,
        course_id=course_id,
        filename=safe_name,
        content_type=file.content_type,
        status="queued_for_processing",
    )
