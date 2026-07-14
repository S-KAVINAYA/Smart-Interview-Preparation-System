from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import UserSignup, UserLogin
from app.auth.service import create_user, login_user
from app.database.session import SessionLocal


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
    user: UserLogin,
    db: Session = Depends(get_db)
):

    return login_user(
        db,
        user.email,
        user.password
    )