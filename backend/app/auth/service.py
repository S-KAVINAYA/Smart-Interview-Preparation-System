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

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise InvalidCredentialsException()

    if not verify_password(
        password,
        user.password_hash
    ):
        raise InvalidCredentialsException()

    token = create_access_token(
        {
            "sub": user.email,
            "user_id": user.id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }