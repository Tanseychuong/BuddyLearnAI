from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories import course_repository
from app.schemas import CourseCreate, CourseRead

router = APIRouter(prefix="/courses", tags=["Courses"])


# list courses router for the fast api
@router.get("", response_model=list[CourseRead])
def list_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[CourseRead]:
    rows = course_repository.list_for_owner(db, owner_id=current_user.id)
    return [
        CourseRead(
            id=course.id,
            code=course.code,
            title=course.title,
            description=course.description,
            material_count=count,
        )
        for course, count in rows
    ]


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(
    payload: CourseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CourseRead:
    course = course_repository.create(
        db,
        owner_id=current_user.id,
        code=payload.code,
        title=payload.title,
        description=payload.description,
    )
    return CourseRead(
        id=course.id,
        code=course.code,
        title=course.title,
        description=course.description,
        material_count=0,
    )