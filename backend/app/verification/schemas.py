from pydantic import BaseModel, Field


class VerifyOTP(BaseModel):

    otp: str = Field(..., min_length=6, max_length=6)