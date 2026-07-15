from datetime import timedelta

from app.utils.datetime_utils import utc_now

from sqlalchemy.orm import Session

from app.utils.otp import generate_otp
from app.verification.models import VerificationCode
from app.constants.verification_types import EMAIL_VERIFICATION
from app.constants.verification_types import MOBILE_VERIFICATION
from app.users.models.user import User
from app.exceptions.custom_exceptions import (
    InvalidCredentialsException
)
from app.exceptions.custom_exceptions import (
    InvalidOTPException,
    ExpiredOTPException,
    OTPAlreadyUsedException
)

def create_email_verification_otp(
    db: Session,
    user_id: int
):
    db.query(VerificationCode).filter(
        VerificationCode.user_id == user_id,
        VerificationCode.verification_type == EMAIL_VERIFICATION,
        VerificationCode.is_used == False
    ).update(
        {
            "is_used": True
        }
    )

    db.commit()
    
    otp = generate_otp()

    verification = VerificationCode(
        user_id=user_id,
        verification_type=EMAIL_VERIFICATION,
        code=otp,
        expires_at=utc_now() + timedelta(minutes=10),
        is_used=False
    )

    db.add(verification)

    db.commit()

    db.refresh(verification)

    return otp

def verify_email_otp(
    db: Session,
    user_id: int,
    otp: str
):

    verification = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.user_id == user_id,
            VerificationCode.verification_type == EMAIL_VERIFICATION
        )
        .order_by(VerificationCode.created_at.desc())
        .first()
    )

    if verification is None:
        raise InvalidOTPException()

    if verification.is_used:
        raise OTPAlreadyUsedException()

    if verification.code != otp:
        raise InvalidOTPException()

    if verification.expires_at < utc_now():
        raise ExpiredOTPException()

    verification.is_used = True

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    user.email_verified = True

    db.commit()

    return {
        "message": "Email verified successfully."
    }



def create_mobile_verification_otp(
    db: Session,
    user_id: int
):

    db.query(VerificationCode).filter(
        VerificationCode.user_id == user_id,
        VerificationCode.verification_type == MOBILE_VERIFICATION,
        VerificationCode.is_used == False
    ).update(
        {
            "is_used": True
        }
    )

    db.commit()

    otp = generate_otp()

    verification = VerificationCode(
        user_id=user_id,
        verification_type=MOBILE_VERIFICATION,
        code=otp,
        expires_at=utc_now() + timedelta(minutes=10),
        is_used=False
    )

    db.add(verification)

    db.commit()

    db.refresh(verification)

    return otp

def verify_mobile_otp(
    db: Session,
    user_id: int,
    otp: str
):

    verification = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.user_id == user_id,
            VerificationCode.verification_type == MOBILE_VERIFICATION
        )
        .order_by(VerificationCode.created_at.desc())
        .first()
    )

    if verification is None:
        raise InvalidOTPException()

    if verification.is_used:
        raise OTPAlreadyUsedException()

    if verification.code != otp:
        raise InvalidOTPException()

    if verification.expires_at < utc_now():
        raise ExpiredOTPException()

    verification.is_used = True

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    user.mobile_verified = True

    if user.email_verified:
        user.account_status = "Active"

    db.commit()

    return {
        "message": "Mobile verified successfully."
    }