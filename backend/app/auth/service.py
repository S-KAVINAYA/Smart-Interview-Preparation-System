from sqlalchemy.orm import Session

from app.auth.schemas import UserSignup
from app.auth.security import hash_password
from app.users.models.user import User


def create_user(db: Session, user: UserSignup):

    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:
        raise Exception("Email already registered.")

    existing_mobile = db.query(User).filter(
        User.mobile_number == user.mobile_number
    ).first()

    if existing_mobile:
        raise Exception("Mobile number already registered.")

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