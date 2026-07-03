from pydantic import BaseModel, Field
from fastapi import APIRouter


router = APIRouter(prefix="/exams", tags=["Exam Analysis"])


class ExamAnalysisRequest(BaseModel):
    course_id: int
    years: list[int] = Field(default_factory=list)


class TopicFrequency(BaseModel):
    topic: str
    frequency_percent: float


class ExamAnalysisResponse(BaseModel):
    course_id: int
    trends: list[TopicFrequency]
    status: str


@router.post("/analyze", response_model=ExamAnalysisResponse)
def analyze_exam_patterns(payload: ExamAnalysisRequest) -> ExamAnalysisResponse:
    return ExamAnalysisResponse(
        course_id=payload.course_id,
        trends=[],
        status="awaiting_exam_materials",
    )
