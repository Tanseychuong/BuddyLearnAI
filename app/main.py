import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.api import (
    auth,
    users,
    courses,
    uploads,
    quiz,
    flashcards,
    study_guide,
    exams,
    recommendations,
)

app = FastAPI(
    title="AI Learning Buddy API",
    version="1.0.0",
    description="AI-powered personalized learning platform.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(uploads.router)
app.include_router(quiz.router)
app.include_router(flashcards.router)
app.include_router(study_guide.router)
app.include_router(exams.router)
app.include_router(recommendations.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Learning Buddy API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
