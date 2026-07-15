from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import UserSignup, UserLogin
from app.auth.service import create_user, login_user
from app.database.session import SessionLocal

from app.auth.security import get_current_user
from app.users.models.user import User

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(
    user: UserSignup,
    db: Session = Depends(get_db)
):
    new_user = create_user(db, user)

    return {
        "message": "User registered successfully.",
        "user_id": new_user.id
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(
        db,
        form_data.username,
        form_data.password
    )

@router.get("/me")
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "mobile_number": current_user.mobile_number,
        "career_stage_id": current_user.career_stage_id,
        "email_verified": current_user.email_verified,
        "mobile_verified": current_user.mobile_verified,
        "account_status": current_user.account_status
    }