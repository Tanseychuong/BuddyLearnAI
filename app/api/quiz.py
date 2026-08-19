# This file contains the API endpoints for generating quizzes based on a given course and difficulty level.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories import course_repository
from app.schemas import QuizGenerateRequest, QuizGenerateResponse
from app.services.generation import GenerationError, generate_quiz_questions
from app.services.retrieval import get_course_context
from app.services.vector_store import VectorStoreError
from app.services.embeddings import EmbeddingError

# initializing the router for quiz module
router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


# This is a class for the quiz generator that connects the router to the RAG pipeline:
# retrieve relevant course material chunks from Qdrant, then generate grounded
# questions from them with Gemini.
@router.post("/generate", response_model=QuizGenerateResponse)

# This function generates a quiz based on the provided request payload, which includes course ID, difficulty level, question types, and question count. It retrieves the relevant course material chunks and generates questions accordingly.
def generate_quiz(
    payload: QuizGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> QuizGenerateResponse:
    course = course_repository.get_for_owner(
        db, course_id=payload.course_id, owner_id=current_user.id
    )
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    query = (
        f"Key concepts, definitions, and important facts suitable for a "
        f"{payload.difficulty} difficulty quiz."
    )

    try:
        context_chunks = get_course_context(payload.course_id, query)
    except (VectorStoreError, EmbeddingError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)
        ) from exc

    if not context_chunks:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No processed material found for this course. Upload material and "
            "wait for it to finish processing before generating a quiz.",
        )

    try:
        questions = generate_quiz_questions(
            context_chunks=context_chunks,
            question_types=payload.question_types,
            difficulty=payload.difficulty,
            question_count=payload.question_count,
        )
    except GenerationError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return QuizGenerateResponse(
        course_id=payload.course_id,
        difficulty=payload.difficulty,
        questions=questions,
    )