from sqlalchemy.orm import Session

from app.models.material import Material, MaterialStatus


def get_by_id(db: Session, material_id: str) -> Material | None:
    return db.get(Material, material_id)


def update_status(db: Session, material_id: str, status: str) -> Material | None:
    material = db.get(Material, material_id)
    if not material:
        return None
    material.status = status
    db.commit()
    db.refresh(material)
    return material


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