from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.material import Material


def list_for_owner(db: Session, owner_id: int) -> list[tuple[Course, int]]:
    stmt = (
        select(Course, func.count(Material.id))
        .outerjoin(Material, Material.course_id == Course.id)
        .where(Course.owner_id == owner_id)
        .group_by(Course.id)
        .order_by(Course.created_at.desc())
    )
    return list(db.execute(stmt).all())


def get_for_owner(db: Session, course_id: int, owner_id: int) -> Course | None:
    stmt = select(Course).where(Course.id == course_id, Course.owner_id == owner_id)
    return db.scalars(stmt).first()


def create(db: Session, *, owner_id: int, code: str, title: str, description: str | None) -> Course:
    course = Course(owner_id=owner_id, code=code, title=title, description=description)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def material_count(db: Session, course_id: int) -> int:
    stmt = select(func.count(Material.id)).where(Material.course_id == course_id)
    return db.scalar(stmt) or 0