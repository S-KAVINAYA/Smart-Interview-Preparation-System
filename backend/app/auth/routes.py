from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.schemas import UserSignup
from app.auth.service import create_user
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
    try:
        new_user = create_user(db, user)

        return {
            "message": "User registered successfully.",
            "user_id": new_user.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )