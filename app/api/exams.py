from pydantic import BaseModel, Field
from fastapi import APIRouter

# intializing the router for the exams analysis modules
router = APIRouter(prefix="/exams", tags=["Exam Analysis"])

#class exam analysis request
class ExamAnalysisRequest(BaseModel):
    course_id: int
    years: list[int] = Field(default_factory=list)


# class for the frequent topic analysis
class TopicFrequency(BaseModel):
    topic: str
    frequency_percent: float


# class for returning the response as per the analyzed exams
class ExamAnalysisResponse(BaseModel):
    course_id: int
    trends: list[TopicFrequency]
    status: str

# class for calling the post funtion to analyze the exams patterns.
@router.post("/analyze", response_model=ExamAnalysisResponse)
def analyze_exam_patterns(payload: ExamAnalysisRequest) -> ExamAnalysisResponse:
    return ExamAnalysisResponse(
        course_id=payload.course_id,
        trends=[],
        status="awaiting_exam_materials",
    )
