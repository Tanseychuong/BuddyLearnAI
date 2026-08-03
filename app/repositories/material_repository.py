from sqlalchemy.orm import Session

from app.models.material import Material, MaterialStatus


def create(
    db: Session,
    *,
    material_id: str,
    course_id: int,
    filename: str,
    content_type: str | None,
    storage_path: str,
) -> Material:
    material = Material(
        id=material_id,
        course_id=course_id,
        filename=filename,
        content_type=content_type,
        storage_path=storage_path,
        status=MaterialStatus.QUEUED,
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material