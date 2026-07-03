from pydantic import BaseModel, Field
from fastapi import APIRouter


router = APIRouter(prefix="/flashcards", tags=["Flashcards"])


class FlashcardGenerateRequest(BaseModel):
    course_id: int
    topic: str | None = Field(default=None, max_length=160)
    count: int = Field(default=20, ge=1, le=100)


class Flashcard(BaseModel):
    front: str
    back: str


class FlashcardGenerateResponse(BaseModel):
    course_id: int
    flashcards: list[Flashcard]


@router.post("/generate", response_model=FlashcardGenerateResponse)
def generate_flashcards(payload: FlashcardGenerateRequest) -> FlashcardGenerateResponse:
    topic = payload.topic or "uploaded material"
    return FlashcardGenerateResponse(
        course_id=payload.course_id,
        flashcards=[
            Flashcard(
                front=f"What should I review first in {topic}?",
                back="The recommendation engine will prioritize concepts from uploaded materials.",
            )
        ],
    )
