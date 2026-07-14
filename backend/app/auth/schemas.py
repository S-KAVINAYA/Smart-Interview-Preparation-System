from pydantic import BaseModel, EmailStr, Field


class UserSignup(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)

    email: EmailStr

    mobile_number: str = Field(..., min_length=10, max_length=15)

    password: str = Field(..., min_length=8)

    career_stage_id: int


class UserLogin(BaseModel):
    email: EmailStr

    password: str