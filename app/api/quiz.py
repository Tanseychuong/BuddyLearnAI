from typing import Literal

from pydantic import BaseModel, Field
from fastapi import APIRouter

# initializing the router for quiz module
router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


QuestionType = Literal["mcq", "true_false", "fill_blank", "short_answer", "essay"]
Difficulty = Literal["easy", "medium", "hard", "mixed"]

# class for quiz generation request
class QuizGenerateRequest(BaseModel):
    course_id: int
    question_types: list[QuestionType] = Field(default_factory=lambda: ["mcq"])
    difficulty: Difficulty = "mixed"
    question_count: int = Field(default=10, ge=1, le=50)


# class that take in the user prompt as a question
class QuizQuestion(BaseModel):
    prompt: str
    type: QuestionType
    options: list[str] = Field(default_factory=list)
    answer: str


# Class for generating the quiz
class QuizGenerateResponse(BaseModel):
    course_id: int
    difficulty: Difficulty
    questions: list[QuizQuestion]

# This is a class for the quiz generator that connect the  the base class to the app router
@router.post("/generate", response_model=QuizGenerateResponse)
def generate_quiz(payload: QuizGenerateRequest) -> QuizGenerateResponse:
    question_type = payload.question_types[0]
    return QuizGenerateResponse(
        course_id=payload.course_id,
        difficulty=payload.difficulty,
        questions=[
            QuizQuestion(
                prompt="Sample generated question awaiting AI content pipeline.",
                type=question_type,
                options=["A", "B", "C", "D"] if question_type == "mcq" else [],
                answer="Generated answer placeholder",
            )
        ],
    )
