from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator

class UserSignup(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)

    email: EmailStr

    mobile_number: str = Field(..., min_length=10, max_length=15)

    password: str = Field(..., min_length=8)

    career_stage_id: int


class UserLogin(BaseModel):
    email: EmailStr

    password: str

class ForgotPasswordRequest(BaseModel):

    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None

    @model_validator(mode="after")
    def validate_contact(self):

        if not self.email and not self.mobile_number:
            raise ValueError(
                "Either email or mobile number must be provided."
            )

        return self


class ResetPasswordRequest(BaseModel):

    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None

    otp: str = Field(
        ...,
        min_length=6,
        max_length=6
    )

    new_password: str = Field(
        ...,
        min_length=8
    )

    @model_validator(mode="after")
    def validate_contact(self):

        if not self.email and not self.mobile_number:
            raise ValueError(
                "Either email or mobile number must be provided."
            )

        return self