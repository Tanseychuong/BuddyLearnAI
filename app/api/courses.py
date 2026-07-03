from pydantic import BaseModel, Field
from fastapi import APIRouter, status


router = APIRouter(prefix="/courses", tags=["Courses"])


class CourseCreate(BaseModel):
    code: str = Field(min_length=2, max_length=20, examples=["CS204"])
    title: str = Field(min_length=2, max_length=160, examples=["Data Structures"])
    description: str | None = None


class Course(CourseCreate):
    id: int
    material_count: int = 0


@router.get("", response_model=list[Course])
def list_courses() -> list[Course]:
    return []


@router.post("", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate) -> Course:
    return Course(id=1, **payload.model_dump())
