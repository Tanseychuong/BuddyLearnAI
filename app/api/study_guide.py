from pydantic import BaseModel, Field
from fastapi import APIRouter


router = APIRouter(prefix="/study-guides", tags=["Study Guides"])


class StudyGuideRequest(BaseModel):
    course_id: int
    topic: str | None = Field(default=None, max_length=160)


class StudyGuideResponse(BaseModel):
    course_id: int
    title: str
    sections: list[str]
    status: str


@router.post("/generate", response_model=StudyGuideResponse)
def generate_study_guide(payload: StudyGuideRequest) -> StudyGuideResponse:
    title = payload.topic or "Course Study Guide"
    return StudyGuideResponse(
        course_id=payload.course_id,
        title=title,
        sections=[
            "Chapter summaries",
            "Key concepts",
            "Important definitions",
            "Examples",
            "Exam tips",
        ],
        status="draft_generated",
    )
