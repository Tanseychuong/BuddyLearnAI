from fastapi import APIRouter
from pydantic import BaseModel, Field

# initializing the router for the recommendation module
router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


#class for recommendation request
class RecommendationRequest(BaseModel):
    course_id: int
    target_exam_date: str | None = Field(default=None, examples=["2026-12-10"])


# class for recommendation structuring
class Recommendation(BaseModel):
    priority: int
    title: str
    reason: str


# class for returning the recommmendations
class RecommendationResponse(BaseModel):
    course_id: int
    recommendations: list[Recommendation]

# class for posting the recommentation
@router.post("", response_model=RecommendationResponse)
def recommend_next_steps(payload: RecommendationRequest) -> RecommendationResponse:
    return RecommendationResponse(
        course_id=payload.course_id,
        recommendations=[
            Recommendation(
                priority=1,
                title="Upload course materials",
                reason="Recommendations become personalized after document processing and quiz results exist.",
            )
        ],
    )
