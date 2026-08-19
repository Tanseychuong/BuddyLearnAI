import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

# Importing necessary modules and routers for the FastAPI application
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

# Importing configuration and database modules
from app.core.config import get_settings
from app.core.database import Base, engine
from app import models  # noqa: F401  (registers model classes on Base.metadata)

# Initializing the base directory

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    if settings.environment == "development":
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("PostgreSQL database tables verified and created successfully.")
        except Exception as exc:
            logger.warning(
                "Could not connect to PostgreSQL on startup (%s). "
                "Ensure Docker container is running (`docker compose up -d postgres`). "
                "Serving static frontend pages.",
                exc
            )
    yield

# Defining the app info
app = FastAPI(
    title="AI Learning Buddy API",
    version="1.0.0",
    description="AI-powered personalized learning platform.",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)

# Adding CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including routers for different API endpoints
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(uploads.router)
app.include_router(quiz.router)
app.include_router(flashcards.router)
app.include_router(study_guide.router)
app.include_router(exams.router)
app.include_router(recommendations.router)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Defining the root endpoint and role-specific routes
@app.get("/")
async def root() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "student" / "index.html")

@app.get("/admin")
async def admin_dashboard() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "admin" / "dashboard.html")

@app.get("/admin/login")
async def admin_login() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "admin" / "login.html")

@app.get("/guidance")
async def guidance_dashboard() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "guidance" / "dashboard.html")

@app.get("/guidance/login")
async def guidance_login() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "guidance" / "login.html")

@app.get("/student")
async def student_dashboard() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "student" / "index.html")

@app.get("/student/login")
async def student_login() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "student" / "login.html")

# Defining a health check endpoint
@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}

# Running the app using Uvicorn when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)