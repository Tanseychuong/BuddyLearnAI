from pydantic import BaseModel, EmailStr
from fastapi import APIRouter


router = APIRouter(prefix="/users", tags=["Users"])


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    study_streak_days: int


@router.get("/me", response_model=UserProfile)
def get_current_user_profile() -> UserProfile:
    return UserProfile(
        id=1,
        email="student@example.com",
        full_name="Demo Student",
        study_streak_days=0,
    )
