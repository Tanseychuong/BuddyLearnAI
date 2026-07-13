'''
[=========================================================================================]
AppName: BuddyLearnAI

version: v1.0

Program dependencies: python 3.14.6

author: Chuong Tiutiu Nyang Mayian
[=========================================================================================]
'''

from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token, get_password_hash


router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> dict[str, str]:
    password_hash = get_password_hash(payload.password)
    return {
        "email": payload.email,
        "full_name": payload.full_name,
        "password_hash_preview": password_hash[:16],
        "status": "registered",
    }


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    if not payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(subject=payload.email))
