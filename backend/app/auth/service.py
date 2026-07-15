from sqlalchemy.orm import Session

from app.auth.schemas import UserSignup
from app.auth.security import hash_password
from app.users.models.user import User

from app.exceptions.custom_exceptions import (
    EmailAlreadyExistsException,
    MobileAlreadyExistsException,
    InvalidCredentialsException
)

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.auth.schemas import ForgotPasswordRequest
from app.constants.verification_types import PASSWORD_RESET
from app.verification.models import VerificationCode
from app.utils.otp import generate_otp
from app.utils.datetime_utils import utc_now
from datetime import timedelta

from app.auth.schemas import ResetPasswordRequest

from app.exceptions.custom_exceptions import (
    InvalidOTPException,
    ExpiredOTPException,
    OTPAlreadyUsedException
)

from app.constants.delivery_methods import (
    EMAIL,
    MOBILE
)

def create_user(db: Session, user: UserSignup):

    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:
        raise EmailAlreadyExistsException()

    existing_mobile = db.query(User).filter(
        User.mobile_number == user.mobile_number
    ).first()

    if existing_mobile:
        raise MobileAlreadyExistsException()

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        mobile_number=user.mobile_number,
        password_hash=hash_password(user.password),
        career_stage_id=user.career_stage_id
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

def login_user(db: Session, email: str, password: str):

    
    print("Email received:", email)

    user = db.query(User).filter(
        User.email == email
    ).first()

    print("User found:", user)

    if not user:
        raise InvalidCredentialsException()

    print("Password entered:", password)
    print("Stored hash:", user.password_hash if user else None)

    if not verify_password(
        password,
        user.password_hash
    ):
        raise InvalidCredentialsException()

    token = create_access_token(
        {
            "sub": user.email,
            "user_id": user.id,
            "career_stage_id": user.career_stage_id,
            "login_provider": user.login_provider
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def forgot_password(
    db: Session,
    request: ForgotPasswordRequest
):

    if request.email:

        user = db.query(User).filter(
            User.email == request.email
        ).first()

    else:

        user = db.query(User).filter(
            User.mobile_number == request.mobile_number
        ).first()

    if not user:
        raise InvalidCredentialsException()

    db.query(VerificationCode).filter(
        VerificationCode.user_id == user.id,
        VerificationCode.verification_type == PASSWORD_RESET,
        VerificationCode.is_used == False
    ).update(
        {
            "is_used": True
        }
    )

    db.commit()

    otp = generate_otp()

    verification = VerificationCode(
        user_id=user.id,
        verification_type=PASSWORD_RESET,
        code=otp,
        expires_at=utc_now() + timedelta(minutes=10),
        is_used=False,
        delivery_method=EMAIL if request.email else MOBILE
    )

    db.add(verification)

    db.commit()

    db.refresh(verification)

    return {
        "message": "Password reset OTP generated successfully.",
        "otp": otp
    }

def reset_password(
    db: Session,
    request: ResetPasswordRequest
):

    if request.email:

        user = db.query(User).filter(
            User.email == request.email
        ).first()

    else:

        user = db.query(User).filter(
            User.mobile_number == request.mobile_number
        ).first()

    if not user:
        raise InvalidCredentialsException()

    verification = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.user_id == user.id,
            VerificationCode.verification_type == PASSWORD_RESET
        )
        .order_by(
            VerificationCode.created_at.desc()
        )
        .first()
    )

    if verification is None:
        raise InvalidOTPException()

    if verification.is_used:
        raise OTPAlreadyUsedException()

    if verification.code != request.otp:
        raise InvalidOTPException()

    if verification.expires_at < utc_now():
        raise ExpiredOTPException()

    user.password_hash = hash_password(
        request.new_password
    )

    verification.is_used = True

    db.commit()

    return {
        "message": "Password reset successfully."
    }