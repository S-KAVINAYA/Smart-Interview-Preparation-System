from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.security import get_current_user, get_db
from app.users.models.user import User

from app.verification.schemas import VerifyOTP
from app.verification.service import (
    create_email_verification_otp,
    verify_email_otp
)

router = APIRouter(
    prefix="/verification",
    tags=["Verification"]
)


@router.post("/send-email-otp")
def send_email_otp(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    otp = create_email_verification_otp(
        db,
        current_user.id
    )

    return {
        "message": "OTP generated successfully.",
        "otp": otp
    }

@router.post("/verify-email-otp")
def verify_email(
    request: VerifyOTP,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return verify_email_otp(
        db,
        current_user.id,
        request.otp
    )