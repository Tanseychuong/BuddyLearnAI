from typing import Literal

from pydantic import BaseModel, Field

QuestionType = Literal["mcq", "true_false", "fill_blank", "short_answer", "essay"]
Difficulty = Literal["easy", "medium", "hard", "mixed"]


class QuizGenerateRequest(BaseModel):
    course_id: int
    question_types: list[QuestionType] = Field(default_factory=lambda: ["mcq"])
    difficulty: Difficulty = "mixed"
    question_count: int = Field(default=10, ge=1, le=50)


class QuizQuestion(BaseModel):
    prompt: str
    type: QuestionType
    options: list[str] = Field(default_factory=list)
    answer: str


class QuizGenerateResponse(BaseModel):
    course_id: int
    difficulty: Difficulty
    questions: list[QuizQuestion]